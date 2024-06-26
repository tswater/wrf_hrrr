# wrf_hrrr
None of the code is optimizied or designed for use outside of the Duke University cluster and is presented as is

### Compress
contains code to compress the output files to more reasonable sizes

### Gaea Processing
processing of the summer analysis datasets etc.

### HRRR
code related to downloading and processing HRRR

### jupyter_notebooks
jupyter notebooks used to explore the data and create paper figures. Jupyter notebooks are not uploaded, rather python script representations of them. Use jupytext to convert them back to jupyter notebooks. Core notebook is the paper3_figures.py notebook.

### mswep
code related to analyzing mswep precipitation

### wrf_mods
modified RUCLSM code needed to homogenize the surface fluxes. Files named as ruclsm_[WE dimension]_[SN dimension]_[Homogenization scale]_[number of threads].F
these files should replace module_sf_ruclsm.F in the wrf code before compilations.
These files will only work for the specified dimensions and WRF must be run with the number of threads described to work
For details, contact owner of this repository

### wrf_run
Run folder for a WRF run.
wrf_preprocess.py will create the necessary inputs for a WRF run (including modifying namelist geographic details, but not physics options)
wrf_run.sh will pull in the WRF executibles from appropriate location (the WRF software folder) and run WRF
