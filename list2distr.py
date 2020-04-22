#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np

if (len(sys.argv) < 2):
	print 'No input file'
	exit()

print 'started'

fin = open (sys.argv[1], "r")

max_step = float(fin.readline())

gist = np.zeros(1000)

for line in fin:
	val = float(line)
	for i in range (1000):
		if (i < (val / max_step * 1000) and (val / max_step  * 1000) <= i + 1):
			gist[i] += 1
			
fin.close()
fout = open (sys.argv[1] + "_o.csv", "w")

for i in range (1000):
	fout.write ("%f\t%f\n"%(float(i) / 1000., gist[i]))

fout.close()
