#!/bin/bash

date

for i in $(seq -f "%02g" 1 20)
do
    for j in $(seq -f "%02g" 1 25)
    do
	cd $DNAROOT/systems/lig-$i/rep-$j
	cp $DNAROOR/scripts/mmpbsa.in .
	MMPBSA.py -O -eo mmpbsa-energy.out -i mmpbsa.in -o mmpbsa.out -sp complex.prmtop -cp complex-dry.prmtop -rp dna.prmtop -lp intercalator.prmtop -y output.dcd > mmpbsa.log &
    done
done

wait

date
