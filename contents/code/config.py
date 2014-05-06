# -*- coding: utf-8 -*-
#   Copyright 2012 Alex Oleshkevich <alex.oleshkevich@gmail.com>
#   Copyright 2014 Lyle Putnam <lcutnam@gmail.com>
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

from PyKDE4.kdecore import KConfigGroup
from PyKDE4.kdecore import KGlobal, KLocale

from PyKDE4.plasma import Plasma
from PyQt4.QtGui import QColor

##
# Configuration manager
##
class SimpleSensorConfig(KConfigGroup):
    def __init__(self, *args):
        KConfigGroup.__init__(self, *args)
        self.defaults = {
                         "normal_color": Plasma.Theme.defaultTheme().color(Plasma.Theme.TextColor),
                         "overheat_color": QColor(255,0,0),
                         "overheat_level": 80,
                         "font": Plasma.Theme.defaultTheme().font(Plasma.Theme.DefaultFont),
                         "sensor": "",
                         "interval_ms": 1000,
                         "units": KGlobal.locale().measureSystem()
                        }
    
    def readEntry(self, key, default=0):
        if self.hasKey(key) or key in self.defaults:
            return KConfigGroup.readEntry(self, key, self.defaults[key])
        else:
            return QVariant(default)