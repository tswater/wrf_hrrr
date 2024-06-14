import os
import netCDF4 as nc
from subprocess import run

from mpi4py import MPI

# MPI4PY Stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()



ggvars=['GFX_het','GFX_hmg','LWN_hmg','LWN_het','SWN_hmg','SWN_het','GLW_hmg','GLW_het']

odir='/home/tsw35/tyche/wrf_gaea/'
scl=20
dimscln=str(int(scl*3))
wescl=int((1559+1)/scl)
snscl=int((1039+1)/scl)
we=1559
sn=1039
N=49

run('mkdir '+odir+'tmp',shell=True)

flist=os.listdir(odir)
flist.sort()

for file in flist[rank::size]:
    if 'conv' not in file:
        continue
    print(str(rank)+': '+file)
    run('mv '+odir+file+' '+odir+'tmp/'+file,shell=True)
    fpi=nc.Dataset(odir+'tmp/'+file,'r')
    fpo=nc.Dataset(odir+file,'w')
    fpo.createDimension('we',1559)
    fpo.createDimension('sn',1039)
    fpo.createDimension('time',N)
    fpo.createDimension('we'+dimscln,wescl)
    fpo.createDimension('sn'+dimscln,snscl)
    fpo.createDimension('z',50)
    for v in fpi.variables:
        if v in ggvars:
            continue
        print(str(rank)+': '+str(v)+' : '+file,flush=True)
        fpo.createVariable(v,'f4',fpi[v].dimensions)
        fpo[v][:]=fpi[v][:]
    fpi.close()
    fpo.close()

