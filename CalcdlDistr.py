#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crpropa import * 

import numpy as np

import sys
import argparse
import os

#-----------------------------------------------------------------------------------------------------------------------------------

class SaveL(Module):
	def __init__ (self, max_step, fname):
		Module.__init__ (self)
		self.fout = open (fname, "w")
		self.fout.write (str (max_step) + "\n")
		
	def process (self, c):
		dl = c.getCurrentStep()
		self.fout.write (str(dl) + "\n")
		
	def close (self):
		self.fout.close()

#-----------------------------------------------------------------------------------------------------------------------------------

if (not os.path.isdir("output")): os.mkdir("output")
os.chdir("output")

print 'started'
	
#турбулентное  поле
n = 500
spacing = 0.2*pc
origin = Vector3d (-n/2 * spacing, -n/2 * spacing, -n/2 * spacing)
lMin, lMax = 0.5 * pc, 50 * pc 
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

max_step = 0.1 * pc

lsave = SaveL(max_step, 'dl.csv')
sim.add (lsave)

sim.add (PropagationCK (Bfield, 10e-11, 10*au, 1*pc))
sim.add (MaximumTrajectoryLength (100*pc))

# source setup
source = Source()

source.add (SourcePosition (Vector3d (0, 0, 0)))
                              
source.add (SourceDirection (Vector3d (1, 1, 0)))
source.add (SourceParticleType (nucleusId (1, 1)))

source.add (SourceEnergy (1 * TeV))

sim.setShowProgress (True)
sim.run (source, 300)

lsave.close()

print 'end simulation'
