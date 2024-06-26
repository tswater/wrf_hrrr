# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.2
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
from matplotlib.lines import Line2D
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.animation import FuncAnimation
import matplotlib.patheffects as pe
import matplotlib
import scipy as sci
from IPython.display import HTML
#import wrf
from sklearn.metrics import mean_squared_error
from matplotlib.gridspec import GridSpec
import cmasher as cmr
mpl.rcParams['figure.dpi'] = 400
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

# %% [markdown]
# # LOAD FILES and SETUP

# %%

# %%
fpst=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/201707_long/het/OUTPUT/static_data.nc','r')
msk=fpst['LU_INDEX'][0,:,:]==17

# %%
hmg_dir='/home/tsw35/tyche/wrf_hrrr/20170717/1560_1040_060_169/OUTPUT/'
het_dir='/home/tsw35/tyche/wrf_hrrr/20170717/1560_1040_003_169/OUTPUT/'
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-17_20:00:00','r')
fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-17_20:00:00','r')

# %%
a=fphmg['ALBBCK'][:]-fphmg['ALBEDO'][:]

# %%
# COLORMAPS
hmap='turbo'
tmap='gist_heat'
dmap='coolwarm'
rmap='viridis'
dmmap='PiYG'
demap='BrBG'
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

cubehelix = cm.get_cmap('cubehelix', 200)
newcl=cubehelix(range(175))
lmap=ListedColormap(newcl)


# %%
#(52, 78)
#(1039, 1559)
def databig(data):
    dout=np.zeros((1039,1559))
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            dout[i*20:(i+1)*20,j*20:(j+1)*20]=data[i,j]
    return dout


# %%
def databig2(data):
    dout=np.zeros((257,1039,1559))
    for t in range(257):
        for i in range(data.shape[1]):
            for j in range(data.shape[2]):
                dout[t,i*20:(i+1)*20,j*20:(j+1)*20]=data[t,i,j]
    return dout


# %%
### CLUSTER PATH ###
#fp2d=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/agg_2d.nc','r')
#fpagg=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/agg_full.nc','r')
#fpscl=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/agg_scaling.nc','r')

### FRAMEWORK PATH ###
frkdir='/home/tswater/Documents/Elements_Temp/WRF/'
fpscl=nc.Dataset(frkdir+'agg_files/agg_scaling.nc','r')



# %%
def meani(data,df=20):
    nx=int(data.shape[0]/df+1)
    ny=int(data.shape[1]/df+1)
    dout=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            dout[i,j] = np.nanmean(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout


# %% [markdown]
# # FIGURE 2: Homogenization Illustration

# %%
### INPUTS ###
cbarlabel1=r'H ($W/m^{-2}$)'
cbarlabel2=r'LH ($W/m^{-2}$)'
cbarlabel3=r'$T_{skin}$ ($K$)'
lbsize=14

### CLUSTER PATH ###
#fpt=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/scaling/het/OUTPUT/wrfout_d01_2023-07-07_19:00:00','r')
#fpg=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/scaling/hmg060/OUTPUT/wrfout_d01_2023-07-07_19:00:00','r')

### FRAMEWORK PATH ###
frkdir='/home/tswater/Documents/Elements_Temp/WRF/'
fpt=nc.Dataset(frkdir+'scaling_compressed/het/wrfout_d01_2023-07-07_190000','r')
fpg=nc.Dataset(frkdir+'scaling_compressed/hmg060/wrfout_d01_2023-07-07_190000','r')


fig = plt.figure(figsize=(6,6),layout='tight')
subfigs = fig.subfigures(1, 3, hspace=0,wspace=0, width_ratios=[1,1, 1],frameon=False)

ht=fpscl['HFX'][0,10,:,:]
hg=databig(meani(ht))#fpscl['HFX'][-2,10,:,:]
lt=fpscl['LH'][0,10,:,:]
lg=databig(meani(lt))#fpscl['LH'][-2,10,:,:]
tt=fpscl['TSK'][0,10,:,:]
tg=databig(meani(tt))#fpg['TSK'][0,:,:]

vxh=np.nanpercentile(ht,99)
vxl=np.nanpercentile(lt,99)
vxt=np.nanpercentile(tt,99)

vnh=np.nanpercentile(ht,1)
vnl=np.nanpercentile(lt,1)
vnt=np.nanpercentile(tt,1)

grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="10%")

im=grid[0].imshow(ht,origin='lower',cmap=hmap,vmin=vnh,vmax=vxh)
im=grid[1].imshow(hg,origin='lower',cmap=hmap,vmin=vnh,vmax=vxh)

grid[0].grid(False)
grid[0].set_xticks([],[])
grid[0].set_yticks([],[])
grid[1].grid(False)
grid[1].set_xticks([],[])
grid[1].set_yticks([],[])

grid[0].set_ylabel('LSM Output')
grid[1].set_ylabel('60km HMG')

cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)



grid=ImageGrid(subfigs[1], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="10%")

im=grid[0].imshow(lt,origin='lower',cmap=lmap,vmin=vnl,vmax=vxl)
im=grid[1].imshow(lg,origin='lower',cmap=lmap,vmin=vnl,vmax=vxl)

grid[0].axis(False)
grid[1].axis(False)

cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel2)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)



grid=ImageGrid(subfigs[2], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="10%")

im=grid[0].imshow(tt,origin='lower',cmap=tmap,vmin=vnt,vmax=vxt)
im=grid[1].imshow(tg,origin='lower',cmap=tmap,vmin=vnt,vmax=vxt)

grid[0].axis(False)
grid[1].axis(False)

cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel3)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel3,size=lbsize)
plt.savefig('fig2.png', bbox_inches = "tight")

# %% [markdown]
# # Figure 2 Alt (HFX only)

# %%
fig = plt.figure(figsize=(6,6),layout='tight')

cbarlabel1=r'H ($W/m^{-2}$)'
cbarlabel2=r'LH ($W/m^{-2}$)'
cbarlabel3=r'$T_{skin}$ ($K$)'
lbsize=14

ht=fpscl['HFX'][0,10,:,:]
hg=databig(meani(ht))#fpscl['HFX'][-2,10,:,:]

vxh=np.nanpercentile(ht,99)

vnh=np.nanpercentile(ht,1)

grid=ImageGrid(fig, 111,  # similar to subplot(111)
                nrows_ncols=(1, 2),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="5%")

im=grid[0].imshow(ht,origin='lower',cmap=hmap,vmin=vnh,vmax=vxh)
im=grid[1].imshow(hg,origin='lower',cmap=hmap,vmin=vnh,vmax=vxh)

grid[0].grid(False)
grid[0].set_xticks([],[])
grid[0].set_yticks([],[])
grid[1].grid(False)
grid[1].set_xticks([],[])
grid[1].set_yticks([],[])

grid[0].set_xlabel('LSM Output')
grid[1].set_xlabel('60km HMG')

cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)

plt.savefig('fig2_alt.png', bbox_inches = "tight")

# %%

# %%

# %% [markdown]
# # FIGURE 3: Homogenization and Precip

# %%
# FILES
fpt=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/20170717/1560_1040_003_169/OUTPUT/wrfout_d01_2017-07-17_18:00:00','r')
fpg=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/20170717/1560_1040_060_169/OUTPUT/wrfout_d01_2017-07-17_18:00:00','r')


# %%
### INPUTS ###
cbarlabel1=r'EF'
cbarlabel2=r'$P_{60\ km}$ - $P_{3\ km}$ ($mm$)'
lbsize=18

### DATA SMOL ###
data1=np.mean(fpscl['LH'][0,:,:,:],axis=0)/(np.mean(fpscl['LH'][0,:,:,:],axis=0)+np.mean(fpscl['HFX'][0,:,:,:],axis=0))
data2=np.mean(fpscl['LH'][-2,:,:,:],axis=0)/(np.mean(fpscl['LH'][-2,:,:,:],axis=0)+np.mean(fpscl['HFX'][-2,:,:,:],axis=0))

data1[msk]=float('nan')
data2[msk]=float('nan')

vmax=1
vmin=0


### DATA LARGE ###
raint=fpscl['RAINNC'][0,-1,:,:]
raing=fpscl['RAINNC'][-2,-1,:,:]
data3=raing-raint
data3[msk]=float('nan')
vmax3=max(np.abs(np.nanpercentile(data3,.5)),np.abs(np.nanpercentile(data3,99.5)))
vmin3=-vmax3


### SETUP ###
fig = plt.figure(figsize=(9,4.5),layout='tight')
subfigs = fig.subfigures(1, 2, hspace=0,wspace=0, width_ratios=[.45, 1],frameon=False)
#subfigs[0].add_subplot(1,1,1)
#subfigs[1].add_subplot(1,1,1)
#### LEFT SIDE FIGURES ####
grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="10%")

im=grid[0].imshow(data1,origin='lower',cmap='YlGnBu',vmin=vmin,vmax=vmax)
im=grid[1].imshow(data2,origin='lower',cmap='YlGnBu',vmin=vmin,vmax=vmax)
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)
grid[0].text(-50,940,'a)',fontsize=lbsize)
grid[1].text(-50,940,'b)',fontsize=lbsize)


#### RIGHT SIDE FIGURE ####
grid=ImageGrid(subfigs[1], 111,  # similar to subplot(111)
                nrows_ncols=(1, 1),
                axes_pad=0,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="3%")

im=grid[0].imshow(data3,origin='lower',cmap=dmap,vmin=vmin3,vmax=vmax3)
grid[0].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel2)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)
grid[0].text(0,980,'c)',fontsize=lbsize)
plt.savefig('fig3.png', bbox_inches = "tight")

# %% [markdown]
# # FIGURE 4: Homogenization Variance

# %%
fpagg=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/agg_full.nc','r')

# %%
fig=plt.figure(figsize=(7,4))
subfigs = fig.subfigures(2, 1, hspace=0,wspace=0,frameon=False)

### INPUTS ###
cbarlabel1=r'$\sigma_H$ ($W/m^{-2}$)'
cbarlabel2=r'$\sigma_{LH}$ ($W/m^{-2}$)'
lbsize=14

### DATA #
data1=fp2d['VARHFX_het'][:]
data2=fp2d['VARLH_het'][:]

data1=databig(data1)
data2=databig(data2)

data1[msk]=float('nan')
data2[msk]=float('nan')

vmin1=0
vmin2=0
vmax1=max(np.nanpercentile(data1,97),np.nanpercentile(data2,97))
vmax2=vmax1

grid=ImageGrid(fig, 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.1,
                cbar_mode='each',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="5%")

im=grid[0].imshow(data1,origin='lower',cmap=hmap,vmin=vmin1,vmax=vmax1,interpolation='none')
im2=grid[1].imshow(data2,origin='lower',cmap=lmap,vmin=vmin2,vmax=vmax2,interpolation='none')
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)

