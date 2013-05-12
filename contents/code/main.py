from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.kio import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyQt4 import QtCore

import os

# config tab
from configwindow import *

# config handler
from config import *

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
        self.color = self.settings.get('color', '#EEE')
        self.interval = int(self.settings.get('interval', 500))
        self.font_family = str(self.settings.get('font_family', 'Dejavu Sans'))
        self.font_size = int(self.settings.get('font_size', 10))
        self.font_weight = int(self.settings.get('font_weight', 10))
        self.units = self.settings.get('units', 'Celsius')
        
        self.overheat_level = int(self.settings.get('overheat_level', 80))
        self.overheat_color = self.settings.get('overheat_color', '#f00')

        # start timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.interval)

        self.startPolling()

    def startPolling(self):
        try:
            self.timer.start()
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

        font = QFont(str(self.settings.get('font_family', 'Dejavu Sans')), int(self.settings.get('font_size', 10)), int(int(self.settings.get('font_weight', 50))))
        # prefill fields
        self.configpage.ui.kcb_color.setColor(QColor(self.settings.get('color', '#ffffff')))
        self.configpage.ui.sb_interval.setValue(int(self.settings.get('interval', 500)))
        self.configpage.ui.sb_overheat_level.setValue(int(self.settings.get('overheat_level', 80)))
        self.configpage.ui.kcb_overheat_color.setColor(QColor(self.settings.get('overheat_color', '#ff0000')))
        self.configpage.ui.fontComboBox.setCurrentFont(font)
        self.configpage.ui.spin_size.setValue(int(self.settings.get('font_size', 10)))
        self.configpage.ui.cb_units.setCurrentIndex(self.configpage.ui.cb_units.findText(self.settings.get('units', 'Celsius')))
        self.configpage.ui.cb_units.setCurrentIndex(self.configpage.ui.cb_units.findText(self.settings.get('units', 'Celsius')))

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
        self.font_family = str(self.configpage.ui.fontComboBox.currentFont().family())
        self.font_size = int(self.configpage.ui.spin_size.value())
        self.units = str(self.configpage.ui.cb_units.currentText())
        
        # save config to settings
        self.settings.set('color', self.color)
        self.settings.set('interval', self.interval)
        self.settings.set('overheat_color', self.overheat_color)
        self.settings.set('overheat_level', self.overheat_level)
        self.settings.set('font_size', self.font_size)
        self.settings.set('font_family', self.font_family)
        self.settings.set('font_weight', self.font_weight)
        self.settings.set('units', self.units)

        # update timer
        self.timer.setInterval(self.interval)
        self.startPolling()
            
        print '[%s]: config accepted' % self._name

    def updateLabel(self):
        t = self.convertUnits(self.getTemperature(), self.units)
        
        if t > self.overheat_level:
            self.color = self.overheat_color
        else:
            self.color = self.settings.get('color', self.color)
            
        text = '<font style="color:%s;font: %dpt \'%s\';"><b>%s&deg; %s</b></font>' % (self.color, self.font_size, self.font_family, str(t), self.units[0])
        self.label.setText(text)
        
    def getTemperature(self):
        t = 0
        if os.path.exists('/sys/class/thermal/thermal_zone0/temp'):
            t = int(open('/sys/class/thermal/thermal_zone0/temp').read().strip()) / 1000
        elif os.path.exists('/proc/acpi/thermal_zone/THM0/temperature'):
            t = open("/proc/acpi/thermal_zone/THM0/temperature").read().strip().lstrip('temperature :').rstrip(' C')
        elif os.path.exists('/proc/acpi/thermal_zone/THRM/temperature') :
            t = open("/proc/acpi/thermal_zone/THRM/temperature").read().strip().lstrip('temperature :').rstrip(' C')
        elif os.path.exists('/proc/acpi/thermal_zone/THRM/temperature') :
            t = open("/proc/acpi/thermal_zone/THRM/temperature").read().strip().lstrip('temperature :').rstrip(' C')
        elif os.path.exists('/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp') :
            t = open("/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp").read().strip().rstrip('000')
        elif os.path.exists('/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp') :
            t = open("/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp").read().strip().rstrip('000')
            t = str(float(t)/10.0)
            
        return t
    
    def convertUnits(self, value, unit):
        if unit == "Fahrenheit":
            return value * 9/5.0 + 32
        else:
            return value
    
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