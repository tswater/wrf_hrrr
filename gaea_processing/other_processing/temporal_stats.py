import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import sys
from datetime import datetime,timedelta

odir='/home/tsw35/tyche/wrf_gaea/'
types=['norm','nr-day','nr-fg','nr-ft']

#### USER INPUT ####
scl=20 #20=60km averaging scale
typ=types[3]

try:
    typ=types[int(sys.argv[1])]
except:
    pass

normalize=True

def databig(data):
    dout=np.zeros((257,1039,1559))
    for t in range (257):
        for i in range(data.shape[1]):
            for j in range(data.shape[2]):
                dout[t,i*20:(i+1)*20,j*20:(j+1)*20]=data[t,i,j]
    return dout



#### RUN IT ####
dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039

fpst=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/201707_long/het/OUTPUT/static_data.nc','r')
msk=fpst['LU_INDEX'][0,:,:]==17

vars=['RAINNC','HFX','LH','PW','T2','RH2','HICLOUD','MDCLOUD','LOCLOUD','LCL','LFC','MsKElo','MsKE','EF']
datab={}
datab['CAL']=np.zeros((len(vars),257))
datab['MEX']=np.zeros((len(vars),257))
datab['FLR']=np.zeros((len(vars),257))
datab['GRL']=np.zeros((len(vars),257))
datab['GSL']=np.zeros((len(vars),257))
datab['CTL']=np.zeros((len(vars),257))
datab['TEX']=np.zeros((len(vars),257))
datab['LND']=np.zeros((len(vars),257))
datab['ALL']=np.zeros((len(vars),257))
masks={}
for k in datab.keys():
    masks[k]=np.zeros((1039, 1559),dtype='bool')
masks['CAL'][500:800,30:150]=True
masks['MEX'][50:400,200:400]=True
masks['FLR'][75:275,1200:1375]=True
masks['GRL'][700:1000,900:1375]=True
masks['GSL'][600:750,300:450]=True
masks['CTL'][400:800,600:1000]=True
masks['TEX'][180:350,700:1000]=True
masks['ALL'][:]=True
masks['LND'][~msk]=True
for k in masks.keys():
    if k!='ALL':
        masks[k][msk]=False
if (typ=='norm') or (typ=='nr-day'):
    fpagg=nc.Dataset(odir+'all/agg_full.nc','r')
else:
    flist=os.listdir(odir+'all/prerain/')
    flist.sort()
i=0

for var in vars:
    print(var,flush=True)
    if typ=='norm':
        if var=='EF':
            datat=fpagg['LH_het'][:]/(fpagg['HFX_het'][:]+fpagg['LH_het'][:])
            datag=fpagg['LH_hmg'][:]/(fpagg['HFX_hmg'][:]+fpagg['LH_hmg'][:])
        elif 'MsKE' in var:
            datag=databig(fpagg[var+'_hmg'][:])
            datat=databig(fpagg[var+'_het'][:])
        else:
            datag=fpagg[var+'_hmg'][:]
            datat=fpagg[var+'_het'][:]
    elif typ=='nr-day':
        if var=='EF':
            datat=fpagg['LH_het'][:]/(fpagg['HFX_het'][:]+fpagg['LH_het'][:])
            datag=fpagg['LH_hmg'][:]/(fpagg['HFX_hmg'][:]+fpagg['LH_hmg'][:])
        elif 'MsKE' in var:
            datag=databig(fpagg[var+'_hmg'][:])
            datat=databig(fpagg[var+'_het'][:])
        else:
            datag=fpagg[var+'_hmg'][:]
            datat=fpagg[var+'_het'][:]
        for t in range(257):
            mm=(fpagg['RAINNC_het'][t,:]>1)|(fpagg['RAINNC_hmg'][t,:]>1)
            datag[t,mm]=float('nan')
            datat[t,mm]=float('nan')

    elif (typ=='nr-fg') or (typ=='nr-ft'):
        datag=np.zeros((257,1039, 1559))
        datat=np.zeros((257,1039, 1559))
        if typ=='nr-fg':
            nm='g'
        elif typ=='nr-ft':
            nm='t'
        for t in range(257):
            fpagg=nc.Dataset(odir+'all/prerain/'+flist[t],'r')
            if var=='EF':
                datat[t,:]=fpagg[nm+'LH_het'][:]/(fpagg[nm+'HFX_het'][:]+fpagg[nm+'LH_het'][:])
                datag[t,:]=fpagg[nm+'LH_hmg'][:]/(fpagg[nm+'HFX_hmg'][:]+fpagg[nm+'LH_hmg'][:])
            else:
                datag[t,:]=fpagg[nm+var+'_hmg'][:]
                datat[t,:]=fpagg[nm+var+'_het'][:]
            
    for k in datab.keys():
        print(k)
        if normalize:
            if var=='T2':
                datab[k][i,:]=(np.nanmean(datag[:,masks[k]],axis=(1))-np.nanmean(datat[:,masks[k]],axis=(1)))/(np.nanmean(datat[:,masks[k]],axis=(1))-273)
            else:
                datab[k][i,:]=(np.nanmean(datag[:,masks[k]],axis=(1))-np.nanmean(datat[:,masks[k]],axis=(1)))/np.nanmean(datat[:,masks[k]],axis=(1))
        else:
            datab[k][i,:]=(np.nanmean(datag[:,masks[k]],axis=(1))-np.nanmean(datat[:,masks[k]],axis=(1)))
    i=i+1

fpagg.close()

#### CREATE OUTPUT ####
try:
    fp=nc.Dataset(odir+'all/new_time_stats_'+typ+'.nc','r+')
except Exception:
    fp=nc.Dataset(odir+'all/new_time_stats_'+typ+'.nc','w')
    fp.createDimension('time',257)
    fp.createDimension('vars',len(vars))
    
#### FINISH OUTPUT SETUP ####
for k in datab.keys():
    try:
        fp.createVariable(k,'f4',('vars', 'time'))
    except Exception:
        pass

try:
    fp.createVariable('VARS','S2',('vars'))
except Exception:
    pass
    
#### OUTPUT DATA ####
for k in datab.keys():
    fp[k][:]=datab[k][:]
try:
    fp['VARS'][:]=vars[:]
except:
    pass


fp.close()