cb=grid.cbar_axes[1].colorbar(im2,label=cbarlabel2)
grid.cbar_axes[1].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)

grid[0].text(-50,940,'a)',fontsize=lbsize)
grid[1].text(-50,940,'b)',fontsize=lbsize)
plt.savefig('fig4.png', bbox_inches = "tight")

# %%
data=(np.sqrt(fp2d['VARHFX_het'][:])+np.sqrt(fp2d['VARLH_het'][:]))/(fp2d['HFX_60'][:]+fp2d['LH_60'][:])
data=databig(data)
data[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo',norm=LogNorm(vmin=0.3, vmax=2.99))
plt.colorbar()

# %%

# %%

# %%

# %%
from matplotlib.colors import LogNorm

# %%
fig=plt.figure(figsize=(7,4))
subfigs = fig.subfigures(1, 2, hspace=0,wspace=0,frameon=False)

### INPUTS ###
cbarlabel1=r'$\sigma_H$ ($W/m^{-2}$)'
cbarlabel2=r'$\sigma_{LH}$ ($W/m^{-2}$)'
lbsize=14

### DATA #
data1=np.sqrt(fp2d['VARHFX_het'][:])
data2=np.sqrt(fp2d['VARLH_het'][:])

data1=databig(data1)
data2=databig(data2)

data1[msk]=float('nan')
data2[msk]=float('nan')

vmin1=5
vmin2=5
vmax1=max(np.nanpercentile(data1,99),np.nanpercentile(data2,99))
vmax2=vmax1

grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.1,
                cbar_mode='each',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="5%")

im=grid[0].imshow(data1,origin='lower',cmap=hmap,vmin=vmin1,vmax=vmax1,interpolation='none')
im2=grid[1].imshow(data2,origin='lower',cmap=lmap,vmin=vmin2,vmax=vmax2,interpolation='none')
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)

cb=grid.cbar_axes[1].colorbar(im2,label=cbarlabel2)
grid.cbar_axes[1].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)

grid[0].text(-50,940,'a)',fontsize=lbsize)
grid[1].text(-50,940,'b)',fontsize=lbsize)


data1=np.sqrt(fp2d['VARHFX_het'][:])/fp2d['HFX_60'][:]
data2=np.sqrt(fp2d['VARLH_het'][:])/fp2d['LH_60'][:]

data1=databig(data1)
data2=databig(data2)

data1[msk]=float('nan')
data2[msk]=float('nan')

cbarlabel1=r'$COV_H$ ($W/m^{-2}$)'
cbarlabel2=r'$COV_{LH}$ ($W/m^{-2}$)'

vmin1=0
vmin2=0
vmax1=1.99
vmax2=1.99

grid=ImageGrid(subfigs[1], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.1,
                cbar_mode='each',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="5%")
im=grid[0].imshow(data1,origin='lower',cmap=hmap,vmin=vmin1,vmax=vmax1,interpolation='none')
im2=grid[1].imshow(data2,origin='lower',cmap=lmap,vmin=vmin2,vmax=vmax2,interpolation='none')

#im=grid[0].imshow(data1,origin='lower',cmap=hmap,interpolation='none',norm=LogNorm(vmin=0.01, vmax=1.99))
#im2=grid[1].imshow(data2,origin='lower',cmap=lmap,interpolation='none',norm=LogNorm(vmin=0.01, vmax=1.99))
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)

cb=grid.cbar_axes[1].colorbar(im2,label=cbarlabel2)
grid.cbar_axes[1].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)

grid[0].text(-50,940,'c)',fontsize=lbsize)
grid[1].text(-50,940,'d)',fontsize=lbsize)
plt.savefig('fig4_alt.png', bbox_inches = "tight")

# %%

# %% [markdown]
# # FIGURE 4 ALT: Homogenization Variance

# %%

# %%

# %%

# %% [markdown]
# # FIGURE 5 Scaling of Homogenization

# %%

# %%
dVar=[]
dErr=[]
for i in range(7):
    dVar.append(np.var(fpscl['HFX'][i,36,:,:][~msk]))
    rmse=mean_squared_error(fpscl['RAINNC'][0,36,:,:][~msk],fpscl['RAINNC'][i,36,:,:][~msk],squared=False)
    dErr.append(rmse)
scales=np.array([3,6,12,15,30,60,120])
dVar=np.array(dVar)
dErr=np.array(dErr)
dStd=np.sqrt(dVar)

# %%
fig=plt.figure(figsize=(6.5,3),layout='tight')
subfigs = fig.subfigures(2, 1, hspace=0,wspace=0, height_ratios=[.5, 1],frameon=False)
zoom=np.zeros((1039, 1559),dtype=bool)
zoom[400:800,1000:1400]=True
lbsize=12
cbarlabel1='H ($W\ m^{-2}$)'

grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(1, 6),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.05,
                cbar_size="15%")
for i in range(6):
    data=fpscl['HFX'][i+1,36,:,:][zoom]
    data=data.reshape(400,400)
    if i==0:
        vmin=np.percentile(data,1)
        vmax=np.percentile(data,99)
    im=grid[i].imshow(data,origin='lower',cmap=hmap,vmin=vmin,vmax=vmax,interpolation='none')
    grid[i].axis(False)
    grid[i].set_title(str(scales[i+1])+r' $km$')
    if i==0:
        cb=grid.cbar_axes[i].colorbar(im,label=cbarlabel1)
        grid.cbar_axes[i].tick_params(labelsize=lbsize)
        cb.set_label(label=cbarlabel1,size=lbsize)
        grid[i].text(-150,325,'a)',fontsize=lbsize)
ax=subfigs[1].add_subplot(111)
ax.semilogx(scales[1:],dStd[1:],'-o',c='firebrick',zorder=5)
ax.set_ylabel(r'$\sigma_{H}$',color='firebrick')
ax.set_xlabel('Homogenization Scale ($km$, log scale)')
ax.text(4.2,170,'b)',fontsize=lbsize)
ax.set_ylim(140,170)
ax.set_yticks([145,150,155,160,165],[145,150,155,160,165],color='firebrick')
ax2=ax.twinx()
ax2.semilogx(scales[1:],dErr[1:],'-o',c='mediumblue',zorder=4)
ax2.set_ylabel(r'RMSE P ($mm$)',color='mediumblue')
ax2.set_xlim(5,130)
ax.set_xticks([6,12,15,30,60,120],[6,12,15,30,60,120])
ax2.set_ylim(5.5,8.5)
ax2.set_yticks([6,6.5,7,7.5,8],[6,6.5,7,7.5,8],color='mediumblue')
ax2.grid(False)
#ax.xaxis.tick_top()

# %%
fig=plt.figure(figsize=(6.5,3),layout='tight')
subfigs = fig.subfigures(2, 1, hspace=0,wspace=0, height_ratios=[.5, 1],frameon=False)
zoom=np.zeros((1039, 1559),dtype=bool)
zoom[400:800,1000:1400]=True
lbsize=12
cbarlabel1='H ($W\ m^{-2}$)'

grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(1, 6),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.05,
                cbar_size="15%")
for i in range(6):
    data=fpscl['HFX'][i+1,36,:,:][zoom]
    data=data.reshape(400,400)
    if i==0:
        vmin=np.percentile(data,1)
        vmax=np.percentile(data,99)
    im=grid[i].imshow(data,origin='lower',cmap=hmap,vmin=vmin,vmax=vmax,interpolation='none')
    grid[i].axis(False)
    grid[i].set_title(str(scales[i+1])+r' $km$')
    if i==0:
        cb=grid.cbar_axes[i].colorbar(im,label=cbarlabel1)
        grid.cbar_axes[i].tick_params(labelsize=lbsize)
        cb.set_label(label=cbarlabel1,size=lbsize)
        grid[i].text(-150,325,'a)',fontsize=lbsize)
        
ax=subfigs[1].add_subplot(111)
ax.plot(scales[1:],dStd[1:],'-o',c='firebrick',zorder=5)
ax.set_ylabel(r'$\sigma_{H}$ ($W\ m^{-2}$)',color='firebrick')
ax.set_xlabel('Homogenization Scale ($km$)')
ax.set_ylim(140,170)
ax.text(-7.5,170,'b)',fontsize=lbsize)
ax.set_yticks([145,150,155,160,165],[145,150,155,160,165],color='firebrick')
#ax.grid(color='dimgrey',axis='x')
ax2=ax.twinx()
ax2.plot(scales[1:],dErr[1:],'-o',c='mediumblue',zorder=4)
ax2.set_ylabel(r'RMSE P ($mm$)',color='mediumblue')
ax2.set_xlim(0,130)
ax.set_xticks([6,12,15,30,60,120],[6,'',15,30,60,120])
ax2.set_ylim(5.5,8.5)
ax2.set_yticks([6,6.5,7,7.5,8],[6,6.5,7,7.5,8],color='mediumblue')
ax2.grid(False)
#ax.xaxis.tick_top()
plt.savefig('fig5.png', bbox_inches = "tight")

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %% [markdown]
# # FIGURE 7 Spatial Statistics of Precipitation

# %%
fp2d=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/agg_2d.nc','r')

# %%
### INPUTS ###
cbarlabel1=r'P ($mm$)'
cbarlabel2=r'$P_{60\ km}$ - $P_{3\ km}$ ($mm$)'
lbsize=18

### DATA SMOL ###
data1=fp2d['RAINNC_het'][:,:]/3
data2=fp2d['RAINNC_hmg'][:,:]/3

data1[msk]=float('nan')
data2[msk]=float('nan')

vmax=max(np.nanpercentile(data1,95),np.nanpercentile(data2,95))
vmin=min(np.nanpercentile(data1,1),np.nanpercentile(data2,1))


### DATA LARGE ###
raint=fp2d['RAINNC_het'][:,:]/3
raing=fp2d['RAINNC_hmg'][:,:]/3
data3=raing-raint
data3[msk]=float('nan')
vmax3=max(np.abs(np.nanpercentile(data3,2)),np.abs(np.nanpercentile(data3,98)))
vmin3=-vmax3


### SETUP ###
fig = plt.figure(figsize=(9,4.5),layout='tight')
subfigs = fig.subfigures(1, 2, hspace=0,wspace=0, width_ratios=[.45, 1],frameon=False)
#subfigs[0].add_subplot(1,1,1)
#subfigs[1].add_subplot(1,1,1)
#### LEFT SIDE FIGURES ####
grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="10%")

im=grid[0].imshow(data1,origin='lower',cmap=rmap,vmin=vmin,vmax=vmax)
im=grid[1].imshow(data2,origin='lower',cmap=rmap,vmin=vmin,vmax=vmax)
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)
grid[0].text(-50,940,'a)',fontsize=lbsize)
grid[1].text(-50,940,'b)',fontsize=lbsize)


