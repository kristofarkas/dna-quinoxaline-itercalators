import simtk.openmm.app as app
import simtk.openmm as mm
import simtk.unit as u

import parmed as pmd

import numpy as np

T_i = 50*u.kelvin
T = 300*u.kelvin
P = 1*u.atmosphere
ts = 0.002*u.picoseconds

sstep = 100
nstep = 1000000

prmtop = app.AmberPrmtopFile('../complex.prmtop')
inpcrd = app.AmberInpcrdFile('../complex.inpcrd')

system = prmtop.createSystem(nonbondedMethod=app.PME, 
                             nonbondedCutoff=10*u.angstrom, 
                             switchDistance=9*u.angstrom,
                             constraints=app.HBonds)

integrator = mm.LangevinIntegrator(T_i, 1/u.picosecond, ts)
barostat = mm.MonteCarloBarostat(P, T)

simulation = app.Simulation(prmtop.topology, system, integrator)

simulation.reporters.append(app.DCDReporter('output.dcd', 1000))
simulation.reporters.append(app.StateDataReporter('state.out', 1000, 
                                                  step=True, 
                                                  potentialEnergy=True, 
                                                  temperature=True))

simulation.context.setPositions(inpcrd.positions)
simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)

simulation.minimizeEnergy()

for temperature in np.arange(T_i, T, 1*u.kelvin):
    integrator.setTemperature(temperature)
    simulation.step(sstep)
    
simulation.saveCheckpoint('temp.chk')

simulation.system.addForce(barostat)
simulation.context.reinitialize()

simulation.loadCheckpoint('temp.chk')

simulation.step(3*nstep)
