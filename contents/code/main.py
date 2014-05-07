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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.kio import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdecore import KLocale

import os

# config tab
from configwindow import *

# config handler
from config import *

class CPUTemp(plasmascript.Applet):
    def __init__(self,parent, args=None):
        plasmascript.Applet.__init__(self,parent)
        
    def init(self):
        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        self.label = Plasma.Label(self.applet)
        self.layout.addItem(self.label)
        self.applet.setLayout(self.layout)
        self.settings = SimpleSensorConfig(self.config(), self.pluginName)
        
        self.engine = self.dataEngine("systemmonitor")
        
        self.engine.sourceAdded.connect(self.sourceAdded)
        self.engine.sourceRemoved.connect(self.sourceRemoved)
        
        self.source = self.settings.readEntry("sensor").toString()
        
        self.setHasConfigurationInterface(True)
        self.start()

    # FIXME: @pyqtSlot is preferred, but I can't find a way to make it work here.
    @pyqtSignature("dataUpdated(const QString &, const Plasma::DataEngine::Data &)")
    def dataUpdated(self, source, data):
        try:
            name = data[QString('name')]
            (temp, ok) = data[QString('value')].toFloat()
            if ok:
                self.updateLabel(name, temp)
        # NOTE: Sometimes the value isn't available right away. That's not really a problem.
        except KeyError:
            pass
    
    @pyqtSlot(str)
    def sourceAdded(self, source):
        if source == self.source:
            self.start()
            
    @pyqtSlot(str)
    def sourceRemoved(self, source):
        if source == self.soruce:
            self.engine.disconnectSource(self.source, self)
    
    def connectToSource(self):
            self.engine.connectSource(self.source, self, self.settings.readEntry("interval_ms").toPyObject())
    
    def start(self):
        if not self.source:
            self.setConfigurationRequired(True)
            self.showTooltip("<b>Select a sensor from the configuration dialog</b>")
        elif self.source:
            self.setConfigurationRequired(False)
            self.connectToSource()
        
    # ---------------------- configuration ------------------------#
    def createConfigurationInterface(self, parent):
        self.configpage = ConfigWindow(self, self.settings, self.engine)

        # add config page
        page = parent.addPage(self.configpage, i18n(self.name()))
        page.setIcon(KIcon(self.icon()))

        parent.okClicked.connect(self.configAccepted)
        parent.applyClicked.connect(self.configAccepted)


    # show configuration window
    def showConfigurationInterface(self):
        plasmascript.Applet.showConfigurationInterface(self)
    
      # if config accepted
    def configAccepted(self):
        font = self.configpage.ui.fontComboBox.currentFont()
        font.setPointSize(int(self.configpage.ui.spin_size.value()))
        self.settings.writeEntry("font", font)
        self.settings.writeEntry("interval_ms", self.configpage.ui.sb_interval.value())
        self.settings.writeEntry("overheat_level", self.configpage.ui.sb_overheat_level.value())
        self.settings.writeEntry("normal_color", self.configpage.ui.kcb_color.color())
        self.settings.writeEntry("overheat_color", self.configpage.ui.kcb_overheat_color.color())
        self.settings.writeEntry("sensor", self.configpage.ui.sensor_device.currentText())
        
        if self.settings.readEntry("sensor").toString():
            if self.source:
                self.engine.disconnectSource(self.source, self)
            self.source = self.settings.readEntry("sensor").toString()

        self.start()
    
    def updateLabel(self, label, temp):
        (value,units) = self.convertUnits(temp, KLocale.MeasureSystem(self.settings.readEntry("units").toPyObject()))
        
        font = self.settings.readEntry('font').toPyObject()
        if value > self.settings.readEntry('overheat_level').toPyObject():
            color = QColor(self.settings.readEntry('overheat_color'))
        else:
            color = QColor(self.settings.readEntry('normal_color'))
            
        print font.family()
        
        #TODO: format specification in config dialog.
        text = '<font style="color:%s;font: %dpt \'%s\';"><b>%s&deg; %s</b></font>' % (color.name(), font.pointSize(), font.family(), str(value), units)
        
        self.label.setText(text)
        self.showTooltip("<b>Temperature</b><br />%s: %0.2f&deg;%s" % (label, value, units))
    
    def convertUnits(self, value, system):
        if system == KLocale.Imperial:
            return (value * 9/5.0 + 32, "F")
        else:
            return (value, "C")
    
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