# -*- coding: utf-8 -*-

import time
import os
import numpy as np
from scipy.io import wavfile

"""
Functions to be added in simple sound later
"""
def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
    """
    Parameters
    ----------
    frequency : float, frequency of the sine wave
    duration : float, duration of the sound
    sample_rate : int, optional: The default is 44100.
    amplitude : int, optional: The default is 4096.
    
    Returns
    -------
    sin_wave : np.array of the sound wave.
    
    """
    t = np.linspace(0, duration, int(sample_rate*duration)) # Time axis
    sin_wave = amplitude*np.sin(2*np.pi*frequency*t)
    return sin_wave

def get_piano_notes():
    """
    Return the frequency of each 88 piano keys (A0-C8).
    ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    In the code you can use:
        freq_array = get_piano_notes()
        freq_of_C4 = freq_array['C4']

    """
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    base_freq = 440 #Frequency of Note A4
    keys = np.array([x+str(y) for y in range(0,9) for x in octave])
    # Trim to standard 88 keys
    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]
    
    note_freqs = dict(zip(keys, [2**((n+1-49)/12)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0 # stop
    return note_freqs

def sonify_muon_WP5():
    """
    1) bip: the beginning of the detector
    2) continuous sound during 2 seconds: the track in the inner detector
    3) a tone with different frequency: change from inner detector to red calorimeter
    4) continuous sound during 4 second: the track continues passing the detectors, it represents a muon.  

    """
    # Set the path to save the sound
    path = os.path.abspath(os.path.dirname(__file__))
    path = path + '/muon_sound.wav'
    # Set the path to open the tickmark
    bip_path = os.path.abspath(os.path.dirname(__file__)) + '/sound_module/sounds/bip.wav'
    #
    note_freqs = get_piano_notes()
    freqD6 = note_freqs['D6']
    freqF7 = note_freqs['F7']
    # Obtain pure sine wave for each frequency
    sine_wave_D6 = get_sine_wave(freqD6, duration=2)
    sine_wave_F7 = get_sine_wave(freqF7, duration=0.1)
    sine_wave_D6_4 = get_sine_wave(freqD6, duration=4)
    # Open the bip tickmark
    rate1, data1 = wavfile.read(bip_path, mmap=False)
    # Generate the final numpy array with all the sounds arrays
    sound = np.append(data1, sine_wave_D6)
    sound = np.append(sound, sine_wave_F7)
    sound = np.append(sound, sine_wave_D6_4)
    # Generate the wav file with the sonification
    wavfile.write(path, rate=44100, data=sound.astype(np.int16))
    
def sonify_electron_WP5():
    """
    1) bip: the beginning of the detector
    2) continuous sound during 2 seconds: the track in the inner detector
    3) a tone with different frequency: change from inner detector to red calorimeter
    4) sound corresponding to the cluster
    
    """
    # Set the path to save the sound
    path = os.path.abspath(os.path.dirname(__file__))
    path = path + '/electron_sound.wav'
    # Set the path to open the tickmark
    bip_path = os.path.abspath(os.path.dirname(__file__)) + '/sound_module/sounds/bip.wav'
    #
    note_freqs = get_piano_notes()
    freqD6 = note_freqs['D6']
    freqF7 = note_freqs['F7']
    # Obtain pure sine wave for each frequency
    sine_wave_D6 = get_sine_wave(freqD6, duration=2)
    sine_wave_F7 = get_sine_wave(freqF7, duration=0.1)
    # sine_wave_D6_4 = get_sine_wave(freqD6, duration=4)
    data = [300,350,600,800,1000,800,800,1000,700,600]
    for x in range(0,10,1):
        signal = get_sine_wave(data[x], 0.1)
        if x==0:
            cluster_sound = signal
        else:
            cluster_sound = np.append(cluster_sound, signal)
    # Open the bip tickmark
    rate1, data1 = wavfile.read(bip_path, mmap=False)
    # Generate the final numpy array with all the sounds arrays
    sound = np.append(data1, sine_wave_D6)
    sound = np.append(sound, sine_wave_F7)
    sound = np.append(sound, cluster_sound)
    # Generate the wav file with the sonification
    wavfile.write(path, rate=44100, data=sound.astype(np.int16))
    
def sonify_muon_WP6():
    """
    1) a tone with an specific frequency if the muon track match with (signal)?
    2) continuous sound during 1 seconds: the track between first and second plot
    3) a tone with the same frequency of 1) if the muon track match with (signal)?
    4) continuous sound during 1 seconds: the track between second and third plot
    5) a tone with the same frequency of 1) if the muon track match with (signal)?
    6) continuous sound during 1 seconds: the muon track continue

    """
    # Set the path to save the sound
    path = os.path.abspath(os.path.dirname(__file__))
    path = path + '/not_muon_sound_WP6.wav'
    #
    note_freqs = get_piano_notes()
    freqD6 = note_freqs['D6']
    freqF7 = note_freqs['F7']
    # Obtain pure sine wave for each frequency
    sine_wave_D6 = get_sine_wave(freqD6, duration=1)
    sine_wave_F7 = get_sine_wave(freqF7, duration=0.1)
    # Generate the final numpy array with all the sounds arrays
    sound = np.append(sine_wave_F7, sine_wave_D6)
    sound = np.append(sound, sine_wave_F7)
    sound = np.append(sound, sine_wave_D6)
    sound = np.append(sound, sine_wave_F7)
    sound = np.append(sound, sine_wave_D6)
    # Generate the wav file with the sonification
    wavfile.write(path, rate=44100, data=sound.astype(np.int16))

sonify_electron_WP5()

"""
calculates the square root of ( (φtrack-φcluster)squared+(θtrack-θcluster) squared)).
If the track(s) point in 3-D to a cluster this value should be small* (<0.1?). 
Then if it is below the cut you play a "cluster" sound simultaneous with the "track(s)" cluster.
"""


