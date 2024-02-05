import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import os
import seaborn as sns
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.animation import FuncAnimation
import matplotlib
from IPython.display import HTML
import wrf
from sklearn.metrics import mean_squared_error
mpl.rcParams['figure.dpi'] = 200
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

data_dir=''
proc_dir='/home/tsw35/tyche/wrf_gaea/'
cum_dir=proc_dir+'all/'

fpht_dly=nc.Dataset(cum_dir+'daily_het.nc','r')
fphg_dly=nc.Dataset(cum_dir+'daily_hmg.nc','r')
fpst=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/201707_long/het/OUTPUT/static_data.nc','r')

rnht=fpht_dly['RAINNC24'][:]
rnhg=fphg_dly['RAINNC24'][:]

time=fpht_dly['time']

daylist=[]
for i in range(89):
    if np.sum(np.isnan(rnht[i,:,:]+rnhg[i,:,:]))>0:
        rnht[i,:,:]=float('nan')
        rnhg[i,:,:]=float('nan')
    else:
        daylist.append(i)

lum=fpst['LU_INDEX'][0,:,:]==17

rnht=np.nancumsum(rnht,axis=0)
rnhg=np.nancumsum(rnhg,axis=0)

for i in range(89):
    rnht[i,:,:][lum]=float('nan')
    rnhg[i,:,:][lum]=float('nan')

### VIDEO ATTEMPT ####
vmax=75
fig = plt.figure(figsize=(18,4),dpi=200)
ax1=fig.add_subplot(131)
ax2=fig.add_subplot(132)
ax3=fig.add_subplot(133)
#cm=plt.cm.get_cmap('Blues')

print('STARTING VIDEO',flush=True)

def animate(i):
    print(i,flush=True)
    j=daylist[i]
    data1=rnht[j,:,:]
    ax1.clear()
    #ax1.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax1.imshow(data1,origin='lower',cmap='terrain',vmin=0,vmax=800)
    ax1.axis('off')
    ax1.set_title('HET: '+str(time[j])[5:])
    
    data2=rnhg[j,:,:]
    ax2.clear()
    #ax2.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax2.imshow(data2,origin='lower',cmap='terrain',vmin=0,vmax=800)
    ax2.axis('off')
    ax2.set_title('HMG: '+str(time[j])[5:])
    #ax2.clear()
    
    data=data1-data2
    ax3.clear()
    #ax1.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax3.imshow(data,origin='lower',cmap='coolwarm',vmin=-200,vmax=200)
    ax3.axis('off')
    ax3.set_title('HET - HMG: '+str(time[j])[5:])

    fig.subplots_adjust(wspace=.05)
    
    return fig
    
ani=FuncAnimation(fig,animate,frames=83,interval=100,repeat=True)
FFwriter = matplotlib.animation.FFMpegWriter(fps=10)
ani.save('long_summer_cum24.mp4',writer=FFwriter)
