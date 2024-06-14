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
zz=50
dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039

smvars=['Z_het','Z_hmg','MsHFX_het','MsHFX_hmg','MsLH_het','MsLH_hmg']

gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/'

flist=os.listdir(odir)
flist.sort()

data={}
for var in smvars:
    data[var]=np.zeros((N,zz,snscl,wescl))

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
    
    for var in smvars:
        data[var][t,:,:,:]=np.mean(fpin[var][24:48,:,:,:],axis=0)

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
    fp.createDimension('z',zz)
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
    fp[var][:]=data[var][:]
#### OUTPUT DATA ####
    
fp.close()



