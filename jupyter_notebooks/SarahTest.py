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
from sklearn.metrics import mean_squared_error
mpl.rcParams['figure.dpi'] = 200
sns.set_theme()
plt.rcParams.update({'figure.max_open_warning': 0})

# %%
wrfdir='/home/tsw35/xTyc_shared/wrfout_sarah/'

# %%
fpn=nc.Dataset(wrfdir+'No_UCM/wrfout_d01_2022-07-19_21:30:00','r')
fp1=nc.Dataset(wrfdir+'UCM = 1/wrfout_d01_2022-07-19_21:30:00','r')
fp3=nc.Dataset(wrfdir+'UCM = 3/wrfout_d01_2022-07-19_21:30:00','r')

# %%
data=fp['TSK'][0,:]

# %%
data=fp['EMISS'][0,:]

# %%
data=fp3['TSK'][0,:]
plt.imshow(data,cmap='coolwarm',origin='lower',vmin=310,vmax=330)
plt.colorbar()
plt.show()

# %%
fpgeo=nc.Dataset('/home/tsw35/xTyc_shared/wrfout_sarah/geo_em.d01.nc')
plt.imshow(fpgeo['EMISS'][0,:,:],origin='lower',cmap='coolwarm')

# %%
print(np.mean(fpn['TSK'][:]))
print(np.mean(fp1['TSK'][:]))
print(np.mean(fp3['TSK'][:]))

# %%
for v in fpgeo.variables:
    if v=='Times':
        continue
    print(str(v)+': '+str(fpgeo[v].description))

# %%
for v in fp.variables:
    try:
        if fp[v][:].shape==(1,111, 129):
            print(str(v).ljust(10)+': '+str(fp[v].description))
    except:
        pass

# %%
