import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import sys
import datetime
from mpi4py import MPI
from sklearn import metrics

# MPI4PY Stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

### USER INPUT ###
idir='/home/tsw35/tyche/wrf_gaea/'
odir='/home/tsw35/tyche/wrf_gaea/all/'
years=[2021,2022,2023]

### 
dlist=list(range(152,242))

N=len(dlist)*len(years)

het=np.ones((N,1039,1559))*float('nan')
hmg=np.ones((N,1039,1559))*float('nan')
msw=np.zeros((N,1039,1559))

# [0,3,6,9,12,15,18,21]
#range(152,243):
t=0
for year in years:
    for td in dlist:
        print('AGG: '+str(td)+'/243',flush=True)
        # aggregate mswep; td first
        dmsw=np.zeros((1039, 1559))
        for th in [12,15,18,21]:
            fp=nc.Dataset(idir+'mswep_gaea/'+str(year)+str(td)+'.'+str(th)+'.nc','r')
            dmsw=dmsw+fp['Band1'][:]
        for th in [0,3,6,9]:
            fp=nc.Dataset(idir+'mswep_gaea/'+str(year)+str(td+1)+'.0'+str(th)+'.nc','r')
            dmsw=dmsw+fp['Band1'][:]
        msw[t,:,:]=dmsw[:]

        # aggregate het/hmg
        date0=datetime.datetime(year,1,1,0)
        datesim=date0+datetime.timedelta(days=td-1)
        name=datesim.strftime('%Y%m%d_conv.nc')
        try:
            fp=nc.Dataset(idir+name,'r')
        except Exception as e:
            print(e)
            t=t+1
            continue
        het[t,:,:]=fp['RAINNC_het'][48,:,:]-fp['RAINNC_het'][24,:,:]
        hmg[t,:,:]=fp['RAINNC_hmg'][48,:,:]-fp['RAINNC_hmg'][24,:,:]
        t=t+1

# Now Compute RMSE and bias
rmset=np.zeros((1039, 1559))
biast=np.zeros((1039, 1559))

rmseg=np.zeros((1039, 1559))
biasg=np.zeros((1039, 1559))

msmean=np.zeros((1039, 1559))

print()
print('Compute RMSE')
for i in range(1039):
    if i%10==0:
        print(str(int(i/10))+'%')
    for j in range(1559):
        ht=het[:,i,j]
        hg=hmg[:,i,j]
        mst=msw[:,i,j]
        msg=msw[:,i,j]

        mst=mst[~np.isnan(ht)]
        msg=msg[~np.isnan(hg)]
        
        ht=ht[~np.isnan(ht)]
        hg=hg[~np.isnan(hg)]

        rmset[i,j]=metrics.mean_squared_error(mst,ht,squared=False)
        rmseg[i,j]=metrics.mean_squared_error(msg,hg,squared=False)

        biast[i,j]=np.mean(ht-mst)
        biasg[i,j]=np.mean(hg-msg)
        
        msmean[i,j]=np.mean(mst)

try:
    fp=nc.Dataset(odir+'mswep_error.nc','r+')
except Exception:
    fp=nc.Dataset(odir+'mswep_error.nc','w')
    fp.createDimension('we',1559)
    fp.createDimension('sn',1039)

#### FINISH OUTPUT SETUP ####
#fp.createVariable(var,'f4',('time','sn'+dimscln, 'we'+dimscln))

fp.createVariable('BIAS2D_het','f4',('sn','we'))
fp.createVariable('BIAS2D_hmg','f4',('sn','we'))
fp.createVariable('RMSE2D_het','f4',('sn','we'))
fp.createVariable('RMSE2D_hmg','f4',('sn','we'))
fp.createVariable('MSWEP_MEAN2D','f4',('sn','we'))

fp['BIAS2D_het'][:]=biast[:]
fp['BIAS2D_hmg'][:]=biasg[:]
fp['RMSE2D_het'][:]=rmset[:]
fp['RMSE2D_hmg'][:]=rmseg[:]
fp['MSWEP_MEAN2D'][:]=msmean[:]


