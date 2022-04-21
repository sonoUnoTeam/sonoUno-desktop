# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:04:39 2022

@author: Johanna
"""

import numpy as np
import cv2 as cv
import time
from sound_module.simple_sound import simpleSound

img = cv.imread('blip.png')
img = cv.resize(img, (960, 540))

gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# print(gray_img.shape)
# column = gray_img[0:223, 0:226]

# Para mostrar la imagen
# cv.imshow('Corazon', img)
# cv.waitKey(0)
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


cv.destroyAllWindows()
