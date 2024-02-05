#!/bin/sh
#SBATCH --nodes=3
#SBATCH --tasks-per-node=2
#SBATCH --job-name="wrf_data"
#SBATCH --output="full.log"

#mpiexec -n 90 python f_tke.py
#mpiexec -n 90 python f_lwp.py
#mpiexec -n 90 python f_fluxes.py
#mpiexec -n 90 python f_cape.py
#mpiexec -n 90 python f_cloud.py
mpiexec -n 90 python f_pw.py

