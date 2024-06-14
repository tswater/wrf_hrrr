import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import sys
import wrf

from mpi4py import MPI

# MPI4PY Stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

odir='/home/tsw35/tyche/wrf_gaea/'
gaea_dir='/home/tsw35/xTyc_shared/full_compress/'

#### USER INPUT ####
scl=20 #20=60km averaging scale

#### MESOSCALE FLUX ####
def ms_flx(w,s,conv,df=20):
    nx=int(w.shape[0]/df+1)
    ny=int(w.shape[1]/df+1)
    dout=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            w_=w[i*df:(i+1)*df,j*df:(j+1)*df]
            s_=s[i*df:(i+1)*df,j*df:(j+1)*df]
            wbar=np.nanmean(w_)
            sbar=np.nanmean(s_)
            try:
                conv_=np.nanmean(conv[i*df:(i+1)*df,j*df:(j+1)*df])
            except Exception as e:
                conv_=conv
            
            dout[i,j] = np.nanmean(conv_*np.nanmean((w_-wbar)*(s_-sbar)))
            # np.nanmean(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout

#### MEAN ####
def meani(data,df=20):
    nx=int(data.shape[0]/df+1)
    ny=int(data.shape[1]/df+1)
    dout=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            dout[i,j] = np.nanmean(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout




#### RUN IT ####

dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039
zlvl=50


# find all days
days=[]
for day in os.listdir(gaea_dir):
    if 'het' in day:
        continue
    day_=day[0:8]
    n1=len(os.listdir(gaea_dir+day_+'_het'))
    n2=len(os.listdir(gaea_dir+day_+'_hmg'))
    if (n1<48) or (n2<48):
        continue

    days.append(day_)


N=49

days.sort()


smvars=['Z_het','Z_hmg','MsHFX_het','MsHFX_hmg','MsLH_het','MsLH_hmg']

for day in days[rank::size]:
    print(day,flush=True)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()

    het_lh=np.zeros((N,zlvl,snscl,wescl))
    hmg_lh=np.zeros((N,zlvl,snscl,wescl))
    het_hfx=np.zeros((N,zlvl,snscl,wescl))
    hmg_hfx=np.zeros((N,zlvl,snscl,wescl))

    z_het=np.zeros((N,zlvl,snscl,wescl))
    z_hmg=np.zeros((N,zlvl,snscl,wescl))

    i=0
    for hr in hrs:
        print(hr,flush=True)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')

        #### FLUX ####
        wt=wrf.getvar(fphet,'wa',meta=False)
        wg=wrf.getvar(fphmg,'wa',meta=False)
        cp=1005
        Lv=2260000 

        # Homogeneous First
        p=wrf.getvar(fphmg,'pres',meta=False)
        qv=fphmg['QVAPOR'][0,:,:,:]
        theta=wrf.getvar(fphmg,'th',meta=False)
        T=wrf.getvar(fphmg,'tk',meta=False)
        rho=p/(287*(1+(.608*qv))*T)
        z=wrf.getvar(fphmg,'z',meta=False,msl=False)
        for zl in range(50):
            hmg_lh[i,zl,:,:]=ms_flx(wg[zl,:,:],qv[zl,:,:],rho[zl,:,:]*Lv)
            hmg_hfx[i,zl,:,:]=ms_flx(wg[zl,:,:],theta[zl,:,:],rho[zl,:,:]*cp)
            z_hmg[i,zl,:,:]=meani(z[zl,:,:])

        # Heterogeneous
        p=wrf.getvar(fphet,'pres',meta=False)
        qv=fphmg['QVAPOR'][0,:,:,:]
        theta=wrf.getvar(fphet,'th',meta=False)
        T=wrf.getvar(fphet,'tk',meta=False)
        rho=p/(287*(1+(.608*qv))*T)
        z=wrf.getvar(fphet,'z',meta=False,msl=False)
        for zl in range(50):
            het_lh[i,zl,:,:]=ms_flx(wt[zl,:,:],qv[zl,:,:],rho[zl,:,:]*Lv)
            het_hfx[i,zl,:,:]=ms_flx(wt[zl,:,:],theta[zl,:,:],rho[zl,:,:]*cp)
            z_het[i,zl,:,:]=meani(z[zl,:,:])


        print(day+' MsFLUX DONE',flush=True)
        fphet.close()
        fphmg.close()
        i=i+1

    #### CREATE OUTPUT ####
    try:
        fp=nc.Dataset(odir+day+'_conv.nc','r+')
    except Exception:
        fp=nc.Dataset(odir+day+'_conv.nc','w')
        fp.createDimension('we',1559)
        fp.createDimension('sn',1039)
        fp.createDimension('time',N)

    try:
        fp.createDimension('z',zlvl)
        fp.createDimension('we'+dimscln,wescl)
        fp.createDimension('sn'+dimscln,snscl)
    except Exception:
        pass


    #### FINISH OUTPUT SETUP ####
    for var in smvars:
        try:
            fp.createVariable(var,'f4',('time','z','sn'+dimscln, 'we'+dimscln))
        except Exception:
            pass
    fp['Z_het'][:]=z_het[:]
    fp['Z_hmg'][:]=z_hmg[:]
    fp['MsLH_het'][:]=het_lh[:]
    fp['MsLH_hmg'][:]=hmg_lh[:]
    fp['MsHFX_het'][:]=het_hfx[:]
    fp['MsHFX_hmg'][:]=hmg_hfx[:]

    fp.close()

