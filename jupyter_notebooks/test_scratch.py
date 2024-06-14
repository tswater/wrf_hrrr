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
import wrf
mpl.rcParams['figure.dpi'] = 300
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

# %%
##### SMALL PLOTS #####
##### SMALL PLOTS #####
##### SMALL PLOTS #####

# %%
hmg_dir='/home/tsw35/tyche/wrf_hrrr/sm_hmg/OUTPUT/'
het_dir='/home/tsw35/tyche/wrf_hrrr/sm_het/OUTPUT/'

# %%
# SHOW ALL VARIABLES
fp=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-20_09:00:00','r')
i=0
for v in fp.variables:
    print(str(v).ljust(20),end='')
    i=i+1
    if i>6:
        print()
        i=0

# %%
fphmg['TLP']

# %%
for v in fphmg.variables:
    try:
        fphmg[v].description
    except:
        continue
    if ('SEA' in fphmg[v].description):
        print(str(v)+': '+str(fphmg[v].description))

# %%
# focus vars: PBLH, HFX, LH, TH2, RAINNC, QCLOUD, CLDFRA
# check ACHFX, LU_INDEX, GHT

# %%
fphmg['SWDNTC']

# %%
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-20_08:00:00','r')
fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-20_08:00:00','r')

# %%
alt_hmg=(fphmg['PH'][:] + fphmg['PHB'][:])/9.8
alt_het=(fphet['PH'][:] + fphet['PHB'][:])/9.8

# %%
plt.figure(figsize=(12,4))

# Bring in Data
hmg_hfx=fphmg['HFX'][0,:,:]
het_hfx=fphet['HFX'][0,:,:]

#var='QVAPOR'
#hmg_data=fphmg[var][0,1,:,:]+300
#het_data=fphet[var][0,1,:,:]+300

#var='QCLOUD'
#hmg_data=np.sum(fphmg[var][0,:,:,:],axis=0)
#het_data=np.sum(fphet[var][0,:,:,:],axis=0)

var='RAINNC'
hmg_data=fphmg[var][0,:,:]
het_data=fphet[var][0,:,:]

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
data=het_hfx-hmg_hfx
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-np.max(np.abs(data)),vmax=np.max(np.abs(data)))
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
data=het_data-hmg_data
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-np.max(np.abs(data)),vmax=np.max(np.abs(data)))
plt.axis(False)
plt.colorbar()

print(np.mean(data))

plt.show()

# %%
plt.imshow(fphet['LU_INDEX'][0,:,:],origin='lower',cmap='tab20')
plt.colorbar()
plt.show()

# %%
plt.imshow(fphet['HGT'][0,:,:],origin='lower',cmap='terrain')
plt.colorbar()
plt.show()

# %%
hmg_dir='/home/tsw35/tyche/wrf_hrrr/conus_1764_1008_54_196TSK/OUTPUT/'
het_dir='/home/tsw35/tyche/wrf_hrrr/conus_1764_1008_03_196/OUTPUT/'
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-19_22:00:00','r')
fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-19_22:00:00','r')

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
dhfx=het_hfx-hmg_hfx
print(np.mean(dhfx[fphet['LU_INDEX'][0,:,:]!=17]))
print(np.mean(dhfx))


# %%
def upscale(_data,dx):
    data2=_data.copy()
    for i in range(int(np.floor(_data.shape[0]/dx))):
        for j in range(int(np.floor(_data.shape[1]/dx))):
            data2[i*dx:(i+1)*dx,j*dx:(j+1)*dx]=np.nanmean(_data[i*dx:(i+1)*dx,j*dx:(j+1)*dx])
    return data2


# %%
vmin=-np.nanmax(np.abs(data))
vmax=np.nanmax(np.abs(data))
#plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
data_2=upscale(data,18)
vmin=-np.nanpercentile(np.abs(data_2),99)
vmax=np.nanpercentile(np.abs(data_2),99)

