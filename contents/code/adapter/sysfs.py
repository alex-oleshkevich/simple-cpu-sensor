# -*- coding: utf-8 -*-
#   Copyright 2012 Alex Oleshkevich <alex.oleshkevich@gmail.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License as
#   published by the Free Software Foundation; either version 2 or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#
#   GNU General Public License for more details
#
#
#   You should have received a copy of the GNU Library General Public
#   License along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#cat /sys/class/thermal/thermal_zone0/temp / 1000

import os

class sysfs():
	def __init__(self):
		self.path = '/sys/class/thermal/thermal_zone0/temp'
		
		if not self.isAvailable():
			raise Exception('Select other method from plasmoid settings.')
		
	def isAvailable(self):
		return os.path.exists(self.path)

	def getTemperature(self):
		file = open(self.path)
		return file.readline()[0:2]
