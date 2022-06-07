# -*- coding: utf-8 -*-

import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from data_lhc import lhc_data

"""
calculates the square root of ( (φtrack-φcluster)squared+(θtrack-θcluster) squared)).
If the track(s) point in 3-D to a cluster this value should be small* (<0.1?). 
Then if it is below the cut you play a "cluster" sound simultaneous with the "track(s)" cluster.
"""
# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))
ax_transversal, ax_longitudinal = lhc_data.lhc_plot.plot3D_init(fig)
plt.pause(0.5)
"""
Particle data file
"""

"""Using lhc_data"""
lines = lhc_data.openfile('sonification_reduced.txt')
"""Using lhc_data"""
particles = lhc_data.read_content(lines)
 
lhc_data.lhc_sonification.sound_init()
lhc_data.lhc_sonification.set_bip()
input("Press a key to continue...")
count = 0
for i in range(0,len(particles),2):
    count = count + 1
    index = 0
    sonified_cluster_list = []
    sonified_tracks_list = []
    for tracks in particles[i]:
        element = 'Track'
        sonified_tracks, sonified_cluster = lhc_data.particles_sonification(index,
                                        element,
                                        particles[i], 
                                        particles[i+1], 
                                        ax_transversal, 
                                        ax_longitudinal,
                                        sonified_tracks_list,
                                        sonified_cluster_list
                                        )
        sonified_tracks_list = sonified_tracks_list + sonified_tracks
        sonified_cluster_list = sonified_cluster_list + sonified_cluster
        plt.pause(0.5)
        track = particles[i][index]
        track_elements = str(track).split()
        if int(track_elements[11])==1:
            time.sleep(5)
        else:
            time.sleep(3)
        index = index + 1
    index = 0
    for cluster in particles[i+1]:
        element = 'Cluster'
        sonified_tracks, sonified_cluster = lhc_data.particles_sonification(index,
                                        element,
                                        particles[i], 
                                        particles[i+1], 
                                        ax_transversal, 
                                        ax_longitudinal,
                                        sonified_tracks_list,
                                        sonified_cluster_list
                                        )
        sonified_tracks_list = sonified_tracks_list + sonified_tracks
        sonified_cluster_list = sonified_cluster_list + sonified_cluster
        plt.pause(0.5)
        time.sleep(3)
        index = index + 1
    plot_path = 'data_lhc/lhc_output/plot_dataset_' + str(count) + '.png'
    plt.savefig(plot_path, format='png')
    # Generate the wav file with the sonification
    sound_path = 'data_lhc/lhc_output/sound_dataset_' + str(count) + '.wav'
    #wavfile.write(sound_path, rate=44100, data=sound_var.astype(np.int16))
    lhc_data.lhc_sonification.save_sound(sound_path)
    lhc_data.lhc_plot.plot_reset()
    key = input("Press 'Q' to close or any other key to continue...")
    if key == 'Q' or key == 'q':
        plt.close()
        break
# Showing the above plot
plt.show()
# Closing the plot
plt.close()