plt.subplot(1,2,2)
im=plt.imshow(data_2,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar(im,fraction=0.026, pad=0.04)
plt.show()
#plt.savefig('PRECIP_DELTA.png')
print(np.mean(data))

# %%
alt_hmg[0,10,500,500]

# %%
plt.imshow(fphet['LU_INDEX'][0,:,:],origin='lower',cmap='tab20')
plt.colorbar()
plt.show()

# %%
rainhet=[]
rainhmg=[]
for t in range(10,24):
    fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')
    fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')
    rainhet.append(fphet['RAINNC'][0,:,:])
    rainhmg.append(fphmg['RAINNC'][0,:,:])


# %%
#fphet2=nc.Dataset(het_dir+'wrfout_d01_2017-07-20_05:00:00','r')
#fphmg2=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-20_05:00:00','r')
#data=fphet2['RAINNC'][0,:,:]-fphmg2['RAINNC'][0,:,:]
#data[fphet2['LU_INDEX'][0,:,:]==17]=float('nan')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.show()

# %%
print(np.mean(data[(data!=0)&(fphet['LU_INDEX'][0,:,:]!=17)]))

# %%
plt.imshow(data[250:350,950:1010],origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.show()

# %%
sgp=data[250:350,950:1010]
np.mean(sgp)

# %%
plt.imshow(data[600:800,750:1000],origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.show()

# %%
plt.subplot(2,1,1)
plt.imshow(rainhet[-1][700:900,750:1000],origin='lower',cmap='terrain',vmin=0,vmax=85)
plt.colorbar()
plt.subplot(2,1,2)
plt.imshow(rainhmg[-1][700:900,750:1000],origin='lower',cmap='terrain',vmin=0,vmax=85)
plt.colorbar()
plt.show()

# %%
plt.imshow(data[700:900,750:1000],origin='lower',cmap='coolwarm')
plt.colorbar()
plt.show()

# %%
plt.subplot(2,1,1)
plt.imshow(het_hfx[700:900,750:1000],origin='lower',cmap='coolwarm',vmin=0,vmax=400)
plt.colorbar()
plt.subplot(2,1,2)
plt.imshow(hmg_hfx[700:900,750:1000],origin='lower',cmap='coolwarm',vmin=0,vmax=400)
plt.colorbar()
plt.show()

# %%
rainhet=[]
rainhmg=[]
hfxhet=[]
hfxhmg=[]
lhxhet=[]
lhxhmg=[]
t2mhet=[]
t2mhmg=[]
q2mhet=[]
q2mhmg=[]
cldhet=[]
cldhmg=[]
for t in range(10,24):
    fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')
    fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')
    msk=fphet['LU_INDEX'][0,:,:]!=17
    rainhet.append(np.mean(fphet['RAINNC'][0,:,:][msk]))
    rainhmg.append(np.mean(fphmg['RAINNC'][0,:,:][msk]))
    hfxhet.append(np.mean(fphet['HFX'][0,:,:][msk]))
    hfxhmg.append(np.mean(fphmg['HFX'][0,:,:][msk]))
    lhxhet.append(np.mean(fphet['LH'][0,:,:][msk]))
    lhxhmg.append(np.mean(fphmg['LH'][0,:,:][msk]))
    t2mhet.append(np.mean(fphet['T2'][0,:,:][msk]))
    t2mhmg.append(np.mean(fphmg['T2'][0,:,:][msk]))
    q2mhet.append(np.mean(fphet['Q2'][0,:,:][msk]))
    q2mhmg.append(np.mean(fphmg['Q2'][0,:,:][msk]))
    cldhet.append(np.mean(np.sum(fphet['CLDFRA'][0,:,:,:],axis=0)[msk]))
    cldhmg.append(np.mean(np.sum(fphmg['CLDFRA'][0,:,:,:],axis=0)[msk]))
for t in range(0,5):
    fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-20_0'+str(t)+':00:00','r')
    fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-20_0'+str(t)+':00:00','r')
    msk=fphet['LU_INDEX'][0,:,:]!=17
    rainhet.append(np.mean(fphet['RAINNC'][0,:,:][msk]))
    rainhmg.append(np.mean(fphmg['RAINNC'][0,:,:][msk]))
    hfxhet.append(np.mean(fphet['HFX'][0,:,:][msk]))
    hfxhmg.append(np.mean(fphmg['HFX'][0,:,:][msk]))
    lhxhet.append(np.mean(fphet['LH'][0,:,:][msk]))
    lhxhmg.append(np.mean(fphmg['LH'][0,:,:][msk]))
    t2mhet.append(np.mean(fphet['T2'][0,:,:][msk]))
    t2mhmg.append(np.mean(fphmg['T2'][0,:,:][msk]))
    q2mhet.append(np.mean(fphet['Q2'][0,:,:][msk]))
    q2mhmg.append(np.mean(fphmg['Q2'][0,:,:][msk]))
    cldhet.append(np.mean(np.sum(fphet['CLDFRA'][0,:,:,:],axis=0)[msk]))
    cldhmg.append(np.mean(np.sum(fphmg['CLDFRA'][0,:,:,:],axis=0)[msk]))


# %%
cldhmg=np.array(cldhmg)
cldhet=np.array(cldhet)
q2mhet=np.array(q2mhet)
q2mhmg=np.array(q2mhmg)
t2mhet=np.array(t2mhet)
t2mhmg=np.array(t2mhmg)
lhxhet=np.array(lhxhet)
lhxhmg=np.array(lhxhmg)
hfxhet=np.array(hfxhet)
hfxhmg=np.array(hfxhmg)
rainhet=np.array(rainhet)
rainhmg=np.array(rainhmg)

# %%
plt.subplot(3,2,3)
plt.plot(rainhmg)
plt.plot(rainhet,'--')
plt.title('PRECIP')
plt.xticks([])

plt.subplot(3,2,1)
plt.plot(hfxhmg)
plt.plot(hfxhet,'--')
plt.title('HFX')
plt.xticks([])

plt.subplot(3,2,2)
plt.plot(lhxhmg)
plt.plot(lhxhet,'--')
plt.title('LH')
plt.xticks([])

plt.subplot(3,2,4)
plt.plot(cldhmg)
plt.plot(cldhet,'--')
plt.title('CLOUD')
plt.xticks([])

plt.subplot(3,2,5)
plt.plot(t2mhmg)
plt.plot(t2mhet,'--')
plt.title('2M TEMP')
plt.xticks([])

plt.subplot(3,2,6)
plt.plot(q2mhmg)
plt.plot(q2mhet,'--')
plt.title('2M Q')
plt.xticks([])

plt.subplots_adjust(wspace=.3,hspace=.2)

plt.show()

# %%
plt.plot((rainhet-rainhmg)/rainhmg*100)
plt.plot((hfxhet-hfxhmg)/hfxhmg*100)
plt.plot((lhxhet-lhxhmg)/lhxhmg*100)
plt.plot((t2mhet-t2mhmg)/t2mhmg*100)
plt.plot((q2mhet-q2mhmg)/q2mhmg*100)
plt.plot((cldhet-cldhmg)/cldhmg*100)
plt.legend(['Precip','HFX','LH','T2','Q2','CLD'])
plt.ylim(-10,10)
plt.show()

# %%

# %%
data5=GRDg-GRDt
data5[~msk]=float('nan')
plt.imshow(data5,vmin=-100,vmax=100,cmap='coolwarm',origin='lower')
plt.colorbar()
plt.show()

# %%
### CHECK Energy Balance 
t=22
stbolt=5.670374419*10**(-8)
fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')
GSWt=(1-fphet['ALBEDO'][0,:,:])*fphet['SWDOWN'][0,:,:]
LWUPt=stbolt*fphet['TSK'][0,:,:]**4
netLWt=fphet['EMISS'][0,:,:]*(fphet['GLW'][0,:,:]-LWUPt)
RNETt=GSWt+netLWt

GRDt=fphet['HFX'][0,:,:]+fphet['LH'][0,:,:]-fphet['GRDFLX'][0,:,:]

GSWg=(1-fphmg['ALBEDO'][0,:,:])*fphmg['SWDOWN'][0,:,:]
LWUPg=stbolt*fphmg['TSK'][0,:,:]**4
netLWg=fphmg['EMISS'][0,:,:]*(fphmg['GLW'][0,:,:]-LWUPg)
RNETg=GSWg+netLWg

GRDg=fphmg['HFX'][0,:,:]+fphmg['LH'][0,:,:]-fphmg['GRDFLX'][0,:,:]

# %%
np.mean(RNETg[msk])-np.mean(RNETt[msk])

# %%
np.mean(GRDg[msk])-np.mean(GRDt[msk])

# %%
plt.hist((RNETt-GRDt)[msk].flatten(),color='blue',bins=np.linspace(-200,200,100))
plt.ylim(0,125000)
plt.title('Energy Balance Histogram HET')
plt.show()

# %%
plt.hist((RNETg-GRDg)[msk].flatten(),color='blue',bins=np.linspace(-200,200,100))
plt.ylim(0,125000)
plt.title('Energy Balance Histogram HMG')
plt.show()

# %%
plt.imshow(fphet['CLDFRA'][0,11,250:300,950:1010],origin='lower',cmap='terrain')
plt.title('3/4km Cloud Cover')
plt.colorbar()
plt.show()

# %%
#[250:350,950:1010]
plt.figure(figsize=(3,8))
t=22
fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')

#t=5
#fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-20_0'+str(t)+':00:00','r')
#fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-20_0'+str(t)+':00:00','r')

plt.subplot(3,1,1)
plt.imshow(fphmg['V'][0,3,260:300,960:1010],origin='lower',cmap='PiYG',vmin=-10,vmax=10)
plt.title('South-North Velocity')
plt.colorbar()
plt.subplot(3,1,2)
plt.title('Surface Temperature')
plt.imshow(fphmg['TSK'][0,260:300,960:1010],origin='lower',cmap='coolwarm',vmin=305,vmax=320)
plt.colorbar()
plt.subplot(3,1,3)
plt.title('Cumulative Rainfall')
d=fphmg['RAINNC'][0,260:300,960:1010]
d[d<=1]=float('nan')
plt.imshow(d,origin='lower',cmap='coolwarm',vmin=0,vmax=45)
plt.colorbar()
plt.subplots_adjust(hspace=.3)
plt.show()

# %%
#[250:350,950:1010]
plt.figure(figsize=(3,8))
t=20
fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')

#t=5
#fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-20_0'+str(t)+':00:00','r')
#fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-20_0'+str(t)+':00:00','r')

plt.subplot(3,1,1)
plt.imshow(fphet['V'][0,3,260:300,960:1010],origin='lower',cmap='PiYG',vmin=-10,vmax=10)
plt.title('East-West Velocity')
plt.colorbar()
plt.subplot(3,1,2)
plt.title('Surface Temperature')
plt.imshow(fphet['TSK'][0,260:300,960:1010],origin='lower',cmap='coolwarm',vmin=305,vmax=320)
plt.colorbar()
plt.subplot(3,1,3)
plt.title('Cumulative Rainfall')
d=fphet['RAINNC'][0,260:300,960:1010]
d[d<=1]=float('nan')
plt.imshow(d,origin='lower',cmap='coolwarm',vmin=0,vmax=7)
plt.colorbar()
plt.subplots_adjust(hspace=.3)
plt.show()

# %%
plt.figure(figsize=(5,5))
t=22
fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-19_'+str(t)+':00:00','r')

#t=5
#fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-20_0'+str(t)+':00:00','r')
#fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-20_0'+str(t)+':00:00','r')

plt.subplot(2,2,1)
plt.imshow(fphmg['V'][0,3,260:300,960:1010],origin='lower',cmap='PiYG',vmin=-10,vmax=10)
plt.title('South-North Velocity')

plt.subplot(2,2,3)
plt.title('Surface Temperature')
plt.imshow(fphmg['TSK'][0,260:300,960:1010],origin='lower',cmap='coolwarm',vmin=305,vmax=320)

plt.subplot(2,2,2)
plt.imshow(fphet['V'][0,3,260:300,960:1010],origin='lower',cmap='PiYG',vmin=-10,vmax=10)
plt.title('South-North Velocity')

plt.subplot(2,2,4)
plt.title('Surface Temperature')
plt.imshow(fphet['TSK'][0,260:300,960:1010],origin='lower',cmap='coolwarm',vmin=305,vmax=320)

plt.show()

# %%

# %%
#[250:350,950:1010]
plt.imshow(fphet['TSK'][0,250:300,950:1010],origin='lower',cmap='coolwarm')
plt.colorbar()
plt.show()

# %%
zh=15
data=np.ones((zh+5,40))*float('nan')
d=fphmg['V'][0,0:zh,265:305,978]
for k in range(zh):
    d[k,:]=d[k,:]-np.mean(d[k,:])
data[5:,:]=d[:,:]
data2=np.ones((zh+5,40))*float('nan')
for i in range(5):
    data2[i,:]=fphmg['TSK'][0,265:305,978]
plt.imshow(data2,origin='lower',cmap='coolwarm')
plt.imshow(data,origin='lower',cmap='terrain')
plt.colorbar(fraction=.025)
plt.plot()
plt.grid(False)
plt.xlabel('SOUTH - NORTH distance')
plt.ylabel('ALTITUDE \n(up to ~3/4km)')
plt.title('Normalized V (terrain colormap)\nSkin Temperature (bottom)')
#plt.colorbar()
plt.show()

# %%
alt=wrf.getvar(fphet,'height_agl',meta=False)[:,250:290,990]

# %%
plt.plot(np.mean(alt[0:13,:],axis=1))
plt.xticks(np.linspace(0,13,27),rotation=45)
plt.show()

# %%
zh=15
data=np.ones((zh+5,40))*float('nan')
d=fphet['W'][0,0:zh,250:290,990]
for k in range(zh):
    d[k,:]=d[k,:]-np.mean(d[k,:])
data[5:,:]=d[:,:]
data2=np.ones((zh+5,40))*float('nan')
for i in range(5):
    data2[i,:]=fphet['TSK'][0,250:290,990]
plt.imshow(data2,origin='lower',cmap='coolwarm')
plt.imshow(data,origin='lower',cmap='terrain')
plt.colorbar(fraction=.025)
plt.plot()
plt.grid(False)
plt.xlabel('SOUTH - NORTH distance')
plt.ylabel('ALTITUDE \n(up to ~3/4km)')
plt.title('Normalized W (terrain colormap)\nSkin Temperature (bottom)')
#plt.colorbar()
plt.show()

# %%
zh=13
data1a=np.ones((zh+5,50))*float('nan')
d=fphet['U'][0,0:zh,270,970:1020]
for k in range(zh):
    d[k,:]=d[k,:]-np.mean(d[k,:])
data1a[5:,:]=d[:,:]

d=fphet['W'][0,0:zh,270,970:1020]
for k in range(zh):
    d[k,:]=d[k,:]-np.mean(d[k,:])
data1b=np.ones((zh+5,50))*float('nan')
data1b[5:,:]=d[:,:]

data2=np.ones((zh+5,50))*float('nan')
for i in range(5):
    data2[i,:]=fphet['TSK'][0,270,970:1020]
plt.imshow(data2,origin='lower',cmap='coolwarm',vmin=303,vmax=313)
plt.colorbar(fraction=0.023)

plt.quiver(data1a,data1b)

#plt.imshow(data,origin='lower',cmap='terrain',vmin=-8,vmax=8)
#plt.plot([0,50],[4.5,4.5],'k-')
#plt.colorbar(fraction=0.023)
#plt.plot()
plt.grid(False,axis='x')
plt.xlabel('WEST - EAST distance (km)',fontsize=14)
plt.ylabel('Altitude (km)',fontsize=14)
#plt.title('Normalized Velocity and \nSurface Temperature (bottom)',fontsize=14)

plt.yticks([4.5,9.75,12.1,15.1,17.25],[0,0.5,1.0,2.0,3.0])
plt.xticks([0,10,20,30,40],[0,30,60,90,120])

#plt.colorbar()
plt.show()

# %%
zh=13
plt.subplot(2,1,1)
data=np.ones((zh+5,50))*float('nan')
d=fphet['U'][0,0:zh,270,970:1020]
for k in range(zh):
    d[k,:]=d[k,:]-np.mean(d[k,:])
data[5:,:]=d[:,:]
data2=np.ones((zh+5,50))*float('nan')
for i in range(5):
    data2[i,:]=fphet['TSK'][0,270,970:1020]
plt.imshow(data2,origin='lower',cmap='coolwarm',vmin=303,vmax=313)
plt.imshow(data,origin='lower',cmap='terrain',vmin=-5,vmax=5)
#plt.plot([0,50],[4.5,4.5],'k-')
plt.colorbar(fraction=0.017,label='u $(m s^{-1})$')
#plt.plot()
plt.grid(False,axis='x')
#plt.xlabel('WEST - EAST distance (km)',fontsize=14)
plt.ylabel('        Altitude (km)',fontsize=14)
#plt.title('Normalized Velocity and \nSurface Temperature (bottom)',fontsize=14)

plt.yticks([4.5,9.75,12.1,15.1,17.25],[0,0.5,1.0,2.0,3.0])
plt.xticks([])


plt.subplot(2,1,2)
data=np.ones((zh+5,50))*float('nan')
d=fphmg['U'][0,0:zh,265,970:1020]
for k in range(zh):
    d[k,:]=d[k,:]-np.mean(d[k,:])
data[5:,:]=d[:,:]
data2=np.ones((zh+5,50))*float('nan')
for i in range(5):
    data2[i,:]=fphmg['TSK'][0,265,970:1020]
plt.imshow(data2,origin='lower',cmap='coolwarm',vmin=303,vmax=313)
plt.colorbar(fraction=0.017,label=r'$T_{skin}$ $(K)$')
plt.imshow(data,origin='lower',cmap='terrain',vmin=-5,vmax=5)
#plt.plot([0,50],[4.5,4.5],'k-')
#plt.colorbar(fraction=0.017,label='u $(m s^{-1})$')
#plt.plot()
plt.grid(False,axis='x')
plt.xlabel('WEST - EAST distance (km)',fontsize=14)
plt.ylabel('        Altitude (km)',fontsize=14)
#plt.title('Normalized Velocity and \nSurface Temperature (bottom)',fontsize=14)

plt.yticks([4.5,9.75,12.1,15.1,17.25],[0,0.5,1.0,2.0,3.0])
plt.xticks([0,10,20,30,40],[0,30,60,90,120])

#plt.colorbar()
plt.show()



# %%
zh=13
data=np.ones((zh+5,50))*float('nan')
yloc=265
d=fphmg['U'][0,0:zh,yloc,970:1020]
for k in range(zh):
    d[k,:]=d[k,:]-np.mean(d[k,:])
data[5:,:]=d[:,:]
data2=np.ones((zh+5,50))*float('nan')
for i in range(5):
    data2[i,:]=fphmg['TSK'][0,yloc,970:1020]
plt.imshow(data2,origin='lower',cmap='coolwarm',vmin=303,vmax=313)
plt.imshow(data,origin='lower',cmap='terrain',vmin=-5,vmax=5)
plt.colorbar()
plt.plot()
plt.grid(False)
plt.xlabel('WEST - EAST distance')
plt.ylabel('ALTITUDE \n(up to ~3/4km)')
plt.title('Normalized U (terrain colormap)\nSensible Heat (bottom)')
#plt.colorbar()
plt.show()

# %%
data.shape

# %%
fphet['TSK']

# %%
fpgeo=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/monsoon_1560_1040_60_169/geo_em.d01.nc','r')

# %%
plt.imshow(fpgeo['LU_INDEX'][0,:,:],cmap='tab20',origin='lower')
plt.show()

# %%
fp.close()

# %%
a=wrf.getvar(fphet,'cloudfrac',meta=False)

# %%
print(a.shape)

# %%
pcftest='/home/tsw35/tyche/wrf_hrrr/conus_1764_1008_54_196TSK/radar_P/2017071901.LDASIN_DOMAIN1'
fp=nc.Dataset(pcftest,'r')

# %%
c0=0
ig=0
jg=0
da=fp['RAINRATE'][0,:,:]>=0
b=fphet['LU_INDEX'][0,:,:]!=17
for i in range(0,150):
    print(str(i)+' ',end='')
    for j in range(0,25):
        a=da[j:j+1007,i:i+1763]
        c=np.sum((a+b)==2)
        if c>c0:
            c0=c
            ig=i
            jg=j
print()
print(ig)
print(jg)

# %%
a=fp['RAINRATE'][0,:,:]>=0
b=fphet['LU_INDEX'][0,:,:]!=17
plt.imshow(a==b,origin='lower')
plt.show()

# %%
from sklearn.metrics import mean_squared_error

# %%
flist=os.listdir('/home/tsw35/tyche/wrf_hrrr/conus_1764_1008_54_196TSK/radar_P/')
flist.sort()
precip=np.zeros((48,1007,1763))
t2m=np.zeros((48,1007,1763))
q2m=np.zeros((48,1007,1763))
t=0
for file in flist:
    if 'LDASIN' not in file:
        continue
    fp=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/conus_1764_1008_54_196TSK/radar_P/'+file,'r')
    precip[t,:,:]=fp['RAINRATE'][0,:,:]
    t2m[t,:,:]=fp['T2D'][0,:,:]
    q2m[t,:,:]=fp['Q2D'][0,:,:]
    t=t+1
    print('.',end='')

# %%
plt.subplot(2,1,1)
dhet=fphet2['RAINNC'][0,:,:]-np.sum(precip[10:29,:,:]*3600,axis=0)
dhmg=fphmg2['RAINNC'][0,:,:]-np.sum(precip[10:29,:,:]*3600,axis=0)
vmax=max(np.percentile(np.abs(dhet),99.9),np.percentile(np.abs(dhmg),99.9))
dhet[~msk]=float('nan')
dhmg[~msk]=float('nan')

plt.imshow(dhet,origin='lower',cmap='coolwarm',vmin=-vmax,vmax=vmax)
plt.colorbar()
plt.title('HETERO')
plt.subplot(2,1,2)
plt.imshow(dhmg,origin='lower',cmap='coolwarm',vmin=-vmax,vmax=vmax)
plt.colorbar()
plt.title('HOMO')
plt.show()

# %%
msk2=(dhet!=0)&(dhmg!=0)
plt.hist(dhet[msk2].flatten(),bins=np.linspace(-10,10,100),alpha=.5)
plt.hist(dhmg[msk2].flatten(),bins=np.linspace(-10,10,100),alpha=.5)
print()
plt.show()

# %%
print(np.nanstd(dhet[msk2]))
print(np.nanstd(dhmg[msk2]))
print(np.nanmean(dhet[msk2]))
print(np.nanmean(dhmg[msk2]))
print(np.nanmean(np.abs(dhet[msk2])))
print(np.nanmean(np.abs(dhmg[msk2])))

# %%
rmse = mean_squared_error(np.sum(precip[10:29,:,:]*3600,axis=0), fphet2['RAINNC'][0,:,:], squared=False)
rmseG = mean_squared_error(np.sum(precip[10:29,:,:]*3600,axis=0), fphmg2['RAINNC'][0,:,:], squared=False)
SS=(rmse-rmseG)/(0-rmseG)*100
print(rmse)
print(rmseG)
print(SS)

# %%
p_het=np.zeros((20,1007,1763))
p_hmg=np.zeros((20,1007,1763))

t_het=np.zeros((20,1007,1763))
t_hmg=np.zeros((20,1007,1763))

q_het=np.zeros((20,1007,1763))
q_hmg=np.zeros((20,1007,1763))

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
    p_het[t,:]=fphet['RAINNC'][0,:,:]
    p_hmg[t,:]=fphmg['RAINNC'][0,:,:]
    
    q_het[t,:]=fphet['Q2'][0,:,:]
    q_hmg[t,:]=fphmg['Q2'][0,:,:]
    
    t_het[t,:]=fphet['T2'][0,:,:]
    t_hmg[t,:]=fphmg['T2'][0,:,:]

# %%
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
    
rmse_p.append(mean_squared_error(np.sum(precip[tt,msk]*3600,axis=0), rhet, squared=False))
rmseG_p.append(mean_squared_error(np.sum(precip[tt,msk]*3600,axis=0), rhmg, squared=False))
SS_p.append((rmse_p[-1]-rmseG_p[-1])/(0-rmseG_p[-1])*100)
    
rmse_t.append(mean_squared_error(t2m[10:30,msk], t_het[0:20,msk], squared=False))
rmseG_t.append(mean_squared_error(t2m[10:30,msk], t_hmg[0:20,msk], squared=False))
SS_t.append((rmse_t[-1]-rmseG_t[-1])/(0-rmseG_t[-1])*100)
    
rmse_q.append(mean_squared_error(q2m[10:30,msk], q_het[0:20,msk], squared=False))
rmseG_q.append(mean_squared_error(q2m[10:30,msk], q_hmg[0:20,msk], squared=False))
SS_q.append((rmse_q[-1]-rmseG_q[-1])/(0-rmseG_q[-1])*100)

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
plt.imshow(t2m[tt,:,:]-t_het[t,:],origin='lower',cmap='terrain')
plt.colorbar()
plt.show()


# %%
(rmse_q[-1]-rmseG_q[-1])/(0-rmseG_q[-1])*100

# %%
vshape=fphet['LU_INDEX'].shape

# %%
vshape[1:]

# %%
a=wrf.getvar(fphet,'tv',meta=False)

# %%
a.shape

# %%
print(np.mean(a[0,:]))
print(np.mean(a[1,:]))
print(np.mean(a[2,:]))
print(np.mean(a[3,:]))

# %%
U=wrf.getvar(fphet,'ua',meta=False)
V=wrf.getvar(fphet,'va',meta=False)

# %%
Uhom=wrf.getvar(fphmg,'ua',meta=False)
Vhom=wrf.getvar(fphmg,'va',meta=False)

# %%
div_hom=np.gradient(Uhom[3,:,:])[1]/3+np.gradient(Vhom[3,:,:])[0]/3

# %%
div=np.gradient(U[3,:,:])[1]/3+np.gradient(V[3,:,:])[0]/3

# %%
H=fphet['HFX'][0,:,:]
gradH=np.gradient(fphet['HFX'][0,:,:])
divh=np.abs(gradH[0]/3)+np.abs(gradH[1]/3)

# %%
plt.hist(divh.flatten(),bins=100)
plt.show()
print(np.std(divh))

# %%
plt.imshow(div,origin='lower',cmap='coolwarm',vmin=-2,vmax=2)
plt.show()

# %%
plt.imshow(div_hom,origin='lower',cmap='coolwarm',vmin=-2,vmax=2)
plt.show()

# %%
cape2d=wrf.getvar(fphet,'cape_2d',meta=False)
cape=cape2d[0,:]

# %%
plt.imshow(cape,origin='lower',cmap='terrain')
plt.show()

# %%
plt.imshow(fDstd,origin='lower',cmap='terrain',vmin=0,vmax=1.5)
plt.show()

# %%
plt.imshow(fHstd,origin='lower',cmap='terrain',vmin=0,vmax=200)
plt.show()

# %%
from scipy import stats
import scipy as sci

# %%
import scipy as sci
Hp=H-sci.ndimage.filters.gaussian_filter(H,sigma=5,mode='reflect')


# %%
def spatialSTD(_data,dx):
    data2=_data.copy()
    for i in range(int(np.floor(_data.shape[0]/dx))):
        for j in range(int(np.floor(_data.shape[1]/dx))):
            data2[i*dx:(i+1)*dx,j*dx:(j+1)*dx]=np.nanstd(_data[i*dx:(i+1)*dx,j*dx:(j+1)*dx])
    return data2


# %%
def fspatialSTD(_data,dx):
    data2=np.zeros((_data.shape))
    dx2=int(np.floor(dx/2))
    for i in range(dx2+1,_data.shape[0]-(dx2+1)):
        for j in range(dx2+1,_data.shape[1]-(dx2+1)):
            data2[i,j]=np.nanstd(_data[i-dx2:i+dx2,j-dx2:j+dx2])
    return data2


# %%
def spatialPR(_data,_data2,dx):
    data2=_data.copy()
    for i in range(int(np.floor(_data.shape[0]/dx))):
        for j in range(int(np.floor(_data.shape[1]/dx))):
            data2[i*dx:(i+1)*dx,j*dx:(j+1)*dx]=stats.pearsonr(_data[i*dx:(i+1)*dx,j*dx:(j+1)*dx].flatten(),_data2[i*dx:(i+1)*dx,j*dx:(j+1)*dx].flatten())[0]
    return data2


# %%
Hstd=spatialSTD(H,10)

# %%
fHstd=fspatialSTD(H,10)

# %%
fDstd=fspatialSTD(div,10)

# %%
fHstd2=fHstd.copy()
fHstd2[fHstd2<5]=float('nan')

# %%
corr=spatialPR(fHstd,fDstd,100)
corr[fHstd<5]=float('nan')

# %%
plt.imshow(corr,origin='lower',cmap='terrain',vmin=0,vmax=1)
plt.colorbar()
plt.show()

# %%
fp2=
