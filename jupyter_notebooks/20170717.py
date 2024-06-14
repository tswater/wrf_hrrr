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
hmg_dir='/home/tsw35/tyche/wrf_hrrr/20170717/1560_1040_060_169/OUTPUT/'
het_dir='/home/tsw35/tyche/wrf_hrrr/20170717/1560_1040_003_169/OUTPUT/'
fphmg=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-17_20:00:00','r')
fphet=nc.Dataset(het_dir+'wrfout_d01_2017-07-17_20:00:00','r')

# %%
for v in fphet.variables:
    try:
        d=fphet[v].description
    except:
        continue
    if "RH" in d:
        print(v)
        #print(fphet[v].description)

# %%
fphet['GLW'].description

# %%
for i in range(24):


# %%
stbolt=5.670*10**(-8)
GSWt=(1-fphet['ALBEDO'][0,:,:])*fphet['SWDOWN'][0,:,:]
LWUPt=stbolt*fphet['TSK'][0,:,:]**4
netLWt=fphet['EMISS'][0,:,:]*(fphet['GLW'][0,:,:]-LWUPt)
RNETt=GSWt+netLWt

GRDt=fphet['HFX'][0,:,:]+fphet['LH'][0,:,:]-fphet['GRDFLX'][0,:,:]

# %%
plt.imshow(fphet['GLW'][0,:,:],origin='lower',cmap='turbo')
plt.colorbar()
plt.show()

# %%
import numpy as np

# %%
a=np.linspace(0,48,49)
len(a[24:])

# %%
fig=plt.figure(figsize=(12,4))

# Bring in Data
hmg_hfx=fphmg['HFX'][0,:,:]
het_hfx=fphet['HFX'][0,:,:]

#var='CLDFRA'
#hmg_data=fphmg[var][0,12,:,:]
#het_data=fphet[var][0,12,:,:]

var='CLDFRA'
hmg_data=np.sum(fphmg[var][0,:,:,:],axis=0)
het_data=np.sum(fphet[var][0,:,:,:],axis=0)

#var='RAINNC'
#hmg_data=fphmg[var][0,:,:]
#het_data=fphet[var][0,:,:]

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
fphet2=nc.Dataset(het_dir+'wrfout_d01_2017-07-18_05:00:00','r')
fphmg2=nc.Dataset(hmg_dir+'wrfout_d01_2017-07-18_05:00:00','r')
data=fphet2['RAINNC'][0,:,:]-fphmg2['RAINNC'][0,:,:]
data[fphet2['LU_INDEX'][0,:,:]==17]=float('nan')
vmin=-np.nanpercentile(np.abs(data),99.8)
vmax=np.nanpercentile(np.abs(data),99.8)
plt.imshow(data,origin='lower',cmap='coolwarm',vmin=-45,vmax=45)
plt.colorbar()
plt.show()

# %%

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
plt.plot([0,21],[0,0],'w-',linewidth=3)
plt.plot(SS_t)
plt.plot(SS_q)
plt.plot(SS_p)
plt.xlim(0,21)
plt.show()

# %%
