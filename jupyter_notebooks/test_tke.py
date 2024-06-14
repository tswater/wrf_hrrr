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
### 20230705
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
data.shape

# %%

# %%

# %%
base_dir='/home/tsw35/xTyc_shared/compressed_output/2023/'

# %%
tke3=np.zeros((2,48))
tke6=np.zeros((2,48))
tke12=np.zeros((2,48))
tke24=np.zeros((2,48))
tke60=np.zeros((2,48))

# %%
hetdir=base_dir+'20230705_het/'
hmgdir=base_dir+'20230705_hmg/'
flist=os.listdir(hetdir)
flist.sort()

# %%
flist=os.listdir(hetdir)
flist.sort()
t=0
for file in flist[33:36]:
    print(file)
    fphet=nc.Dataset(hetdir+file,'r')
    fphmg=nc.Dataset(hmgdir+file,'r')
    ut=wrf.getvar(fphet,'ua',meta=False)
    vt=wrf.getvar(fphet,'va',meta=False)
    wt=wrf.getvar(fphet,'wa',meta=False)
    ug=wrf.getvar(fphmg,'ua',meta=False)
    vg=wrf.getvar(fphmg,'va',meta=False)
    wg=wrf.getvar(fphmg,'wa',meta=False)
    
    tke3[0,t]=np.mean(tke(ug,vg,wg,3))
    tke3[1,t]=np.mean(tke(ut,vt,wt,3))
    
    tke6[0,t]=np.mean(tke(ug,vg,wg,6))
    tke6[1,t]=np.mean(tke(ut,vt,wt,6))
    
    tke12[0,t]=np.mean(tke(ug,vg,wg,12))
    tke12[1,t]=np.mean(tke(ut,vt,wt,12))
    
    tke24[0,t]=np.mean(tke(ug,vg,wg,24))
    tke24[1,t]=np.mean(tke(ut,vt,wt,24))
    
    tke60[0,t]=np.mean(tke(ug,vg,wg,60))
    tke60[1,t]=np.mean(tke(ut,vt,wt,60))
    
    t=t+1

# %%
rain=np.zeros((48,1039,1559))

# %%
t=0
for file in flist:
    print(t,end=',')
    fphet=nc.Dataset(hetdir+file,'r')
    rain[t,:]=fphet['RAINNC'][0,:,:]
    t=t+1

# %%
plt.imshow(rain[35,:,:],origin='lower',cmap='turbo',vmax=100)


# %%
plt.plot(np.mean(rain[1:,:]-rain[0:-1,:],axis=(1,2)))

# %%
file=flist[35]
fphet=nc.Dataset(hetdir+file,'r')
fphmg=nc.Dataset(hmgdir+file,'r')
ut=wrf.getvar(fphet,'ua',meta=False)
vt=wrf.getvar(fphet,'va',meta=False)
wt=wrf.getvar(fphet,'wa',meta=False)
ug=wrf.getvar(fphmg,'ua',meta=False)
vg=wrf.getvar(fphmg,'va',meta=False)
wg=wrf.getvar(fphmg,'wa',meta=False)

# %%
ut.shape

# %%
lvl=3


