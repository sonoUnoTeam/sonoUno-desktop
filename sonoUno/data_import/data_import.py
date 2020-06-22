#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Dec 12 2017

@author: sonounoteam (view licence)
"""

import numpy as np
import pandas as pd
import wx

from data_export.data_export import DataExport


class DataImport(object):


    def __init__(self):

        """
        This class allow to get the paths of the files to open and import
        this files to the programm.
        """        
        # The class DataExport is instantiated to print the messages and 
        # errors.
        self._export_error_info = DataExport()
        # Parameters to save the previous data of the method's use.
        self._prevpath = ''
        self._prevfiletipe = ''
        self._prev_m_filepath = ''
        self._del_xy = np.array([0,1])
        # Parameters initialization with setter methods
        self.set_datafilename('')
        
    def set_datafilename(self, filename): 
        
        """
        This method set the internal filename of the data opened.
        It not modify the file on the operative system.
        """
        self._filename = filename
        
    def get_datafilename(self): 
        
        """
        This method return the file name of the data imported.
        """
        return self._filename
        
    def get_datapath(self):
        
        """
        This method return the path of the data to import and the file type.
        
        Check if the path and file type is not empty, if is empty through a
        message to the user, because there is no data imported.
        
        A state value is added to return, this is false if the process
        through an exception.
        """
        try:
            # This generate a pop-up window where the user serch the file.
            with wx.FileDialog(
                    parent = None, 
                    message = 'Open data file', 
                    wildcard = 'Data files |*.txt;*.csv', 
                    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
                    ) as filedialog:
                if filedialog.ShowModal() == wx.ID_CANCEL:
                    return self._prevpath, self._prevfiletipe, True
                else:
                    # We save the path selected by the user and the file name.
                    path = filedialog.GetPath()
                    self.set_datafilename(filedialog.GetFilename())
                    # Check the file extention and save it as the file type.
                    if path.endswith('.txt'): 
                        filetipe = 'txt'
                    elif path.endswith('.csv'): 
                        filetipe = 'csv'
                    else:
                        filetipe = 'other'
                    # We update the previous parameters.
                    self._prevpath = path
                    self._prevfiletipe = filetipe
                    return path, filetipe, True
        except Exception as Error:
            self._export_error_info.writeexception(Error)
            return self._prevpath, self._prevfiletipe, False
    
    def get_m_filepath(self):
        
        """
        This method return the path to one m file selected by the user.
        
        Check if the string is None (the user change their mind) or 'Error'
        (the method through an error.).
        """
        try:
            with wx.FileDialog(
                    parent = None, 
                    message = 'Open M file', 
                    wildcard = 'Data files |*.m', 
                    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
                    ) as filedialog:
                if filedialog.ShowModal() == wx.ID_CANCEL:
                    return None
                else:
                    path = filedialog.GetPath()
                    filename = filedialog.GetFilename()
                    return path, filename
        except Exception as Error:
            self._export_error_info.writeexception(Error)
            return 'Error'
    
    def get_m_dirpath(self):
        
        """
        This method return the path to the directory that the user select.
        
        Check if the string is empty (the user change his mind and is the
        first time that the software open a directory of m files) or 'Error'
        (the method through an error.).
        """
        try:
            with wx.DirDialog(
                    parent = None, 
                    message = 'Choose m files folder.', 
                    defaultPath = '', 
                    style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
                    ) as dirdialog:
                if dirdialog.ShowModal() == wx.ID_CANCEL:
                    return self._prev_m_filepath
                else:
                    path = dirdialog.GetPath()
                    self._prev_m_filepath = path
                    return path
        except Exception as Error:
            self._export_error_info.writeexception(Error)
            return 'Error'

    def set_arrayfromfile(self, archivo, filetype):
        
        """
        This method import a txt or csv data file into a dataFrame, check 
        if the columns have names if not one generic name is set, and check 
        that the names don't have spaces, if there is any space the program
        delete it.
        """
        if filetype == 'txt':
            try:
                with open (archivo, 'r') as txtfile:
                    data = pd.read_csv(txtfile, delimiter = '\t', header = None)
            except IOError as Error:
                msg = 'Cannot open the txt file, this is an IO Error. \
                    Check the error file for more information.'
                wx.LogError(msg)
                self._export_error_info.writeexception(Error)
                return None, False, msg
            except Exception as Error:
                msg = 'Cannot open the txt file. Check the error file for \
                    more information.'
                self._export_error_info.writeexception(Error)
                return None, False, msg
            # Check if the data are imported in the right way, if not try to
            # import as space separated.
            if data.shape[1] < 2:
                with open (archivo, 'r') as txtfile:
                    data = pd.read_csv(txtfile, sep = ' ', header = None)
                if data.shape[1] < 2:
                    msg = 'Check the delimiter on the data, txt separator \
                        must be "\t" or " ".'
                    self._export_error_info.printoutput(msg)
                    return None, False, msg
        elif filetype == 'csv':
            try:
                with open (archivo, 'r') as csvfile:
                    data = pd.read_csv(csvfile, delimiter = ',', header = None)
            except IOError as Error:
                msg = 'Cannot open the csv file, this is an IO Error. \
                    Check the error file for more information.'
                wx.LogError(msg)
                self._export_error_info.writeexception(Error)
                return None, False, msg
            except Exception as Error:
                msg = 'Cannot open the txt file. Check the error file for \
                    more information.'
                self._export_error_info.writeexception(Error)
                return None, False, msg
            # Check if the data are imported in the right way, if not try to
            # import as ; separated.
            if data.shape[1] < 2:
                with open (archivo, 'r') as csvfile:
                    data = pd.read_csv(csvfile, sep = ';', header = None)
                if data.shape[1] < 2:
                    msg = 'Check the delimiter on the data, csv separator \
                        must be "," or ";".'
                    self._export_error_info.printoutput(msg)
                    return None, False, msg
        else:
            msg = 'The data type provided is unknow.'
            self._export_error_info.printoutput(msg)
            return None, False, msg
        # If the data are imported correctly, continue checking the columns
        # names.
        if type(data.loc[0,0]) is not str:
            # Walk the first row and set generic column names
            for i in range (0, data.shape[1]):
                if i == 0:
                    xlabel = pd.DataFrame({i : ['Column'+str(i)]})
                else:
                    xlabel.loc[:, i] = 'Column' + str(i)
            data = pd.concat([xlabel, data]).reset_index(drop = True)
        # This part check if the column names present spaces and if it has, 
        # it delete it.
        for i in range (0, data.shape[1]):
            data.iloc[0,i] = data.iloc[0,i].replace(' ','')
        msg = 'The data was correctly imported.'
        return data, True, msg
