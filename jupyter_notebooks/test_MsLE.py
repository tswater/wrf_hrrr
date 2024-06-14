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
from matplotlib.lines import Line2D
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.animation import FuncAnimation
import matplotlib
import scipy as sci
from IPython.display import HTML
import wrf
from sklearn.metrics import mean_squared_error
from matplotlib.gridspec import GridSpec
mpl.rcParams['figure.dpi'] = 100
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

# %%
dir_het='/home/tsw35/tyche/wrf_hrrr/compressed/het/'
dir_hmg='/home/tsw35/tyche/wrf_hrrr/compressed/hmg060/'


# %%
def ms_flx(w,s,conv,df=20):
    nx=int(w.shape[0]/df+1)
    ny=int(w.shape[1]/df+1)
    dout=np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            w_=w[i*df:(i+1)*df,j*df:(j+1)*df]
            s_=s[i*df:(i+1)*df,j*df:(j+1)*df]
            wbar=np.nanmean(w_)
            sbar=np.nanmean(s_)
            try:
                conv_=np.nanmean(conv[i*df:(i+1)*df,j*df:(j+1)*df])
            except Exception as e:
                conv_=conv
            
            dout[i,j] = np.nanmean(conv_*np.nanmean((w_-wbar)*(s_-sbar)))
            # np.nanmean(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout


# %%
def databig(data):
    dout=np.zeros((1039,1559))
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            dout[i*20:(i+1)*20,j*20:(j+1)*20]=data[i,j]
    return dout


# %%
fpst=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/201707_long/het/OUTPUT/static_data.nc','r')
msk=fpst['LU_INDEX'][0,:,:]==17
fpst.close()

# %%
cp=1005
Lv=2260000 

# %%
fpt=nc.Dataset(dir_het+'wrfout_d01_2023-07-08_18:00:00','r')
fpg=nc.Dataset(dir_hmg+'wrfout_d01_2023-07-08_18:00:00','r')

# %%
fpt['PBLH']

# %%
plt.imshow(fpg['PBLH'][0,:]-fpt['PBLH'][0,:],cmap='coolwarm')
plt.colorbar()

# %%
T_g=wrf.getvar(fpg,'tk',meta=False)
T_t=wrf.getvar(fpt,'tk',meta=False)
RH_g=wrf.getvar(fpg,'rh',meta=False)
RH_t=wrf.getvar(fpt,'rh',meta=False)

# %%
T2_g=wrf.getvar(fpg,'T2',meta=False)
T2_t=wrf.getvar(fpt,'T2',meta=False)
RH2_g=wrf.getvar(fpg,'rh2',meta=False)
RH2_t=wrf.getvar(fpt,'rh2',meta=False)

# %%
plt.figure(dpi=300)
data=T_g[0,:,:]-T_t[0,:,:]
data[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-4,vmax=4)

# %%
plt.figure(dpi=300)
data=T2_g[:,:]-T2_t[:,:]
#data[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-4,vmax=4)

