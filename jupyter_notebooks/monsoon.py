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
hmg_dir='/home/tsw35/tyche/wrf_hrrr/monsoon_1560_1040_60_169/OUTPUT/'
het_dir='/home/tsw35/tyche/wrf_hrrr/monsoon_1560_1040_03_169/OUTPUT/'
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2022-08-04_01:00:00','r')
fphet=nc.Dataset(het_dir+'wrfout_d01_2022-08-04_01:00:00','r')

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

var='RAINNC'
hmg_data=fphmg[var][0,:,:]
het_data=fphet[var][0,:,:]

#var='UH'
#het_data=wrf.getvar(fphet, "updraft_helicity",meta=False)
#hmg_data=wrf.getvar(fphmg, "updraft_helicity",meta=False)

# Set Vmins/Vmaxs
vminA=max(np.percentile(hmg_hfx,.1),np.percentile(het_hfx,.1))
vmaxA=min(np.percentile(hmg_hfx,99.9),np.percentile(het_hfx,99.9))

vminB=max(np.percentile(hmg_data,.1),np.percentile(het_data,.1))
vmaxB=min(np.percentile(hmg_data,99.9),np.percentile(het_data,99.9))

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
vmin=-np.nanpercentile(np.abs(data),99.5)
vmax=np.nanpercentile(np.abs(data),99.5)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.show()

# %%
#data=rainhet[-1]-rainhmg[-1]
vmin=-np.nanpercentile(np.abs(data[300:600,200:600]),99)
vmax=np.nanpercentile(np.abs(data[300:600,200:600]),99)
plt.imshow(data[300:600,200:600],origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.show()
print(np.nanmean(data[300:600,200:600]))

# %%
dhg=np.zeros((20,300,400))
dht=np.zeros((20,300,400))
drg=np.zeros((20,300,400))
drt=np.zeros((20,300,400))
msk=fphet['LU_INDEX'][0,300:600,200:600]==17
for t in range(20):
    if t<=(23-10):
        tt=t+10
    else:
        tt=t-14
    if tt<=5:
        fbase='wrfout_d01_2022-08-04_0'+str(tt)+':00:00'
    else:
        fbase='wrfout_d01_2022-08-03_'+str(tt)+':00:00'
    print(fbase)
    fphet=nc.Dataset(het_dir+fbase,'r')
    fphmg=nc.Dataset(hmg_dir+fbase,'r')
    
    dhg[t,:]=fphmg['HFX'][0,300:600,200:600]
    dhg[t,msk]=float('nan')
    dht[t,:]=fphet['HFX'][0,300:600,200:600]
    dht[t,msk]=float('nan')
    
    drg[t,:]=fphmg['RAINNC'][0,300:600,200:600]
    drg[t,msk]=float('nan')
    drt[t,:]=fphet['RAINNC'][0,300:600,200:600]
    drt[t,msk]=float('nan')

# %%

# %%
vmax=max(np.nanpercentile(drg,99),np.nanpercentile(drt,99))
vmin=0

# %%

# %%
### VIDEO ATTEMPT ####
fig = plt.figure(figsize=(6,4),dpi=200)
ax1=fig.add_subplot(211)
ax2=fig.add_subplot(212)
#cm=plt.cm.get_cmap('Blues')

def animate(i):
    print(i)
    data=drg[i,:,:]
    ax1.clear()
    ax1.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax1.axis('off')
    ax1.set_title('Homogenized')
    
    data=drt[i,:,:]
    ax2.clear()
    ax2.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax2.axis('off')
    ax2.set_title('Heterogenenous')
    #ax2.clear()
    
    
    #fig.subplots_adjust(wspace=.45, hspace=.45)
    
    return fig
    
ani=FuncAnimation(fig,animate,frames=20,interval=200,repeat=True)
#FFwriter = animation.FFMpegWriter(fps=10)
#ani.save('ani_1.mp4',writer=FFwriter)
HTML(ani.to_jshtml())
#HTML(ani.to_html5_video())

# %%
fig = plt.figure(dpi=200)
ax1=fig.add_subplot(111)
#cm=plt.cm.get_cmap('Blues')
vmax=30
vmin=-30

def animate(i):
    data=drt[i,:,:]-drg[i,:,:]
    ax1.clear()
    ax1.imshow(data,origin='lower',cmap='coolwarm',vmax=vmax,vmin=vmin)
    ax1.axis('off')
    
    return fig
    
ani=FuncAnimation(fig,animate,frames=20,interval=200,repeat=True)
#FFwriter = animation.FFMpegWriter(fps=10)
#ani.save('ani_1.mp4',writer=FFwriter)
HTML(ani.to_jshtml())
#HTML(ani.to_html5_video())

# %%
