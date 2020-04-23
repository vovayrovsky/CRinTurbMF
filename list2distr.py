#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np

if (len(sys.argv) < 2):
	print 'No input file'
	exit()

print 'started'

fin = open (sys.argv[1], "r")

max_step = float(fin.readline()) * 0.1

resolution = 1000

gist = np.zeros(resolution)

for line in fin:
	val = float(line)
	for i in range (resolution):
		if (i < (val / max_step * resolution) and (val / max_step  * resolution) <= i + 1):
			gist[i] += 1

fin.close()
fout = open (sys.argv[1] + "_o.csv", "w")

for i in range (resolution):
	fout.write ("%f\t%f\n"%(float(i) / float(resolution), gist[i]))

fout.close()
