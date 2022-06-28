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
    file = open(path,'r')
    lines = file.readlines()
    return lines

def read_content(file):
    """
    This method require the lines readed from a file that contain the lhc events

    Parameters
    ----------
    file : TYPE list
    
    Returns
    -------
    particles : TYPE list, contain diferent lists of each event, where inside 
        each event there are lists of each track and cluster found in it.
    """
    # Search the separator '------------' on the file, which one indicate the
    # beginning of a new event, and store the index
    count = 0
    element_list = [0]
    for line in file:
        count = count + 1
        if '---------' in str(line) and count <= len(file):
            element_list.append(count)
    # Initialize the counter and the list where events will be saved
    count = 0
    particles = []
    # Initialize a list of tracks and clusters where their will be stored before
    # to save it in the final list
    particles_1_tracks = []
    particles_1_clusters = []
    # Generate a loop with the number of events found
    for i in element_list:
        if i == 0:
            iant = i
            continue
        # Iterates through the file as many times as there are events in the file
        for line in file[iant:i]:
            split = str(line).split()
            if len(split) == 1 and not '------' in line:
                particles.append(line[:-1])
            # Store each track on a list and each cluster on other list
            if 'track' in str(line):
                particles_1_tracks.append(line)
            if 'cluster' in str(line):
                particles_1_clusters.append(line)
        # Add the tracks and cluster lists of the specific event on the general
        # list
        particles.append(particles_1_tracks)
        particles.append(particles_1_clusters)
        # Restore the specific track and cluster lists for the next iteration
        particles_1_tracks = []
        particles_1_clusters = []
        # Update the iant for stablish the next file part to be revised
        iant = i
    return particles

def particles_sonification(index, element, track_list, cluster_list, play_sound_status=True):
    """
    This method allows to iterate through a given event ploting and sonifying 
    the data provided.

    Parameters
    ----------
    index : TYPE int, where we are located in the event reproduction
    element : TYPE str, indicate Track or Cluster
    track_list : TYPE list, contain the track elements
    cluster_list : TYPE list, contain the cluster element
    play_sound_status : TYPE bool, optional-default True, to not play sound
    """
    # Enable the global variables to be used and modified
    global cluster_tosonify, sonified_cluster_list, sonified_tracks_list
    # If this is the first track element of the event, initialize colour counter
    # and sonified elements lists
    if index == 0 and element == 'Track':
        lhc_plot.set_count_colors(0)
        sonified_cluster_list = []
        sonified_tracks_list = []
    # Restore variables
    cluster_tosonify = []
    converted_photon = ' '
    # Copy the track list to be used to search a close track
    track_list_2 = track_list.copy()
    # Select action depending on Track or Cluster reproduction
    if element == 'Track':
        # Obtain track elements to be reproduced
        track = track_list[index]
        track_elements = str(track).split()
        nextindex = index + 1
        # Check if the track has been sonified
        if not track_elements[0] in sonified_tracks_list:
            if int(track_elements[11])==1:
                # If the track is a muon plot it
                lhc_plot.plot_muontrack(track_elements)
            else:
                # If the track is not a muon plot a simple track
                lhc_plot.plot_innertrack(track_elements)
            # With each track calculate if it points out a cluster or not, if points a
            # cluster we will sonify the track and the cluster; and check if there
            # are a close track
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
                    # If the track points to the cluster, plot it and include it
                    # in the list to sonify.
                    if not cluster_elements[0] in sonified_cluster_list:
                        sonified_cluster_list.append(cluster_elements[0])
                    lhc_plot.plot_cluster(
                        phi=float(track_elements[4]),
                        theta=float(track_elements[5]),
                        eta=float(track_elements[6]),
                        amplitud=float(cluster_elements[3])/100)
                    cluster_tosonify.append(cluster)
                    # In addition, search if there are a close track
                    if nextindex < len(track_list):
                        for track2 in track_list_2[nextindex:]:
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
                                # If exist a track very close, plot it and set the variable
                                # to reproduce the converted photon sound
                                if not track2_elements[0] in sonified_tracks_list:
                                    sonified_tracks_list.append(track2_elements[0])
                                lhc_plot.plot_innertrack(track2_elements)
                                converted_photon = track2_elements[0]
            """
            Sonification part
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
                        # The element is a muon with cluster
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
                        # The element is an electron
                        """
                        1) bip: the beginning of the detector
                        2) continuous sound during 2 seconds: the track in the inner detector
                        3) a tone with different frequency: change from inner detector to red calorimeter
                        4) sound corresponding to the cluster
                        """
                        sound = lhc_sonification.singletrack_withcluster(float(cluster_elements[3])/100)
                else:
                    # The element is a converted photon
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
                    # The element is a muon
                    sound = lhc_sonification.doubletrack_only()
            # check the flag and sonify
            if play_sound_status:
                lhc_sonification.play_sound(sound)
            # Store the element in the array to save sound
            if nextindex == 1:
                lhc_sonification.array_savesound(sound)
            else:
                lhc_sonification.add_array_savesound(sound)
            # Add a silence between each element
            lhc_sonification.add_array_savesound(lhc_sonification.get_silence(1))
            # Restore variables
            cluster_tosonify = []
            converted_photon = ' '
    elif element == 'Cluster':
        # Obtain Cluster elements to be reproduced
        cluster = cluster_list[index]
        cluster_elements = str(cluster).split()
        # Check if the cluster has been sonified
        if not cluster_elements[0] in sonified_cluster_list:
            # Plot the cluster
            lhc_plot.plot_cluster(
                phi=float(cluster_elements[4]),
                theta=float(cluster_elements[5]),
                eta=float(cluster_elements[6]),
                amplitud=float(cluster_elements[3])/100)
            # Sonify the cluster
            """
            1) bip: the beginning of the detector
            2) silence during 2 seconds: there are no track in the inner detector
            3) a tone with different frequency: change from inner detector to red calorimeter
            4) sound corresponding to the cluster
            """
            print('Sonifying '+cluster_elements[0])
            sound = lhc_sonification.cluster_only(float(cluster_elements[3])/100)
            # Check the flag and reproduce the sound
            if play_sound_status:
                lhc_sonification.play_sound(sound)
            # Store the sound to be saved later
            lhc_sonification.add_array_savesound(sound)
            lhc_sonification.add_array_savesound(lhc_sonification.get_silence(1))
    else:
        print("The element provided is unknown")
