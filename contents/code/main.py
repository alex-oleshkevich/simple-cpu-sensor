# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyQt4 import QtCore
import commands

class CPUTemp(plasmascript.Applet):
	def __init__(self,parent,args=None):
		plasmascript.Applet.__init__(self,parent)

	def init(self):
		self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
		self.label = Plasma.Label(self.applet)
		self.label.setText("Init")
		self.layout.addItem(self.label)
		self.applet.setLayout(self.layout)
		self.resize(80, 20)
		
		self.timer = QtCore.QTimer()
		self.timer.setInterval(500)
		self.timer.start(1000)
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateLabel)
		
		self.updateLabel()

	def updateLabel(self):
		color = 'blue'
		
		sensor = commands.getoutput("sensors | grep temp1");
		sensor = sensor[sensor.find("+")+1:sensor.find("C")-2];

		t = int(float(sensor))
		
		'''f = open('/proc/acpi/thermal_zone/THRM/temperature', 'r')
		t = f.read()
		t = int(t.replace('temperature:', '').replace('C', '')); '''

		if(t > 75 and t < 80):
			color = 'white'
		elif(t > 80):
			color = 'red'
		else:
			color = 'white'
	
		self.label.setText('<font color="' + color + '"><b>' + str(t) + "&deg; C</b></font>")

def CreateApplet(parent):
	return CPUTemp(parent)