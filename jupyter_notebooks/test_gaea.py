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
mpl.rcParams['figure.dpi'] = 300
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

# %%
data_dir=''
proc_dir='/home/tsw35/tyche/wrf_gaea/'
cum_dir=proc_dir+'all/'

# %%
hmg_dir='/stor/soteria/hydro/shared/WRF_HRRR/20230709_hmg/'
het_dir='/stor/soteria/hydro/shared/WRF_HRRR/20230709_het/'
fphmg=nc.Dataset(hmg_dir+'wrfrst_d01_2023-07-10_18:00:00','r')
fphet=nc.Dataset(het_dir+'wrfrst_d01_2023-07-10_18:00:00','r')

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
a=fphet['LU_INDEX'][0,:,:]!=17

# %%
dd=fphet['RAINNC'][0,:,:][a]

# %%
dd.shape

# %%
fphet2=fphet#nc.Dataset(het_dir+'wrfout_d01_2017-07-18_05:00:00','r')
fphmg2=fphmg#nc.Dataset(hmg_dir+'wrfout_d01_2017-07-18_05:00:00','r')
data=fphet2['RAINNC'][0,:,:]-fphmg2['RAINNC'][0,:,:]
data[fphet2['LU_INDEX'][0,:,:]==17]=float('nan')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.show()

# %%
het=True
het=not het
print(het)

# %%

# %%
zis=700#750
zie=800#1150
zjs=500#650
zje=700#900
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
        fbase='wrfout_d01_2017-07-18_0'+str(tt)+':00:00'
    else:
        fbase='wrfout_d01_2017-07-17_'+str(tt)+':00:00'
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
    
    data=drg[i,:,:]
    ax3.clear()
    #ax1.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax3.imshow(data,origin='lower',cmap='PiYG',vmin=0,vmax=60)
    ax3.axis('off')
    ax3.set_title('Homogenized')
    
    data=drt[i,:,:]
    ax4.clear()
    #ax2.imshow(data,origin='lower',cmap='terrain',vmax=vmax,vmin=0)
    ax4.imshow(data,origin='lower',cmap='PiYG',vmin=0,vmax=60)
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
np.nanmean(drg[-1,:])

# %%
from sklearn.metrics import mean_squared_error

# %%
flist=os.listdir('/home/tsw35/tyche/wrf_hrrr/20170717/radar/')
flist.sort()
precip=np.zeros((48,1039,1559))
t2m=np.zeros((48,1039,1559))
q2m=np.zeros((48,1039,1559))
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
        fbase='wrfout_d01_2017-07-18_0'+str(tt)+':00:00'
    else:
        fbase='wrfout_d01_2017-07-17_'+str(tt)+':00:00'
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
plt.plot([0,20],[0,0],'w-',linewidth=3)
plt.plot(SS_t)
plt.plot(SS_q)
plt.plot(SS_p)
plt.xlim(0,21)
plt.show()

# %%
fp707=nc.Dataset(proc_dir+'20230717_conv.nc','r')

# %%
plt.imshow(fp707['RAINNC_het'][-1,:,:]-fp707['RAINNC_hmg'][-1,:,:],origin='lower',cmap='turbo',vmax=80,vmin=-80)

# %%
print(np.mean(fp707['RAINNC_het'][-1,:,:]))

# %%
fp708.close()

# %%
fmswep=nc.Dataset('/home/tsw35/tyche/wrf_gaea/mswep_gaea/zoomin.nc','r')
fmswep2=nc.Dataset('/home/tsw35/tyche/wrf_gaea/mswep_gaea/zoomin2.nc','r')
fmswep3=nc.Dataset('/home/tsw35/tyche/wrf_gaea/mswep_gaea/zoomin3.nc','r')

# %%

# %%
plt.imshow(np.sqrt(fmswep3['Band1'][:]),origin='lower',cmap='turbo',vmin=0,vmax=3)
plt.colorbar()

# %%
fphrrr=nc.Dataset('/home/tsw35/tyche/wrf_gaea/mswep_gaea/cmp_2023-07-07_12:00:00.nc','r')

# %%
plt.imshow(np.sqrt(fphrrr['RAINNC'][0,:]),origin='lower',cmap='turbo',vmax=3,vmin=0)
plt.colorbar()

# %%
fphrrr['MAPFAC_MX'].description

# %%
hrlt=fphrrr['XLAT'][0,:,:]
mslt=fmswep2['lat'][0,:,:]

# %%
import rasterio

