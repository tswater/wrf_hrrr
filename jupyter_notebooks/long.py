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
mpl.rcParams['figure.dpi'] = 200
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

# %%
hmg_dir='/home/tsw35/tyche/wrf_hrrr/201707_long/hom60/OUTPUT/'
het_dir='/home/tsw35/tyche/wrf_hrrr/201707_long/het/OUTPUT/'
fphmg=nc.Dataset(hmg_dir+'tsw2out_2017-07-18_19.nc','r')
fphet=nc.Dataset(het_dir+'tsw2out_2017-07-18_19.nc','r')
fphmg2=nc.Dataset(hmg_dir+'tsw2out_2017-07-17_00.nc','r')
fphet2=nc.Dataset(het_dir+'tsw2out_2017-07-17_00.nc','r')

# %%
data_trad=fphet['TSK'][0,:]
dzoom=fphet['TSK'][0,285:340,760:825]
data_trad[fpst['LU_INDEX'][0,:,:]==17]=float('nan')

# %%
data=fphet['SWDOWN'][0,:,:]
plt.imshow(data,cmap='terrain',origin='lower')

# %%
plt.imshow(dzoom,cmap='coolwarm',origin='lower',vmin=306,vmax=320)
plt.colorbar()

# %%
plt.imshow(fpst['EMISS'][0,285:340,760:825],origin='lower',cmap='tab20')
plt.colorbar()

# %%
fpst['LU_INDEX']

# %%
fpst=nc.Dataset(het_dir+'static_data.nc','r')

# %%
fig=plt.figure(figsize=(12,4))

# Bring in Data
hmg_hfx=fphmg['HFX'][0,:,:]
het_hfx=fphet['HFX'][0,:,:]

#var='CLDFRA'
#hmg_data=fphmg[var][0,12,:,:]
#het_data=fphet[var][0,12,:,:]

#var='CLDFRA'
#hmg_data=np.sum(fphmg[var][0,:,:,:],axis=0)
#het_data=np.sum(fphet[var][0,:,:,:],axis=0)

#var='lwp'
#hmg_data=fphmg[var][0,:,:]
#het_data=fphet[var][0,:,:]

#var='RAINNC'
#hmg_data=fphmg[var][0,:,:]
#het_data=fphet[var][0,:,:]

var='RAINNC'
hmg_data=fphmg[var][0,:,:]-fphmg2[var][0,:,:]
het_data=fphet[var][0,:,:]-fphet2[var][0,:,:]

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
data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
dltmax=np.nanpercentile(np.abs(data),99)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-dltmax,vmax=dltmax)
plt.axis(False)
plt.colorbar()

print(np.nanmean(data))
#plt.savefig('CLDF.png')
plt.show()


# %%
fphet['RAINNC']

# %%
fphet2=nc.Dataset(het_dir+'wrfout_d01_2017-07-18_05:00:00','r')
fphmg2=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-18_05:00:00','r')
fphet3=nc.Dataset(het_dir+'wrfout_d01_2017-07-17_09:00:00','r')
fphmg3=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-17_09:00:00','r')
data=(fphet2['RAINNC'][0,:,:]-fphet3['RAINNC'][0,:,:])-(fphmg2['RAINNC'][0,:,:]-fphmg3['RAINNC'][0,:,:])
data[fphet2['LU_INDEX'][0,:,:]==17]=float('nan')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-45,vmax=45)
plt.colorbar()
plt.show()

# %%
plt.figure(dpi=300)
fphet2=nc.Dataset(het_dir+'tsw2out_2017-07-17_20.nc','r')
fphmg2=nc.Dataset(hmg_dir+'tsw2out_2017-07-17_20.nc','r')
#fphet3=nc.Dataset(het_dir+'wrfout_d01_2017-07-17_09:00:00','r')
#fphmg3=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-17_09:00:00','r')
#data=(fphet2['RAINNC'][0,:,:])-(fphmg2['RAINNC'][0,:,:])
data=(fphet2['HFX'][0,:,:])-(fphmg2['HFX'][0,:,:])
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-100,vmax=100)
plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Difference in Cumulative Rainfall')
plt.show()

