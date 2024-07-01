#!/bin/sh
#SBATCH --nodes=5
#SBATCH --tasks-per-node=2
#SBATCH --exclusive
#SBATCH --job-name="wrf_qke"
#SBATCH --output="log.qke"

#mpiexec -n 90 python f_tke.py
#mpiexec -n 90 python f_lwp.py
#mpiexec -n 90 python f_fluxes.py
#mpiexec -n 90 python f_cape.py
#mpiexec -n 90 python f_cloud.py
#mpiexec -n 90 python f_pw.py
#mpiexec -n 90 python f_ms_fluxes.py
#mpiexec -n 90 python f_TRH.py
#mpiexec -n 90 python f_fix.py
#mpiexec -n 90 python f_eb.py
#mpiexec -n 90 python f_mske.py
mpiexec -n 140 python f_qke.py
