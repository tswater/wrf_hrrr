from subprocess import run
import os
import sys

#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="wrf_cmp"
#SBATCH --output="log.compress120"
#SBATCH --nodelist=node14

folder=sys.argv[1]

comp=True
dele=False

scdir='/home/tsw35/tyche/wrf_hrrr/scaling/'
odir='/home/tsw35/tyche/wrf_hrrr/compressed/'

dir2=scdir+folder+'/OUTPUT/'
flist=os.listdir(dir2)
flist.sort()
i=0
for file in flist:
    print(file)
    cmd='ncks -7 -L 1 --baa=4 --ppc default=1 '+dir2+file+' '+odir+folder+'/'+file
    fp=open('compsh/'+'cmp'+file+'.sh','w')
    lines=[]
    lines.append("#!/bin/sh\n")
    lines.append("#SBATCH --nodes=1\n")
    lines.append("#SBATCH --tasks-per-node=2\n")
    lines.append('#SBATCH --job-name="wrf_cmp"\n')
    lines.append('#SBATCH --output="log.compress'+str(i)+'"\n')
    lines.append('\n'+cmd+'\n')
    fp.writelines(lines)
    fp.close()
    run('chmod +x '+'compsh/'+'cmp'+file+'.sh',shell=True)
    run('sbatch '+'compsh/'+'cmp'+file+'.sh',shell=True)
    i=i+1

