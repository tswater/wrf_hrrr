import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import sys

from mpi4py import MPI

# MPI4PY Stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

gaea_dir='/home/tsw35/xTyc_shared/full_compress/'

#gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/all/'


#### USER INPUT ####
scl=20 #20=60km averaging scale

print()
print('WRF',flush=True)
print()

#### RUN IT ####
fpst=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/201707_long/het/OUTPUT/static_data.nc','r')
msk=fpst['LU_INDEX'][0,:,:]!=17

# find all days
days=[]

stbolt=5.670*10**(-8)

lwug=np.zeros((24,))
lwdg=np.zeros((24,))
swg=np.zeros((24,))
grdflxg=np.zeros((24,))
hfxg=np.zeros((24,))
lhg=np.zeros((24,))

lwut=np.zeros((24,))
lwdt=np.zeros((24,))
swt=np.zeros((24,))
grdflxt=np.zeros((24,))
hfxt=np.zeros((24,))
lht=np.zeros((24,))

for day in os.listdir(gaea_dir):
    if 'het' in day:
        continue
    day_=day[0:8]
    n1=len(os.listdir(gaea_dir+day_+'_het'))
    n2=len(os.listdir(gaea_dir+day_+'_hmg'))
    if (n1<48) or (n2<48):
        continue

    days.append(day_)


days.sort()

for day in days:
    print(day,flush=True)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()
    
    hrs=hrs[25:]

    i=0
    for hr in hrs:
        print('   '+hr,flush=True)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')
        
        emissg=fphmg['EMISS'][0,:][msk]
        emisst=fphet['EMISS'][0,:][msk]

        lwug[i]=lwug[i]+np.nanmean(emissg*fphmg['TSK'][0,:][msk]**4)*stbolt
        lwdg[i]=lwdg[i]+np.nanmean(emissg*fphmg['GLW'][0,:][msk])
        swg[i]=swg[i]+np.nanmean((1-fphmg['ALBEDO'][0,:][msk])*fphmg['SWDOWN'][0,:][msk])
        grdflxg[i]=grdflxg[i]+np.nanmean(fphmg['GRDFLX'][0,:][msk])
        hfxg[i]=hfxg[i]+np.nanmean(fphmg['HFX'][0,:][msk])
        lhg[i]=lhg[i]+np.nanmean(fphmg['LH'][0,:][msk])
        
        lwut[i]=lwut[i]+np.nanmean(emisst*fphet['TSK'][0,:][msk]**4)*stbolt
        lwdt[i]=lwdt[i]+np.nanmean(emisst*fphet['GLW'][0,:][msk])
        swt[i]=swt[i]+np.nanmean((1-fphet['ALBEDO'][0,:][msk])*fphet['SWDOWN'][0,:][msk])
        grdflxt[i]=grdflxt[i]+np.nanmean(fphet['GRDFLX'][0,:][msk])
        hfxt[i]=hfxt[i]+np.nanmean(fphet['HFX'][0,:][msk])
        lht[i]=lht[i]+np.nanmean(fphet['LH'][0,:][msk])

        fphet.close()
        fphmg.close()
        i=i+1

#### CREATE OUTPUT ####
try:
    fp=nc.Dataset(odir+'diurnal.nc','r+')
except Exception:
    fp=nc.Dataset(odir+'diurnal.nc','w')
    fp.createDimension('time',24)
except Exception:
    pass

try:
    fp.createVariable('LW_DOWN_het','f4',('time'))
except Exception:
    pass
try:
    fp.createVariable('LW_UP_het','f4',('time'))
except Exception:
    pass
try:
    fp.createVariable('SW_NET_het','f4',('time'))
except Exception:
    pass
try:
    fp.createVariable('HFX_het','f4',('time'))
except Exception:
    pass
try:
    fp.createVariable('LH_het','f4',('time'))
except Exception:
    pass
try:
    fp.createVariable('GRDFLX_het','f4',('time'))
except Exception:
    pass


try:
    fp.createVariable('LW_DOWN_hmg','f4',('time'))
except Exception:
    pass
try:
    fp.createVariable('LW_UP_hmg','f4',('time'))
except Exception:
    pass
try:
    fp.createVariable('SW_NET_hmg','f4',('time'))
except Exception:
    pass
try:
    fp.createVariable('HFX_hmg','f4',('time'))
except Exception:
    pass
try:
    fp.createVariable('LH_hmg','f4',('time'))
except Exception:
    pass
try:
    fp.createVariable('GRDFLX_hmg','f4',('time'))
except Exception:
    pass

fp['LW_DOWN_het'][:]=lwdt[:]/257
fp['LW_UP_het'][:]=lwut[:]/257
fp['SW_NET_het'][:]=swt[:]/257
fp['HFX_het'][:]=hfxt[:]/257
fp['LH_het'][:]=lht[:]/257
fp['GRDFLX_het'][:]=grdflxt[:]/257

fp['LW_DOWN_hmg'][:]=lwdg[:]/257
fp['LW_UP_hmg'][:]=lwug[:]/257
fp['SW_NET_hmg'][:]=swg[:]/257
fp['HFX_hmg'][:]=hfxg[:]/257
fp['LH_hmg'][:]=lhg[:]/257
fp['GRDFLX_hmg'][:]=grdflxg[:]/257

fp.close()
