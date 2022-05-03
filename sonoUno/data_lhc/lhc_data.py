#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 08:18:55 2022

@author: sonounoteam

This script open the file and apply specific transforms to it.
"""

import math
from . import lhc_plot
from . import lhc_sonification

#Global lists to sonification and plot
sonified_cluster_list = []
sonified_tracks_list = []
cluster_tosonify = []

def openfile(path):
    """
    This method open the file with the given path, read its lines and return 
    a list with its content.

    """
    # First open the file and store it.
    path = 'sonification_reduced.txt'
    file = open(path,'r')
    lines = file.readlines()
    return lines

def read_content(file):
    # Search the separator on the file and store the index where each event begin
    count = 0
    element_list = [0]
    for line in file:
        count = count + 1
        if '---------' in str(line) and count <= len(file):
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
        for line in file[iant:i]:
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
    # Particles is a list of list that contain a list of tracks and a list of
    # clusters for each event.
    return particles

def particles_sonification(index, element, track_list, cluster_list, ax_transversal, ax_longitudinal):
    # With each track calculate if it points out a cluster or not, if points a
    # cluster we will sonify the track and the cluster
    global sonified_cluster_list, sonified_tracks_list, cluster_tosonify
    if index == 0:
        lhc_plot.set_count_colors(0)
        sonified_cluster_list = []
        sonified_tracks_list = []
    cluster_tosonify = []
    converted_photon = ' '
    track_list_2 = track_list.copy()
    # Variable to store all sound to save at the end
    # for track in track_list:
    """
    Trying to use events not for
    """
    if element == 'Track':
        #plot the track
        track = track_list[index]
        track_elements = str(track).split()
        count = index + 1
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
                    # Search for a close track
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
                        lhc_plot.plot_innertrack(track_elements)
                        converted_photon = track2_elements[0]
            for cluster in cluster_list:
                cluster_elements = str(cluster).split()
                # Search if the track points a cluster
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
                        eta=float(track_elements[6]))
                    cluster_tosonify.append(cluster)
            """
            Sonification of the tracks
            """
            if cluster_tosonify:
                # The track point out a cluster
                if len(cluster_tosonify) > 1:
                    #Arreglar el mensaje aqui
                    print('Could a track points out to more than one cluster?')
                    print(cluster_tosonify)
                    return
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
                        sound = lhc_sonification.muontrack_withcluster()
                    else:
                        """
                        1) bip: the beginning of the detector
                        2) continuous sound during 2 seconds: the track in the inner detector
                        3) a tone with different frequency: change from inner detector to red calorimeter
                        4) sound corresponding to the cluster
                        """
                        sound = lhc_sonification.singletrack_withcluster()
                else:
                    """
                    1) bip: the beginning of the detector
                    2) two continuous sound during 2 seconds: the tracks in the inner detector
                    3) a tone with different frequency: change from inner detector to red calorimeter
                    4) sound corresponding to the cluster
                    """
                    print('Sonifying '+track_elements[0]+', '+converted_photon+' and '+cluster_elements[0])
                    sound = lhc_sonification.doubletrack_withcluster()
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
            cluster_tosonify = []
            converted_photon = ' '
    
    elif element == 'Cluster':
    #for cluster in cluster_list:
        cluster = cluster_list[index]
        cluster_elements = str(cluster).split()
        if not cluster_elements[0] in sonified_cluster_list:
            lhc_plot.plot_cluster(
                phi=float(cluster_elements[4]),
                theta=float(cluster_elements[5]),
                eta=float(cluster_elements[6]))
            """
            1) bip: the beginning of the detector
            2) silence during 2 seconds: there are no track in the inner detector
            3) a tone with different frequency: change from inner detector to red calorimeter
            4) sound corresponding to the cluster
            """
            print('Sonifying '+cluster_elements[0])
            sound = lhc_sonification.cluster_only()
            lhc_sonification.play_sound(sound)
            lhc_sonification.add_array_savesound(sound)
            lhc_sonification.add_array_savesound(lhc_sonification.get_silence_1s())
    else:
        print("problem with element!!!!")