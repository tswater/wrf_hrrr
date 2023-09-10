import numpy as np
import subprocess as sp
import os
import netCDF4 as nc
import wrf

#### SETUP ####

# stuff
rmold=False

# variables to be copmuted by wrf-python
"""
postvars=['mcape','mcin','lcl','lfc','low_cloudfrac','mid_cloudfrac',\
          'high_cloudfrac','helicity','updraft_helicity','pres','tk','th',\
          'tv','height_agl']
"""
postvars=['mcape','mcin','lcl','lfc','low_cloudfrac','mid_cloudfrac',\
          'high_cloudfrac','helicity','updraft_helicity','pres','tk','th',\
          'height_agl']
# variables to be computed by me in this script
tswvars=['lwp','netLW','netSW']

# variables to keep from wrf for one Timestep
wrfvars0=['XLAT','XLONG','LU_INDEX','ZS','ZNU','ZNW','ALBEDO','EMISS','LAI','LANDMASK','LAKEMASK','IVGTYP','ISLTYP','VEGFRA']

# variables to keep from wrf for multiple Timesteps
"""
wrfvars1=['U','V','W','Q2','T2','TH2','PSFC','U10','V10','QVAPOR',\
          'QRAIN','SMOIS','SFROFF','UDROFF',\
          'GRDFLX','SNOW','LAI','QKE','NUPDRAFT','TKE_PBL','HGT','TSK',\
          'RAINNC','RAINC','RAINSH','CLDFRA','ALBEDO','EMISS','UST',\
          'PBLH','HFX','QFX','LH','SST','MU','MUB']
"""

wrfvars1=['U','V','W','Q2','T2','PSFC','U10','V10','QVAPOR',\
          'SMOIS',\
          'GRDFLX','TKE_PBL','HGT','TSK',\
          'RAINNC','UST',\
          'PBLH','HFX','QFX','LH','SST']

wrfmapf=['MAPFAC_M','MAPFAC_U','MAPFAC_V','MAPFAC_MX','MAPFAC_MY','MAPFAC_UX',\
         'MAPFAC_UY','MAPFAC_VX','MF_VX_INV','MAPFAC_VY']

#### SETUP FILELISTS ####
odir='OUTPUT/'
filelist=os.listdir(odir)
filelist.sort()
n=len(filelist)
dims={'Time':1,'west_east':1559,'south_north':1039,'bottom_top':50,'bottom_top_stag':51,\
      'soil_layers_stag':6,'west_east_stag':1560,'south_north_stag':1040,'seed_dim_stag':12}

print('Postprocessing a total of '+str(n)+' files',flush=True)

#### FIGURE OUT PART II ####
ovars={}
odesc={'lwp':'Liquid Water Path',
       'netLW':'Net Longwave',
       'netSW':'Net Shortwave',
       'mcape':'Maximum CAPE',
       'mcin' :'Maximum CIN',
       'lcl':'Lifting Condensation Level',
       'lfc':'Level of Free Convection',
       'low_cloudfrac':'Low level Cloud Fraction (300-2000)',
       'mid_cloudfrac':'Mid Level Cloud Fraction (2000-6000)',
       'high_cloudfrac':'High Level Cloud Fraction (6000+)',
       'helicity':'Storm Relative Helicity (<3000m)',
       'updraft_helicity':'Updraft Helicity 2000-5000m',
       'pres':'Pressure',
       'tk':'Temperature in Kelvin',
       'th':'Potential Temperature',
       'tv':'Virtual Temperature',
       'height_agl':'Height Above Ground Level'}
ounit={'lwp':'g kg-1',
       'netLW':'W m-2',
       'netSW':'W m-2',
       'mcape':'J kg-1',
       'mcin':'J kg-1',
       'lcl':'m',
       'lfc':'m',
       'low_cloudfrac':'%',
       'mid_cloudfrac':'%',
       'high_cloudfrac':'%',
       'helicity':'m2 s-2',
       'updraft_helicity':'m2 s-2',
       'pres':'Pa',
       'tk':'K',
       'th':'K',
       'tv':'K',
       'height_agl':'m'}