# %%
a=wrf.getvar(fphet,'cloudfrac',meta=False)

# %%
np.mean(fphmg2['SH2O'][0,0,:,:])

# %%
fig = plt.figure(figsize=(7,5),dpi=200)
subfigs = fig.subfigures(1, 1, hspace=.1,frameon=False)
# Build Grid
gd=[]
grid=ImageGrid(subfigs, 111,  # similar to subplot(111)
                 nrows_ncols=(1, 2),
                 axes_pad=0.1,
                 cbar_mode='single',
                 cbar_pad=.1,
                 cbar_size="10%")
data=fphmg2['SH2O'][0,0,:,:]
data=data[0:400,100:400]
im=grid[0].imshow(data,origin='lower',cmap='coolwarm',vmin=0,vmax=.3)
grid[0].axis(False)
grid[0].set_title('HMG Latent Heat\nGulf of California')

data=fphet2['SH2O'][0,0,:,:]
data=data[0:400,100:400]
im=grid[1].imshow(data,origin='lower',cmap='coolwarm',vmin=0,vmax=.3)
grid.cbar_axes[0].colorbar(im)
grid[1].axis(False)
grid[1].set_title('HET Latent Heat\nGulf of California')
plt.show()

# %%
plt.figure(dpi=300)
#fphet2=nc.Dataset(het_dir+'tsw2out_2017-07-17_17.nc','r')
#fphmg2=nc.Dataset(hmg_dir+'tsw2out_2017-07-17_17.nc','r')
fphet2=nc.Dataset(het_dir+'wrfout_d01_2017-07-17_17:00:00','r')
fphmg2=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-17_17:00:00','r')
#data=(fphet2['RAINNC'][0,:,:])-(fphmg2['RAINNC'][0,:,:])
#data=wrf.getvar(fphmg2,'lfc',meta=False)#fphmg2['PBLH'][0,:,:]
plt.subplot(1,2,1)
data=fphmg2['LH'][0,:,:]
data=data[0:400,100:400]
#data=np.sum((fphet2['QVAPOR'][0,:,:])-(fphmg2['QVAPOR'][0,:,:]),axis=0)
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=0,vmax=400)
plt.axis(False)
#plt.colorbar(shrink=.73)
plt.title('HMG Latent Heat\nGulf of California')

plt.subplot(1,2,2)
data=fphet2['LH'][0,:,:]
data=data[0:400,100:400]
#data=np.sum((fphet2['QVAPOR'][0,:,:])-(fphmg2['QVAPOR'][0,:,:]),axis=0)
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=0,vmax=400)
plt.axis(False)
#plt.colorbar(shrink=.73)
plt.title('HET Latent Heat\nGulf of California')

plt.show()
print(np.mean(data))

# %%

# %%
plt.figure(dpi=300)
#fphet3=nc.Dataset(het_dir+'wrfout_d01_2017-07-17_09:00:00','r')
#fphmg3=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-17_09:00:00','r')
#data=(fphet2['RAINNC'][0,:,:])-(fphmg2['RAINNC'][0,:,:])
data=fphet2['LH'][0,:,:]
data=data[0:400,100:400]
#data=np.sum((fphet2['QVAPOR'][0,:,:])-(fphmg2['QVAPOR'][0,:,:]),axis=0)
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=0,vmax=400)
plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Difference in Cumulative Rainfall')
plt.show()
print(np.mean(data))

# %%
plt.figure(dpi=300)
fphet2=nc.Dataset(het_dir+'tsw2out_2017-07-19_11.nc','r')
fphmg2=nc.Dataset(hmg_dir+'tsw2out_2017-07-19_11.nc','r')
#fphet3=nc.Dataset(het_dir+'wrfout_d01_2017-07-17_09:00:00','r')
#fphmg3=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-17_09:00:00','r')
data=(fphet2['RAINNC'][0,:,:])-(fphmg2['RAINNC'][0,:,:])
data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-75,vmax=75)
plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Difference in Cumulative Rainfall')
plt.show()

