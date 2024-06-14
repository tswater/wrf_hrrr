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
mpl.rcParams['figure.dpi'] = 300
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

# %%
hmg_dir='/home/tsw35/tyche/wrf_hrrr/conus_1764_1008_54_196TSK/OUTPUT/'
het_dir='/home/tsw35/tyche/wrf_hrrr/conus_1764_1008_03_196/OUTPUT/'
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-19_22:00:00','r')
fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-19_22:00:00','r')

# %%
fphet2=nc.Dataset(het_dir+'wrfout_d01_2017-07-20_05:00:00','r')
fphmg2=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-20_05:00:00','r')
data=fphet2['RAINNC'][0,:,:]-fphmg2['RAINNC'][0,:,:]
data[fphet2['LU_INDEX'][0,:,:]==17]=float('nan')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.show()

# %%
fphet2=nc.Dataset(het_dir+'wrfout_d01_2017-07-20_05:00:00','r')
fphmg2=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-20_05:00:00','r')
#[0,260:300,960:1010]
zis=960#750
zie=1010#1150
zjs=260#650
zje=300#900
data=fphet2['RAINNC'][0,zjs:zje,zis:zie]-fphmg2['RAINNC'][0,zjs:zje,zis:zie]
data[fphet2['LU_INDEX'][0,zjs:zje,zis:zie]==17]=float('nan')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.show()

# %%
dhg=np.zeros((20,zje-zjs,zie-zis))
dht=np.zeros((20,zje-zjs,zie-zis))
drg=np.zeros((20,zje-zjs,zie-zis))
drt=np.zeros((20,zje-zjs,zie-zis))
dvg=np.zeros((20,zje-zjs,zie-zis))
dvt=np.zeros((20,zje-zjs,zie-zis))
dug=np.zeros((20,zje-zjs,zie-zis))
dut=np.zeros((20,zje-zjs,zie-zis))
dwg=np.zeros((20,zje-zjs,zie-zis))
dwt=np.zeros((20,zje-zjs,zie-zis))
msk=fphet['LU_INDEX'][0,zjs:zje,zis:zie]==17
for t in range(20):
    if t<=(23-10):
        tt=t+10
    else:
        tt=t-14
    if tt<=9:
        fbase='wrfout_d01_2017-07-20_0'+str(tt)+':00:00'
    else:
        fbase='wrfout_d01_2017-07-19_'+str(tt)+':00:00'
    print(fbase)
    fphet=nc.Dataset(het_dir+fbase,'r')
    fphmg=nc.Dataset(hmg_dir+fbase,'r')
    
    dhg[t,:]=fphmg['HFX'][0,zjs:zje,zis:zie]
    dhg[t,msk]=float('nan')
    dht[t,:]=fphet['HFX'][0,zjs:zje,zis:zie]
    dht[t,msk]=float('nan')
    
    drg[t,:]=fphmg['RAINNC'][0,zjs:zje,zis:zie]
    drg[t,msk]=float('nan')
    drt[t,:]=fphet['RAINNC'][0,zjs:zje,zis:zie]
    drt[t,msk]=float('nan')
    
    dug[t,:]=fphmg['U'][0,3,zjs:zje,zis:zie]
    dug[t,msk]=float('nan')
    dut[t,:]=fphet['U'][0,3,zjs:zje,zis:zie]
    dut[t,msk]=float('nan')
    
    dvg[t,:]=fphmg['V'][0,3,zjs:zje,zis:zie]
    dvg[t,msk]=float('nan')
    dvt[t,:]=fphet['V'][0,3,zjs:zje,zis:zie]
    dvt[t,msk]=float('nan')
    
    dwg[t,:]=fphmg['W'][0,3,zjs:zje,zis:zie]
    dwg[t,msk]=float('nan')
    dwt[t,:]=fphet['W'][0,3,zjs:zje,zis:zie]
    dwt[t,msk]=float('nan')

# %%
plt.plot(np.nansum(drg[5:,:]>=1,axis=(1,2))/(40*40)*100,'k-')
plt.plot(np.nansum(drt[5:,:]>=1,axis=(1,2))/(40*40)*100,'k--')
plt.legend(['Homogenized (60km)','3km'])
plt.ylabel('Spatial Coverage of Rainfall (%)',fontsize=14)
plt.xlabel('Local Time (hr)',fontsize=14)
plt.xticks([0,2,4,6,8,10,12,14],[10,12,14,16,18,20,22,24])
plt.show()

# %%
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# %%
### VIDEO ATTEMPT ####
vmax=75
fig = plt.figure(figsize=(6,4),dpi=200)
ax1=fig.add_subplot(221)
ax2=fig.add_subplot(222)
ax3=fig.add_subplot(223)
ax4=fig.add_subplot(224)
#cm=plt.cm.get_cmap('Blues')

def animate(i):
    print(i)
    data=dug[i,:,:]
    ax1.clear()
    #ax1.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax1.imshow(data,origin='lower',cmap='PiYG',vmin=-10,vmax=10)
    ax1.axis('off')
    ax1.set_title('Homogenized')
    
    data=dut[i,:,:]
    ax2.clear()
    #ax2.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax2.imshow(data,origin='lower',cmap='PiYG',vmin=-10,vmax=10)
    ax2.axis('off')
    ax2.set_title('Heterogenenous')
    #ax2.clear()
    
    data=dhg[i,:,:]
    ax3.clear()
    #ax1.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax3.imshow(data,origin='lower',cmap='terrain',vmin=-100,vmax=500)
    ax3.axis('off')
    ax3.set_title('Homogenized')
    
    data=dht[i,:,:]
    ax4.clear()
    #ax2.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax4.imshow(data,origin='lower',cmap='terrain',vmin=-100,vmax=500)
    ax4.axis('off')
    ax4.set_title('Heterogenenous')
    #ax2.clear()
    
    
    #fig.subplots_adjust(wspace=.45, hspace=.45)
    
    return fig
    
ani=FuncAnimation(fig,animate,frames=20,interval=200,repeat=True)
#FFwriter = animation.FFMpegWriter(fps=10)
#ani.save('ani_1.mp4',writer=FFwriter)
HTML(ani.to_jshtml())
#HTML(ani.to_html5_video())

# %%
np.nanpercentile(np.abs(dwt),99.9)

# %%
ttt=19
msk_s=(drt[-1,:]>0)|(drg[-1,:]>0)
np.nanmean(drt[ttt,msk_s]-drg[ttt,msk_s])

# %%

# %%
data.shape

# %%
