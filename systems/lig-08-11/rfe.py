"""Relative free energy calculations

Example implementation using ABIGAIL and NAMD.

"""

import numpy as np

from htbac import Runner, System, Simulation, Protocol, AbFile
from htbac.protocols import Rfe


def run_rfe():
    pdb = AbFile('complex.pdb', tag='pdb')
    top = AbFile('complex.prmtop', tag='topology')
    tag = AbFile('tags.pdb', tag='alchemicaltags')
    cor = AbFile('complex.inpcrd', tag='coordinate')
    system = System(name='1z3f-l08-l11', files=[pdb, top, tag, cor])

    p = Protocol(clone_settings=False)
    
    min, run = Rfe.steps

    for step, numsteps in zip([min, run, run, run, run, run], [100, 500, 1000, 1000, 1000, 10000, 8000000]):

        rfe = Simulation()
        rfe.system = system
        rfe.engine = 'namd'
        rfe.processes = 8
        rfe.threads_per_process = 16

        rfe.cutoff = 10.0
        rfe.switchdist = 8.0
        rfe.pairlistdist = 11.5
        rfe.numsteps = numsteps
        rfe.watermodel = 'tip4'
        
        rfe.add_input_file(step, is_executable_argument=True)
        
        rfe.add_ensemble('replica', range(3))
        # to increase the number of EnTK tasks: change the lambdawindow parameter
        rfe.add_ensemble('lambdawindow', np.linspace(0, 1, 13))
        
        p.append(rfe)
        
    ht = Runner('titan_aprun')
    ht.add_protocol(p)
    ht.run(walltime=720)


if __name__ == '__main__':
    run_rfe()
