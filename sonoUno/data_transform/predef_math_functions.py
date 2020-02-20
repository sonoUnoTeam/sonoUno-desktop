#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Dec 12 2017

@author: sonounoteam (view licence)
"""

import numpy as np

from data_export.data_export import DataExport


class PredefMathFunctions(object):


    def __init__(self):
        
        """
        This class perform some predefined mathematical functions on the data.
        """
        # DataExport instance to save the error and messages on the output
        # and error files.
        self._export_error_info = DataExport()
    
    def normalize(self, data_x, data_y):

        """
        This method normalize the data provided between 0 and 1 with the
        Feature Scaling method. The changes are applied to the y variable.
        
        This method return the new data with a true status or the unchanged
        data with false status.
        """
        # Normalization by variable scaling (Feature Scaling o MinMax Scaler)
        # The standardization by standard scaling (Standard Scaler) is not 
        # posible because the data is not between 0 and 1. The Standard Scaler
        # operation is:
        # self.new_y = (data_y-np.mean(data_y)) / np.std(data_y)
        try:
            new_y = ((data_y-np.amin(data_y)) 
                / (np.amax(data_y)-np.amin(data_y)))
            return data_x, new_y, True
        except Exception as Error:
            self._export_error_info.writeexception(Error)
            return data_x, data_y, False
    
    def square(self, x, y):
        
        """
        This method apply the square function to the data provided. The 
        changes are applied to the y variable.
        
        This method return the new data with a true status or the unchanged
        data with false status.
        """
        try:
            new_y = np.square(y)
            return x, new_y, True
        except Exception as Error:
            self._export_error_info.writeexception(Error)
            return x, y, False
    
    def squareroot(self, x, y):
        
        """
        This method apply the square root function to the data provided. The 
        changes are applied to the y variable.
        
        This method return the new data with a true status or the unchanged
        data with false status.
        """
        try:
            new_y = np.sqrt(y)
            return x, new_y, True
        except Exception as Error:
            self._export_error_info.writeexception(Error)
            return x, y, False
        
    def logarithm(self, x, y):
        
        """
        This method apply the logarithm function to the data provided. The 
        changes are applied to the y variable.
        
        This method return the new data with a true status or the unchanged
        data with false status.
        
        The logarithm method applied ignore the #o values and maintain this
        value on the array, assign #0 to negative infinitive values and 
        assign #1 to positive infinitive values.
        """
        try:
            new_y = np.log10(y)
            new_y = np.where(np.isnan(new_y), 0, new_y)
            new_y = np.where(np.isneginf(new_y), 0, new_y)
            new_y = np.where(np.isposinf(new_y), 1, new_y)
            return x, new_y, True
        except Exception as Error:
            self._export_error_info.writeexception(Error)
            return x, y, False
    
    def average(self, x, y, pointsnumber):
        
        """
        This method apply the average function to the data provided. The 
        changes are applied to the y variable.
        
        This method return the new data with a true status or the unchanged
        data with false status.
        
        This operation is performed with for bucle, take into account that
        this can delay the operation when a large data is imported.
        """
        conter = 0
        sumvalue = 0
        index = 0
        try:
            for j in range (0, y.size):
                conter = conter + 1
                sumvalue = sumvalue + y[j]
                if (conter == pointsnumber):
                    average = sumvalue / conter
                    for a in range (0, conter):
                        if index == 0:
                            new_y = np.array([average])
                        else:
                            new_y = np.append(new_y, [average], axis=0)
                        index = index + 1
                    conter = 0
                    sumvalue = 0
        except Exception as Error:
            self._export_error_info.writeexception(Error)
            return x, y, False
        try:
            if conter != 0:
                average = sumvalue / conter
                for b in range (0, conter):
                    if index == 0:
                        new_y = np.array([average])
                    else:
                        new_y = np.append(new_y, [average], axis=0)
                    index = index + 1
                conter = 0
                sumvalue = 0
        except Exception as Error:
            self._export_error_info.writeexception(Error)
            return x, y, False
        try:
            new_y = ((new_y - np.amin(new_y)) 
                / (np.amax(new_y) - np.amin(new_y)))
            return x, new_y, True
        except Exception as Error:
            self._export_error_info.writeexception(Error)
            return x, y, False