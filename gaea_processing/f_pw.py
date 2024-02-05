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

vars=['PW_het','PW_hmg','RH2_het','RH2_hmg','T2_het','T2_hmg']

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

    pw_het=np.zeros((N,sn,we))
    pw_hmg=np.zeros((N,sn,we))
    
    rh2_het=np.zeros((N,sn,we))
    rh2_hmg=np.zeros((N,sn,we))
    
    t2_het=np.zeros((N,sn,we))
    t2_hmg=np.zeros((N,sn,we))

    i=0
    for hr in hrs:
        print(hr,flush=True)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')

        #### WRF ####
        pw_het[i,:,:]=wrf.getvar(fphet,'pw',meta=False)
        pw_hmg[i,:,:]=wrf.getvar(fphmg,'pw',meta=False)

        rh2_het[i,:,:]=wrf.getvar(fphet,'rh2',meta=False)
        rh2_hmg[i,:,:]=wrf.getvar(fphmg,'rh2',meta=False)

        t2_het[i,:,:]=wrf.getvar(fphet,'T2',meta=False)
        t2_hmg[i,:,:]=wrf.getvar(fphmg,'T2',meta=False)

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

    for var in vars:
        try:
            fp.createVariable(var,'f4',('time','sn', 'we'))
        except Exception:
            pass
    
    fp['PW_hmg'][:]=pw_hmg[:]
    fp['RH2_hmg'][:]=rh2_hmg[:]
    fp['T2_hmg'][:]=t2_hmg[:]
    fp['PW_het'][:]=pw_het[:]
    fp['RH2_het'][:]=rh2_het[:]
    fp['T2_het'][:]=t2_het[:]
    
    fp.close()
