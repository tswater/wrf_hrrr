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
    dtemp['g'+var+'_het']=np.zeros((sn,we))
    dtemp['g'+var+'_hmg']=np.zeros((sn,we))
    dtemp['t'+var+'_het']=np.zeros((sn,we))
    dtemp['t'+var+'_hmg']=np.zeros((sn,we))


t=0
for file in flist:
    if file=='all':
        continue
    if file=='old':
        continue
    if file=='mswep_gaea':
        continue
    print(file,flush=True,end='')
    fpin=nc.Dataset(odir+file,'r')
    
    for var in vars:
        dtemp['g'+var+'_het']=np.ones((sn,we))*float('nan')
        dtemp['g'+var+'_hmg']=np.ones((sn,we))*float('nan')
        dtemp['t'+var+'_het']=np.ones((sn,we))*float('nan')
        dtemp['t'+var+'_hmg']=np.ones((sn,we))*float('nan')

    for hr in range(6,49):
        print('.',end='',flush=True)
        mmg=(rg[t,:]==hr)&(rt[t,:]>=hr)
        mmt=(rt[t,:]==hr)&(rg[t,:]>=hr)
        
        for var in vars:
            if ('MsKE' in var):
                dtemp['g'+var+'_het'][mmg]=databig(fpin[var+'_het'][hr-delay,:])[mmg]
                dtemp['g'+var+'_hmg'][mmg]=databig(fpin[var+'_hmg'][hr-delay,:])[mmg]
                dtemp['t'+var+'_het'][mmt]=databig(fpin[var+'_het'][hr-delay,:])[mmt]
                dtemp['t'+var+'_hmg'][mmt]=databig(fpin[var+'_hmg'][hr-delay,:])[mmt]
            elif ('VAR' in var):
                dtemp['g'+var+'_het'][mmg]=databig(fpin[var+'_het'][hr-delay,:])[mmg]
                dtemp['t'+var+'_het'][mmt]=databig(fpin[var+'_het'][hr-delay,:])[mmt]
            else:
                dtemp['g'+var+'_het'][mmg]=fpin[var+'_het'][hr-delay,:][mmg]
                dtemp['g'+var+'_hmg'][mmg]=fpin[var+'_hmg'][hr-delay,:][mmg]
                dtemp['t'+var+'_het'][mmt]=fpin[var+'_het'][hr-delay,:][mmt]
                dtemp['t'+var+'_hmg'][mmt]=fpin[var+'_hmg'][hr-delay,:][mmt]
    

    try:
        fp=nc.Dataset(odir+'all/prerain/'+file[0:8]+'.nc','r+')
    except Exception:
        fp=nc.Dataset(odir+'all/prerain/'+file[0:8]+'.nc','w')
        fp.createDimension('we',1559)
        fp.createDimension('sn',1039)


    #### FINISH OUTPUT SETUP ####
    for var in dtemp.keys():
        try:
            fp.createVariable(var,'f4',('sn','we'))
        except Exception:
            pass
        fp[var][:]=dtemp[var][:]

    fp.close()
    print('DONE')
    t=t+1
    




