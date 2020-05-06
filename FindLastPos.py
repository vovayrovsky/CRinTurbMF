#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sys

print 'started'

if (len(sys.argv) < 2):
	print 'No input file'
	exit(0)

data = np.genfromtxt (sys.argv[1])

fout = open(sys.argv[1] + 'last.txt', 'w')
fout.write ('#id\tL\tD_x\tD_y\tmu\tX\tY\tZ\tdl\n')

prev = data[0]

for element in data:
	if (prev.all() == element.all()):
		continue
		
	if (element[1] <= prev[1]):
		print 'New particle'
		fout.write('%i\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (prev[0], prev[1], prev[2], prev[3], 
															prev[4], prev[5], prev[6], prev[7], prev[8]))
	prev = element
else:
	fout.write('%i\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (prev[0], prev[1], prev[2], prev[3], 
															 	prev[4], prev[5], prev[6], prev[7], prev[8]))
fout.close()
print 'end'
