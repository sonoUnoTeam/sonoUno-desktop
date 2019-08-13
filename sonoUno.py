#!/usr/bin python2.7
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------
# 
#--------------------------------------------------------------------------------------

import platform
import wx
import numpy as np
from weakref import ref
import math
import pandas as pd
from wx.lib import dialogs
#from oct2py import octave
#import oct2py

import gui.design_origin as gui
from dataImport.dataImport import dataImport as oD
from soundModule.simpleSound import simpleSound as sound
from dataExport.dataExport import dataExport as dExport
from dataTransform.matFcDefault import matFcDefault

class core (gui.Sonorizador):
    def __init__(self):
        #clase de la cual hereda
        gui.Sonorizador.__init__(self)
        #instancias de clases
        self._expData = dExport()
        self._openData = oD()
        self._dataSound = sound()
        self._matFc = matFcDefault()
        #evento timer
        self._timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._sonoPlot, self._timer)
        #se genera una asignación de variable porque se utiliza mucho en esta clase.
        self.panel = self._axes

        self._pythonShell.Execute("from oct2py import octave")

        #we don't add soundFonts for now
        #self._sFontLabel = 'gm'
        try:
            if platform.system() == 'Windows':
                self._sFontChoice = "soundModule\soundFont\FluidR3_GM.sf2"
            else:
                if platform.system() == 'Linux':
                    self._sFontChoice = "soundModule/soundFont/FluidR3_GM.sf2"
                else:
                    if platform.system() == 'Darwin':
                        self._sFontChoice = "soundModule/soundFont/FluidR3_GM.sf2"
                    else:
                        self._expData.writeInfo("The operative system is unknown, the software can't set the sound font.")
        except Exception as e:
            self._expData.writeException(e)
        try:
            self._sFontTextCtrl.SetLabel("General MIDI")
        except Exception as e:
            self._expData.writeException(e)
        #self._soundFontChoice()
        try:
            self._dataSound.reproductor.openMidi(self._sFontChoice)
        except Exception as e:
            self._expData.writeException(e)
        
        #Variables globales de estado 
        self._lineExist = False
        self._plotCounter = 0
        self._fileSaved = False
        self._firstOpen = False
        self._xOctChange = False
        self._yOctChange = False
        self.limitDataToLoad = 5000
        self.dataUpdateToOctave = False
        self.inverseFunc = False
        self.cont = 0
        
        #Variables globales con set y get
        self.setXActual(np.array(None))
        self.setYActual(np.array(None))
        self._setXOrigin(np.array(None))
        self._setYOrigin(np.array(None))
        self._setXOctave(np.array(None))
        self._setYOctave(np.array(None))
        self._setTimerIndex(0)
        self._setVelocity(50)
        self._soundVelSlider.SetValue(50)
        self._askPoints = True
        
        array = np.array([0,1])
        index = [i for i in range(0, len(array))]
        self._setxPoints(np.delete(array,index))
        self._setyPoints(np.delete(array,index))
        
        self._setMatSelection("Original")
        self._setavNPoints(1)
        self._setMarkerStyleIndex(22)
        self._setLineChar('')
        self._setMarkerChar('')
        self._setColorChar('b')
        self._setCoreInstruments()
        self._setInstNum(1)
        self._instListBox.InsertItems(self._instruments[:23], 0)
#        self._instListBox.InsertItems(self._instruments, 0)
        
        self._setGridColor("Black")
        self._setGridLinestyle("Dashed line")
        self._setGridLinewidth(0.5)
        
        self._setXLabel('')
        self._setYLabel('')
        self._setXName('')
        self._setYName('')
        
        self._setDataFrame(None)
        
#Setters!!!        
    def _setDataFrame (self, data):
        self._expData.printOutput("Setting class variable dataFrame.")
        self._dataFrame = data
    
    def setXActual (self, x):
        self._expData.printOutput("Setting class variable X.")
        self.x = x
        
    def setYActual (self, y):
        self._expData.printOutput("Setting class variable Y.")
        self.y = y
        
    def _setXOrigin (self, xOrigin):
        self._expData.printOutput("Setting class variable xOrigin.")
        self._xOrigin = xOrigin
        
    def _setYOrigin (self, yOrigin):
        self._expData.printOutput("Setting class variable yOrigin.")
        self._yOrigin = yOrigin
        
    def _setNormXY (self, x, y):
        self._expData.printOutput("Setting class variables norm_x and norm_y.")
        self._norm_x, self._norm_y = self._matFc.normalizar(x, y)
        
    def _setTimerIndex (self, index):
        self._expData.printOutput("Setting class variable timerIndex.")
        self._timerIndex = index
        
    def _setVelocity (self, vel):
        self._expData.printOutput("Setting class variable velocity.")
        self._velocity = vel
        
    def _setxPoints (self, points):
        self._expData.printOutput("Setting class variable xPoints.")
        self._xPoints = points
        
    def _setyPoints (self, points):
        self._expData.printOutput("Setting class variable yPoints.")
        self._yPoints = points
        
    def _setAbsMarkPoint (self, point):
        self._expData.printOutput("Setting class variable absPoint.")
        self._absPoint = point
        
    def _setOrdMarkPoint (self, point):
        self._expData.printOutput("Setting class variable ordPoint.")
        self._ordPoint = point
        
    def _setMatSelection (self, select):
        self._expData.printOutput("Setting class variable matSelection.")
        self._matSelection = select
        
    def _setHoriLower (self, hl):
        self._expData.printOutput("Setting class variable horiLower.")
        self._horiLower = hl
        
    def _setHoriUpper (self, hu):
        self._expData.printOutput("Setting class variable horiUpper.")
        self._horiUpper = hu
        
    def _setavNPoints (self, num):
        self._expData.printOutput("Setting class variable avNPoints.")
        self._avNPoints = num
        
    def _setMarkerStyleIndex (self, index):
        self._expData.printOutput("Setting class variable markerStyleIndex.")
        self._markerStyleIndex = index
        
    def _setLineChar (self, char):
        self._expData.printOutput("Setting class variable lineChar.")
        self._lineChar = char
        
    def _setMarkerChar (self, char):
        self._expData.printOutput("Setting class variable markerChar.")
        self._markerChar = char
        
    def _setColorChar (self, char):
        self._expData.printOutput("Setting class variable colorChar.")
        self._colorChar = char
        
    def _setCoreInstruments (self):
        self._expData.printOutput("Setting class variables instruments and instRange.")
        self._instruments, self._instRange = self._dataSound.reproductor.getInstrument()
        
    def _setInstNum (self, num):
        self._expData.printOutput("Setting class variable instNum.")
        self._instNum = num
        
    def _setGridColor(self, color):
        self._expData.printOutput("Setting class variable gridColor.")
        if color=="Blue":
            self._gridColor = u'b'
        elif color=="Green":
            self._gridColor = 'g'
        elif color=="Red":
            self._gridColor = 'r'
        elif color=="Cyan":
            self._gridColor = 'c'
        elif color=="Magenta":
            self._gridColor = 'm'
        elif color=="Yellow":
            self._gridColor = 'y'
        elif color=="Black":
            self._gridColor = 'k'
        elif color=="White":
            self._gridColor = 'w'
        else:
            self._expData.writeInfo("The color selected is not valid.")
    
    def _setGridLinestyle(self, linestyle):
        self._expData.printOutput("Setting class variable gridLineStyle.")
        if linestyle == "Solid line":
            self._gridLinestyle = '-'
        elif linestyle == "Dashed line":
            self._gridLinestyle = '--'
        elif linestyle == "Dash-dot line":
            self._gridLinestyle = '-.'
        elif linestyle == "Dotted line":
            self._gridLinestyle = ':'
        else:
            self._expData.writeInfo("The line style selected is not valid.")
        
    def _setGridLinewidth(self, linewidth):
        self._expData.printOutput("Setting class variable gridLinewidth.")
        self._gridLinewidth = linewidth
        
    def _setXLabel(self, xlabel):
        self._expData.printOutput("Setting class variable xLabel.")
        self.xLabel = xlabel
        
    def _setYLabel(self, ylabel):
        self._expData.printOutput("Setting class variable yLabel.")
        self.yLabel = ylabel
        
    def _setXName(self, xName):
        self._expData.printOutput("Setting class variable xName.")
        self.xName = xName
        
    def _setYName(self, yName):
        self._expData.printOutput("Setting class variable yName.")
        self.yName = yName
        
    def _setXOctave(self, x):
        self._expData.printOutput("Setting class variable xOctave.")
        self.xOctave = x
    
    def _setYOctave(self, y):
        self._expData.printOutput("Setting class variable yOctave.")
        self.yOctave = y

#Getters!!!
    def getDataFrame (self):
        self._expData.printOutput("Class variable dataFrame requested.")
        return self._dataFrame
        
    def getXActual (self):
        self._expData.printOutput("Class variable X requested.")
        if self.x.any() == None:
            self._expData.writeInfo("The class variable X has not yet been set.")
        return self.x
    
    def getYActual (self):
        self._expData.printOutput("Class variable Y requested.")
        if self.y.any() == None:
            self._expData.writeInfo("The class variable Y has not yet been set.")
        return self.y
        
    def getXOriginal (self):
        self._expData.printOutput("Class variable xOrigin requested.")
        if self._xOrigin.any() == None:
            self._expData.writeInfo("The class variable xOrigin has not yet been set.")
        return self._xOrigin
    
    def getYOriginal (self):
        self._expData.printOutput("Class variable yOrigin requested.")
        if self._yOrigin.any() == None:
            self._expData.writeInfo("The class variable yOrigin has not yet been set.")
        return self._yOrigin
        
    def _getTimerIndex (self):
        self._expData.printOutput("Class variable timerIndex requested.")
        return self._timerIndex
    
    def _getNormX (self):
        self._expData.printOutput("Class variable norm_x requested.")
        return self._norm_x
    
    def _getNormY (self):
        self._expData.printOutput("Class variable norm_y requested.")
        return self._norm_y
    
    def _getVelocity (self):
        self._expData.printOutput("Class variable velocity requested.")
        index = [i for i in range(100, -1, -1)]
        return index[self._velocity]
    
    def _getxPoints (self):
        self._expData.printOutput("Class variable xPoints requested.")
        return self._xPoints
    
    def _getyPoints (self):
        self._expData.printOutput("Class variable yPoints requested.")
        return self._yPoints
    
    def _getAbsMarkPoint (self):
        self._expData.printOutput("Class variable absPoint requested.")
        return self._absPoint
        
    def _getOrdMarkPoint (self):
        self._expData.printOutput("Class variable ordPoint requested.")
        return self._ordPoint
    
    def _getMatSelection (self):
        self._expData.printOutput("Class variable matSelection requested.")
        return self._matSelection
    
    def _getHoriLower (self):
        self._expData.printOutput("Class variable horiLower requested.")
        return self._horiLower
        
    def _getHoriUpper (self):
        self._expData.printOutput("Class variable horiUpper requested.")
        return self._horiUpper
    
    def _getavNPoints (self):
        self._expData.printOutput("Class variable avNPoints requested.")
        return self._avNPoints
    
    def _getMarkerStyleIndex (self):
        self._expData.printOutput("Class variable markerStyleIndex requested.")
        return self._markerStyleIndex
    
    def _getLineChar (self):
        self._expData.printOutput("Class variable lineChar requested.")
        return self._lineChar
    
    def _getMarkerChar (self):
        self._expData.printOutput("Class variable markerChar requested.")
        return self._markerChar
    
    def _getColorChar (self):
        self._expData.printOutput("Class variable colorChar requested.")
        return self._colorChar
    
    def _getPlotStile (self):
        self._expData.printOutput("Graphic style requested.")
        return (self._getColorChar() + self._getMarkerChar() + self._getLineChar())
    
    def _getCoreInstruments (self):
        self._expData.printOutput("Class variable instruments requested.")
        return self._instruments
    
    def _getInstNum (self):
        self._expData.printOutput("Class variable instNum requested.")
        return self._instNum
    
    def _getGridColor(self):
        self._expData.printOutput("Class variable gridColor requested.")
        return self._gridColor
    
    def _getGridLinestyle(self):
        self._expData.printOutput("Class variable gridLinestyle requested.")
        return self._gridLinestyle
    
    def _getGridLinewidth(self):
        self._expData.printOutput("Class variable gridLinewidth requested.")
        return self._gridLinewidth
    
    def getXLabel(self):
        self._expData.printOutput("Class variable xLabel requested.")
        return self.xLabel
        
    def getYLabel(self):
        self._expData.printOutput("Class variable yLabel requested.")
        return self.yLabel
    
    def getXName(self):
        self._expData.printOutput("Class variable xName requested.")
        return self.xName
    
    def getYName(self):
        self._expData.printOutput("Class variable yName requested.")
        return self.yName
    
    def getXOctave(self):
        self._expData.printOutput("Class variable xOctave requested.")
        return self.xOctave
    
    def getYOctave(self):
        self._expData.printOutput("Class variable yOctave requested.")
        return self.yOctave
    
