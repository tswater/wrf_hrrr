#!/bin/sh
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --job-name="WRFpost"
#SBATCH --output="log.postproc"

#cd gaea_processing
#time python agg_full.py
#time python 2d_agg.py
cd mswep/
time python error_1d.py
#time python error_2d.py
