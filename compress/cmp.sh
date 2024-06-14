#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="wrf_cmp"
#SBATCH --output="log.compress120"
#SBATCH --nodelist=node14

time python compress.py hmg120
