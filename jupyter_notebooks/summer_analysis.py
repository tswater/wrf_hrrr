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
import matplotlib
from IPython.display import HTML
import wrf
from sklearn.metrics import mean_squared_error
from matplotlib.gridspec import GridSpec
mpl.rcParams['figure.dpi'] = 200
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

# %%
data_dir=''
proc_dir='/home/tsw35/tyche/wrf_gaea/'
cum_dir=proc_dir+'all/'

# %%
fpst=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/201707_long/het/OUTPUT/static_data.nc','r')

# %%
fphet=nc.Dataset(cum_dir+'cum_het.nc','r')
fphmg=nc.Dataset(cum_dir+'cum_hmg.nc','r')

# %%
ht_lwp=fphet['LWP'][:]
ht_prcp=fphet['RAINNC'][:]
hg_lwp=fphmg['LWP'][:]
hg_prcp=fphmg['RAINNC'][:]
delta_lwp=ht_lwp-hg_lwp
delta_prcp=ht_prcp-hg_prcp

# %%
vmax=np.percentile(ht_lwp,99)
vmin=0
plt.imshow(ht_lwp,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Heterogeneous LWP')
plt.show()

# %%
vmax=np.percentile(hg_lwp,99)
vmin=0
plt.imshow(hg_lwp,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Homogeneous LWP')
plt.show()

# %%
vmax=np.percentile(delta_lwp,99)
vmin=-vmax
data=delta_lwp.copy()
#data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
#data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Delta LWP')
plt.show()

# %%
vmax=np.percentile(ht_prcp,99)
vmin=0
data=ht_prcp.copy()
data[data==0]=float('nan')
plt.imshow(data,origin='lower',cmap='terrain',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Heterogeneous Precip')
plt.show()

# %%
vmax=np.percentile(hg_prcp,99)
vmin=0
plt.imshow(hg_prcp,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Homogeneous Precip')
plt.show()

# %%
plt.figure(dpi=400)
data=delta_prcp/sci.ndimage.filters.gaussian_filter(ht_prcp,sigma=10,mode='reflect')*100
vmax=100#np.percentile(np.abs(data),97)
vmin=-vmax
#data=delta_prcp.copy()
data=sci.ndimage.filters.gaussian_filter(data,sigma=10,mode='reflect')
data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
#plt.axis(False)
plt.colorbar(shrink=.73,label=r'%$\Delta$ Precipitation')
plt.title(r'$\Delta$ Precipitation (3km - 60km)')
plt.xticks([0,200,400,600,800,1000,1200,1400],[])
plt.yticks([0,200,400,600,800,1000],[])
plt.show()

# %%
vmax=np.percentile(delta_prcp,99)
vmin=-vmax
data=delta_prcp.copy()
import scipy as sci
#data=sci.ndimage.filters.gaussian_filter(data,sigma=10,mode='reflect')
data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
#plt.axis(False)
plt.colorbar(shrink=.73,label=r'$\Delta$ Precipitation (mm)')
plt.title(r'$\Delta$ Precipitation (3km - 60km)')
plt.xticks([0,200,400,600,800,1000,1200,1400],[])
plt.yticks([0,200,400,600,800,1000],[])
plt.show()

# %%

# %%
data=fpst['LU_INDEX'][0,:,:]
plt.imshow(data,cmap='tab20',origin='lower')
plt.colorbar(shrink=.73)

# %%
print(np.mean(delta_prcp))

# %%
fpht_dly=nc.Dataset(cum_dir+'daily_het.nc','r')
fphg_dly=nc.Dataset(cum_dir+'daily_hmg.nc','r')

# %%
rnht=fpht_dly['RAINNC'][:]
rnhg=fphg_dly['RAINNC'][:]

# %%

# %%
daylist=[]
for i in range(89):
    if np.sum(np.isnan(rnht[i,:,:]+rnhg[i,:,:]))>0:
        rnht[i,:,:]=float('nan')
        rnhg[i,:,:]=float('nan')
    else:
        daylist.append(i)

# %%
countht=np.zeros((a[0,:,:].shape))
counthg=np.zeros((a[0,:,:].shape))
for i in range(89):
    countht=countht+(rnht[i,:,:]>5)
    counthg=counthg+(rnhg[i,:,:]>5)

# %%
data=count
data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='terrain')
#plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Precip Events')
plt.show()

# %%
data=countht-counthg
data[np.abs(data)<5]=0
data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-10,vmax=10)
#plt.axis(False)
plt.colorbar(shrink=.73)
plt.title('Precip Events')
plt.show()

# %%
time=fpht_dly['time']

# %%
lum=fpst['LU_INDEX'][0,:,:]==17

# %%
for i in range(89):
    rnht[i,:,:][lum]=float('nan')
    rnhg[i,:,:][lum]=float('nan')

# %%
a=np.nancumsum(rnht,axis=0)

# %%
plt.imshow(a[10,:,:])
plt.colorbar()

# %%
plt.figure(figsize=(6,12),dpi=200)
sd
plt.subplot(3,1,1)
plt.title('HET - ')
plt.imshow(rnht[5,:,:],origin='lower',cmap='terrain',vmin=0,vmax=50)
plt.xticks([])
plt.yticks([])
plt.subplot(3,1,2)
plt.title('HMG - ')
plt.imshow(rnhg[5,:,:],origin='lower',cmap='terrain',vmin=0,vmax=50)
plt.xticks([])
plt.yticks([])
plt.subplot(3,1,3)
plt.title('HET - HMG')
plt.imshow(rnht[5,:,:]-rnhg[5,:,:],origin='lower',cmap='coolwarm',vmin=-50,vmax=50)
plt.xticks([])
plt.yticks([])
plt.subplots_adjust(hspace=.1)

# %%
#fpht_dly.close()
#fphg_dly.close()

# %%
fptest=nc.Dataset('/home/tsw35/xTyc_shared/compressed_output/20230617_het/cmp_2023-06-17_19:00:00','r')

# %%
H=fptest['HFX'][0,:,:]


# %%
def vari(data,df=20):
    ni=data.shape[0]
    nj=data.shape[1]
    dout=np.zeros((ni,nj))
    for i in range(int((ni+1)/df)):
        for j in range(int((nj+1)/df)):
            dout[i*df:(i+1)*df,j*df:(j+1)*df] = np.nanvar(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout       


# %%
hvar=vari(H)

# %%
fp.close()

# %%
plt.imshow(Hvsum,origin='lower',cmap='terrain')
plt.xticks([0,200,400,600,800,1000,1200,1400],[])
plt.yticks([0,200,400,600,800,1000],[])
plt.colorbar(shrink=.73)

# %%
plt.imshow(fp['RAINNC_het'][36,:,:]-fp['RAINNC_hmg'][36,:,:],origin='lower',cmap='coolwarm',vmin=-50,vmax=50)
plt.colorbar()

# %%
lie=np.linspace(0,1)

# %%
fp=nc.Dataset('/home/tsw35/tyche/wrf_gaea/20230601_conv.nc','r')

# %%
fp

# %%
a=fp['RAINNC_het'][:]

# %%
test=fp['5mmTime0_48'][:]

# %%
# ls '/home/tsw35/tyche/wrf_gaea/'

# %%
test[0,:,:]

# %%
fpt=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/daily_het.nc','r')
fpg=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/daily_hmg.nc','r')

# %%
fpt

# %%
t=1
data=fpt['1mmTime0_48'][t,:,:]-fpg['1mmTime0_48'][t,:,:]
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-5,vmax=5)
plt.colorbar()

# %%
i=0
Hvsum=np.zeros((1039, 1559))
for file in os.listdir('/home/tsw35/tyche/wrf_gaea'):
    if 'all' in file:
        continue
    fpsum=nc.Dataset('/home/tsw35/tyche/wrf_gaea/'+file,'r')
    Hvsum=Hvsum+np.sum(fpsum['HFX_hetvar'][:,:,:],axis=0)
    i=i+fpsum['HFX_hetvar'][:,:,:].shape[0]
    print(i,end=',')
Hvsum=Hvsum/i

# %%
plt.imshow(Hvsum,origin='lower',cmap='turbo',vmax=15000,interpolation='none')
plt.xticks([0,200,400,600,800,1000,1200,1400],[])
plt.yticks([0,200,400,600,800,1000],[])
plt.colorbar(shrink=.73)
plt.axis(False)
plt.title(r'Variability Loss ($\sigma_H$)')

# %%
# ls '/home/tsw35/xTyc_shared/compressed_output/20230609_het'

# %%
fp=nc.Dataset('/home/tsw35/xTyc_shared/compressed_output/'+'20230609_het/cmp_2023-06-09_19:00:00','r')
data=fp['HFX'][0,:,:]
vmin=np.percentile(data,2)
vmax=np.percentile(data,99)
plt.figure(dpi=300)
plt.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.show()

# %%
fp=nc.Dataset('/home/tsw35/xTyc_shared/compressed_output/'+'20230716_het/cmp_2023-07-16_19:00:00','r')
data=fp['HFX'][0,:,:]
#vmin=np.percentile(data,2)
#vmax=np.percentile(data,99)
plt.figure(dpi=300)
plt.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.show()

# %%

# %%
fp=nc.Dataset('/home/tsw35/xTyc_shared/compressed_output/'+'20230813_het/cmp_2023-08-13_19:00:00','r')
data=fp['HFX'][0,:,:]
#vmin=np.percentile(data,2)
#vmax=np.percentile(data,99)
plt.figure(dpi=300)
plt.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
plt.axis(False)
plt.show()

# %%
t=19
d='20230810'
dd=d[0:4]+'-'+d[4:6]+'-'+str(int(d[6:8])+1)+'_'+str(t)

fig=plt.figure(figsize=(8.5,4),dpi=300)
gs = GridSpec(2, 3, figure=fig)
fphet=nc.Dataset('/home/tsw35/xTyc_shared/compressed_output/'+d+'_het/cmp_'+dd+':00:00','r')
fphmg=nc.Dataset('/home/tsw35/xTyc_shared/compressed_output/'+d+'_hmg/cmp_'+dd+':00:00','r')

ax=fig.add_subplot(gs[0,0])
data=fphet['HFX'][0,:,:]
vmin=np.percentile(data,5)
vmax=np.percentile(data,99)
im=ax.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
ax.axis(False)
ax.set_title('3 km Heat Flux')

ax=fig.add_subplot(gs[1,0])
data=fphmg['HFX'][0,:,:]
ax.imshow(data,cmap='turbo',origin='lower',vmin=vmin,vmax=vmax)
ax.axis(False)
ax.set_title('60 km Heat Flux')

ax=fig.add_subplot(gs[:,1:])
data=fphet['RAINNC'][0,:,:]-fphmg['RAINNC'][0,:,:]
vmin=-np.percentile(np.abs(data),99.5)
data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
im=ax.imshow(data,cmap='coolwarm',origin='lower',vmin=vmin,vmax=-vmin)
ax.axis(False)
ax.set_title(r'$P_{3 km} - P_{60 km}$')
fig.colorbar(im,ax=ax,label=r'$\Delta$ Precipitation (mm)',shrink=.73)
plt.subplots_adjust(hspace=.05)


# %%
data=np.nanmean(fpt['1mmTime0_48'][:,:,:]-fpg['1mmTime0_48'][:,:,:],axis=0)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-5,vmax=5)
plt.colorbar()

# %%
fphet.close()

# %%
fp.close()

# %%
fphmg.close()

# %%

# %%