# %%
fp=nc.Dataset('/home/tsw35/tyche/wrf_gaea/mswep_gaea/cmp_2023-07-07_12:00:00.nc','r')


# %%
data=fp['RAINNC'][0,:,:]

# %%
from rasterio.transform import from_origin

# %%
transform=from_origin(-2337000,1557000,3000,3000)

# %%
new_data=rasterio.open('/home/tsw35/tyche/wrf_gaea/mswep_gaea/wrf2.tif',
                       'w',driver='GTiff',height=data.shape[0],width=data.shape[1],
                       count=1,dtype=str(data.dtype),
                       crs='+proj=lcc +a=6370000 +b=6370000 +lat_0=38.5 +lon_0=-97.5 +lat_1=38.5 +lat_2=38.5',
                       transform=transform)

# %%
new_data.write(data,1)
new_data.close()

# %%
fpwrf=nc.Dataset('/home/tsw35/tyche/wrf_gaea/mswep_gaea/wrfP.nc','r')
fpwrf2=nc.Dataset('/home/tsw35/tyche/wrf_gaea/mswep_gaea/wrfH.nc','r')

# %%
data1=fpwrf['Band1'][:]
data2=fmswep['Band1'][:]
hfx=fpwrf2['Band1'][:]

# %%
plt.imshow(data2,origin='lower',cmap='turbo')

# %%
plt.imshow(data1,origin='lower',cmap='turbo')

# %%
plt.imshow(data,origin='lower',cmap='turbo')

# %%
plt.imshow(hfx,cmap='turbo',vmin=-168,vmax=216)

# %%
data3=fp.read(1)

# %%
np.max(data)

# %%
data=fmswep2['Band1'][:]
data.shape

# %%
#fp1=nc.Dataset('/home/tsw35/tyche/wrf_gaea/mswep_gaea/2023152.03.nc','r')
#data=fp1['Band1'][:]
data[data>1]=1
plt.imshow(data,origin='lower',cmap='turbo')

# %%
data.shape

# %%
fp=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/mswep_error.nc','r')

# %%
for var in fp.variables:
    if '2D' in var:
        plt.figure()
        plt.imshow(fp[var][:],origin='lower',cmap='turbo')
        plt.title(var+' '+str(np.nanmean(fp[var][:]))[0:5])
    else:
        plt.figure()
        plt.plot(fp[var][:])
        plt.title(var+' '+str(np.nanmean(fp[var][:]))[0:5])

# %%
fp=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/mswep_error.nc','r')

# %%
for var in fp.variables:
    if '2D' in var:
        plt.figure()
        plt.imshow(fp[var][:],origin='lower',cmap='turbo')
        plt.title(var+' '+str(np.nanmean(fp[var][:]))[0:5])
    else:
        plt.figure()
        plt.plot(fp[var][:])
        plt.title(var+' '+str(np.nanmean(fp[var][:]))[0:5])

# %%
#[fphet2['LU_INDEX'][0,:,:]==17]=float('nan')

#fp=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/mswep_error.nc','r')
for var in fp.variables:
    if '2D' in var:
        plt.figure()
        data=fp[var][:]
        data[fphet['LU_INDEX'][0,:,:]==17]=float('nan')
        plt.imshow(data,origin='lower',cmap='turbo')
        plt.colorbar()
        plt.title(var+' '+str(np.nanmean(fp[var][:]))[0:5])

