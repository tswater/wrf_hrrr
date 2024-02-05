# Script to download hrrr data from the aws server

###### IMPORT STATEMENTS #######
import s3fs
import time
import os
import subprocess as sp
import numpy as np
import re

###### SETUP AND USER INPUT ######
odir = '/home/tsw35/tyche/data/HRRR/' # destination directory
#dates=['20230601']
dates=['20220601',
 '20210601',
 '20220602',
 '20210602',
 '20220603',
 '20210603',
 '20220604',
 '20210604',
 '20220605',
 '20210605',
 '20220606',
 '20210606',
 '20220607',
 '20210607',
 '20220608',
 '20210608',
 '20220609',
 '20210609',
 '20220610',
 '20210610',
 '20220611',
 '20210611',
 '20220612',
 '20210612',
 '20220613',
 '20210613',
 '20220614',
 '20210614',
 '20220615',
 '20210615',
 '20220616',
 '20210616',
 '20220617',
 '20210617',
 '20220618',
 '20210618',
 '20220619',
 '20210619',
 '20220620',
 '20210620',
 '20220621',
 '20210621',
 '20220622',
 '20210622',
 '20220623',
 '20210623',
 '20220624',
 '20210624',
 '20220625',
 '20210625',
 '20220626',
 '20210626',
 '20220627',
 '20210627',
 '20220628',
 '20210628',
 '20220629',
 '20210629',
 '20220630',
 '20210630',
 '20220701',
 '20210701',
 '20220702',
 '20210702',
 '20220703',
 '20210703',
 '20220704',
 '20210704',
 '20220705',
 '20210705',
 '20220706',
 '20210706',
 '20220707',
 '20210707',
 '20220708',
 '20210708',
 '20220709',
 '20210709',
 '20220710',
 '20210710',
 '20220711',
 '20210711',
 '20220712',
 '20210712',
 '20220713',
 '20210713',
 '20220714',
 '20210714',
 '20220715',
 '20210715',
 '20220716',
 '20210716',
 '20220717',
 '20210717',
 '20220718',
 '20210718',
 '20220719',
 '20210719',
 '20220720',
 '20210720',
 '20220721',
 '20210721',
 '20220722',
 '20210722',
 '20220723',
 '20210723',
 '20220724',
 '20210724',
 '20220725',
 '20210725',
 '20220726',
 '20210726',
 '20220727',
 '20210727',
 '20220728',
 '20210728',
 '20220729',
 '20210729',
 '20220730',
 '20210730',
 '20220731',
 '20210731',
 '20220801',
 '20210801',
 '20220802',
 '20210802',
 '20220803',
 '20210803',
 '20220804',
 '20210804',
 '20220805',
 '20210805',
 '20220806',
 '20210806',
 '20220807',
 '20210807',
 '20220808',
 '20210808',
 '20220809',
 '20210809',
 '20220810',
 '20210810',
 '20220811',
 '20210811',
 '20220812',
 '20210812',
 '20220813',
 '20210813',
 '20220814',
 '20210814',
 '20220815',
 '20210815',
 '20220816',
 '20210816',
 '20220817',
 '20210817',
 '20220818',
 '20210818',
 '20220819',
 '20210819',
 '20220820',
 '20210820',
 '20220821',
 '20210821',
 '20220822',
 '20210822',
 '20220823',
 '20210823',
 '20220824',
 '20210824',
 '20220825',
 '20210825',
 '20220826',
 '20210826',
 '20220827',
 '20210827',
 '20220828',
 '20210828',
 '20220829',
 '20210829',
 '20220830',
 '20210830',
 '20220831',
 '20210831',
 '20220901',
 '20210901',
 '20220902',
 '20210902']

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
        if ('prs' in file) and ('f00' in file) and ('idx' not in file):
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
                print('ERROR t00z NOT AVAILABLE')
                print('ERROR t00z NOT AVAILABLE')
                quitloop=True
                break
            t2=t-1
            if t2<10:
                tstr='0'+str(t2)
            else:
                tstr=str(t2)
            
            fname=re.sub(r"t\d+z",'t'+tstr+'z',genfile)
            fname=re.sub('f00','f01',fname)
            print('  missing f00 for '+tstr)
            print('  Trying with '+fname)
            try:
                s3.get(fname,odir+date+str(t)+'hrrr2')
            except:
                t2=t2-1
                if t2<0:
                    print('ERROR t0-1z NOT AVAILABLE')
                    print('ERROR t0-1z NOT AVAILABLE')
                    quitloop=True
                    break
                if t2<10:
                    tstr2='0'+str(t2)
                else:
                    tstr2=str(t2)
                fname=re.sub('t'+tstr+'z',tstr2,fname)
                fname=re.sub('f01','f02',fname)
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



