import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import sys
from datetime import datetime,timedelta

gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/'


#### USER INPUT ####
scl=20 #20=60km averaging scale


#### RUN IT ####
N=257
dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039


bigvars=['LOCLOUD_hmg','MDCLOUD_hmg','HICLOUD_hmg','LOCLOUD_het','MDCLOUD_het','HICLOUD_het',
         'LCL_hmg','LFC_hmg','LCL_het','LFC_het',
         'RAINNC_het','RAINNC_hmg','LWP_het','LWP_hmg',
         'HFX_het','HFX_hmg','LH_het','LH_hmg']

smvars=['MsKElo_het','MsKElo_hmg','MsKE_het','MsKE_hmg','HFX_60','VARHFX_het','LH_60','VARLH_het']

gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/'

flist=os.listdir(odir)
flist.sort()


het_tkelo=np.zeros((N,snscl,wescl))
hmg_tkelo=np.zeros((N,snscl,wescl))
het_tke=np.zeros((N,snscl,wescl))
hmg_tke=np.zeros((N,snscl,wescl))
cape2d_het=np.zeros((N,2,sn,we))
clouds_het=np.zeros((N,3,sn,we))

cape2d_hmg=np.zeros((N,2,sn,we))
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



time=np.zeros((N,))

t=0
for file in flist:
    if file=='all':
        continue
    if file=='old':
        continue
    if file=='mswep_gaea':
        continue
    print(file,flush=True)
    fpin=nc.Dataset(odir+file,'r')
    
    het_tke[t,:,:]=np.mean(fpin['MsKE_het'][24:48,:,:],axis=0)
    hmg_tke[t,:,:]=np.mean(fpin['MsKE_hmg'][24:48,:,:],axis=0)
    
    het_tkelo[t,:,:]=np.mean(fpin['MsKElo_het'][24:48,:,:],axis=0)
    hmg_tkelo[t,:,:]=np.mean(fpin['MsKElo_hmg'][24:48,:,:],axis=0)

    cape2d_het[t,0,:,:]=np.mean(fpin['LCL_het'][24:48,:,:],axis=0)
    cape2d_het[t,1,:,:]=np.mean(fpin['LFC_het'][24:48,:,:],axis=0)
    cape2d_hmg[t,0,:,:]=np.mean(fpin['LCL_hmg'][24:48,:,:],axis=0)
    cape2d_hmg[t,1,:,:]=np.mean(fpin['LFC_hmg'][24:48,:,:],axis=0)


    clouds_het[t,0,:,:]=np.mean(fpin['LOCLOUD_het'][24:48,:,:],axis=0)
    clouds_het[t,1,:,:]=np.mean(fpin['MDCLOUD_het'][24:48,:,:],axis=0)
    clouds_het[t,2,:,:]=np.mean(fpin['HICLOUD_het'][24:48,:,:],axis=0)

    clouds_hmg[t,0,:,:]=np.mean(fpin['LOCLOUD_hmg'][24:48,:,:],axis=0)
    clouds_hmg[t,1,:,:]=np.mean(fpin['MDCLOUD_hmg'][24:48,:,:],axis=0)
    clouds_hmg[t,2,:,:]=np.mean(fpin['HICLOUD_hmg'][24:48,:,:],axis=0)
    
    het_hfx[t,:,:]=np.mean(fpin['HFX_het'][24:48,:,:],axis=0)
    hmg_hfx[t,:,:]=np.mean(fpin['HFX_hmg'][24:48,:,:],axis=0)
    hfx60[t,:,:]=np.mean(fpin['HFX_60'][24:48,:,:],axis=0)
    het_hfxv[t,:,:]=np.mean(fpin['VARHFX_het'][24:48,:,:],axis=0)
    
    het_lh[t,:,:]=np.mean(fpin['LH_het'][24:48,:,:],axis=0)
    hmg_lh[t,:,:]=np.mean(fpin['LH_hmg'][24:48,:,:],axis=0)
    lh60[t,:,:]=np.mean(fpin['LH_60'][24:48,:,:],axis=0)
    het_lhv[t,:,:]=np.mean(fpin['VARLH_het'][24:48,:,:],axis=0)


    het_r[t,:,:]=fpin['RAINNC_het'][48,:,:]-fpin['RAINNC_het'][24,:,:]
    hmg_r[t,:,:]=fpin['RAINNC_hmg'][48,:,:]-fpin['RAINNC_hmg'][24,:,:]
    het_lwp[t,:,:]=np.mean(fpin['LWP_het'][24:48,:,:],axis=0)
    hmg_lwp[t,:,:]=np.mean(fpin['LWP_hmg'][24:48,:,:],axis=0)

    d0=datetime(2020,1,1,0)
    dt=datetime(int(file[0:4]),int(file[4:6]),int(file[6:8]),9)+timedelta(hours=24)
    time[t]=(dt-d0).total_seconds()

    t=t+1
    
#### CREATE OUTPUT ####
try:
    fp=nc.Dataset(odir+'all/agg_full.nc','r+')
except Exception:
    fp=nc.Dataset(odir+'all/agg_full.nc','w')
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
    fp.createVariable('seconds_from_2020','i4',('time'))
    fp['time'][:]=time[:]
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
fp['MsKElo_het'][:]=het_tkelo[:]
fp['MsKElo_hmg'][:]=hmg_tkelo[:]
fp['LOCLOUD_hmg'][:]=clouds_hmg[:,0,:]
fp['MDCLOUD_hmg'][:]=clouds_hmg[:,1,:]
fp['HICLOUD_hmg'][:]=clouds_hmg[:,2,:]
fp['LOCLOUD_het'][:]=clouds_het[:,0,:]
fp['MDCLOUD_het'][:]=clouds_het[:,1,:]
fp['HICLOUD_het'][:]=clouds_het[:,2,:]
fp['LCL_hmg'][:]=cape2d_hmg[:,0,:]
fp['LFC_hmg'][:]=cape2d_hmg[:,1,:]
fp['LCL_het'][:]=cape2d_het[:,0,:]
fp['LFC_het'][:]=cape2d_het[:,1,:]
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



