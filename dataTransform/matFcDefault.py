# -*- coding: utf-8 -*-

import numpy as np
from dataExport.dataExport import dataExport as eErr

class matFcDefault (object):
    def __init__(self):
        #instancia de la clase dataExport para imprimir los print y los errores en los archivos correspondientes
        self.expErr = eErr()
    
    def normalizar(self, dataX, dataY):
        #normalización de la tabla de valores
        newDataX = dataX
        #normalización por escalado de variables (Feature Scaling o MinMax Scaler)
        try:
            newDataY = ((dataY - np.amin(dataY)) / (np.amax(dataY) - np.amin(dataY)))
        except Exception as e:
            self.expErr.writeException(e)
        #normalización por escalado estándar (Standard Scaler)
        #no es viable porque no queda entre 0 y 1
        #self.newDataY = (dataY - np.mean(dataY)) / np.std(dataY)
        return newDataX, newDataY
    
    def mfOriginal (self, x, y):
        return x, y
    
    def mfInverse (self, x, y):
        try:
            xStandard = x
            yStandard = (np.amax(y) - y) + np.amin(y)
            print (y)
            print (yStandard)
        except Exception as e:
            self.expErr.writeException(e)
        return xStandard, yStandard
    
    def mfSquare (self, x, y):
        try:
            yStandard = np.square(y)
        except Exception as e:
            self.expErr.writeException(e)
        return x, yStandard
    
    def mfSquareRot (self, x, y):
        try:
            yStandard = np.sqrt(y)
        except Exception as e:
            self.expErr.writeException(e)
        return x, yStandard
    
    def mfLog (self, x, y):
        try:
            for j in range (0, y.size):
                if not y[j]==0:
                    yValue = np.log10(y[j])
                    if np.isposinf(yValue):
                        yValue = 1
                    if np.isneginf(yValue):
                        yValue = 0
                else:
                    yValue=0
                    self.expErr.printOutput("The Logarithm of 0 don't exist.")
                if j==0:
                    ylog = np.array([yValue])
                else:
                    ylog = np.append(ylog, [yValue], axis=0)
        except Exception as e:
            self.expErr.writeException(e)
        return x, ylog
    
    def mfAverage (self, x, y, pointsNumber):        
        conter = 0
        valueSum = 0
        index = 0
        try:
            for j in range (0, y.size):
                conter = conter + 1
                valueSum = valueSum + y[j]
                if (conter == pointsNumber):
                    average = valueSum / conter
                    for a in range (0, conter):
                        if index == 0:
                            yStandard = np.array([average])
                        else:
                            yStandard = np.append(yStandard, [average], axis=0)
                        index = index + 1
                    conter = 0
                    valueSum = 0
        except Exception as e:
            self.expErr.writeException(e)
        try:
            if conter != 0:
                average = valueSum / conter
                for b in range (0, conter):
                    if index == 0:
                        yStandard = np.array([average])
                    else:
                        yStandard = np.append(yStandard, [average], axis=0)
                    index = index + 1
                conter = 0
                valueSum = 0
        except Exception as e:
            self.expErr.writeException(e)
        try:
            yStandard = (yStandard - np.amin(yStandard)) / (np.amax(yStandard) - np.amin(yStandard))
        except Exception as e:
            self.expErr.writeException(e)
        return x, yStandard