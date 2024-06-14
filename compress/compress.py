from subprocess import run
import os
import sys

folder=sys.argv[1]

comp=True
dele=False

scdir='/home/tsw35/tyche/wrf_hrrr/scaling/'
odir='/home/tsw35/tyche/wrf_hrrr/compressed/'

dir2=scdir+folder+'/OUTPUT/'
flist=os.listdir(dir2)
flist.sort()
for file in flist:
    print(file)
    cmd='ncks -7 -L 1 --baa=4 --ppc default=1 '+dir2+file+' '+odir+folder+'/'+file
    cmd_d='rm '+dir2+file
    if comp:
        run(cmd,shell=True)
    if dele:
        run(cmd_d,shell=True)
            