#Interfaz!!! - funcionalización
    def setCutSliderLimits (self, xOrigin, yOrigin, x, y):
        self._expData.printOutput("Updating text control labels.")
        #Aún no se funcionalizarlo
#        try:
#            self._lVLimitSlider.SetMax(np.amax(yOrigin))
#            self._lVLimitSlider.SetMin(np.amin(yOrigin))
#            self._lVLimitSlider.SetValue(np.amin(y))
#        except Exception as e:
#            self._expData.writeException(e)
#        try:
#            self._uVLimitSlider.SetMax(np.amax(yOrigin))
#            self._uVLimitSlider.SetMin(np.amin(yOrigin))
#            self._uVLimitSlider.SetValue(np.amax(y))
#        except Exception as e:
#            self._expData.writeException(e)
        try:
#            self._lHLimitSlider.SetMax(np.amax(xOrigin))
#            self._lHLimitSlider.SetMin(np.amin(xOrigin))
#            self._lHLimitSlider.SetValue(np.amin(x))
            self._lHLimitSlider.SetMax(xOrigin.size)
            self._lHLimitSlider.SetMin(0)
            self._lHLimitSlider.SetValue(self._getHoriLower())
        except Exception as e:
            self._expData.writeException(e)
        try:
            self._uHLimitSlider.SetMax(xOrigin.size)
            self._uHLimitSlider.SetMin(0)
            self._uHLimitSlider.SetValue(self._getHoriUpper())
        except Exception as e:
            self._expData.writeException(e)
        self.SendSizeEvent()
        
    def setArrayLimits (self, x, y):
        self._expData.printOutput("Setting the Upper and Lower limits.")
        try:
            limitVLower = np.amin(y)
        except Exception as e:
            self._expData.writeException(e)
        try: 
            limitVUpper = np.amax(y)
        except Exception as e:
            self._expData.writeException(e)
        try:
            limitHLower = np.amin(x)
        except Exception as e:
            self._expData.writeException(e)
        try:
            limitHUpper = np.amax(x)
        except Exception as e:
            self._expData.writeException(e)
        return limitVLower, limitVUpper, limitHLower, limitHUpper
        
    def setAbsSliderLimits (self, x):
        self._expData.printOutput("Setting the slider limits.")
        try:
            self._absPosSlider.SetMax(x.size)
            self._absPosSlider.SetMin(0)
            self.SendSizeEvent()
        except Exception as e:
            self._expData.writeException(e)

        #Para python 3:
        """if(x[x.size-1]<10000):
            name="Abscissa Position:\n"+str("{0:.2f}".format(x[0]))+" to "+ \
            str("{0:.2f}".format(x[x.size-1]))
        else:
            name="Abscissa Position:\n"+str("{0:.2f}".format(x[0]))+" to "+ \
            str("{0:.2f}".format(x[x.size-1]))
            self._absPosTextCtrl.SetMinSize(wx.Size( 120,30 ))"""
            
        #Para python 2:
        try:
            if(x[x.size-1]<10000):
                name="Abscissa Position:\n"+str(x[0])+" to "+ \
                str(x[x.size-1])
            else:
                name="Abscissa Position:\n"+str(x[0])+" to "+ \
                str(x[x.size-1])
                self._absPosTextCtrl.SetMinSize(wx.Size( 120,40 ))
            self._absPosTextCtrl.SetValue(name)
        except Exception as e:
            self._expData.writeException(e)
    
    def plotTitles(self):
        self._expData.printOutput("Setting the titles and labels.")
        try:
            self.panel.set_title(self._titleEdDataTextCtrl.GetValue())
        except Exception as e:
            self._expData.writeException(e)
        try:
            #self.panel.set_xlabel( self._axisChoiceX.GetString(self.getXLabel()) )
            #text=self.getXName()+'\n'+self.getYName()
            #wx.MessageBox(text, 'Info', wx.OK | wx.ICON_INFORMATION)
            self.panel.set_xlabel( self.getXName() )
        except Exception as e:
            self._expData.writeException(e)
        try:
            #self.panel.set_ylabel( self._axisChoiceX.GetString(self.getYLabel()) )
            self.panel.set_ylabel( self.getYName() )
        except Exception as e:
            self._expData.writeException(e)
        
    def plot2D (self, x, y):
        #para graficar cambios con los datos originales
        self._expData.printOutput("Plot the graph.")
        try:
            if self._gridChoice.IsChecked():
                self.panel.grid(color=self._getGridColor(), linestyle=self._getGridLinestyle(), linewidth=self._getGridLinewidth())
        except Exception as e:
            self._expData.writeException(e)
        try:
            style = self._getPlotStile()
            self._lines = self.panel.plot(x, y, style)
            self._plotCounter = self._plotCounter + 1
        except Exception as e:
            self._expData.writeException(e)
        
        #Se pone una variable de estado en lugar de enviarlo directamente para no ralentizar los procesos.
        self.dataUpdateToOctave = True
#        try:
#            self._sendToOctave()
#        except Exception as e:
#            self._expData.writeException(e)
        
        self._figure.tight_layout()
        self._figure.canvas.draw()
        
    def plotRedLine (self, abscisa, ordenada):
        self._expData.printOutput("Plot the red line.")
        try:
            if not self._lineExist:
                #plot the line the first time
                self._lineExist = True
            else:
                #update the line and generate de sound
                self.panel.lines.remove(self._wr())
            self.panel.plot(abscisa, ordenada, 'r')
            self._wr = ref(self.panel.lines[self._plotCounter])
        except Exception as e:
            self._expData.writeException(e)
        self._figure.canvas.draw()
    
    def plotMarkLine (self):
        self._expData.printOutput("Plot the mark line.")
        try:
            self.panel.plot(self._getAbsMarkPoint(), self._getOrdMarkPoint(), 'k')
            self._plotCounter = self._plotCounter + 1
        except Exception as e:
            self._expData.writeException(e)
        
    def replot2D (self, x, y):
        if x.any()==None or y.any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:
            self._expData.printOutput("Clean and plot the graph")
            self._lineExist = False
            self.panel.cla()
            self._figure.canvas.draw()
            self.panel.lines = []
            self._plotCounter = 0
            try:
                markX = self._getxPoints()   
                for i in range (0, markX.size):
                    self._setAbsMarkPoint( np.array([float(markX[i]), float(markX[i])]) )
                    self._setOrdMarkPoint( np.array([float(np.amin(y)), float(np.amax(y))]) )
                    self.plotMarkLine()
            except Exception as e:
                self._expData.writeException(e)
            try:
                timerIndex = self._getTimerIndex()
                if not timerIndex==0:
                    ordenada = np.array([float(np.amin(y)), float(np.amax(y))])
                    abscisa = np.array([float(x[timerIndex]), float(x[timerIndex])])
                    self.plotRedLine(abscisa, ordenada)
            except Exception as e:
                self._expData.writeException(e)
            
            if self.inverseFunc:
                self.panel.invert_yaxis()
                self._figure.canvas.draw()
            
            try:
                self.plotTitles()
                self.plot2D(x, y)
            except AttributeError as e:
                self._expData.writeInfo("The data has not been imported yet.")
                self._expData.writeException(e)
            except Exception as e:
                self._expData.writeException(e)
            try:
                self.SendSizeEvent()
            except Exception as e:
                self._expData.writeException(e)
                 
    def _sonoPlot (self, event):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            self._expData.printOutput("Generate the sound and refresh plot.")
            timerIndex = self._getTimerIndex()
            x=self.getXActual()
            y=self.getYActual() 
            try:
                ordenada = np.array([float(np.amin(y)), float(np.amax(y))])
                abscisa = np.array([float(x[timerIndex]), float(x[timerIndex])])
            except Exception as e:
                self._expData.writeException(e)
            try:
                self.plotRedLine(abscisa, ordenada)
            except Exception as e:
                self._expData.writeException(e)
            try:
                self._absPosSlider.SetValue(timerIndex)
            except Exception as e:
                self._expData.writeException(e)
            try:
                self._dataSound.makeSound(self._getNormY(), timerIndex)
            except Exception as e:
                self._expData.writeException(e)
            self._setTimerIndex(timerIndex + 1)
            if timerIndex==(x.size-1):
                self.stopMethod()
        
    def openMethod(self):
        if self._timer.IsRunning():
            self.stopMethod()
            wx.MessageBox("The previous reproduction of the data has been stopped.", 
                          'Info', wx.OK | wx.ICON_INFORMATION)
        if not self._askPoints:
            self.askSavePoints()
            
