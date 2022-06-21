#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 07:52:36 2022

@author: sonounoteam

This script is dedicated to sonification based on a LHC data set
"""

import pygame
import os
from scipy.io import wavfile
import numpy as np

def sound_init():
    """
    Initializate the sound mixer with pygame to play sounds during plot display
    """
    pygame.mixer.init(44100, -16, channels = 1, buffer=4095, allowedchanges=pygame.AUDIO_ALLOW_FREQUENCY_CHANGE)

def set_bip():
    """
    Open the sound bip and store it in a global var to use it later during the
    sonification of particles. The bip represent the beginning of the particle
    track, at the center of the inner detector.
    """
    global bip
    # Set the path to open the tickmark
    bip_path = os.path.abspath(os.path.dirname(__file__)) + '/bip.wav'
    # Open the bip tickmark
    rate1, bip_local = wavfile.read(bip_path, mmap=False)
    bip = bip_local
    
def get_bip():
    return bip

def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=2000):
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
    """
    This method generate the sound of the tickmark that indicate the step from 
    the inner detector to the green calorimeter and return the array.
    """
    note_freqs = get_piano_notes()
    freqF7 = note_freqs['F7']
    bip_calorimeter = get_sine_wave(freqF7, duration=0.1)
    return bip_calorimeter

def get_cluster(amplitude):
    """
    This method generate the sound of a cluster, setting the sound amplitude 
    depending on the cluster energy, and return the array.
    """
    data = [300,350,600,800,1000,800,800,1000,700,600]
    if amplitude != 0:
        amplitude = amplitude*2000 + 100
    for x in range(0,10,1):
        signal = get_sine_wave(data[x], 0.1, amplitude=amplitude)
        if x==0:
            cluster_sound = signal
        else:
            cluster_sound = np.append(cluster_sound, signal)
    return cluster_sound

def get_silence(duration):
    """
    This method generate the sound of a silence given the duration of it and 
    return the array.
    """
    return get_sine_wave(0, duration)

def muontrack_withcluster(amplitude):
    """
    This method generate the sound of a muon track with cluster and return 
    the array. Include tickmarks indicating the beginning and transition 
    between inner detector and green calorimeter.
    """
    sound = np.append(bip, get_innersingletrack())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    cluster_track = get_cluster(amplitude) + get_innersingletrack(duration=1)
    sound = np.append(sound, cluster_track)
    sound = np.append(sound, get_innersingletrack())
    sound = np.append(sound, get_silence(0.5))
    return sound

def singletrack_withcluster(amplitude):
    """
    This method generate the sound of a single track with cluster and return 
    the array.Include tickmarks indicating the beginning and transition 
    between inner detector and green calorimeter.
    """
    sound = np.append(bip, get_innersingletrack())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    sound = np.append(sound, get_cluster(amplitude))
    return sound

def doubletrack_withcluster(amplitude):
    """
    This method generate the sound of a double track with cluster and return 
    the array. Include tickmarks indicating the beginning and transition 
    between inner detector and green calorimeter.
    """
    sound = np.append(bip, get_innerdoubletrack())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    sound = np.append(sound, get_cluster(amplitude))
    return sound

def singletrack_only():
    """
    This method generate the sound of a simple track without cluster and return 
    the array. Include tickmarks indicating the beginning and transition 
    between inner detector and green calorimeter.
    """
    sound = np.append(bip, get_innersingletrack())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    return sound

def doubletrack_only():
    """
    This method generate the sound of a double track without cluster and return 
    the array. Include tickmarks indicating the beginning and transition 
    between inner detector and green calorimeter.
    """
    sound = np.append(bip, get_innerdoubletrack())
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    return sound

def cluster_only(amplitude):
    """
    This method generate the sound of a cluster (taking in consideration the 
    cluster energy) and return the array. Include tickmarks indicating the 
    beginning and transition between inner detector and green calorimeter.
    """
    sound = np.append(bip, get_silence(2))
    sound = np.append(sound, get_tickmark_inner_calorimeter())
    sound = np.append(sound, get_cluster(amplitude))
    return sound

def play_sound(sound):
    """
    Use pygame and play the given array.
    Parameters
    ----------
    sound : array, parameter to be sonified
    """
    sound_play = pygame.mixer.Sound(sound.astype('int16'))
    sound_play.play()
    
def array_savesound(array):
    """
    Parameters
    ----------
    array : array, parameter to be saved (this overwrite the global variable 
            sound_to_save). If you want to add info to the global variable see
            add_array_savesound(array)
    """
    global sound_to_save
    sound_to_save = array
    
def add_array_savesound(array):
    """
    Parameters
    ----------
    array : array, parameter to be saved (this add the information to the global 
            variable sound_to_save). If you want to overwrite the global 
            variable see array_savesound(array)
    """
    global sound_to_save
    sound_to_save = np.append(sound_to_save, array)

def save_sound(sound_path):
    """
    Use the path provided to store the sound file in the computer
    Parameters
    ----------
    sound_path : path where to save sound in wav
    """
    wavfile.write(sound_path, rate=44100, data=sound_to_save.astype(np.int16))
    
        