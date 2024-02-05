import numpy as np
import os
from subprocess import run
import netCDF4 as nc
import time

start_time = time.time()

gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'

filelist=[]

for day in os.listdir(gaea_dir):
    for file in os.listdir(gaea_dir+day):
        filelist.append(gaea_dir+day+'/'+file)

print(len(filelist))
n=len(filelist)
i=0
for file in filelist:
    fp=nc.Dataset(file,'r')
    a=np.mean(fp['QCLOUD'][:])
    print(str(time.time()-start_time)+': '+str(i/n*100)[0:4])
    i=i+1
    if i>84:
        break


