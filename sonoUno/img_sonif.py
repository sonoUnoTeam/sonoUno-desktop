# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:04:39 2022

@author: Johanna
"""

import numpy as np
import cv2 as cv
import time
import argparse
from sound_module.simple_sound import simpleSound
# from pydub import AudioSegment

# def wav_to_mp3(wav_path, mp3_path):
#     sound_mp3 = AudioSegment.from_mp3(wav_path)
#     sound_mp3.export(mp3_path, format='wav')

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

img = cv.imread(path)
img = cv.resize(img, (960, 540))

gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow('Windows', img)
cv.waitKey(0)
print('Press ESC to exit the sonification.')

# Initialize simplesound
sound = simpleSound()

# Sound configurations, predefined at the moment
sound.reproductor.set_continuous()
sound.reproductor.set_waveform('celesta')
sound.reproductor.set_time_base(0.04)
sound.reproductor.set_max_freq(1500)

#Calculo valor de la columna normalizado
for j in range(0,gray_img.shape[1]):
    column = gray_img[:, j:j+1]
    for i in range(0,column.shape[0]):
        if i==0:
            suma = int(column[i,0])
        else:
            suma = suma + int(column[i,0])
    value = (suma/column.shape[0])/column.max()
    # generate the numpy array to save the sound
    if j == 0:
        x = np.array([j])
        y = np.array([value])
    else:
        x = np.append(x,j)
        y = np.append(y,value)
    new_img = img.copy()
    cv.line(new_img,(j,0),((j),gray_img.shape[0]),(255,0,0),5)
    cv.imshow('Windows', new_img)
    k = cv.waitKey(33)
    sound.make_sound(value, 1)
    time.sleep(0.02)
    if k==27:    # Esc key to stop
        break
    if j == gray_img.shape[1]-1:
        break

path_wav = path[:-4] + '_sound.wav'
# path_mp3 = path[:-4] + '_sound.mp3'
sound.save_sound(path_wav, x, y)
# wav_to_mp3(path_wav, path_mp3)

cv.destroyAllWindows()
