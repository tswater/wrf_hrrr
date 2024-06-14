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
import netCDF4 as nc
import numpy as np
import pygrib
import matplotlib.pyplot as plt
#PRECIP= 628

# %%
hdir='/home/tsw35/tyche/data/HRRR/'

# %%
grbs=pygrib.open(hdir+'hrrr2.20170718.t00z.grib2')

# %%
grbs.seek(600)
grbs.read(80)

# %%
grb = grbs.select(name='Total Precipitation')[0]
prc = grb.values

# %%
pc2=grbs.select(name='Precipitation rate')[0].values

# %%

# %%
pc2.shape

# %%
1007*1763

# %%
52/2

# %%
prc[26:-26,:].shape

# %%
np.max(pc2)

# %%
wdir='/home/tsw35/tyche/workspace/'
fpp=pygrib.open(wdir+'hrrr.t00z.wrfprsf01.grib2')
fpn=pygrib.open(wdir+'hrrr.t00z.wrfnatf00.grib2')

# %%
plt.imshow(fpp.select(name='Total Precipitation')[0].values,origin='lower',cmap='terrain')
plt.colorbar()
plt.show()

# %%
