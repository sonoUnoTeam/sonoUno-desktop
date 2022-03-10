#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mar 6 2022

@author: sonounoteam (view licence)
"""

from data_export.data_export import DataExport


class DataOpenedColumns(object):
    
    
    def __init__(self):
        
        """
        This class store and manage the data file opened by the software
        """
        # DataExport instance to save the error and messages on the output
        # and error files.
        self._export_error_info = DataExport()
        # Initializa the data variables with None to check possible errors 
        # after return
        self.set_dataframe(None, 'original')
        
    def set_dataframe(self, dataframe, whichone='actual'):
        """
        Parameters
        ----------
        set_dataframe(dataframe, whichone='actual')
            DESCRIPTION. The default is 'actual', the other option to save 
            also the original dataFrame is 'original'. With any other 
            parameter don't save anything and return a message.'

        Returns
        -------
        True: when the data was stored.
        False: when there were a problem.

        """
        if whichone == 'actual':
            self.dataframe = dataframe
            return True
        elif whichone == 'original':
            self.dataframe = dataframe
            self.original_dataframe = dataframe
            return True
        else:
            return False
        
    def get_dataframe(self, whichone='actual'):
        """
        Parameters
        ----------
        get_dataframe(whichone='actual')
            DESCRIPTION. The default is 'actual'. If you want to obtain the 
            original dataFrame you must indicate it with 'original'.

        Returns
        -------
        actual dataFrame
        original dataFrame
        None: when any other str was indicated.

        """
        if whichone == 'actual':
            return self.dataframe
        elif whichone == 'original':
            return self.original_dataframe
        else:
            return None