# %%
plt.figure(dpi=300)
data=fpg['QVAPOR'][0,2,:,:]-fpt['QVAPOR'][0,2,:,:]
data[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo')
plt.colorbar()

# %%
plt.figure(dpi=300)
data=RH2_g[:,:]-RH2_t[:,:]
data[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-10,vmax=10)

# %%
w_g=wrf.getvar(fpg,'wa',meta=False)
p_g=wrf.getvar(fpg,'pres',meta=False)
qv_g=fpg['QVAPOR'][0,:,:,:]
theta_g=wrf.getvar(fpg,'th',meta=False)
T_g=wrf.getvar(fpg,'tk',meta=False)
rho_g=p_g/(287*(1+(.608*qv_g))*T_g)

# %%
w_t=wrf.getvar(fpt,'wa',meta=False)
p_t=wrf.getvar(fpt,'pres',meta=False)
qv_t=fpt['QVAPOR'][0,:,:,:]
theta_t=wrf.getvar(fpt,'th',meta=False)
T_t=wrf.getvar(fpt,'tk',meta=False)
rho_t=p_t/(287*(1+(.608*qv_t))*T_t)

# %%
ms_lht_1=ms_flx(w_t[1,:,:],qv_t[1,:,:],rho_t[1,:,:]*Lv)
ms_lht_5=ms_flx(w_t[5,:,:],qv_t[5,:,:],rho_t[5,:,:]*Lv)
ms_lht_10=ms_flx(w_t[10,:,:],qv_t[10,:,:],rho_t[10,:,:]*Lv)
print('.')

ms_lhg_1=ms_flx(w_g[1,:,:],qv_g[1,:,:],rho_g[1,:,:]*Lv)
ms_lhg_5=ms_flx(w_g[5,:,:],qv_g[5,:,:],rho_g[5,:,:]*Lv)
ms_lhg_10=ms_flx(w_g[10,:,:],qv_g[10,:,:],rho_g[10,:,:]*Lv)
print('.')

ms_sht_1=ms_flx(w_t[1,:,:],theta_t[1,:,:],rho_t[1,:,:]*cp)
ms_sht_5=ms_flx(w_t[5,:,:],theta_t[5,:,:],rho_t[5,:,:]*cp)
ms_sht_10=ms_flx(w_t[10,:,:],theta_t[10,:,:],rho_t[10,:,:]*cp)
print('.')

ms_shg_1=ms_flx(w_g[1,:,:],theta_g[1,:,:],rho_g[1,:,:]*cp)
ms_shg_5=ms_flx(w_g[5,:,:],theta_g[5,:,:],rho_g[5,:,:]*cp)
ms_shg_10=ms_flx(w_g[10,:,:],theta_g[10,:,:],rho_g[10,:,:]*cp)

# %%
w_g.shape

# %%
ms_shg_1.shape

# %%
prof_lh_t=np.zeros((50,52,78))
prof_lh_g=np.zeros((50,52,78))
prof_sh_t=np.zeros((50,52,78))
prof_sh_g=np.zeros((50,52,78))

# %%
for i in range(50):
    prof_lh_t[i,:,:]=ms_flx(w_t[i,:,:],qv_t[i,:,:],rho_t[i,:,:]*Lv)
    prof_lh_g[i,:,:]=ms_flx(w_g[i,:,:],qv_g[i,:,:],rho_g[i,:,:]*Lv)
    prof_sh_t[i,:,:]=ms_flx(w_t[i,:,:],theta_t[i,:,:],rho_t[i,:,:]*cp)
    prof_sh_g[i,:,:]=ms_flx(w_g[i,:,:],theta_g[i,:,:],rho_g[i,:,:]*cp)
    print('.',end='',flush=True)

# %%
zt=wrf.getvar(fpt,'z',meta=False,msl=False)
zg=wrf.getvar(fpg,'z',meta=False,msl=False)

# %%
plt.imshow(zt[10,:,:],origin='lower',cmap='turbo')
plt.colorbar()

# %%

# %%
datat=databig(ms_sht_10)
datat[msk]=float('nan')
plt.imshow(datat,origin='lower',cmap='coolwarm',vmin=-300,vmax=300)
plt.colorbar()

# %%
datag=databig(ms_shg_10)
datag[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-300,vmax=300)
plt.colorbar()

# %%
plt.imshow(datag-datat,origin='lower',cmap='coolwarm',vmin=-100,vmax=100)
plt.colorbar()

# %%
np.nanmean(datag-datat)

# %%

# %%
mp_lht=np.nanmean(prof_lh_t,axis=(1,2))
mp_lhg=np.nanmean(prof_lh_g,axis=(1,2))
mp_sht=np.nanmean(prof_sh_t,axis=(1,2))
mp_shg=np.nanmean(prof_sh_g,axis=(1,2))

# %%
zt_1=np.nanmean(zt,axis=(1,2))
zg_1=np.nanmean(zg,axis=(1,2))

# %%
zt_1=np.nanmean(zt,axis=(1,2))
zg_1=np.nanmean(zg,axis=(1,2))
plt.plot(mp_lht,zt_1)
plt.plot(mp_lhg,zg_1)

# %%
plt.plot(mp_sht,zt_1)
plt.plot(mp_shg,zg_1)

# %%
prof_lh_t.shape

# %%
w_t.shape

# %%
52*78*50

# %%
1039*1559/(52*78*50)

# %%
1039/20

# %%
fp=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/agg_full.nc','r')

# %%
fp

# %%
mp_lht=np.nanmean(fp['MsLH_het'][:],axis=(0,2,3))
mp_lhg=np.nanmean(fp['MsLH_hmg'][:],axis=(0,2,3))
mp_sht=np.nanmean(fp['MsHFX_het'][:],axis=(0,2,3))
mp_shg=np.nanmean(fp['MsHFX_hmg'][:],axis=(0,2,3))

# %%
zt_1=np.nanmean(fp['Z_het'][:],axis=(0,2,3))
zg_1=np.nanmean(fp['Z_hmg'][:],axis=(0,2,3))

# %%
plt.plot(mp_lht,zt_1,'--',color='forestgreen')
plt.plot(mp_lhg,zg_1,'-',color='forestgreen')
plt.plot(mp_sht,zt_1,'--',color='firebrick')
plt.plot(mp_shg,zg_1,'-',color='firebrick')

# %%
print(zt_1[0:5])

# %%
zt_2=np.nanmean(fp['Z_het'][:,4,:,:],axis=(0))
zg_2=np.nanmean(fp['Z_hmg'][:,4,:,:],axis=(0))

# %%
plt.imshow(zt_2,origin='lower',cmap='turbo')
plt.colorbar()

# %%
plt.plot(mp_lht,'--')
plt.plot(mp_lhg,'-')
plt.plot(mp_sht,'--')
plt.plot(mp_shg,'-') 

# %%
lht=np.nanmean(fp['MsLH_het'][:,7,:,:],axis=0)
lhg=np.nanmean(fp['MsLH_hmg'][:,7,:,:],axis=0)
sht=np.nanmean(fp['MsHFX_het'][:,7,:,:],axis=0)
shg=np.nanmean(fp['MsHFX_hmg'][:,7,:,:],axis=0)

# %%
lht=databig(lht)
lht[msk]=float('nan')

lhg=databig(lhg)
lhg[msk]=float('nan')

sht=databig(sht)
sht[msk]=float('nan')

shg=databig(shg)
shg[msk]=float('nan')

# %%
plt.figure(dpi=200)
plt.imshow(lhg-lht,cmap='coolwarm',origin='lower',vmin=-60,vmax=60)
plt.colorbar()

# %%
plt.figure(dpi=200)
plt.imshow(shg-sht,cmap='coolwarm',origin='lower',vmin=-10,vmax=10)
plt.colorbar()

# %%
len('......................')

# %%
22+60-38

# %%
12*5

# %%
20*30

# %%
150*3/60

# %%
fp=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/diurnal.nc','r')

# %%
vars=list(fp.variables.keys())
vars.sort()
vars

# %%
fp.close()

# %%
plt.figure()
plt.plot(fp['HFX_het'][:])
plt.plot(fp['LH_het'][:])
plt.plot(-fp['GRDFLX_het'][:])
plt.plot(fp['LW_DOWN_het'][:])
plt.plot(-fp['LW_UP_het'][:])
plt.plot(fp['SW_NET_het'][:])
plt.legend(['HFX','LH','GFX','LW_dwn','LW_up','SW_net'])

plt.figure()
plt.plot(fp['HFX_hmg'][:])
plt.plot(fp['LH_hmg'][:])
plt.plot(-fp['GRDFLX_hmg'][:])
plt.plot(fp['LW_DOWN_hmg'][:])
plt.plot(-fp['LW_UP_hmg'][:])
plt.plot(fp['SW_NET_hmg'][:])
plt.legend(['HFX','LH','GFX','LW_dwn','LW_up','SW_net'])

plt.figure()
plt.plot(fp['HFX_hmg'][:]-fp['HFX_het'][:])
plt.plot(fp['LH_hmg'][:]-fp['LH_het'][:])
plt.plot(-fp['GRDFLX_hmg'][:]+fp['GRDFLX_het'][:])
plt.plot(fp['LW_DOWN_hmg'][:]-fp['LW_DOWN_het'][:])
plt.plot(-fp['LW_UP_hmg'][:]+fp['LW_UP_het'][:])
plt.plot(fp['SW_NET_hmg'][:]-fp['SW_NET_het'][:])
plt.legend(['HFX','LH','GFX','LW_dwn','LW_up','SW_net'])

# %%
plt.figure()
plt.plot(fp['HFX_hmg'][:]-fp['HFX_het'][:])
plt.plot(fp['LH_hmg'][:]-fp['LH_het'][:])
plt.plot(-fp['GRDFLX_hmg'][:]+fp['GRDFLX_het'][:])
plt.plot(fp['LW_DOWN_hmg'][:]-fp['LW_DOWN_het'][:]-fp['LW_UP_hmg'][:]+fp['LW_UP_het'][:])
plt.plot(fp['SW_NET_hmg'][:]-fp['SW_NET_het'][:])
plt.legend(['HFX','LH','GFX','LW_net','SW_net'])

# %%
fp['LW_DOWN_het'].dimensions

# %%
Rnet=fp['LW_DOWN_het'][:]-fp['LW_UP_het'][:]+fp['SW_NET_het'][:]

# %%
plt.plot(Rnet+fp['GRDFLX_het'][:]-fp['HFX_het'][:]-fp['LH_het'][:])

# %%

# %%
np.mean(Rnet+fp['GRDFLX_het'][:]-fp['HFX_het'][:]-fp['LH_het'][:])

# %%
Rnet=fp['LW_DOWN_hmg'][:]-fp['LW_UP_hmg'][:]+fp['SW_NET_hmg'][:]

# %%
np.mean(Rnet+fp['GRDFLX_hmg'][:]-fp['HFX_hmg'][:]-fp['LH_hmg'][:])

# %%
plt.plot(Rnet+fp['GRDFLX_hmg'][:]-fp['HFX_hmg'][:]-fp['LH_hmg'][:])


# %%
def databig(data):
    dout=np.zeros((1039,1559))
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            dout[i*20:(i+1)*20,j*20:(j+1)*20]=data[i,j]
    return dout


# %%
fp2d=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/agg_2d.nc','r')
fpst=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/201707_long/het/OUTPUT/static_data.nc','r')
msk=fpst['LU_INDEX'][0,:,:]==17

# %%
plt.figure(dpi=300)
data1=fp2d['HFX_hmg'][:]-fp2d['HFX_het'][:]#-databig(fp2d['HFX_60'][:])
#data=sci.ndimage.filters.gaussian_filter(data,sigma=5,mode='reflect')
data1[msk]=float('nan')
plt.imshow(data1,origin='lower',cmap='coolwarm',vmin=-40,vmax=40)
plt.colorbar()
print(np.nanmean(data1))

# %%
plt.figure(dpi=300)
data2=fp2d['LH_hmg'][:]-fp2d['LH_het'][:]#-databig(fp2d['LH_60'][:])
#data=sci.ndimage.filters.gaussian_filter(data,sigma=5,mode='reflect')
data2[msk]=float('nan')
plt.imshow(data2,origin='lower',cmap='coolwarm',vmin=-60,vmax=60)
plt.colorbar()

# %%
plt.figure(dpi=300)
efhet=(fp2d['LH_het'][:])/(fp2d['LH_het'][:]+fp2d['HFX_het'][:])
efhmg=(fp2d['LH_hmg'][:])/(fp2d['LH_hmg'][:]+fp2d['HFX_hmg'][:])
data=efhmg-efhet
data[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='BrBG',vmin=-.3,vmax=.3)


# %%
plt.figure(dpi=300)
data1=fp2d['T2_hmg'][:]-fp2d['T2_het'][:]#-databig(fp2d['HFX_60'][:])
#data1=sci.ndimage.filters.gaussian_filter(data1,sigma=5,mode='reflect')
data1[~msk]=float('nan')
plt.imshow(data1,origin='lower',cmap='coolwarm',vmin=-4,vmax=4)
plt.colorbar()
print(np.nanmean(data1))

# %%
plt.figure(dpi=300)
data1=fp2d['RH2_hmg'][:]-fp2d['RH2_het'][:]#-databig(fp2d['HFX_60'][:])
data1=sci.ndimage.filters.gaussian_filter(data1,sigma=5,mode='reflect')
data1[~msk]=float('nan')
plt.imshow(data1,origin='lower',cmap='coolwarm',vmin=-4,vmax=4)
plt.colorbar()
print(np.nanmean(data1))

# %%
plt.figure(dpi=300)
data1=fp2d['T2_het'][:]#-databig(fp2d['HFX_60'][:])
#data1=sci.ndimage.filters.gaussian_filter(data1,sigma=5,mode='reflect')
#data1[msk]=float('nan')
plt.imshow(data1,origin='lower',cmap='turbo',vmin=280,vmax=310)
plt.colorbar()
print(np.nanmean(data1))

# %%
plt.figure(dpi=300)
data1=fp2d['T2_hmg'][:]#-databig(fp2d['HFX_60'][:])
#data1=sci.ndimage.filters.gaussian_filter(data1,sigma=5,mode='reflect')
#data1[msk]=float('nan')
plt.imshow(data1,origin='lower',cmap='turbo',vmin=280,vmax=310)
plt.colorbar()
print(np.nanmean(data1))

# %%
fp['RH']

# %%
fpst=nc.Dataset('/home/tsw35/tyche/wrf_hrrr/201707_long/het/OUTPUT/static_data.nc','r')
msk=fpst['LU_INDEX'][0,:,:]==17
fpagg=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/agg_full.nc','r')

# %%
t0_t=np.nanmean(fpagg['T0_het'][:],axis=0)
t0_g=np.nanmean(fpagg['T0_hmg'][:],axis=0)
q0_t=np.nanmean(fpagg['Q0_het'][:],axis=0)
q0_g=np.nanmean(fpagg['Q0_hmg'][:],axis=0)
pblh_t=np.nanmean(fpagg['PBLH_het'][:],axis=0)
pblh_g=np.nanmean(fpagg['PBLH_hmg'][:],axis=0)

# %%
plt.figure(dpi=300)
data=t0_g-t0_t
data[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-4,vmax=4)

# %%
plt.figure(dpi=300)
data=q0_g-q0_t
data[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-.002,vmax=.002)

# %%
plt.figure(dpi=300)
data=q0_t
data[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='turbo')
plt.colorbar()

# %%
plt.figure(dpi=200)
data=pblh_g-pblh_t
data[msk]=float('nan')
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-150,vmax=150)

