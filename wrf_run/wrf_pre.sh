#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="wrftst"
#SBATCH --output="wrf_prelog.txt"

time python parallel_wrf_preprocess.py