# %%
var='BIAS2D_het'
plt.figure()
data=fp[var][:]
data[fphet['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo',vmin=-8,vmax=8)
plt.colorbar()
plt.title(var+' '+str(np.nanmean(fp[var][:]))[0:5])

# %%
var='BIAS2D_hmg'
plt.figure()
data=fp[var][:]
data[fphet['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo',vmin=-8,vmax=8)
plt.colorbar()
plt.title(var+' '+str(np.nanmean(fp[var][:]))[0:5])

# %%
var='RMSE2D_het'
plt.figure()
data=fp[var][:]/fp['MSWEP_MEAN2D'][:]
data[fphet['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo',vmin=2,vmax=10)
plt.colorbar()
plt.title(var+' '+str(np.nanmean(data))[0:5])

# %%
var='RMSE2D_hmg'
plt.figure()
data=fp[var][:]/fp['MSWEP_MEAN2D'][:]
data[fphet['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo',vmin=2,vmax=10)
plt.colorbar()
plt.title(var+' '+str(np.nanmean(data))[0:5])

# %%
var='BIAS2D_het'
plt.figure()
data=fp[var][:]-fp['BIAS2D_hmg'][:]
data[fphet['LU_INDEX'][0,:,:]==17]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo',vmin=-2,vmax=2)
plt.colorbar()
plt.title(var+' '+str(np.nanmean(fp[var][:]))[0:5])

# %%
data.shape

# %%
stbolt=5.670*10**(-8)
GSWt=(1-fphet['ALBEDO'][0,:,:])*fphet['SWDOWN'][0,:,:]
LWUPt=stbolt*fphet['TSK'][0,:,:]**4
netLWt=fphet['EMISS'][0,:,:]*(fphet['GLW'][0,:,:]-LWUPt)
RNETt=GSWt+netLWt

GRDt=fphet['HFX'][0,:,:]+fphet['LH'][0,:,:]-fphet['GRDFLX'][0,:,:]

# %%
gdir='/home/tsw35/xTyc_shared/compressed_output/20230710_het/'

albedo=np.zeros((49,1039, 1559))
swdown=np.zeros((49,1039, 1559))
tsk=np.zeros((49,1039, 1559))
emis=np.zeros((49,1039, 1559))
glw=np.zeros((49,1039, 1559))
hfx=np.zeros((49,1039, 1559))
lh=np.zeros((49,1039, 1559))
grdflx=np.zeros((49,1039, 1559))
t=0
flist=os.listdir(gdir)
flist.sort()
for file in flist:
    print('.',flush=True,end='')
    fp=nc.Dataset(gdir+file,'r')
    albedo[t,:,:]=fp['ALBEDO'][0,:,:]
    swdown[t,:,:]=fp['SWDOWN'][0,:,:]
    tsk[t,:,:]=fp['TSK'][0,:,:]
    emis[t,:,:]=fp['EMISS'][0,:,:]
    glw[t,:,:]=fp['GLW'][0,:,:]
    hfx[t,:,:]=fp['HFX'][0,:,:]
    lh[t,:,:]=fp['LH'][0,:,:]
    grdflx[t,:,:]=fp['GRDFLX'][0,:,:]
    t=t+1

# %%
stbolt=5.670*10**(-8)
GSWt=np.mean((1-albedo)*swdown,axis=0)
LWUPt=np.mean(stbolt*tsk**4,axis=0)
netLWt=np.mean(emis,axis=0)*(np.mean(glw,axis=0)-LWUPt)
RNETt=GSWt+netLWt

GRDt=np.mean(hfx+lh-grdflx,axis=0)

# %%
data=np.mean(lh,axis=0)
data[(fp['LU_INDEX'][0,:,:]<17)]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo',vmin=0,vmax=180)
plt.colorbar()
plt.show()

# %%
data=np.mean(hfx,axis=0)
data[(fp['LU_INDEX'][0,:,:]<17)]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo')
plt.colorbar()
plt.show()

# %%
plt.imshow(RNETt-GRDt,origin='lower',cmap='turbo')
plt.colorbar()
plt.show()

# %%
vars=['EF','MsKE','MsKElo','VARHFX','VARLH','LCL','LFC','LOCLOUD','MDCLOUD','HICLOUD','PW','RH2','T2']


# %%
flist=os.listdir('/home/tsw35/tyche/wrf_gaea/all/prerain')
N=len(flist)
data={}
for v in vars:
    data[v]=np.zeros((N,1039, 1559))

# %%

# %%
t=0
for file in flist:
    print('.',end='',flush=True)
    fp=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/prerain/'+file,'r')
    for v in vars:
        if v=='EF':
            d1=fp['gLH_hmg'][:]/(fp['gHFX_hmg'][:]+fp['gLH_hmg'][:])
            d2=fp['gLH_het'][:]/(fp['gHFX_het'][:]+fp['gLH_het'][:])
            data[v][t,:]=d1-d2
        else:
            data[v][t,:]=fp['g'+v+'_hmg'][:]-fp['g'+v+'_het'][:]
    t=t+1

# %%
for v in vars:
    dd=np.nanmean(data[v][msk])
    print(v+': '+str(dd))


# %%
for v in vars:
    plt.figure()
    dd=np.nanmean(data[v],axis=0)
    vmx=np.nanpercentile(np.abs(dd),97.5)
    plt.imshow(dd,origin='lower',cmap='coolwarm',vmin=-vmx,vmax=vmx)
    plt.title(v)
    plt.colorbar()

# %%

# %%
