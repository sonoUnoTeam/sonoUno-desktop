# -*- coding: utf-8 -*-

import platform
import logging
import sys
import pandas as pd
import wx
import os
import datetime
#from oct2py import Oct2Py, get_log


class dataExport (object):
    def __init__(self):
        
#        #To print from oct2py
#        self.oc = Oct2Py(logger=get_log())
#        self.oc.logger = get_log('new_log')
#        self.oc.logger.setLevel(logging.DEBUG)
        
        #crear archivo para salvar errores
        self.now = datetime.datetime.now()
        time = self.now.strftime("%Y-%m-%d_%H-%M-%S")
        try:
            #logging.basicConfig(filename=('err_'+time+'.log'), filemode='w+', level=logging.DEBUG)
            #logging.basicConfig(filename='errFile.log', filemode='w+', level=logging.DEBUG)
            if platform.system() == 'Windows':
                logging.basicConfig(filename=('output\err_'+time+'.log'), filemode='w+', level=logging.DEBUG)
                #logging.basicConfig(filename='output\errFile.log', filemode='w+', level=logging.DEBUG)
            else:
                if platform.system() == 'Linux':
                    logging.basicConfig(filename=('output/err_'+time+'.log'), filemode='w+', level=logging.DEBUG)
                    #logging.basicConfig(filename='output/errFile.log', filemode='w+', level=logging.DEBUG)
                else:
                    if platform.system() == 'Darwin':
                        logging.basicConfig(filename=('output/err_'+time+'.log'), filemode='w+', level=logging.DEBUG)
                        #logging.basicConfig(filename='output/errFile.log', filemode='w+', level=logging.DEBUG)
                    else:
                        print(time+": El sistema operativo es desconocido (errFile).")
        except Exception as e:    
            error = str(e)
            if not error.find("No such file or directory") == -1:
                os.makedirs('output')
                if platform.system() == 'Windows':
                    logging.basicConfig(filename=('output\err_'+time+'.log'), filemode='w+', level=logging.DEBUG)
                    #logging.basicConfig(filename='output\errFile.log', filemode='w+', level=logging.DEBUG)
                else:
                    if platform.system() == 'Linux':
                        logging.basicConfig(filename=('output/err_'+time+'.log'), filemode='w+', level=logging.DEBUG)
                        #logging.basicConfig(filename='output/errFile.log', filemode='w+', level=logging.DEBUG)
                    else:
                        if platform.system() == 'Darwin':
                            logging.basicConfig(filename=('output/err_'+time+'.log'), filemode='w+', level=logging.DEBUG)
                            #logging.basicConfig(filename='output/errFile.log', filemode='w+', level=logging.DEBUG)
                        else:
                            print(time+": El sistema operativo es desconocido (errFile).")
            else:
                print (time+": Error al generar el archivo log")
                print (time+": "+e)
        try:
            #sys.stdout = open(('out_'+time+'.log'), 'w+')
            #sys.stdout = open('outputFile.log', 'w+')
            if platform.system() == 'Windows':
                sys.stdout = open(('output\out_'+time+'.log'), 'w+')
                #sys.stdout = open('output\outputFile.log', 'w+')
            else:
                if platform.system() == 'Linux':
                    sys.stdout = open(('output/out_'+time+'.log'), 'w+')
                    #sys.stdout = open('output/outputFile.log', 'w+')
                else:
                    if platform.system() == 'Darwin':
                        sys.stdout = open(('output/out_'+time+'.log'), 'w+')
                        #sys.stdout = open('output/outputFile.log', 'w+')
                    else:
                        print(time+": El sistema operativo es desconocido, no se pudo crear el outputFile.")
        except:
            print (time+": Error al generar el archivo para imprimir consola")
    
    #metodo para imprimir informacion    
    def writeInfo(self, info):
        self.now = datetime.datetime.now()
        time = self.now.strftime("%H-%M-%S")
        logging.info("The time of the next information is: "+time+"\n"+info)
        
    #metodo para imprimir errores
    def writeException(self, e):
        self.now = datetime.datetime.now()
        time = self.now.strftime("%H-%M-%S")
        logging.info("The time of the next exception is: "+time)
        logging.exception(e)
        
    #método para imprimir en el archivo de salida
    def printOutput(self, message):
        self.now = datetime.datetime.now()
        time = self.now.strftime("%H-%M-%S")
        print(time+": "+message)
        
    #método para guardar archivo con puntos marcados        
    def writePointFile(self, x, y):
        path = False
        fileStatus = False
        try:
            savePath = self.setPath("Save data file", "Data files |*.csv")
            path = True
        except Exception as e:
            self.writeException(e)
        try:        
            param = pd.DataFrame({'x': x, 'y': y}, columns=['x', 'y'])
            param.to_csv(savePath, sep=',', index=0)
            fileStatus = True
        except Exception as e:
            self.writeException(e)
        return path, fileStatus

    #Se prueba con un solo método que pide el título y el tipo de dato
    def setPath (self, title, dataTipe):
        try:
            with wx.FileDialog(None, title, wildcard=dataTipe, 
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return "Empty"    # the user changed their mind
                # Proceed loading the file chosen by the user
                pathName = fileDialog.GetPath()
        except Exception as e:
            self.writeException(e)
        return pathName
