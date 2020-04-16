#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from mpl_toolkits.mplot3d import axes3d
from mayavi import mlab
import os

from crpropa import *

import Field2File as f2f

#-----------------------------------------------------------------------------------------------------------------------------------

if (not os.path.isdir("output")): os.mkdir("output")
os.chdir("output")

print 'started'

data = np.genfromtxt('my_trajectory.txt', names=True)

print 'data loaded'
# trajectory points
x_d, y_d, z_d = data['X'], data['Y'], data['Z']

Bfield = MagneticFieldList()

empty_field = UniformMagneticField (Vector3d(0, 0, 0))
Bfield.addField (empty_field)

vGrid = f2f.FileToGrid ("magnetic_field.mf")
Bfield.addField (MagneticFieldGrid (vGrid))

print 'field loaded'

N = 30# samples per direction

start_r = -0.1*kpc
end_r   =  0.1*kpc

samples = (np.linspace(start_r, end_r, N, endpoint=True))

B = np.zeros((N,N,N))
Bx = np.zeros((N,N,N))
By = np.zeros((N,N,N))
Bz = np.zeros((N,N,N))
X_pos = np.zeros((N,N,N))
Y_pos = np.zeros((N,N,N))
Z_pos = np.zeros((N,N,N))

X_, Y_, Z_ = np.mgrid[start_r:end_r:(N*1j), start_r:end_r:(N*1j), start_r:end_r:(N*1j)]

for i, xx in enumerate(samples):
	for j, yy in enumerate(samples):
		for k, zz in enumerate(samples):
   	  		pos = Vector3d(xx, yy, zz)
			B[i, j, k] = Bfield.getField(pos).getR() / gauss # B in [G]
			Bx[i, j, k] = Bfield.getField(pos).x / gauss # B in [G]
			By[i, j, k] = Bfield.getField(pos).y / gauss # B in [G]
			Bz[i, j, k] = Bfield.getField(pos).z / gauss # B in [G]
		
print 'magnetic fields view'

tr = mlab.plot3d(x_d,y_d,z_d)
#start_pos = mlab.
u = mlab.flow(X_,Y_,Z_,Bx,By,Bz,seedtype='point')

print kpc
mlab.show()
