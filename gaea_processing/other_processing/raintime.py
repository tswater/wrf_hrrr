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


odir='/home/tsw35/tyche/wrf_gaea/'

flist=os.listdir(odir)
flist.sort()

rntime_het=np.ones((N,sn,we))*float('nan')
rntime_hmg=np.ones((N,sn,we))*float('nan')



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
    
    het_r=fpin['RAINNC_het'][:]
    hmg_r=fpin['RAINNC_hmg'][:]

    for hr in range(48,0,-1):
        rntime_het[t,:][het_r[hr,:]>1]=hr
        rntime_hmg[t,:][hmg_r[hr,:]>1]=hr

    t=t+1
    
#### CREATE OUTPUT ####
try:
    fp=nc.Dataset(odir+'all/raintime.nc','r+')
except Exception:
    fp=nc.Dataset(odir+'all/raintime.nc','w')
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
    fp.createVariable('RAINTIME1_het','f4',('time','sn', 'we'))
except Exception:
    pass

try:
    fp.createVariable('RAINTIME1_hmg','f4',('time','sn', 'we'))
except Exception:
    pass


    
#### OUTPUT DATA ####
fp['RAINTIME1_het'][:]=rntime_het[:]
fp['RAINTIME1_hmg'][:]=rntime_het[:]

fp.close()