#### RIGHT SIDE FIGURE ####
grid=ImageGrid(subfigs[1], 111,  # similar to subplot(111)
                nrows_ncols=(1, 1),
                axes_pad=0,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="3%")

im=grid[0].imshow(data3,origin='lower',cmap=dmap,vmin=vmin3,vmax=vmax3)
grid[0].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel2)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)
grid[0].text(0,980,'c)',fontsize=lbsize)
#plt.savefig('fig6.png', bbox_inches = "tight")

# %%
blist=['LND','CTL','FLR','GRL','GSL','MEX','TEX','CAL']
names=['$\Delta$EF','$\Delta$PW',r'$\Delta$$T_{2m}$',r'$\Delta$$RH_{2m}$','$\Delta$LCL','$\Delta$LFC',r'$\Delta$$MsKE_{low}$',r'$\Delta$$MsKE$',r'$\Delta$$CC_{high}$',r'$\Delta$$CC_{mid}$',r'$\Delta$$CC_{low}$']
boxes={}
for b in blist:
    boxes[b]=[]
boxes['CAL'].append([500,800,30,150])
boxes['MEX'].append([50,400,200,400])
boxes['FLR'].append([75,275,1200,1375])
boxes['GRL'].append([700,1000,900,1375])
boxes['GSL'].append([600,750,300,450])
boxes['CTL'].append([400,800,600,1000])
boxes['TEX'].append([180,350,700,1000])
boxes['LND'].append([0,1039,0,1559])
#boxes['ALL'].append([0,1039,0,1559])


masks={}
for k in boxes.keys():
    masks[k]=np.zeros((1039, 1559),dtype='bool')
    boxs=boxes[k]
    for bx in boxs:
        masks[k][bx[0]:bx[1],bx[2]:bx[3]]=True
    if k!='ALL':
        masks[k][msk]=False


# %%

# %% [markdown]
# # FIGURE 7.5 Spatial Precipitation Percentage

# %%
### INPUTS ###
cbarlabel1=r'P ($mm$)'
cbarlabel2=r'$P_{60\ km}$ - $P_{3\ km}$ ($mm$)'
lbsize=14

### DATA SMOL ###
data1=fp2d['RAINNC_het'][:,:]/3
data2=fp2d['RAINNC_hmg'][:,:]/3

data1[msk]=float('nan')
data2[msk]=float('nan')

vmax=max(np.nanpercentile(data1,95),np.nanpercentile(data2,95))
vmin=min(np.nanpercentile(data1,1),np.nanpercentile(data2,1))


### DATA LARGE ###
raint=fp2d['RAINNC_het'][:,:]/3
raing=fp2d['RAINNC_hmg'][:,:]/3
data3=raing-raint
data3[msk]=float('nan')
vmax3=max(np.abs(np.nanpercentile(data3,2)),np.abs(np.nanpercentile(data3,98)))
vmin3=-vmax3





fig = plt.figure(figsize=(8,5.5),layout='tight')
subfigs = fig.subfigures(2, 1, hspace=0,wspace=0,frameon=False)
#subfigs[0].add_subplot(1,1,1)
#subfigs[1].add_subplot(1,1,1)
#### LEFT SIDE FIGURES ####
grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(1, 2),
                axes_pad=0.1,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="5%")


im=grid[0].imshow(data1,origin='lower',cmap=rmap,vmin=vmin,vmax=vmax)
im=grid[1].imshow(data2,origin='lower',cmap=rmap,vmin=vmin,vmax=vmax)
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)
cb=grid.cbar_axes[1].colorbar(im,label=cbarlabel1)
grid.cbar_axes[1].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)
grid[0].text(0,940,'a)',fontsize=lbsize)
grid[1].text(0,940,'b)',fontsize=lbsize)


grid=ImageGrid(subfigs[1], 111,  # similar to subplot(111)
                nrows_ncols=(1, 2),
                axes_pad=0.1,
                cbar_mode='each',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="5%")

im=grid[0].imshow(data3,origin='lower',cmap=dmap,vmin=vmin3,vmax=vmax3)
grid[0].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel2)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)
grid[0].text(0,980,'c)',fontsize=lbsize)


raint=fp2d['RAINNC_het'][:,:]/3
raint=sci.ndimage.filters.gaussian_filter(raint,sigma=15,mode='reflect')
raing=fp2d['RAINNC_hmg'][:,:]/3
raing=sci.ndimage.filters.gaussian_filter(raing,sigma=15,mode='reflect')
data=(raing-raint)/raint*100
#sci.ndimage.filters.gaussian_filter(raint,sigma=10,mode='reflect')*100

data[msk]=float('nan')
vmax=75
vmin=-75

cbarlabel=r'$P_{60\ km}$ - $P_{3\ km}$ (%)'
im=grid[1].imshow(data,origin='lower',cmap=dmap,vmin=vmin,vmax=vmax)
grid[1].axis(False)
cb=grid.cbar_axes[1].colorbar(im,label=cbarlabel)
grid.cbar_axes[1].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel,size=lbsize)
grid[1].text(0,980,'d)',fontsize=lbsize)

plt.savefig('fig6.png', bbox_inches = "tight")

# %%
print(np.nanmedian(data))

# %%
print(np.nanmedian(data3))

# %%

# %%
mask=masks['MEX']
raint_=np.zeros((257,))
raing_=np.zeros((257,))
for i in range(257):
    print('.',end='',flush=True)
    raint_[i]=np.nanmean(fpagg['RAINNC_het'][i,:][mask])
    raing_[i]=np.nanmean(fpagg['RAINNC_hmg'][i,:][mask])

# %%
craint=np.zeros((257,))
craing=np.zeros((257,))

craint[0:86]=np.cumsum(raint_[0:86])
craing[0:86]=np.cumsum(raing_[0:86])

craint[86:172]=np.cumsum(raint_[86:172])
craing[86:172]=np.cumsum(raing_[86:172])

craint[172:]=np.cumsum(raint_[172:])
craing[172:]=np.cumsum(raing_[172:])

plt.plot(craing/craint)

# %%

# %% [markdown]
# # FIGURE 8 Spatial Precipitation Percentage

# %%
raint=fp2d['RAINNC_het'][:,:]/3
raint=sci.ndimage.filters.gaussian_filter(raint,sigma=15,mode='reflect')
raing=fp2d['RAINNC_hmg'][:,:]/3
raing=sci.ndimage.filters.gaussian_filter(raing,sigma=15,mode='reflect')
data=(raing-raint)/raint*100
#sci.ndimage.filters.gaussian_filter(raint,sigma=10,mode='reflect')*100

data[msk]=float('nan')
vmax=75
vmin=-75

plt.figure()
plt.imshow(data,origin='lower',cmap=dmap,vmin=vmin,vmax=vmax)
#plt.grid(False)
plt.axis(False)
plt.text(-20,940,'d)',fontsize=lbsize)
#plt.xticks([])
#plt.yticks([])
cbarlabel=r'$P_{3\ km}$ - $P_{60\ km}$ (%)'
plt.colorbar(shrink=.72,label=cbarlabel)

# %%

# %%

# %%

# %% [markdown]
# # FIGURE 9 MSWEP COMPARISON

# %%
fpmsw=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/mswep_error.nc','r')

# %%
### INPUTS ###
cbarlabel1=r'Bias P ($mm$)'
cbarlabel2=r'$P_{3\ km}$ - $P_{60\ km}$ ($mm$)'
lbsize=18

### DATA SMOL ###
data1=np.abs(fpmsw['BIAS2D_het'][:])/fpmsw['MSWEP_MEAN2D'][:]
data2=np.abs(fpmsw['BIAS2D_hmg'][:])/fpmsw['MSWEP_MEAN2D'][:]

data1[msk]=float('nan')
data2[msk]=float('nan')

vmax=max(np.nanpercentile(data1,95),np.nanpercentile(data2,95))
vmin=0#min(np.nanpercentile(data1,1),np.nanpercentile(data2,1))


### DATA LARGE ###



### SETUP ###
fig = plt.figure(figsize=(9,6),layout='tight')
subfigs = fig.subfigures(3, 1, hspace=0,wspace=0, height_ratios=[1, .7,.7],frameon=False)
#subfigs[0].add_subplot(1,1,1)
#subfigs[1].add_subplot(1,1,1)
#### LEFT SIDE FIGURES ####
grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(1, 2),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="4%")

im=grid[0].imshow(data1,origin='lower',cmap='jet',vmin=vmin,vmax=vmax)
im=grid[1].imshow(data2,origin='lower',cmap='jet',vmin=vmin,vmax=vmax)
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=14)
grid[0].text(-20,940,'a)',fontsize=lbsize)
grid[1].text(-20,940,'b)',fontsize=lbsize)

#fpmsw=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/mswep_error_land.nc','r')

#### TIME ONE ####
ax=subfigs[1].add_subplot(1,1,1)
#ax=plt.subplot(1,1,1)
dt=np.abs(fpmsw['BIAS_d_het'][:])
dg=np.abs(fpmsw['BIAS_d_hmg'][:])
N=len(dt)

dgclr=np.zeros((N,),dtype='object')
dgclr[dg>dt]='blue'
dgclr[dg<=dt]='red'
dgclr[np.isnan(dg)]='blue'

time=np.linspace(1,270,270)
ax.set_xticks([0,90,180],['Jun21','Jun22','Jun23'],rotation=45)
ax.set_xticks([30,60,120,150,210,240],['Jul21','Aug21','Jul22','Aug22','Jul23','Aug23'],rotation=45,minor=True)

ax.grid(which='minor',linewidth=1)
ax.grid(axis='x',which='major',linewidth=3)


a=[dg,dt]
ax.plot([time,time],a,'--',c='k',linewidth=.5)
ax.scatter(time,dt,s=5,facecolors='none', edgecolors='k',alpha=.75)
ax.scatter(time,dg,s=10,c=dgclr,alpha=.5)

handles=[]
point1 = Line2D([0], [0], label='HET', marker='o',markersize=5, 
         markeredgecolor='k', markerfacecolor='none', linestyle='')
point2 = Line2D([0], [0], label='HMG (< HET)', marker='o',markersize=5, 
         markeredgecolor='red', markerfacecolor='red', linestyle='')
point3 = Line2D([0], [0], label='HMG (> HET)', marker='o',markersize=5, 
         markeredgecolor='blue', markerfacecolor='blue', linestyle='')
handles.append(point1)
handles.append(point2)
handles.append(point3)

plt.legend(handles=handles,loc='upper right')
plt.ylabel('Absolute\nBias $(mm)$',fontsize=14)
plt.ylim(-.1,2.5)
ax.text(-10,2.1,'c)',fontsize=lbsize)


