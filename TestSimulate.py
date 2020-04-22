#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crpropa import *
import Field2File as f2f
from DataSavers import * 

import sys
import argparse
import os

#-----------------------------------------------------------------------------------------------------------------------------------

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-mf', '--mfield', action='store_true', default = False, help = 'Enabling saving magnetic field and trajectory')
 
    return parser

#-----------------------------------------------------------------------------------------------------------------------------------

if (not os.path.isdir("output")): os.mkdir("output")
os.chdir("output")

cargpars = createParser();
params = cargpars.parse_args(sys.argv[1:])

if (params.mfield):
	print 'started with saving magnetic field'
else:
	print 'started'
	
#турбулентное  поле
n = 500
spacing = 200*au
origin = Vector3d (-n/2 * spacing, -n/2 * spacing, -n/2 * spacing)
lMin, lMax = spacing*2, n * spacing 
Brms = 6*nG
alpha = -11./3.
seed = 40

Lc = turbulentCorrelationLength (lMin, lMax, alpha)
vGrid = VectorGrid (origin, n, spacing)
initTurbulence (vGrid, Brms, lMin, lMax, alpha, seed)
B_turbulent_field = MagneticFieldGrid (vGrid)

#тянущее поле
ConstMagVec = Vector3d (6*nG, 0*nG, 0*nG)
B_const_field = UniformMagneticField (ConstMagVec)

#общее поле
Bfield = MagneticFieldList()
Bfield.addField (B_turbulent_field)
Bfield.addField (B_const_field)

print 'end B_field'

sim = ModuleList()

if (params.mfield):
	f2f.FieldToFile (Bfield, Vector3d(n * spacing, n * spacing, n * spacing), origin, 30, "magnetic_field.mf")
	print 'B_field writed to file magnetic_field.mf'
	
	myoutput = StepOutput ('my_trajectory.txt', 100)
	sim.add (myoutput)

diffoutput = DiffOutput ('my_diff_trajectory.txt', 10)
sim.add (diffoutput)

sim.add (PropagationCK (Bfield, 10e-11, 10*au, 1*pc))
sim.add (MaximumTrajectoryLength (100*pc))

# source setup
source = Source()
#source.add (SourceUniformBox (Vector3d(0.1*n*spacing, 0.2*n*spacing, 0.2*n*spacing),
#                              Vector3d(0.5*n*spacing, 0.8*n*spacing, 0.8*n*spacing)))

source.add (SourcePosition (Vector3d (0, 0, 0)))
                              
source.add (SourceDirection (Vector3d (1, 1, 0)))
source.add (SourceParticleType (nucleusId (1, 1)))

source.add (SourceEnergy (1 * TeV))

sim.setShowProgress (True)
sim.run (source, 1)

#output.close()

if (params.mfield):
	myoutput.close()
	
diffoutput.close()

print 'end simulation'
