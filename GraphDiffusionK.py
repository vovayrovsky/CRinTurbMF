#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import tk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pylab import *
import os
import sys

from crpropa import *

#-----------------------------------------------------------------------------------------------------------------------------------

def MakeGraph (X, Y, fname):
	plt.figure (figsize = (12,12))
	plt.subplot()
	plt.scatter (X, Y, s=5)
	plt.savefig (fname)
	print 'Generated ' + fname
	return

#-----------------------------------------------------------------------------------------------------------------------------------

print 'started'

if (len(sys.argv) < 2):
	print 'No input file'
	exit(0)

#id,L,D_x,D_y,mu,x,y,z, dl = np.genfromtxt (sys.argv[1], unpack=True, skip_footer=1)
L,D_x,D_y = np.genfromtxt (sys.argv[1], unpack=True)

if (not os.path.isdir(sys.argv[1]+"dir")): os.mkdir(sys.argv[1]+"dir")
os.chdir(sys.argv[1]+"dir")

#Diff_xx = np.cumsum (D_x) 

#Norm = np.linspace (1,  Diff_xx.size, Diff_xx.size)

#Diff_xx_norm = Diff_xx/Norm

# plot trajectories
#MakeGraph (L, (L - x), 'demo_coord.png')

#  plot Diff_x
MakeGraph ((L)/pc, D_x, 'Diff_X_scatter.png')

#  plot Diff_y
MakeGraph ((L)/pc, D_y, 'Diff_Y_scatter.png')

#  plot Diff_mu
#MakeGraph ((L)/pc, mu, 'Diff_angle.png')
