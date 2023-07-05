# Script to download hrrr data from the aws server

###### IMPORT STATEMENTS #######
import s3fs
import time

###### SETUP AND USER INPUT ######
odir = '/home/tsw35/tyche/data/HRRR/' # destination directory
fs= 'noaa-hrrr-bdp-pds/'


###### MAIN BODY #######
s3 = s3fs.S3FileSystem(anon=True)

test_file=fs+'hrrr.20201202/conus/hrrr.t20z.wrfprsf10.grib2'
start=time.process_time()
s3.get(test_file,odir)
print('Done with get: '+str(time.process_time()-start))
a = s3.du(fs+'hrrr.20201202/conus/')
print(a)

