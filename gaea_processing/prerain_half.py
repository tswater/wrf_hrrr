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
hmg=True

#### RUN IT ####
N=257
dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039

def databig(data):
    dout=np.zeros((1039,1559))
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            dout[i*20:(i+1)*20,j*20:(j+1)*20]=data[i,j]
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
    if hmg:
        data['g'+var+'_het']=np.ones((257,sn,we))*float('nan')
        data['g'+var+'_hmg']=np.ones((257,sn,we))*float('nan')
        data['gCOUNT']=np.zeros((sn,we))
        data['gCOUNT_tm']=np.zeros((N,))
    else:
        data['t'+var+'_het']=np.ones((257,sn,we))*float('nan')
        data['t'+var+'_hmg']=np.ones((257,sn,we))*float('nan')
        data['tCOUNT']=np.zeros((sn,we))
        data['tCOUNT_tm']=np.zeros((N,))
    
    dtemp['g'+var+'_het']=np.zeros((sn,we))
    dtemp['g'+var+'_hmg']=np.zeros((sn,we))
    dtemp['t'+var+'_het']=np.zeros((sn,we))
    dtemp['t'+var+'_hmg']=np.zeros((sn,we))


t=0
for file in [flist[0]]:
    if file=='all':
        continue
    if file=='old':
        continue
    if file=='mswep_gaea':
        continue
    print(file,flush=True)
    fpin=nc.Dataset(odir+file,'r')
    
    for var in vars:
        if hmg:
            dtemp['g'+var+'_het']=np.ones((sn,we))*-9999
            dtemp['g'+var+'_hmg']=np.ones((sn,we))*-9999
        else:
            dtemp['t'+var+'_het']=np.ones((sn,we))*-9999
            dtemp['t'+var+'_hmg']=np.ones((sn,we))*-9999

    for hr in range(6,49):
        mmg=(rg[t,:]==hr)&(rt[t,:]>=hr)
        mmt=(rt[t,:]==hr)&(rg[t,:]>=hr)
        
        for var in vars:
            if ('MsKE' in var):
                if hmg:
                    dtemp['g'+var+'_het'][mmg]=databig(fpin[var+'_het'][hr-delay,:])[mmg]
                    dtemp['g'+var+'_hmg'][mmg]=databig(fpin[var+'_hmg'][hr-delay,:])[mmg]
                else:
                    dtemp['t'+var+'_het'][mmt]=databig(fpin[var+'_het'][hr-delay,:])[mmt]
                    dtemp['t'+var+'_hmg'][mmt]=databig(fpin[var+'_hmg'][hr-delay,:])[mmt]
            elif ('VAR' in var):
                if hmg:
                    dtemp['g'+var+'_het'][mmg]=databig(fpin[var+'_het'][hr-delay,:])[mmg]
                else:
                    dtemp['t'+var+'_het'][mmt]=databig(fpin[var+'_het'][hr-delay,:])[mmt]
            else:
                if hmg:
                    dtemp['g'+var+'_het'][mmg]=fpin[var+'_het'][hr-delay,:][mmg]
                    dtemp['g'+var+'_hmg'][mmg]=fpin[var+'_hmg'][hr-delay,:][mmg]
                else:
                    dtemp['t'+var+'_het'][mmt]=fpin[var+'_het'][hr-delay,:][mmt]
                    dtemp['t'+var+'_hmg'][mmt]=fpin[var+'_hmg'][hr-delay,:][mmt]
    for var in vars:
        if hmg:
            mg=dtemp['g'+var+'_het'][:]!=-9999
        else:
            mt=dtemp['t'+var+'_het'][:]!=-9999
        if hmg:
            data['g'+var+'_het'][t,:][mg]=dtemp['g'+var+'_het'][mg]
            data['g'+var+'_hmg'][t,:][mg]=dtemp['g'+var+'_hmg'][mg]
            data['gCOUNT'][:]=data['gCOUNT'][:]+mg
            data['gCOUNT_tm'][t]=np.sum(mg)
        else:
            data['t'+var+'_het'][t,:][mt]=dtemp['t'+var+'_het'][mt]
            data['t'+var+'_hmg'][t,:][mt]=dtemp['t'+var+'_hmg'][mt]
            data['tCOUNT'][:]=data['tCOUNT'][:]+mt
            data['tCOUNT_tm'][t]=np.sum(mt)



    t=t+1
    

print('OUTPUT STARTIN')
#### CREATE OUTPUT ####
if hmg:
    name='hmg'
else:
    name='het'
try:
    fp=nc.Dataset(odir+'all/'+name+'prerain'+str(delay)+'.nc','r+')
except Exception:
    fp=nc.Dataset(odir+'all/'+name+'prerain'+str(delay)+'.nc','w')
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



