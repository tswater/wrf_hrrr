#!/bin/sh
#SBATCH --nodes=6
#SBATCH --tasks-per-node=2
#SBATCH --job-name="wrf024"
#SBATCH --output="logs/wrf_runlog.txt"
#SBATCH --exclusive
#SBATCH --nodelist=node1[0-5]

# -------------------------------------- #
# ----------- USER SETTINGS ------------ #
WRFdir=/home/tsw35/soteria/software/avgs_WRF/wrf_1560_1040_24_169
NUMproc=169


# -------------------------------------- #


#### Link Meteorology Files ####
for i in $(ls MET/); do
ln -s MET/$i .
done

#### Link Tables and Data ####
ln -s $WRFdir/run/VEGPARM.TBL .
ln -s $WRFdir/run/SOILPARM.TBL .
ln -s namelists/namelist.input .
ln -s $WRFdir/run/CAMtr_volume_mixing_ratio .
ln -s $WRFdir/run/LANDUSE.TBL .
ln -s $WRFdir/run/ozone_plev.formatted .
ln -s $WRFdir/run/ozone_lat.formatted .
ln -s $WRFdir/run/ozone.formatted .
ln -s $WRFdir/run/RRTMG_LW_DATA .
ln -s $WRFdir/run/RRTMG_SW_DATA .
ln -s $WRFdir/run/GENPARM.TBL .
ln -s $WRFdir/run/CCN_ACTIVATE.BIN .

#### Run real.exe ####
if [ -e wrfbdy_d01 ] && [ -e wrfinput_d01 ]
then
    echo "Real.exe already ran"
else
    ln -s $WRFdir/main/real.exe
    mpiexec -n $NUMproc ./real.exe
    rm real.exe
fi

#### Unlink Meteorology/Real ####
for i in $(ls MET/); do
    rm $i
done

#### Run Wrf.exe ####
if [ -e wrfbdy_d01 ] && [ -e wrfinput_d01 ]
then
    ulimit -s unlimited
    ln -s $WRFdir/main/wrf.exe
    printf "\n\nRUNNING WRF.EXE\n\n"
    mpiexec -n $NUMproc ./wrf.exe
else
    echo "Real.exe Failed"
    exit 0 
fi

#### Clean things up a bit ####
rm wrf.exe
rm *.TBL
mv rsl.* logs/
mv wrfout_* OUTPUT/
rm ozone*
rm CAMtr_volume_mixing_ratio
rm RRTMG*
rm CCN_ACTIVATE.BIN
rm freezeH2O.dat
rm qr_acr
rm namelist.output
rm namelist.input
