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

gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/'


#### USER INPUT ####
scl=20 #20=60km averaging scale


#### TKE ####
def tke(u,v,w,lvl,scl):
    nx=int(u.shape[1]/scl+1)
    ny=int(u.shape[2]/scl+1)
    out=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            uu=u[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
            uu=uu-np.mean(uu)
            
            vv=v[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
            vv=vv-np.mean(vv)
            
            ww=w[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
            ww=ww-np.mean(ww)
            
            out[i,j]=.5*(np.mean(uu**2)+np.mean(vv**2)+np.mean(ww**2))
    return out

#### RUN IT ####

name='TKE'+str(int(scl*3))
dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)


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

#days=['20230705']

for day in days[rank::size]:
    print(day,flush=True)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()

    het_tke=np.zeros((N,snscl,wescl))
    hmg_tke=np.zeros((N,snscl,wescl))

    i=0
    for hr in hrs:
        print(hr)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')
        
        #DO STUFF HERE (compute tke etc.)
        ut=wrf.getvar(fphet,'ua',meta=False)
        vt=wrf.getvar(fphet,'va',meta=False)
        wt=wrf.getvar(fphet,'wa',meta=False)
        ug=wrf.getvar(fphmg,'ua',meta=False)
        vg=wrf.getvar(fphmg,'va',meta=False)
        wg=wrf.getvar(fphmg,'wa',meta=False)
       
        het_tke[i,:,:]=tke(ut,vt,wt,3,scl)
        hmg_tke[i,:,:]=tke(ug,vg,wg,3,scl)

        i=i+1
    try:
        fp=nc.Dataset(odir+day+'_conv.nc','r+')
    except Exception:
        print('ERROR')
        continue
        #fp=nc.Dataset(odir+day+'_conv.nc','w')
        #fp.createDimension('we',1559)
        #fp.createDimension('sn',1039)
        #fp.createDimension('time',N)
    
    try:
        fp.createDimension('we'+dimscln,wescl)
        fp.createDimension('sn'+dimscln,snscl)
    except Exception:
        pass
    # OUTPUT info
    try:
        fp.createVariable('time','i4',('time'))
        fp['time'][:]=list(range(49))
    except:
        pass

    try:
        fp.createVariable(name+'_het','f4',('time','sn'+dimscln, 'we'+dimscln))
    except Exception:
        pass
    try:
        fp.createVariable(name+'_hmg','f4',('time','sn'+dimscln, 'we'+dimscln))
    except Exception:
        pass


    fp[name+'_het'][:]=het_tke[:]
    fp[name+'_hmg'][:]=hmg_tke[:]
    
    fp.close()


