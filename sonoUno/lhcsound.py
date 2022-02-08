# -*- coding: utf-8 -*-

import time
from sound_module.simple_sound import tickMark
from sound_module.simple_sound import simpleSound


_tickmark = tickMark()
_simplesound = simpleSound()

_simplesound.reproductor.set_continuous()
_simplesound.reproductor.set_waveform('celesta')

_tickmark.bip()
time.sleep(0.2)
for i in range(0,10):
    _simplesound.make_sound(0.1, 0)
    time.sleep(0.1)
    print(i)
time.sleep(0.1)
_tickmark.bip()
for i in range(0,10):
    _simplesound.make_sound(0.1, 0)
    time.sleep(0.1)
    print(i)

#time.sleep(0.2)
#_tickmark.explosion()


time.sleep(1)