# %%
def tke(u,v,w,lvl,scl):
    nx=int(u.shape[1]/scl)
    ny=int(u.shape[2]/scl)
    out=np.zeros((nx,ny))
    for i in range(nx):
        print(i,end=',')
        for j in range(ny):
            uu=u[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
            uu=uu-np.mean(uu)
            
            vv=v[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
            vv=vv-np.mean(vv)
            
            ww=w[lvl,int(i*scl):int((i+1)*scl),int(j*scl):int((j+1)*scl)]
            ww=ww-np.mean(ww)
            
            out[i,j]=.5*(np.mean(uu**2)+np.mean(vv**2)+np.mean(ww**2))
    return out


# %%
tke0t=tke(ut,vt,wt,2,20)

# %%
tke0g=tke(ug,vg,wg,2,20)

# %%
np.percentile(tke0t,99)

# %%
plt.imshow(tke0t,origin='lower',cmap='turbo',vmax=19)

# %%
plt.imshow(tke0g,origin='lower',cmap='turbo',vmax=19)

# %%
plt.imshow(tke0t-tke0g,origin='lower',cmap='coolwarm',vmax=10,vmin=-10)

# %%
tkedir='/home/tsw35/tyche/wrf_gaea/'
flist=os.listdir(tkedir)
tke60het=np.zeros((83,52,78))
tke60hmg=np.zeros((83,52,78))
dpct=np.zeros((83,52,78))
flist.sort()
t=0
for file in flist:
    if file=='all':
        continue
    fp=nc.Dataset(tkedir+file,'r')
    tke60het[t,:,:]=np.mean(fp['TKE60_het'][24:,:],axis=0)
    tke60hmg[t,:,:]=np.mean(fp['TKE60_hmg'][24:,:],axis=0)
    dpct[t,:,:]=np.mean((fp['TKE60_het'][24:,:]-fp['TKE60_hmg'][24:,:])/fp['TKE60_hmg'][24:,:],axis=0)
    t=t+1

# %%
plt.imshow(np.mean(tke60het,axis=0),origin='lower',cmap='turbo',vmin=0,vmax=12.5)

# %%
plt.imshow(np.mean(tke60hmg,axis=0),origin='lower',cmap='turbo',vmin=0,vmax=12.5)

# %%
print(np.min(tke60het))

# %%
plt.imshow(np.mean(tke60het-tke60hmg,axis=0),origin='lower',cmap='coolwarm',vmin=-1,vmax=1)
plt.colorbar()

# %%
plt.imshow(np.mean(tke60het-tke60hmg,axis=0)/np.mean(tke60hmg,axis=0),origin='lower',cmap='coolwarm',vmin=-.5,vmax=.5)
plt.colorbar()

# %%
plt.imshow(np.mean(dpct,axis=0),origin='lower',cmap='seismic',vmin=-1.5,vmax=1.5)
plt.colorbar()

# %%
capes=wrf.getvar(fphet,'cape_2d',meta=False)
print('done',flush=True)
clouds=wrf.getvar(fphet,'cloudfrac',meta=False)

# %%
wrf.getvar(fphet,'rho',meta=False)

# %%
for v in fphet.variables:
    try:
        if 'rho' in fphet[v].description:
            print(v)
    except:
        print('ERROR: '+str(v))
    if 'T' in v:
        print(v)

# %%
a=fphet['T'][:]

# %%
a.shape

# %%
pg=wrf.getvar(fphmg,'pres',meta=False)
qvg=fphmg['QVAPOR'][0,:,:,:]
Tg=wrf.getvar(fphmg,'tk',meta=False)
rhog=pg/(287*(1+(.608*qvg))*Tg)


# %%
np.mean(rhog[0,:,:])

# %%
np.mean(Tg[0,:])

# %%
fphmg['TMN'].description

# %%
# CLOUDS
# CAPE2D 
# MsKE [DONE]
# HFX (at 60; also variance)
# LH (at 60; also variance)
# LWP
# RAINNC

# %%
fphet.close()

# %%
fphmg.close()

# %%
fp.close()

# %%
fphet=nc.Dataset(hetdir+'cmp_2023-07-05_21:00:00','r')

# %%
a=wrf.getvar(fphet,'cloudfrac',meta=False)

# %%
a.shape

# %%
test='/home/tsw35/tyche/wrf_gaea/all/agg_full.nc'
fp=nc.Dataset(test,'r')

# %%
for v in fp.variables:
    if v=='time':
        continue
    plt.figure()
    data=np.mean(fp[v][:,:,:],axis=0)
    plt.imshow(data,origin='lower',cmap='turbo',vmin=np.percentile(data,1),vmax=np.percentile(data,99))
    plt.colorbar()
    plt.title(str(v))

# %%
fpst=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/201707_long/het/OUTPUT/static_data.nc','r')

# %%
varlist=['LWP','LCL','LFC','MsKE','LOCLOUD','MDCLOUD','HICLOUD']
for var in varlist:
    plt.figure()
    data=np.median(fp[var+'_het'][:,:,:],axis=0)-np.median(fp[var+'_hmg'][:,:,:],axis=0)
    minmax=max(np.abs(np.percentile(data,2)),np.abs(np.percentile(data,98)))
    try:
        data[fpst['LU_INDEX'][0,:,:]==17]=float('nan')
    except:
        data[modei(fpst['LU_INDEX'][0,:,:])==17]=float('nan')
    plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-minmax,vmax=minmax)
    plt.colorbar()
    plt.title(str(var))


# %%
def meani(data,df=20):
    nx=int(data.shape[0]/df+1)
    ny=int(data.shape[1]/df+1)
    dout=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            dout[i,j] = np.nanmean(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout


# %%
from scipy import stats


# %%
def modei(data,df=20):
    nx=int(data.shape[0]/df+1)
    ny=int(data.shape[1]/df+1)
    dout=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            dout[i,j] = stats.mode(data[i*df:(i+1)*df,j*df:(j+1)*df],axis=None)[0][0]
    return dout


# %%
stats.mode(data,axis=None)[0][0]

# %%
d2=-np.mean(fp['HFX_hmg'][:,:,:],axis=0)-np.mean(fp['LH_hmg'][:,:,:],axis=0)
d2=meani(d2)
data=np.mean(fp['HFX_60'][:,:,:],axis=0)+d2+np.mean(fp['LH_60'][:,:,:],axis=0)
plt.imshow(data,origin='lower',cmap='coolwarm',vmax=15,vmin=-15)
plt.colorbar()

# %%
d2=-np.mean(fp['HFX_hmg'][:,:,:],axis=0)#-np.mean(fp['LH_hmg'][:,:,:],axis=0))
d2=meani(d2)
data=np.mean(fp['HFX_60'][:,:,:],axis=0)+d2#+np.mean(fp['LH_60'][:,:,:],axis=0)
plt.imshow(data,origin='lower',cmap='coolwarm',vmax=15,vmin=-15)
plt.colorbar()

# %%
d2=-np.mean(fp['LH_hmg'][:,:,:],axis=0)
d2=meani(d2)
data=d2+np.mean(fp['LH_60'][:,:,:],axis=0)
plt.imshow(data,origin='lower',cmap='coolwarm',vmax=15,vmin=-15)
plt.colorbar()

# %%
EFhmg=np.mean(fp['LH_hmg'][:,:,:],axis=0)/(np.mean(fp['LH_hmg'][:,:,:],axis=0)+np.mean(fp['HFX_hmg'][:,:,:],axis=0))
EFhet=np.mean(fp['LH_60'][:,:,:],axis=0)/(np.mean(fp['LH_60'][:,:,:],axis=0)+np.mean(fp['HFX_60'][:,:,:],axis=0))
EFhmg=meani(EFhmg)
plt.imshow(EFhet-EFhmg,origin='lower',cmap='coolwarm',vmax=.1,vmin=-.1)

# %%
data2=-data[data<0]
plt.hist(data2.flatten(),bins=np.linspace(0,.5,101))

# %%
fphet=nc.Dataset('/home/tsw35/xTyc_shared/compressed_output/20230601_het/cmp_2023-06-01_20:00:00','r')
fphmg=nc.Dataset('/home/tsw35/xTyc_shared/compressed_output/20230601_hmg/cmp_2023-06-01_20:00:00','r')



# %%
fphet=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/20170717/1560_1040_003_169/OUTPUT/wrfout_d01_2017-07-17_20:00:00','r')




# %%
lwp2=np.sum(fphet['QCLOUD'][0,:,:,:]+fphet['QRAIN'][0,:,:,:],axis=0)

# %%
data=lwp2
plt.imshow(data,origin='lower',cmap='turbo',vmax=.00000005)
plt.colorbar()

# %%
np.(data)

# %%
data=np.sum(fphet['CLDFRA'][0,3:-1,:,:],axis=0)
plt.imshow(data,origin='lower',cmap='turbo',vmax=10)
plt.colorbar()

# %%
data=fphet['RAINNC'][0,:]
plt.imshow(data,origin='lower',cmap='turbo',vmax=10)
plt.colorbar()

# %%
print(len(os.listdir('/home/tsw35/tyche/wrf_gaea/')))

# %%
test='/home/tsw35/tyche/wrf_gaea/all/agg_full.nc'
fp=nc.Dataset(test,'r')

# %%

# %%
test='/home/tsw35/tyche/wrf_gaea/20220717_conv.nc'
fp=nc.Dataset(test,'r')
for v in fp.variables:
    if v=='time':
        continue
    plt.figure()
    data=np.mean(fp[v][:,:,:],axis=0)
    plt.imshow(data,origin='lower',cmap='turbo',vmin=np.percentile(data,1),vmax=np.percentile(data,99))
    plt.colorbar()
    plt.title(str(v))

# %%
fp.close()

# %%
