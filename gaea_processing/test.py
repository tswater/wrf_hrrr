import netCDF4 as nc
odir='/home/tsw35/tyche/wrf_gaea/'

try:
    fp=nc.Dataset(odir+'all/agg_full.nc','r+')
except Exception as e:
    print(e)

