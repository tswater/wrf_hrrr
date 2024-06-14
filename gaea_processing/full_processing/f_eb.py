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

#argv = sys.argv[1:]
#gaea_dir = argv[0]

gaea_dir='/home/tsw35/xTyc_shared/full_compress/'

#gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/'

#### USER INPUT ####
scl=20 #20=60km averaging scale

#### TKE ####
def tke(u,v,w,lvl,scl,cc):
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

            cc2=np.mean(cc[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)])

            out[i,j]=cc2*.5*(np.mean(uu**2)+np.mean(vv**2)+np.mean(ww**2))
    return out



print()
print('FLUXES',flush=True)
print()

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
stbolt=5.67037*10**(-8)

for day in days[rank::size]:
    print(day,flush=True)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()
    
    het_gfx=np.zeros((N,sn,we))
    hmg_gfx=np.zeros((N,sn,we))

    het_netsw=np.zeros((N,sn,we))
    hmg_netsw=np.zeros((N,sn,we))
    
    het_netlw=np.zeros((N,sn,we))
    hmg_netlw=np.zeros((N,sn,we))

    het_glw=np.zeros((N,sn,we))
    hmg_glw=np.zeros((N,sn,we))

    i=0
    for hr in hrs:
        print(hr,flush=True)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')
        
        emissg=fphmg['EMISS'][0,:]
        emisst=fphet['EMISS'][0,:]
        
        hmg_netlw[i,:]=emissg*(fphmg['GLW'][0,:]-stbolt*fphmg['TSK'][0,:][:]**4)
        hmg_netsw[i,:]=(1-fphmg['ALBEDO'][0,:])*fphmg['SWDOWN'][0,:]
        hmg_gfx[i,:]=fphmg['GRDFLX'][0,:]
        hmg_glw[i,:]=fphmg['GLW'][0,:]*emissg

        het_netlw[i,:]=emisst*(fphet['GLW'][0,:]-stbolt*fphet['TSK'][0,:][:]**4)
        het_netsw[i,:]=(1-fphet['ALBEDO'][0,:])*fphet['SWDOWN'][0,:]
        het_gfx[i,:]=fphet['GRDFLX'][0,:]
        het_glw[i,:]=fphet['GLW'][0,:]*emisst

        #### FLUXES ####
        fphet.close()
        fphmg.close()
        i=i+1

    #### CREATE OUTPUT ####
    try:
        fp=nc.Dataset(odir+day+'_conv.nc','r+')
    except Exception:
        pass

    try:
        fp.createDimension('we'+dimscln,wescl)
        fp.createDimension('sn'+dimscln,snscl)
    except Exception:
        pass
    
    ggvars=['GFX_het','GFX_hmg','LWN_hmg','LWN_het','SWN_hmg','SWN_het','GLW_hmg','GLW_het']

    for var in ggvars:
        try:
            fp.createVariable(var,'f4',('time','sn', 'we'))
        except Exception:
            pass


    fp['GFX_hmg'][:,:,:]=hmg_gfx[:]
    fp['GFX_het'][:,:,:]=het_gfx[:]
    fp['LWN_hmg'][:,:,:]=hmg_netlw[:]
    fp['LWN_het'][:,:,:]=het_netlw[:]
    fp['SWN_hmg'][:,:,:]=hmg_netsw[:]
    fp['SWN_het'][:,:,:]=het_netsw[:]
    fp['GLW_hmg'][:,:,:]=hmg_glw[:]
    fp['GLW_het'][:,:,:]=het_glw[:]

    fp.close()


