# -*- coding: utf-8 -*-
#   Copyright 2012 Alex Oleshkevich <alex.oleshkevich@gmail.com>
#   Copyright 2014 Lyle Putnam   <lcputnam@gmail.com>
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
# NOTE: I am uncertain of the copyright status of this file. The original author
#       did _not_ include this notification. I have modified it heavily and wish
#       to apply the same license as the other files, and have assumed that the
#       original author has asserted this copyright.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import *
from PyQt4 import uic
from PyKDE4 import plasmascript
from PyKDE4.kdecore import KLocale

class ConfigWindow(QWidget):
    def __init__(self, parent, settings, engine):
        QWidget.__init__(self)
        self.ui = uic.loadUi(parent.package().filePath('ui', 'configwindow.ui'), self)
        self.parent = parent
        self.settings = settings
        self.engine = engine
        
        font = QFont(self.settings.readEntry("font"))
        
        self.ui.sb_overheat_level.setValue(self.settings.readEntry("overheat_level").toPyObject())
        self.ui.sb_interval.setValue(self.settings.readEntry("interval_ms").toPyObject())
        self.ui.fontComboBox.setCurrentFont(font)
        self.ui.spin_size.setValue(font.pointSize())
        self.ui.sensor_device.addItems(engine.sources().filter("lmsensors"))
        self.ui.kcb_color.setColor(QColor(self.settings.readEntry("normal_color")))
        self.ui.kcb_overheat_color.setColor(QColor(self.settings.readEntry("overheat_color")))
        
        sensor = self.settings.readEntry("sensor").toString()
        print sensor
        if len(sensor):
            self.ui.sensor_device.setCurrentIndex(self.ui.sensor_device.findText(sensor))
            
        units = KLocale.MeasureSystem(self.settings.readEntry("units").toPyObject())
        if units ==  KLocale.Metric:
            self.ui.cb_units.setCurrentIndex(self.ui.cb_units.findText("Celsius"))
        else:
            self.ui.cb_units.setCurrentIndex(self.ui.cb_units.findText("Fahrenheit"))
        