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

#### TKE ####
def tke(u,v,w,lvl,scl,cc):
    nx=int(u.shape[1]/scl+1)
    ny=int(u.shape[2]/scl+1)
    out=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            uu=u[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
            uu=uu-np.mean(uu)

            vv=v[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
            vv=vv-np.mean(vv)

            ww=w[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
            ww=ww-np.mean(ww)

            cc2=np.mean(cc[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)])

            out[i,j]=cc2*.5*(np.mean(uu**2)+np.mean(vv**2)+np.mean(ww**2))
    return out

#### RUN IT ####

dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039


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

bigvars=['LOCLOUD_hmg','MDCLOUD_hmg','HICLOUD_hmg','LOCLOUD_het','MDCLOUD_het','HICLOUD_het',
         'MAXCAPE_hmg','MINCIN_hmg','LCL_hmg','LFC_hmg','MAXCAPE_het','MINCIN_het','LCL_het','LFC_het',
         'RAINNC_het','RAINNC_hmg','LWP_het','LWP_hmg',
         'HFX_het','HFX_hmg','LH_het','LH_hmg']

smvars=['MsKE_het','MsKE_hmg','HFX_60','VARHFX_het','LH_60','VARLH_het']

for day in days[rank::size]:
    print(day,flush=True)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()

    het_tke=np.zeros((N,snscl,wescl))
    hmg_tke=np.zeros((N,snscl,wescl))

    i=0
    for hr in hrs:
        print(hr,flush=True)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')

        #### TKE ####
        ut=wrf.getvar(fphet,'ua',meta=False)
        vt=wrf.getvar(fphet,'va',meta=False)
        wt=wrf.getvar(fphet,'wa',meta=False)
        ug=wrf.getvar(fphmg,'ua',meta=False)
        vg=wrf.getvar(fphmg,'va',meta=False)
        wg=wrf.getvar(fphmg,'wa',meta=False)

        zg=wrf.getvar(fphmg,'zstag',msl=False,meta=False)
        dz=zg[1:,:,:]-zg[:-1,:,:]
        p=wrf.getvar(fphmg,'pres',meta=False)
        qv=fphmg['QVAPOR'][0,:,:,:]
        T=wrf.getvar(fphmg,'tk',meta=False)
        rho=p/(287*(1+(.608*qv))*T)
        cg=rho*dz

        zt=wrf.getvar(fphet,'zstag',msl=False,meta=False)
        dz=zt[1:,:,:]-zt[:-1,:,:]
        p=wrf.getvar(fphet,'pres',meta=False)
        qv=fphmg['QVAPOR'][0,:,:,:]
        T=wrf.getvar(fphet,'tk',meta=False)
        rho=p/(287*(1+(.608*qv))*T)
        ct=rho*dz

        for lv in range(50):
            het_tke[i,:,:]=het_tke[i,:,:]+tke(ut,vt,wt,lv,scl,ct)
            hmg_tke[i,:,:]=hmg_tke[i,:,:]+tke(ug,vg,wg,lv,scl,cg)

        print(day+' TKE DONE',flush=True)
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
        fp.createDimension('we'+dimscln,wescl)
        fp.createDimension('sn'+dimscln,snscl)
    except Exception:
        pass


    #### FINISH OUTPUT SETUP ####
    try:
        fp.createVariable('time','i4',('time'))
        fp['time'][:]=list(range(49))
    except:
        pass

    for var in smvars:
        try:
            fp.createVariable(var,'f4',('time','sn'+dimscln, 'we'+dimscln))
        except Exception:
            pass
    for var in bigvars:
        try:
            fp.createVariable(var,'f4',('time','sn', 'we'))
        except Exception:
            pass
    fp['MsKE_het'][:]=het_tke[:]
    fp['MsKE_hmg'][:]=hmg_tke[:]

    fp.close()

