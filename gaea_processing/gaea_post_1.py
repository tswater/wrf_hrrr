import numpy as np
import os
from subprocess import run
import netCDF4 as nc

gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/cum/'

cmprecip=False
cmlwp=True

# find all days that are usable
days=[]
for day in os.listdir(gaea_dir):
    if 'het' in day:
        continue
    day_=day[0:8]
    n1=len(os.listdir(gaea_dir+day_+'_het'))
    n2=len(os.listdir(gaea_dir+day_+'_hmg'))
    if (n1<48) or (n2<48):
        continue

    days.append(day_)

# PRECIP CUM
if cmprecip:
    prcp_het=np.zeros((1039, 1559))
    prcp_hmg=np.zeros((1039, 1559))

    for day in days:
        hrs=os.listdir(gaea_dir+day+'_het/')
        hrs.sort()
        fphet0=nc.Dataset(gaea_dir+day+'_het/'+hrs[24],'r')
        fphet1=nc.Dataset(gaea_dir+day+'_het/'+hrs[48],'r')
        fphmg0=nc.Dataset(gaea_dir+day+'_hmg/'+hrs[24],'r')
        fphmg1=nc.Dataset(gaea_dir+day+'_hmg/'+hrs[48],'r')
        
        prcp_het=prcp_het+(fphet1['RAINNC'][0,:,:]-fphet0['RAINNC'][0,:,:])
        prcp_hmg=prcp_hmg+(fphmg1['RAINNC'][0,:,:]-fphmg0['RAINNC'][0,:,:])

# LWP CUM
if cmlwp:    
    lwp_het=np.zeros((1039, 1559))
    lwp_hmg=np.zeros((1039, 1559))
    for day in days:
        print(day,end='')
        hrs=os.listdir(gaea_dir+day+'_het/')
        hrs.sort()
        for hr in hrs[24:]:
            print('.',end='',flush=True)
            fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
            fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')
            pres=fphet['PH'][:]+fphet['PHB'][:]
            dpres=pres[:,1:,:,:]-pres[:,:-1,:,:]
            lwp_het=lwp_het+np.sum(dpres/9.81*fphet['QCLOUD'][:],axis=1)

            pres=fphmg['PH'][:]+fphmg['PHB'][:]
            dpres=pres[:,1:,:,:]-pres[:,:-1,:,:]
            lwp_hmg=lwp_hmg+np.sum(dpres/9.81*fphmg['QCLOUD'][:],axis=1)
        print()

fphet=nc.Dataset(odir+'het.nc','w')
fphmg=nc.Dataset(odir+'hmg.nc','w')
fphet.createDimension('we',1559)
fphet.createDimension('sn',1039)

fphmg.createDimension('we',1559)
fphmg.createDimension('sn',1039)

fphet.createVariable('LWP','f4',('sn', 'we'))
fphmg.createVariable('LWP','f4',('sn', 'we'))
if cmprecip:
    fphet.createVariable('RAINNC','f4',('sn', 'we'))
    fphmg.createVariable('RAINNC','f4',('sn', 'we'))

fphet['LWP'][:]=lwp_het[:]
fphmg['LWP'][:]=lwp_hmg[:]
if cmprecip:
    fphet['RAINNC'][:]=prcp_het[:]
    fphmg['RAINNC'][:]=prcp_hmg[:]



# CLOUD CUM
# 'low_cloudfrac','mid_cloudfrac', 'high_cloudfrac'

