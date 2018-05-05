#!/bin/bash

#PBS -l nodes=16:ppn=32:xe
#PBS -l walltime=00:30:00

export AMBERHOME=/u/sciteam/farkaspa/anaconda3/envs/ambertools
export DNAROOT=/u/sciteam/farkaspa/scratch/dna-quinoxaline-itercalators

source $AMBERHOME/bin/activate ambertools

date

aprun -n 16 mmpbsa.sh

date
