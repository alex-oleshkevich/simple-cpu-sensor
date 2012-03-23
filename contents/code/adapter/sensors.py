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

import os
import commands

class sensors():
	def __init__(self):
		if not self.isAvailable():
			raise Exception('Please install `lm-sensors` package or change plasmoid settings.')

	def isAvailable(self):
		return os.path.exists('/usr/bin/sensors')

	def getTemperature(self):
		sensor = commands.getoutput("sensors | grep temp1");
		sensor = sensor[sensor.find("+") + 1 : sensor.find("C") - 2];
		return int(float(sensor))