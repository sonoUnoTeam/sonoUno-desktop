# -*- coding: utf-8 -*-

import time
import wave
import os
import pygame

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
time.sleep(0.1)
_tickmark.bip()
for i in range(0,10):
    _simplesound.make_sound(0.1, 0)
    time.sleep(0.1)

#time.sleep(0.2)
#_tickmark.explosion()

_simplesound.reproductor.set_continuous()

path = os.path.abspath(os.path.dirname(__file__))
path = path + '\\testsound.wav'

rep = _simplesound.reproductor
sound_buffer=b''
base_path = os.path.abspath(os.path.dirname(__file__)) + '\\sound_module'
print(base_path)

for i in range (0,2):    
    s = pygame.mixer.Sound(os.path.join(base_path, 'sounds','bip.wav'))
    #_tickmark.bip()
    print('tickmark')
    print(s)
    sound_buffer += s.get_raw()
    for x in range (0, 10):
        freq = rep.max_freq*0.1+rep.min_freq
        print(freq)
        env = rep._adsr_envelope()
        print(env)
        f = env*rep.volume*2**15*rep.generate_waveform(freq,
            delta_t = 1)
        print(f)
        s = pygame.mixer.Sound(f.astype('int16'))
        print(s)
        sound_buffer += s.get_raw()
        print(sound_buffer)

with wave.open(path,'wb') as output_file:
    output_file.setframerate(rep.f_s)
    output_file.setnchannels(1)
    output_file.setsampwidth(2)
    output_file.writeframesraw(sound_buffer)
    #output_file.close()


time.sleep(10)
