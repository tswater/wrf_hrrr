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
mpl.rcParams['figure.dpi'] = 300
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

# %%
hmg_dir='/home/tsw35/tyche/wrf_hrrr/20180709/1560_1040_060_169/OUTPUT/'
het_dir='/home/tsw35/tyche/wrf_hrrr/20180709/1560_1040_003_169/OUTPUT/'
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2018-07-09_22:00:00','r')
fphet=nc.Dataset(het_dir+'wrfout_d01_2018-07-09_22:00:00','r')

# %%
fig=plt.figure(figsize=(12,4))

# Bring in Data
hmg_hfx=fphmg['HFX'][0,:,:]
het_hfx=fphet['HFX'][0,:,:]

#var='CLDFRA'
#hmg_data=fphmg[var][0,12,:,:]
#het_data=fphet[var][0,12,:,:]

var='CLDFRA'
hmg_data=np.sum(fphmg[var][0,:,:,:],axis=0)
het_data=np.sum(fphet[var][0,:,:,:],axis=0)

#var='RAINNC'
#hmg_data=fphmg[var][0,:,:]
#het_data=fphet[var][0,:,:]

# Set Vmins/Vmaxs
vminA=max(np.min(hmg_hfx),np.min(het_hfx))
vmaxA=min(np.max(hmg_hfx),np.max(het_hfx))

vminB=max(np.min(hmg_data),np.min(het_data))
vmaxB=min(np.max(hmg_data),np.max(het_data))

plt.subplot(2,3,1)
plt.title('HMG - HFX')
plt.imshow(hmg_hfx,origin='lower',cmap='coolwarm',vmin=vminA,vmax=vmaxA)
plt.axis(False)
plt.colorbar()

plt.subplot(2,3,2)
plt.title('HET - HFX')
plt.imshow(het_hfx,origin='lower',cmap='coolwarm',vmin=vminA,vmax=vmaxA)
plt.axis(False)
plt.colorbar()

plt.subplot(2,3,3)
plt.title('DELTA - HFX')
data=(het_hfx-hmg_hfx)/np.max(np.abs(het_hfx))*100
dltmax=np.percentile(np.abs(data),95)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-dltmax,vmax=dltmax)
plt.axis(False)
plt.colorbar()

plt.subplot(2,3,4)
plt.title('HMG - '+str(var))
plt.imshow(hmg_data,origin='lower',cmap='terrain',vmin=vminB,vmax=vmaxB)
plt.axis(False)
plt.colorbar()

plt.subplot(2,3,5)
plt.title('HET - '+str(var))
plt.imshow(het_data,origin='lower',cmap='terrain',vmin=vminB,vmax=vmaxB)
plt.axis(False)
plt.colorbar()

plt.subplot(2,3,6)
plt.title('DELTA - '+str(var))
data=(het_data-hmg_data)
print(np.nanmean(data))
data[fphet['LU_INDEX'][0,:,:]==17]=float('nan')
dltmax=np.nanpercentile(np.abs(data),99)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-dltmax,vmax=dltmax)
plt.axis(False)
plt.colorbar()

print(np.nanmean(data))
#plt.savefig('CLDF.png')
plt.show()


# %%
fphmg2=nc.Dataset(hmg_dir+'wrfout_d01_2018-07-10_05:00:00','r')
fphet2=nc.Dataset(het_dir+'wrfout_d01_2018-07-10_05:00:00','r')
data=fphet2['RAINNC'][0,:,:]-fphmg2['RAINNC'][0,:,:]
data[fphet2['LU_INDEX'][0,:,:]==17]=float('nan')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.show()

# %%
flist=os.listdir('/home/tsw35/tyche/wrf_hrrr/20180709/radar/')
flist.sort()
precip=np.zeros((48,1039,1559))
t2m=np.zeros((48,1039,1559))
q2m=np.zeros((48,1039,1559))
t=0
for file in flist:
    if 'LDASIN' not in file:
        continue
    fp=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/20180709/radar/'+file,'r')
    precip[t,:,:]=fp['RAINRATE'][0,:,:]
    t2m[t,:,:]=fp['T2D'][0,:,:]
    q2m[t,:,:]=fp['Q2D'][0,:,:]
    t=t+1
    print('.',end='')

