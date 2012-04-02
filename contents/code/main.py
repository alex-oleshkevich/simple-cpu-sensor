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
#
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.kio import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyQt4 import QtCore

import commands

# config tab
from configwindow import *

# config handler
from config import *

from util import *

class CPUTemp(plasmascript.Applet):
	def __init__(self,parent, args=None):
		plasmascript.Applet.__init__(self,parent)
		
	def init(self):
		self._name = str(self.package().metadata().pluginName())
		self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
		self.setHasConfigurationInterface(True)
		
		self.label = Plasma.Label(self.applet)
		self.label.setText("N\A")
		self.layout.addItem(self.label)
		self.applet.setLayout(self.layout)

		# Setup configuration
		self.settings = Config(self)
		self.color = self.settings.get('color', '#fff')
		self.interval = int(self.settings.get('interval', 500))
		self.method = self.settings.get('method', 'sysfs')

		self.overheat_level = int(self.settings.get('overheat_level', 80))
		self.overheat_color = self.settings.get('overheat_color', '#f00')
		self.units = self.settings.get('units', 'Celsius')

		# start timer
		self.timer = QtCore.QTimer()
		self.timer.setInterval(self.interval)

		self.startPolling()

	def startPolling(self):
		try:
			self.timer.start(1000)
			QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateLabel)

			# update temp label
			self.updateLabel()
			self.showTooltip('')
		except Exception as (strerror):
			self.showTooltip(str(strerror))
			self.label.setText('<font color="red">ERROR</font>')
			return
		
	# ---------------------- configuration ------------------------#
	def createConfigurationInterface(self, parent):
		self.configpage = ConfigWindow(self, self.settings)

		# prefill fields
		self.configpage.ui.kcb_color.setColor(QColor(self.settings.get('color', '#ffffff')))
		self.configpage.ui.sb_interval.setValue(int(self.settings.get('interval', 500)))
		self.configpage.ui.sb_overheat_level.setValue(int(self.settings.get('overheat_level', 80)))
		self.configpage.ui.kcb_overheat_color.setColor(QColor(self.settings.get('overheat_color', '#ff0000')))

		# add config page
		page = parent.addPage(self.configpage, i18n(self.name()))
		page.setIcon(KIcon(self.icon()))

		parent.okClicked.connect(self.configAccepted)

	# show configuration window
	def showConfigurationInterface(self):
		plasmascript.Applet.showConfigurationInterface(self)

	# if config accepted
	def configAccepted(self):
		# update local variables
		self.color = str(self.configpage.ui.kcb_color.color().name())
		self.interval = int(self.configpage.ui.sb_interval.value())
		self.overheat_level = int(self.configpage.ui.sb_overheat_level.value())
		self.overheat_color = str(self.configpage.ui.kcb_overheat_color.color().name())

		# save config to settings
		self.settings.set('color', self.color)
		self.settings.set('interval', self.interval)
		self.settings.set('overheat_color', self.overheat_color)
		self.settings.set('overheat_level', self.overheat_level)

		# update timer
		self.timer.setInterval(self.interval)
		self.startPolling()
			
		print '[%s]: config accepted' % self._name

	def updateLabel(self):
		file = open('/sys/class/thermal/thermal_zone0/temp')
		t = int(file.readline()) / 1000

		if t > self.overheat_level:
			self.color = self.overheat_color
		else:
			self.color = self.settings.get('color', self.color)

		self.label.setText('<font style="color:' + self.color + '"><b>' + str(t) + '&deg; C</b></font>')

	def showTooltip(self, text):
			# create and set tooltip
			tooltip = Plasma.ToolTipContent()
			tooltip.setImage(KIcon(self.icon()))
			tooltip.setSubText(text)
			tooltip.setAutohide(False)
			Plasma.ToolTipManager.self().setContent(self.applet, tooltip)
			Plasma.ToolTipManager.self().registerWidget(self.applet)
		
def CreateApplet(parent):
	return CPUTemp(parent)