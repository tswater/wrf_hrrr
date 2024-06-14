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
zlvl=50

v4dvars={}
statvars={}

fp=nc.Dataset(odir+'20210812_conv.nc','r')
for v in fp.variables:
    if '4D' in str(v):
        vv=str(v)
        v4dvars[vv]=float('nan')*np.ones((N,zlvl,snscl,wescl))
        if ('U_' in vv) or ('V_' in vv) or ('W_' in vv) or ('T_' in vv) or ('P_' in vv) or ('Q_' in vv) or ('MsKE_' in vv):
            statvars['daily_min_'+vv]=float('nan')*np.ones((N,zlvl,snscl,wescl))
            statvars['daily_max_'+vv]=float('nan')*np.ones((N,zlvl,snscl,wescl))
            statvars['daily_med_'+vv]=float('nan')*np.ones((N,zlvl,snscl,wescl))
            statvars['daily_std_'+vv]=float('nan')*np.ones((N,zlvl,snscl,wescl))
            
gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/'

flist=os.listdir(odir)
flist.sort()

print('Setup complete',flush=True)
print()
t=0
for file in flist:
    if file=='all':
        continue
    if file=='old':
        continue
    if file=='mswep_gaea':
        continue
    if file=='20210601_conv.nc':
        t=t+1
        continue
    if file=='20210602_conv.nc':
        t=t+1
        continue
    print(file,flush=True)
    fpin=nc.Dataset(odir+file,'r')
    
    for var in v4dvars.keys():
        v4dvars[var][t,:,:,:]=np.mean(fpin[var][24:48,:,:,:],axis=0)
    for var in statvars.keys():
        if 'min' in var:
            statvars[var][t,:,:,:]=np.min(fpin[var[10:]][24:48,:,:,:],axis=0)
        elif 'max' in var:
            statvars[var][t,:,:,:]=np.max(fpin[var[10:]][24:48,:,:,:],axis=0)
        elif 'med' in var:
            statvars[var][t,:,:,:]=np.median(fpin[var[10:]][24:48,:,:,:],axis=0)
        elif 'std' in var:
            statvars[var][t,:,:,:]=np.std(fpin[var[10:]][24:48,:,:,:],axis=0)

    t=t+1
print()
print('Processing done... Preparing to output',flush=True)

#### CREATE OUTPUT ####
try:
    fp=nc.Dataset(odir+'all/agg_4d.nc','r+')
except Exception:
    fp=nc.Dataset(odir+'all/agg_4d.nc','w')
    fp.createDimension('time',N)
    fp.createDimension('z',zlvl)
    
try:
    fp.createDimension('we'+dimscln,wescl)
    fp.createDimension('sn'+dimscln,snscl)
except Exception:
    pass
    
    
#### FINISH OUTPUT SETUP ####
for var in v4dvars.keys():
    try:
        fp.createVariable(var,'f4',('time','z','sn'+dimscln, 'we'+dimscln))
    except Exception:
        pass
    fp[var][:]=v4dvars[var][:]
    
#### FINISH OUTPUT SETUP ####
for var in statvars.keys():
    try:
        fp.createVariable(var,'f4',('time','z','sn'+dimscln, 'we'+dimscln))
    except Exception:
        pass
    fp[var][:]=statvars[var][:]

fp.close()