# %%
p_het=np.zeros((20,1039,1559))
p_hmg=np.zeros((20,1039,1559))

t_het=np.zeros((20,1039,1559))
t_hmg=np.zeros((20,1039,1559))

q_het=np.zeros((20,1039,1559))
q_hmg=np.zeros((20,1039,1559))

for t in range(20):
    if t<=(23-10):
        tt=t+10
    else:
        tt=t-14
    if tt<=9:
        fbase='wrfout_d01_2018-07-10_0'+str(tt)+':00:00'
    else:
        fbase='wrfout_d01_2018-07-09_'+str(tt)+':00:00'
    print(fbase)
    fphet=nc.Dataset(het_dir+fbase,'r')
    fphmg=nc.Dataset(hmg_dir+fbase,'r')
    p_het[t,:]=fphet['RAINNC'][0,:,:]
    p_hmg[t,:]=fphmg['RAINNC'][0,:,:]
    
    q_het[t,:]=fphet['Q2'][0,:,:]
    q_hmg[t,:]=fphmg['Q2'][0,:,:]
    
    t_het[t,:]=fphet['T2'][0,:,:]
    t_hmg[t,:]=fphmg['T2'][0,:,:]

# %%
from sklearn.metrics import mean_squared_error

# %%
msk=fphet['LU_INDEX'][0,:,:]!=17

rmse_q=[]
rmse_t=[]
rmse_p=[]
rmseG_q=[]
rmseG_t=[]
rmseG_p=[]

SS_q=[]
SS_t=[]
SS_p=[]

rhetp=0
rhmgp=0

for t in range(20):
    print(t)
    tt=t+10
    
    rhet= p_het[t,msk]
    rhmg= p_hmg[t,msk]
    
    rmse_p.append(mean_squared_error(precip[tt,msk]*3600, rhet-rhetp, squared=False))
    rmseG_p.append(mean_squared_error(precip[tt,msk]*3600, rhmg-rhmgp, squared=False))
    SS_p.append((rmse_p[-1]-rmseG_p[-1])/(0-rmseG_p[-1])*100)
    
    rmse_t.append(mean_squared_error(t2m[tt,msk], t_het[t,msk], squared=False))
    rmseG_t.append(mean_squared_error(t2m[tt,msk], t_hmg[t,msk], squared=False))
    SS_t.append((rmse_t[-1]-rmseG_t[-1])/(0-rmseG_t[-1])*100)
    
    rmse_q.append(mean_squared_error(q2m[tt,msk], q_het[t,msk], squared=False))
    rmseG_q.append(mean_squared_error(q2m[tt,msk], q_hmg[t,msk], squared=False))
    SS_q.append((rmse_q[-1]-rmseG_q[-1])/(0-rmseG_q[-1])*100)
    
    rhetp=rhet[:]
    rhmgp=rhmg[:]

# %%
rmse_p.append(mean_squared_error(np.sum(precip[10:30,msk]*3600,axis=0), rhet, squared=False))
rmseG_p.append(mean_squared_error(np.sum(precip[10:30,msk]*3600,axis=0), rhmg, squared=False))
SS_p.append((rmse_p[-1]-rmseG_p[-1])/(0-rmseG_p[-1])*100)
    
rmse_t.append(mean_squared_error(t2m[10:30,msk], t_het[0:20,msk], squared=False))
rmseG_t.append(mean_squared_error(t2m[10:30,msk], t_hmg[0:20,msk], squared=False))
SS_t.append((rmse_t[-1]-rmseG_t[-1])/(0-rmseG_t[-1])*100)
    
rmse_q.append(mean_squared_error(q2m[10:30,msk], q_het[0:20,msk], squared=False))
rmseG_q.append(mean_squared_error(q2m[10:30,msk], q_hmg[0:20,msk], squared=False))
SS_q.append((rmse_q[-1]-rmseG_q[-1])/(0-rmseG_q[-1])*100)

# %%
plt.plot([0,21],[0,0],'w-',linewidth=3)
plt.plot(SS_t)
plt.plot(SS_q)
plt.plot(SS_p)
plt.xlim(0,21)
plt.show()

# %%
