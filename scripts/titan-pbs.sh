#!/bin/bash

#PBS -A chm126
#PBS -N dna-intercalator
#PBS -l nodes=500
#PBS -l walltime=04:00:00
#PBS -l gres=atlas1%atlas2

cd $MEMBERWORK/chm126/dna-quinoxaline-itercalators/systems

module load cudatoolkit
module load python wraprun

export OPENMM_PYTHON="/ccs/proj/chm126/farkaspall/miniconda2/bin/python"
export OPENMM_CUDA_COMPILER=`which nvcc`

date

DNADIRS=""

for i in $(seq -f "%02g" 1 20)
do
    cd lig-$i
    for j in $(seq -f "%02g" 1 25)
    do
      mkdir rep-$j
      cd rep-$j
      cp ../../../scripts/simulate.py .
      DNADIRS="$DNADIRS,lig-$i/rep-$j"
      cd ../
    done
    cd ../
done

DNADIRS=${DNADIRS#","}

wraprun -n 1 serial --w-cd $DNADIRS $OPENMM_PYTHON simulate.py

date
