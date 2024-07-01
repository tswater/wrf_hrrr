import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import sys
#import wrf

from mpi4py import MPI

# MPI4PY Stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

odir='/home/tsw35/tyche/wrf_gaea/qke_only/'
gaea_dir='/home/tsw35/xTyc_shared/full_compress/'

#### USER INPUT ####
scl=20 #20=60km averaging scale

def a_v(full,scl=20):
    nx=int(full.shape[1]/scl+1)
    ny=int(full.shape[2]/scl+1)
    out1=np.zeros((full.shape[0],nx,ny))
    out2=np.zeros((full.shape[0],nx,ny))
    for lvl in range(zlvl):
        print('.',end='',flush=True)
        for i in range(nx):
            for j in range(ny):
                dd=full[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
                out1[lvl,i,j]=np.mean(dd)
                out2[lvl,i,j]=np.var(dd)
    return out1,out2

#### RUN IT ####

dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039
zlvl=50

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

smvars=['QKE_4D_het','QKE_4D_hmg']

for day in days[rank::size]:
    print(day,flush=True)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()

    het_pbl=np.zeros((N,zlvl,snscl,wescl))
    hmg_pbl=np.zeros((N,zlvl,snscl,wescl))

    i=0
    for hr in hrs:
        print(hr,end='',flush=True)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')

        pblt=fphet['QKE'][0,:,:,:]
        pblg=fphmg['QKE'][0,:,:,:]

        het_pbl[i,:,:,:],_=a_v(pblt)
        hmg_pbl[i,:,:,:],_=a_v(pblg)
        
        print('',flush=True)

        fphet.close()
        fphmg.close()
        i=i+1

    #### CREATE OUTPUT ####
    print(day+': analysis done',flush=True)
    

    #### FINISH OUTPUT SETUP ####
    fp=nc.Dataset(odir+day+'_qke.nc','w')
    fp.createDimension('we',1559)
    fp.createDimension('sn',1039)
    fp.createDimension('time',N)

    try:
        fp.createDimension('z',zlvl)
        fp.createDimension('we'+dimscln,wescl)
        fp.createDimension('sn'+dimscln,snscl)
    except Exception:
        pass


    for var in smvars:
        try:
            fp.createVariable(var,'f4',('time','z','sn'+dimscln, 'we'+dimscln))
        except Exception:
            pass
    fp['QKE_4D_het'][:]=het_pbl[:]
    fp['QKE_4D_hmg'][:]=hmg_pbl[:]

    fp.close()
    print(day+': output complete',flush=True)

