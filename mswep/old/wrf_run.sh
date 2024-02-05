#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="conus_RG"
#SBATCH --output="log.regrid"
#SBATCH --exclusive

mpiexec -n 3 python wrf_regrid.py

