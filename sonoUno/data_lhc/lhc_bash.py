# -*- coding: utf-8 -*-

import time
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import math
import pygame
import lhc_plot
import lhc_sonification

def particles_sonification(track_list, cluster_list):
    """
    Thi loop method reproduce each track and cluster of an event.
    """
    lhc_plot.plot_reset()
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
                #Muon
                lhc_plot.plot_muontrack(track_elements)
            else:
                #Other tracks
                lhc_plot.plot_innertrack(track_elements)
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
                    if value_tracks < 0.04 and track_elements[1] != track2_elements[1]:
                        if not track2_elements[0] in sonified_tracks_list:
                            sonified_tracks_list.append(track2_elements[0])
                        lhc_plot.plot_innertrack(track_elements)
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
                    lhc_plot.plot_cluster(
                        phi=float(track_elements[4]),
                        theta=float(track_elements[5]),
                        eta=float(track_elements[6]),
                        amplitud=float(cluster_elements[3])/100)
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
                    if int(track_elements[11])==1:
                        """
                        1) bip: the beginning of the detector
                        2) continuous sound during 2 seconds: the track in the inner detector
                        3) a tone with different frequency: change from inner detector to red calorimeter
                        4) sound corresponding to the cluster with the continuous sound of the track of the muon
                        """
                        # For the amplitud of the sound we use the transverse energy
                        # supposing a range of [0;100], we devide the value by 100
                        # to normalize it.
                        sound = lhc_sonification.muontrack_withcluster(float(cluster_elements[3])/100)
                    else:
                        """
                        1) bip: the beginning of the detector
                        2) continuous sound during 2 seconds: the track in the inner detector
                        3) a tone with different frequency: change from inner detector to red calorimeter
                        4) sound corresponding to the cluster
                        """
                        sound = lhc_sonification.singletrack_withcluster(float(cluster_elements[3])/100)
                else:
                    """
                    1) bip: the beginning of the detector
                    2) two continuous sound during 2 seconds: the tracks in the inner detector
                    3) a tone with different frequency: change from inner detector to red calorimeter
                    4) sound corresponding to the cluster
                    """
                    print('Sonifying '+track_elements[0]+', '+converted_photon+' and '+cluster_elements[0])
                    sound = lhc_sonification.doubletrack_withcluster(float(cluster_elements[3])/100)
            else:
                # The track don't point out a cluster
                """
                1) bip: the beginning of the detector
                2) continuous sound during 2 seconds: the track in the inner detector
                3) a tone with different frequency: change from inner detector to red calorimeter
                """
                print('Sonifying '+track_elements[0])
                sound = lhc_sonification.singletrack_only()
                if int(track_elements[11])==1:
                    sound = lhc_sonification.doubletrack_only()
            lhc_sonification.play_sound(sound)
            if count == 1:
                lhc_sonification.array_savesound(sound)
            else:
                lhc_sonification.add_array_savesound(sound)
            lhc_sonification.add_array_savesound(lhc_sonification.get_silence_1s())
            
            if int(track_elements[11])==1:
                time.sleep(4.5)
            else:
                time.sleep(3)
            cluster_tosonify = []
            converted_photon = ' '
    for cluster in cluster_list:
        cluster_elements = str(cluster).split()
        if not cluster_elements[0] in sonified_cluster_list:
            lhc_plot.plot_cluster(
                phi=float(cluster_elements[4]),
                theta=float(cluster_elements[5]),
                eta=float(cluster_elements[6]),
                amplitud=float(cluster_elements[3])/100)
            plt.pause(0.5)
            """
            1) bip: the beginning of the detector
            2) silence during 2 seconds: there are no track in the inner detector
            3) a tone with different frequency: change from inner detector to red calorimeter
            4) sound corresponding to the cluster
            """
            print('Sonifying '+cluster_elements[0])
            sound = lhc_sonification.cluster_only(float(cluster_elements[3])/100)
            lhc_sonification.play_sound(sound)
            lhc_sonification.add_array_savesound(sound)
            lhc_sonification.add_array_savesound(lhc_sonification.get_silence_1s())
            time.sleep(3)

#sonify_electron_WP5()

"""
calculates the square root of ( (φtrack-φcluster)squared+(θtrack-θcluster) squared)).
If the track(s) point in 3-D to a cluster this value should be small* (<0.1?). 
Then if it is below the cut you play a "cluster" sound simultaneous with the "track(s)" cluster.
"""
# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))
lhc_plot.plot3D_init(fig)
plt.pause(0.5)
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
 
lhc_sonification.sound_init()
lhc_sonification.set_bip()
input("Press a key to continue...")
count = 0
for i in range(0,len(particles),2):
    count = count + 1
    particles_sonification(particles[i],particles[i+1])
    plot_path = 'lhc_output/plot_dataset_' + str(count) + '.png'
    plt.savefig(plot_path, format='png')
    # Generate the wav file with the sonification
    sound_path = 'lhc_output/sound_dataset_' + str(count) + '.wav'
    #wavfile.write(sound_path, rate=44100, data=sound_var.astype(np.int16))
    lhc_sonification.save_sound(sound_path)
    lhc_plot.set_count_colors(0)
    key = input("Press 'Q' to close or any other key to continue...")
    if key == 'Q' or key == 'q':
        plt.close()
        break
# Showing the above plot
plt.show()
plt.close()
# Last but not least, close the file
file1.close()
