# -*- coding: utf-8 -*-

import time
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import math
import pygame

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
    
def make_a_cluster(phi,theta,eta,amplitud=1):
    """
    Hago una esfera
    """
    if np.abs(eta) < 1.5:
        r = 150
    else:
        r = 210
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 10 * np.outer(np.cos(u), np.sin(v)) + x
    y = 10 * np.outer(np.sin(u), np.sin(v)) + y
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v)) + z
    # ax.plot_surface(x, y, z, color='b')
    # Corte longitudinal
    ax_longitudinal.plot_surface(z, y, x, color='b')
    ax_transversal.plot_surface(x, y, z, color='b')

def particles_sonification(track_list, cluster_list):
    ax_longitudinal.cla()
    ax_transversal.cla()
    ax_transversal.set_xlabel('$X$')
    ax_transversal.set_ylabel('$Y$')
    ax_transversal.set_zlabel('$Z$')
    ax_longitudinal.set_xlabel('$Z$')
    ax_longitudinal.set_ylabel('$Y$')
    ax_longitudinal.set_zlabel('$X$')
    ax_transversal.set_xlim([-150,150])
    ax_transversal.set_ylim([-150,150])
    ax_transversal.set_zlim([-150,150])
    ax_longitudinal.set_xlim([-300,300])
    ax_longitudinal.set_ylim([-300,300])
    ax_longitudinal.set_zlim([-300,300])
    # Corte transversal
    ax_transversal.view_init(90, 270)
    ax_longitudinal.view_init(90, 270)
    # With each track calculate if it points out a cluster or not, if points a
    # cluster we will sonify the track and the cluster
    count = 0
    count_colors = 0
    sonified_cluster_list = []
    sonified_tracks_list = []
    cluster_tosonify = []
    converted_photon = ' '
    track_list_2 = track_list.copy()
    # Variable to store all sound to save at the end
    #sound_to_save = np.empty([0,0])
    for track in track_list:
        #plot the track
        track_elements = str(track).split()
        count = count + 1
        if not track_elements[0] in sonified_tracks_list:
            if int(track_elements[11])==1:
                ax_transversal.plot3D(
                    [float(track_elements[-6]),float(track_elements[-3])*2.5],
                    [float(track_elements[-5]),float(track_elements[-2])*2.5],
                    [float(track_elements[-4]),float(track_elements[-1])*2.5],
                    plot_colours[count_colors])
                # Corte longitudinal
                ax_longitudinal.plot3D(
                    [float(track_elements[-4]),float(track_elements[-1])*2.5],
                    [float(track_elements[-5]),float(track_elements[-2])*2.5],
                    [float(track_elements[-6]),float(track_elements[-3])*2.5],
                    plot_colours[count_colors])
                count_colors = count_colors + 1
            else:
                ax_transversal.plot3D(
                    [float(track_elements[-6]),float(track_elements[-3])],
                    [float(track_elements[-5]),float(track_elements[-2])],
                    [float(track_elements[-4]),float(track_elements[-1])],
                    plot_colours[count_colors])
                # Corte longitudinal
                ax_longitudinal.plot3D(
                    [float(track_elements[-4]),float(track_elements[-1])],
                    [float(track_elements[-5]),float(track_elements[-2])],
                    [float(track_elements[-6]),float(track_elements[-3])],
                    plot_colours[count_colors])
                count_colors = count_colors + 1
            # check if there are a track very close
            if count < len(track_list):
                for track2 in track_list_2[count:]:
                    track2_elements = str(track2).split()
                    value_tracks = math.sqrt(
                        pow(
                            (float(track_elements[4])-float(track2_elements[4])),
                            2) 
                        + pow(
                            (float(track_elements[5])-float(track2_elements[5])),
                            2)
                        )
                    if value_tracks < 0.02:
                        if not track2_elements[0] in sonified_tracks_list:
                            sonified_tracks_list.append(track2_elements[0])
                        ax_transversal.plot3D(
                            [float(track2_elements[-6]),float(track2_elements[-3])],
                            [float(track2_elements[-5]),float(track2_elements[-2])],
                            [float(track2_elements[-4]),float(track2_elements[-1])],
                            plot_colours[count_colors])
                        # Corte longitudinal
                        ax_longitudinal.plot3D(
                            [float(track2_elements[-4]),float(track2_elements[-1])],
                            [float(track2_elements[-5]),float(track2_elements[-2])],
                            [float(track2_elements[-6]),float(track2_elements[-3])],
                            plot_colours[count_colors])
                        count_colors = count_colors + 1
                        converted_photon = track2_elements[0]
            for cluster in cluster_list:
                cluster_elements = str(cluster).split()
                value = math.sqrt(
                    pow(
                        (float(track_elements[4])-float(cluster_elements[4])),
                        2) 
                    + pow(
                        (float(track_elements[5])-float(cluster_elements[5])),
                        2)
                    )
                if value < 0.07:
                    if not cluster_elements[0] in sonified_cluster_list:
                        sonified_cluster_list.append(cluster_elements[0])
                    make_a_cluster(
                        phi=float(track_elements[4]),
                        theta=float(track_elements[5]),
                        eta=float(track_elements[6]))
                    cluster_tosonify.append(cluster)
            """
            Plot and sonification of the tracks
            """
            plt.pause(0.5)
            if cluster_tosonify:
                # The track point out a cluster
                if len(cluster_tosonify) > 1:
                    print('Could a track points out to more than one cluster?')
                    break
                cluster_elements = str(cluster_tosonify[0]).split()
                if converted_photon == ' ':
                    print('Sonifying '+track_elements[0]+' and '+cluster_elements[0])
                    sound = np.append(bip, track_sound)
                    sound = np.append(sound, bip_calorimeter)
                    if int(track_elements[11])==1:
                        cluster_track = cluster_sound + track_1s
                        sound = np.append(sound, cluster_track)
                        sound = np.append(sound, track_1s)
                    else:
                        sound = np.append(sound, cluster_sound)  
                else:
                    print('Sonifying '+track_elements[0]+', '+converted_photon+' and '+cluster_elements[0])
                    sound = np.append(bip, double_track_sound)
                    sound = np.append(sound, bip_calorimeter)
                    sound = np.append(sound, cluster_sound)
                    # if count == 1:
                    #     sound_to_save = sound
                    # else:
                    #     sound_to_save = np.append(sound_to_save, sound)
            else:
                # The track don't point out a cluster
                print('Sonifying '+track_elements[0])
                sound = np.append(bip, track_sound)
                sound = np.append(sound, bip_calorimeter)
                if int(track_elements[11])==1:
                    sound = np.append(sound, track_sound)
                # if count == 1:
                #     sound_to_save = sound
                # else:
                #     sound_to_save = np.append(sound_to_save, sound)
            sound_play = pygame.mixer.Sound(sound.astype('int16'))
            sound_play.play()
            if count == 1:
                sound_to_save = sound
            else:
                sound_to_save = np.append(sound_to_save, sound)
            sound_to_save = np.append(sound_to_save, silence_1s)
            
            if int(track_elements[11])==1:
                time.sleep(4.5)
            else:
                time.sleep(3)
            
            cluster_tosonify = []
            converted_photon = ' '
            
    for cluster in cluster_list:
        cluster_elements = str(cluster).split()
        if not cluster_elements[0] in sonified_cluster_list:
            make_a_cluster(
                phi=float(cluster_elements[4]),
                theta=float(cluster_elements[5]),
                eta=float(cluster_elements[6]))
            plt.pause(0.5)
            print('Sonifying '+cluster_elements[0])
            sound = np.append(bip, silence_2s)
            sound = np.append(sound, bip_calorimeter)
            sound = np.append(sound, cluster_sound)
            sound_play = pygame.mixer.Sound(sound.astype('int16'))
            sound_play.play()
            sound_to_save = np.append(sound_to_save, sound)
            sound_to_save = np.append(sound_to_save, silence_1s)
            time.sleep(3)
    return sound_to_save

