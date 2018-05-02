#!/bin/bash

#PBS -A chm126
#PBS -N dna-intercalator
#PBS -l nodes=500
#PBS -l walltime=04:00:00
#PBS -l gres=atlas1%atlas2

cd $MEMBERWORK/chm126/dna-quinoxaline-itercalators/systems

module load cudatoolkit

export PATH=/ccs/proj/chm126/farkaspall/miniconda3/bin:$PATH
export LD_LIBRARY_PATH=/ccs/proj/chm126/farkaspall/miniconda3/lib:$LD_LIBRARY_PATH
export OPENMM_CUDA_COMPILER=/opt/nvidia/cudatoolkit7.5/7.5.18-1.0502.10743.2.1/bin/nvcc

date

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

date