#### TIME 2 ####
ax=subfigs[2].add_subplot(1,1,1)
dt=fpmsw['RMSE_d_het'][:]
dg=fpmsw['RMSE_d_hmg'][:]
N=len(dt)

dgclr=np.zeros((N,),dtype='object')
dgclr[dg>dt]='blue'
dgclr[dg<=dt]='red'
dgclr[np.isnan(dg)]='blue'

time=np.linspace(1,270,270)
ax.set_xticks([0,90,180],['Jun21','Jun22','Jun23'],rotation=45)
ax.set_xticks([30,60,120,150,210,240],['Jul21','Aug21','Jul22','Aug22','Jul23','Aug23'],rotation=45,minor=True)

ax.grid(which='minor',linewidth=1)
ax.grid(axis='x',which='major',linewidth=3)


a=[dg,dt]
ax.plot([time,time],a,'--',c='k',linewidth=.5)
ax.scatter(time,dt,s=5,facecolors='none', edgecolors='k',alpha=.75)
ax.scatter(time,dg,s=10,c=dgclr,alpha=.5)

handles=[]
point1 = Line2D([0], [0], label='HET', marker='o',markersize=5, 
         markeredgecolor='k', markerfacecolor='none', linestyle='')
point2 = Line2D([0], [0], label='HMG (< HET)', marker='o',markersize=5, 
         markeredgecolor='red', markerfacecolor='red', linestyle='')
point3 = Line2D([0], [0], label='HMG (> HET)', marker='o',markersize=5, 
         markeredgecolor='blue', markerfacecolor='blue', linestyle='')
handles.append(point1)
handles.append(point2)
handles.append(point3)

plt.legend(handles=handles,loc='upper right')
plt.ylim(5,20)
ax.text(-10,17.5,'d)',fontsize=lbsize)
plt.ylabel(r'RMSE $(mm)$',fontsize=14)

plt.xlabel(r'Time of Year')
plt.savefig('fig7.png', bbox_inches = "tight")

# %%

# %%

# %% [markdown]
# # Figure 10 EVAPORATIVE FRACTION

# %%
#EFhmg=np.mean(fp['LH_hmg'][:,:,:],axis=0)/(np.mean(fp['LH_hmg'][:,:,:],axis=0)+np.mean(fp['HFX_hmg'][:,:,:],axis=0))
#EFhet=np.mean(fp['LH_60'][:,:,:],axis=0)/(np.mean(fp['LH_60'][:,:,:],axis=0)+np.mean(fp['HFX_60'][:,:,:],axis=0))

### INPUTS ###
cbarlabel1=r'EF'
cbarlabel2=r'$EF_{60\ km}$ - $EF_{3\ km}$'
lbsize=18

### DATA SMOL ###
data1=fp2d['LH_60'][:]/(fp2d['LH_60'][:]+fp2d['HFX_60'][:])
data1=databig(data1)
data2=fp2d['LH_hmg'][:]/(fp2d['LH_hmg'][:]+fp2d['HFX_hmg'][:])

data1[msk]=float('nan')
data2[msk]=float('nan')

vmax=1
vmin=0


### DATA LARGE ###
data3=data2-data1
vmax3=.1
vmin3=-vmax3


### SETUP ###
fig = plt.figure(figsize=(9,4.5),layout='tight')
subfigs = fig.subfigures(1, 2, hspace=0,wspace=0, width_ratios=[.45, 1],frameon=False)
#subfigs[0].add_subplot(1,1,1)
#subfigs[1].add_subplot(1,1,1)
#### LEFT SIDE FIGURES ####
grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="10%")

im=grid[0].imshow(data1,origin='lower',cmap=hmap,vmin=vmin,vmax=vmax)
im=grid[1].imshow(data2,origin='lower',cmap=hmap,vmin=vmin,vmax=vmax)
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)
grid[0].text(-50,940,'a)',fontsize=lbsize)
grid[1].text(-50,940,'b)',fontsize=lbsize)


#### RIGHT SIDE FIGURE ####
grid=ImageGrid(subfigs[1], 111,  # similar to subplot(111)
                nrows_ncols=(1, 1),
                axes_pad=0,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="3%")

im=grid[0].imshow(data3,origin='lower',cmap=demap,vmin=vmin3,vmax=vmax3)
grid[0].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel2)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)
grid[0].text(0,980,'c)',fontsize=lbsize)


# %%

# %%

# %% [markdown]
# # FIGURE 11 MsKE: Cumulative

# %%
#EFhmg=np.mean(fp['LH_hmg'][:,:,:],axis=0)/(np.mean(fp['LH_hmg'][:,:,:],axis=0)+np.mean(fp['HFX_hmg'][:,:,:],axis=0))
#EFhet=np.mean(fp['LH_60'][:,:,:],axis=0)/(np.mean(fp['LH_60'][:,:,:],axis=0)+np.mean(fp['HFX_60'][:,:,:],axis=0))

### INPUTS ###
cbarlabel1=r'MsKE'
cbarlabel2=r'$MsKE_{60\ km}$ - $MsKE_{3\ km}$'
lbsize=18

### DATA SMOL ###
data1=fp2d['MED_MsKE_het'][:]
data1=databig(data1)
data2=fp2d['MED_MsKE_hmg'][:]
data2=databig(data2)

data1[msk]=float('nan')
data2[msk]=float('nan')

vmax=max(np.nanpercentile(data1,95),np.nanpercentile(data2,95))
vmin=min(np.nanpercentile(data1,1),np.nanpercentile(data2,1))


### DATA LARGE ###
data3=data2-data1
vmax3=max(np.abs(np.nanpercentile(data3,2)),np.abs(np.nanpercentile(data3,98)))
vmin3=-vmax3

### SETUP ###
fig = plt.figure(figsize=(9,4.5),layout='tight')
subfigs = fig.subfigures(1, 2, hspace=0,wspace=0, width_ratios=[.45, 1],frameon=False)
#subfigs[0].add_subplot(1,1,1)
#subfigs[1].add_subplot(1,1,1)
#### LEFT SIDE FIGURES ####
grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="10%")

im=grid[0].imshow(data1,origin='lower',cmap=hmap,vmin=vmin,vmax=vmax)
im=grid[1].imshow(data2,origin='lower',cmap=hmap,vmin=vmin,vmax=vmax)
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)
grid[0].text(-50,940,'a)',fontsize=lbsize)
grid[1].text(-50,940,'b)',fontsize=lbsize)


#### RIGHT SIDE FIGURE ####
grid=ImageGrid(subfigs[1], 111,  # similar to subplot(111)
                nrows_ncols=(1, 1),
                axes_pad=0,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="3%")

im=grid[0].imshow(data3,origin='lower',cmap=dmmap,vmin=vmin3,vmax=vmax3)
grid[0].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel2)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)
grid[0].text(0,980,'c)',fontsize=lbsize)

# %%

# %%

# %%

# %%

# %% [markdown]
# # FIGURE 11 MsKE: Low Level

# %%
#EFhmg=np.mean(fp['LH_hmg'][:,:,:],axis=0)/(np.mean(fp['LH_hmg'][:,:,:],axis=0)+np.mean(fp['HFX_hmg'][:,:,:],axis=0))
#EFhet=np.mean(fp['LH_60'][:,:,:],axis=0)/(np.mean(fp['LH_60'][:,:,:],axis=0)+np.mean(fp['HFX_60'][:,:,:],axis=0))

### INPUTS ###
cbarlabel1=r'MsKE'
cbarlabel2=r'$Low\ MsKE_{60\ km}$ - $Low\ MsKE_{3\ km}$'
lbsize=18

### DATA SMOL ###
data1=fp2d['MsKElo_het'][:]
data1=databig(data1)
data2=fp2d['MsKElo_hmg'][:]
data2=databig(data2)

#data1[msk]=float('nan')
#data2[msk]=float('nan')

vmax=max(np.nanpercentile(data1,95),np.nanpercentile(data2,95))
vmin=min(np.nanpercentile(data1,1),np.nanpercentile(data2,1))


### DATA LARGE ###
data3=data2-data1
vmax3=max(np.abs(np.nanpercentile(data3,2)),np.abs(np.nanpercentile(data3,98)))
vmin3=-vmax3

### SETUP ###
fig = plt.figure(figsize=(9,4.5),layout='tight')
subfigs = fig.subfigures(1, 2, hspace=0,wspace=0, width_ratios=[.45, 1],frameon=False)
#subfigs[0].add_subplot(1,1,1)
#subfigs[1].add_subplot(1,1,1)
#### LEFT SIDE FIGURES ####
grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="10%")

im=grid[0].imshow(data1,origin='lower',cmap=hmap,vmin=vmin,vmax=vmax)
im=grid[1].imshow(data2,origin='lower',cmap=hmap,vmin=vmin,vmax=vmax)
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)
grid[0].text(-50,940,'a)',fontsize=lbsize)
grid[1].text(-50,940,'b)',fontsize=lbsize)


#### RIGHT SIDE FIGURE ####
grid=ImageGrid(subfigs[1], 111,  # similar to subplot(111)
                nrows_ncols=(1, 1),
                axes_pad=0,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="3%")

im=grid[0].imshow(data3,origin='lower',cmap=dmmap,vmin=vmin3,vmax=vmax3)
grid[0].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel2)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)
grid[0].text(0,980,'c)',fontsize=lbsize)

# %%

# %% [markdown]
# # FIUGRE 12 CLOUDS

# %%
fig=plt.figure(figsize=(3,6))

### INPUTS ###
cbarlabel1='Cloud Cover Change\n 60km - 3km (%)'
lbsize=14

### DATA ###
data1=(fp2d['HICLOUD_hmg'][:]-fp2d['HICLOUD_het'][:])/fp2d['HICLOUD_het'][:]*100
data2=(fp2d['MDCLOUD_hmg'][:]-fp2d['MDCLOUD_het'][:])/fp2d['MDCLOUD_het'][:]*100
data3=(fp2d['LOCLOUD_hmg'][:]-fp2d['LOCLOUD_het'][:])/fp2d['LOCLOUD_het'][:]*100

#vmin1=-.05
#vmin2=-.05
#vmin3=-.05
#vmax1=.05
#vmax2=.05
#vmax3=.05

vmin1=-20
vmin2=-20
vmin3=-20
vmax1=20
vmax2=20
vmax3=20

data1[msk]=float('nan')
data2[msk]=float('nan')
data3[msk]=float('nan')

grid=ImageGrid(fig, 111,  # similar to subplot(111)
                nrows_ncols=(3, 1),
                axes_pad=0.1,
                cbar_mode='single',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="10%")

