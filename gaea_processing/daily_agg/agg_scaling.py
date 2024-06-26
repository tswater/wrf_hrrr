import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import sys


#argv = sys.argv[1:]
#gaea_dir = argv[0]

### CLUSTER FILEPATHS ###
gaea_dir='/home/tsw35/tyche/wrf_hrrr/compressed/'
odir='/home/tsw35/tyche/wrf_hrrr/'

### FRAMEWORK FILEPATHS ###
gaea_dir='/run/media/tswater/Elements/WRF/scaling_compressed/'
odir='/home/tswater/Documents/Elements_Temp/WRF/agg_files/'

#### MEANS AND VARIANCES ####
def vari(data,df=20):
    nx=int(data.shape[0]/df+1)
    ny=int(data.shape[1]/df+1)
    dout=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            dout[i,j] = np.nanvar(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout

def meani(data,df=20):
    nx=int(data.shape[0]/df+1)
    ny=int(data.shape[1]/df+1)
    dout=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            dout[i,j] = np.nanmean(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout

#### RUN IT ####

dimscln=str(int(40*3))
wescl=int((1559+1)/40)
snscl=int((1039+1)/40)
we=1559
sn=1039

N=49

# find all days
scls=['het','hmg006','hmg012','hmg015','hmg030','hmg060','hmg120']

hfx=np.zeros((7,N,sn,we))
lh=np.zeros((7,N,sn,we))
rain=np.zeros((7,N,sn,we))
tsurf=np.zeros((7,N,sn,we))

s=0
for scl in scls:
    print(scl,flush=True)
    hrs=os.listdir(gaea_dir+scl)
    hrs.sort()

    i=0
    for hr in hrs:
        print('   '+hr,flush=True)

        fp=nc.Dataset(gaea_dir+scl+'/'+hr,'r')

        hfx[s,i,:,:]=fp['HFX'][0,:]
        lh[s,i,:,:]=fp['LH'][0,:]
        tsurf[s,i,:,:]=fp['TSK'][0,:]
        rain[s,i,:,:]=fp['RAINNC'][0,:]

        fp.close()

        i=i+1
    s=s+1
    print()



#### CREATE OUTPUT ####
fp=nc.Dataset(odir+'agg_scaling.nc','w')
fp.createDimension('we',1559)
fp.createDimension('sn',1039)
fp.createDimension('time',N)
fp.createDimension('scale',7)

fp.createVariable('HFX','f4',('scale','time','sn', 'we'))
fp.createVariable('TSK','f4',('scale','time','sn', 'we'))
fp.createVariable('RAINNC','f4',('scale','time','sn', 'we'))
fp.createVariable('LH','f4',('scale','time','sn', 'we'))

fp['HFX'][:]=hfx[:]
fp['LH'][:]=lh[:]
fp['RAINNC'][:]=rain[:]
fp['TSK'][:]=tsurf[:]

fp.close()