# %%
fp2d=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/agg_2d.nc','r')
fpagg=nc.Dataset('/home/tsw35/tyche/wrf_gaea/all/agg_full.nc','r')

# %%
list(fp2d.variables)


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
netrad=fp2d['LWN_hmg'][:]+fp2d['SWN_hmg'][:]#-fp2d['GLW_het'][:]
eb_het=netrad-(fp2d['LH_het'][:]+fp2d['HFX_het'][:]-fp2d['GFX_hmg'][:])
eb_het[msk]=float('nan')

# %%
eb2=meani(eb_het)

# %%
eb_het[msk]=float('nan')
plt.figure(dpi=400)
plt.imshow(eb2,origin='lower',cmap='coolwarm',vmin=-10,vmax=10)
plt.colorbar()

# %%

plt.figure(dpi=400)
plt.imshow(fp2d['GLW_hmg'][:],origin='lower',cmap='terrain')
plt.colorbar()

# %%
d=28
netrad=fpagg['LWN_hmg'][d,:]+fpagg['SWN_hmg'][d,:]#-fp2d['GLW_het'][:]
eb_het=netrad-(fpagg['LH_het'][d,:]+fpagg['HFX_het'][d,:]-fpagg['GFX_hmg'][d,:])

# %%

# %%
eb_het[msk]=float('nan')
plt.figure(dpi=400)
plt.imshow(eb_het,origin='lower',cmap='coolwarm',vmin=-10,vmax=10)
plt.colorbar()

