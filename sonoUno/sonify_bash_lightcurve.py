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
import math
import pandas as pd
from data_transform import smooth
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
    # x = data.loc[1:, 2]
    # xnumpy = x.values.astype(np.float64)
    # y = data.loc[1:, 4]
    # ynumpy = y.values.astype(np.float64)
    
    #Select columns to order next
    selected_columns = data[[2,4]]
    new_df = selected_columns.copy()
    # sort_df = pd.DataFrame(new_df).sort_values(2, axis=0)
    
    
    # x = sort_df[:,0].astype(np.float64)
    # y = sort_df[:,1].astype(np.float64)
    
    # x = sort_df.loc[1:, 0]
    # xnumpy = x.values.astype(np.float64)
    # y = sort_df.loc[1:, 1]
    # ynumpy = y.values.astype(np.float64)
    
    # Para estrellas variables
    periodo_CGCas = 4.3652815
    periodo_RWPhe = 5.4134367
    t0_CGCas = 2457412.70647
    t0_RWPhe = 2458053.49761

    # """Para CGCas"""
    # new_df.loc[:,2] = (new_df.loc[:,2].astype(float) - t0_CGCas) / periodo_CGCas
    # new_df.loc[:,2] = (new_df.loc[:,2] - new_df.loc[:,2].astype(float).astype(int)) + 0.79
    # for i in range (1,(len(new_df.loc[:,2]))):
    #     if new_df.loc[i,2] < 0:
    #         new_df.loc[i,2] = new_df.loc[i,2] + 2
    """Para RWPhe"""
    new_df.loc[:,2] = (new_df.loc[:,2].astype(float) - t0_RWPhe) / periodo_RWPhe
    new_df.loc[:,2] = (new_df.loc[:,2] - new_df.loc[:,2].astype(float).astype(int)) + 0.55
    for i in range (1,(len(new_df.loc[:,2]))):
        if new_df.loc[i,2] < 0:
            new_df.loc[i,2] = new_df.loc[i,2] + 2
    
    
    new_df.loc[:,4] = new_df.loc[:,4].astype(float)
    
    sort_df = pd.DataFrame(new_df).sort_values(2, axis=0)
    
    print(sort_df.loc[:,4])
    
    yl = sort_df.loc[:,4].values
    yhat = smooth.savitzky_golay(yl, 51, 7)
    
    
    x, y, status = _math.normalize(sort_df.loc[:,2], sort_df.loc[:,4])
    if plot_flag:
        # Configure axis, plot the data and save it
        # Erase the plot
        ax.cla()
        # First file of the column is setted as axis name
        x_name = str(data.iloc[0,0])
        ax.set_xlabel('Phase')
        y_name = str(data.iloc[0,0])
        ax.set_ylabel('Mag')
        ax.invert_yaxis()
        # Separate the name file from the path to set the plot title
        head, tail = os.path.split(filename)
        ax.set_title('CG-Cas-Cepheid')
        # xnumpy = xnumpy / 10
        # ax.scatter(xnumpy, ynumpy)
        # ax.plot(sort_df.loc[:,2], sort_df.loc[:,4], 'o')
        ax.plot(sort_df.loc[:,2], yhat)        
        # Set the path to save the plot and save it
        plot_path = path + '\\' + os.path.basename(filename) + '_plot.png'
        fig.savefig(plot_path)
    # Save the sound
    wav_name = path + '\\' + os.path.basename(filename) + '_sound.wav'
    _simplesound.save_sound(wav_name, x, y)
    now = datetime.datetime.now()
    print(now.strftime('%Y-%m-%d_%H-%M-%S'))
    i = i + 1