im=grid[0].imshow(data1,origin='lower',cmap=dmap,vmin=vmin1,vmax=vmax1,interpolation='none')
im2=grid[1].imshow(data2,origin='lower',cmap=dmap,vmin=vmin2,vmax=vmax2,interpolation='none')
im3=grid[2].imshow(data3,origin='lower',cmap=dmap,vmin=vmin3,vmax=vmax3,interpolation='none')
grid[0].axis(False)
grid[1].axis(False)
grid[2].axis(False)

cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)

grid[0].text(-50,940,'a)',fontsize=lbsize)
grid[1].text(-50,940,'b)',fontsize=lbsize)
grid[2].text(-50,940,'c)',fontsize=lbsize)

plt.savefig('fig9.png', bbox_inches = "tight")

# %% [markdown]
# # FIGURE 13 ALL Comparison

# %%
mapvars=['PW','T2','RH2','EF','LFC','MsKE','MsKElo']
cmaps=['Blues',tmap,'BuPu','YlGnBu','copper','autumn','spring']
dcmaps=['rainbow','RdGy','PRGn',demap,'terrain',dmmap,dmmap]
cblb=[r'PW $(kg\ m^{-2})$',r'$T_{2m} (K)$',r'$RH_{2m} (\%)$',
      r'EF',r'LFC ($km$)',r'MsKE ($m^{2} s^{-2}$)',
      r'$MsKE_{lo}$ ($m^{2} s^{-2}$)']
cblb2=[r'$\Delta$PW $(kg\ m^{-2})$',r'$\Delta$$T_{2m} (K)$',r'$\Delta$$RH_{2m} (\%)$',
      r'$\Delta$EF',r'$\Delta$LFC ($km$)',r'$\Delta$MsKE ($m^{2} s^{-2}$)',
      r'$\Delta$$MsKE_{lo}$ ($m^{2} s^{-2}$)']
cblb3=[r'$PW_{60km} - PW_{3km}$ $(kg\ m^{-2})$',
       r'$T_{2m_{60km}}-T_{2m_{3km}}(K)$',
       r'$RH_{2m_{60km}}-RH_{2m_{3km}} (%)$',
       r'$EF_{60km}-EF_{3km}$',
       r'$LCL_{60km}-LCL_{3km}$ ($m$)',
       r'$LFC_{60km}-LFC_{3km}$ ($m$)',
       r'$MsKE_{60km}-MsKE_{3km}$ ($m^{2} s^{-2}$)',
       r'$MsKE_{lo_{60km}}-MsKE_{lo_{3km}}$ ($m^{2} s^{-2}$)']
lbsize=10
letter=['a','b','c','d','e','f','g']

fig=plt.figure(figsize=(6.5,9),layout='tight',dpi=600)
subfigs = fig.subfigures(len(mapvars),3, hspace=0,wspace=0, width_ratios=[2,.3, 1],frameon=False)

for i in range(len(mapvars)):
    var=mapvars[i]
    grid=ImageGrid(subfigs[i,0], 111,  # similar to subplot(111)
                nrows_ncols=(1, 2),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="5%")
   
    #### DATA IMPORT ####
    if var=='EF':
        datat=databig(fp2d['LH_60'][:]/(fp2d['LH_60'][:]+fp2d['HFX_60'][:]))
        datag=fp2d['LH_hmg'][:]/(fp2d['LH_hmg'][:]+fp2d['HFX_hmg'][:])
    elif 'MsKE' in var:
        datat=databig(fp2d[var+'_het'][:])
        datag=databig(fp2d[var+'_hmg'][:])
    else:
        datat=fp2d[var+'_het'][:]
        datag=fp2d[var+'_hmg'][:]
   
    if var=='LFC':
        datat=datat/1000
        datag=datag/1000
   
    datat[msk]=float('nan')
    datag[msk]=float('nan')
   
    vmx=max(np.nanpercentile(datat,99),np.nanpercentile(datag,99))
    vmn=min(np.nanpercentile(datat,1),np.nanpercentile(datag,1))
   
    imt=grid[1].imshow(datat,origin='lower',cmap=cmaps[i],vmin=vmn,vmax=vmx)
    img=grid[0].imshow(datag,origin='lower',cmap=cmaps[i],vmin=vmn,vmax=vmx)
   
    grid[0].axis(False)
    grid[1].axis(False)
   
    grid[0].text(-50,940,letter[i]+')',fontsize=lbsize)
   
    if var=='PW':
        grid[0].set_title('$HMG$')
        grid[1].set_title('$HET$')
   
    cb=grid.cbar_axes[0].colorbar(imt,label=cblb[i])
    grid.cbar_axes[0].tick_params(labelsize=lbsize)
    cb.set_label(label=cblb[i],size=lbsize)
   
    #### DIFFERENCE PLOT ####
    datad=(datag-datat)#/datat
    grid=ImageGrid(subfigs[i,2], 111,  # similar to subplot(111)
                nrows_ncols=(1, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="5%")
   
    vmxd=np.nanpercentile(np.abs(datad),97.5)
    vmnd=-vmxd
   
    im=grid[0].imshow(datad,origin='lower',cmap=dcmaps[i],vmin=vmnd,vmax=vmxd)
   
    if var=='PW':
        grid[0].set_title('$HET-HMG$')
   
    grid[0].axis(False)
    cb=grid.cbar_axes[0].colorbar(im,label=cblb2[i])
    grid.cbar_axes[0].tick_params(labelsize=lbsize)
    cb.set_label(label=cblb2[i],size=lbsize)
    
plt.savefig('fig8.png', bbox_inches = "tight")

# %%

# %%

# %% [markdown]
# # ALT FIGURE: EF

# %%
#mask prep
#### BASIC PREPARATION ####
avars=['RAINNC','HFX','LH','PW','T2','RH2','HICLOUD','MDCLOUD','LOCLOUD','LCL','LFC','MsKElo','MsKE','EF']
bvars=['EF','PW','T2','RH2','LCL','LFC','MsKElo','MsKE','HICLOUD','MDCLOUD','LOCLOUD']
blist=['LND','CTL','FLR','GRL','GSL','MEX','TEX','CAL']
names=['$\Delta$EF','$\Delta$PW',r'$\Delta$$T_{2m}$',r'$\Delta$$RH_{2m}$','$\Delta$LCL','$\Delta$LFC',r'$\Delta$$MsKE_{low}$',r'$\Delta$$MsKE$',r'$\Delta$$CC_{high}$',r'$\Delta$$CC_{mid}$',r'$\Delta$$CC_{low}$']
boxes={}
for b in blist:
    boxes[b]=[]
boxes['CAL'].append([500,800,30,150])
boxes['MEX'].append([50,400,200,400])
boxes['FLR'].append([75,275,1200,1375])
boxes['GRL'].append([700,1000,900,1375])
boxes['GSL'].append([600,750,300,450])
boxes['CTL'].append([400,800,600,1000])
boxes['TEX'].append([180,350,700,1000])
boxes['LND'].append([0,1039,0,1559])
#boxes['ALL'].append([0,1039,0,1559])


masks={}
for k in boxes.keys():
    masks[k]=np.zeros((1039, 1559),dtype='bool')
    boxs=boxes[k]
    for bx in boxs:
        masks[k][bx[0]:bx[1],bx[2]:bx[3]]=True
    if k!='ALL':
        masks[k][msk]=False

fptime=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_norm.nc','r')
fptt=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_nr-ft.nc')
fptg=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_nr-fg.nc')

def fixit(f,locs,varlist,var):
    out=np.zeros((len(locs),257))
    i=0
    idx=np.where(np.array(varlist)==var)[0][0]
    for l in locs:
        out[i,:]=f[l][idx,:]
        i=i+1
    return out


# %%
### INPUTS ###
cbarlabel1=r'EF'
cbarlabel2=r'$EF_{60\ km}$ - $EF_{3\ km}$'
lbsize=16

### DATA SMOL ###
data1=fp2d['LH_60'][:]/(fp2d['LH_60'][:]+fp2d['HFX_60'][:])
data1=databig(data1)
data2=fp2d['LH_hmg'][:]/(fp2d['LH_hmg'][:]+fp2d['HFX_hmg'][:])

data1[msk]=float('nan')
data2[msk]=float('nan')

vmax=1
vmin=0


### DATA LARGE ###
data3=data2-data1
vmax3=.11
vmin3=-vmax3


### SETUP ###
fig = plt.figure(figsize=(7,7),layout='tight',dpi=500)
subfigs = fig.subfigures(3, 1, hspace=0,wspace=0, height_ratios=[.5, 1,.5],frameon=False)


#### HET and HMG ####
grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(1, 2),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="7%")

imt=grid[1].imshow(data2,origin='lower',cmap='YlGnBu',vmin=vmin,vmax=vmax)
img=grid[0].imshow(data1,origin='lower',cmap='YlGnBu',vmin=vmin,vmax=vmax)
   
grid[0].axis(False)
grid[1].axis(False)
   
grid[0].text(-50,940,'a)',fontsize=lbsize)
grid[1].text(-40,940,'b)',fontsize=lbsize)
   
#grid[0].set_title('$HMG$')
#grid[1].set_title('$HET$')

cb=grid.cbar_axes[0].colorbar(imt,label='EF')
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label='EF',size=lbsize)

##### DELTA ####
grid=ImageGrid(subfigs[1], 111,  # similar to subplot(111)
                nrows_ncols=(1, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="4%")
im=grid[0].imshow(data3,origin='lower',cmap=demap,vmin=vmin3,vmax=vmax3)
grid[0].axis(False)
grid[0].text(-20,940,'c)',fontsize=lbsize)
#grid[0].set_title('$HMG$ - $HET$')

cb=grid.cbar_axes[0].colorbar(im,label='EF')
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label='$\Delta$EF',size=lbsize)

