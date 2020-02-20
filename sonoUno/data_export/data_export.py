#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Dec 12 2017

@author: sonounoteam (view licence)
"""

import platform
import logging
import sys
import os
import datetime
from pathlib import Path

import pandas
import wx


class DataExport(object):

    
    def __init__(self):
        
        """
        This class allow to export data and save the outputs of the software.
        First save the time and then create the error and output file.
        """
        # Save the home directory to append to output folder
        homepath = str(Path.home())
        # Create the string with the time to create the output file.
        now = datetime.datetime.now()
        time = now.strftime('%Y-%m-%d_%H-%M-%S')
        # Create the errors file depending on the operative system.
        try:
            if platform.system() == 'Windows':
                logging.basicConfig(
                    filename = (homepath + '\\sonouno\\output\\err_' + time 
                        + '.log'), 
                    filemode = 'w+', 
                    level = logging.DEBUG
                    )
            elif platform.system() == 'Linux':
                logging.basicConfig(
                    filename = (homepath + '/sonouno/output/err_' + time 
                        + '.log'), 
                    filemode = 'w+', 
                    level = logging.DEBUG
                    )
            elif platform.system() == 'Darwin':
                logging.basicConfig(
                    filename = (homepath + '/sonouno/output/err_' + time 
                        + '.log'), 
                    filemode = 'w+', 
                    level = logging.DEBUG
                    )
            else:
                error = (time + ': The operative system is unknown and the \
                    error file could not be created.')
                print(error)
                wx.MessageBox(
                    message = error,
                    caption = 'Error creating error file', 
                    style = wx.OK|wx.ICON_INFORMATION
                    )
        except Exception as Error:   
            # Checking if the problem is that the software don't find the
            # output folder. If this is the problem, we create the folder
            # and try again.
            exception_error = str(Error)
            if exception_error.find('No such file or directory') is not -1 or exception_error.find('No existe el archivo o el directorio') is not -1:
                if platform.system() == 'Windows':
                    os.makedirs(homepath + '\\sonouno\\output')
                    logging.basicConfig(
                        filename = (homepath + '\\sonouno\\output\\err_' + time
                            + '.log'), 
                        filemode = 'w+', 
                        level = logging.DEBUG
                        )
                elif platform.system() == 'Linux':
                    os.makedirs(homepath + '/sonouno/output')
                    logging.basicConfig(
                        filename = (homepath + '/sonouno/output/err_' + time 
                            + '.log'), 
                        filemode = 'w+', 
                        level = logging.DEBUG
                        )
                elif platform.system() == 'Darwin':
                    os.makedirs(homepath + '/sonouno/output')
                    logging.basicConfig(
                        filename = (homepath + '/sonouno/output/err_' + time 
                            + '.log'), 
                        filemode = 'w+', 
                        level = logging.DEBUG
                        )
                else:
                    error = (time + (': The operative system is unknown and \
                        the error file could not be created.'))
                    print(error)
                    wx.MessageBox(
                        message = error,
                        caption = 'Error creating error file', 
                        style = wx.OK|wx.ICON_INFORMATION
                        )
            else:
                error = (time + ': Error generating the error file. The error\
                    message is: \n' + exception_error)
                print(error)
                wx.MessageBox(
                    message = error,
                    caption = 'Error creating error file', 
                    style = wx.OK|wx.ICON_INFORMATION
                    )
        try:
            # Create the output file depending on the operative system.
            if platform.system() == 'Windows':
                sys.stdout = open(
                    file = (homepath + '\\sonouno\\output\\out_' + time 
                        + '.log'), 
                    mode = 'w+'
                    )
            elif platform.system() == 'Linux':
                sys.stdout = open(
                    file = (homepath + '/sonouno/output/out_' + time 
                        + '.log'), 
                    mode = 'w+'
                    )
            elif platform.system() == 'Darwin':
                sys.stdout = open(
                    file = (homepath + '/sonouno/output/out_' + time 
                        + '.log'), 
                    mode = 'w+'
                    )
            else:
                error = (time + ': The operative system is unknown,the \
                    output file could not be created.')
                print(error)
                wx.MessageBox(
                    message = error,
                    caption = 'Error creating error file', 
                    style = wx.OK|wx.ICON_INFORMATION
                    )
        except Exception as Error:   
            # Catch the problem and print it.
            error = (time + ': Error generating the output file. The error\
                message is: \n' + str(Error))
            print(error)
            wx.MessageBox(
                message = error,
                caption = 'Error creating output file', 
                style = wx.OK|wx.ICON_INFORMATION
                )
    
    def writeinfo(self, info):
        
        """
        This method print information on the error file.
        """
        now = datetime.datetime.now()
        time = now.strftime('%H-%M-%S')
        msg = ('The time of the next information is: '
            + time
            + '\n' 
            + info
            )
        logging.info(msg)
        
    def writeexception(self, e):
        
        """
        This method print errors on the error file.
        """
        now = datetime.datetime.now()
        time = now.strftime('%H-%M-%S')
        logging.info('The time of the next exception is: ' + time)
        logging.exception(e)
        
    def printoutput(self, message):
    
        """
        This method print messages on the output file.
        """
        now = datetime.datetime.now()
        time = now.strftime('%H-%M-%S')
        msg = (time
            + ': '
            + message)
        print(msg)
        
    def setpath(self, title, datatipe):
        
        """
        This method return the path that the user select to save a file, if 
        the user close or cancel the dialog return 'Empty' string and if the
        programm catch an error return 'Error' string.
        
        We asked the datatipe to do a generic method.
        """
        try:
            with wx.FileDialog(
                    parent = None, 
                    message = title, 
                    wildcard = datatipe, 
                    style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
                    ) as filedialog:
                if filedialog.ShowModal() == wx.ID_CANCEL:
                    return 'Empty'
                pathName = filedialog.GetPath()
        except Exception as Error:
            self.writeexception(Error)
            return 'Error'
        return pathName
    
    def writepointfile(self, x, y):
        
        """
        This method save the file with the coordinates of the points that 
        the user marked on the data. 
        
        Return two state variables, pathstatus and filestatus to check if the 
        file has been saved. You must check if is true.
        """
        pathstatus = False
        filestatus = False
        # First use the setpath method to have the detination of the file.
        try:
            savepath = self.setpath('Save data file', 'Data files |*.csv')
            pathstatus = True
        except Exception as Error:
            self.writeexception(Error)
        # Second save the file using the pandas library.
        try:        
            param = pandas.DataFrame({'x': x, 'y': y}, columns=['x', 'y'])
            param.to_csv(
                savepath, 
                sep=',', 
                index=0
                )
            filestatus = True
        except Exception as Error:
            self.writeException(Error)
        return pathstatus, filestatus
