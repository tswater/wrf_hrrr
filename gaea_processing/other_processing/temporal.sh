#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="wrf_data"
#SBATCH --output="log.temporal2"
time python temporal_stats.py 0
time python temporal_stats.py 2
time python temporal_stats.py 3

