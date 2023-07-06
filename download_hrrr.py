# Script to download hrrr data from the aws server

###### IMPORT STATEMENTS #######
import s3fs
import time
import os
import subprocess as sp

###### SETUP AND USER INPUT ######
odir = '/home/tsw35/tyche/data/HRRR/' # destination directory
dates=['20170719','20170720']
###### MAIN BODY #######
s3 = s3fs.S3FileSystem(anon=True)
for date in dates:
    fs= 'noaa-hrrr-bdp-pds/'
    fs=fs+'hrrr.'+date+'/conus/'
    print('Beginning download for '+date,flush=True)
    print('  Retrieving file list...',flush=True)
    files = s3.ls(fs)
    print('  Downloading...',flush=True)
    for file in files:
        if ('prs' in file) and ('f00' in file) and ('idx' not in file):
            print('    '+file,end='...',flush=True)
            s3.get(file,odir)
            print('  DOWNLOADED',flush=True)
    print('  '+date+' COMPLETE')
    
    for file in os.listdir(odir):
        if 'hrrr2' in file:
            continue
        ff=odir+file
        sp.run('mv '+ff+' '+odir+'hrrr2.'+date+'.'+file[5:9]+'.grib2',shell=True)
    print('moved')
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



