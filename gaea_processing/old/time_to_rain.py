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

prcp_het1=np.ones((N,1039, 1559))*float('nan')
prcp_het5=np.ones((N,1039, 1559))*float('nan')
prcp_het25=np.ones((N,1039, 1559))*float('nan')

prcp_hmg1=np.ones((N,1039, 1559))*float('nan')
prcp_hmg5=np.ones((N,1039, 1559))*float('nan')
prcp_hmg25=np.ones((N,1039, 1559))*float('nan')

i=0
for day in days:
    print(day)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()

    if len(hrs)<48:
        continue
    j=47
    for hr in hrs[::-1]:
        try:
            fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        except Exception:
            pass
        rain=fphet['RAINNC'][0,:,:]
        prcp_het1[i,:][rain>=1]=j
        prcp_het5[i,:][rain>=5]=j
        prcp_het25[i,:][rain>=25]=j
        
        j=j-1
    
    
    hrs=os.listdir(gaea_dir+day+'_hmg/')
    hrs.sort()

    if len(hrs)<48:
        continue
    j=47
    for hr in hrs[::-1]:
        try:
            fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')
        except Exception:
            pass
        rain=fphmg['RAINNC'][0,:,:]
        prcp_hmg1[i,:][rain>=1]=j
        prcp_hmg5[i,:][rain>=5]=j
        prcp_hmg25[i,:][rain>=25]=j

        j=j-1

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
    fphet.createVariable('1mmTime0_48','f4',('time','sn', 'we'))
except Exception:
    pass
try:
    fphet.createVariable('5mmTime0_48','f4',('time','sn', 'we'))
except Exception:
    pass
try:
    fphet.createVariable('25mmTime0_48','f4',('time','sn', 'we'))
except Exception:
    pass
fphet['1mmTime0_48'][:]=prcp_het1[:]
fphet['5mmTime0_48'][:]=prcp_het5[:]
fphet['25mmTime0_48'][:]=prcp_het25[:]


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
    fphmg.createVariable('1mmTime0_48','f4',('time','sn', 'we'))
except Exception:
    pass
try:
    fphmg.createVariable('5mmTime0_48','f4',('time','sn', 'we'))
except Exception:
    pass
try:
    fphmg.createVariable('25mmTime0_48','f4',('time','sn', 'we'))
except Exception:
    pass
fphmg['1mmTime0_48'][:]=prcp_hmg1[:]
fphmg['5mmTime0_48'][:]=prcp_hmg5[:]
fphmg['25mmTime0_48'][:]=prcp_hmg25[:]



