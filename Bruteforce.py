#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crpropa import *

import Field2File as f2f
from DataSavers import * 

from datetime import datetime

import sys
import argparse
import os

import math

#-----------------------------------------------------------------------------------------------------------------------------------

def createParser ():
	parser = argparse.ArgumentParser ()
	parser.add_argument ('-mf', '--mfield', action = 'store_true', default = False, help = 'Enabling saving turbulent part of magnetic field and trajectories for visualisation')
	
	parser.add_argument ('-bm', '--minB',   action = 'store', default = 0.0, type = float, help = 'starting B value')
	parser.add_argument ('-mb', '--maxB',   action = 'store', default = 6.0, type = float, help = 'final B value')
	parser.add_argument ('-bs', '--stepsB', action = 'store', default = 60,  type = int,   help = 'B steps')
	
	parser.add_argument ('-mum', '--minMu',   action = 'store', default = 0.0,       type = float, help = 'starting Mu value')
	parser.add_argument ('-mmu', '--maxMu',   action = 'store', default = math.pi/2, type = float, help = 'final Mu value')
	parser.add_argument ('-mus', '--stepsMu', action = 'store', default = 20,        type = int,   help = 'Mu steps')
	 
	parser.add_argument ('-np', '--particles', action = 'store', default = 2, type = int, help = 'number of particles for one step')
	
	parser.add_argument ('-p', '--additional_path', action = 'store', default = '.', help = 'number of particles for one step')
	
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

saveMF = params.mfield

num_of_part = params.particles

#-----------------------------------------------------------------------------------------------------------------------------------


logfile = open ("log.txt", "w")
logfile.write ("Start logging at " + str(datetime.now()) + "\n");
logfile.write ("Log dir is " + path + "\n\n");

logfile.write ("Simulation parameters:\n");
logfile.write ("B from "  + str(minB)  + " to " + str(maxB)  + " with " + str(stepsB)  + "steps\n")
logfile.write ("Mu from " + str(minMu) + " to " + str(maxMu) + " with " + str(stepsMu) + "steps\n")
logfile.write ("Saving of magnetic filed is " + ("enabled" if saveMF  else "disabled") + "\n")

logfile.write ("\nEnd logging at " + str(datetime.now()) + "\n")
logfile.close()
