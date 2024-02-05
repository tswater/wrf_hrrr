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

gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/'


#### USER INPUT ####
scl=20 #20=60km averaging scale


#### MEANS AND VARIANCES ####
def vari(data,df=20):
    nx=int(data.shape[0]/df+1)
    ny=int(data.shape[1]/df+1)
    dout=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            dout[i,j] = np.nanvar(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout

def meani(data,df=20):
    nx=int(data.shape[0]/df+1)
    ny=int(data.shape[1]/df+1)
    dout=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            dout[i,j] = np.nanmean(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout

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

#days=['20230705']

for day in days[rank::size]:
    print(day,flush=True)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()

    het_tke=np.zeros((N,snscl,wescl))
    hmg_tke=np.zeros((N,snscl,wescl))
    cape2d_het=np.zeros((N,4,sn,we))
    clouds_het=np.zeros((N,3,sn,we))
    
    cape2d_hmg=np.zeros((N,4,sn,we))
    clouds_hmg=np.zeros((N,3,sn,we))

    
    het_hfx=np.zeros((N,sn,we))
    hmg_hfx=np.zeros((N,sn,we))
    hfx60=np.zeros((N,snscl,wescl))
    het_hfxv=np.zeros((N,snscl,wescl))
    
    het_lh=np.zeros((N,sn,we))
    hmg_lh=np.zeros((N,sn,we))
    lh60=np.zeros((N,snscl,wescl))
    het_lhv=np.zeros((N,snscl,wescl))

    het_r=np.zeros((N,sn,we))
    hmg_r=np.zeros((N,sn,we))
    het_lwp=np.zeros((N,sn,we))
    hmg_lwp=np.zeros((N,sn,we))

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
        pg=wrf.getvar(fphmg,'pres',meta=False)
        qvg=fphmg['QVAPOR'][0,:,:,:]
        Tg=wrf.getvar(fphmg,'tk',meta=False)
        rho=pg/(287*(1+(.608*qvg))*Tg)
        cg=rho*dz

        zt=wrf.getvar(fphet,'zstag',msl=False,meta=False)
        dz=zt[1:,:,:]-zt[:-1,:,:]
        pt=wrf.getvar(fphet,'pres',meta=False)
        qvt=fphmg['QVAPOR'][0,:,:,:]
        Tt=wrf.getvar(fphet,'tk',meta=False)
        rho=pt/(287*(1+(.608*qvt))*Tt)
        ct=rho*dz

        for lv in range(50):
            het_tke[i,:,:]=het_tke[i,:,:]+tke(ut,vt,wt,lv,scl,ct)
            hmg_tke[i,:,:]=hmg_tke[i,:,:]+tke(ug,vg,wg,lv,scl,cg)
        
        print(day+' TKE DONE',flush=True)

        #### LWP ####
        dpg=pg[1:,:,:]-pg[:-1,:,:]
        dpt=pt[1:,:,:]-pt[:-1,:,:]

        het_lwp[i,:,:]=np.sum(-dpt/9.81*fphet['QCLOUD'][0,:-1,:],axis=0)
        hmg_lwp[i,:,:]=np.sum(-dpg/9.81*fphmg['QCLOUD'][0,:-1,:],axis=0)
        
        print(day+' LWP DONE',flush=True)

        #### FLUXES ####
        het_hfx[i,:,:]=fphet['HFX'][0,:]
        hmg_hfx[i,:,:]=fphmg['HFX'][0,:]
        het_lh[i,:,:]=fphet['LH'][0,:]
        hmg_lh[i,:,:]=fphmg['LH'][0,:]
        
        het_r[i,:,:]=fphet['RAINNC'][0,:,:]
        hmg_r[i,:,:]=fphmg['RAINNC'][0,:,:]

        het_hfxv[i,:,:]=vari(het_hfx[i,:,:])
        hfx60[i,:,:]=meani(het_hfx[i,:,:])

        het_lhv[i,:,:]=vari(het_lh[i,:,:])
        lh60[i,:,:]=meani(het_lh[i,:,:])
        
        print(day+' FLUXES DONE',flush=True)

        #### WRF ####
        cape2d_het[i,:,:,:]=wrf.getvar(fphet,'cape2d',meta=False)
        clouds_het[i,:,:,:]=wrf.getvar(fphet,'cloudfrac',meta=False)

        cape2d_hmg[i,:,:,:]=wrf.getvar(fphmg,'cape2d',meta=False)
        clouds_hmg[i,:,:,:]=wrf.getvar(fphmg,'cloudfrac',meta=False)
        
        print(day+' WRF DONE',flush=True)
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


    
    #### OUTPUT DATA ####
    fp['MsKE_het'][:]=het_tke[:]
    fp['MsKE_hmg'][:]=hmg_tke[:]
    fp['LOCLOUD_hmg'][:]=clouds_hmg[:,0,:]
    fp['MDCLOUD_hmg'][:]=clouds_hmg[:,1,:]
    fp['HICLOUD_hmg'][:]=clouds_hmg[:,2,:]
    fp['LOCLOUD_het'][:]=clouds_het[:,0,:]
    fp['MDCLOUD_het'][:]=clouds_het[:,1,:]
    fp['HICLOUD_het'][:]=clouds_het[:,2,:]
    fp['MAXCAPE_hmg'][:]=cape2d_hmg[:,0,:]
    fp['MINCIN_hmg'][:]=cape2d_hmg[:,1,:]
    fp['LCL_hmg'][:]=cape2d_hmg[:,2,:]
    fp['LFC_hmg'][:]=cape2d_hmg[:,3,:]
    fp['MAXCAPE_het'][:]=cape2d_het[:,0,:]
    fp['MINCIN_het'][:]=cape2d_het[:,1,:]
    fp['LCL_het'][:]=cape2d_het[:,2,:]
    fp['LFC_het'][:]=cape2d_het[:,3,:]
    fp['LWP_hmg'][:]=hmg_lwp[:]
    fp['LWP_het'][:]=het_lwp[:]
    fp['HFX_hmg'][:]=hmg_hfx[:]
    fp['HFX_het'][:]=het_hfx[:]
    fp['HFX_60'][:]=hfx60[:]
    fp['VARHFX_het'][:]=het_hfxv
    fp['LH_hmg'][:]=hmg_lh[:]
    fp['LH_het'][:]=het_lh[:]
    fp['LH_60'][:]=lh60[:]
    fp['VARLH_het'][:]=het_lhv
    fp['RAINNC_hmg'][:]=hmg_r[:]
    fp['RAINNC_het'][:]=het_r[:]
    
    fp.close()



