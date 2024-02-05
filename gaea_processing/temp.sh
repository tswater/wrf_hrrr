#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="wrf_data"
#SBATCH --output="log.temporal"
time python temporal_stats.py

