#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=2
#SBATCH --job-name="grb2nc"
#SBATCH --output="grb2nc.log"
#SBATCH --exclusive

time python grb2nc.py
