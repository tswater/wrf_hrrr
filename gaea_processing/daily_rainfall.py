import numpy as np
import os
from subprocess import run
import netCDF4 as nc

gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/all/'

# find all days
days=[]
for day in os.listdir(gaea_dir):
    day_=day[0:8]
    if day_ in days:
        continue
    else:
        days.append(day_)

N=len(days)

days.sort()

prcp_het=np.ones((N,1039, 1559))*float('nan')
prcp_hmg=np.ones((N,1039, 1559))*float('nan')

i=0
for day in days:
    print(day)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()

    try:
        fphet0=nc.Dataset(gaea_dir+day+'_het/'+hrs[24],'r')
        fphet1=nc.Dataset(gaea_dir+day+'_het/'+hrs[48],'r')
        
        prcp_het[i,:,:]=(fphet1['RAINNC'][0,:,:]-fphet0['RAINNC'][0,:,:])
    except Exception:
        pass

    hrs=os.listdir(gaea_dir+day+'_hmg/')
    hrs.sort()

    try:
        fphmg0=nc.Dataset(gaea_dir+day+'_hmg/'+hrs[24],'r')
        fphmg1=nc.Dataset(gaea_dir+day+'_hmg/'+hrs[48],'r')
    
        prcp_hmg[i,:,:]=(fphmg1['RAINNC'][0,:,:]-fphmg0['RAINNC'][0,:,:])
    except Exception:
        pass

    i=i+1

try:
    #fphet=nc.Dataset(odir+'daily_het.nc','w')
    #fphmg=nc.Dataset(odir+'daily_hmg.nc','w')
    fphet.createDimension('we',1559)
    fphet.createDimension('sn',1039)
    fphet.createDimension('time',N)
    fphmg.createDimension('we',1559)
    fphmg.createDimension('sn',1039)
    fphmg.createDimension('time',N)
except Exception:
    fphet=nc.Dataset(odir+'daily_het.nc','r+')
    fphmg=nc.Dataset(odir+'daily_hmg.nc','r+')


# OUTPUT info
try:
    fphet.createVariable('time','i4',('time'))
    times=[]
    for d in days:
        times.append(int(d))
    times=np.array(times)
    fphet['time'][:]=times[:]
except:
    pass

try:
    fphet.createVariable('RAINNC','f4',('time','sn', 'we'))
except Exception:
    pass
fphet['RAINNC'][:]=prcp_het[:]



try:
    fphmg.createVariable('time','i4',('time'))
    times=[]
    for d in days:
        times.append(int(d))
    times=np.array(times)
    fphmg['time'][:]=times[:]
except:
    pass
try:
    fphmg.createVariable('RAINNC','f4',('time','sn', 'we'))
except Exception:
    pass
fphmg['RAINNC'][:]=prcp_hmg[:]



