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
hmg_dir='/home/tsw35/tyche/wrf_hrrr/tornado_1560_1040_60_169/OUTPUT/'
het_dir='/home/tsw35/tyche/wrf_hrrr/tornado_1560_1040_03_169/OUTPUT/'
#fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2022-03-21_23:00:00','r')
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2022-03-22_04:00:00','r')
fphet=nc.Dataset(het_dir+'wrfout_d01_2022-03-22_04:00:00','r')
#fphet=nc.Dataset(het_dir+'wrfout_d01_2022-03-21_23:00:00','r')

# %%
test=wrf.getvar(fphet, "updraft_helicity")
test2='hello!'

# %%

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
dltmax=np.nanpercentile(np.abs(data),99.9)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-dltmax,vmax=dltmax)
plt.axis(False)
plt.colorbar()

print(np.nanmean(data))
#plt.savefig('CLDF.png')
plt.show()

# %%
np.percentile(het_data,99.9)

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
minx=500
maxx=1000
miny=200
maxy=600

dx=maxx-minx
dy=maxy-miny

dhg=np.zeros((21,dy,dx))
dht=np.zeros((21,dy,dx))
drg=np.zeros((21,dy,dx))
drt=np.zeros((21,dy,dx))
dug=np.zeros((21,dy,dx))
dut=np.zeros((21,dy,dx))
msk=fphet['LU_INDEX'][0,miny:maxy,minx:maxx]==17
for t in range(21):
    if t<=(23-11):
        tt=t+11
    else:
        tt=t-13
    if tt<=9:
        fbase='wrfout_d01_2022-03-22_0'+str(tt)+':00:00'
    else:
        fbase='wrfout_d01_2022-03-21_'+str(tt)+':00:00'
    
    fphet=nc.Dataset(het_dir+fbase,'r')
    fphmg=nc.Dataset(hmg_dir+fbase,'r')
    
    dhg[t,:]=fphmg['HFX'][0,miny:maxy,minx:maxx]
    dhg[t,msk]=float('nan')
    dht[t,:]=fphet['HFX'][0,miny:maxy,minx:maxx]
    dht[t,msk]=float('nan')
    
    drg[t,:]=fphmg['RAINNC'][0,miny:maxy,minx:maxx]
    drg[t,msk]=float('nan')
    drt[t,:]=fphet['RAINNC'][0,miny:maxy,minx:maxx]
    drt[t,msk]=float('nan')
    
    dug[t,:]=wrf.getvar(fphmg, "updraft_helicity",meta=False)[miny:maxy,minx:maxx]
    dug[t,msk]=float('nan')
    dut[t,:]=wrf.getvar(fphet, "updraft_helicity",meta=False)[miny:maxy,minx:maxx]
    dut[t,msk]=float('nan')


# %%
print('DONE!!!!\n\n\n\n\n\nDONE!!!!')

# %%
vmax=max(np.nanpercentile(dug,99.9),np.nanpercentile(dut,99.9))
vmin=0

# %%
print(vmax)

# %%
### VIDEO ATTEMPT ####
fig = plt.figure(figsize=(6,4),dpi=200)
ax1=fig.add_subplot(211)
ax2=fig.add_subplot(212)
#cm=plt.cm.get_cmap('Blues')
vmax=75

def animate(i):
    print(i)
    data=dug[i,:,:]
    ax1.clear()
    #ax1.hist(data[data>1],bins=np.linspace(0,75,100))
    ax1.imshow(data,origin='lower',cmap='cool',vmax=vmax,vmin=0)
    ax1.axis('off')
    ax1.set_title('Homogenized')
    
    data=dut[i,:,:]
    ax2.clear()
    #ax2.hist(data[data>1],bins=np.linspace(0,75,100))
    ax2.imshow(data,origin='lower',cmap='cool',vmax=vmax,vmin=0)
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
mn_t=[]
mn_g=[]
p99_t=[]
p99_g=[]
for t in range(21):
    mn_t.append(np.nanmean(dut[t,:]))
    mn_g.append(np.nanmean(dug[t,:]))
    p99_t.append(np.nanpercentile(dut[t,:],99.9))
    p99_g.append(np.nanpercentile(dug[t,:],99.9))

# %%
plt.plot(p99_t,'--o')
plt.plot(p99_g,'--o')
plt.show()

# %%
fig = plt.figure(dpi=200)
ax1=fig.add_subplot(111)
#cm=plt.cm.get_cmap('Blues')
vmax=5
vmin=-5

def animate(i):
    data=(drt[i+1,:,:]-drt[i,:,:])-(drg[i+1,:,:]-drg[i,:,:])
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
pcftest=
