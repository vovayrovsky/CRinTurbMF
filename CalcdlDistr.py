#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crpropa import *
import Field2File as f2f
from DataSavers import * 

import numpy as np

import sys
import argparse
import os

#-----------------------------------------------------------------------------------------------------------------------------------

class CaldLDistr(cr.Module):
	def __init__ (self, max_step):
		cr.Module.__init__ (self)
		self.gist = np.zeros(1000)
		self.max_step = max_step
		#form 0 to max_step
	
	def process (self, c):
		dl = c.getCurrentStep()
		for i in range (1000):
			if (i < (dl / self.max_step * 1000) and (dl / pc * 1000) <= i + 1):
				self.gist[i] += 1
		
	def save (self, fname):
		fout = open(fname, 'w')
		fout.write ("#X\tY\n");
		
		for i in range (1000):
			fout.write ("%f\t%f\n"%(float(i) / 1000., self.gist[i]))
			
		fout.close()

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

diffoutput = DiffOutput ('my_diff_trajectory.txt', 10)
sim.add (diffoutput)

max_step = 0.02 * pc

calcdistr = CaldLDistr(max_step)
sim.add (calcdistr)

sim.add (PropagationCK (Bfield, 10e-11, 10*au, 1*pc))
sim.add (MaximumTrajectoryLength (100*pc))

# source setup
source = Source()

source.add (SourcePosition (Vector3d (0, 0, 0)))
                              
source.add (SourceDirection (Vector3d (1, 1, 0)))
source.add (SourceParticleType (nucleusId (1, 1)))

source.add (SourceEnergy (1 * TeV))

sim.setShowProgress (True)
sim.run (source, 20)
	
diffoutput.close()
calcdistr.save('distr.csv')

print 'end simulation'
