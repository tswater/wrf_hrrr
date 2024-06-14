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
#     display_name: Python 3 (ipykernel)
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
flist=os.listdir('/home/tsw35/tyche/wrf_hrrr/20170717/radar/')
flist.sort()
precip=np.zeros((96,1039,1559))
t2m=np.zeros((96,1039,1559))
q2m=np.zeros((96,1039,1559))
t=0
for file in flist:
    if 'LDASIN' not in file:
        continue
    if '20170716' in file:
        continue
    fp=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/20170717/radar/'+file,'r')
    precip[t,:,:]=fp['RAINRATE'][0,:,:]
    t2m[t,:,:]=fp['T2D'][0,:,:]
    q2m[t,:,:]=fp['Q2D'][0,:,:]
    t=t+1
    print('.',end='')

# %%
scls=['003','012','015','024','030','060','120']

# %%

# %%
pc=np.zeros((7,20,1039,1559))
lwp_=np.zeros((7,20,1039,1559))
pw_=np.zeros((7,20,1039,1559))

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
        #pres=fp['PH'][:]+fp['PHB'][:]
        #dpres=pres[:,1:,:,:]-pres[:,:-1,:,:]
        #lwp_[i,t,:,:]=np.sum(dpres/9.81*fp['QCLOUD'][:],axis=1)
        #pw_[i,t,:,:]=wrf.getvar(fp,'pw',meta=False)
        print('.',end='',flush=True)

# %%
t2m=np.zeros((7,20,1039,1559))
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
        t2m[i,t,:,:]=fp['T2'][0,:,:]

# %%
msk=fp['LU_INDEX'][0,:,:]!=17

rmse=np.zeros((7,21))
SS=np.zeros((7,21))

rhet=0
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
        
        rhet= pc[s,t,msk]
        if t>0:
            rhetp=pc[s,t-1,msk]
        
        rmse[s,t]=mean_squared_error(precip[tt,msk]*3600, rhet-rhetp, squared=False)
        if s>0:
            SS[s,t]=(rmse[0,t]-rmse[s,t])/(0-rmse[s,t])*100

# %%
plt.plot([0,20],[0,0],'w-',linewidth=3)
leg=[' ']

for s in range(7):
    leg.append(scls[s])
    plt.plot(SS[s,:])
plt.legend(leg)
plt.xlim(0,20)
plt.show()

# %%
np.mean(precip[10:30,msk]*3600)

# %%
for s in range(7):
    print(scls[s]+': '+str(np.mean(SS[s,10:19])))

# %%
s=-1
np.mean(pc[s,1:,msk]-pc[s,:-1,msk])

# %%

# %%
msk=fp['LU_INDEX'][0,:,:]!=17
rmse2=np.zeros((7,21))
drain=np.zeros((7,21))
for t in range(1,20):
    for s in range(7):
        rmse2[s,t]=mean_squared_error(sci.ndimage.filters.gaussian_filter(pc[0,t,msk],5,mode='reflect'),sci.ndimage.filters.gaussian_filter(pc[s,t,msk],5,mode='reflect'), squared=False)
#for s in range(7):
#    rmse2[s,21]=mean_squared_error(pc[0,20,msk],pc[s,20,msk], squared=False)

# %%
msk=fp['LU_INDEX'][0,:,:]!=17
rmse2=np.zeros((7,21))
drain=np.zeros((7,21))
for t in range(1,20):
    for s in range(7):
        rmse2[s,t]=mean_squared_error(pw_[0,t,msk],t2m[s,t,msk], squared=False)
#for s in range(7):
#    rmse2[s,21]=mean_squared_error(pc[0,20,msk],pc[s,20,msk], squared=False)

# %%
msk=fp['LU_INDEX'][0,:,:]!=17
rmse3=np.zeros((7,21))
drain=np.zeros((7,21))
for t in range(1,20):
    for s in range(7):
        rmse3[s,t]=mean_squared_error(pc[0,t,msk],pc[s,t,msk], squared=False)
#for s in range(7):
#    rmse2[s,21]=mean_squared_error(pc[0,20,msk],pc[s,20,msk], squared=False)

# %%
for s in range(7):
    rmse2[s,20]=mean_squared_error(pc[0,19,msk],pc[s,19,msk], squared=False)/np.mean(pc[0,t,msk]-pc[0,t-1,msk])

