#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import tk
import matplotlib.pyplot as plt
from pylab import *
from mpl_toolkits.mplot3d import axes3d
from mayavi import mlab
import os

from crpropa import *

#-----------------------------------------------------------------------------------------------------------------------------------

def MakeGraph (X, Y, fname):
	plt.figure (figsize = (12,12))
	plt.subplot()
	plt.plot (X, Y)
	plt.savefig (fname)
	print 'Generated ' + fname
	return

#-----------------------------------------------------------------------------------------------------------------------------------

if (not os.path.isdir("output")): os.mkdir("output")
os.chdir("output")

print 'started'

i,L,D_x,D_y,mu,x,y,z = np.genfromtxt('my_diff_trajectory.txt', unpack=True, skip_footer=1)

Diff_xx = np.cumsum (D_x) 

Norm = np.linspace(1,  Diff_xx.size, Diff_xx.size)

Diff_xx_norm = Diff_xx/Norm

# plot trajectories
MakeGraph (L, (L - x), 'demo_coord.png')

#  plot Diff_x
MakeGraph ((L + i * pc)/pc, D_x, 'Diff_X_scatter.png')

#  plot Diff_y
MakeGraph ((L + i * pc)/pc, D_y, 'Diff_Y_scatter.png')

#  plot Diff_mu
MakeGraph ((L + i * pc)/pc, mu, 'Diff_angle.png')
