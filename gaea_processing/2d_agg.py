import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import sys
from datetime import datetime,timedelta

odir='/home/tsw35/tyche/wrf_gaea/'


#### USER INPUT ####
scl=20 #20=60km averaging scale


#### RUN IT ####
dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039


#bigvars=['LOCLOUD_hmg','MDCLOUD_hmg','HICLOUD_hmg','LOCLOUD_het','MDCLOUD_het','HICLOUD_het',
#         'LCL_hmg','LFC_hmg','LCL_het','LFC_het',
#         'RAINNC_het','RAINNC_hmg','LWP_het','LWP_hmg',
#         'HFX_het','HFX_hmg','LH_het','LH_hmg','PW_het','PW_hmg','RH2_het','RH2_hmg','T2_het','T2_hmg']

#smvars=['MsKElo_het','MsKElo_hmg','MsKE_het','MsKE_hmg','HFX_60','VARHFX_het','LH_60','VARLH_het']

#medvars=['MsKElo_het','MsKElo_hmg','MsKE_het','MsKE_hmg','LOCLOUD_hmg',\
#         'MDCLOUD_hmg','HICLOUD_hmg','LOCLOUD_het','MDCLOUD_het',\
#         'HICLOUD_het','RAINNC_het','RAINNC_hmg','LWP_het','LWP_hmg']

bigvars=['PW_het','PW_hmg','RH2_het','RH2_hmg','T2_het','T2_hmg']
smvars=[]
medvars=[]

data={}
for var in bigvars:
    data[var]=np.zeros((sn,we))
for var in smvars:
    data[var]=np.zeros((snscl,wescl))
for var in medvars:
    if var in smvars:
        data['MED_'+var]=np.zeros((snscl,wescl))
    else:
        data['MED_'+var]=np.zeros((sn,we))

fp=nc.Dataset(odir+'all/agg_full.nc','r')


for var in data.keys():
    if (var=='RAINNC_het') or (var=='RAINNC_hmg'):
        data[var]=np.sum(fp[var][:],axis=0)
    elif 'MED_' in var:
        data[var]=np.median(fp[var[4:]][:],axis=0)
    else:
        data[var]=np.mean(fp[var][:],axis=0)

fp.close()

#### CREATE OUTPUT ####
try:
    fp=nc.Dataset(odir+'all/agg_2d.nc','r+')
except Exception:
    fp=nc.Dataset(odir+'all/agg_2d.nc','w')
    fp.createDimension('we',1559)
    fp.createDimension('sn',1039)
    
try:
    fp.createDimension('we'+dimscln,wescl)
    fp.createDimension('sn'+dimscln,snscl)
except Exception:
    pass
    
    
#### FINISH OUTPUT SETUP ####
for var in smvars:
    try:
        fp.createVariable(var,'f4',('sn'+dimscln, 'we'+dimscln))
    except Exception:
        pass
    if var in medvars:
        try:
            fp.createVariable('MED_'+var,'f4',('sn'+dimscln, 'we'+dimscln))
        except Exception:
            pass
for var in bigvars:
    try:
        fp.createVariable(var,'f4',('sn', 'we'))
    except Exception:
        pass
    if var in medvars:
        try:
            fp.createVariable('MED_'+var,'f4',('sn', 'we'))
        except Exception:
            pass


    
#### OUTPUT DATA ####
for var in data.keys():
    fp[var][:]=data[var][:]


fp.close()



