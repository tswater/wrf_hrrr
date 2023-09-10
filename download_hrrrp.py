# Script to download hrrr data from the aws server

###### IMPORT STATEMENTS #######
import s3fs
import time
import os
import subprocess as sp
import numpy as np
import re

###### SETUP AND USER INPUT ######
odir = '/home/tsw35/tyche/data/HRRRp/' # destination directory
dates=['20170716','20170717','20170718','20170719','20170720','20160625','20160626','20180709','20180710','20220803','20220804']

###### MAIN BODY #######

manual=False
quitloop=False
s3 = s3fs.S3FileSystem(anon=True)
for date in dates:
    fs= 'noaa-hrrr-bdp-pds/'
    fs=fs+'hrrr.'+date+'/conus/'
    print('Beginning download for '+date,flush=True)
    print('  Retrieving file list...',flush=True)
    files = s3.ls(fs)
    files.sort()
    print('  Downloading...',flush=True)

    genfile=''

    for file in files:
        if ('prs' in file) and ('f01' in file) and ('idx' not in file):
            print('    '+file,end='...',flush=True)
            s3.get(file,odir)
            genfile=file
            print('  DOWNLOADED',flush=True)

    # check to make sure 24 hours were downloaded
    dwnld=np.zeros((24,))
    for file in os.listdir(odir):
        if 'hrrr2' in file:
            continue
        for t in range(24):
            if t<10:
                tstr='0'+str(t)
            else:
                tstr=str(t)
            if ('t'+tstr+'z') in file:
                dwnld[t]=1
    for t in range(24):
        if dwnld[t]==0:
            if t==0:
                print('ERROR t01z NOT AVAILABLE')
                print('ERROR t01z NOT AVAILABLE')
                quitloop=True
                break
            t2=t-1
            if t2<10:
                tstr='0'+str(t2)
            else:
                tstr=str(t2)
            
            fname=re.sub(r"t\d+z",'t'+tstr+'z',genfile)
            fname=re.sub('f01','f02',fname)
            print('  missing f01 for '+tstr)
            print('  Trying with '+fname)
            try:
                s3.get(fname,odir+date+str(t)+'hrrr2')
            except:
                t2=t2-1
                if t2<0:
                    print('ERROR t02z NOT AVAILABLE')
                    print('ERROR t02z NOT AVAILABLE')
                    quitloop=True
                    break
                if t2<10:
                    tstr2='0'+str(t2)
                else:
                    tstr2=str(t2)
                fname=re.sub('t'+tstr+'z',tstr2,fname)
                fname=re.sub('f02','f03',fname)
                print('  ... FAILED Trying with '+fname)
                try:
                    s3.get(fname,odir+date+str(t)+'hrrr2')
                except:
                    print('  FAILED, skipping')
            manual=True
    print('  '+date+' COMPLETE')
    


    for file in os.listdir(odir):
        if 'hrrr2' in file:
            continue
        ff=odir+file
        sp.run('mv '+ff+' '+odir+'hrrr2.'+date+'.'+file[5:9]+'.grib2',shell=True)
    
    if quitloop:
        print('ERROR NEEDS FIXING .... ')
        break
    print('moved')
    print()

if manual:
    print('MANUAL MOVES REQUIRED')




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



