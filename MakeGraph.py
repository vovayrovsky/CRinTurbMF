#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import tk
import matplotlib.pyplot as plt

import sys

import crpropa as cr

#-----------------------------------------------------------------------------------------------------------------------------------

def MakeGraph (X, Y, fname):
	print 'Start generating ' + fname
	plt.figure (figsize = (12, 12))
	plt.subplot()
	#plt.tick_params (axis='both', which='major', labelsize=30)
	plt.scatter (X, Y)
	plt.savefig (fname)
	print 'Generated ' + fname
	return

#-----------------------------------------------------------------------------------------------------------------------------------

if (len(sys.argv) < 2):
	print 'No input file'
	exit()
	
print 'started'

id,L,D_x,D_y,mu,X,Y,Z, dl = np.genfromtxt (sys.argv[1], unpack=True)

#X /= 1 * cr.pc
#Y /= 1 * cr.pc
#Z /= 1 * cr.pc

R = np.sqrt(Y ** 2 + Z ** 2)

MakeGraph (X, R, sys.argv[1] + 'XR.png')
MakeGraph (X, Y, sys.argv[1] + 'XY.png')
MakeGraph (X, Z, sys.argv[1] + 'XZ.png')
