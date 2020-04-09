#!/usr/bin/python
# -*- coding: utf-8 -*-

from crpropa import *

#турбулентное  поле
origin = Vector3d (0, 0, 0)
n = 500
spacing = 100*au
lMin, lMax = spacing*2, n*spacing 
Brms = 3*nG
alpha = -11./3.
seed = 40

Lc = turbulentCorrelationLength (lMin, lMax, alpha)
vGrid = VectorGrid (origin, n, spacing)
initTurbulence (vGrid, Brms, lMin, lMax, alpha, seed)
B_turbulent_field = MagneticFieldGrid (vGrid)

#тянущее поле
ConstMagVec = Vector3d (0*nG, 0*nG, 0*nG)
B_const_field = UniformMagneticField (ConstMagVec)

#общее поле
Bfield = MagneticFieldList()
Bfield.addField (B_turbulent_field)
Bfield.addField (B_const_field)

print 'end B_field'

sim = ModuleList()
sim.add (PropagationCK (Bfield, 10e-11, 10*au, 1*pc))
sim.add (MaximumTrajectoryLength (10*pc))
output = TextOutput ('trajectory.txt', Output.Trajectory3D)
sim.add (output)

# source setup
source = Source()
source.add (SourceUniformBox (Vector3d(0.1*n*spacing, 0.2*n*spacing, 0.2*n*spacing),
                              Vector3d(0.5*n*spacing, 0.8*n*spacing, 0.8*n*spacing)))
                              
source.add (SourceDirection (Vector3d (1, 0, 0)))
source.add (SourceParticleType (nucleusId (1, 1)))

source.add (SourceEnergy (1 * TeV))

sim.setShowProgress (True)
sim.run (source, 2)

output.close()

print 'end simulation'