# %%
np.nanmean(netrad)

# %%
fp=nc.Dataset('/home/tsw35/tyche/wrf_gaea/20220805_conv.nc')

# %%
fp['LWN_het'][:].shape

# %%
gaea_dir='/home/tsw35/xTyc_shared/full_compress/'
day='20230706'
hrs=['cmp_2023-07-07_17:00:00']
N=1
sn=1039
we=1559
stbolt=5.67037*10**(-8)

het_gfx=np.zeros((N,sn,we))
hmg_gfx=np.zeros((N,sn,we))

het_netsw=np.zeros((N,sn,we))
hmg_netsw=np.zeros((N,sn,we))

het_netlw=np.zeros((N,sn,we))
hmg_netlw=np.zeros((N,sn,we))

het_glw=np.zeros((N,sn,we))
hmg_glw=np.zeros((N,sn,we))

i=0
for hr in hrs:
    print(hr,flush=True)
    fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
    fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')

    emissg=fphmg['EMISS'][0,:]
    emisst=fphet['EMISS'][0,:]

    hmg_netlw[i,:]=emissg*(fphmg['GLW'][0,:]-stbolt*fphmg['TSK'][0,:][:]**4)
    hmg_netsw[i,:]=(1-fphmg['ALBEDO'][0,:])*fphmg['SWDOWN'][0,:]
    hmg_gfx[i,:]=fphmg['GRDFLX'][0,:]
    hmg_glw[i,:]=fphmg['GLW'][0,:]*emissg

    hmg_netlw[i,:]=emisst*(fphet['GLW'][0,:]-stbolt*fphet['TSK'][0,:][:]**4)
    hmg_netsw[i,:]=(1-fphet['ALBEDO'][0,:])*fphet['SWDOWN'][0,:]
    hmg_gfx[i,:]=fphet['GRDFLX'][0,:]
    hmg_glw[i,:]=fphet['GLW'][0,:]*emisst

    #### FLUXES ####
    fphet.close()
    fphmg.close()
    i=i+1


# %%
t=10
netrad=fp['LWN_hmg'][t,:]+fp['SWN_hmg'][t,:]#-fp2d['GLW_het'][:]
eb_het=netrad-(fp['LH_het'][t,:]+fp['HFX_het'][t,:]-fp['GFX_hmg'][t,:])

# %%
eb_het[msk]=float('nan')
plt.figure(dpi=400)
plt.imshow(eb_het,origin='lower',cmap='coolwarm',vmin=-20,vmax=20)
plt.colorbar()

# %%
data=fp['LWP_het'][t,:]
data[msk]=float('nan')
plt.figure(dpi=400)
plt.imshow(data,cmap='turbo',origin='lower',vmax=1,vmin=.1)

# %%
data=netrad
data[msk]=float('nan')
plt.figure(dpi=400)
plt.imshow(data,cmap='turbo',origin='lower',vmin=-150,vmax=900)
plt.colorbar()

# %%
data=(fp['LH_het'][t,:]+fp['HFX_het'][t,:]-fp['GFX_hmg'][t,:])
data[msk]=float('nan')
plt.figure(dpi=400)
plt.imshow(data,cmap='turbo',origin='lower',vmin=-150,vmax=900)
plt.colorbar()

# %%
