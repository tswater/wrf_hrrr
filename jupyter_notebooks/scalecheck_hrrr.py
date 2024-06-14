# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import os
import seaborn as sns
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import wrf
from sklearn.metrics import mean_squared_error
mpl.rcParams['figure.dpi'] = 300
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

# %%
precip=np.zeros((48,1039,1559))
t2m=np.zeros((48,1039,1559))
q2m=np.zeros((48,1039,1559))
#t=0

fp=nc.Dataset('/home/tsw35/tyche/data/GRBNC/data20170717.nc','r')
precip[0:24,:,:]=fp['Total Precipitation'][:]
fp=nc.Dataset('/home/tsw35/tyche/data/GRBNC/data20170718.nc','r')
precip[24:48,:,:]=fp['Total Precipitation'][:]
#for file in flist:
#    if 'LDASIN' not in file:
#        continue
#    fp=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/20170717/radar/'+file,'r')
#    precip[t,:,:]=fp['RAINRATE'][0,:,:]
    #t2m[t,:,:]=fp['T2D'][0,:,:]
    #q2m[t,:,:]=fp['Q2D'][0,:,:]
#    t=t+1
#    print('.',end='')

# %%
scls=['003','012','015','024','030','060','120']

# %%
#pc=np.zeros((7,20,1039,1559))

for t in range(20):
    if t<=(23-10):
        tt=t+10
    else:
        tt=t-14
    if tt<=9:
        fbase='wrfout_d01_2017-07-18_0'+str(tt)+':00:00'
    else:
        fbase='wrfout_d01_2017-07-17_'+str(tt)+':00:00'
    print(fbase+'::',end='')
    for i in range(7):
        diri='/home/tsw35/tyche/wrf_hrrr/20170717/1560_1040_'+str(scls[i])+'_169/'
        fp=nc.Dataset(str(diri+'OUTPUT/'+fbase),'r')
        pc[i,t,:,:]=fp['RAINNC'][0,:,:]
        print('.',end='',flush=True)

# %%
np.mean(precip)

# %%
msk=fp['LU_INDEX'][0,:,:]!=17

rmse=np.zeros((7,21))
SS=np.zeros((7,21))

rhetp=0
rhmgp=0

for t in range(20):
    print(t)
    tt=t+10
    if t<=(23-10):
        ttt=t+10
    else:
        ttt=t-14
    if ttt<=9:
        fbase='wrfout_d01_2017-07-18_0'+str(ttt)+':00:00'
    else:
        fbase='wrfout_d01_2017-07-17_'+str(ttt)+':00:00'
    for s in range(7):
        diri='/home/tsw35/tyche/wrf_hrrr/20170717/1560_1040_'+str(scls[s])+'_169/'
        fp=nc.Dataset(str(diri+'OUTPUT/'+fbase),'r')
        
        rhet= pc[s,t,msk]
        if t>0:
            rhetp=pc[s,t-1,msk]
        
        rmse[s,t]=mean_squared_error(precip[tt,msk], rhet-rhetp, squared=False)
        if s>0:
            SS[s,t]=(rmse[0,t]-rmse[s,t])/(0-rmse[s,t])*100

# %%
plt.plot([0,20],[0,0],'w-',linewidth=3)
leg=[' ']

for s in range(7):
    leg.append(scls[s])
    plt.plot(SS[s,:-1])
plt.legend(leg)
plt.xlim(0,20)
plt.show()

# %%
for s in range(7):
    print(scls[s]+': '+str(np.mean(SS[s,10:19])))

# %%
plt.bar(scls,np.mean(SS[:,10:19],axis=1))
plt.xlabel('Averaging Scale')
plt.ylabel('$\Delta RMSE$')
plt.show()

# %%
plt.plot([0,20],[0,0],'w-',linewidth=3)
leg=[' ']

for s in range(7):
    leg.append(scls[s])
    plt.plot(rmse[s,:])
plt.legend(leg)
plt.xlim(0,20)
#plt.ylim(0.5,1.6)
plt.show()

# %%
