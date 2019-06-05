"""
This program performs linear interpolation of a spherical coordinate point to the points of measurement in a goniophotmometric reading.
It then returns the candela value at the point, based on the linear interpolation.

By: Daniel Santander
Started: April 14th
Completed: April 15th
"""

import math
import first
import second
import pandas as pd


class li (object):
	"""
	The provided point with accompanying functions to return lighting data given the point.
	
	Instance Attributes:
		Point: (list) spherical coordinates of the point. index 0 = theta, index 1 = phi, index 2 = r
		Verts: (list) all of the vertical angles recorded in the IES file
		Horiz: (list) all of the horizontal angles recorded in the IES file
		Data: (Pandas data frame) Contains the lighting data, verts = columns | horiz = rows
	"""

	def __init__ (self,x,y,z,file):
		"""
		Intializes an instance of a linear interpolation object

		Parameter: file is the IES file with horizontal and vertical angles
		Precondition file: file is a string
		"""
		x = float(x)
		y = float(y)
		z = float(z)

		point = second.point(x,y,z)
		spoint = point.thetaphi()

		self.point = spoint
		angles = first.getangles(file)
		self.verts = angles[0]
		self.horiz = angles[1]

		self.data = first.organizedata(file)


	def getpoint(self):
		return self.point
	def getverts(self):
		return self.verts
	def gethoriz (self):
		return self.horiz
	def getphirange (self):
		return self.phirange
	def getthetarange (self):
		return self.thetarange
	def getdata(self):
		return self.data

	def anglesearch(self,angles,a):
		"""
		Returns the two closest angles in the IES file to the angle(a) provided.
		"""
		for x in range(len(angles)):
			if a <= angles[x] and a >= angles[x-1]:
				list = [angles[x-1], angles[x]]
				return list

	def interpolationfactor(self,closest,a):
		"""
		Returns a list of the relative closeness of the angle to both of the angles in the list closest.

		Parameters: closest, contains the two closest angles two angle a
		Precondition closest: closest is a list containing two elements

		Parameters: a, angle of reference
		"""
		a = float(a)
		high = closest[1]
		low = closest[0]
		ranges = high - low

		highfactor = 1 - ((high - a) / ranges)
		lowfactor = 1 - ((a - low) / ranges)

		output = [lowfactor,highfactor]
		return output

	def quadrant(self):
		"""
		Defines the 4 closest points defined in the IES file to the objects points. Contained within in a list.
		"""
		point = self.getpoint()
		theta = point[0]
		phi = point[1]

		v = self.getverts()
		thetas = self.anglesearch(v,theta)
		self.thetarange = thetas

		h = self.gethoriz()
		phis = self.anglesearch(h,phi)
		self.phirange = phis

		quadrant = [[thetas[1],phis[0]],[thetas[1],phis[1]],[thetas[0],phis[0]],[thetas[0],phis[1]]] 

		return quadrant

	def quadraticinterpolation(self):
		"""
		Returns the factor by which to multiply each of the point 
		"""
		point = self.getpoint()
		theta = point[0]
		phi = point[1]

		quad = self.quadrant()
		thetas = self.getthetarange()
		phis = self.getphirange()

		phisf = self.interpolationfactor(phis,phi)
		thetasf = self.interpolationfactor(thetas,theta)

		return [thetasf,phisf]

	def relativity(self):
		"""
		Returns a list that contains 4 elements, each element of the list is itself a list, which contains:
		1. theta of point  2. phi of point   3. Relative linear interpolation factor
		"""
		quad = self.quadrant()
		i = self.quadraticinterpolation()
		thetafactor = i[0]
		phifactor = i[1]

		output = []
		for x in range(4):
			point = quad[x]

			if ((x % 2) == 0):
				phi = phifactor[0]
			elif ((x % 2) == 1):
				phi = phifactor[1]

			if x <= 1:
				theta = thetafactor[1]
			elif x >= 2:
				theta = thetafactor[0]

			factor = theta * phi

			list = [point[0], point[1], factor]
			output.append(list)

		return output

	def candelavalues (self):
		"""
		Returns a value corresponding to the intensity in candela that corresponds to the candela value of 
		4-points in a quadrant defined by their theta and phi.
		"""
		data = self.getdata()
		quad = self.relativity()

		output = 0
		for x in range(len(quad)):
			point = quad [x]
			theta = point[0]
			phi = point[1]
			factor = point[2]

			candelaval = data.loc[phi,theta]
			adjustedval = candelaval * factor
			output += adjustedval

		return output













	