### ADD BOXES TO DELTA ###
i=0
for k in boxes.keys():
    if k=='LND':
        i=i+1
        continue
    bxs=boxes[k]
    for bx in bxs:
        rect = patches.Rectangle((bx[2], bx[0]), bx[3]-bx[2], bx[1]-bx[0], linewidth=1, edgecolor='k', facecolor='none',path_effects=[pe.withStroke(linewidth=2, foreground="white")])
        grid[0].add_patch(rect)
    if k=='TEX':
        grid[0].text((bx[3]+bx[2])/2-85,bx[1]-260,blist[i],fontsize=lbsize,path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    elif k=='GRL':
        grid[0].text((bx[3]+bx[2])/2-85,bx[0]-90,blist[i],fontsize=lbsize,path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    else:
        grid[0].text((bx[3]+bx[2])/2-85,bx[1]+25,blist[i],fontsize=lbsize,path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    i=i+1


#### STATS ####
i=0
ax=subfigs[2].add_subplot(111)
var=bvars[i]
dg=fixit(fptime,blist,avars,var)*100
ax.boxplot(dg.T,labels=blist,showfliers=False)
ax.tick_params(axis='x',which='both',labelsize=lbsize)

d_g=fixit(fptg,blist,avars,var)*100
dd=np.nanmedian(d_g,axis=1)
d0=np.nanmedian(dg,axis=1)
cs=[]
for j in range(len(d0)):
    if dd[j]>d0[j]:
        cs.append('red')
    else:
        cs.append('blue')
ax.scatter([1,2,3,4,5,6,7,8],dd,zorder=5,c=cs,s=350,marker='_')
ax.set_yticks([0,50,100,150],[0,50,100,150])

ax.minorticks_on()
ax.set_yticks([-20,-10,10,20,30,40,60,70,80,90,110,120,130,140],[],minor=True)
ax.grid(which='minor',linestyle=':',linewidth=.5,axis='y')



ax.set_ylim(-25,155)
ax.text(.50,175,'d)',fontsize=lbsize)
ax.set_ylabel('$\%$ change EF',fontsize=lbsize)
ax.grid(visible=False,axis='x')


# %%

# %% [markdown]
# # ALT FIGURE: Wet Variables

# %%

# %%
mapvars=['PW','RH2','T2','LOCLOUD','MDCLOUD','HICLOUD']
mcmaps={'PW':'Blues','RH2':'BuPu','T2':tmap,'LOCLOUD':cmr.sepia,'MDCLOUD':cmr.sepia,'HICLOUD':cmr.sepia}
dcmaps={'PW':'PuOr','RH2':'PRGn','T2':'RdGy','LOCLOUD':'bwr','MDCLOUD':'bwr','HICLOUD':'bwr'}
mcblb={'PW':r'PW $(kg\ m^{-2})$','RH2':r'$RH_{2m} (\%)$','T2':r'$T_{2m} (C)$','LOCLOUD':r'$CC_{low} (\%)$','MDCLOUD':r'$CC_{mid} (\%)$','HICLOUD':r'$CC_{high} (\%)$'}
lbsize=10
letter=['a','b','c','d','e','f','g']

alpha=1.2
fig=plt.figure(figsize=(6.5*alpha,8*alpha),layout='tight',dpi=600)
subfigs = fig.subfigures(len(mapvars),4, hspace=0,wspace=0, width_ratios=[.45,1,.2, .9],frameon=False)

for i in range(len(mapvars)):
    var=mapvars[i]
    grid=ImageGrid(subfigs[i,0], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='left',
                cbar_pad=.02,
                cbar_size="5%")
    
    ### DATA PREP ###
    datat=fp2d[var+'_het'][:]
    datag=fp2d[var+'_hmg'][:]
    try:
        datat[msk]=float('nan')
    except Exception as e:
        datat=databig(datat)
        datat[msk]=float('nan')
    try:
        datag[msk]=float('nan')
    except Exception as e:
        datag=databig(datag)
        datag[msk]=float('nan')
    if 'T2' in var:
        datag=datag-273.15
        datat=datat-273.15
    if ('CLOUD' in var):
        datag=datag*100
        datat=datat*100
        vmin=1
        vmax=50
    elif ('RH' in var):
        vmin=1
        vmax=100
    else:
        vmin=np.nanpercentile(datat,2)
        vmax=np.nanpercentile(datat,98)
    data3=datag-datat
    if 'CLOUD' in var:
        vmax3=7
        vmin3=-7
    elif 'T2' in var:
        vmax3=3
        vmin3=-3
    elif 'PW' in var:
        vmax3=2.5
        vmin3=-2.5
    else:
        vmax3=max(np.abs(np.nanpercentile(data3,1)),np.abs(np.nanpercentile(data3,99)))
        vmin3=-vmax3
    
    imt=grid[1].imshow(datat,origin='lower',cmap=mcmaps[var],vmin=vmin,vmax=vmax)
    img=grid[0].imshow(datag,origin='lower',cmap=mcmaps[var],vmin=vmin,vmax=vmax)
    grid[0].axis(False)
    grid[1].axis(False)
    cb=grid.cbar_axes[0].colorbar(imt,label=mcblb[var])
    grid.cbar_axes[0].tick_params(labelsize=lbsize)
    cb.set_label(label=mcblb[var],size=lbsize)
    grid.cbar_axes[0].yaxis.set_ticks_position('left')
    grid.cbar_axes[0].yaxis.set_label_position('left')
   
    grid[0].text(-1100,940,letter[i]+')',fontsize=lbsize+4)
    
    ### Delta Plot
    grid=ImageGrid(subfigs[i,1], 111,  # similar to subplot(111)
                nrows_ncols=(1, 1),
                axes_pad=0,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="5%")

    im=grid[0].imshow(data3,origin='lower',cmap=dcmaps[var],vmin=vmin3,vmax=vmax3)
    grid[0].axis(False)
    cb=grid.cbar_axes[0].colorbar(im,label='$\Delta$'+mcblb[var])
    grid.cbar_axes[0].tick_params(labelsize=lbsize)
    cb.set_label(label='$\Delta$'+mcblb[var],size=lbsize)
    
    ### BOXPLOT ###
    ax=subfigs[i,3].add_subplot(111)
    dg=fixit(fptime,blist,avars,var)*100
    ax.plot([-1,10],[0,0],linewidth=2,color='white',zorder=0)
    ax.boxplot(dg.T,labels=blist,showfliers=False)
    ax.tick_params(axis='x',which='both',labelsize=lbsize,labelrotation=45)
    
    d_g=fixit(fptg,blist,avars,var)*100
    dd=np.nanmedian(d_g,axis=1)
    d0=np.nanmedian(dg,axis=1)
    cs=[]
    for j in range(len(d0)):
        if dd[j]>d0[j]:
            cs.append('red')
        else:
            cs.append('blue')
    ax.scatter([1,2,3,4,5,6,7,8],dd,zorder=5,c=cs,s=150,marker='_')
    if 'CLOUD' in var:
        ax.set_yticks([0,50,100],[0,50,100])
        ax.minorticks_on()
        ax.set_yticks([-20,-10,10,20,30,40,60,70,80,90,110,120],[],minor=True)
        ax.grid(which='minor',linestyle=':',linewidth=.5,axis='y')
        ax.set_ylim(-25,125)
    else:
        ax.set_yticks([-10,0,10,20],[-10,0,10,20])
        ax.set_ylim(-15,25)
        
    ax.grid(visible=False,axis='x')
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.set_ylabel('$\%$ Change',fontsize=lbsize)
    ax.set_xlim(.5,8.5)

plt.savefig('fig9_alt.png', bbox_inches = "tight")

# %%
print(np.nanmedian(d_g,axis=1))

# %%
print(np.nanmedian(dg,axis=1))

# %%
d0

# %% [markdown]
# # ALT MsKE

# %%
mapvars=['MsKElo','MsKE']
mcmaps={'MsKElo':'copper','MsKE':'pink'}
dcmaps={'MsKElo':dmmap,'MsKE':cmr.holly_r}
mcblb={'MsKElo':r'$MsKE_{low}$ ($m^{2} s^{-2}$)',
      'MsKE':r'$MsKE$ ($m^{2} s^{-2}$)'}
lbsize=10
letter=['a','b','c','d','e','f','g']

alpha=1.2
fig=plt.figure(figsize=(6.5*alpha,3*alpha),layout='tight',dpi=600)
subfigs = fig.subfigures(len(mapvars),4, hspace=0,wspace=0, width_ratios=[.45,1,.2, .9],frameon=False)

for i in range(len(mapvars)):
    var=mapvars[i]
    grid=ImageGrid(subfigs[i,0], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='left',
                cbar_pad=.02,
                cbar_size="5%")
    
    ### DATA PREP ###
    datat=fp2d[var+'_het'][:]
    datag=fp2d[var+'_hmg'][:]
    datat=databig(datat)
    datat[msk]=float('nan')
    datag=databig(datag)
    datag[msk]=float('nan')
        
    vmin=np.nanpercentile(datat,2)
    vmax=np.nanpercentile(datat,98)
    data3=datag-datat
    
    if 'lo' in var:
        vmin=800
        vmax=2400
        vmin3=-300
        vmax3=300
    else:
        vmin=8000
        vmax=24000
        vmin3=-3000
        vmax3=3000
    
    imt=grid[1].imshow(datat,origin='lower',cmap=mcmaps[var],vmin=vmin,vmax=vmax)
    img=grid[0].imshow(datag,origin='lower',cmap=mcmaps[var],vmin=vmin,vmax=vmax)
    grid[0].axis(False)
    grid[1].axis(False)
    cb=grid.cbar_axes[0].colorbar(imt,label=mcblb[var])
    grid.cbar_axes[0].tick_params(labelsize=lbsize)
    cb.set_label(label=mcblb[var],size=lbsize)
    grid.cbar_axes[0].yaxis.set_ticks_position('left')
    grid.cbar_axes[0].yaxis.set_label_position('left')
   
    grid[0].text(-1300,940,letter[i]+')',fontsize=lbsize+4)
    
    ### Delta Plot
    grid=ImageGrid(subfigs[i,1], 111,  # similar to subplot(111)
                nrows_ncols=(1, 1),
                axes_pad=0,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="5%")

    im=grid[0].imshow(data3,origin='lower',cmap=dcmaps[var],vmin=vmin3,vmax=vmax3)
    grid[0].axis(False)
    cb=grid.cbar_axes[0].colorbar(im,label='$\Delta$'+mcblb[var])
    grid.cbar_axes[0].tick_params(labelsize=lbsize)
    cb.set_label(label='$\Delta$'+mcblb[var],size=lbsize)
    
    ### BOXPLOT ###
    ax=subfigs[i,3].add_subplot(111)
    dg=fixit(fptime,blist,avars,var)*100
    ax.plot([-1,10],[0,0],linewidth=2,color='white',zorder=0)
    ax.boxplot(dg.T,labels=blist,showfliers=False)
    ax.tick_params(axis='x',which='both',labelsize=lbsize,labelrotation=45)
    
    d_g=fixit(fptg,blist,avars,var)*100
    dd=np.nanmedian(d_g,axis=1)
    d0=np.nanmedian(dg,axis=1)
    cs=[]
    for j in range(len(d0)):
        if dd[j]>d0[j]:
            cs.append('red')
        else:
            cs.append('blue')
    ax.scatter([1,2,3,4,5,6,7,8],dd,zorder=5,c=cs,s=150,marker='_')
    
    ax.set_yticks([-40,-20,0,20,40],[-40,-20,0,20,40])
    ax.minorticks_on()
    ax.set_yticks([-30,-10,10,30],[],minor=True)
    ax.set_ylim(-45,45)
    ax.grid(which='minor',linestyle=':',linewidth=.5,axis='y')
    
    ax.grid(visible=False,axis='x')
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.set_ylabel('$\%$ Change',fontsize=lbsize)
    ax.set_xlim(.5,8.5)

plt.savefig('fig10_alt.png', bbox_inches = "tight")


# %%

# %%

# %%

# %%

# %% [markdown]
# # FIUGRE 14 All Stats

# %%
def fixit(f,locs,varlist,var):
    out=np.zeros((len(locs),257))
    i=0
    idx=np.where(np.array(varlist)==var)[0][0]
    for l in locs:
        out[i,:]=f[l][idx,:]
        i=i+1
    return out


# %%
fptime=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_norm.nc')
fptt=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_nr-ft.nc')
fptg=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_nr-fg.nc')

# %%
#d_g=fixit(fptg,blist,avars,var)
#ax.scatter([1,2,3,4,5,6,7,8],np.nanmedian(d_g,axis=1),zorder=5)

# %%
#### BASIC PREPARATION ####
avars=['RAINNC','HFX','LH','PW','T2','RH2','HICLOUD','MDCLOUD','LOCLOUD','LCL','LFC','MsKElo','MsKE','EF']
bvars=['EF','PW','T2','RH2','LCL','LFC','MsKElo','MsKE','HICLOUD','MDCLOUD','LOCLOUD']
blist=['LND','CTL','FLR','GRL','GSL','MEX','TEX','CAL']
names=['$\Delta$EF','$\Delta$PW',r'$\Delta$$T_{2m}$',r'$\Delta$$RH_{2m}$','$\Delta$LCL','$\Delta$LFC',r'$\Delta$$MsKE_{low}$',r'$\Delta$$MsKE$',r'$\Delta$$CC_{high}$',r'$\Delta$$CC_{mid}$',r'$\Delta$$CC_{low}$']
boxes={}
for b in blist:
    boxes[b]=[]
boxes['CAL'].append([500,800,30,150])
boxes['MEX'].append([50,400,200,400])
boxes['FLR'].append([75,275,1200,1375])
boxes['GRL'].append([700,1000,900,1375])
boxes['GSL'].append([600,750,300,450])
boxes['CTL'].append([400,800,600,1000])
boxes['TEX'].append([180,350,700,1000])
boxes['LND'].append([0,1039,0,1559])
#boxes['ALL'].append([0,1039,0,1559])


masks={}
for k in boxes.keys():
    masks[k]=np.zeros((1039, 1559),dtype='bool')
    boxs=boxes[k]
    for bx in boxs:
        masks[k][bx[0]:bx[1],bx[2]:bx[3]]=True
    if k!='ALL':
        masks[k][msk]=False

#### RUN ####
a=1.6
#fig=plt.figure(figsize=(6.5*a,5*a),layout='tight')
fig,axs=plt.subplots(8,1,figsize=(2.5*a,6*a),layout='tight',dpi=400)
i=0
for ax in axs.flatten():
    print(i,flush=True)
    var=bvars[i]
    dg=fixit(fptime,blist,avars,var)
    ax.boxplot(dg.T,labels=blist,showfliers=False)
    
    d_g=fixit(fptg,blist,avars,var)
    dd=np.nanmedian(d_g,axis=1)
    d0=np.nanmedian(dg,axis=1)
    cs=[]
    for j in range(len(d0)):
        if dd[j]>d0[j]:
            cs.append('red')
        else:
            cs.append('blue')
    ax.scatter([1,2,3,4,5,6,7,8],dd,zorder=5,c=cs,s=150,marker='_')
    
    #ax.set_xlim(-1.5,10.5)
    ax.set_ylabel(names[i])
    #ax.set_yticks([-.4,0,.4],[])
    if (var=='EF') or (var =='LOCLOUD') or (var =='MDCLOUD'):
        ax.set_yticks([0,.5,1,1.5],[0,.5,1,1.5])
        ax.set_ylim(-.5,2)
    else:
        ax.set_yticks([-.2,0,.2],[-.2,0,.2])
        ax.set_ylim(-.4,.4)
    if i ==7:
        ax.set_xticklabels(blist,rotation=45)
        ax.grid(visible=False,axis='x')
    else:
        ax.set_xticks([],[])
    
    i=i+1

# %%
ax=plt.subplot(1,1,1)
data=fp2d['HFX_het'][:]
data[msk]=float('nan')
#data[masks['CAL']]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo')
plt.axis(False)
i=0
for k in boxes.keys():
    if k=='LND':
        i=i+1
        continue
    bxs=boxes[k]
    for bx in bxs:
        rect = patches.Rectangle((bx[2], bx[0]), bx[3]-bx[2], bx[1]-bx[0], linewidth=2, edgecolor='k', facecolor='none')
        ax.add_patch(rect)
    if k=='TEX':
        plt.text((bx[3]+bx[2])/2-85,bx[1]-245,blist[i],fontsize=lbsize+6)
    elif k=='GRL':
        plt.text((bx[3]+bx[2])/2-85,bx[0]-75,blist[i],fontsize=lbsize+6)
    else:
        plt.text((bx[3]+bx[2])/2-85,bx[1]+25,blist[i],fontsize=lbsize+6)
    i=i+1
cb=plt.colorbar(shrink=.73,location='bottom')
cb.set_label(label=r'H ($W/m^{-2}$)',size=lbsize+6)

# %%

# %%

# %%
fpst.variables

# %%

# %% [markdown]
# # FIUGRE Testing

# %%

# %%
dd=fptg['GSL'][:]
dd.shape
for i in range(14):
    plt.figure()
    ddd=dd[i,:]
    mmm=np.isinf(ddd)
    if np.sum(mmm)>0:
        print('ERROR: '+str(np.sum(mmm)))
        print(avars[i])
        print('ERROR')
        ddd=ddd[~mmm]
    plt.hist(ddd)


# %%
vars=['RAINNC','HFX','LH','HICLOUD','MDCLOUD','LOCLOUD','LCL','LFC','MsKElo','MsKE','EF']
datab={}
datab['CAL']=np.zeros((len(vars),257))
datab['MEX']=np.zeros((len(vars),257))
datab['FLR']=np.zeros((len(vars),257))
datab['GRL']=np.zeros((len(vars),257))
datab['GSL']=np.zeros((len(vars),257))
datab['CTL']=np.zeros((len(vars),257))
datab['TEX']=np.zeros((len(vars),257))
datab['ALL']=np.zeros((len(vars),257))
masks={}
for k in datab.keys():
    masks[k]=np.zeros((1039, 1559),dtype='bool')
masks['CAL'][500:800,50:150]=True
masks['MEX'][100:400,300:400]=True
masks['FLR'][75:200,1275:1350]=True
masks['GRL'][800:1000,900:1300]=True
masks['GSL'][600:750,300:450]=True
masks['CTL'][400:800,600:1000]=True
masks['TEX'][180:350,700:1000]=True
masks['ALL'][:]=True
    
i=0
for var in vars:
    print(var)
    if var=='HF':
        datat=fpagg['LH_het'][:]/(fpagg['HFX_het'][:]+fpagg['LH_het'][:])
        datag=fpagg['LH_hmg'][:]/(fpagg['HFX_hmg'][:]+fpagg['LH_hmg'][:])
    else:
        datag=fpagg[var+'_hmg'][:]
        datat=fpagg[var+'_het'][:]
    for k in datab.keys():
        print(k)
        datab[k][i,:]=(np.mean(datag[:,masks[k]],axis=(1))-np.mean(datat[:,masks[k]],axis=(1)))/np.mean(datat[:,masks[k]],axis=(1))
    
    i=i+1

# %%
datat=fpagg['LH_het'][:]/(fpagg['HFX_het'][:]+fpagg['LH_het'][:])

# %%
d=datat[:,masks['CAL'][:]]

# %%

# %%
plt.boxplot(data.T,labels=vars)
plt.xticks(rotation=45)

# %%
fptest=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/raintime.nc','r')

# %%
data1.shape

# %%
flist=[]
for file in os.listdir('/home/tsw35/tyche/wrf_gaea/'):
    if (file=='old') or (file=='mswep_gaea') or (file=='all'):
        continue
    else:
        flist.append(file)
flist.sort()

# %%
data=np.zeros((257,))
i=0
for file in flist:
    print('.',end='',flush=True)
    fp=nc.Dataset('/home/tsw35/tyche/wrf_gaea/'+file,'r')
    lht=np.zeros((1039, 1559))
    lhg=np.zeros((1039, 1559))
    rt=fptest['RAINTIME1_het'][i,:,:]
    rg=fptest['RAINTIME1_het'][i,:,:]
    for t in range(2,49):
        mm=(rg==(t))&(rt>=t)
        lht[mm]=fp['LH_het'][t-1,:,:][mm]
        lhg[mm]=fp['LH_hmg'][t-1,:,:][mm]
    data[i]=np.mean(lhg-lht)
    i=i+1

# %%
plt.plot(data[data!=0])

# %%
data=fptest['RAINTIME1_het'][5,:,:]

# %%
plt.imshow(data,origin='lower',cmap='turbo')
plt.colorbar()

# %%
a=np.array(['abc','def','ghi','jkl','mnop'])
np.where(a=='ghi')[0][0]


# %%
def reorder(indata,invar,outvar):
    invar=np.array(invar)
    outdata=np.zeros((len(outvar),indata.shape[1]))
    i=0
    for var in outvar:
        idx=np.where(invar==var)[0][0]
        outdata[i,:]=indata[idx,:]
        i=i+1
    return outdata


# %%
avars=['RAINNC','HFX','LH','PW','T2','RH2','HICLOUD','MDCLOUD','LOCLOUD','LCL','LFC','MsKElo','MsKE','EF']
bvars=['PW','T2','RH2','LCL','LFC','MsKElo','MsKE','HICLOUD','MDCLOUD','LOCLOUD','EF']
fptime=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_norm.nc','r')
for typ in ['CAL']:
    dg=reorder(fptime[typ][:],avars,bvars)
    plt.figure()
    plt.boxplot(dg.T,labels=bvars)
    plt.xticks(rotation=45)
    plt.title(typ)
    plt.ylim(-.5,.5)

# %%
fig = plt.figure(figsize=(9,4.5),layout='tight')
subfigs = fig.subfigures(1, 2, hspace=0,wspace=.1, width_ratios=[1, .33],frameon=False)
subfigs[0].add_subplot(111)
plt.boxplot(dg[0:9,:].T,labels=bvars[0:9])
plt.xticks(rotation=45)
plt.yticks([-.25,0,.25])
plt.title(typ)
plt.ylim(-.5,.5)

ax=subfigs[1].add_subplot(111)
plt.boxplot(dg[9:,:].T,labels=bvars[9:])
plt.xticks(rotation=45)
plt.yticks([-1.25,-1,-.75,-.5,-.25,0,.25,.5,.75,1.0,1.25])
plt.title(typ)
plt.ylim(-1.5,1.5)
ax.yaxis.tick_right()

# %%
bvars=['PW','T2','RH2','HICLOUD','MDCLOUD','LOCLOUD','LCL','LFC','MsKElo','MsKE','EF']
fptime=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_norm.nc','r')
for typ in ['CAL','MEX','FLR','GRL','GSL','CTL','TEX','LND','ALL']:
    dg=fptime[typ][3:]
    plt.figure()
    plt.boxplot(dg.T,labels=bvars)
    plt.xticks(rotation=45)
    plt.title(typ)
    plt.ylim(-.5,.5)

# %%
bvars=['RAINNC','HFX','LH','PW','T2','RH2','HICLOUD','MDCLOUD','LOCLOUD','LCL','LFC','MsKElo','MsKE','EF']
fptime=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_nr-day.nc','r')
for typ in ['CAL','MEX','FLR','GRL','GSL','CTL','TEX','LND','ALL']:
    dg=fptime[typ][:]
    plt.figure()
    plt.boxplot(dg.T,labels=bvars)
    plt.xticks(rotation=45)
    plt.title(typ)
    plt.ylim(-2,2)

# %%
#EFhmg=np.mean(fp['LH_hmg'][:,:,:],axis=0)/(np.mean(fp['LH_hmg'][:,:,:],axis=0)+np.mean(fp['HFX_hmg'][:,:,:],axis=0))
#EFhet=np.mean(fp['LH_60'][:,:,:],axis=0)/(np.mean(fp['LH_60'][:,:,:],axis=0)+np.mean(fp['HFX_60'][:,:,:],axis=0))

### INPUTS ###
cbarlabel1=r'EF'
cbarlabel2=r'$EF_{60\ km}$ - $EF_{3\ km}$'
lbsize=18

### DATA SMOL ###
data1=np.mean(fpagg['PW_het'][:],axis=0)
data2=np.mean(fpagg['PW_hmg'][:],axis=0)
data1[msk]=float('nan')
data2[msk]=float('nan')

vmax=np.nanpercentile(data1,99)
vmin=np.nanpercentile(data1,1)


### DATA LARGE ###
data3=data2-data1
vmax3=np.nanpercentile(np.abs(data3),97)
vmin3=-vmax3


### SETUP ###
fig = plt.figure(figsize=(9,4.5),layout='tight')
subfigs = fig.subfigures(1, 2, hspace=0,wspace=0, width_ratios=[.45, 1],frameon=False)
#subfigs[0].add_subplot(1,1,1)
#subfigs[1].add_subplot(1,1,1)
#### LEFT SIDE FIGURES ####
grid=ImageGrid(subfigs[0], 111,  # similar to subplot(111)
                nrows_ncols=(2, 1),
                axes_pad=0.05,
                cbar_mode='single',
                cbar_location='bottom',
                cbar_pad=.02,
                cbar_size="10%")

im=grid[0].imshow(data1,origin='lower',cmap=hmap,vmin=vmin,vmax=vmax)
im=grid[1].imshow(data2,origin='lower',cmap=hmap,vmin=vmin,vmax=vmax)
grid[0].axis(False)
grid[1].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel1)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel1,size=lbsize)
grid[0].text(-50,940,'a)',fontsize=lbsize)
grid[1].text(-50,940,'b)',fontsize=lbsize)


#### RIGHT SIDE FIGURE ####
grid=ImageGrid(subfigs[1], 111,  # similar to subplot(111)
                nrows_ncols=(1, 1),
                axes_pad=0,
                cbar_mode='single',
                cbar_location='right',
                cbar_pad=.02,
                cbar_size="3%")

im=grid[0].imshow(data3,origin='lower',cmap=demap,vmin=vmin3,vmax=vmax3)
grid[0].axis(False)
cb=grid.cbar_axes[0].colorbar(im,label=cbarlabel2)
grid.cbar_axes[0].tick_params(labelsize=lbsize)
cb.set_label(label=cbarlabel2,size=lbsize)
grid[0].text(0,980,'c)',fontsize=lbsize)

# %%

# %%
fpt1=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/pretest.nc','r')
fpt2=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/pretest_full.nc','r')

# %%
dt=fpt2['gLH_het'][0,:]/(fpt2['gLH_het'][0,:]+fpt2['gHFX_het'][0,:])
dg=fpt2['gLH_hmg'][0,:]/(fpt2['gLH_hmg'][0,:]+fpt2['gHFX_hmg'][0,:])


# %%

# %%
plt.imshow(dg-dt,origin='lower',cmap='turbo',vmin=-1,vmax=1)
plt.colorbar()

# %%
np.nanmean(dg-dt)

# %%
blist=['CAL','MEX','FLR','GRL','GSL','CTL','TEX','ALL','LND']
boxes={}
for b in blist:
    boxes[b]=[]
boxes['CAL'].append([500,800,30,150])
boxes['MEX'].append([50,400,200,400])
boxes['FLR'].append([75,275,1200,1375])
boxes['GRL'].append([700,1000,900,1375])
boxes['GSL'].append([600,750,300,450])
boxes['CTL'].append([400,800,600,1000])
boxes['TEX'].append([180,350,700,1000])
boxes['LND'].append([0,1039,0,1559])
boxes['ALL'].append([0,1039,0,1559])


masks={}
for k in boxes.keys():
    masks[k]=np.zeros((1039, 1559),dtype='bool')
    boxs=boxes[k]
    for bx in boxs:
        masks[k][bx[0]:bx[1],bx[2]:bx[3]]=True
    if k!='ALL':
        masks[k][msk]=False

# %%
ax=plt.subplot(1,1,1)
data=fp2d['HFX_het'][:]
data[msk]=float('nan')
#data[masks['CAL']]=float('nan')
plt.imshow(data,origin='lower',cmap='terrain')
plt.grid(False)
for k in boxes.keys():
    bxs=boxes[k]
    for bx in bxs:
        rect = patches.Rectangle((bx[2], bx[0]), bx[3]-bx[2], bx[1]-bx[0], linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

#rect = patches.Rectangle((50, 500), 100, 300, linewidth=1, edgecolor='w', facecolor='none')


# %%
data.shape

# %%
data.shape

# %%
dm=np.zeros((1039),dtype='bool')
dm[1]=True
dm[234]=True
dm[24]=True
dm[232]=True
dm[235]=True
dm[834]=True
d2=data[dm,100:200]

# %%
dg.shape

# %%
bvars=['HFX','LH','PW','T2','RH2','HICLOUD','MDCLOUD','LOCLOUD','LCL','LFC','MsKElo','MsKE','EF']
varis={}
for k in masks.keys():
    varis[k]=np.zeros((13,))
i=0
for var in bvars:
    print('*',end='',flush=True)
    if var in ['PW','T2','RH2']:
        data=np.mean(fpagg[var+'_het'][:],axis=0)
    elif 'MsKE' in var:
        data=databig(fp2d[var+'_het'][:])
    else:
        data=fp2d[var+'_het'][:]
    for k in masks.keys():
        print('.',end='')
        varis[k][i]=np.sqrt(np.nanvar(data[masks[k]]))
    i=i+1

# %%
bvars=['HFX','LH','PW','T2','RH2','HICLOUD','MDCLOUD','LOCLOUD','LCL','LFC','MsKElo','MsKE','EF']
means={}
for k in masks.keys():
    means[k]=np.zeros((13,))
i=0
for var in bvars:
    print('*',end='',flush=True)
    if var in ['PW','T2','RH2']:
        data=np.mean(fpagg[var+'_het'][:],axis=0)
    elif 'MsKE' in var:
        data=databig(fp2d[var+'_het'][:])
    else:
        data=fp2d[var+'_het'][:]
    for k in masks.keys():
        print('.',end='')
        if var=='T2':
            means[k][i]=np.nanmean(data[masks[k]]-273)
        means[k][i]=np.nanmean(data[masks[k]])
    i=i+1

# %%
EF=fp2d['LH_het'][:]/(fp2d['LH_het'][:]+fp2d['HFX_het'][:])
for k in masks.keys():
    varis[k][-1]=np.nanvar(EF[masks[k]])
    means[k][-1]=np.nanmean(EF[masks[k]])

# %%
mean2={}
for k in masks.keys():
    mean2[k]=np.zeros((13,257))
i=0
for var in bvars:
    print('*',end='',flush=True)
    if var in ['PW','T2','RH2']:
        data=np.mean(fpagg[var+'_het'][:],axis=0)
    if 'MsKE' in var:
        data=databig2(fpagg[var+'_het'][:])
    elif 'T2' in var:
        data=fp2d[var+'_het'][:]
    elif var=='EF':
        
    else:
        data=fp2d[var+'_het'][:]
    for k in masks.keys():
        print('.',end='')
        means[k][i]=np.nanmean(data[masks[k]])
    i=i+1

# %%
bvars=['RAINNC','HFX','LH','PW','T2','RH2','HICLOUD','MDCLOUD','LOCLOUD','LCL','LFC','MsKElo','MsKE','EF']
fpt1=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_norm.nc','r')
fpt2=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/time_stats_nr-day.nc','r')
for typ in ['CAL','MEX','FLR','GRL','GSL','CTL','TEX','LND','ALL']:
    print(typ,flush=True)
    dg1=fpt1[typ][3:]
    dg2=fpt2[typ][3:]
    plt.figure(dpi=150)
    plt.boxplot(dg1.T,positions=[1,3,5,7,9,11,13,15,17,19,21],labels=bvars[3:])
    plt.boxplot(dg2.T,positions=np.array([1,3,5,7,9,11,13,15,17,19,21])+1)
    plt.xticks(rotation=45)
    plt.title(typ)
    plt.ylim(-.5,.5)

# %%

# %%

# %%
print(means)

# %%
dddt=np.mean(databig2(fpagg['MsKE_het'][:])[:,~msk],axis=(1))
dddg=np.mean(databig2(fpagg['MsKE_hmg'][:])[:,~msk],axis=(1))

# %%
plt.plot((dddg-dddt)/dddt)

# %%
plt.plot(dddg)
plt.plot(dddt)

# %%
ddgt=fpt1['LND'][-2]

# %%
plt.plot(ddgt/dddt)

# %%
plt.plot(ddgt)

# %%
fpt2.close()

# %%
print(np.min(fpagg['HFX_het'][:]))
print(np.max(fpagg['HFX_het'][:]))

# %%
print(np.min(fpagg['LH_het'][:]))
print(np.max(fpagg['LH_het'][:]))

# %%
