#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:16:05 2022

@author: sonounoteam
"""

import time
import os
import argparse
import datetime
import glob
from data_import.data_import import DataImportColumns
import matplotlib.pyplot as plt
import numpy as np
from data_lhc import lhc_sonification as sd
from pydub import AudioSegment

def wav_to_mp3(wav_path, mp3_path):
    sound = AudioSegment.from_mp3(wav_path)
    sound.export(mp3_path, format='wav')


open_csv = DataImportColumns()


# The argparse library is used to pass the path and extension where the data
# files are located
parser = argparse.ArgumentParser()
# Receive the extension from the arguments
parser.add_argument("-t", "--file-type", type=str,
                    help="Select file type.",
                    choices=['csv', 'txt'])
# Receive the directory path from the arguments
parser.add_argument("-d", "--directory", type=str,
                    help="Indicate a directory to process as batch.")
# Indicate to save or not the plot
parser.add_argument("-p", "--save-plot", type=bool,
                    help="Indicate if you want to save the plot (False as default)",
                    choices=[False,True])
# Alocate the arguments in variables, if extension is empty, select txt as
# default
args = parser.parse_args()
ext = args.file_type or 'txt'
path = args.directory
plot_flag = args.save_plot or False
# Print a messege if path is not indicated by the user
if not path:
    print('At least on intput must be stated.\nUse -h if you need help.')
    exit()
# Format the extension to use it with glob
extension = '*.' + ext
# Initialize a counter to show a message during each loop
i = 1
if plot_flag:
    # # Create an empty figure or plot to save it
    # cm = 1/2.54  # centimeters in inches
    # fig = plt.figure(figsize=(15*cm, 10*cm), dpi=300)
    # # Defining the axes so that we can plot data into it.
    # ax = plt.axes()
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2)
    fig.suptitle('Muon event 1D')

# init sound
sd.sound_init()
note_freq = sd.get_piano_notes()
# list_32 = [note_freq['D2'], note_freq['E2'], note_freq['F2'], note_freq['G2'], 
#            note_freq['A2'], note_freq['B2'], note_freq['C3'], note_freq['D3'], 
#            note_freq['E3'], note_freq['F3'], note_freq['G3'], note_freq['A3'], 
#            note_freq['B3'], note_freq['C4'], note_freq['D4'], note_freq['E4'], 
#            note_freq['F4'], note_freq['G4'], note_freq['A4'], note_freq['B4'], 
#            note_freq['C5'], note_freq['D5'], note_freq['E5'], note_freq['F5'], 
#            note_freq['G5'], note_freq['A5'], note_freq['B5'], note_freq['C6'], 
#            note_freq['D6'], note_freq['E6'], note_freq['F6'], note_freq['G6']]#, 
# #           note_freq['A6']]

list_notes = [note_freq['A3'], note_freq['B3'], note_freq['C4'], note_freq['D4'], 
              note_freq['E4'], note_freq['F4'], note_freq['G4'], note_freq['A4'], 
              note_freq['B4'], note_freq['C5'], note_freq['D5'], note_freq['E5'], 
              note_freq['F5'], note_freq['G5'], note_freq['A5'], note_freq['B5']]

# list_16 = [note_freq['D2'], note_freq['F2'], note_freq['A2'], note_freq['C3'], 
#            note_freq['E3'], note_freq['G3'], note_freq['B3'], note_freq['D4'], 
#            note_freq['F4'], note_freq['A4'], note_freq['C5'], note_freq['E5'], 
#            note_freq['G5'], note_freq['B5'], note_freq['D6'], note_freq['F6']]#, 
# #           note_freq['A6']]
    
sd.set_bip()
bip = sd.get_bip()
loop_number = 0

# Loop to walk the directory and sonify each data file
now = datetime.datetime.now()
print(now.strftime('%Y-%m-%d_%H-%M-%S'))
for filename in glob.glob(os.path.join(path, extension)):
    print("Converting data file number "+str(i)+" to sound.")
    # Open each file
    file, status, msg = open_csv.set_arrayfromfile(filename, ext)

# name = '5683061_1093057'
# file, flag, msg = open_csv.set_arrayfromfile('data_muon/muon_line/'+name+'.csv', 'csv')

# fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2)
# fig.suptitle('Vertically stacked subplots')
    
    if plot_flag:
        ax1.cla()
        ax2.cla()
        ax3.cla()
        ax4.cla()
        ax5.cla()
        ax6.cla()
        ax1.set_xlabel('channel')
        ax2.set_xlabel('channel')
        ax3.set_xlabel('channel')
        ax4.set_xlabel('channel')
        ax5.set_xlabel('channel')
        ax6.set_xlabel('channel')
        
        ax1.plot((file.iloc[1:,0].astype(float)), (file.iloc[1:,1].astype(float)), 'bo')
        ax2.plot((file.iloc[1:,0].astype(float)), (file.iloc[1:,2].astype(float)), 'bo')
        ax3.plot((file.iloc[1:,0].astype(float)), (file.iloc[1:,3].astype(float)), 'bo')
        ax4.plot((file.iloc[1:,0].astype(float)), (file.iloc[1:,4].astype(float)), 'bo')
        ax5.plot((file.iloc[1:,0].astype(float)), (file.iloc[1:,5].astype(float)), 'bo')
        ax6.plot((file.iloc[1:,0].astype(float)), (file.iloc[1:,6].astype(float)), 'bo')
        plt.pause(0.5)
        
        plot_path = path + '/' + os.path.basename(filename[:-4]) + '_plot.png'
        fig.savefig(plot_path)
    
    # Plot ax5
    count = 0
    count1 = 0
    sound_ax5 = []
    sound_ax6 = []
    sound_ax3 = []
    sound_ax4 = []
    sound_ax1 = []
    sound_ax2 = []
    for note in list_notes:
        # plot 5
        if not len(sound_ax5):
            if float(file.iloc[count+1,5]) != 0:
                sound_ax5 = sd.get_sine_wave(note, 1)
                px_ax5 = [count+1]
                py_ax5 = [float(file.iloc[count+1,5])]
                if float(file.iloc[count+2,5]) != 0:
                    sound_ax5 = sound_ax5 + sd.get_sine_wave(note, 1)
                    px_ax5.append(count+2)
                    py_ax5.append(float(file.iloc[count+2,5]))
            elif float(file.iloc[count+2,5]) != 0:
                sound_ax5 = sd.get_sine_wave(note, 1)
                px_ax5 = [count+2]
                py_ax5 = [float(file.iloc[count+2,5])]
        else:
            if float(file.iloc[count+1,5]) != 0:
                sound_ax5 = sound_ax5 + sd.get_sine_wave(note, 1)
                px_ax5.append(count+1)
                py_ax5.append(float(file.iloc[count+1,5]))
            if float(file.iloc[count+2,5]) != 0:
                sound_ax5 = sound_ax5 + sd.get_sine_wave(note, 1)
                px_ax5.append(count+2)
                py_ax5.append(float(file.iloc[count+2,5]))
        # plot 6
        if not len(sound_ax6):
            if float(file.iloc[count+1,6]) != 0:
                sound_ax6 = sd.get_sine_wave(note, 1)
                px_ax6 = [count+1]
                py_ax6 = [float(file.iloc[count+1,6])]
                if float(file.iloc[count+2,6]) != 0:
                    sound_ax6 = sound_ax6 + sd.get_sine_wave(note, 1)
                    px_ax6.append(count+2)
                    py_ax6.append(float(file.iloc[count+2,6]))
            elif float(file.iloc[count+2,6]) != 0:
                sound_ax6 = sd.get_sine_wave(note, 1)
                px_ax6 = [count+2]
                py_ax6 = [float(file.iloc[count+2,6])]
        else:
            if float(file.iloc[count+1,6]) != 0:
                sound_ax6 = sound_ax6 + sd.get_sine_wave(note, 1)
                px_ax6.append(count+1)
                py_ax6.append(float(file.iloc[count+1,6]))
            if float(file.iloc[count+2,6]) != 0:
                sound_ax6 = sound_ax6 + sd.get_sine_wave(note, 1)
                px_ax6.append(count+2)
                py_ax6.append(float(file.iloc[count+2,6]))
        # plot 3
        if not len(sound_ax3):
            if float(file.iloc[count1+1,3]) != 0:
                sound_ax3 = sd.get_sine_wave(note, 1)
                px_ax3 = [count1+1]
                py_ax3 = [float(file.iloc[count1+1,3])]
        else:
            if float(file.iloc[count1+1,3]) != 0:
                sound_ax3 = sound_ax3 + sd.get_sine_wave(note, 1)
                px_ax3.append(count1+1)
                py_ax3.append(float(file.iloc[count1+1,3]))
        # plot 4
        if not len(sound_ax4):
            if float(file.iloc[count1+1,4]) != 0:
                sound_ax4 = sd.get_sine_wave(note, 1)
                px_ax4 = [count1+1]
                py_ax4 = [float(file.iloc[count1+1,4])]
        else:
            if float(file.iloc[count1+1,4]) != 0:
                sound_ax4 = sound_ax4 + sd.get_sine_wave(note, 1)
                px_ax4.append(count1+1)
                py_ax4.append(float(file.iloc[count1+1,4]))
        # plot 1
        if not len(sound_ax1):
            if float(file.iloc[count+1,1]) != 0:
                sound_ax1 = sd.get_sine_wave(note, 1)
                px_ax1 = [count+1]
                py_ax1 = [float(file.iloc[count+1,1])]
                if float(file.iloc[count+2,1]) != 0:
                    sound_ax1 = sound_ax1 + sd.get_sine_wave(note, 1)
                    px_ax1.append(count+2)
                    py_ax1.append(float(file.iloc[count+2,1]))
            elif float(file.iloc[count+2,1]) != 0:
                sound_ax1 = sd.get_sine_wave(note, 1)
                px_ax1 = [count+2]
                py_ax1 = [float(file.iloc[count+2,1])]
        else:
            if float(file.iloc[count+1,1]) != 0:
                sound_ax1 = sound_ax1 + sd.get_sine_wave(note, 1)
                px_ax1.append(count+1)
                py_ax1.append(float(file.iloc[count+1,1]))
            if float(file.iloc[count+2,1]) != 0:
                sound_ax1 = sound_ax1 + sd.get_sine_wave(note, 1)
                px_ax1.append(count+2)
                py_ax1.append(float(file.iloc[count+2,1]))
        # plot 2
        if not len(sound_ax2):
            if float(file.iloc[count+1,2]) != 0:
                sound_ax2 = sd.get_sine_wave(note, 1)
                px_ax2 = [count+1]
                py_ax2 = [float(file.iloc[count+1,2])]
                if float(file.iloc[count+2,2]) != 0:
                    sound_ax2 = sound_ax2 + sd.get_sine_wave(note, 1)
                    px_ax2.append(count+2)
                    py_ax2.append(float(file.iloc[count+2,2]))
            elif float(file.iloc[count+2,2]) != 0:
                sound_ax2 = sd.get_sine_wave(note, 1)
                px_ax2 = [count+2]
                py_ax2 = [float(file.iloc[count+2,2])]
        else:
            if float(file.iloc[count+1,2]) != 0:
                sound_ax2 = sound_ax2 + sd.get_sine_wave(note, 1)
                px_ax2.append(count+1)
                py_ax2.append(float(file.iloc[count+1,2]))
            if float(file.iloc[count+2,2]) != 0:
                sound_ax2 = sound_ax2 + sd.get_sine_wave(note, 1)
                px_ax2.append(count+2)
                py_ax2.append(float(file.iloc[count+2,2]))
        count = count + 2
        count1 = count1 + 1
        
    list_colors = ['tab:red', 'tab:orange', 'yellow', 'tab:olive', 'tab:green', 
                   'tab:cyan', 'tab:blue', 'tab:purple']

    # ax1.plot(
    #     (file.iloc[1:5,0].astype(float)), 
    #     (file.iloc[1:5,1].astype(float)),
    #     color=list_colors[0], marker='o', linestyle=''
    #     )
    # ax1.plot(
    #     (file.iloc[5:9,0].astype(float)), 
    #     (file.iloc[5:9,1].astype(float)),
    #     color=list_colors[1], marker='o', linestyle=''
    #     )
    # ax1.plot(
    #     (file.iloc[9:13,0].astype(float)), 
    #     (file.iloc[9:13,1].astype(float)),
    #     color=list_colors[2], marker='o', linestyle=''
    #     )
    # ax1.plot(
    #     (file.iloc[13:17,0].astype(float)), 
    #     (file.iloc[13:17,1].astype(float)),
    #     color=list_colors[3], marker='o', linestyle=''
    #     )
    # ax1.plot(
    #     (file.iloc[17:21,0].astype(float)), 
    #     (file.iloc[17:21,1].astype(float)),
    #     color=list_colors[4], marker='o', linestyle=''
    #     )
    # ax1.plot(
    #     (file.iloc[21:25,0].astype(float)), 
    #     (file.iloc[21:25,1].astype(float)),
    #     color=list_colors[5], marker='o', linestyle=''
    #     )
    # ax1.plot(
    #     (file.iloc[25:29,0].astype(float)), 
    #     (file.iloc[25:29,1].astype(float)),
    #     color=list_colors[6], marker='o', linestyle=''
    #     )
    # ax1.plot(
    #     (file.iloc[29:33,0].astype(float)), 
    #     (file.iloc[29:33,1].astype(float)),
    #     color=list_colors[7], marker='o', linestyle=''
    #     )
    
    # play bip of the beggining
    sd.play_sound(bip)
    sd.array_savesound(bip)
    time.sleep(1)
    #play the part on the left
    sd.play_sound(sound_ax1)
    sd.add_array_savesound(sound_ax1)
    count = 0
    for px in px_ax1:
        ax1.plot(px,py_ax1[count],color=list_colors[int(px/4)], marker='o', linestyle='')
        count = count + 1
    plt.pause(0.5)
    time.sleep(0.5)
    sd.play_sound(sound_ax3)
    sd.add_array_savesound(sound_ax3)
    count = 0
    ax1.plot(px_ax1,py_ax1,color='k', marker='o', linestyle='')
    for px in px_ax3:
        ax3.plot(px,py_ax3[count],color=list_colors[int(px/2)], marker='o', linestyle='')
        count = count + 1
    plt.pause(0.5)
    time.sleep(0.5)
    sd.play_sound(sound_ax5)
    sd.add_array_savesound(sound_ax5)
    count = 0
    ax3.plot(px_ax3,py_ax3,color='k', marker='o', linestyle='')
    for px in px_ax5:
        ax5.plot(px,py_ax5[count],color=list_colors[int(px/4)], marker='o', linestyle='')
        count = count + 1
    plt.pause(0.5)
    time.sleep(0.5)
    ax5.plot(px_ax5,py_ax5,color='k', marker='o', linestyle='')
    # play bip of the beggining
    sd.play_sound(bip)
    sd.add_array_savesound(bip)
    time.sleep(1)
    #silence
    sd.play_sound(sd.get_silence(1))
    sd.add_array_savesound(sd.get_silence(1))
    time.sleep(1)
    #play the part on the right
    sd.play_sound(sound_ax2)
    sd.add_array_savesound(sound_ax2)
    count = 0
    for px in px_ax2:
        ax2.plot(px,py_ax2[count],color=list_colors[int(px/4)], marker='o', linestyle='')
        count = count + 1
    plt.pause(0.5)
    time.sleep(0.5)
    sd.play_sound(sound_ax4)
    sd.add_array_savesound(sound_ax4)
    count = 0
    ax2.plot(px_ax2,py_ax2,color='k', marker='o', linestyle='')
    for px in px_ax4:
        ax4.plot(px,py_ax4[count],color=list_colors[int(px/2)], marker='o', linestyle='')
        count = count + 1
    plt.pause(0.5)
    time.sleep(0.5)
    sd.play_sound(sound_ax6)
    sd.add_array_savesound(sound_ax6)
    count = 0
    ax4.plot(px_ax4,py_ax4,color='k', marker='o', linestyle='')
    for px in px_ax6:
        ax6.plot(px,py_ax6[count],color=list_colors[int(px/4)], marker='o', linestyle='')
        count = count + 1
    plt.pause(0.5)
    time.sleep(0.5)
    ax6.plot(px_ax6,py_ax6,color='k', marker='o', linestyle='')
    
    wav_name = path + '/' + os.path.basename(filename[:-4]) + '_sound.wav'
    mp3_name = path + '/' + os.path.basename(filename[:-4]) + '_sound.mp3'
    sd.save_sound(wav_name)
    wav_to_mp3(wav_name, mp3_name)
    # sd.save_sound('data_muon/muon_line/'+name+'.wav')
    key = input("Press 'Q' to close or any other key to continue...")
    if key == 'Q' or key == 'q':
        plt.close()
        break

plt.pause(0.5)
# Showing the above plot
plt.show()
plt.close()


