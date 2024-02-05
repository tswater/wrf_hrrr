# A script to handle all steps of the WRF preprocessing, including
#   geogrid, ungrib and metgrid, for HRRR initialized WRF

import os
import subprocess as sp
import numpy as np
import netCDF4 as nc
import rasterio
from datetime import datetime
from datetime import timedelta
import sys

# ------------------------------------------------------------------------- #
# ----------------------- USER INPUTS and CONSTANTS ----------------------- #
# ------------------------------------------------------------------------- #
# This is the only section of the code that the user should need to edit
# for most basic level runs

#### DOMAIN DESCRIPTION ####
lat_center     = 38.5 # latitude of the center of the domain
lon_center     = -97.5 # longitude of the center of the domain
e_we           = 1560 # number of gridcells in west_east direction (n+1)
e_sn           = 1040 # number of gridcells in north_south direction (n+1)
e_vert         = 51  # number of gridcells from top to bottom
dx             = 3000 # gridcell size for mass grid
dy             = 3000 # gridcell size for mass grid
start_date     = '2023-07-19_09:00:00' # format 'yyyy-mm-dd_hh:mm:ss'
end_date       = '2023-07-19_11:00:00' # format 'yyyy-mm-dd_hh:mm:ss'
dt             = 15 # timestep for the WRF model in seconds

#### PROJECTION #####
truelat1       = 38.5 # first standard parallel
truelat2       = 38.5 # second standard parallel
stand_lon      = -97.5 # standard_longitude

#### FILE LOCATIONS ####
wrf_dir        = '/home/tsw35/soteria/software/WRF/'
wps_dir        = '/home/tsw35/soteria/software/WPS/'
wps_geo_dir    = '/home/tsw35/soteria/software/WRFv4.3/WPS_GEOG/'
hrrr_dir       = '/home/tsw35/tyche/data/HRRR/'
ungrib_dir     = '/home/tsw35/tyche/data/UNGRIB/'

vtable         = wps_dir+'ungrib/Variable_Tables/Vtable.HRRR.bkb'
mettable       = wps_dir+'metgrid/METGRID.TBL.HRRR.bkb'



# -------------------------------------------------------------------------- #
# --------------------------- GENERAL SETUP -------------------------------- #
# -------------------------------------------------------------------------- #
# General setup of the script and declaration of some constants

#### RELATIVE FILEPATHS ####
namelist_dir='namelists/'
w_dir= 'workspace/'
out_dir = 'OUTPUT/'
met_dir = 'MET/'
log_dir = 'logs/'
tbl_dir = 'tables/'
run_dir = os.getcwd()+'/'


#### MAKE SOME FOLDERS ####
try:
    os.mkdir(log_dir)
except:
    pass
try:
    os.mkdir(met_dir)
except:
    pass
try:
    os.mkdir(out_dir)
except:
    pass

proj = "+proj=lcc +a=6371229 +b=6371229 +lon_0="+str(stand_lon)+" +lat_1="+\
       str(truelat1)+" +lat_2="+str(truelat2)

#### TIME SETUP ####
start_dt = datetime.strptime(start_date,'%Y-%m-%d_%X')
end_dt   = datetime.strptime(end_date,'%Y-%m-%d_%X')
dt_met   = timedelta(hours=1)
runtime  = end_dt-start_dt
runhours = int(runtime.total_seconds()/3600)

# -------------------------------------------------------------------------- #
# ---------------------------- DOMAIN SETUP -------------------------------- #
# -------------------------------------------------------------------------- #
# Edit the namelist.wps file, and then run geogrid.exe in the WPS folder to  
# create a geo_emd01.nc file.

print('SETTING UP DOMAIN (GEOGRID)',flush=True)

