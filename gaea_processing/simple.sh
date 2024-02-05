#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="wrf_data"
#SBATCH --output="simple2.log"
#SBATCH --exclusive
#SBATCH --nodelist=node8
time python prerain_full.py

