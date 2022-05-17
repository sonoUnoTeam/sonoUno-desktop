import lhc_sonification as s
import pygame
import numpy as np
import time

"""
This script was used to test the values of amplitud related to the volume
feature of the sound.
"""

s.sound_init()

note=s.get_sine_wave(440,1,amplitude=100)
sou=np.append(note,s.get_sine_wave(440,1,amplitude=500))
sou=np.append(sou,s.get_sine_wave(440,1,amplitude=1000))
sou=np.append(sou,s.get_sine_wave(440,1,amplitude=2000))

sound=pygame.mixer.Sound(sou.astype('int16'))
sound.play()

time.sleep(5)
