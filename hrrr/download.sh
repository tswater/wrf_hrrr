#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="dwnHRRR"
#SBATCH --output="download.log"
#SBATCH --exclusive

time python download_hrrr.py
