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
	plt.bar (X, Y, width = 0.001)
	plt.savefig (fname)
	print 'Generated ' + fname
	return

#-----------------------------------------------------------------------------------------------------------------------------------

if (len(sys.argv) < 2):
	print 'No input file'
	exit()
	
print 'started'

X,Y = np.genfromtxt(sys.argv[1], unpack=True, skip_footer=1)


MakeGraph (X[0:30], Y[0:30], sys.argv[1] + '.png')
