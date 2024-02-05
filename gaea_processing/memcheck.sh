#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="wrf_data"
#SBATCH --output="log.mem"
#SBATCH --exclusive
#SBATCH --partition=chaney-md
free -h

