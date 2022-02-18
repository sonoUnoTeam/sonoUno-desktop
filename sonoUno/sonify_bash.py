# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 11:13:42 2022

@author: johi-
"""

import os
import argparse
import glob
import numpy as np
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
# Alocate the arguments in variables, if extension is empty, select txt as
# default
args = parser.parse_args()
ext = args.file_type or 'txt'
path = args.directory
# Print a messege if path is not indicated by the user
if not path:
    print('At least on intput must be stated.\nUse -h if you need help.')
    exit()
# Format the extension to use it with glob
extension = '*.' + ext
# Initialize a counter to show a message during each loop
i = 1
# Loop to walk the directory and sonify each data file
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
    # Save the sound
    wav_name = path + '\\' + os.path.basename(filename) + '_sound.wav'
    _simplesound.save_sound(wav_name, x, y)
    i = i + 1

