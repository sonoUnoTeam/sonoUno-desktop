# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 11:13:42 2022

@author: johi-
"""

import os
import argparse
import glob
import numpy as np
import datetime
import matplotlib.pyplot as plt
from data_export.data_export import DataExport
from data_import.data_import import DataImport
from sound_module.simple_sound import simpleSound
from data_transform.predef_math_functions import PredefMathFunctions

# Instanciate the sonoUno clases needed
_dataexport = DataExport(False)
_dataimport = DataImport()
_simplesound = simpleSound()
_math = PredefMathFunctions()
# Sound configurations, predefined at the moment
_simplesound.reproductor.set_continuous()
_simplesound.reproductor.set_waveform('celesta')
_simplesound.reproductor.set_time_base(0.05)
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
    # Create an empty figure or plot to save it
    cm = 1/2.54  # centimeters in inches
    fig = plt.figure(figsize=(15*cm, 10*cm), dpi=300)
    # Defining the axes so that we can plot data into it.
    ax = plt.axes()
# Loop to walk the directory and sonify each data file
now = datetime.datetime.now()
print(now.strftime('%Y-%m-%d_%H-%M-%S'))
for filename in glob.glob(os.path.join(path, extension)):
    print("Converting data file number "+str(i)+" to sound.")
    # Open each file
    data, status, msg = _dataimport.set_arrayfromfile(filename, ext)
    # Convert into numpy, split in x and y and normalyze
    if data.shape[1]<2:
        print("Error reading file, only detect one column.")
        exit()
    data = data.iloc[1:, :]
    x = data.loc[1:, 0]
    xnumpy = x.values.astype(np.float64)
    y = data.loc[1:, 1]
    ynumpy = y.values.astype(np.float64)
    x, y, status = _math.normalize(xnumpy, ynumpy)
    if plot_flag:
        # Configure axis, plot the data and save it
        # Erase the plot
        ax.cla()
        # First file of the column is setted as axis name
        x_name = str(data.iloc[0,0])
        ax.set_xlabel('x')
        y_name = str(data.iloc[0,0])
        ax.set_ylabel('y')
        # Separate the name file from the path to set the plot title
        head, tail = os.path.split(filename)
        ax.set_title(tail)
        ax.plot(xnumpy, ynumpy)
        # Set the path to save the plot and save it
        plot_path = path + '\\' + os.path.basename(filename) + '_plot.png'
        fig.savefig(plot_path)
    # Save the sound
    wav_name = path + '\\' + os.path.basename(filename) + '_sound.wav'
    _simplesound.save_sound(wav_name, x, y)
    now = datetime.datetime.now()
    print(now.strftime('%Y-%m-%d_%H-%M-%S'))
    i = i + 1
    
# now = datetime.datetime.now()
# print(now.strftime('%Y-%m-%d_%H-%M-%S'))
# n = np.arange(0, 10000, 1, dtype=int)
# wav_name = path + '\\_sound10000.wav'
# _simplesound.save_sound(wav_name, n, n)
# now = datetime.datetime.now()
# print(now.strftime('%Y-%m-%d_%H-%M-%S'))
# n = np.arange(0, 20000, 1, dtype=int)
# wav_name = path + '\\_sound20000.wav'
# _simplesound.save_sound(wav_name, n, n)
# now = datetime.datetime.now()
# print(now.strftime('%Y-%m-%d_%H-%M-%S'))
# n = np.arange(0, 30000, 1, dtype=int)
# wav_name = path + '\\_sound30000.wav'
# _simplesound.save_sound(wav_name, n, n)
# now = datetime.datetime.now()
# print(now.strftime('%Y-%m-%d_%H-%M-%S'))
# n = np.arange(0, 40000, 1, dtype=int)
# wav_name = path + '\\_sound40000.wav'
# _simplesound.save_sound(wav_name, n, n)
# now = datetime.datetime.now()
# print(now.strftime('%Y-%m-%d_%H-%M-%S'))

