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

def a_v(full,scl=20):
    nx=int(full.shape[1]/scl+1)
    ny=int(full.shape[2]/scl+1)
    out1=np.zeros((full.shape[0],nx,ny))
    out2=np.zeros((full.shape[0],nx,ny))
    for lvl in range(zlvl):
        for i in range(nx):
            for j in range(ny):
                dd=full[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
                out1[lvl,i,j]=np.mean(dd)
                out2[lvl,i,j]=np.var(dd)
    return out1,out2

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

bigvars=['TKE_PBLCOL_het','TKE_PBLCOL_hmg','TKE_PBL_5_het','TKE_PBL_5_hmg']

smvars=['TKE_PBL_4D_het','TKE_PBL_4D_hmg','MsKE_4D_het','MsKE_4D_hmg',\
        'U_4D_het','U_4D_hmg','V_4D_het','V_4D_hmg','W_4D_het','W_4D_hmg',\
        'T_4D_het','T_4D_hmg','Q_4D_het','Q_4D_hmg','P_4D_het','P_4D_hmg',\
        'UUspatial_4D_het','UUspatial_4D_hmg','VVspatial_4D_het','VVspatial_4D_hmg',\
        'WWspatial_4D_het','WWspatial_4D_hmg','TTspatial_4D_het','TTspatial_4D_hmg',\
        'QQspatial_4D_het','QQspatial_4D_hmg']

for day in days[rank::size]:
    print(day,flush=True)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()

    het_pblc=np.zeros((N,sn,we))
    hmg_pblc=np.zeros((N,sn,we))
    het_pbl5=np.zeros((N,sn,we))
    hmg_pbl5=np.zeros((N,sn,we))

    het_pbl=np.zeros((N,zlvl,snscl,wescl))
    hmg_pbl=np.zeros((N,zlvl,snscl,wescl))
    het_mske=np.zeros((N,zlvl,snscl,wescl))
    hmg_mske=np.zeros((N,zlvl,snscl,wescl))
    het_UU=np.zeros((N,zlvl,snscl,wescl))
    hmg_UU=np.zeros((N,zlvl,snscl,wescl))
    het_VV=np.zeros((N,zlvl,snscl,wescl))
    hmg_VV=np.zeros((N,zlvl,snscl,wescl))
    het_WW=np.zeros((N,zlvl,snscl,wescl))
    hmg_WW=np.zeros((N,zlvl,snscl,wescl))
    het_QQ=np.zeros((N,zlvl,snscl,wescl))
    hmg_QQ=np.zeros((N,zlvl,snscl,wescl))
    het_PP=np.zeros((N,zlvl,snscl,wescl))
    hmg_PP=np.zeros((N,zlvl,snscl,wescl))
    het_TT=np.zeros((N,zlvl,snscl,wescl))
    hmg_TT=np.zeros((N,zlvl,snscl,wescl))
    het_U=np.zeros((N,zlvl,snscl,wescl))
    hmg_U=np.zeros((N,zlvl,snscl,wescl))
    het_V=np.zeros((N,zlvl,snscl,wescl))
    hmg_V=np.zeros((N,zlvl,snscl,wescl))
    het_W=np.zeros((N,zlvl,snscl,wescl))
    hmg_W=np.zeros((N,zlvl,snscl,wescl))
    het_Q=np.zeros((N,zlvl,snscl,wescl))
    hmg_Q=np.zeros((N,zlvl,snscl,wescl))
    het_P=np.zeros((N,zlvl,snscl,wescl))
    hmg_P=np.zeros((N,zlvl,snscl,wescl))
    het_T=np.zeros((N,zlvl,snscl,wescl))
    hmg_T=np.zeros((N,zlvl,snscl,wescl))

    i=0
    for hr in hrs:
        print(hr,flush=True)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')

        #### UVW ####
        ut=wrf.getvar(fphet,'ua',meta=False)
        vt=wrf.getvar(fphet,'va',meta=False)
        wt=wrf.getvar(fphet,'wa',meta=False)
        ug=wrf.getvar(fphmg,'ua',meta=False)
        vg=wrf.getvar(fphmg,'va',meta=False)
        wg=wrf.getvar(fphmg,'wa',meta=False)
        
        het_U[i,:,:,:],het_UU[i,:,:,:]=a_v(ut)
        hmg_U[i,:,:,:],hmg_UU[i,:,:,:]=a_v(ug)
        het_V[i,:,:,:],het_VV[i,:,:,:]=a_v(vt)
        hmg_V[i,:,:,:],hmg_VV[i,:,:,:]=a_v(vg)
        het_W[i,:,:,:],het_WW[i,:,:,:]=a_v(wt)
        hmg_W[i,:,:,:],hmg_WW[i,:,:,:]=a_v(wg)
        
        # HMG
        zg=wrf.getvar(fphmg,'zstag',msl=False,meta=False)
        dz=zg[1:,:,:]-zg[:-1,:,:]
        p=wrf.getvar(fphmg,'pres',meta=False)
        qv=fphmg['QVAPOR'][0,:,:,:]
        T=wrf.getvar(fphmg,'tk',meta=False)
        rho=p/(287*(1+(.608*qv))*T)
        cg=rho*dz
        
        hmg_T[i,:,:,:],hmg_TT[i,:,:,:]=a_v(T)
        hmg_Q[i,:,:,:],hmg_QQ[i,:,:,:]=a_v(qv)
        hmg_P[i,:,:,:],hmg_PP[i,:,:,:]=a_v(p)


        # HET
        zt=wrf.getvar(fphet,'zstag',msl=False,meta=False)
        dz=zt[1:,:,:]-zt[:-1,:,:]
        p=wrf.getvar(fphet,'pres',meta=False)
        qv=fphmg['QVAPOR'][0,:,:,:]
        T=wrf.getvar(fphet,'tk',meta=False)
        rho=p/(287*(1+(.608*qv))*T)
        ct=rho*dz
        
        het_T[i,:,:,:],het_TT[i,:,:,:]=a_v(T)
        het_Q[i,:,:,:],het_QQ[i,:,:,:]=a_v(qv)
        het_P[i,:,:,:],het_PP[i,:,:,:]=a_v(p)
        
        pblt=wrf.destagger(fphet['TKE_PBL'][0,:,:,:],0)
        pblg=wrf.destagger(fphmg['TKE_PBL'][0,:,:,:],0)

        het_pbl5[i,:,:]=pblt[5,:,:]
        hmg_pbl5[i,:,:]=pblg[5,:,:]
        het_pbl[i,:,:,:],_=a_v(pblt)
        hmg_pbl[i,:,:,:],_=a_v(pblg)
        
        print('ONLY NEED TO DO VERTICAL STUFF',flush=True)

        for lv in range(50):
            het_mske[i,lv,:,:]=tke(ut,vt,wt,lv,scl,ct)
            hmg_mske[i,lv,:,:]=tke(ug,vg,wg,lv,scl,cg)
            het_pblc[i,:,:]=het_pblc[i,:,:]+pblt[lv,:,:]*ct[lv,:,:]
            hmg_pblc[i,:,:]=hmg_pblc[i,:,:]+pblg[lv,:,:]*cg[lv,:,:]

        print(day+' TKE DONE',flush=True)
        fphet.close()
        fphmg.close()
        i=i+1

    #### CREATE OUTPUT ####
    print(day+': analysis done',flush=True)
    fp=nc.Dataset(odir+day+'_conv.nc','r+')

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
            fp.createVariable(var,'f4',('time','z','sn'+dimscln, 'we'+dimscln))
        except Exception:
            pass
    for var in bigvars:
        try:
            fp.createVariable(var,'f4',('time','sn', 'we'))
        except Exception:
            pass
    fp['TKE_PBLCOL_het'][:]=het_pblc[:]
    fp['TKE_PBLCOL_hmg'][:]=hmg_pblc[:]
    fp['TKE_PBL_5_het'][:]=het_pbl5[:]
    fp['TKE_PBL_5_hmg'][:]=hmg_pbl5[:]
    fp['TKE_PBL_4D_het'][:]=het_pbl[:]
    fp['TKE_PBL_4D_hmg'][:]=hmg_pbl[:]
    fp['MsKE_4D_het'][:]=het_mske[:]
    fp['MsKE_4D_hmg'][:]=hmg_mske[:]
    fp['U_4D_het'][:]=het_U[:]
    fp['U_4D_hmg'][:]=hmg_U[:]
    fp['V_4D_het'][:]=het_V[:]
    fp['V_4D_hmg'][:]=hmg_V[:]
    fp['W_4D_het'][:]=het_W[:]
    fp['W_4D_hmg'][:]=hmg_W[:]
    fp['T_4D_het'][:]=het_T[:]
    fp['T_4D_hmg'][:]=hmg_T[:]
    fp['Q_4D_het'][:]=het_Q[:]
    fp['Q_4D_hmg'][:]=hmg_Q[:]
    fp['P_4D_het'][:]=het_P[:]
    fp['P_4D_hmg'][:]=hmg_P[:]
    fp['UUspatial_4D_het'][:]=het_UU[:]
    fp['UUspatial_4D_hmg'][:]=hmg_UU[:]
    fp['VVspatial_4D_het'][:]=het_VV[:]
    fp['VVspatial_4D_hmg'][:]=hmg_VV[:]
    fp['WWspatial_4D_het'][:]=het_WW[:]
    fp['WWspatial_4D_hmg'][:]=hmg_WW[:]
    fp['TTspatial_4D_het'][:]=het_TT[:]
    fp['TTspatial_4D_hmg'][:]=hmg_TT[:]
    fp['QQspatial_4D_het'][:]=het_QQ[:]
    fp['QQspatial_4D_hmg'][:]=hmg_QQ[:]

    fp.close()
    print(day+': output complete',flush=True)