odims={'lwp':('Time','south_north','west_east'),
       'netLW':('Time','south_north','west_east'),
       'netSW':('Time','south_north','west_east'),
       'mcape':('Time','south_north','west_east'),
       'mcin':('Time','south_north','west_east'),
       'lcl':('Time','south_north','west_east'),
       'lfc':('Time','south_north','west_east'),
       'low_cloudfrac':('Time','south_north','west_east'),
       'mid_cloudfrac':('Time','south_north','west_east'),
       'high_cloudfrac':('Time','south_north','west_east'),
       'helicity':('Time','south_north','west_east'),
       'updraft_helicity':('Time','south_north','west_east'),
       'pres':('Time','bottom_top','south_north','west_east'),
       'tk':('Time','bottom_top','south_north','west_east'),
       'th':('Time','bottom_top','south_north','west_east'),
       'tv':('Time','bottom_top','south_north','west_east'),
       'height_agl':('Time','bottom_top','south_north','west_east')}


tt=0
for file in filelist:
    fpin=nc.Dataset(odir+file,'r')
    print(fpin)
    newname='tsw2out'+file[10:24]+'.nc'
    if tt==0:
        print('  STATIC FILE',end='',flush=True)
        fpstat=nc.Dataset(odir+'static_data.nc','w')
        print('.',end='',flush=True)
        for d in dims:
            fpstat.createDimension(d,dims[d])
        print('.',end='',flush=True)
        for var in wrfvars0:
            fpstat.createVariable(var,'f4',fpin[var].dimensions)
            fpstat[var][:]=fpin[var][:]
            fpstat[var].description=fpin[var].description
            fpstat[var].units=fpin[var].units
        print('.',end='',flush=True)
        for var in wrfmapf:
            fpstat.createVariable(var,'f4',fpin[var].dimensions)
            fpstat[var][:]=fpin[var][:]
            fpstat[var].description=fpin[var].description
            fpstat[var].units=fpin[var].description
        print('.',end='',flush=True)
        for at in fpin.ncattrs():
            setattr(fpstat,at,fpin.getncattr(at))
        fpstat.close()
        print('COMPLETE',flush=True)
    
    print('  DAY '+file[10:24]+'...',end='',flush=True)
    fpout=nc.Dataset(odir+newname,'w')
    for d in dims:
        fpout.createDimension(d,dims[d])
    print('wrf...',end='',flush=True)
    for var in wrfvars1:
        fpout.createVariable(var,'f4',fpin[var].dimensions)
        fpout[var][:]=fpin[var][:]
        fpout[var].description=fpin[var].description
        fpout[var].units=fpin[var].description
    print('tsw...',end='',flush=True)
    for var in tswvars:
        fpout.createVariable(var,'f4',odims[var])
        fpout[var].description=odesc[var]
        fpout[var].units=ounit[var]
        if var=='lwp':
            pres=fpin['PH'][:]+fpin['PHB'][:]
            print(pres.shape)
            dpres=pres[:,1:,:,:]-pres[:,:-1,:,:]
            print(dpres.shape)
            fpout[var][:]=np.sum(dpres/9.81*fpin['QCLOUD'][:],axis=1)
        elif var=='netSW':
            fpout[var][:]=(1-fpin['ALBEDO'][:])*fpin['SWDOWN'][:]
        elif var=='netLW':
            stbolt=5.670374419*10**(-8)
            lwup=stbolt*fpin['TSK'][:]**4
            fpout[var][:]=fpin['EMISS'][:]*(fpin['GLW'][:]-lwup)
    print('wrfpy',end='',flush=True)
    for var in postvars:
        print('.',end='',flush=True)
        fpout.createVariable(var,'f4',odims[var])
        fpout[var].description=odesc[var]
        fpout[var].units=ounit[var]
        if var=='mcape':
            fpout[var][0,:]=wrf.getvar(fpin,'cape_2d',meta=False)[0,:,:]
        elif var=='mcin':
            fpout[var][0,:]=wrf.getvar(fpin,'cape_2d',meta=False)[1,:,:]
    for at in fpin.ncattrs():
        setattr(fpstat,at,fpin.getncattr(at))

    print()
    fpout.close()
    fpin.close()
    if rmold:
        sp.run('rm '+odir+file,shell=True)
    tt=tt+1



