# -*- coding: utf-8 -*-
#   Copyright 2012 Alex Oleshkevich <alex.oleshkevich@gmail.com>
#
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
#

from util import *

##
# Configuration manager
##
class Config():
	def __init__(self, applet):
		self.applet = applet
		self.config = self.applet.config()
		
	##
	# Read option from configuration file
	#
	# @param key string The option name
	# @param default mixed The default value if option is not found 
	# @param section string [optional] The section to write in
	# @return int|string The value
	def get(self, key, default = ''):
		return self.config.readEntry(key, default).toString()

	##
	# Set option to configuration file
	#
	# @param key string The option name
	# @param value mixed The value to set
	# @return void
	def set(self, key, value):
		self.config.writeEntry(key, value)