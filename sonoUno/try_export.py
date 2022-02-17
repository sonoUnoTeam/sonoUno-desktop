# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 11:13:42 2022

@author: johi-
"""

import os
import glob
import time
import numpy as np
from data_export.data_export import DataExport
from data_import.data_import import DataImport
from sound_module.simple_sound import simpleSound
from sound_module.simple_sound import tickMark
from data_transform.predef_math_functions import PredefMathFunctions

_dataexport = DataExport(False)
_dataimport = DataImport()
_simplesound = simpleSound()
_math = PredefMathFunctions()

_simplesound.reproductor.set_continuous()
_simplesound.reproductor.set_waveform('celesta')
_simplesound.reproductor.set_time_base(0.005)

# print("Write the path with data sets to be sonifyed:")
# path = input()
# print(f"The selected path is: {path}" )
ext = 'csv'

path = r'C:\Users\johi-\Documents\Datos astronomicos (muestra)\Galaxies'
extension = '*.' + ext
i = 1

for filename in glob.glob(os.path.join(path, extension)):
    print(filename)
    # Open each file
    data, status, msg = _dataimport.set_arrayfromfile(filename,ext)
    # Convert into numpy, split in x and y and normalyze
    print(data)
    data = data.iloc[1:,:]
    x = data.loc[1:,0]
    xnumpy = x.values.astype(np.float64)
    y = data.loc[1:,2]
    ynumpy = y.values.astype(np.float64)
    x, y, status = _math.normalize(xnumpy,ynumpy)
    print("save")
    # Save the sound
    path1 = path + '\\' + str(i) + '.wav'
    _simplesound.save_sound(path1, x, y)
    i = i + 1
    print(i)
    
  # with open(filename, 'r') as f:
  #   text = f.read()
  #   print (filename)
  #   print (len(text))