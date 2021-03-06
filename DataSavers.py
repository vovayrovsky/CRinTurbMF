#!/usr/bin/env python
# -*- coding: utf-8 -*-

import crpropa as cr
import math
#-----------------------------------------------------------------------------------------------------------------------------------

class StepOutput(cr.Module):
	def __init__ (self, fname, step):
		cr.Module.__init__ (self)
		self.fout = open(fname, 'w')
		self.fout.write ('#X\tY\tZ\n')
		self.step = step
		self.i = 0
	
	def process (self, c):
		if (self.i < self.step):
			self.i += 1
			return
		
		self.i = 1	
		
		x = c.current.getPosition().x
		y = c.current.getPosition().y
		z = c.current.getPosition().z
		self.fout.write('%f\t%f\t%f\n'%(x, y, z))
		
	def close(self):
		self.fout.close()
		
	def __del__(self):
		if (not self.fout.closed):
			self.fout.close()
		
#-----------------------------------------------------------------------------------------------------------------------------------

class DiffOutput(cr.Module):
	def __init__ (self, fname, step, append = False):
		cr.Module.__init__ (self)
		self.fout = open(fname, 'a+' if append else 'w')
		if not append:
			self.fout.write ('#id\tL\tD_x\tD_r\tmu\tX\tY\tZ\tdl\n')
		
		self.step = step
		self.i = 0
		
		self.count = 0
		
		self.Diff_coeff_x = 0
		self.Diff_coeff_r = 0
		self.current_id = 0
	
	def process (self, c):
		
		if (self.current_id != c.getSerialNumber()):
			self.current_id = c.getSerialNumber()
			self.Diff_coeff_x = 0
			self.Diff_coeff_r = 0
			self.count = 1
			self.i = self.step	
			#print 'New particle'
		
		L = c.getTrajectoryLength()
	
 		d0 = c.source.getDirection()
		p0 = c.source.getPosition()
		
		d = c.current.getDirection()
		p = c.current.getPosition()
		
		x = (p.x-p0.x)/cr.pc
		y = (p.y-p0.y)/cr.pc
		z = (p.z-p0.z)/cr.pc
		
		V_x0 = d0.x
		V_y0 = d0.y
		V_z0 = d0.z
			
		V_x = d.x
		V_y = d.y
		V_z = d.z
	
		tetta = d0.getAngleTo (d)
		mu = math.cos (d0.getAngleTo (cr.Vector3d (1,0,0))) - math.cos(d.getAngleTo (cr.Vector3d (1,0,0)))
		
		self.count += 1
		self.Diff_coeff_x += x * cr.pc * V_x
		self.Diff_coeff_r += y * cr.pc * V_y
		
		if (self.i < self.step):
			self.i += 1
			return
			
		self.i = 1	
		
		self.fout.write('%i\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (self.current_id, L, self.Diff_coeff_x / self.count,
		                                                                 self.Diff_coeff_r / self.count, mu, x, y, z, c.getCurrentStep()))
		
	def close(self):
		self.fout.close()

	def __del__(self):
		if (not self.fout.closed):
			self.fout.close()
#-----------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	print "It's a libriary.\nYou can use python -i DataSavers.py for testing\nStarting test script"
	StepOutput("test", 10).close();
