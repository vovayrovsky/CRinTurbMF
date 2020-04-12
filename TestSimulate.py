#!/usr/bin/python
# -*- coding: utf-8 -*-

from crpropa import *
import Field2File as f2f

#-----------------------------------------------------------------------------------------------------------------------------------

class MyOutput(Module):
	def __init__ (self, fname):
		Module.__init__ (self)
		self.fout = open(fname, 'w')
		self.fout.write ('#X\tY\tZ\n')
		self.i = 0
	
	def process (self, c):
		if (self.i % 100 != 0):
			self.i += 1
			return
		
		self.i = 1	
		x = c.current.getPosition().x
		y = c.current.getPosition().y
		z = c.current.getPosition().z
		self.fout.write('%f\t%f\t%f\n'%(x, y, z))
		
	def close(self):
		self.fout.close()
		
#-----------------------------------------------------------------------------------------------------------------------------------

print 'started'

#турбулентное  поле
n = 500
spacing = 200*au
origin = Vector3d (-n/2 * spacing, -n/2 * spacing, -n/2 * spacing)
lMin, lMax = spacing*2, n * spacing 
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

f2f.FieldToFile (Bfield, Vector3d(n * spacing, n * spacing, n * spacing), origin, 200, "magnetic_field.mf")

print 'B_field writed to file magnetic_field.mf'

sim = ModuleList()
sim.add (PropagationCK (Bfield, 10e-11, 10*au, 1*pc))
sim.add (MaximumTrajectoryLength (100*pc))
#output = TextOutput ('trajectory.txt', Output.Trajectory3D)
myoutput = MyOutput ('my_trajectory.txt')

#sim.add (output)
sim.add (myoutput)

# source setup
source = Source()
#source.add (SourceUniformBox (Vector3d(0.1*n*spacing, 0.2*n*spacing, 0.2*n*spacing),
#                              Vector3d(0.5*n*spacing, 0.8*n*spacing, 0.8*n*spacing)))

source.add (SourcePosition (Vector3d (0, 0, 0)))
                              
source.add (SourceDirection (Vector3d (1, 1, 0)))
source.add (SourceParticleType (nucleusId (1, 1)))

source.add (SourceEnergy (1 * TeV))

sim.setShowProgress (True)
sim.run (source, 1)

#output.close()
myoutput.close()


print 'end simulation'
