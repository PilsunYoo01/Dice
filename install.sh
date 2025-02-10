#!/bin/bash


export LD_LIBRARY_PATH=/home/_qamd/apps/boost_1_85_0/stage/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/home/_qamd/apps/hdf5-1.10.6_build/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/home/yoo_ps/_qamd/apps/OpenBLAS_build/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/home/yoo_ps/_qamd/apps/lapack_build/lib:$LD_LIBRARY_PATH
make clean
make Dice -j 
