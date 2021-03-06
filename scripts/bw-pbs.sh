#!/bin/bash

#PBS -l nodes=500:ppn=16:xk
#PBS -l walltime=04:00:00

cd $PBS_O_WORKDIR
cd ../systems

module load cudatoolkit

export PATH=/u/sciteam/farkaspa/anaconda3/bin:$PATH
export LD_LIBRARY_PATH=/u/sciteam/farkaspa/anaconda3/lib:$LD_LIBRARY_PATH
export OPENMM_CUDA_COMPILER=/opt/nvidia/cudatoolkit7.5/7.5.18-1.0502.10743.2.1/bin/nvcc


for i in $(seq -f "%02g" 1 20)
do
    cd lig-$i
    for j in $(seq -f "%02g" 1 25)
    do
      mkdir rep-$j
      cd rep-$j
      cp ../../../scripts/simulate.py .
      aprun -n1 python simulate.py &
      cd ../
    done
    cd ../
done

wait



