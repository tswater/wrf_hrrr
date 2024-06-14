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

vars=['PBLH_het','PBLH_hmg','T0_het','T0_hmg','Q0_het','Q0_hmg']

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

    rh2_het=np.zeros((N,sn,we))
    rh2_hmg=np.zeros((N,sn,we))
    
    t2_het=np.zeros((N,sn,we))
    t2_hmg=np.zeros((N,sn,we))
    
    pblh_hmg=np.zeros((N,sn,we))
    pblh_het=np.zeros((N,sn,we))

    i=0
    for hr in hrs:
        print(hr,flush=True)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')

        #### WRF ####
        rh2_het[i,:,:]=fphet['QVAPOR'][0,0,:,:]
        rh2_hmg[i,:,:]=fphmg['QVAPOR'][0,0,:,:]
        
        pblh_het[i,:,:]=fphet['PBLH'][0,:,:]
        pblh_hmg[i,:,:]=fphmg['PBLH'][0,:,:]

        ptot=fphet['PB'][0,0,:,:]+fphet['P'][0,0,:,:]
        theta=fphet['T'][0,0,:,:]+300
        t2_het[i,:,:]=theta*(ptot/1000)**(2/7)

        ptot=fphmg['PB'][0,0,:,:]+fphmg['P'][0,0,:,:]
        theta=fphmg['T'][0,0,:,:]+300
        t2_hmg[i,:,:]=theta*(ptot/1000)**(2/7)

        print(day+' WRF DONE',flush=True)
        fphet.close()
        fphmg.close()
        i=i+1

    #### CREATE OUTPUT ####
    fp=nc.Dataset(odir+day+'_conv.nc','r+')

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
    fp['PBLH_het'][:]=pblh_het[:]
    fp['PBLH_hmg'][:]=pblh_hmg[:]
    fp['Q0_hmg'][:]=rh2_hmg[:]
    fp['T0_hmg'][:]=t2_hmg[:]
    fp['Q0_het'][:]=rh2_het[:]
    fp['T0_het'][:]=t2_het[:]
    
    fp.close()
