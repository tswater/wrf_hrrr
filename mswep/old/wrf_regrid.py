# Parallel script for regridding the forcing data to desired inpu
# OVERVIEW:
import sys
from mpi4py import MPI
import netCDF4 as nc
import ast
import numpy as np
import os
import rasterio
import subprocess
import datetime

# MPI4PY Stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# -------------- #
# LOAD ARGUMENTS #
# -------------- #
# load in the arguments from wrf_preprocessing.py 
x=1559
y=1039

argv = sys.argv[1:]
w_input = '/stor/soteria/hydro/shared/data/PCF/1hr/daily/'
w_dir = 'wdir/'
forcing_dir = ''
run_dir = ''
geogrid = '../geo_em.d01.nc'
gdal_cmd = ''
filelist =['20170716.nc','20170717.nc','20170718.nc']
src_proj = "'+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'"

proj="'+proj=lcc +a=6370000 +b=6370000 +lat_0=38.5 +lon_0=-97.5 +lat_1=38.5 +lat_2=38.5'"

# --------------------- #
# INITIAL SETUP STUFFS  #
# --------------------- #

# pull info from geogrid
fp_geo = nc.Dataset(geogrid,'r')
corner_lats = fp_geo.corner_lats[0:4]
corner_lons = fp_geo.corner_lons[0:4]
dx = fp_geo.DX
dy = fp_geo.DY

# Set up approximate extent map
fp_1=nc.Dataset(w_input+filelist[0],'r')
lats = fp_1['lat'][:]
lons = fp_1['lon'][:]
dlat = lats[1]-lats[0]
dlon = lons[1]-lons[0]
min_lon = np.min(corner_lons)-2*dlon
min_lat = np.min(corner_lats)-2*dlat
max_lon = np.max(corner_lons)+2*dlon
max_lat = np.max(corner_lats)+2*dlat
lat_m = (lats>=min_lat) & (lats<=max_lat) # mask for lat extent
lon_m = (lons>min_lon) & (lons<=max_lon)  # mask for lon extent
trim_lats = lats[lat_m]
trim_lons = lons[lon_m]
fill_value=fp_1['swdown']._FillValue
fp_1.close()

fp_co_ll = open('lat_lon.txt','w')
for i in range(4):
    fp_co_ll.write(str(corner_lons[i])+" "+str(corner_lats[i])+'\n')
fp_co_ll.close()
cmd = "gdaltransform -output_xy -s_srs '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs' -t_srs "+proj+" < lat_lon.txt > xy_out.txt"
subprocess.run(cmd,shell=True)

fp_xy=open('xy_out.txt','r')
x_val=np.ones((4,))
y_val=np.ones((4,))
for i in range(4):
    xy = fp_xy.readline().split()
    x_val[i]=xy[0]
    y_val[i]=xy[1]
fp_xy.close()

extent=[0,0,0,0]
extent[0]=np.round(np.mean(x_val))-dx*x/2 # get left extent for x
extent[2]=np.round(np.mean(x_val))+dx*x/2 # get right extent for x
extent[1]=np.round(np.mean(y_val))-dy*y/2 # get lower extent for y
extent[3]=np.round(np.mean(y_val))+dy*y/2 # get upper extent for y
ex_string = str(extent[0])+' '+str(extent[1])+' '+str(extent[2])+' '+str(extent[3])

gdal_cmd = "gdalwarp -s_srs "+src_proj+" -t_srs "+proj+" -te "+ex_string+" -tr "+\
           str(dx)+' '+str(dy)+' -r bilinear'
print(gdal_cmd)

# --------------------------------- #
# REGRID THE FILES NETCDF to NETCDF #
# --------------------------------- #
# NOTE: this is not an optimized method to accomplish the regridding
# figuring out how to regrid with CDO or with GDAL directly from netCDF
# would be optimal, but unfortunately I had issues with this and getting
# it to work is a higher priority than optimization

# Create subdirectory for this parallel filegroup
out_dir = 'out'+str(rank)+'/'
subprocess.run('mkdir '+run_dir+w_dir+out_dir,shell=True)

# Some variable lists
var_names={'T2D':'tair','Q2D':'spfh','RAINRATE':'precip'}
var_max={'T2D':335,'Q2D':.05,'RAINRATE':10}

# Delcare proj4 and Create transform (west, north, xsize, ysize)
proj4_src = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

print('Rank '+str(rank)+' regridding...',flush=True)
for file in filelist[rank::size]:
	for var in var_names.keys():
		src_file =w_input+file
		src_name = "NETCDF:\""+src_file+"\":"+var_names[var]
		new_name = run_dir+w_dir+out_dir+file[0:8]+"_"+var+".nc"
		regrid_cmd = gdal_cmd+' '+src_name+' '+new_name+' >/dev/null'
		subprocess.run(regrid_cmd,shell=True)
	data = nc.Dataset(new_name,'r')['Band20'][:]
	for t in range(24):
		name=file[0:8]+format(t,'02d')+'.LDASIN_DOMAIN1'
		fp_out=nc.Dataset(run_dir+forcing_dir+name,'w')
		fp_out.createDimension('south_north',data.shape[0])
		fp_out.createDimension('west_east',data.shape[1])
		fp_out.createDimension('Time',1)
		fp_out.createDimension('DateStrLen',20)

		# read in data
		for var in var_names.keys():
			fp_out.createVariable(var,'f4',('Time','south_north','west_east'),\
                                              fill_value=fill_value)
			var_file =  run_dir+w_dir+out_dir+file[0:8]+"_"+var+".nc"
			data = nc.Dataset(var_file,'r')['Band'+str(t+1)][:]
			msk=(data>=var_max[var])
			smmsk=np.sum(msk)
			data[msk]=np.median(data)
			if(smmsk>0):
				print(str(smmsk)+' BAD VALUES FILLED FOR '+str(var)\
                    +' ON '+file[0:8]+format(t,'02d'))
			fp_out[var][0,:,:]=data[:]
			fp_out[var].missing_value=fill_value
		# load in other data
		fp_out.createVariable('Times','c',('DateStrLen'))
		time_str=file[0:4]+'-'+file[4:6]+'-'+file[6:8]+'_'+format(t,'02d')+':00:00 '
		fp_out['Times'][:]=time_str[:]
		fp_out.createVariable('valid_time','i4',('Time'))
		dt = datetime.datetime(int(file[0:4]),int(file[4:6]),int(file[6:8]),t)
		fp_out['valid_time'][0]=dt.replace(tzinfo=datetime.timezone.utc).timestamp()
		fp_out.createVariable('lat','f4',('south_north','west_east'))
		fp_out.createVariable('lon','f4',('south_north','west_east'))
		fp_out['lat'].FieldType=104
		fp_out['lat'].units="degrees latitude"
		fp_out['lat'].sr_x=1
		fp_out['lat'].sr_y=1
		fp_out['lat'].stagger='M'
		fp_out['lat'].description = 'Latitude on mass grid'
		fp_out['lon'].FieldType=104
		fp_out['lon'].units="degrees longitude"
		fp_out['lon'].sr_x=1
		fp_out['lon'].sr_y=1
		fp_out['lon'].stagger='M'
		fp_out['lon'].description = 'Longitude on mass grid'

		# load in lat and long
		fp_out['lat'][:]=fp_geo['XLAT_M'][0,:,:]
		fp_out['lon'][:]=fp_geo['XLONG_M'][0,:,:]
		fp_out.close()
	subprocess.run('rm '+run_dir+w_dir+out_dir+file[0:8]+"_*",shell=True)

			
	
