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
delay=1

#### RUN IT ####
N=257
dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039

def databig(data):
    dout=np.zeros((49,1039,1559))
    for t in range (49):
        for i in range(data.shape[1]):
            for j in range(data.shape[2]):
                dout[t,i*20:(i+1)*20,j*20:(j+1)*20]=data[t,i,j]
    return dout


odir='/home/tsw35/tyche/wrf_gaea/'

flist=os.listdir(odir)
flist.sort()

fprt=nc.Dataset(odir+'all/raintime.nc','r')

rt=fprt['RAINTIME1_het'][:]
rg=fprt['RAINTIME1_hmg'][:]

dtemp={}

vars=['MsKE','MsKElo','HFX','LH','VARHFX','VARLH','LWP','RAINNC','LCL','LFC','LOCLOUD','MDCLOUD','HICLOUD','PW','RH2','T2']
data={}
for var in vars:
    data['g'+var+'_het']=np.ones((257,sn,we))*float('nan')
    data['g'+var+'_hmg']=np.ones((257,sn,we))*float('nan')
    data['gCOUNT']=np.zeros((sn,we))
    data['gCOUNT_tm']=np.zeros((N,))
    data['t'+var+'_het']=np.ones((257,sn,we))*float('nan')
    data['t'+var+'_hmg']=np.ones((257,sn,we))*float('nan')
    data['tCOUNT']=np.zeros((sn,we))
    data['tCOUNT_tm']=np.zeros((N,))
    
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
    
    mmt=np.zeros((49,sn,we),dtype='bool')
    mmg=np.zeros((49,sn,we),dtype='bool')
    for hr in range(6,49):
        mmg[hr-delay,:]=(rg[t,:]==hr)&(rt[t,:]>=hr)
        mmt[hr-delay,:]=(rt[t,:]==hr)&(rg[t,:]>=hr)
    for var in vars:
        print(var,flush=True)
        dgt=np.zeros((49,sn,we))
        dgg=np.zeros((49,sn,we))
        dtt=np.zeros((49,sn,we))
        dtg=np.zeros((49,sn,we))
        if ('MsKE' in var):
            dgt[mmg]=databig(fpin[var+'_het'][:])[mmg]
            dgg[mmg]=databig(fpin[var+'_hmg'][:])[mmg]
            dtt[mmt]=databig(fpin[var+'_het'][:])[mmt]
            dtg[mmt]=databig(fpin[var+'_hmg'][:])[mmt]
        elif ('VAR' in var):
            dgt[mmg]=databig(fpin[var+'_het'][:])[mmg]
            dtt[mmt]=databig(fpin[var+'_het'][:])[mmt]
        else:
            dgt[mmg]=fpin[var+'_het'][:][mmg]
            dgg[mmg]=fpin[var+'_hmg'][:][mmg]
            dtt[mmt]=fpin[var+'_het'][:][mmt]
            dtg[mmt]=fpin[var+'_hmg'][:][mmt]
        mg=np.sum(mmg,axis=0)
        mt=np.sum(mmt,axis=0)
        data['g'+var+'_het'][t,:][mg]=np.sum(dgt,axis=0)[mg]
        data['g'+var+'_hmg'][t,:][mg]=np.sum(dgg,axis=0)[mg]
        data['t'+var+'_het'][t,:][mt]=np.sum(dtt,axis=0)[mt]
        data['t'+var+'_hmg'][t,:][mt]=np.sum(dtg,axis=0)[mt]
        data['gCOUNT'][:]=data['gCOUNT'][:]+mg
        data['gCOUNT_tm'][t]=np.sum(mg)
        data['tCOUNT'][:]=data['tCOUNT'][:]+mt
        data['tCOUNT_tm'][t]=np.sum(mt)



    t=t+1
    

print('OUTPUT STARTIN')
#### CREATE OUTPUT ####
try:
    fp=nc.Dataset(odir+'all/prerain'+str(delay)+'.nc','r+')
except Exception:
    fp=nc.Dataset(odir+'all/prerain'+str(delay)+'.nc','w')
    fp.createDimension('we',1559)
    fp.createDimension('sn',1039)
    fp.createDimension('time',N)
    
try:
    fp.createDimension('we'+dimscln,wescl)
    fp.createDimension('sn'+dimscln,snscl)
except Exception:
    pass
    
    
#### FINISH OUTPUT SETUP ####
for var in data.keys():
    if 'tm' in var:
        try:
            fp.createVariable(var,'f4',('time'))
        except Exception:
            pass
    elif 'COUNT' in var:
        try:
            fp.createVariable(var,'f4',('sn','we'))
        except Exception:
            pass
    else:
        try:
            fp.createVariable(var,'f4',('time','sn','we'))
        except Exception:
            pass
    fp[var][:]=data[var][:]

fp.close()



