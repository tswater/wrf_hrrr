import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import sys
import wrf

from mpi4py import MPI

# MPI4PY Stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

gaea_dir='/home/tsw35/xTyc_shared/full_compress/'

#gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/'


#### USER INPUT ####
scl=20 #20=60km averaging scale

print()
print('WRF',flush=True)
print()

#### RUN IT ####

dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039


# find all days
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


N=49

days.sort()

for day in days[rank::size]:
    print(day,flush=True)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()

    cape2d_het=np.zeros((N,4,sn,we))

    cape2d_hmg=np.zeros((N,4,sn,we))

    i=0
    for hr in hrs:
        print(hr,flush=True)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')

        #### WRF ####
        cape2d_het[i,:,:,:]=wrf.getvar(fphet,'cape2d',meta=False)

        cape2d_hmg[i,:,:,:]=wrf.getvar(fphmg,'cape2d',meta=False)

        print(day+' WRF DONE',flush=True)
        fphet.close()
        fphmg.close()
        i=i+1

    #### CREATE OUTPUT ####
    try:
        fp=nc.Dataset(odir+day+'_conv.nc','r+')
    except Exception:
        fp=nc.Dataset(odir+day+'_conv.nc','w')
        fp.createDimension('we',1559)
        fp.createDimension('sn',1039)
        fp.createDimension('time',N)

    try:
        fp.createDimension('we'+dimscln,wescl)
        fp.createDimension('sn'+dimscln,snscl)
    except Exception:
        pass

    fp['MAXCAPE_hmg'][:]=cape2d_hmg[:,0,:]
    fp['MINCIN_hmg'][:]=cape2d_hmg[:,1,:]
    fp['LCL_hmg'][:]=cape2d_hmg[:,2,:]
    fp['LFC_hmg'][:]=cape2d_hmg[:,3,:]
    fp['MAXCAPE_het'][:]=cape2d_het[:,0,:]
    fp['MINCIN_het'][:]=cape2d_het[:,1,:]
    fp['LCL_het'][:]=cape2d_het[:,2,:]
    fp['LFC_het'][:]=cape2d_het[:,3,:]
    
    fp.close()
