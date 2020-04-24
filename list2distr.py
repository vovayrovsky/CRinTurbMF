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

fin.close()

data = np.loadtxt (sys.argv[1], skiprows = 1) 

resolution = 10

hist, bins = np.histogram (data, bins = resolution)

fout = open (sys.argv[1] + "_o.csv", "w")

for i in range (resolution):
	fout.write ("%f\t%f\n"%(bins[i], hist[i]))

fout.close()
