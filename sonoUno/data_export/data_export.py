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


class DataExport(object):


    def __init__(self, log=False):

        """
        This class allow to export data and save the outputs of the software.
        First save the time and then create the error and output file.
        """
        self.log = log
        if self.log:
            # Save the home directory to append to output folder
            homepath = str(Path.home())
            # Create the string with the time to create the output file.
            now = datetime.datetime.now()
            time = now.strftime('%Y-%m-%d_%H-%M-%S')
            # Create error variable to store posible errors in the save process
            error_loggingfiles = ''
            # Create the errors file depending on the operative system.
            try:
                if platform.system() == 'Windows':
                    logging.basicConfig(
                        filename=(homepath + '\\sonouno\\output\\err_' + time 
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
                    error_loggingfiles = (time + ': The operative system is unknown and the \
                        error file could not be created.')
                    print(error_loggingfiles)
                    
                    # I have to print this messages in the future.
                    # wx.MessageBox(
                    #     message = error,
                    #     caption = 'Error creating error file', 
                    #     style = wx.OK|wx.ICON_INFORMATION
                    #     )
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
                        error_loggingfiles = (time + (': The operative system is unknown and \
                            the error file could not be created.'))
                        print(error_loggingfiles)
                        # wx.MessageBox(
                        #     message = error,
                        #     caption = 'Error creating error file', 
                        #     style = wx.OK|wx.ICON_INFORMATION
                        #     )
                else:
                    error_loggingfiles = (time + ': Error generating the error file. The error\
                        message is: \n' + exception_error)
                    print(error_loggingfiles)
                    # wx.MessageBox(
                    #     message = error,
                    #     caption = 'Error creating error file', 
                    #     style = wx.OK|wx.ICON_INFORMATION
                    #     )
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
                    error_loggingfiles = (time + ': The operative system is unknown,the \
                        output file could not be created.')
                    print(error_loggingfiles)
                    # wx.MessageBox(
                    #     message = error,
                    #     caption = 'Error creating error file', 
                    #     style = wx.OK|wx.ICON_INFORMATION
                    #     )
            except Exception as Error:   
                # Catch the problem and print it.
                error_loggingfiles = (time + ': Error generating the output file. The error\
                    message is: \n' + str(Error))
                print(error_loggingfiles)
                # wx.MessageBox(
                #     message = error,
                #     caption = 'Error creating output file', 
                #     style = wx.OK|wx.ICON_INFORMATION
                #     )
    
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
        if self.log:
            logging.info(msg)
        else:
            print(msg)
        
    def writeexception(self, e):
        
        """
        This method print errors on the error file.
        """
        now = datetime.datetime.now()
        time = now.strftime('%H-%M-%S')
        info_msj = 'The time of the next exception is: ' + time
        if self.log:
            logging.info(info_msj)
            logging.exception(e)
        else:
            print(info_msj)
            print(e)
        
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
    
    def writepointfile(self, x, y, savepath):
        
        """
        This method save the file with the coordinates of the points that 
        the user marked on the data and in the path indicated.
        
        Return one state variables, filestatus to check if the 
        file has been saved. You must check if is true.
        """
        filestatus = False
        # Save the file using the pandas library.
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
        return filestatus
