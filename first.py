"""
Program to organize ies files into data matrix.

Daniel Santander
February 23, 2019
"""

import pandas as pd


def openfile(file):
	"""
	Opens file and returns a list containig the contents of the file, where each new line is indexed.

	Parameters file: File to open
	Preconditions: File is string name of a '.txt' file
	"""
	if type(file) != str:
		str(file)

	with open(file) as f:
		lines = [x.rstrip() for x in f]

	return lines

def rowsncols(file):
	"""
	Returns the rows and columns of the IES dataset as a list, where the first element is the
	number of rows and the second elemnt is the number of columns.

	Parameters list: line #11 of the file contains the information pertaining to the dimensions
		of the dataset
	Preconditions: File is string name of a '.txt' file
	"""
	list = openfile(file)

	for line in list:
		if 'TILT' in line:
			if 'NONE' in line:
				num = list.index(line)
				break
			elif 'INCLUDE' in line:
				num = (list.index(line) + 4)
				break

	copy = list[num + 1]
	for x in range(4):
		index = copy.find(' ')
		copy = copy[index + 1:]
		if x == 2:
			index = copy.find(' ')
			cols = int(copy[:index])
		if x == 3:
			index = copy.find(' ')
			rows = int(copy[:index])
	output = [rows,cols]
	return output

def getdataset(file):
	"""
	Returns a list that includes the data from a dataset with the header and file information removed.
	Each line of the original file is a new index in the list

	Parameters file: File to open
	Preconditions: File is string name of a '.txt' file
	"""
	list = openfile(file)
	for line in list:
		if 'TILT' in line:
			if 'NONE' in line:
				num = 14 
			elif 'INCLUDE' in line:
				num = 18
	copy = list[num:]

	return copy

def organizedata(file):
	"""
	Returns the data from the file organized into a dataframe

	Parameters file: File to open
	Preconditions: File is string name of a '.txt' file
	"""
	data = getdataset(file)
	header = rowsncols(file)
	angles = getangles(file)
	verts = angles [0]
	horiz = angles [1]

	output = []
	for x in range(header[0]):
		copy = data[x]
		line = []
		for x in range(header[1]):
			index = copy.find(' ')
			num = float(copy[:index])
			line.append(num)
			copy = copy[index + 1:]
		output.append(line)

	frame = pd.DataFrame(output, columns = verts, index = horiz)
	return frame

def headerinfo(file):
	"""
	Returns all of the header information indexed in a list

	Parameters file: File to open
	Preconditions: File is string name of a '.txt' file
	"""
	data = openfile(file)
	output = dict()
	for x in data:
		index = x.find('[')
		if index != -1:
			index2 = x.find(']')
			title = x[index + 1:index2]
			copy = x[index2 + 2:]
			if copy != ' ':
				output[title] = copy
	
	return output


def spheretopoint(theta,phi,radius=None):
	"""
	Returns the x,y,and z coordinate of a point described by a theta, phi, and radius from a central point.
	
	Parameters: input values 
	Preconditions: all input are floats. theta between 0-360, phi between 0-90

	Parameters Radius: the radius of the photometric sphere, if unspecified the value of the arm is 1.
	Preconditions: type(radius) == float and radius > 0.
	"""
	import math

	if radius == None:
		radius = 1.0

	z = radius * math.cos(phi)
	r = radius * math.sin(phi)
	y = r * math.sin(theta)
	x = r * math.cos(theta)
	list = [x,y,z]

	return list

def anglestocoor(file):
	"""
	

	Parameters:
	Preconditions:
	"""
	angles = getangles(file)
	vert = angles[0]
	horizon = angles[1]
	#for x in vert:


def getangles(file):
	list = openfile(file)
	for line in list:
		if 'TILT' in line:
			if 'NONE' in line:
				num = 12 
			elif 'INCLUDE' in line:
				num = 16
	angles = list[num:num + 2]

	header = rowsncols(file)
	output = []
	for x in range(2):
		copy = angles[x]
		line = []
		if x == 0:
			for x in range(header[1]):
				index = copy.find(' ')
				num = float(copy[:index])
				line.append(num)
				copy = copy[index + 1:]
			output.append(line)
		else:
			for x in range(header[0]):
				index = copy.find(' ')
				num = float(copy[:index])
				line.append(num)
				copy = copy[index + 1:]
			output.append(line)

	return output