# %%
plt.figure(dpi=300)
fphet2=nc.Dataset(het_dir+'tsw2out_2017-07-19_11.nc','r')
fphmg2=nc.Dataset(hmg_dir+'tsw2out_2017-07-19_11.nc','r')
#fphet3=nc.Dataset(het_dir+'wrfout_d01_2017-07-17_09:00:00','r')
#fphmg3=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-17_09:00:00','r')
data=(fphet2['RAINNC'][0,:,:])-(fphmg2['RAINNC'][0,:,:])
data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data[250:350,500:800],origin='lower',cmap='coolwarm',vmin=-10,vmax=10)
plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Difference in Cumulative Rainfall')
plt.show()

# %%
print(np.nanmean(data[200:400,300:400]))

# %%
data.shape

# %%
data=precip[27,:,:]
data[fphet2['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='terrain')
plt.colorbar()
plt.show()

# %%

# %%
print(t)

# %%
lwp_het = np.zeros((73,data.shape[0],data.shape[1]))
lwp_hmg = np.zeros((73,data.shape[0],data.shape[1]))
flist=os.listdir(het_dir)
flist.sort()
t=0
for file in os.listdir(het_dir):
    if 'wrfout' in file:
        continue
    print(t,end=',',flush=True)
    fphet=nc.Dataset(het_dir+file,'r')
    fphmg=nc.Dataset(hmg_dir+file,'r')
    try:
        lwp_het[t,:]=fphet['lwp'][0,:,:]
        lwp_hmg[t,:]=fphmg['lwp'][0,:,:]
    except:
        print('ERROR')
        lwp_het[t,:]=float('nan')
        lwp_hmg[t,:]=float('nan')
    
    t=t+1

# %%
plt.figure(dpi=300)
data=np.nanmean(lwp_het-lwp_hmg,axis=0)
data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-.09,vmax=.09)
plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Difference in Mean LWP')
plt.show()

# %%

# %%
#### COMPARE PRECIP ####

# %%
flist=os.listdir('/home/tsw35/tyche/wrf_hrrr/20170717/radar/')
flist.sort()
precip=np.zeros((120,1039,1559))
t2m=np.zeros((120,1039,1559))
q2m=np.zeros((120,1039,1559))
t=0
for file in flist:
    if 'LDASIN' not in file:
        continue
    fp=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/20170717/radar/'+file,'r')
    precip[t,:,:]=fp['RAINRATE'][0,:,:]
    t2m[t,:,:]=fp['T2D'][0,:,:]
    q2m[t,:,:]=fp['Q2D'][0,:,:]
    t=t+1
    print('.',end='')

# %%
# Alternative Precip:
precip=np.zeros((48,1039,1559))

fp=nc.Dataset('/home/tsw35/tyche/data/GRBNC/data20170717.nc','r')
precip[0:24,:,:]=fp['Total Precipitation'][:]
fp=nc.Dataset('/home/tsw35/tyche/data/GRBNC/data20170718.nc','r')
precip[24:48,:,:]=fp['Total Precipitation'][:]

# %%
scls=['het','hom60']

# %%
pc=np.zeros((2,44,1039,1559))

# need to redo

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
    for i in range(2):
        diri='/home/tsw35/tyche/wrf_hrrr/201707_long/'+str(scls[i])+'/'
        if scls[i]=='het':
            fp=nc.Dataset(str(diri+fbase),'r')
        else:
            fp=nc.Dataset(str(diri+'OUTPUT/'+fbase),'r')
        pc[i,t,:,:]=fp['RAINNC'][0,:,:]
        print('.',end='',flush=True)

# %%
msk=fp['LU_INDEX'][0,:,:]!=17

rmse=np.zeros((7,21))
SS=np.zeros((7,21))

rhet=0
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
    for s in range(2):
        diri='/home/tsw35/tyche/wrf_hrrr/201707_long/'+str(scls[i])+'/'
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

for s in range(2):
    leg.append(scls[s])
    plt.plot(SS[s,:])
plt.legend(leg)
plt.xlim(0,20)
plt.show()

# %%
