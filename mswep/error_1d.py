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
thresh=1
land=True

# 3hr, daily, total RMSE and BIAS
# 3hr and daily rainfall coverage as f1_score and coverage area bias

### 
dlist=list(range(152,242))

fphet=nc.Dataset('/stor/soteria/hydro/shared/WRF_HRRR/20230709_het/wrfrst_d01_2023-07-10_21:00:00','r')
if land:
    lumsk=fphet['LU_INDEX'][0,:,:]!=17
else:
    lumsk=fphet['LU_INDEX'][0,:,:]!=1437
fphet.close()

Nd=len(dlist)*len(years)
N3=Nd*8

hetd=np.ones((Nd,1039,1559))*float('nan')
hmgd=np.ones((Nd,1039,1559))*float('nan')
mswd=np.zeros((Nd,1039,1559))

het3=np.ones((N3,1039,1559))*float('nan')
hmg3=np.ones((N3,1039,1559))*float('nan')
msw3=np.zeros((N3,1039,1559))

het=np.zeros((1039,1559))
hmg=np.zeros((1039,1559))
msw=np.zeros((1039,1559))

m3=np.zeros((N3,))
md=np.ones((Nd,))

# [0,3,6,9,12,15,18,21]
#range(152,243):
t=0
t3=0
print('#### STEP 1/3: AGGREGATE ####')
for year in years:
    for td in dlist:
        print('AGG: '+str(td)+'/243')
    
        # load het/hmg
        date0=datetime.datetime(year,1,1,0)
        datesim=date0+datetime.timedelta(days=td-1)
        name=datesim.strftime('%Y%m%d_conv.nc')
        try:
            fp=nc.Dataset(idir+name,'r')
        except Exception as e:
            md[t]=0
            t=t+1
            print(e)
            continue
    
        # aggregate mswep; td first
        dmsw=np.zeros((1039, 1559))
        t32=27
        for th in [12,15,18,21]:
            fpm=nc.Dataset(idir+'mswep_gaea/'+str(year)+str(td)+'.'+str(th)+'.nc','r')
            dmsw=dmsw+fpm['Band1'][:]
            msw3[t3,:,:]=fpm['Band1'][:]
            het3[t3,:,:]=fp['RAINNC_het'][t32,:,:]-fp['RAINNC_het'][t32-3,:,:]
            hmg3[t3,:,:]=fp['RAINNC_hmg'][t32,:,:]-fp['RAINNC_hmg'][t32-3,:,:]
            m3[t3]=1
            t3=t3+1
            t32=t32+3
        for th in [0,3,6,9]:
            fpm=nc.Dataset(idir+'mswep_gaea/'+str(year)+str(td+1)+'.0'+str(th)+'.nc','r')
            dmsw=dmsw+fpm['Band1'][:]
            msw3[t3,:,:]=fpm['Band1'][:]
            het3[t3,:,:]=fp['RAINNC_het'][t32,:,:]-fp['RAINNC_het'][t32-3,:,:]
            hmg3[t3,:,:]=fp['RAINNC_hmg'][t32,:,:]-fp['RAINNC_hmg'][t32-3,:,:]
            m3[t3]=1
            t3=t3+1
            t32+3
        mswd[t,:,:]=dmsw[:]
    
        # aggregate het/hmg
        hetd[t,:,:]=fp['RAINNC_het'][48,:,:]-fp['RAINNC_het'][24,:,:]
        hmgd[t,:,:]=fp['RAINNC_hmg'][48,:,:]-fp['RAINNC_hmg'][24,:,:]
    
        het[:]=het[:]+hetd[t,:,:]
        hmg[:]=hmg[:]+hmgd[t,:,:]
        msw[:]=msw[:]+mswd[t,:,:]

        t=t+1
    
# 3hr, daily, total RMSE and BIAS
# 3hr and daily rainfall coverage as f1_score and coverage area bias
rmse3t=np.ones((N3,))*float('nan')
rmse3g=np.ones((N3,))*float('nan')
bias3t=np.ones((N3,))*float('nan')
bias3g=np.ones((N3,))*float('nan')

rmsedt=np.ones((Nd,))*float('nan')
rmsedg=np.ones((Nd,))*float('nan')
biasdt=np.ones((Nd,))*float('nan')
biasdg=np.ones((Nd,))*float('nan')

f13t=np.ones((N3,))*float('nan')
f13g=np.ones((N3,))*float('nan')
area3t=np.ones((N3,))*float('nan')
area3g=np.ones((N3,))*float('nan')
area3m=np.ones((N3,))*float('nan')

f1dt=np.ones((Nd,))*float('nan')
f1dg=np.ones((Nd,))*float('nan')
areadt=np.ones((Nd,))*float('nan')
areadg=np.ones((Nd,))*float('nan')
areadm=np.ones((Nd,))*float('nan')

rmse=0
bias=0

