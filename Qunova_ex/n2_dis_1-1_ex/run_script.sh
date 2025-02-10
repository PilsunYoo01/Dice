#!/bin/bash

export PYSCF_TMPDIR='.'

source /home/_qamd/apps/QunovaPulsar/activate

export LD_LIBRARY_PATH=/home/_qamd/apps/boost_1_85_0/stage/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/home/_qamd/apps/hdf5-1.10.6_build/hdf5/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/home/_qamd/apps/OpenBLAS_build/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/home/_qamd/apps/lapack_build/lib:$LD_LIBRARY_PATH

which python
#python fci_dump_generation.py
#python Single_diagonalization_test.py > output &
python Single_diagonalization_test.py