#### EDIT NAMELIST.WPS ####
print('  Modifying WPS namelist...',end='',flush=True)
wps_write =''
fp_wps = open(namelist_dir+'templates/namelist.wps','r')
for line in fp_wps:
    if 'start_date' in line:
        wps_write += ' start_date = \''+start_date+'\','+'\n'
    elif 'end_date' in line:
        wps_write += ' end_date   = \''+end_date+'\','+'\n'
    elif 'e_we' in line:
        wps_write += ' e_we           ='+str(e_we)+','+'\n'
    elif 'e_sn' in line:
        wps_write += ' e_sn           ='+str(e_sn)+','+'\n'
    elif 'dx' in line:
        wps_write += 'dx = '+str(dx)+','+'\n'
    elif 'dy' in line:
        wps_write += 'dy = '+str(dy)+','+'\n'
    elif 'ref_lat' in line:
        wps_write += ' ref_lat   = '+str(lat_center)+','+'\n'
    elif 'ref_lon' in line:
        wps_write += ' ref_lon   = '+str(lon_center)+','+'\n'
    elif 'truelat1' in line:
        wps_write += ' truelat1  = '+str(truelat1)+','+'\n'
    elif 'truelat2' in line:
        wps_write += ' truelat2  = '+str(truelat2)+','+'\n'
    elif 'stand_lon' in line:
        wps_write += ' stand_lon = '+str(stand_lon)+','+'\n'
    elif 'geog_data_path' in line:
        wps_write += ' geog_data_path = \''+wps_geo_dir+'\''+'\n'
    elif 'opt_output_from_metgrid_path' in line:
        wps_write += ' opt_output_from_metgrid_path = \''+str(run_dir+met_dir)+'\','+'\n'
    else:
        wps_write += line
fp_wps.close()
fp_out = open(namelist_dir+'namelist.wps','w')
fp_out.write(wps_write)
fp_out.close()
print('COMPLETE',flush=True)

#### RUN GEOGRID ####
print('  Running Geogrid.exe')
sp.run('ln -s '+wps_dir+'geogrid.exe .',shell=True)
sp.run('mkdir geogrid',shell=True)
sp.run('cp '+wps_dir+'geogrid/GEOGRID.TBL geogrid/',shell=True)
sp.run('cp '+run_dir+namelist_dir+'namelist.wps '+run_dir,shell=True)
sp.run('./geogrid.exe >'+run_dir+log_dir+'geogrid_log.txt',shell=True)
sp.run('rm -rf geogrid',shell=True)
sp.run('unlink geogrid.exe',shell=True)
sp.run('mv log.geogrid '+run_dir+log_dir,shell=True)
print('  Geogrid Run Complete')
print('DOMAIN SETUP COMPLETE\n',flush=True)


# -------------------------------------------------------------------------- #
# -------------------------- METEOROLOGY SETUP ----------------------------- #
# -------------------------------------------------------------------------- #
# Run ungrib.exe and metgrid.exe to produce necessary meteorological files.

#### UNGRIB ####

# check if ungrib is necessary
print('UNGRIBBING HRRR FILES',flush=True)
print('  checking if ungrib is needed...',flush=True,end='')
ungrib=False
ungrib_files=os.listdir(ungrib_dir)
final_files=[]
for t in (start_dt+timedelta(hours=n) for n in range(runhours+1)):
    t_str=t.strftime('%Y-%m-%d_%H')
    final_files.append('FILE:'+t_str)
    if ('FILE:'+t_str) in ungrib_files:
        continue
    else:
        ungrib=True

# if ungrib unecessary, only need to link
if not ungrib:
    print('COMPLETE ungrib is not required')
    for file in final_files:
        sp.run('ln -s '+ungrib_dir+file+' '+file,shell=True)
    print('UNGRIB COMPLETE!\n',flush=True)

# ungrib and copy files to ungrib folder
if ungrib:
    print('COMPLETE ungrib is required')
    sp.run('ln -s '+vtable+' Vtable',shell=True) #link to Vtable
    print('  generating ungrib filelist...',flush=True,end='')
    
    filelist=''
    for t in (start_dt+timedelta(hours=n) for n in range(runhours+1)):
        file=t.strftime('hrrr2.%Y%m%d.t%Hz.grib2')
        filelist+=(hrrr_dir+file+' ')
    sp.run('ln -s '+wps_dir+'link_grib.csh',shell=True)
    sp.run('ln -s '+wps_dir+'ungrib.exe',shell=True)
    cmd = './link_grib.csh '+str(filelist)
    print(cmd)
    sp.run(cmd,shell=True)    
    print('COMPLETE')
    print('  beginning ungrib...',flush=True,end='')
    sp.run('./ungrib.exe >'+run_dir+log_dir+'ungrib_log.txt',shell=True)
    sp.run('mv FILE:* '+ungrib_dir,shell=True)
    for file in final_files:
        sp.run('ln -s '+ungrib_dir+file+' '+file,shell=True)
    print('UNGRIB COMPLETE!\n',flush=True)

