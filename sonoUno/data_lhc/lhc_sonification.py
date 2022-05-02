#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 07:52:36 2022

@author: sonounoteam
"""

import pygame
import os
from scipy.io import wavfile
import numpy as np

def sound_init():
    # Initializate sound
    pygame.mixer.init(44100, -16, channels = 1, buffer=4095, allowedchanges=pygame.AUDIO_ALLOW_FREQUENCY_CHANGE)

def set_bip():
    global bip
    # Set the path to open the tickmark
    bip_path = os.path.abspath(os.path.dirname(__file__)) + '/bip.wav'
    # Open the bip tickmark
    rate1, bip_local = wavfile.read(bip_path, mmap=False)
    bip = bip_local

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

def get_innersingletrack(duration=2):
    """
    This method generate the sound of a track and return the array.
    """
    note_freqs = get_piano_notes()
    freqD6 = note_freqs['D6']
    track_sound = get_sine_wave(freqD6, duration)
    return track_sound

def get_innerdoubletrack(duration=2):
    """
    This method generate the sound of a double track and return the array.
    """
    note_freqs = get_piano_notes()
    freqC6 = note_freqs['C6']
    freqD6 = note_freqs['D6']
    double_track_sound = (get_sine_wave(freqD6, duration) 
                          + get_sine_wave(freqC6, duration)
                          )
    return double_track_sound

def get_tickmark_inner_calorimeter(freq=440, duration=0.1):
    note_freqs = get_piano_notes()
    freqF7 = note_freqs['F7']
    bip_calorimeter = get_sine_wave(freqF7, duration=0.1)
    return bip_calorimeter

def get_cluster():
    # Obtain a generic cluster sound
    data = [300,350,600,800,1000,800,800,1000,700,600]
    for x in range(0,10,1):
        signal = get_sine_wave(data[x], 0.1)
        if x==0:
            cluster_sound = signal
        else:
            cluster_sound = np.append(cluster_sound, signal)

def get_silence_2s():
    return get_sine_wave(0, duration=2)

def get_silence_1s():
    return get_sine_wave(0, duration=1)

def muontrack_withcluster():
    sound = np.append(bip, get_innersingletrack())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    cluster_track = get_cluster() + get_innersingletrack(duration=1)
    sound = np.append(sound, cluster_track)
    sound = np.append(sound, get_innersingletrack())
    return sound

def singletrack_withcluster():
    sound = np.append(bip, get_innersingletrack())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    sound = np.append(sound, get_cluster())
    return sound

def doubletrack_withcluster():
    sound = np.append(bip, get_innerdoubletrack())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    sound = np.append(sound, get_cluster())
    return sound

def singletrack_only():
    sound = np.append(bip, get_innersingletrack())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    return sound

def doubletrack_only():
    sound = np.append(bip, get_innerdoubletrack())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    return sound

def cluster_only():
    sound = np.append(bip, get_silence_2s())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    sound = np.append(sound, get_cluster())
    return sound

def play_sound(sound):
    sound_play = pygame.mixer.Sound(sound.astype('int16'))
    sound_play.play()
    
def array_savesound(array):
    global sound_to_save
    sound_to_save = array
    
def add_array_savesound(array):
    global sound_to_save
    sound_to_save = np.append(sound_to_save, array)

def save_sound(sound_path):
    wavfile.write(sound_path, rate=44100, data=sound_to_save.astype(np.int16))
    
        