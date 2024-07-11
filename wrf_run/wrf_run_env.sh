#!/bin/bash

export DIR=/home/tswater/Software
export CC=gcc
export CXX=g++
export F77=gfortran
export FC=gfortran
export FFLAGS="-m64 -w -fallow-argument-mismatch -O2"
export FCFLAGS="-m64 -w -fallow-argument-mismatch -O2"
export CFLAGS="-Wno-error=implicit-function-declaration -Wno-incompatible-function-pointer-types"
export NETCDF=/home/tswater/Software
export PATH=$PATH:/home/tswater/Software/bin
export CPPFLAGS="-fcommon"
export LD_LIBRARY_PATH=/home/tswater/miniconda3/envs/wrfrun/lib:/usr/lib:/usr/include:/home/tswater/Software/lib:/home/tswater/Software/include
