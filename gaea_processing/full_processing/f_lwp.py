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

#argv = sys.argv[1:]
#gaea_dir = argv[0]

gaea_dir='/home/tsw35/xTyc_shared/full_compress/'

#gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/'


#### USER INPUT ####
scl=20 #20=60km averaging scale

print()
print('LWP',flush=True)
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

    het_r=np.zeros((N,sn,we))
    hmg_r=np.zeros((N,sn,we))
    het_lwp=np.zeros((N,sn,we))
    hmg_lwp=np.zeros((N,sn,we))

    i=0
    for hr in hrs:
        print(hr,flush=True)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')

        pg=wrf.getvar(fphmg,'pres',meta=False)
        pt=wrf.getvar(fphet,'pres',meta=False)

        #### LWP ####
        dpg=pg[1:,:,:]-pg[:-1,:,:]
        dpt=pt[1:,:,:]-pt[:-1,:,:]

        het_lwp[i,:,:]=np.sum(-dpt/9.81*fphet['QCLOUD'][0,:-1,:],axis=0)
        hmg_lwp[i,:,:]=np.sum(-dpg/9.81*fphmg['QCLOUD'][0,:-1,:],axis=0)

        het_r[i,:,:]=fphet['RAINNC'][0,:,:]
        hmg_r[i,:,:]=fphmg['RAINNC'][0,:,:]
        
        print(day+' LWP DONE',flush=True)
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
    
    fp['LWP_hmg'][:]=hmg_lwp[:]
    fp['LWP_het'][:]=het_lwp[:]
    fp['RAINNC_hmg'][:]=hmg_r[:]
    fp['RAINNC_het'][:]=het_r[:]

    fp.close()