#sonify_electron_WP5()

"""
calculates the square root of ( (φtrack-φcluster)squared+(θtrack-θcluster) squared)).
If the track(s) point in 3-D to a cluster this value should be small* (<0.1?). 
Then if it is below the cut you play a "cluster" sound simultaneous with the "track(s)" cluster.
"""
"""
Plot init
"""
# figure, (ax_transversal, ax_longitudinal) = plt.subplots(1, 2)
# # Defining the axes as a 3D axes so that we can plot 3D data into it.
# ax_transversal = plt.axes(projection="3d")
# ax_longitudinal = plt.axes(projection="3d")

# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))
# =============
# First subplot
# =============
# set up the axes for the first plot
ax_transversal = fig.add_subplot(1, 2, 1, projection='3d')
ax_transversal.set_xlim([-250,250])
ax_transversal.set_ylim([-250,250])
ax_transversal.set_zlim([-250,250])
# ==============
# Second subplot
# ==============
# set up the axes for the second plot
ax_longitudinal = fig.add_subplot(1, 2, 2, projection='3d')
ax_longitudinal.set_xlim([-250,250])
ax_longitudinal.set_ylim([-250,250])
ax_longitudinal.set_zlim([-250,250])

plot_colours = ['blue','orange','green','red','purple','brown','pink','grey','olive','cyan']
"""
Particle data file
"""
# First open the file and store it.
file1 = open('sonification_reduced.txt','r')
lines = file1.readlines()
# Search the separator on the file and store the index where each event begin
count = 0
element_list = [0]
for line in lines:
    count = count + 1
    if '---------' in str(line) and count <= len(lines):
        element_list.append(count)
