# reproject MSWEP onto 3km WRF grid

import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import sys
import datetime
from mpi4py import MPI

# MPI4PY Stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

### USER INPUT ###
indir='/home/tsw35/tyche/wrf_gaea/'
odir='/home/tsw35/tyche/wrf_gaea/mswep_gaea/'

#fpout=nc.Dataset(odir+'mswep_gaea.nc','r')
#fp.createDimension('we',1559)
#fp.createDimension('time',1559)
#fp.createVariable(var,'f4',('time','sn', 'we'))

#152
#242

### LOOP THROUGH CONV FILES ###
cmd="gdalwarp -s_srs '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs' -t_srs '+proj=lcc +a=6370000 +b=6370000 +lat_0=38.5 +lon_0=-97.5 +lat_1=38.5 +lat_2=38.5' -te -2338500.0 -1558499.0 2338500.0 1558501.0 -tr 3000.0 3000.0 -r bilinear NETCDF:" 
#2023188.12.nc":precipitation
for year in [2021,2022]:
    for i in range(152,243):
        for j in [0,3,6,9,12,15,18,21]:
            if j<10:
                js='0'+str(j)
            else:
                js=str(j)
            oname=str(year)+str(i)+'.'+js+'.nc'
            cmdfull=cmd+'"/home/tsw35/xTyc_shared/MSWEP/'+oname+'":precipitation '+odir+oname
            run(cmdfull,shell=True)

