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
    parser.add_argument ('-mf', '--mfield', action='store_true', default = False, help = 'EnablimuG savimuG magnetic field and trajectory')
 
    return parser

#-----------------------------------------------------------------------------------------------------------------------------------

if (not os.path.isdir("output")): os.mkdir("output")
os.chdir("output")

cargpars = createParser();
params = cargpars.parse_args(sys.argv[1:])

if (params.mfield):
	print 'started with savimuG magnetic field'
else:
	print 'started'
	
#турбулентное  поле
n = 500
spacimuG = 200*au
origin = Vector3d (-n/2 * spacimuG, -n/2 * spacimuG, -n/2 * spacimuG)
lMin, lMax = spacimuG*2, n * spacimuG 
Brms = 6*muG
alpha = -11./3.
seed = 40

Lc = turbulentCorrelationLength (lMin, lMax, alpha)
vGrid = VectorGrid (origin, n, spacimuG)
initTurbulence (vGrid, Brms, lMin, lMax, alpha, seed)
B_turbulent_field = MagneticFieldGrid (vGrid)

#тянущее поле
ConstMagVec = Vector3d (6*muG, 0*muG, 0*muG)
B_const_field = UniformMagneticField (ConstMagVec)

#общее поле
Bfield = MagneticFieldList()
Bfield.addField (B_turbulent_field)
Bfield.addField (B_const_field)

print 'end B_field'
     
sim = ModuleList()

if (params.mfield):
	f2f.FieldToFile (Bfield, Vector3d(n * spacimuG, n * spacimuG, n * spacimuG), origin, 30, "magnetic_field.mf")
	print 'B_field writed to file magnetic_field.mf'
	
	myoutput = StepOutput ('my_trajectory.txt', 100)
	sim.add (myoutput)

diffoutput = DiffOutput ('my_diff_trajectory.txt', 200, append = False)
sim.add (diffoutput)

sim.add (PropagationCK (Bfield, 10e-11, 10*au, 1*pc))
sim.add (MaximumTrajectoryLength (50*pc))

# source setup
source = Source()
source.add (SourceUniformBox (Vector3d(-2 * spacimuG, - 2 * spacimuG, -2 * spacimuG),
                              Vector3d(4 * spacimuG, 4 * spacimuG, 4 * spacimuG)))

#source.add (SourcePosition (Vector3d (0, 0, 0)))
                              
source.add (SourceDirection (Vector3d (1, 0, 0)))
source.add (SourceParticleType (nucleusId (1, 1)))

source.add (SourceEnergy (1 * TeV))

sim.setShowProgress (True)
sim.run (source, 20)

#output.close()

if (params.mfield):
	myoutput.close()
	
diffoutput.close()

print 'end simulation'