# %%
#plt.plot([0,20],[0,0],'w-',linewidth=3)
#leg=[' ']
leg=[]
sc=.7
plt.figure(figsize=(7*sc,4*sc))
colors=['lightsteelblue','powderblue','darkturquoise','cadetblue','steelblue','slategrey']
colors = plt.cm.cool(np.linspace(0,1,6))
for s in range(1,7):
    leg.append(scls[s])
    #plt.plot((rmse3[s,0:20]-rmse3[s-1,0:20])/(int(scls[s])/int(scls[s-1])))
    plt.plot(rmse3[s,0:20],c=colors[s-1])
plt.legend(leg,title='SCALE',fontsize=12,handlelength=1,labelspacing=.2)
plt.xticks([0,3,6,9,12,15,18])
plt.xlim(-.3,19.5)
plt.xlabel('Simulation Hour',fontsize=16)
#plt.ylim(0,2)
plt.ylabel('RMSE Rainfall',fontsize=16)
plt.show()

# %%
sint=[]
for s in range(7):
    sint.append(int(scls[s]))
sint=np.array(sint)

# %%
for s in range(7):
    print(scls[s]+': '+str(rmse3[s,20]))

# %%
mhg=[]
for i in range(7):
    Hgrad=np.array(np.gradient(H[i]))/3
    mhg.append(np.mean(np.sqrt(Hgrad[0]**2+Hgrad[1]**2)))

# %%

# %%
plt.figure(figsize=(10,3))
plt.plot(sint,mhg,'o-',color='slategrey',linewidth=3)
plt.xlabel('Homogenization Scale (km)',fontsize=16)
plt.ylabel(r'H Gradient $(W m^{-2}km^{-1})$',fontsize=16)
plt.show()

# %%
13*2

# %%
fbase='wrfout_d01_2017-07-17_20:00:00'
H=np.zeros((7,1039,1559))
for i in range(7):
    diri='/home/tsw35/tyche/wrf_hrrr/20170717/1560_1040_'+str(scls[i])+'_169/'
    fp=nc.Dataset(str(diri+'OUTPUT/'+fbase),'r')
    H[i,:,:]=fp['HFX'][0,:,:]

# %%

# %%
data3=H[0,:]
vmin=np.percentile(data3,2)
vmax=np.percentile(data3,99)
for i in range(7):
    plt.figure(dpi=300)
    plt.imshow(H[i,:,:],cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
    plt.axis(False)
plt.show()

# %%
data3=H[0,:]
vmin=np.percentile(data3,2)
vmax=np.percentile(data3,99)
plt.figure(dpi=300)
plt.imshow(H[0,:,:],cmap='terrain',origin='lower',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.savefig('quick')


# %%
data3=H[0,200:700,1000:1500]
vmin=np.percentile(data3,2)
vmax=np.percentile(data3,99)
plt.figure(figsize=(4,6))
plt.subplot(3,2,1)
data=H[0,200:700,1000:1500]
plt.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.title('3 km')

plt.subplot(3,2,2)
data=H[1,200:700,1000:1500]
plt.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.title('12 km')


plt.subplot(3,2,3)
data=H[3,200:700,1000:1500]
plt.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.title('24 km')


plt.subplot(3,2,4)
data=H[4,200:700,1000:1500]
plt.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.title('30 km')


plt.subplot(3,2,5)
data=H[5,200:700,1000:1500]
plt.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.title('60 km')

plt.subplot(3,2,6)
data=H[6,200:700,1000:1500]
plt.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.title('120 km')

plt.show()

# %%
import scipy as sci

# %%
#sci.ndimage.filters.gaussian_filter(pw_[0,13,:,:],10,mode='reflect')

data=sci.ndimage.filters.gaussian_filter(pw_[0,13,:,:],5,mode='reflect')-sci.ndimage.filters.gaussian_filter(pw_[1,13,:,:],5,mode='reflect')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.show()

# %%
np.std(lwp_[0,:,:,:])

# %%
np.std(lwp_[6,:,:,:])

# %%
np.std(pw_[0,:,:,:])

# %%
np.std(pw_[6,:,:,:])

# %%
