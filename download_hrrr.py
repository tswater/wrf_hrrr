# Script to download hrrr data from the aws server

###### IMPORT STATEMENTS #######
import s3fs
import time
import os
import subprocess as sp

###### SETUP AND USER INPUT ######
odir = '/home/tsw35/tyche/data/HRRR/' # destination directory
fs= 'noaa-hrrr-bdp-pds/'
dates=['20170719']

###### MAIN BODY #######
s3 = s3fs.S3FileSystem(anon=True)
for date in dates:
    fs=fs+'hrrr.'+date+'/conus/'
    try:
        sp.run('mkdir '+odir+date,shell=True)
    except Exception as e:
        print(e)
    print('Beginning download for '+date,flush=True)
    print('  Retrieving file list...',flush=True)
    files = s3.ls(fs)
    print('  Downloading...',flush=True)
    for file in files:
        if ('prs' in file) and ('f00' in file) and ('idx' not in file):
            print('    '+file,end='...',flush=True)
            s3.get(file,odir+date)
            print('  DOWNLOADED',flush=True)
    print('  '+date+' COMPLETE')
    print()








###### EXTRA STUFF I USED TO TEST THINGS #######

'''
#test_file=fs+'hrrr.20201202/conus/hrrr.t20z.wrfprsf10.grib2'
#start=time.process_time()


### Get a File ###
s3.get(test_file,odir)
print('Done with get: '+str(time.process_time()-start))

### Size of folder ###
a = s3.du(fs+'hrrr.20201202/conus/')
print(a)

### find all prs files ###
a = s3.ls(fs+'hrrr.20201202/conus/')
b=[]
for c in a:
    if ('prs' in c) and ('f00' in c):
        b.append(c)
'''