print('#### STEP 2/3: daily data ####')
for t in range(Nd):
    print('.',flush=True,end='')
    if md[t]==0:
        continue
    rmsedt[t]=metrics.mean_squared_error(mswd[t,:,:][lumsk],hetd[t,:,:][lumsk],squared=False)
    rmsedg[t]=metrics.mean_squared_error(mswd[t,:,:][lumsk],hmgd[t,:,:][lumsk],squared=False)
    biasdt[t]=np.mean(hetd[t,:,:][lumsk]-mswd[t,:,:][lumsk])
    biasdg[t]=np.mean(hmgd[t,:,:][lumsk]-mswd[t,:,:][lumsk])

    cvgm=mswd[t,:,:]
    cvgm[cvgm>1]=1
    cvgm[cvgm<1]=0

    cvgt=hetd[t,:,:]
    cvgt[cvgt>1]=1
    cvgt[cvgt<1]=0

    cvgg=hmgd[t,:,:]
    cvgg[cvgg>1]=1
    cvgg[cvgg<1]=0


    f1dt[t]=metrics.f1_score(cvgm[lumsk],cvgt[lumsk])
    f1dg[t]=metrics.f1_score(cvgm[lumsk],cvgg[lumsk])

    areadm[t]=np.sum(cvgm[lumsk])/len(cvgm[lumsk])
    areadt[t]=np.sum(cvgt[lumsk])/len(cvgt[lumsk])
    areadg[t]=np.sum(cvgg[lumsk])/len(cvgg[lumsk])


print()
print('#### STEP 3/3: 3 hourly data '+str(N3)+' timesteps ####')
for t in range(N3):
    print('.',flush=True,end='')
    if m3[t]==0:
        continue
    rmse3t[t]=metrics.mean_squared_error(msw3[t,:,:][lumsk],het3[t,:,:][lumsk],squared=False)
    rmse3g[t]=metrics.mean_squared_error(msw3[t,:,:][lumsk],hmg3[t,:,:][lumsk],squared=False)
    bias3t[t]=np.mean(het3[t,:,:][lumsk]-msw3[t,:,:][lumsk])
    bias3g[t]=np.mean(hmg3[t,:,:][lumsk]-msw3[t,:,:][lumsk])

    cvgm=msw3[t,:,:]
    cvgm[cvgm>1]=1
    cvgm[cvgm<1]=0

    cvgt=het3[t,:,:]
    cvgt[cvgt>1]=1
    cvgt[cvgt<1]=0

    cvgg=hmg3[t,:,:]
    cvgg[cvgg>1]=1
    cvgg[cvgg<1]=0

    f13t[t]=metrics.f1_score(cvgm[lumsk],cvgt[lumsk])
    f13g[t]=metrics.f1_score(cvgm[lumsk],cvgg[lumsk])
    
    area3m[t]=np.sum(cvgm[lumsk])/len(cvgm[lumsk])
    area3t[t]=np.sum(cvgt[lumsk])/len(cvgt[lumsk])
    area3g[t]=np.sum(cvgg[lumsk])/len(cvgg[lumsk])
    
print()
print('#### EXPORT ####')

###### OUTPUT ########
try:
    if land:
        fp=nc.Dataset(odir+'mswep_error_land.nc','r+')
    else:
        fp=nc.Dataset(odir+'mswep_error.nc','r+')
except Exception:
    if land:
        fp=nc.Dataset(odir+'mswep_error_land.nc','w')
    else:
        fp=nc.Dataset(odir+'mswep_error.nc','w')
    fp.createDimension('we',1559)
    fp.createDimension('sn',1039)

#### FINISH OUTPUT SETUP ####
#fp.createVariable(var,'f4',('time','sn'+dimscln, 'we'+dimscln))
fp.createDimension('days',Nd)
fp.createDimension('3hours',N3)

vars=['RMSE_d_het','RMSE_d_hmg','RMSE_3_het','RMSE_3_hmg','BIAS_d_het',
      'BIAS_d_hmg','BIAS_3_het','BIAS_3_hmg','F1SCORE_d_het','F1SCORE_d_hmg',
      'F1SCORE_3_het','F1SCORE_3_hmg','AREA_3_het','AREA_3_hmg',
      'AREA_3_mswep','AREA_d_het','AREA_d_hmg','AREA_d_mswep']

for var in vars:
    if '_d_' in var:
        fp.createVariable(var,'f4',('days'))
    elif '_3_' in var:
        fp.createVariable(var,'f4',('3hours'))

fp['RMSE_d_het'][:]=rmsedt[:]
fp['RMSE_d_hmg'][:]=rmsedg[:]
fp['RMSE_3_het'][:]=rmse3t[:]
fp['RMSE_3_hmg'][:]=rmse3g[:]
fp['BIAS_d_het'][:]=biasdt[:]
fp['BIAS_d_hmg'][:]=biasdg[:]
fp['BIAS_3_het'][:]=bias3t[:]
fp['BIAS_3_hmg'][:]=bias3g[:]
fp['F1SCORE_d_het'][:]=f1dt[:]
fp['F1SCORE_d_hmg'][:]=f1dg[:]
fp['F1SCORE_3_het'][:]=f13t[:]
fp['F1SCORE_3_hmg'][:]=f13g[:]
fp['AREA_3_het'][:]=area3t[:]
fp['AREA_3_hmg'][:]=area3g[:]
fp['AREA_3_mswep'][:]=area3m[:]
fp['AREA_d_het'][:]=areadt[:]
fp['AREA_d_hmg'][:]=areadg[:]
fp['AREA_d_mswep'][:]=areadm[:]
