# Generate a list of tracks and clusters of the first event
count = 0
particles = []
particles_1_tracks = []
particles_1_clusters = []
# Here generate the list with all list of tracks and clusters
for i in element_list:
    if i == 0:
        iant = i
        continue
    for line in lines[iant:i]:
        # Here we are in the first element
        if 'track' in str(line):
            particles_1_tracks.append(line)
        if 'cluster' in str(line):
            particles_1_clusters.append(line)
    particles.append(particles_1_tracks)
    particles.append(particles_1_clusters)
    particles_1_tracks = []
    particles_1_clusters = []
    iant = i
    
# Initializate sound
pygame.mixer.init(44100, -16, channels = 1, buffer=4095, allowedchanges=pygame.AUDIO_ALLOW_FREQUENCY_CHANGE)
# Set the path to open the tickmark
bip_path = os.path.abspath(os.path.dirname(__file__)) + '/sound_module/sounds/bip.wav'
# Open the bip tickmark
rate1, bip = wavfile.read(bip_path, mmap=False)
#
note_freqs = get_piano_notes()
freqC6 = note_freqs['C6']
freqD6 = note_freqs['D6']
freqF7 = note_freqs['F7']
# Obtain pure sine wave for each frequency
track_1s = get_sine_wave(freqD6, duration=1)
track_sound = get_sine_wave(freqD6, duration=2)
double_track_sound = get_sine_wave(freqD6, duration=2)+get_sine_wave(freqC6, duration=2)
bip_calorimeter = get_sine_wave(freqF7, duration=0.1)
silence_2s = get_sine_wave(0, duration=2)
silence_1s = get_sine_wave(0, duration=1)
# Obtain a generic cluster sound
data = [300,350,600,800,1000,800,800,1000,700,600]
for x in range(0,10,1):
    signal = get_sine_wave(data[x], 0.1)
    if x==0:
        cluster_sound = signal
    else:
        cluster_sound = np.append(cluster_sound, signal)
# Here we call the method to sonify and plot each pair of track and cluster
plt.pause(0.5)
input("Press a key to continue...")
count = 0
for i in range(0,len(particles),2):
    count = count + 1
    sound_var = particles_sonification(particles[i],particles[i+1])
    plot_path = 'lhc_output/plot_dataset_' + str(count) + '.png'
    plt.savefig(plot_path, format='png')
    # Generate the wav file with the sonification
    sound_path = 'lhc_output/sound_dataset_' + str(count) + '.wav'
    wavfile.write(sound_path, rate=44100, data=sound_var.astype(np.int16))
    key = input("Press 'Q' to close or any other key to continue...")
    if key == 'Q' or key == 'q':
        plt.close()
        break
# Showing the above plot
plt.show()
plt.close()
# Last but not least, close the file
file1.close()
