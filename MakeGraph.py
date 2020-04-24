#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import tk
import matplotlib.pyplot as plt

import sys

import crpropa as cr

#-----------------------------------------------------------------------------------------------------------------------------------

def MakeGraph (X, Y, fname):
	plt.figure (figsize = (24,24))
	plt.subplot()
	plt.tick_params(axis='both', which='major', labelsize=30)
	plt.bar (X, Y, width = 0.1*X[-1])
	plt.savefig (fname)
	print 'Generated ' + fname
	return

#-----------------------------------------------------------------------------------------------------------------------------------

if (len(sys.argv) < 2):
	print 'No input file'
	exit()
	
print 'started'

X,Y = np.genfromtxt(sys.argv[1], unpack=True)

X /= 1 * cr.pc

MakeGraph (X, Y, sys.argv[1] + '.png')
