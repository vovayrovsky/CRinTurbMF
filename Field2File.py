#!/usr/bin/python
# -*- coding: utf-8 -*-

#Magnetic filed file format
#MF%lg%lg%lg%u%lg%lg%lg\n		--x_size --y_size --z_size --steps --x_origin --y_origin --z_origin
#*** %lg%lg%lg					3d array of vectors (--x, --y, --z)

import crpropa as cr
import struct

#-----------------------------------------------------------------------------------------------------------------------------------

def FieldToFile (field, size, origin, steps, filename):
	output_file = open (filename, 'wb')
	output_file.write (struct.pack ('ccdddIdddc', 'M', 'F', size.x, size.y, size.z, steps, 
						origin.x, origin.y, origin.z, 'I'))
	
	for x in range (steps):
		for y in range (steps):
			for z in range (steps):
				fieldValue = field.getField (cr.Vector3d (x / steps * size.x, y / steps * size.y, z / steps * size.z))
				output_file.write(struct.pack('ddd', fieldValue.x, fieldValue.y, fieldValue.z))
	
	output_file.close()

#-----------------------------------------------------------------------------------------------------------------------------------

def FileToGrid (filename):
	
	try:
		output_file = open (filename, 'rb')
	except IOError:
		print "Unable to open file " + filename;
		return 0;
		
	try:
		bufstr = output_file.read(struct.calcsize('ccdddIdddc'))
	except IOError:
		print "Wrong file format";
		return 0;
		
	buf = struct.unpack('ccdddIdddc', bufstr)
	size = cr.Vector3d (buf[2], buf[3], buf[4])
	origin = cr.Vector3d (buf[6], buf[7], buf[8])
	steps = buf[5]
		
	if (buf[0] != 'M' or buf[1] != 'F' or buf[9] != 'I'):
		print "Wrong file format";
		return 0;
	
	retGrid = cr.VectorGrid (origin, steps, steps, steps, size / steps)
	
	for x in range (steps):
		for y in range (steps):
			for z in range (steps):
				bufstr = output_file.read(struct.calcsize('ddd'))
				buf = struct.unpack('ddd', bufstr)
				retGrid.setValue (x, y, z, cr.Vector3f(buf[0], buf[1], buf[2])) #I've np idea why VectorGrid is Grid<Vector3<float>>
	
	output_file.close()

#-----------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    print "It's a libriary.\nYou'd better use python -i Field2File.py\nStarting test script"
    tstfield = cr.UniformMagneticField(cr.Vector3d (1, 0, 0))
    test_file_name = "test_magnetic_field.mf"
    FieldToFile (tstfield,  cr.Vector3d (1 * cr.pc, 1 * cr.pc, 1 * cr.pc), 
    						cr.Vector3d (0, 0, 0), 10, test_file_name)
    
    tstload = FileToGrid (test_file_name)
