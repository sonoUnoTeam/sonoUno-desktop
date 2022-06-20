# -*- coding: utf-8 -*-

import argparse
import matplotlib.pyplot as plt
from data_lhc import lhc_data

"""
calculates the square root of ( (φtrack-φcluster)squared+(θtrack-θcluster) squared)).
If the track(s) point in 3-D to a cluster this value should be small* (<0.1?). 
Then if it is below the cut you play a "cluster" sound simultaneous with the "track(s)" cluster.
"""
# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))
lhc_data.lhc_plot.plot3D_init(fig)
"""
Particle data file
"""
# The argparse library is used to pass the path and extension where the data
# files are located
parser = argparse.ArgumentParser()
# Receive the directory path from the arguments
parser.add_argument("-d", "--path", type=str,
                    help="Indicate the path to the image to sonify.")
# Alocate the arguments in variables, if extension is empty, select txt as
# default
args = parser.parse_args()
path = args.path

"""Using lhc_data"""
lines = lhc_data.openfile(path)
"""Using lhc_data"""
particles = lhc_data.read_content(lines)
 
lhc_data.lhc_sonification.sound_init()
lhc_data.lhc_sonification.set_bip()
count = 0
for i in range(0,len(particles),2):
    count = count + 1
    index = 0
    for tracks in particles[i]:
        element = 'Track'
        lhc_data.particles_sonification(index,
                                        element,
                                        particles[i], 
                                        particles[i+1], 
                                        play_sound_status=False
                                        )
        index = index + 1
    index = 0
    for cluster in particles[i+1]:
        element = 'Cluster'
        lhc_data.particles_sonification(index,
                                        element,
                                        particles[i], 
                                        particles[i+1], 
                                        play_sound_status=False
                                        )
        index = index + 1
    plot_path = 'data_lhc/lhc_output/plot_dataset_' + str(count) + '.png'
    plt.savefig(plot_path, format='png')
    # Generate the wav file with the sonification
    sound_path = 'data_lhc/lhc_output/sound_dataset_' + str(count) + '.wav'
    lhc_data.lhc_sonification.save_sound(sound_path)
    lhc_data.lhc_plot.plot_reset()
