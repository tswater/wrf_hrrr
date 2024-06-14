# CONVERT PYGRIB to NETCDF

import pygrib
import netCDF4 as nc
import numpy as np
import os
import subprocess as sp

#### USER INPUT ####
idir ='/home/tsw35/tyche/data/HRRRp/' 
odir ='/home/tsw35/tyche/data/GRBNC/'
vars =['Total Precipitation']
odims=[1039,1559]


flists={}
days=[]
crlst=os.listdir(idir)
crlst.sort()
for file in crlst:
    #6:14
    day=file[6:14]
    if day not in days:
        days.append(day)
        flists[day]=[]
    flists[day].append(file)

days=['20170717','20170718']

for day in days:
    print(day+': ',end='')
    fpo=nc.Dataset(odir+'data'+day+'.nc','w')
    fpo.createDimension('lat',odims[0])
    fpo.createDimension('lon',odims[1])
    fpo.createDimension('hour',24)
    for var in vars:
        fpo.createVariable(var,'f4',('hour','lat','lon'))
    t=0
    for file in flists[day]:
        print('.',end='',flush=True)
        fp=pygrib.open(idir+file)
        for var in vars:
            data=fp.select(name=var)[0].values
            xi=int((data.shape[0]-odims[0])/2)
            xf=-xi
            yi=int((data.shape[1]-odims[1])/2)
            yf=-yi
            try:
                fpo[var][t,:]=data[xi:xf,yi:yf]
            except Exception as e:
                print(xi)
                print(xf)
                print(yi)
                print(yf)
                print(data.shape)
                print(fpo[var].shape)
                raise e
        t=t+1
    fpo.close()
    print()



