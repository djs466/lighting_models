"""
Program to convert cartesian coordinates to spherical coordinates

By: Daniel Santander
Started: March 16th
Completed: Aprtil 14th
"""
import first
import math


class point (object):
	"""
	The provided point with accompanying functions to return lighting data given the point.
	
	Instance Attributes:
		x: the x coordinate of the provided point. With the origin starting where phi = 180 
		y: the y coordinate of the provided point. With the origin starting where phi = 180
			larger values indicate a greater distance below the SSL product so they are in the 
			relative negative direction, but for simplicity the negative was omitted.
		z: the z coordinate of the provided point. With the origin starting where phi = 90
		Theta: Vertical angles. the value for theta in degrees. the values start directionally above the origin
			  and precede down a lateral arc so that 180 degrees is immediately under the reference origin
		Phi: Horizontal angles. the value for phi in degrees, the values range from 0 - 360 degrees. 0 is in the positive
			direction of the x-axis, 90 is in the positive direction of the y-axis, 180 is in the negative direction of the x-axis,
			and 270 is in the negative direction of the y-axis.
	
	Invariants:
		Theta (vertical angles) must be less than 180 and phi (horizontal angles) must be within 0-360.
	"""
	def __init__ (self,x,y,z):
		"""
		Sets up instance attributes of the class

		Precondition X: positive or negative
		Precondition Y: positive or negative 
		Precondition Z: must be greater than 0
		"""
		x = float(x)
		y = float(y)
		z = float(z)

		self.x = x
		self.y = y
		self.z = z 

	def getx(self):
		return self.x
	def gety(self):
		return self.y
	def getz(self):
		return self.z


	def thetaphi(self):
		x = self.getx()
		y = self.gety()
		z = self.getz()

		r2 = (x ** 2) + (y ** 2) + (z ** 2)
		r = math.sqrt(r2)

		theta = math.acos(z/r)
		theta = (theta * 360) / (2 * math.pi)
		iestheta = 180 - theta


		l2 = (x ** 2) + (y ** 2)
		l = math.sqrt(l2)

		if x == 0 and y != 0:
			phi = math.asin(y/l)
		elif y == 0 and x != 0:
			phi = math.acos(x/l)
		elif l == 0:
			phi = 0
		else:
			phi = math.acos(x/l)

		phi = (phi * 360) / (2 * math.pi)

		return [iestheta,phi,r]





