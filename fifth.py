"""

By: Daniel Santander
Started: April 19th, 2019
Completed:
"""

import third
import second
import first
import math


class illuminance (object):
	"""
	Invariants:
		point: point defined by a theta, phi, and r value all of which are (floats).
		verts: (list) of vertical angles in the dataset
		horiz: (list) of horizontal angles in the dataset
		data: the data set (pd data frame)
		candela: (float) candela value at the provided point caluclated with class third.
	"""
	def __init__ (self,x,y,z,file):
		"""
		Intializes an instance of a linear illuminance object

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
		self.setintensity(x,y,z,file)


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
	def getintensity(self):
		return self.intensity

	def setintensity(self,x,y,z,file):
		a = third.li(x,y,z,file)
		self.intensity = a.candelavalues()

	def E(self):
		"""
		returns the emissitivity of the coordinate
		"""
		theta = self.getpoint()[0]
		if theta > 90:
			theta -= 90
		theta = (theta / 360) * (2 * math.pi)
		angle = math.cos(theta)

		d = self.getpoint()[2]
		d2 = (d ** d)

		i = self.getintensity()

		e = (i/d2) * angle

		return e










