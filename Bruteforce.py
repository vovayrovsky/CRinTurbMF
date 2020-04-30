#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crpropa import *

import Field2File as f2f
from DataSavers import * 

from datetime import datetime

import sys
import argparse
import os

import numpy as np
import math

#-----------------------------------------------------------------------------------------------------------------------------------

def Log(str):
	global logfile
	logfile.write(str)
	sys.stdout.write(str)
	return
	
#-----------------------------------------------------------------------------------------------------------------------------------

def DoSimulation (turb_field, B, Mu, particle_num, energy, length):
	global spacing
	global n
	Log ("Simultaion B = " + str (B) + " Mu = " + str (Mu) + " with " + str (particle_num) + " particles at " + str (datetime.now()) +"\n")
	
	#Магнитное поле
	ConstMagVec = Vector3d (B*muG, 0*muG, 0*muG)
	B_const_field = UniformMagneticField (ConstMagVec)

	Bfield = MagneticFieldList()
	Bfield.addField (B_turbulent_field)
	Bfield.addField (B_const_field)
	
	sim = ModuleList()

	diffoutput = DiffOutput ('B' + str(B) + 'Mu' + str(Mu) +"_sim.txt", 10)
	sim.add (diffoutput)
	
	sim.add (PropagationCK (Bfield, 10e-11, 10*au, 1*pc))
	sim.add (MaximumTrajectoryLength (length))
	
	# source setup
	source = Source()
	source.add (SourceUniformBox (Vector3d(0.1*n*spacing, 0.2*n*spacing, 0.2*n*spacing),
	                              Vector3d(0.5*n*spacing, 0.8*n*spacing, 0.8*n*spacing)))
	
	#source.add (SourcePosition (Vector3d (0, 0, 0)))
                              	
	source.add (SourceDirection (Vector3d (math.cos(Mu), math.sin(Mu), 0)))
	source.add (SourceParticleType (nucleusId (1, 1)))
	
	source.add (SourceEnergy (energy))
	
	sim.setShowProgress (True)
	sim.run (source, particle_num)

	Log ("\n")
	
#-----------------------------------------------------------------------------------------------------------------------------------

def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument ('-mf', '--mfield', action = 'store_true', default = False, help = 'Enabling saving turbulent part of magnetic field and trajectories for visualisation')
	
	parser.add_argument ('-bm', '--minB',   action = 'store', default = 0.0, type = float, help = 'starting B value in muG')
	parser.add_argument ('-mb', '--maxB',   action = 'store', default = 6.0, type = float, help = 'final B value in muG')
	parser.add_argument ('-bs', '--stepsB', action = 'store', default = 60,  type = int,   help = 'B steps')
	
	parser.add_argument ('-mum', '--minMu',   action = 'store', default = 0.0,       type = float, help = 'starting Mu value in radians')
	parser.add_argument ('-mmu', '--maxMu',   action = 'store', default = math.pi/2, type = float, help = 'final Mu value in radians')
	parser.add_argument ('-mus', '--stepsMu', action = 'store', default = 20,        type = int,   help = 'Mu steps')
	 
	parser.add_argument ('-np', '--particles', action = 'store', default = 2, type = int, help = 'number of particles for one step')
	
	parser.add_argument ('-e', '--energy', action = 'store', default = 1000, type = float, help = 'energy of particle in GeV')
	parser.add_argument ('-l', '--length', action = 'store', default = 100,  type = float, help = 'maximum trajectory length in pc')
	
	parser.add_argument ('-p', '--additional_path', action = 'store', default = '.', help = 'additional path for output directory')
	
	return parser

#-----------------------------------------------------------------------------------------------------------------------------------

cargpars = createParser();
params = cargpars.parse_args(sys.argv[1:])

#-----------------------------------------------------------------------------------------------------------------------------------

path = params.additional_path + "/output" + datetime.now().strftime("%Y-%m-%d_%H:%M")

if (not os.path.isdir(path)): 
	os.mkdir(path)
	
os.chdir(path)

#-----------------------------------------------------------------------------------------------------------------------------------

stepsB = params.stepsB
minB   = params.minB
maxB   = params.maxB

stepsMu = params.stepsMu
minMu   = params.minMu
maxMu   = params.maxMu

energy = params.energy * GeV
tr_length = params.length * pc

saveMF = params.mfield

num_of_part = params.particles

#-----------------------------------------------------------------------------------------------------------------------------------

logfile = open ("log.txt", "w")
Log ("Start logging at " + str (datetime.now()) + "\n");
Log ("Output dir is " + path + "\n\n");

Log ("Simulation parameters:\n");
Log ("B from "  + str (minB)  + " to " + str (maxB)  + " with " + str (stepsB)  + " steps\n")
Log ("Mu from " + str (minMu) + " to " + str (maxMu) + " with " + str (stepsMu) + " steps\n")
Log ("Saving of magnetic filed is " + ("enabled" if saveMF  else "disabled") + "\n\n")

#-----------------------------------------------------------------------------------------------------------------------------------
#турбулентное  поле
Log ("Generating of turbulent magnetic field...\n")
n = 500
spacing = 200*au
origin = Vector3d (-n/2 * spacing, -n/2 * spacing, -n/2 * spacing)
lMin, lMax = spacing*2, n * spacing 
Brms = 6*muG
alpha = -11./3.
seed = 40

Lc    = turbulentCorrelationLength (lMin, lMax, alpha)
vGrid = VectorGrid (origin, n, spacing)
initTurbulence (vGrid, Brms, lMin, lMax, alpha, seed)
B_turbulent_field = MagneticFieldGrid (vGrid)

Log ("Generating of turbulent magnetic field ended\n")

if (saveMF):
	Log ("Writing magnetic field into " + path + "/turbfield.mf\n")
	f2f.FieldToFile (B_turbulent_field, Vector3d(n * spacing, n * spacing, n * spacing), origin, 10, "turbfield.mf")
	Log ("Writed\n")
	
Log ("\n")	

#-----------------------------------------------------------------------------------------------------------------------------------

Log ("Starting simulation cycle\n\n")

for B in np.linspace(minB, maxB, num = stepsB):
	for Mu in np.linspace(minMu, maxMu, num = stepsMu):
		DoSimulation (B_turbulent_field, B, Mu, num_of_part, energy, tr_length)
		logfile.flush()
		
Log ("\nSimulation end\n")
		
#-----------------------------------------------------------------------------------------------------------------------------------

Log ("\nEnd logging at " + str (datetime.now()) + "\n")
logfile.close()
