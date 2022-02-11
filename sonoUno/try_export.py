# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 11:13:42 2022

@author: johi-
"""

import time
from data_export.data_export import DataExport
from sound_module.simple_sound import simpleSound
from sound_module.simple_sound import tickMark

_dataexport = DataExport(False)
_tick = tickMark()

_tick.loop()
print('loop')
time.sleep(1)