#        if not self._firstOpen:
#            self._sendToOctaveListBox.Clear()
#            self._sendToOctaveListBox.InsertItems(["X","Y","Original X","Original Y"], 0)
        self.setArrayLimits(0,0)
        self._askLabelDataCheckBox.SetValue(True)
        try:
            pathName, fileTipe = self._openData.getDataPath()
            
            if fileTipe == "txt":
                data, status = self._openData.setArraysFromTxt(pathName)
            else:
                if fileTipe == "csv":
                    data, status = self._openData.setArraysFromCsv(pathName)
                else:
                    self._expData.writeInfo("Error: the file type not match with txt or csv.")
            if not status:
                wx.MessageBox("The data file can't be opened, the software continue with the previous data if exist. \nCheck the file and contact the development team if you need help.\nContact mail: sonounoteam@gmail.com.", 
                          'Info', wx.OK | wx.ICON_INFORMATION)
            else:
                #aquí las nuevas opciones
                self._titleEdDataTextCtrl.SetValue(self._openData.getDataFileName()[:-4])
                self._setDataFrame(data)
                x, y, status1 = self.dataSelection(data)
                if status1:
                    self.setXActual(x)
                    self.setYActual(y)
                    self._setXOrigin(x)
                    self._setYOrigin(y)
                    self._setHoriLower(0)
                    self._setHoriUpper(x.size)
                    self.setCutSliderLimits(x, y, x, y)
                    self.setArrayLimits(x, y)
                    self.setAbsSliderLimits(x)
                    self._sendAllToOctave()
                    self.replot2D(x, y)
                    self._expData.printOutput("Data imported and graphed.")
                else:
                    wx.MessageBox("The data file can't be opened, the software continue with the previous data if exist. \nCheck the file and contact the development team if you need help.\nContact mail: sonounoteam@gmail.com.", 
                          'Info', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            self._expData.writeException(e)
    
    def dataSelection(self, data):
        if self.limitDataToLoad < data.shape[0]:
            if wx.MessageBox("The data file have more than 5000 values, the software might delay to show all the data array on a grid element. Do you want to display all the values on the grid element anyway?\n\nNOTE: The other functionalities (plot, math fuctions, etc) use all the values of the array in any case.", "Information", wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                rowNumber = self.limitDataToLoad
            else:
                rowNumber = data.shape[0]
        else:
            rowNumber = data.shape[0]
        
        if data.shape[1]<2:
            return None, None, False
        
        #Chequeo si los datos son mas de cierto valor
#        if self.limitDataToLoad > data.shape[0]:
#            rowNumber = data.shape[0]
#        else:
#            rowNumber = self.limitDataToLoad
        
        #Chequeo si tienen nombre de columnas
        if not type(data.loc[0,0]) == str:
            #Se debe colocar un for
            for a in range (0,data.shape[1]):
                if a==0:
                    xLabel = pd.DataFrame({a:["Column "+str(a)]})
                else:
                    xLabel.loc[:, a] = "Column "+str(a)
            data = pd.concat([xLabel, data]).reset_index(drop=True)
            self._setDataFrame(data)
        
        #Limpio la grilla
        self._dataGrid.ClearGrid()
        #Redimencionamos la grilla
        if data.shape[1]>self._dataGrid.GetNumberCols():
            self._dataGrid.AppendCols(data.shape[1]-self._dataGrid.GetNumberCols())
        elif data.shape[1]<self._dataGrid.GetNumberCols():
            self._dataGrid.DeleteCols( numCols=(self._dataGrid.GetNumberCols()-data.shape[1]) )
        if rowNumber>self._dataGrid.GetNumberRows():
            self._dataGrid.AppendRows(rowNumber-self._dataGrid.GetNumberRows())
        elif rowNumber<self._dataGrid.GetNumberRows():
            self._dataGrid.DeleteRows( numRows=(self._dataGrid.GetNumberRows()-rowNumber) )
#        #Lo coloco en la grilla
        dlg = wx.ProgressDialog("Loading data to the grid", " ", maximum=data.shape[0], style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT)
        dlg.Show()
        if data.shape[0] < rowNumber:
            for j in range (0,data.shape[0]):
                for i in range (0,data.shape[1]):
                    self._dataGrid.SetCellValue (j, i, str(data.iloc[j,i]))
                    if not j == 0:
                        self._dataGrid.SetReadOnly(j, i, isReadOnly=True)
                    else:
                        self._dataGrid.SetReadOnly(j, i, isReadOnly=False)
                dlg.Pulse("Loading data")
                #dlg.Update(j, "Loading data")
                #dlg.Update (j, "%i of %i"%(j, int(data.shape[0])))
                if dlg.WasCancelled():
                    break
        else:
            for j in range (0,rowNumber):
                for i in range (0,data.shape[1]):
                    self._dataGrid.SetCellValue (j, i, str(data.iloc[j,i]))
                    if not j == 0:
                        self._dataGrid.SetReadOnly(j, i, isReadOnly=True)
                    else:
                        self._dataGrid.SetReadOnly(j, i, isReadOnly=False)
                #dlg.Update(j, "Loading data")
                dlg.Pulse("Loading data")
                #dlg.Update (j, "%i of %i"%(j, int(data.shape[0])))
                if dlg.WasCancelled():
                    break
        dlg.Destroy()
        self._axisChoiceX.Clear()
        self._axisChoiceY.Clear()
        #Inserto los titulos de los ejes en los cuadros de opciones de ejes
        for a in range (0,data.shape[1]):
            self._axisChoiceX.InsertItems([str(data.iloc[0,a])],a)
            self._axisChoiceY.InsertItems([str(data.iloc[0,a])],a)
        #Se actualizan los valores
        self._axisChoiceX.Update()
        self._axisChoiceY.Update()
        #Por defecto como X se selecciona la primer columna y como Y la segunda
        self._axisChoiceX.SetSelection(0)
        self._axisChoiceY.SetSelection(1)

        #Se generan los numpy array de las primeras dos columnas y se devuelven
        try:
            self._setXLabel(0)
            self._setYLabel(1)
            self._setXName(data.iloc[0,0])
            self._setYName(data.iloc[0,1])
            #text=self.getXName()+'\n'+self.getYName()
            #wx.MessageBox(text, 'Info', wx.OK | wx.ICON_INFORMATION)
            x = data.loc[1:,0]
            xnumpy = x.values.astype(np.float64)
            y = data.loc[1:,1]
            ynumpy = y.values.astype(np.float64)
            status=True
        except Exception as e:
            status=False
            xnumpy=np.array(None)
            ynumpy=np.array(None)
            self._expData.writeException(e)
            
        self.del_xy = np.array([0,1])
        index1 = [i for i in range(0, len(self.del_xy))]
        if not self.del_xy.size==0:
            self.del_xy=np.delete(self.del_xy,index1)
        
        if status:
            delNum=False
            try:
                for i in range (0, xnumpy.size):
                    #if xnumpy[i] == nan or ynumpy[i] == nan:
                    if math.isnan(xnumpy[i]) or math.isnan(ynumpy[i]):
                        self.del_xy = np.append(self.del_xy, i)
                        delNum=True
            except Exception as e:
                self._expData.writeException(e)
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
                    xnumpy=np.delete(xnumpy, self.del_xy)
                    ynumpy=np.delete(ynumpy, self.del_xy)
            except Exception as e:
                self._expData.writeException(e)
            
        return xnumpy, ynumpy, status
    
    def pandasToNumpy(self, x):
        #Se generan los numpy array de las primeras dos columnas y se devuelven
        try:
            xnumpy = x.values.astype(np.float64)
            status=True
        except Exception as e:
            status=False
            xnumpy=np.array(None)
            self._expData.writeException(e)
            
        self.del_xy = np.array([0,1])
        index1 = [i for i in range(0, len(self.del_xy))]
        if not self.del_xy.size==0:
            self.del_xy=np.delete(self.del_xy,index1)
        
        if status:
            delNum=False
            try:
                for i in range (0, xnumpy.size):
                    #if xnumpy[i] == nan or ynumpy[i] == nan:
                    if math.isnan(xnumpy[i]):
                        self.del_xy = np.append(self.del_xy, i)
                        delNum=True
            except Exception as e:
                self._expData.writeException(e)
            try:
                if delNum:
                    text="Algunos puntos se han importado vacios y han tenido que eliminarse. Los mismos estaban en las direcciones: ["
                    for i in range (0, self.del_xy.size):
                        if i != (self.del_xy.size-1):
                            text=text+str(self.del_xy[i]+1)+" ; "
                        else:
                            text=text+str(self.del_xy[i]+1)
                    text=text+"] del archivo original."
                    #wx.MessageBox(text, 
                     #             'Info', wx.OK | wx.ICON_INFORMATION)
                    delNum=False
                    xnumpy=np.delete(xnumpy, self.del_xy)
            except Exception as e:
                self._expData.writeException(e)
            
        return xnumpy, status
                    
    def titleEdData(self):
        #Fijarse si es aquí donde se pierden los labels
        self.panel.set_title(self._titleEdDataTextCtrl.GetValue())
        self._figure.tight_layout()
        self._figure.canvas.draw()
    
    def askLabelData(self):
        if self.getDataFrame() is not None:
            data = self.getDataFrame()
            if not self._askLabelDataCheckBox.IsChecked():
                self._dataGrid.InsertRows()
                for i in range (0,data.shape[1]):
                    self._dataGrid.SetReadOnly(1, i, isReadOnly=True)
            else:
                if self._dataGrid.GetNumberRows() > self.limitDataToLoad:
                    self._dataGrid.DeleteRows()
                    for i in range (0,data.shape[1]):
                        self._dataGrid.SetReadOnly(0, i, isReadOnly=False)
        else:
            self._expData.writeInfo("The data has not been opened yet.")
            wx.MessageBox("The data has not been opened yet.", 
                          'Info', wx.OK | wx.ICON_INFORMATION)
    
    def dataGridChange(self):
        if self.getDataFrame() is not None:
            data = self.getDataFrame()
            if data.shape[1] == self._dataGrid.GetNumberCols():
                self._axisChoiceX.Clear()
                self._axisChoiceY.Clear()
                
                #for a in range (0,data.shape[1]):
                for a in range (0, self._dataGrid.GetNumberCols()):
                    self._axisChoiceX.InsertItems([self._dataGrid.GetCellValue(0,a)],a)
                    self._axisChoiceY.InsertItems([self._dataGrid.GetCellValue(0,a)],a)
                    data.at[0, a] = self._dataGrid.GetCellValue(0,a)
                
                self._setXName(self._dataGrid.GetCellValue(0,self.getXLabel()))
                self._setYName(self._dataGrid.GetCellValue(0,self.getYLabel()))
                
                self._axisChoiceX.Update()
                self._axisChoiceY.Update()
                self.plotTitles()
                self._figure.tight_layout()
                self._figure.canvas.draw()
            
    def dataGridUpdate(self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:
            x = self.getXActual()
            y = self.getYActual()
            
            if self.limitDataToLoad < x.shape[0]:
                if wx.MessageBox("The data file have more than 5000 values, the software might delay to show all the data array on a grid element. Do you want to display all the values on the grid element anyway?\n\nNOTE: The other functionalities (plot, math fuctions, etc) use all the values of the array in any case.", "Information", wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                    rowNumber = self.limitDataToLoad
                else:
                    rowNumber = x.shape[0]
            else:
                rowNumber = x.shape[0]

            #Limpio la grilla
            self._dataGrid.ClearGrid()
            #Redimencionamos la grilla
            if 2>self._dataGrid.GetNumberCols():
                self._dataGrid.AppendCols(2-self._dataGrid.GetNumberCols())
            elif 2<self._dataGrid.GetNumberCols():
                self._dataGrid.DeleteCols( numCols=(self._dataGrid.GetNumberCols()-2) )
            if rowNumber>self._dataGrid.GetNumberRows():
                self._dataGrid.AppendRows(rowNumber-self._dataGrid.GetNumberRows())
            elif rowNumber<self._dataGrid.GetNumberRows():
                self._dataGrid.DeleteRows( numRows=(self._dataGrid.GetNumberRows()-rowNumber) )
                
            #Detectar los titulos de columna
            data = self.getDataFrame()
            self._dataGrid.SetCellValue (0, 0, str(data.iloc[0,self._axisChoiceX.GetSelection()]))
            self._dataGrid.SetCellValue (0, 1, str(data.iloc[0,self._axisChoiceY.GetSelection()]))
            self._dataGrid.SetReadOnly(0, 0, isReadOnly=True)
            self._dataGrid.SetReadOnly(0, 1, isReadOnly=True)
                
            #Lo coloco en la grilla
            dlg = wx.ProgressDialog("Loading data to the grid", " ", maximum=data.shape[0], style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT)
            dlg.Show()  
            if x.shape < rowNumber:
                for j in range (1,x.shape):
                    self._dataGrid.SetCellValue (j, 0, str(x[j-1]))
                    self._dataGrid.SetCellValue (j, 1, str(y[j-1]))
                    self._dataGrid.SetReadOnly(j, 0, isReadOnly=True)
                    self._dataGrid.SetReadOnly(j, 1, isReadOnly=True)
                    dlg.Pulse("Loading data")
                    #dlg.Update(j, "Loading data")
                    #dlg.Update (j, "%i of %i"%(j, int(data.shape[0])))
                    if dlg.WasCancelled():
                        break
            else:
                for j in range (1,rowNumber):
                    self._dataGrid.SetCellValue (j, 0, str(x[j-1]))
                    self._dataGrid.SetCellValue (j, 1, str(y[j-1]))
                    self._dataGrid.SetReadOnly(j, 0, isReadOnly=True)
                    self._dataGrid.SetReadOnly(j, 1, isReadOnly=True)
                    dlg.Pulse("Loading data")
                    #dlg.Update(j, "Loading data")
                    #dlg.Update (j, "%i of %i"%(j, int(data.shape[0])))
                    if dlg.WasCancelled():
                        break
            dlg.Destroy()
                
    def dataGridOriginal(self):
        if self.getDataFrame() is not None:
            data = self.getDataFrame()
            
            if self.limitDataToLoad < data.shape[0]:
                if wx.MessageBox("The data file have more than 5000 values, the software might delay to show all the data array on a grid element. Do you want to display all the values on the grid element anyway?\n\nNOTE: The other functionalities (plot, math fuctions, etc) use all the values of the array in any case.", "Information", wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                    rowNumber = self.limitDataToLoad
                else:
                    rowNumber = data.shape[0]
            else:
                rowNumber = data.shape[0]
            
            #Limpio la grilla
            self._dataGrid.ClearGrid()
            #Redimencionamos la grilla
            if data.shape[1]>self._dataGrid.GetNumberCols():
                self._dataGrid.AppendCols(data.shape[1]-self._dataGrid.GetNumberCols())
            elif data.shape[1]<self._dataGrid.GetNumberCols():
                self._dataGrid.DeleteCols( numCols=(self._dataGrid.GetNumberCols()-data.shape[1]) )
            if rowNumber>self._dataGrid.GetNumberRows():
                self._dataGrid.AppendRows(rowNumber-self._dataGrid.GetNumberRows())
            elif rowNumber<self._dataGrid.GetNumberRows():
                self._dataGrid.DeleteRows( numRows=(self._dataGrid.GetNumberRows()-rowNumber) )
            
            #Lo coloco en la grilla
            dlg = wx.ProgressDialog("Loading data to the grid", " ", maximum=data.shape[0], style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT)
            dlg.Show()
            if data.shape[0] < rowNumber:
                for j in range (0,data.shape[0]):
                    for i in range (0,data.shape[1]):
                        self._dataGrid.SetCellValue (j, i, str(data.iloc[j,i]))
                        if not j == 0:
                            self._dataGrid.SetReadOnly(j, i, isReadOnly=True)   
                        else:
                            self._dataGrid.SetReadOnly(j, i, isReadOnly=False)
                    dlg.Pulse("Loading data")
                    #dlg.Update(j, "Loading data")
                    #dlg.Update (j, "%i of %i"%(j, int(data.shape[0])))
                    if dlg.WasCancelled():
                        break
            else:
                for j in range (0,rowNumber):
                    for i in range (0,data.shape[1]):
                        self._dataGrid.SetCellValue (j, i, str(data.iloc[j,i]))
                        if not j == 0:
                            self._dataGrid.SetReadOnly(j, i, isReadOnly=True)
                        else:
                            self._dataGrid.SetReadOnly(j, i, isReadOnly=False)
                    dlg.Pulse("Loading data")
                    #dlg.Update(j, "Loading data")
                    #dlg.Update (j, "%i of %i"%(j, int(data.shape[0])))
                    if dlg.WasCancelled():
                        break
            dlg.Destroy()
    
    def axisChoiceXMethod(self):
        if self.getDataFrame() is not None:
            if not self._askPoints:
                self.askSavePoints()
            data = self.getDataFrame()
            self._setXLabel(self._axisChoiceX.GetSelection())
            self._setXName(self._axisChoiceX.GetString(self._axisChoiceX.GetSelection()))
            #wx.MessageBox(self.getXName(), 'Info', wx.OK | wx.ICON_INFORMATION)
            x1 = data.loc[1:,self._axisChoiceX.GetSelection()]
            x = x1.values.astype(np.float64)
            self.setXActual(x)
            self._setXOrigin(x)
            y = self.getYOriginal()
            self._setHoriLower(0)
            self._setHoriUpper(x.size)
            self.setCutSliderLimits(x, y, x, y)
            self.setArrayLimits(x, y)
            self.setAbsSliderLimits(x)
            self.replot2D(x, y)
    
    def axisChoiceYMethod(self):
        if self.getXOriginal().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            if self.getDataFrame() is not None:
                if not self._askPoints:
                    self.askSavePoints()
                data = self.getDataFrame()
                self._setYLabel(self._axisChoiceY.GetSelection())
                self._setYName(self._axisChoiceY.GetString(self._axisChoiceY.GetSelection()))
                #wx.MessageBox(self.getYName(), 'Info', wx.OK | wx.ICON_INFORMATION)
                y1 = data.loc[1:,self._axisChoiceY.GetSelection()]
                y = y1.values.astype(np.float64)
                self.setYActual(y)
                self._setYOrigin(y)
                x = self.getXOriginal()
                self._setHoriLower(0)
                self._setHoriUpper(x.size)
                self.setCutSliderLimits(x, y, x, y)
                self.setArrayLimits(x, y)
                self.setAbsSliderLimits(x)
                self.replot2D(x, y)
    
    def eSound (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            eSoundPath=self._expData.setPath("Save sound file", "Sound files |*.mid;*.midi")
            x = self.getXActual()
            y = self.getYActual()
            try:
                self._dataSound.reproductor.setInstrument(self._getInstNum())
                norm_x, norm_y = self._matFc.normalizar(x, y)
                self._dataSound.saveSound(eSoundPath, norm_x, norm_y)
            except AttributeError as e:
                self._expData.writeInfo("The data has not been imported yet.")
                self._expData.writeException(e)
            except Exception as e:
                self._expData.writeException(e)

    def savePlot(self):
        plotPath = self._expData.setPath("Save plot file", "Image files |*.png")
        try:
            self._figure.savefig(plotPath)
        except Exception as e:
            self._expData.writeException(e)
    
    def play (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            if not self._timer.IsRunning():
                try:
                    self._dataSound.reproductor.setInstrument(self._getInstNum())
                except Exception as e:
                    self._expData.writeException(e)
                try:
                    x = self.getXActual()
                    y = self.getYActual()
                    norm_x, norm_y = self._matFc.normalizar(x, y)
                    self._expData.printOutput("Normalize the input data.")
                    self._setNormXY(norm_x, norm_y)
                except AttributeError as e:
                    self._expData.writeInfo("The data has not been imported yet.")
                    self._expData.writeException(e)
                except Exception as e:
                    self._expData.writeException(e)
                #Seteo el tempo dependiendo del tiempo del timer
                self._timer.Start((self._getVelocity()*10) + 200)
            else:
                self._expData.printOutput("The timer is alredy on when the user press Play button.")
    
    def stopMethod(self):
        self._playButton.SetValue(False)
        self._playMenuItem.Check(False)
        self._playButton.SetLabel("Play")
        self._playMenuItem.SetItemLabel("Play")
        
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:
            if self._timer.IsRunning():
                self._dataSound.makeSound(0, -1)
                self._timer.Stop()
            self._setTimerIndex(0)
            self._absPosSlider.SetValue(0)
            self.replot2D(self.getXActual(), self.getYActual())
            
    def markPoints (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            #Se eliminarán los datos cada vez que se guardan o que se ingresa un archivo de datos nuevo.
            x = self.getXActual()
            y = self.getYActual()
            xp = self._getxPoints()
            yp = self._getyPoints()
            try:
                index = self._getTimerIndex() - 1
                xp = np.append(xp, x[index])
                yp = np.append(yp, y[index])
                self._setxPoints(xp)
                self._setyPoints(yp)
            except Exception as e:
                self._expData.writeException(e)
            self._askPoints = False
            #para graficar una línea
            try:
                self._setAbsMarkPoint( np.array([float(x[index]), float(x[index])]))
                self._setOrdMarkPoint( np.array([float(np.amin(y)), float(np.amax(y))]))
            except AttributeError as e:
                self._expData.writeInfo("The data has not been imported yet.")
                self._expData.writeException(e)
            except Exception as e:
                self._expData.writeException(e)
            self.plotMarkLine()
    
    def deleteLastMark (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            try:
                xp = self._getxPoints()
                yp = self._getyPoints()
                xp = xp[:-1].copy()
                yp = yp[:-1].copy()
                self._setxPoints(xp)
                self._setyPoints(yp)
                self.replot2D(self.getXActual(),self.getYActual())
            except Exception as e:
                self._expData.writeException(e)
        
    def deleteAllMark (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            xp = self._getxPoints()
            yp = self._getyPoints()
            try:
                index = [i for i in range(0, len(xp))]
            except Exception as e:
                self._expData.writeException(e)
            try:
                self._setxPoints(np.delete(xp,index))
                self._setyPoints(np.delete(yp,index))
            except Exception as e:
                self._expData.writeException(e)
            try:
                self.replot2D(self.getXActual(), self.getYActual())
            except Exception as e:
                self._expData.writeException(e)
                
    def saveData (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            x = self.getXActual()
            y = self.getYActual()
            try:
                self._expData.writePointFile(x, y)
            except Exception as e:
                self._expData.writeException(e)
            
    def saveMarks (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            xp = self._getxPoints()
            yp = self._getyPoints()
            try:
                self._expData.writePointFile(xp, yp)
            except AttributeError as e:
                self._expData.writeInfo("The array with numbers of interest has not been created yet.")
                self._expData.writeException(e)
            except Exception as e:
                self._expData.writeException(e)
            index = [i for i in range(0, len(xp))]
            self._setxPoints(np.delete(xp,index))
            self._setyPoints(np.delete(yp,index))
            self.replot2D(self.getXActual(), self.getYActual())
        
    def absPosSetting (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            #Set the red line to mark de points in the graph
            x = self.getXActual()
            y = self.getYActual()
            ordenada = np.array([float(np.amin(y)), float(np.amax(y))])
            abscisa = np.array([float(x[self._absPosSlider.GetValue()]), float(x[self._absPosSlider.GetValue()])])
            self.plotRedLine(abscisa, ordenada)
            
#    def cutVertical(self):
#        self.askSavePoints()
#        #Se debe realizar todo el mapeo para que reproduzca tick marks en los valores que exeden el límite y que se remapee el resto que si está en los límites.
#        try:
#            self.limitVLower = float(self._lVLimitSlider.GetValue())
#        except Exception as e:
#            self._expData.writeException(e)
#        try:
#            self.limitVUpper = float(self._uVLimitSlider.GetValue())
#        except Exception as e:
#            self._expData.writeException(e)
        
    def cutHorizontal (self):
        if self.getXOriginal().any()==None or self.getYOriginal().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:
            if not self._askPoints:
                self.askSavePoints()
            try:
                lower = (self._lHLimitSlider.GetValue())
                self._setHoriLower(lower)
            except Exception as e:
                self._expData.writeException(e)
            try:
                upper = (self._uHLimitSlider.GetValue())        
                self._setHoriUpper(upper)
            except Exception as e:
                self._expData.writeException(e)
            xo = self.getXOriginal()
            yo = self.getYOriginal()
            try:
                x = xo[lower:(upper+1)]
                y = yo[lower:(upper+1)]
                self.setXActual(x)
                self.setYActual(y)
            except AttributeError as e:
                self._expData.writeInfo("The data has not been imported yet.")
                self._expData.writeException(e)
            except Exception as e:
                self._expData.writeException(e)
            try:
                self.setCutSliderLimits(xo, yo, x, y)
                self.setArrayLimits(x, y)
                self.setAbsSliderLimits(x)
                self.replot2D(x, y)
            except AttributeError as e:
                self._expData.writeInfo("The data has not been imported yet.")
                self._expData.writeException(e)
            except Exception as e:
                self._expData.writeException(e)
            
    #Maybe we add soundfont in the future
    """def _soundFontChoice(self):
        if self._sFontLabel == 'gm':
            self._expData.printOutput("The choice of sound font is general midi, that's the default sound font.")
            if platform.system() == 'Windows':
                self._sFontChoice = "soundModule\soundFont\FluidR3_GM.sf2"
            else:
                if platform.system() == 'Linux':
                    self._sFontChoice = "soundModule/soundFont/FluidR3_GM.sf2"
                else:
                    if platform.system() == 'Darwin':
                        self._sFontChoice = "soundModule/soundFont/FluidR3_GM.sf2"
                    else:
                        self._expData.writeInfo("The operative system is unknown, the software can't open the sound font.")
        elif self._sFontLabel == 'other':
            self._expData.printOutput("The choice of sound font is look on the operative system.")
            self._sFontChoice = self._openData.getSFPath()
        else:
            self._expData.printOutput("Error!: the sound font chosen is not correct!.")
            self._expData.writeInfo("Error in 'soundFontChoice', on core.py!: the sound 
            font chosen is not correct!.")"""
    
    def instListBoxChoice(self):
        self._setInstNum(self._instListBox.GetSelection()+1)
        instrument = self._instListBox.GetString(self._instListBox.GetSelection())
        return instrument
            
    def matFcSelection(self):
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Last limits cut":
            self._avNPointsspinCtrl.Enable(False)
            self._expData.printOutput("Last limits cut function is selected.")
            self._setMatSelection("Last limits cut")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Original":
            self._avNPointsspinCtrl.Enable(False)
            self._expData.printOutput("Original function is selected.")
            self._setMatSelection("Original")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Inverse":
            self._avNPointsspinCtrl.Enable(False)
            self._expData.printOutput("Inverse function is selected.")
            self._setMatSelection("Inverse")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Play Backward":
            self._avNPointsspinCtrl.Enable(False)
            self._expData.printOutput("Play Backward function is selected.")
            self._setMatSelection("Play Backward")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Square":
            self._avNPointsspinCtrl.Enable(False)
            self._expData.printOutput("Square function is selected.")
            self._setMatSelection("Square")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Square root":
            self._avNPointsspinCtrl.Enable(False)
            self._expData.printOutput("Square root function is selected.")
            self._setMatSelection("Square root")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Logarithm":
            self._avNPointsspinCtrl.Enable(False)
            self._expData.printOutput("Logarithm function is selected.")
            self._setMatSelection("Logarithm")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Average":
            self._avNPointsspinCtrl.SetValue(1)
            self._avNPointsspinCtrl.Enable(True)
            self._expData.printOutput("Average function is selected.")
            self._setMatSelection("Average")
        self.matFcExecutor()
            
    def matFcExecutor(self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            if not self._askPoints:
                self.askSavePoints()
            xo, yo = self._matFc.mfOriginal(self.getXOriginal(), self.getYOriginal())
            x, y = self._matFc.mfOriginal(self.getXActual(), self.getYActual())
            if self._getMatSelection() == "Last limits cut":
                self._lHLimitSlider.Enable(True)
                self._uHLimitSlider.Enable(True)
                x = xo[self._getHoriLower():(self._getHoriUpper()+1)]
                y = yo[self._getHoriLower():(self._getHoriUpper()+1)]
                self._expData.printOutput("Last limits cut function is executed.")
                self.inverseFunc = False
            if self._getMatSelection() == "Original":
                self._lHLimitSlider.Enable(True)
                self._uHLimitSlider.Enable(True)
                x, y = self._matFc.mfOriginal(self.getXOriginal(), self.getYOriginal())
                self._expData.printOutput("Original function is executed.")
                self.inverseFunc = False
            if self._getMatSelection() == "Inverse":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                #x, y = self._matFc.mfInverse(self.getXOriginal(), self.getYOriginal())
                self.inverseFunc = True
                self._expData.printOutput("Inverse function is executed.")
            if self._getMatSelection() == "Play Backward":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                x, y = self._matFc.mfPlayBack(self.getXOriginal(), self.getYOriginal())
                self._expData.printOutput("Play Backward function is executed.")
                self.inverseFunc = False
            if self._getMatSelection() == "Square":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                x, y = self._matFc.mfSquare(self.getXOriginal(), self.getYOriginal())
                self._expData.printOutput("Square function is executed.")
                self.inverseFunc = False
            if self._getMatSelection() == "Square root":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                x, y = self._matFc.mfSquareRot(self.getXOriginal(), self.getYOriginal())
                self._expData.printOutput("Square root function is executed.")
                self.inverseFunc = False
            if self._getMatSelection() == "Logarithm":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                x, y = self._matFc.mfLog(self.getXOriginal(), self.getYOriginal())
                self._expData.printOutput("Logarithm function is executed.")
                self.inverseFunc = False
            if self._getMatSelection() == "Average":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                x, y = self._matFc.mfAverage(self.getXOriginal(), self.getYOriginal(), self._getavNPoints())
                self._expData.printOutput("Average function is executed.")
                self.inverseFunc = False
            try:
                self.setXActual(x)
                self.setYActual(y)
            except AttributeError as e:
                self._expData.writeInfo("The data has not been imported yet.")
                self._expData.writeException(e)
            except Exception as e:
                self._expData.writeException(e)
            try:
                self.setCutSliderLimits(xo, yo, x, y)
                self.setArrayLimits(x, y)
                self.setAbsSliderLimits(x)
                self.replot2D(x, y)
            except AttributeError as e:
                self._expData.writeInfo("The data has not been imported yet.")
                self._expData.writeException(e)
            except Exception as e:
                self._expData.writeException(e)
            
    def averageSelect(self):
        if self.getXActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            #seteo los límites de average
            x = self.getXActual()
            if not x == None:
                self._avNPointsspinCtrl.SetMax(x.size-1)
                self._avNPointsspinCtrl.SetMin(1)
                self._avNPointsspinCtrl.SetValue(1)
                self._setavNPoints(1)
                self._avNPointsspinCtrl.Enable(True)
                self._setMatSelection("Average")
                self.matFcExecutor()
        
    def lineStyleConfig(self, index):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            if index == 0:
                self._setLineChar('')
                if self._getMarkerStyleIndex()<1 or self._getMarkerStyleIndex()>21:
                    self._setMarkerStyleIndex(0)
                self.markerStyleConfig()
                self._expData.printOutput("Discreet line was selected.")
            elif index == 1:
                self._setLineChar('-')
                self._setMarkerChar('')
                self._setMarkerStyleIndex(22)
                self.replot2D(self.getXActual(), self.getYActual())
                self.SendSizeEvent()
                self._expData.printOutput("Solid line was selected.")
            elif index == 2:
                self._setLineChar('--')
                self._setMarkerChar('')
                self._setMarkerStyleIndex(22)
                self.replot2D(self.getXActual(), self.getYActual())
                self.SendSizeEvent()
                self._expData.printOutput("Dashed line was selected.")
            elif index == 3:
                self._setLineChar('-.')
                self._setMarkerChar('')
                self._setMarkerStyleIndex(22)
                self.replot2D(self.getXActual(), self.getYActual())
                self.SendSizeEvent()
                self._expData.printOutput("Dash-dot line was selected.")
            elif index == 4:
                self._setLineChar(':')
                self._setMarkerChar('')
                self._setMarkerStyleIndex(22)
                self.replot2D(self.getXActual(), self.getYActual())
                self.SendSizeEvent()
                self._expData.printOutput("Dotted line was selected.")
            else:
                self._setLineChar('-')
                self._setMarkerChar('')
                self._setMarkerStyleIndex(22)
                self.replot2D(self.getXActual(), self.getYActual())
                self.SendSizeEvent()
                self._expData.printOutput("The line style was unknow, solid line was selected by default.")
	
    def markerStyleConfig(self):
        if self._getMarkerStyleIndex() == 0:
            self._setMarkerChar('.')
            self._expData.printOutput("Point marker line was selected.")
        elif self._getMarkerStyleIndex() == 1:
            self._setMarkerChar(',')
            self._expData.printOutput("Pixel marker line was selected.")
        elif self._getMarkerStyleIndex() == 2:
            self._setMarkerChar('o')
            self._expData.printOutput("Circle marker line was selected.")
        elif self._getMarkerStyleIndex() == 3:
            self._setMarkerChar('v')
            self._expData.printOutput("Triangle down marker line was selected.")
        elif self._getMarkerStyleIndex() == 4:
            self._setMarkerChar('^')
            self._expData.printOutput("Triangle up marker line was selected.")
        elif self._getMarkerStyleIndex() == 5:
            self._setMarkerChar('<')
            self._expData.printOutput("Triangle left marker line was selected.")
        elif self._getMarkerStyleIndex() == 6:
            self._setMarkerChar('>')
            self._expData.printOutput("Triangle right marker line was selected.")
        elif self._getMarkerStyleIndex() == 7:
            self._setMarkerChar('1')
            self._expData.printOutput("Tri-down marker line was selected.")
        elif self._getMarkerStyleIndex() == 8:
            self._setMarkerChar('2')
            self._expData.printOutput("Tri-up marker line was selected.")
        elif self._getMarkerStyleIndex() == 9:
            self._setMarkerChar('3')
            self._expData.printOutput("Tri-left marker line was selected.")
        elif self._getMarkerStyleIndex() == 10:
            self._setMarkerChar('4')
            self._expData.printOutput("Tri-right marker line was selected.")
        elif self._getMarkerStyleIndex() == 11:
            self._setMarkerChar('s')
            self._expData.printOutput("Square marker line was selected.")
        elif self._getMarkerStyleIndex() == 12:
            self._setMarkerChar('p')
            self._expData.printOutput("Pentagon marker line was selected.")
        elif self._getMarkerStyleIndex() == 13:
            self._setMarkerChar('*')
            self._expData.printOutput("Star marker line was selected.")
        elif self._getMarkerStyleIndex() == 14:
            self._setMarkerChar('h')
            self._expData.printOutput("Hexagon (1) marker line was selected.")
        elif self._getMarkerStyleIndex() == 15:
            self._setMarkerChar('H')
            self._expData.printOutput("Hexagon (2) marker line was selected.")
        elif self._getMarkerStyleIndex() == 16:
            self._setMarkerChar('+')
            self._expData.printOutput("Plus marker line was selected.")
        elif self._getMarkerStyleIndex() == 17:
            self._setMarkerChar('x')
            self._expData.printOutput("X marker line was selected.")
        elif self._getMarkerStyleIndex() == 18:
            self._setMarkerChar('D')
            self._expData.printOutput("Diamond marker line was selected.")
        elif self._getMarkerStyleIndex() == 19:
            self._setMarkerChar('d')
            self._expData.printOutput("Thin diamond marker line was selected.")
        elif self._getMarkerStyleIndex() == 20:
            self._setMarkerChar('|')
            self._expData.printOutput("Vertical line marker of the line was selected.")
        elif self._getMarkerStyleIndex() == 21:
            self._setMarkerChar('_')
            self._expData.printOutput("Horizontal line marker of the line was selected.")
        elif self._getMarkerStyleIndex() == 22:
            self._setMarkerChar('')
            self._expData.printOutput("Any marker line was selected.")
        else:
            self._setMarkerChar('')
            self._expData.printOutput("The line marker style was unknow, any marker line was selected by default.")
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            self.replot2D(self.getXActual(), self.getYActual())
            self.SendSizeEvent()
	
    def colorStyleConfig(self, index):
        if index == 0:
            self._setColorChar('b')
            self._expData.printOutput("Blue line color was selected.")
        elif index == 1:
            self._setColorChar('g')
            self._expData.printOutput("Green line color was selected.")
        elif index == 2:
            self._setColorChar('r')
            self._expData.printOutput("Red line color was selected.")
        elif index == 3:
            self._setColorChar('c')
            self._expData.printOutput("Cyan line color was selected.")
        elif index == 4:
            self._setColorChar('m')
            self._expData.printOutput("Magenta line color was selected.")
        elif index == 5:
            self._setColorChar('y')
            self._expData.printOutput("Yellow line color was selected.")
        elif index == 6:
            self._setColorChar('k')
            self._expData.printOutput("Black line color was selected.")
        else:
            self._setColorChar('b')
            self._expData.printOutput("The line color style was unknow, blue line color was selected by default.")
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
        else:    
            self.replot2D(self.getXActual(), self.getYActual())
            self.SendSizeEvent()
        
    def askSavePoints(self):
        self._askPoints = True
        if self._timer.IsRunning():
            self.stopMethod()
        xp = self._getxPoints()
        yp = self._getyPoints()
        if not xp.size==0:
            if wx.MessageBox("Brands have been made on the data. Do you want to save them?.", "Please confirm",
                         wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                index = [i for i in range(0, len(xp))]
                self._setxPoints(np.delete(xp,index))
                self._setyPoints(np.delete(yp,index))
            else:
                self.saveMarks()
#Métodos para vincular con octave
                
    def _savePythonConsole(self):
        text = self._pythonShell.GetText()
        self._expData.printOutput("Python console text: \n" + text.encode('utf-8'))
        self._pythonShell.Execute("self._pythonShell.clear()")
        
    def _analizeOctaveOutput(self):
        text = self._pythonShell.GetText()
        self._expData.printOutput("Python console text: \n" + text.encode('utf-8'))
        
        indexError = text.find("Traceback")
        if not indexError == -1:
            self._octaveOutputTextCtrl.SetValue(" ")
            text1 = text[indexError:-5]
            text2 = text1.rstrip('\n')
#            self._octaveOutputTextCtrl.SetValue(text2)
            wx.MessageBox(text2, 
                          'Error from octave', wx.OK | wx.ICON_INFORMATION)
        else:
            index1 = text.find(">>>")
            text3 = text[index1:]
            index2 = text3.find("\n")
            text4 = text[index2:]
            self._octaveOutputTextCtrl.SetValue(text4)
        
        self._pythonShell.Execute("self._pythonShell.clear()")
        
    def _sendAllToOctave(self):
        if self.getDataFrame() is not None:
            self._expData.printOutput("Sending imported data to octave.")
            try:
                
                #if data.shape[0] < rowNumber:
                data = self.getDataFrame()
                
                for i in range (0, data.shape[1]):
                    #text = "octave.push('" + data.iloc[0,i] + "', data.iloc[1:,i])"
                    #wx.MessageBox(text, " ", wx.OK | wx.ICON_INFORMATION)
                    
                    self.dataToOctave, status = self.pandasToNumpy(data.iloc[1:,i])
                    
                    if status:
                        #self._pythonShell.Execute("octave.push('x', self.getXActual())")
                        self._pythonShell.Execute("octave.push('" + data.iloc[0,i] + "', self.dataToOctave)")
                    else:
                        wx.MessageBox("Problemas al pasar los datos a octave", " ", wx.OK | wx.ICON_INFORMATION)
                
#                self._pythonShell.Execute("octave.push('x', self.getXActual())")
#                self._analizeOctaveOutput()
#                self._pythonShell.Execute("octave.push('y', self.getYActual())")
#                self._analizeOctaveOutput()
#                self._pythonShell.Execute("octave.push('xoriginal', self.getXOriginal())")
#                self._analizeOctaveOutput()
#                self._pythonShell.Execute("octave.push('yoriginal', self.getYOriginal())")
#                self._analizeOctaveOutput()
            except Exception as e:
                    self._expData.writeException(e)
                
    def _sendToOctave(self):
        self._expData.printOutput("Sending data to octave.")
        try:
            self._pythonShell.Execute("octave.push('x', self.getXActual())")
            self._analizeOctaveOutput()
            self._pythonShell.Execute("octave.push('y', self.getYActual())")
            self._analizeOctaveOutput()
#            self._pythonShell.Execute("octave.push('xoriginal', self.getXOriginal())")
#            self._analizeOctaveOutput()
#            self._pythonShell.Execute("octave.push('yoriginal', self.getYOriginal())")
#            self._analizeOctaveOutput()
#        try:
#            if self._sendToOctaveListBox.GetString(self._sendToOctaveListBox.GetSelection()) == "X":
#                self._pythonShell.Execute("octave.push('x', self.getXActual())")
#                self._analizeOctaveOutput()
#                
#            if self._sendToOctaveListBox.GetString(self._sendToOctaveListBox.GetSelection()) == "Y":
#                self._pythonShell.Execute("octave.push('y', self.getYActual())")
#                self._analizeOctaveOutput()
#                
#            if self._sendToOctaveListBox.GetString(self._sendToOctaveListBox.GetSelection()) == "Original X":
#                self._pythonShell.Execute("octave.push('xoriginal', self.getXOriginal())")
#                self._analizeOctaveOutput()
#                
#            if self._sendToOctaveListBox.GetString(self._sendToOctaveListBox.GetSelection()) == "Original Y":
#                self._pythonShell.Execute("octave.push('yoriginal', self.getYOriginal())")
#                self._analizeOctaveOutput()
        except Exception as e:
                self._expData.writeException(e)
    
    def _octaveInput(self):
        if self.dataUpdateToOctave:
            try:
                self._sendToOctave()
            except Exception as e:
                self._expData.writeException(e)
        self._expData.printOutput("Sending commands to octave.")
        text = self._octaveInputTextCtrl.GetLineText(0)
        self._octaveInputTextCtrl.Clear()
        self._pythonShell.Execute('octave.eval("'+text+'")')
        self._analizeOctaveOutput()      
        
    def _xFromOctave(self, x):
        self._expData.printOutput("Receiving x from octave.")
        self._pythonShell.Execute("self.xOctave = octave.pull('"+x+"')")
        self._analizeOctaveOutput()
        self.xOctave = self.xOctave[0]
        #self._xOctChange = True
        
    def _yFromOctave(self, y):
        self._expData.printOutput("Receiving y from octave.")
        self._pythonShell.Execute("self.yOctave = octave.pull('"+y+"')")
        self._analizeOctaveOutput()
        self.yOctave = self.yOctave[0]
        #self._xOctChange = True
        
    def _octaveReplot(self):
        
        self._leftPanel.Hide()
        self._rightPanel.Hide()
        self.retrieveFromOctavePanel.Show()
        
        self._xFromOctaveLabelTextCtrl.SetFocus()
        
#        with gui.ReplotFromOctave(None, title='Change Color Depth') as cdDialog:
#            print ("********************Estoy en el dialogo!")
#            if cdDialog.ShowModal() == 1:
#                print ("********************Entre en el continue!")
#                if not cdDialog._xFromOctaveTextCtrl.GetLineText(0) == "":
#                    self._xFromOctave(cdDialog._xFromOctaveTextCtrl.GetLineText(0))
#                else:
#                    self.xOctave = np.array(None)
#                if not cdDialog._yFromOctaveTextCtrl.GetLineText(0) == "":
#                    self._yFromOctave(cdDialog._yFromOctaveTextCtrl.GetLineText(0))
#                else:
#                    self.yOctave = np.array(None)
#                status = True
#            else:
#                status = False
#    
#        cdDialog.Destroy()
        
    def _continueRetrieveFromOctave(self):
        
        if not self._xFromOctaveTextCtrl.GetLineText(0) == "":
            self._xFromOctave(self._xFromOctaveTextCtrl.GetLineText(0))
        else:
            self.xOctave = np.array(None)
        if not self._yFromOctaveTextCtrl.GetLineText(0) == "":
            self._yFromOctave(self._yFromOctaveTextCtrl.GetLineText(0))
        else:
            self.yOctave = np.array(None)
        
        x = self.getXOctave()
        y = self.getYOctave()
    
        if x.any()==None or y.any()==None:
            self._expData.writeInfo("The two arrays from Octave has not been retrieved.")
            wx.MessageBox("The two arrays from Octave has not been retrieved. You must to complete the 'Name of x array' text box and the 'Name of y array' text box, located before the 'Refresh Plot' button.", 
                          'Information', wx.OK | wx.ICON_INFORMATION)
        else:
            self._setXName(self._xFromOctaveTextCtrl.GetLineText(0))
            self._setYName(self._yFromOctaveTextCtrl.GetLineText(0))
            
            self.replot2D(x, y)
            self.setXActual(x)
            self.setYActual(y)
            
        self._xFromOctaveTextCtrl.Clear()
        self._yFromOctaveTextCtrl.Clear()
#        self._leftPanel.Show()
#        self._rightPanel.Show()
#        self.retrieveFromOctavePanel.Hide()
        self._absPosTextCtrl.SetFocus()
        
#    def addPathToOctave(self):
#        path = self._openData.getMDirPath()
#        self._pythonShell.Execute('octave.addpath("'+path+'")')
        
#    def runMFile(self):
#        path = self._openData.getMFilePath()
#        try:
#            with open(path, "r") as f:
#                list_lines = f.readlines() 
#                for line in list_lines:
#                    cut = line.find("%")
#                    self._pythonShell.Execute('octave.eval("'+line[:cut]+'")')
#        except Exception as e:
#            self._expData.writeException(e)
#            wx.MessageBox("An error occurred while trying to run the M file in Octave.", 
#                          'Information', wx.OK | wx.ICON_INFORMATION)

#Displays configs!!!
    #Muestra o esconde el panel de la grilla con los botones correspondientes.
    def displayGridChoice(self):
        if self._gridChoice.IsChecked():
            self._plotGridPanel.Show()
            self.panel.grid(color=self._getGridColor(), linestyle=self._getGridLinestyle(), linewidth=self._getGridLinewidth())
            self._figure.tight_layout()
            self._figure.canvas.draw()
            self._gridOpMenuItem.Check(True)
        else:
            self._plotGridPanel.Hide()
            self.panel.grid(False)
            self._gridOpMenuItem.Check(False)
        self.SendSizeEvent()
    #Muestra o esconde el panel File con los botones correspondientes.
    def displayGFile(self):
        if self._filePanel.IsShown():
            self._filePanel.Hide()
            self._fileToggleBtn.SetLabel("Show File")
            self._fileToggleBtn.SetValue(False)
            self._cpFileMenuItem.Check(False)
            self.SendSizeEvent()
        else:
            self._filePanel.Show()
            self._fileToggleBtn.SetLabel("Hide File")
            self._fileToggleBtn.SetValue(True)
            self._cpFileMenuItem.Check(True)
            self.SendSizeEvent()
    #Muestra o esconde el panel Configuraciones, sin preocuparse por los paneles de sonido y gráfico porque contiene los toggle buttons.
    def displayGConfig(self):
        if self._congifPanel.IsShown():
            self._congifPanel.Hide()
            self._configToggleBtn.SetLabel("Show Configuration")
            self._configToggleBtn.SetValue(False)
            self._cpCAllMenuItem.Check(False)
            self.SendSizeEvent()
        else:
            self._congifPanel.Show()
            self._configToggleBtn.SetLabel("Hide Configuration")
            self._configToggleBtn.SetValue(True)
            self._cpCAllMenuItem.Check(True)
            self.SendSizeEvent()
    #Muestra o esconde el panel Display, es suficiente porque no se esconde ningún elemento de este panel.
    def displayData(self):
        if self._displayPanel.IsShown():
            self._displayPanel.Hide()
            self._displayToggleBtn.SetLabel("Show Data Display")
            self._displayToggleBtn.SetValue(False)
            self._cpDataDisplayMenuItem.Check(False)
            self.SendSizeEvent()
            if self._mainRightSizer.IsRowGrowable(0):
                self._mainRightSizer.RemoveGrowableRow(0)
        else:
            if not self._mainRightSizer.IsRowGrowable(0):
                self._mainRightSizer.AddGrowableRow(0)
            self._displayPanel.Show()
            self._displayToggleBtn.SetLabel("Hide Data Display")
            self._displayToggleBtn.SetValue(True)
            self._cpDataDisplayMenuItem.Check(True)
            self._absPosTextCtrl.SetFocus()
            self.SendSizeEvent()
    
    def displayDataOp(self):
        if self._operationPanel.IsShown():
            self._operationPanel.Hide()
            self._cpDataOpMenuItem.Check(False)
            self._gnuOctavePanel.Show()
            self.displayOctave()
            self._sizersMFPanel.Show()
            self.displayFunctions()
        else:
            self._operationPanel.Show()
            self._cpDataOpMenuItem.Check(True)
            self._gnuOctavePanel.Hide()
            self.displayOctave()
            self._sizersMFPanel.Hide()
            self.displayFunctions()
        self.SendSizeEvent()
            
    def displayOctave(self):
        if self._gnuOctavePanel.IsShown():
            self._gnuOctavePanel.Hide()
            self._octaveToggleBtn.SetLabel("Show Octave Operation")
            self._octaveToggleBtn.SetValue(False)
            self._cpDOOctaveMenuItem.Check(False)
            if not self._sizersMFPanel.IsShown():
                self._operationPanel.Hide()
                self._cpDataOpMenuItem.Check(False)
        else:
            self._operationPanel.Show()
            self._cpDataOpMenuItem.Check(True)
            self._gnuOctavePanel.Show()
            self._octaveToggleBtn.SetLabel("Hide Octave Operation")
            self._octaveToggleBtn.SetValue(True)
            self._cpDOOctaveMenuItem.Check(True)
        self.SendSizeEvent()
        
    def displayFunctions(self):
        if self._sizersMFPanel.IsShown():
            self._sizersMFPanel.Hide()
            self._sliderToggleBtn.SetLabel("Show Sliders and Math Functions")
            self._sliderToggleBtn.SetValue(False)
            self._cpDOSliderMenuItem.Check(False)
            if not self._gnuOctavePanel.IsShown():
                self._operationPanel.Hide()
                self._cpDataOpMenuItem.Check(False)
        else:
            self._operationPanel.Show()
            self._cpDataOpMenuItem.Check(True)
            self._sizersMFPanel.Show()
            self._sliderToggleBtn.SetLabel("Hide Sliders and Math Functions")
            self._sliderToggleBtn.SetValue(True)
            self._cpDOSliderMenuItem.Check(True)
        self.SendSizeEvent()
    
    def displaySoundFontConfig (self):
        if self._soundFontPanel.IsShown():
            self._soundFontPanel.Hide()
            self._configSoundToggleBtn.SetLabel("Show Sound\nConfigurations")
            self._configSoundToggleBtn.SetValue(False)
            self._cpCSoundMenuItem.Check(False)
        else:
            self._congifPanel.Show()
            self._configToggleBtn.SetLabel("Hide Configuration")
            self._configToggleBtn.SetValue(True)
            self._cpCAllMenuItem.Check(True)
            self._soundFontPanel.Show()
            self._configSoundToggleBtn.SetLabel("Hide Sound\nConfigurations")
            self._configSoundToggleBtn.SetValue(True)
            self._cpCSoundMenuItem.Check(True)
        self.SendSizeEvent()
            
    def displayPlotConfig(self):
        if self._configPlotPanel.IsShown():
            self._configPlotPanel.Hide()
            self._configPlotToggleBtn.SetLabel("Show Plot\nConfigurations")
            self._configPlotToggleBtn.SetValue(False)
            self._cpCPlotMenuItem.Check(False)
        else:
            self._congifPanel.Show()
            self._configToggleBtn.SetLabel("Hide Configuration")
            self._configToggleBtn.SetValue(True)
            self._cpCAllMenuItem.Check(True)
            self._configPlotPanel.Show()
            self._configPlotToggleBtn.SetLabel("Hide Plot\nConfigurations")
            self._configPlotToggleBtn.SetValue(True)
            self._cpCPlotMenuItem.Check(True)
        self.SendSizeEvent()

    def displayVisualConfig(self):
        #under construction
        self.SendSizeEvent()
        
    def displayDataParamPanel(self):
        if self._openPanel.IsShown():
            self._openPanel.Hide()
            self._dataParamPlotToggleBtn.SetValue( False ) 
            self._dataParamPlotMenuItem.Check(False)
            self._dataGridMenuItem.Check(False)
        else:
            self._openPanel.Show()
            self._dataParamPlotToggleBtn.SetValue( True ) 
            self._dataParamPlotMenuItem.Check(True)
            self._dataGridMenuItem.Check(True)
        self._displayPanel.SendSizeEvent()

    def soundFontSelect(self):
        self._soundFontPanel.Hide()
        self.displaySoundFontConfig()
        self._soundFontTextCtrl.SetFocus()
        
    def panelSSInstSelect(self):
        self._soundFontPanel.Hide()
        self.displaySoundFontConfig()
        self._instTextCtrl.SetFocus()
        
    def lineStyleSelect(self):
        self._configPlotPanel.Hide()
        self.displayPlotConfig()
        self._lineStileTextCtrl.SetFocus()
        
    def markerStyleSelect(self):
        self._configPlotPanel.Hide()
        self.displayPlotConfig()
        self._markerTextCtrl.SetFocus()
        
    def colorStyleSelect(self):
        self._configPlotPanel.Hide()
        self.displayPlotConfig()
        self._colorTextCtrl.SetFocus()
        
    def gridOpSelect(self):
        self._configPlotPanel.Hide()
        self.displayPlotConfig()
        self._gridChoice.SetFocus()

#Eventos!!!
    #De aquí en adelante están los eventos derivados de la clase design_origin.py
    def _OnClose(self, event):
        self.Close()
        
    def _eventClose( self, event ):
#        try:
#            text = self._pythonShell.GetText()
#            #text.encode('utf-8')
#            self._expData.printOutput("Python console text: \n" + text.encode('utf-8'))
#        except Exception as e:
#            self._expData.writeException(e)
        if self._fileSaved: #cambiar a 'if not' para que pregunte cuando no ha sido salvado.
            if wx.MessageBox("The file has not been saved... continue closing?",
                                 "Please confirm",
                                 wx.ICON_QUESTION | wx.YES_NO, self) != wx.YES:
                return
            else:
                event.Skip()
        else:
            event.Skip()
    
    def _eventOpen( self, event ):
        self._expData.printOutput("Open button pressed.")
        self.openMethod()
        
    def _eventTitleEdData( self, event ):
        self._expData.printOutput("Enter key pressed on the text box of data title.")
        self.titleEdData()
    
    def _eventAskLabelData( self, event ):
        self._expData.printOutput("The check box to set if the data have the labels on the fisrt row, is selected.")
        self.askLabelData()
        
    def _eventAddGridChanges( self, event ):
        self._expData.printOutput("Apply changes button of the grid is pressed.")
        self.dataGridChange()
        
    def _eventUpdateGrid( self, event ):
        self._expData.printOutput("Update button of the grid is pressed.")
        self.dataGridUpdate()
        
    def _eventOriginalGrid( self, event ):
        self._expData.printOutput("Original Array button of the grid is pressed.")
        self.dataGridOriginal()
    
    def _eventAxisChoiceX( self, event ):
        self._expData.printOutput("A new choice on the X axis is selected.")
        self.axisChoiceXMethod()
        
    def _eventAxisChoiceY( self, event ):
        self._expData.printOutput("A new choice on the Y axis is selected.")
        self.axisChoiceYMethod()
        
    def _eventDeleteAllMark( self, event ):
        self._expData.printOutput("Delete all marks button is pressed.")
        self.deleteAllMark()

    def _eventSavePlot( self, event ):
        self._expData.printOutput("Export Plot button is pressed.")
        self.savePlot()
	
    def _eventSaveSound( self, event ):
        self._expData.printOutput("Export Sound button is pressed.")
        self.eSound()
	
    def _eventPlay( self, event ):
        if self.getXActual().any()==None:
            self._expData.writeInfo("The data has not been imported yet.")
            self._playButton.SetValue(False)
            self._playMenuItem.Check(False)
        else: 
            if not self._timer.IsRunning():
                self._expData.printOutput("Play button is pressed.")
                self._playButton.SetLabel("Pause")
                self._playButton.SetValue(True)
                self._playMenuItem.SetItemLabel("Pause")
                self._playMenuItem.Check(True)
                self.play()
            elif self._timer.IsRunning():
                self._expData.printOutput("Pause button is pressed.")
                self._playButton.SetLabel("Play")
                self._playButton.SetValue(False)
                self._playMenuItem.SetItemLabel("Play")
                self._playMenuItem.Check(False)
                self._dataSound.makeSound(0, -1)
                self._timer.Stop()
            else:
                self._expData.writeInfo("Error con el contador del botón Play-Pausa")

#    def _eventPause( self, event ):
#        self._expData.printOutput("Pause button is pressed.")
#        self._dataSound.makeSound(0, -1)
#        self._timer.Stop()
        
    def _eventStop( self, event ):
        self._expData.printOutput("Stop button is pressed.")
        self.stopMethod()

    def _eventMarkPt( self, event ):
        self._expData.printOutput("Mark point button is pressed.")
        self.markPoints()
        
    def _eventDeleteLastMark( self, event ):
        self._expData.printOutput("Delete last mark button is pressed.")
        self.deleteLastMark()
        
    def _eventDataParamPlot( self, event ):
        self.displayDataParamPanel()
    
    def _eventSaveData( self, event ):
        self._expData.printOutput("Export Data button is pressed.")
        self.saveData()
    
    def _eventSaveMarks( self, event ):
        self._expData.printOutput("Export Points button is pressed.")
        self.saveMarks()
    
    def _eventAbsPos( self, event ):
        self._expData.printOutput("Position Slider Bar is modified.")
        self._setTimerIndex(self._absPosSlider.GetValue())
        self.absPosSetting()
        event.Skip()
        
    def _eventSoundVel( self, event ):
        self._expData.printOutput("Sound Velocity Slider Bar is modified.")
        self._setVelocity(self._soundVelSlider.GetValue())
        if self._timer.IsRunning():
            self._timer.Stop()
            self._timer.Start((self._getVelocity()*10) + 200)

#    def _eventLVLimitSlider( self, event ):
#        self._expData.printOutput("Horizontal lower limit is setted.")
#        self.cutVertical()
    
#    def _eventUVLimitSlider( self, event ):
#        self._expData.printOutput("Horizontal upper limit is setted.")
#        self.cutVertical()

    def _eventLHLimitSlider( self, event ):
        self._expData.printOutput("Horizontal lower limit is setted.")
        self.cutHorizontal()
    
    def _eventUHLimitSlider( self, event ):
        self._expData.printOutput("Horizontal upper limit is setted.")
        self.cutHorizontal()
        
    def _eventConfigSound(self, event):
        self._expData.printOutput("Event configuration sound is setted.")
        self.displaySoundFontConfig()
        
    def _eventSelectInst(self, event):
        self._expData.printOutput("Event select instrument choice on the main display is setted.")
        self.instListBoxChoice()
        
    def _eventGFile(self, event):
        self._expData.printOutput("Event File Panel is setted.")
        self.displayGFile()
    
    def _eventGConfig(self, event):
        self._expData.printOutput("Event Config Panel is setted.")
        self.displayGConfig()
        
    def _eventGDisplay(self, event):
        self._expData.printOutput("Event data display is setted.")
        self.displayData()

    def _eventOctaveToggle( self, event ):
        self._expData.printOutput("Event octave panel is setted.")
        self.displayOctave()
        
    def _eventSliderToggle( self, event ):
        self._expData.printOutput("Event cut sliders panel is setted.")
        self.displayFunctions()
        
    def _eventMatFc(self, event):
        self._expData.printOutput("Event mathematical function is setted.")
        self.matFcSelection()
        
    def _eventAvNPoints(self, event):
        self._expData.printOutput("Event average number of points is setted.")
        self._setavNPoints(self._avNPointsspinCtrl.GetValue())
        self.matFcExecutor()
        
    def _eventMFLastCut(self, event):
        self._avNPointsspinCtrl.Enable(False)
        self._expData.printOutput("Last limits cut function is selected.")
        self._setMatSelection("Last limits cut")
        self.matFcExecutor()
        
    def _eventMFOriginal(self, event):
        self._avNPointsspinCtrl.Enable(False)
        self._expData.printOutput("Original function is selected.")
        self._setMatSelection("Original")
        self.matFcExecutor()
        
    def _eventMFInverse(self, event):
        self._avNPointsspinCtrl.Enable(False)
        self._expData.printOutput("Inverse function is selected.")
        self._setMatSelection("Inverse")
        self.matFcExecutor()

#    def _eventMFPlayBack(self, event):
#        self._avNPointsspinCtrl.Enable(False)
#        self._expData.printOutput("Play Backward function is selected.")
#        self._setMatSelection("Play Backward")
#        self.matFcExecutor()

    def _eventMFSquare(self, event):
        self._avNPointsspinCtrl.Enable(False)
        self._expData.printOutput("Square function is selected.")
        self._setMatSelection("Square")
        self.matFcExecutor()
        
    def _eventMFSquareRot( self, event ):
        self._avNPointsspinCtrl.Enable(False)
        self._expData.printOutput("Square root function is selected.")
        self._setMatSelection("Square root")
        self.matFcExecutor()

    def _eventMFLog(self, event):
        self._avNPointsspinCtrl.Enable(False)
        self._expData.printOutput("Logarithm function is selected.")
        self._setMatSelection("Logarithm")
        self.matFcExecutor()

    def _eventMFAverage(self, event):
        self._sizersMFPanel.Hide()
        self.displayFunctions()
        self._expData.printOutput("Average function is selected.")
        self.averageSelect()
        
    def _eventAbsPosSelect(self, event):
        self._expData.printOutput("Set the focus on the abscisa position.")
        self._displayPanel.Hide()
        self.displayData()
        self._absPosTextCtrl.SetFocus()
        
    def _eventTempoSelect(self, event):
        self._expData.printOutput("Set the focus on the tempo.")
        self._displayPanel.Hide()
        self.displayData()
        self._soundVelTextCtrl.SetFocus()
        
#    def _eventVLLimitSelect(self, event):
#        self._expData.printOutput("Set the focus on the vertical lower limit.")
#        self._sizersMFPanel.Hide()
#        self.displayFunctions()
#        self._lvLimitTextCtrl.SetFocus()
        
#    def _eventVULimitSelect(self, event):
#        self._expData.printOutput("Set the focus on the vertical upper limit.")
#        self._sizersMFPanel.Hide()
#        self.displayFunctions()
#        self._uvLimitTextCtrl.SetFocus()
        
    def _eventHLLimitSelect(self, event):
        self._expData.printOutput("Set the focus on the horizontal lower limit.")
        self._sizersMFPanel.Hide()
        self.displayFunctions()
        self._lhLimitTextCtrl.SetFocus()
        
    def _eventHULimitSelect(self, event):
        self._expData.printOutput("Set the focus on the horizontal upper limit.")
        self._sizersMFPanel.Hide()
        self.displayFunctions()
        self._uhLimitTextCtrl.SetFocus()
        
    def _eventAvNumPtsSelect(self, event):
        self._expData.printOutput("The average function is selected.")
        self._sizersMFPanel.Hide()
        self.displayFunctions()
        self._avNPointsTextCtrl.SetFocus()
        self.averageSelect()
        
    def _eventOctaveSelect(self, event):
        self._expData.printOutput("The octave output was selected.")
        self._gnuOctavePanel.Hide()
        self.displayOctave()
        self._octaveInputTextCtrl.SetFocus()
        
    def _eventSSInstSelect(self, event):
        self._expData.printOutput("The instrument select on panel was selected.")
        self.panelSSInstSelect()
        
    def _eventCPFileSelect(self, event):
        self._expData.printOutput("The panel file was selected.")
        self.displayGFile()
        self._openButton.SetFocus()
    
    def _eventCPDataDisplaySelect(self, event):
        self._expData.printOutput("The panel data display was selected.")
        self.displayData()
        self._absPosTextCtrl.SetFocus()
        
    def _eventCPDataOpSelect(self, event):
        self._expData.printOutput("The panel data operation was selected.")
        self.displayDataOp()
        self._octaveInputTextCtrl.SetFocus()
        
    def _eventCPDOOctaveSelect( self, event ):
        self._expData.printOutput("The panel octave was selected.")
        self.displayOctave()
        self._octaveInputTextCtrl.SetFocus()
	
    def _eventCPDOSliderSelect( self, event ):
        self._expData.printOutput("The panel sliders and mathematical functions was selected.")
        self.displayFunctions()
#        self._vAxisTextCtrl.SetFocus()
        
    def _eventCPCAllSelect(self, event):
        self._expData.printOutput("The panel configurations was selected.")
        self.displayGConfig()
        self._configSoundToggleBtn.SetFocus()
        
    def _eventCPCSoundSelect(self, event):
        self._expData.printOutput("The panel configuration sound was selected.")
        self.displaySoundFontConfig()
        self._configSoundToggleBtn.SetFocus()
    
    def _eventCPCPlotSelect(self, event):
        self._expData.printOutput("The panel configuration plot was selected.")
        self.displayPlotConfig()
        self._configPlotToggleBtn.SetFocus()
        
    def _eventCPCVisualSelect(self, event):
        self._expData.printOutput("The panel configuration visual was selected.\nUNDER CONSTRUCTION.")
        self.displayVisualConfig()
##Set focus cuando se generen los objetos

    def _eventSFSelect( self, event ):
        self._expData.printOutput("The sound font button was selected.")
        self.soundFontSelect()
        self._configSoundToggleBtn.SetFocus()
        
    def _eventConfigPlot( self, event ):
        self._expData.printOutput("Plot configurations panel was modified.")
        self.displayPlotConfig()
        self._configPlotToggleBtn.SetFocus()
	
    def _eventLineStyleConfig( self, event ):
        self._expData.printOutput("Line style of the plot was modified.")
        index = self._lineStyleChoice.GetSelection()
        self.lineStyleConfig(index)
	
    def _eventMarkerStyleConfig( self, event ):
        self._expData.printOutput("Marker style of the plot was modified.")
        self._setMarkerStyleIndex(self._markerStyleChoice.GetSelection())
        self.markerStyleConfig()
	
    def _eventColorStyleConfig( self, event ):
        self._expData.printOutput("Color style of the plot was modified.")
        index = self._colorStyleChoice.GetSelection()
        self.colorStyleConfig(index)

    def _eventLineStyleSelect( self, event ):
        self._expData.printOutput("The line style configuration is selected.")
        self.lineStyleSelect()
        
    def _eventMarkerStyleSelect( self, event ):
        self._expData.printOutput("The line marker style configuration is selected.")
        self.markerStyleSelect()
        
    def _eventColorStyleSelect( self, event ):
        self._expData.printOutput("The line color style configuration is selected.")
        self.colorStyleSelect()
        
    def _eventGridOpSelect( self, event ):
        self._expData.printOutput("The grid option configurations is selected.")
        self.gridOpSelect()
        if self._gridChoice.IsChecked():
            self._gridChoice.SetValue(False)
        else:
            self._gridChoice.SetValue(True)
        self.displayGridChoice()
        
    def _eventGridChoice( self, event ):
        self._expData.printOutput("The grid check box is selected.")
        self.displayGridChoice()
    
    def _eventGridColorChoice( self, event ):
        self._expData.printOutput("The grid color style is modified.")
        self._setGridColor(self._gridColorChoice.GetString(self._gridColorChoice.GetSelection()))
        self.displayGridChoice()
        
    def _eventGridLineChoice( self, event ):
        self._expData.printOutput("The grid line style is modified.")
        self._setGridLinestyle(self._gridLineChoice.GetString(self._gridLineChoice.GetSelection()))
        self.displayGridChoice()
        
    def _eventGridWidthSpinCtrl( self, event ):
        self._expData.printOutput("The grid width is modified.")
        self._setGridLinewidth(self._gridWidthSpinCtrl.GetValue())
        self.displayGridChoice()
        
#    def _eventSendToOctave( self, event ):
#        #Evento que envía atributo seleccionado a octave
#        self._sendToOctave()

    def _eventOctaveReplot( self, event ):
        #Evento que resetea la session de octave
        self._octaveReplot()
        
    def _eventContinueReplotFromOctave( self, event ):
        self._continueRetrieveFromOctave()
        
    def _eventCloseReplotFromOctave( self, event ):
        self._leftPanel.Show()
        self._rightPanel.Show()
        self.retrieveFromOctavePanel.Hide()
        
#    def _eventXFromOctave( self, event ):
#        #Evento que trae x array desde octave
#        self._xFromOctave()
#        
#    def _eventYFromOctave( self, event ):
#        #Evento que trae y array desde octave
#        self._yFromOctave()
        
    def _eventOctaveInput( self, event ):
        #Evento que envía comandos a octave
        self._octaveInput()
        
    def _eventHAbout( self, event ):
        message = "SonoUno is a Sonification Software for astronomical data in two column files. \n\nThis software is being developed by Bioing. Johanna Casado on her PhD tesis framework, under direction of Dr. Beatriz García. With general collaboration of Dr. Wanda Diaz Merced, and the collaboration on software development of Aldana Palma and Bioing. Julieta Carricondo Robino.\n\nThe email contact of the SonoUno team is: sonounoteam@gmail.com"
        wx.MessageBox(message, 'Information', wx.OK | wx.ICON_INFORMATION)
        
    def _eventHManual( self, event ):
        message = "The user manual of the software is located in the software root folder in PDF format, or in the next link (copy and paste on the browser): \n"
        url = "https://docs.google.com/document/d/11_mTYgqX7OdgvkuxYaXB6G3Hd4U0YRFLd9mjISAO688/edit?usp=sharing"
        dialogs.scrolledMessageDialog(parent=self, message=message+url, title='Information', pos=wx.DefaultPosition, size=(500, 150))

if __name__ == "__main__":
    app = wx.App()
    frame = core()
    frame.Show()
    app.MainLoop()
