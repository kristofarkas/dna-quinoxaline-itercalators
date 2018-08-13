"""Relative free energy calculations

Example implementation using ABIGAIL and NAMD.

"""

import sys

import numpy as np

from htbac import Runner, System, Simulation, Protocol, AbFile, DataAggregate
from htbac.protocols import RFE


def run_rfe(s, steps, proc):
    pdb = AbFile('{}.pdb'.format(s), tag='pdb')
    top = AbFile('{}.prmtop'.format(s), tag='topology')
    tag = AbFile('{}_tags.pdb'.format(s), tag='alchemicaltags')
    cor = AbFile('{}.inpcrd'.format(s), tag='coordinate')
    system = System(name='1z3f-intercalator-complex', files=[pdb, top, tag, cor])

    p = Protocol(RFE.minimize(),
                 RFE.simulation(),
                 RFE.simulation(),
                 RFE.simulation(),
                 RFE.simulation(),
                 RFE.simulation(),
                 RFE.simulation(),
                 DataAggregate(extension=".alch"))
    
    step_counts = [1000, 500, 500, 1000, 1000, 10000, steps] 

    for rfe, numsteps in zip(p.simulations(), step_counts):
        rfe.system = system
        rfe.engine = 'namd'
        rfe.processes = proc
        rfe.threads_per_process = 1
        
        rfe.cutoff = 10.0
        rfe.switchdist = 8.0
        rfe.pairlistdist = 11.5
        rfe.numsteps = numsteps
        rfe.watermodel = 'tip3'
        
        rfe.add_ensemble('replica', range(5))
        rfe.add_ensemble('lambdawindow', [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0])
            
    ht = Runner('bw_aprun', comm_server=('two.radical-project.org', 33227))
    ht.add_protocol(p)
    ht.run(walltime=1440, queue='high')

if __name__ == '__main__':
    comp = sys.argv[1]
    if comp.startswith('int'):
        s = 'intercalator'
        steps = 3000000
        proc = 32
    elif comp.startswith('com'):
        s = 'complex'
        steps = 10000000
        proc = 128
    else:
        exit(1)
    run_rfe(s, steps, proc)
