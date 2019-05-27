# -*- coding: utf-8 -*-

import wx
import numpy as np
import pandas as pd
import math

from dataExport.dataExport import dataExport as eErr

class dataImport (object):
    def __init__ (self):
        #instancia de la clase dataExport para imprimir los print y los errores en los archivos correspondientes
        self.expErr = eErr()
        #variables globales para guardar datos entre dos llamados a los metodos.
        self.prevPath = ' '
        self.prevFileTipe = ' '
        self.prevSFPath = ' '
        self.prevMFilePath = ' '
        self.del_xy = np.array([0,1])
        
        self.setDataFileName(' ')
        self.setXLabel(' ')
        self.setYLabel(' ')
        
    def setDataFileName(self, fileName):
        self.fileName = fileName
        
    def setXLabel(self, xlabel):
        self.xLabel = xlabel
        
    def setYLabel(self, ylabel):
        self.yLabel = ylabel
        
    def getDataFileName(self):
        return self.fileName
        
    def getXLabel(self):
        return self.xLabel
    
    def getYLabel(self):
        return self.yLabel
        
    #metodo encargado de obtener la ruta donde se encuentra el archivo de datos.
    def getDataPath (self):
        try:
            #se despliega una ventana emergente para buscar el archivo deseado.
            with wx.FileDialog(None, "Open data file", wildcard="Data files |*.txt;*.csv", 
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                #Si se preciona el boton cancel, se devuelven los path anteriores
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return self.prevPath, self.prevFileTipe
                else:
                    #sino, se procede a guardar la ruta seleccionada por el usuario.
                    pathName = fileDialog.GetPath()
                    #se guarda ademas el nombre del archivo, para utilizarlo luego como titulo.
                    fileName = fileDialog.GetFilename()
                    self.setDataFileName(fileName)
                    #Chequea la extensión para devolver además si se importo un archivo csv, txt u otro.
                    if pathName[-4:] == ".txt":
                        fileTipe = "txt"
                    else:
                        if pathName[-4:] == ".csv":
                            fileTipe = "csv"
                        else:
                            fileTipe = "otro"
                    #Se actualizan las variables que guardan la ruta para la proxima vez.
                    self.prevPath=pathName
                    self.prevFileTipe=fileTipe
        except Exception as e:
            self.expErr.writeException(e)
        #Devuelve la ruta donde se encuentra el archivo y el tipo de datos.
        return pathName, fileTipe
    
    def getSFPath (self):
        try:
            with wx.FileDialog(None, "Open data file", wildcard="Data files |*.sf2", 
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return self.prevSFPath    # the user changed their mind
                else:
                    # Proceed loading the file chosen by the user
                    pathName = fileDialog.GetPath()
                    self.prevSFPath=pathName
        except Exception as e:
            self.expErr.writeException(e)
        return pathName
    
    def getMFilePath (self):
        try:
            with wx.FileDialog(None, "Open M file", wildcard="Data files |*.m", 
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return None    # the user changed their mind
                else:
                    # Proceed loading the file chosen by the user
                    pathName = fileDialog.GetPath()
        except Exception as e:
            self.expErr.writeException(e)
            return None
        return pathName
    
    def getMDirPath (self):
        try:
            with wx.DirDialog(None, "Choose m files folder.", "", 
                               style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dirDialog:
                if dirDialog.ShowModal() == wx.ID_CANCEL:
                    return self.prevMFilePath    # the user changed their mind
                else:
                    # Proceed loading the file chosen by the user
                    pathName = dirDialog.GetPath()
                    self.prevMFilePath=pathName
        except Exception as e:
            self.expErr.writeException(e)
        return pathName
    
    def setXY_txt(self, archivo):
        delNum=False
        try:
            txt_x = np.genfromtxt(archivo, dtype=None, delimiter='\t', usecols=[0])#, encoding='UTF-8')
            txt_y = np.genfromtxt(archivo, dtype=None, delimiter='\t', usecols=[1])#, encoding='UTF-8')
        except ValueError:
            try:
                txt_x = np.genfromtxt(archivo, dtype=None, delimiter=' ', usecols=[0])#, encoding='UTF-8')
                txt_y = np.genfromtxt(archivo, dtype=None, delimiter=' ', usecols=[1])#, encoding='UTF-8')
            except IOError as e:
                wx.LogError("Cannot open file.")
                self.expErr.writeException(e)
            except Exception as e:
                self.expErr.writeException(e)
        except IOError as e:
            wx.LogError("Cannot open file.")
            self.expErr.writeException(e)
        except Exception as e:
            self.expErr.writeException(e)
        try:
            if type(txt_x[0]) == np.string_:
                txt_xLabel = txt_x[0]
                txt_yLabel = txt_y[0]
                if len(txt_xLabel)>10:
                    txt_xLabel=txt_xLabel[:10]
                if len(txt_yLabel)>10:
                    txt_yLabel=txt_yLabel[:10]
                data_x = txt_x[1:]
                data_y = txt_y[1:]
                data_x = data_x.astype(np.float64)
                data_y = data_y.astype(np.float64)
            else:
                data_x = txt_x.astype(np.float64)
                data_y = txt_y.astype(np.float64)
                txt_xLabel = "x_def_value"
                txt_yLabel = "y_def_value"
        except Exception as e:
            self.expErr.writeException(e)
        try:
            index1 = [i for i in range(0, len(self.del_xy))]
            if not self.del_xy.size==0:
                self.del_xy=np.delete(self.del_xy,index1)
        except Exception as e:
            self.expErr.writeException(e)
        try:
            for i in range (0, data_x.size):
                #if data_x[i] == nan or data_y[i] == nan:
                if math.isnan(data_x[i]) or math.isnan(data_y[i]):
                    self.del_xy = np.append(self.del_xy, i)
                    delNum=True
        except Exception as e:
            self.expErr.writeException(e)
        try:
            if delNum:
                text="Algunos puntos se han importado vacios y han tenido que eliminarse. Los mismos estaban en las direcciones: ["
                for i in range (0, self.del_xy.size):
                    if i != (self.del_xy.size-1):
                        text=text+str(self.del_xy[i]+1)+" ; "
                    else:
                        text=text+str(self.del_xy[i]+1)
                text=text+"] del archivo original."
                wx.MessageBox(text, 
                              'Info', wx.OK | wx.ICON_INFORMATION)
                delNum=False
                data_x=np.delete(data_x, self.del_xy)
                data_y=np.delete(data_y, self.del_xy)
        except Exception as e:
            self.expErr.writeException(e)
        try:
            self.setXLabel(txt_xLabel)
            self.setYLabel(txt_yLabel)
        except Exception as e:
            self.expErr.writeException(e)
        return data_x, data_y

    def setXY_csv(self, archivo):
        delNum=False
        try:
            with open (archivo,'r') as csvfile:
                csv_data = np.genfromtxt(csvfile, dtype = None, delimiter = ',', encoding=None)
        except IOError as e:
            wx.LogError("Cannot open file.")
            self.expErr.writeException(e)
        except Exception as e:
            self.expErr.writeException(e)
        #chequeo si se importó bien, sino se intenta importar como separado por ;
        try:
            print(csv_data[:,0])
        except IndexError as e:
            error = str(e)
            if not error.find("too many indices for array") == -1:
                self.expErr.printOutput("Maybe the csv file is separated by ;.")
                try:
                    with open (archivo,'r') as csvfile:
                        csv_data = np.genfromtxt(csvfile, dtype = None, delimiter = ';', encoding=None)
                except Exception as e:
                    self.expErr.writeException(e)
            else:
                self.expErr.writeException(e)
        except Exception as e:
            self.expErr.writeException(e)
        try:    
            csv_x1, csv_y1 = np.hsplit(csv_data, 2)
        except Exception as e:
            self.expErr.writeException(e)
        
        #chequeo si la primer fila contiene caracteres:
        try:
            float(csv_x1[0])
            float(csv_y1[0])
            data_xLabel = "default_x"
            data_yLabel = "default_y"
            csv_x=csv_x1.astype(np.float64)
            csv_y=csv_y1.astype(np.float64)
        except ValueError as e:
            error = str(e)
            if not error.find("could not convert string to float") == -1:
                self.expErr.printOutput("The first values are the label of each column.")
                data_xLabel = str(csv_x1[0])
                data_yLabel = str(csv_y1[0])
                csv_x=csv_x1[1:].astype(np.float64)
                csv_y=csv_y1[1:].astype(np.float64)
            else:
                self.expErr.writeException(e)
        except TypeError as e:
            error = str(e)
            if not error.find("don't know how to convert scalar number to float") == -1:
                self.expErr.printOutput("The first values are the label of each column.")
                data_xLabel = str(csv_x1[0])
                data_yLabel = str(csv_y1[0])
                csv_x=csv_x1[1:].astype(np.float64)
                csv_y=csv_y1[1:].astype(np.float64)
            else:
                self.expErr.writeException(e)
        except Exception as e:
            self.expErr.writeException(e)
        
        #chequeo de valores nan
        try:
            index1 = [i for i in range(0, len(self.del_xy))]
            if not self.del_xy.size==0:
                self.del_xy=np.delete(self.del_xy,index1)
        except Exception as e:
            self.expErr.writeException(e)
        
        try:
            for i in range (0, csv_x.size):
                #if csv_x[i] == nan or csv_y[i] == nan:
                if math.isnan(csv_x[i]) or math.isnan(csv_y[i]):
                    self.del_xy = np.append(self.del_xy, i)
                    delNum=True
        except Exception as e:
            self.expErr.writeException(e)
        
        try:
            if delNum:
                text="Algunos puntos se han importado vacios y han tenido que eliminarse. Los mismos estaban en las direcciones: ["
                for i in range (0, self.del_xy.size):
                    if i != (self.del_xy.size-1):
                        text=text+str(self.del_xy[i]+1)+" ; "
                    else:
                        text=text+str(self.del_xy[i]+1)
                text=text+"] del archivo original."
                wx.MessageBox(text, 
                              'Info', wx.OK | wx.ICON_INFORMATION)
                delNum=False
                csv_x=np.delete(csv_x, self.del_xy)
                csv_y=np.delete(csv_y, self.del_xy)
        except Exception as e:
            self.expErr.writeException(e)
        try:
            self.setXLabel(data_xLabel)
            self.setYLabel(data_yLabel)
        except Exception as e:
            self.expErr.writeException(e)
        try:
            csv_x=np.concatenate(csv_x)
            csv_y=np.concatenate(csv_y)
        except Exception as e:
            self.expErr.writeException(e)
        return csv_x, csv_y
    
    def setArraysFromTxt (self, archivo):
        try:
            with open (archivo,'r') as txtfile:
                txt_data = pd.read_csv(txtfile, delimiter='\t', header=None)
            importData = True
        except IOError as e:
            importData = False
            txt_data=None
            wx.LogError("Cannot open file.")
            self.expErr.writeException(e)
        except Exception as e:
            importData = False
            txt_data=None
            self.expErr.writeException(e)
        if importData:
            #chequeo si se importó bien, sino se intenta importar como separado por ;
            if txt_data.shape[1] < 2:
                with open (archivo,'r') as txtfile:
                    txt_data = pd.read_csv(txtfile, sep=' ', header=None)
                if txt_data.shape[1] < 2:
                    self.expErr.printOutput('Check the delimiter on the data, txt separator must be \'\t\' or \' \'.')
            status=True
        else:
            status=False
        return txt_data, status

    def setArraysFromCsv (self, archivo):
        try:
            with open (archivo,'r') as csvfile:
                #csv_data = np.genfromtxt(csvfile, dtype = None, delimiter = ',', encoding=None)
                csv_data = pd.read_csv(csvfile, delimiter=',', header=None)
            importData = True
        except IOError as e:
            importData = False
            wx.LogError("Cannot open file.")
            self.expErr.writeException(e)
        except Exception as e:
            importData = False
            self.expErr.writeException(e)
        #chequeo si se importó bien, sino se intenta importar como separado por ;
        if importData:
            if csv_data.shape[1] < 2:
                with open (archivo,'r') as csvfile:
                    csv_data = pd.read_csv(csvfile, sep=';', header=None)
                if csv_data.shape[1] < 2:
                    self.expErr.printOutput('Check the delimiter on the data, csv separator must be \',\' or \';\'.')
            status=True
        else:
            status=False
        return csv_data, status