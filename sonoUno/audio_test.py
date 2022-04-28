# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

sample_rate = 44100
amplitude = 4096
duration = 2
frequency = 440
t = np.linspace(0, duration, int(sample_rate*duration)) # Time axis
sin_wave = amplitude*np.sin(2*np.pi*frequency*t)
t2 = np.linspace(0.1, duration, int(sample_rate*duration))
sin_wave2 = amplitude*np.sin(2*np.pi*frequency*t2)

sin_wave = sin_wave + sin_wave2

fig, ax1 = plt.subplots()
#fig, (ax1,ax2) = plt.subplots(1,2)
ax1.plot(t, sin_wave)
ax1.set(xlabel='time (s)', ylabel='Amplitude',
       title='Sine wave')
#ax1.set_xlim(0,0.1)
ax1.grid()
#
#ax2.plot(t2, sin_wave2)
#ax2.set(xlabel='time (s)', ylabel='Amplitude',
#       title='Sine wave')
#ax2.set_xlim(0.1,0.2)
#ax2.grid()

#fig.savefig("test.png")
plt.show()

# Set the path to save the sound
path = os.path.abspath(os.path.dirname(__file__))
path = path + '/sound.wav'
# Generate the wav file with the sonification
wavfile.write(path, rate=44100, data=sin_wave2.astype(np.int16))