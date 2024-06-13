#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="wrf_agg"
#SBATCH --output="log.agg"
#SBATCH --exclusive
#time python 2d_agg.py
#time python agg_full.py
time python agg_4d.py