#### METGRID ####
print('GENERATING MET FILES',flush=True)
print('  ...',flush=True)
sp.run('mkdir metgrid',shell=True)
sp.run('cp '+mettable+' metgrid/METGRID.TBL',shell=True)
sp.run('ln -s '+wps_dir+'metgrid.exe',shell=True)
sp.run('./metgrid.exe',shell=True)
sp.run('rm metgrid',shell=True)
sp.run('unlink link_grib.csh',shell=True)
sp.run('unlink metgrid.exe',shell=True)
sp.run('mv *.log logs/',shell=True)
sp.run('unlink ungrib.exe',shell=True)
print('METGRID COMPLETE\n',flush=True)

# Remove ungrib links
for file in final_files:
    sp.run('unlink '+file,shell=True)
sp.run('unlink Vtable',shell=True)
print('UNGRIB UNLINKED!\n',flush=True)



# -------------------------------------------------------------------------- #
# --------------------------- FINAL RUN SETUP ------------------------------ #
# -------------------------------------------------------------------------- #
# Link tables and edit the main run namelist to match desired characteristics


#### MODIFY NAMELIST.INPUT ####
print('Modifying WRF namelist...',end='',flush=True)
wrf_write =''
fp_wrf = open(namelist_dir+'templates/namelist.input','r')
for line in fp_wrf:
    if 'run_days' in line:
        wrf_write += ' run_days = '+str(runtime.days)+','+'\n'
    elif 'run_hours' in line:
        wrf_write += ' run_hours = '+str(int(runtime.seconds/3600))+','+'\n'
    elif 'start_year' in line:
        wrf_write += ' start_year = '+str(start_dt.year)+',\n'
    elif 'start_month' in line:
        wrf_write += ' start_month = '+str(start_dt.month)+',\n'
    elif 'start_day' in line:
        wrf_write += ' start_day = '+str(start_dt.day)+',\n'
    elif 'start_hour' in line:
        wrf_write += ' start_hour = '+str(start_dt.hour)+',\n'
    elif 'end_year' in line:
        wrf_write += ' end_year = '+str(end_dt.year)+',\n'
    elif 'end_month' in line:
        wrf_write += ' end_month = '+str(end_dt.month)+',\n'
    elif 'end_day' in line:
        wrf_write += ' end_day = '+str(end_dt.day)+',\n'
    elif 'end_hour' in line:
        wrf_write += ' end_hour = '+str(end_dt.hour)+',\n'
    elif 'e_we' in line:
        wrf_write += ' e_we           ='+str(e_we)+','+'\n'
    elif 'e_sn' in line:
        wrf_write += ' e_sn           ='+str(e_sn)+','+'\n'
    elif 'e_vert' in line:
        wrf_write += ' e_vert         ='+str(e_vert)+','+'\n'
    elif 'dx' in line:
        wrf_write += 'dx = '+str(dx)+','+'\n'
    elif 'dy ' in line:
        wrf_write += 'dy = '+str(dy)+','+'\n'
    elif ' time_step ' in line:
        wrf_write += ' time_step = '+str(dt)+',\n'
    else:
        wrf_write += line
fp_wrf.close()
fp_out = open(namelist_dir+'namelist.input','w')
fp_out.write(wrf_write)
fp_out.close()
print('COMPLETE',flush=True)

# -------------------------------------------------------------------------- #
# ------------------------------- CLEAN ------------------------------------ #
# -------------------------------------------------------------------------- #
# Clean out clutter that is no longer needed to run WRF (i.e. only for WPS)


print()
print('#### WRF SETUP IS NOW COMPLETE ####')
print()
