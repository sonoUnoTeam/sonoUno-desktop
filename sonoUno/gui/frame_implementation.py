#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 15:57:00 2022

@author: johi-
"""

import platform
import wx
import numpy as np
from weakref import ref
import math
import pandas as pd
from wx.lib import dialogs
import oct2py
import re
import webbrowser

import gui.frame_design as gui
from data_import.data_import import DataImport
from sound_module.simple_sound import simpleSound
from sound_module.simple_sound import tickMark
from data_export.data_export import DataExport
from data_transform.predef_math_functions import PredefMathFunctions


class SonoUnoGUI (gui.FrameDesign):


    def __init__(self):
        
        """
        This class makes work the sonoUno interface. The specific methods are
        overwrited in the sonoUnoCore class.
        This method initialize all the class variables.
        """
        # This class inherit from gui module, class FrameDesign
        gui.FrameDesign.__init__(self)
        # Class instantiation
        self._expdata = DataExport()
        self._opendata = DataImport()
        self._datasound = simpleSound()
        self._tickmark = tickMark()
        self._matfunc = PredefMathFunctions()
        # wx.timer events
        # First timer to sonify the data
        self._timer = wx.Timer(self)
        self.Bind(
            event=wx.EVT_TIMER, 
            handler=self._sonificationloop_event, 
            source=self._timer
            )
        # Second timer to sonify the sound envelope
        self._timer_envelope = wx.Timer(self)
        self.Bind(
            event=wx.EVT_TIMER, 
            handler=self._playenvelope_event, 
            source=self._timer_envelope
            )
        # Here we assign the name of the plot panel, because this is very
        # used inside this class
        self.panel = self._axes
        # Try to open octave bridge library on Python Shell
        # Then we use this python shell to send and receive octave message
        # If the library can't be opened the GUI through an error message
        try:
            self._pythonShell.Execute("from oct2py import octave")
            self.octaveStatus = True
            self._pythonShell.Execute("self._pythonShell.clear()")
        except Exception as e:
            self.octaveStatus = False
            wx.MessageBox(
                message='Problems importing octave library.',
                caption='Information', 
                style=wx.OK | wx.ICON_INFORMATION,
                parent=None
                )
            self._expdata.writeexception(e)
        # Here we generate a dictionary of functions without parameters
        # to use on the command line for the GUI
        # In the user manual there are a list and descriptions of these functions
        self.command_dict_withoutparam = {
            'open':self.open_method,
            'dellastmark':self.deleteLastMark,
            'delallmarks':self.deleteAllMark,
            'delallmark':self.deleteAllMark,
            'savedata':self.saveData,
            'savemarks':self.saveMarks,
            'savemark':self.saveMarks,
            'saveplot':self.savePlot,
            'savesound':self.eSound,
            'quit':self.Close,
            'exit':self.Close,
            'play':self.playMethod,
            'playloop':self.playinloop,
            'pause':self.playMethod,
            'stop':self.stopMethod,
            'markpoint':self.markPoints,
            'originaldata':self.originaldata_command,
            'xlastcut':self.xlastcut_command,
            'inverse_mf':self.inverse_command,
            'square_mf':self.square_command,
            'squareroot_mf':self.squareroot_command,
            'logarithm_mf':self.logarithm_command
            }
        # Here we generate a dictionary of functions with parameters
        # to use on the command line for the GUI
        self.command_dict_withparam = {
            'xposition':self.xposition_command,
            'tempo':self.selecttempo_command,
            'xlowerlimit':self.xlowerlimit_command,
            'xupperlimit':self.xupperlimit_command,
            'octave':self._octaveInput_command,
            'fromoctave':self._retrieveFromOctave_command,
            'play_time':self.play_with_time,
            'playloop_time':self.play_with_time_inloop,
            'set_1min_loops':self.set_number_1min_loops
            }
        # Here we set some class variables to know the state of some tasks
        # 1)Flags
        self._posline_exist = False
        self._filesaved = False
        self._datasenttooctave = False
        self._inversefunc = False
        self._redraw_panel = True
        # 2)Values and counters
        self._plotcounter = 0
        self._dataperpage = 101
        self._waitonloop = 500
        self.number_1min_loops = 1500
        # Here we set some class variables with setter and getter methods
        # 1)Data file variables
        self.set_dataframe(None)
        self.set_dataframe_original(None)
        self.set_actual_x(np.array(None))
        self.set_actual_y(np.array(None))
        self._set_original_x(np.array(None))
        self._set_original_y(np.array(None))
        # 2)Counters
        self._set_timerindex(0)
        self._timerindex_space = 0
        self._set_timerenvelopeindex(0)
        # 3)Predefined variables related to sound configurations
        self._set_velocity(0)
        # -The tempo slider is setted to 0, just in case that the default value
        # -is different to that.
        self._soundVelSlider.SetValue(0)
        # -Setting the waveform list on the GUI and by default to sine
        self._swaveformlistbox.InsertItems(
            items=self._datasound.reproductor.get_available_waveforms(),
            pos=0
            )
        self._datasound.reproductor.set_waveform(
            self._swaveformlistbox.GetString(0)
            )
        # -Setting sound envelope
        adrs = self._datasound.reproductor.get_adsr()
        # -Set sliders, labels and plot of envelope
        self._soundattackslider.SetValue(adrs['a']*100)
        self._actualattacktextctrl.SetValue(str(adrs['a']))
        self._sounddecayslider.SetValue(adrs['d']*100)
        self._actualdecaytextctrl.SetValue(str(adrs['d']))
        self._soundreleaseslider.SetValue(adrs['r']*100)
        self._actualreleasetextctrl.SetValue(str(adrs['r']))
        self._soundsustainslider.SetValue(adrs['s'])
        self._actualsustaintextctrl.SetValue(str(adrs['s']))
        # -Set class variables for envelope values
        self._set_soundattack(adrs['a'])
        self._set_sounddecay(adrs['d'])
        self._set_soundsustain(adrs['s'])
        self._set_soundrelease(adrs['r'])
        # -Plot the envelope at sound configuration panel
        self.plotsoundenvelope()
        # 4)Predefined variables related to marks configuration
        self._set_markedpoints_xcoord(np.array([]))
        self._set_markedpoints_ycoord(np.array([]))
        # -This variable return True if there aren't data to save, and False
        # -if there are marks made on data without save.
        self._ask_markpoints = True
        # 5)Predefined variables related to data modifications
        self._set_mathfunction("Original")
        self._set_average_numpoints(2)
        # -Set the value to the spin control on the GUI
        self._avNPointsspinCtrl.SetValue(2)
        # 6)Predefined variables related to plot configurations
        self._set_markerstyle_index(22)
        self._set_linechar('')
        self._set_markerchar('')
        self._set_colorchar('b')
        self._set_gridcolor("Black")
        self._set_gridlinestyle("Dashed line")
        self._set_gridlinewidth(0.5)

        # Set the labels and name of the data plotted
        self._setXLabel('')
        self._setYLabel('')
        self._setXName('')
        self._setYName('')
        # Flag to detect when the original data is showed by the grid
        self.originaldataselected = True
        # Next variables can be changed later to getter and setter
        # Parameters to save the previous data file path of the method's use.
        self._prevpath = ''
        self._prevfiletipe = ''
        # self._prev_m_filepath = ''

    """
    This section below contain all the setters for class variables.
    """
    
    def set_dataframe(self, data):
        
        self._expdata.printoutput(
            "Setting class variable _dataframe."
            )
        self._dataframe = data
        
    def set_dataframe_original(self, data):
        
        self._expdata.printoutput(
            "Setting class variable dataframe_original."
            )
        self._dataframe_original = data

    def set_actual_x(self, x):
        
        self._expdata.printoutput(
            "Setting class variable x."
            )
        self.x = x

    def set_actual_y (self, y):
        self._expdata.printoutput("Setting class variable Y.")
        self.y = y

    def _set_original_x (self, xOrigin):
        self._expdata.printoutput("Setting class variable xOrigin.")
        self._xOrigin = xOrigin

    def _set_original_y (self, yOrigin):
        self._expdata.printoutput("Setting class variable yOrigin.")
        self._yOrigin = yOrigin

    def _setNormXY (self, x, y):
        self._expdata.printoutput("Setting class variables norm_x and norm_y.")
        self._norm_x = x
        self._norm_y = y
        #self._norm_x, self._norm_y, status = self._matfunc.normalize(x, y)

    def _set_timerindex (self, index):
        self._expdata.printoutput("Setting class variable timerIndex.")
        self._timerIndex = index
        
    def _set_timerenvelopeindex(self, index):
        self._timerenvelopeindex = index

    def _set_velocity (self, vel):
        self._expdata.printoutput("Setting class variable velocity.")
        self._velocity = vel

    def _set_markedpoints_xcoord (self, points):
        self._expdata.printoutput("Setting class variable xPoints.")
        self._xPoints = points

    def _set_markedpoints_ycoord (self, points):
        self._expdata.printoutput("Setting class variable yPoints.")
        self._yPoints = points

    def _set_mathfunction (self, select):
        self._expdata.printoutput("Setting class variable matSelection.")
        self._matSelection = select

    def _setHoriLower (self, hl):
        self._expdata.printoutput("Setting class variable horiLower.")
        self._horiLower = hl

    def _setHoriUpper (self, hu):
        self._expdata.printoutput("Setting class variable horiUpper.")
        self._horiUpper = hu

    def _set_average_numpoints (self, num):
        self._expdata.printoutput("Setting class variable avNPoints.")
        self._avNPoints = num

    def _set_markerstyle_index (self, index):
        self._expdata.printoutput("Setting class variable markerStyleIndex.")
        self._markerStyleIndex = index

    def _set_linechar (self, char):
        self._expdata.printoutput("Setting class variable lineChar.")
        self._lineChar = char

    def _set_markerchar (self, char):
        self._expdata.printoutput("Setting class variable markerChar.")
        self._markerChar = char

    def _set_colorchar (self, char):
        self._expdata.printoutput("Setting class variable colorChar.")
        self._colorChar = char

    def set_soundvolumn(self, vol):
        self._expdata.printoutput("Setting class variables soundvolumn.")
        self._soundvolumn = vol

    def _set_gridcolor(self, color):
        self._expdata.printoutput("Setting class variable gridColor.")
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
            self._expdata.writeinfo("The color selected is not valid.")

    def _set_gridlinestyle(self, linestyle):
        self._expdata.printoutput("Setting class variable gridLineStyle.")
        if linestyle == "Solid line":
            self._gridLinestyle = '-'
        elif linestyle == "Dashed line":
            self._gridLinestyle = '--'
        elif linestyle == "Dash-dot line":
            self._gridLinestyle = '-.'
        elif linestyle == "Dotted line":
            self._gridLinestyle = ':'
        else:
            self._expdata.writeinfo("The line style selected is not valid.")

    def _set_gridlinewidth(self, linewidth):
        self._expdata.printoutput("Setting class variable gridLinewidth.")
        self._gridLinewidth = linewidth

    def _setXLabel(self, xlabel):
        self._expdata.printoutput("Setting class variable xLabel.")
        self.xLabel = xlabel

    def _setYLabel(self, ylabel):
        self._expdata.printoutput("Setting class variable yLabel.")
        self.yLabel = ylabel

    def _setXName(self, xName):
        self._expdata.printoutput("Setting class variable xName.")
        self.xName = xName

    def _setYName(self, yName):
        self._expdata.printoutput("Setting class variable yName.")
        self.yName = yName

    def _set_soundattack(self, a):
        self._expdata.printoutput("Setting class variable soundattack.")
        self.soundattack = a

    def _set_sounddecay(self, d):
        self._expdata.printoutput("Setting class variable sounddecay.")
        self.sounddecay = d

    def _set_soundsustain(self, s):
        self._expdata.printoutput("Setting class variable soundsustain.")
        self.soundsustain = s

    def _set_soundrelease(self, r):
        self._expdata.printoutput("Setting class variable soundrelease.")
        self.soundrelease = r
        
    def setenvelope(self, env):
        self._expdata.printoutput("Setting class variable soundenv.")
        self.soundenv = env

    """
    This section below contain all the getters for class variables.
    """

    def get_dataframe (self):
        self._expdata.printoutput("Class variable dataFrame requested.")
        return self._dataframe
    
    def get_dataframe_original(self):
        self._expdata.printoutput("Class variable dataframe_original requested.")
        return self._dataframe_original

    def getXActual (self):
        self._expdata.printoutput("Class variable X requested.")
        if self.x.any() == None:
            self._expdata.writeinfo("The class variable X has not yet been set.")
        return self.x

    def getYActual (self):
        self._expdata.printoutput("Class variable Y requested.")
        if self.y.any() == None:
            self._expdata.writeinfo("The class variable Y has not yet been set.")
        return self.y

    def getXOriginal (self):
        self._expdata.printoutput("Class variable xOrigin requested.")
        if self._xOrigin.any() == None:
            self._expdata.writeinfo("The class variable xOrigin has not yet been set.")
        return self._xOrigin

    def getYOriginal (self):
        self._expdata.printoutput("Class variable yOrigin requested.")
        if self._yOrigin.any() == None:
            self._expdata.writeinfo("The class variable yOrigin has not yet been set.")
        return self._yOrigin

    def _getTimerIndex (self):
        self._expdata.printoutput("Class variable timerIndex requested.")
        return self._timerIndex
    
    def _gettimerenvelopeindex(self):
        return self._timerenvelopeindex

    def _getNormX (self):
        self._expdata.printoutput("Class variable norm_x requested.")
        return self._norm_x

    def _getNormY (self):
        self._expdata.printoutput("Class variable norm_y requested.")
        return self._norm_y

    def _getVelocity (self):
        self._expdata.printoutput("Class variable velocity requested.")
        index = [i for i in range(100, -1, -1)]
        return index[self._velocity]

    def _get_markedpoints_xcoord (self):
        self._expdata.printoutput("Class variable xPoints requested.")
        return self._xPoints

    def _get_markedpoints_ycoord (self):
        self._expdata.printoutput("Class variable yPoints requested.")
        return self._yPoints

    def _getMatSelection (self):
        self._expdata.printoutput("Class variable matSelection requested.")
        return self._matSelection

    def _getHoriLower (self):
        self._expdata.printoutput("Class variable horiLower requested.")
        return self._horiLower

    def _getHoriUpper (self):
        self._expdata.printoutput("Class variable horiUpper requested.")
        return self._horiUpper

    def _getavNPoints (self):
        self._expdata.printoutput("Class variable avNPoints requested.")
        return self._avNPoints

    def _getMarkerStyleIndex (self):
        self._expdata.printoutput("Class variable markerStyleIndex requested.")
        return self._markerStyleIndex

    def _getLineChar (self):
        self._expdata.printoutput("Class variable lineChar requested.")
        return self._lineChar

    def _getMarkerChar (self):
        self._expdata.printoutput("Class variable markerChar requested.")
        return self._markerChar

    def _getColorChar (self):
        self._expdata.printoutput("Class variable colorChar requested.")
        return self._colorChar

    def _getPlotStile (self):
        self._expdata.printoutput("Graphic style requested.")
        return (self._getColorChar() + self._getMarkerChar() + self._getLineChar())

    def get_soundvolumn(self):
        return self._soundvolumn

    def _getGridColor(self):
        self._expdata.printoutput("Class variable gridColor requested.")
        return self._gridColor

    def _getGridLinestyle(self):
        self._expdata.printoutput("Class variable gridLinestyle requested.")
        return self._gridLinestyle

    def _getGridLinewidth(self):
        self._expdata.printoutput("Class variable gridLinewidth requested.")
        return self._gridLinewidth

    def getXLabel(self):
        self._expdata.printoutput("Class variable xLabel requested.")
        return self.xLabel

    def getYLabel(self):
        self._expdata.printoutput("Class variable yLabel requested.")
        return self.yLabel

    def getXName(self):
        self._expdata.printoutput("Class variable xName requested.")
        return self.xName

    def getYName(self):
        self._expdata.printoutput("Class variable yName requested.")
        return self.yName

    def getXOctave(self):
        self._expdata.printoutput("Class variable xOctave requested.")
        return self.xOctave

    def getYOctave(self):
        self._expdata.printoutput("Class variable yOctave requested.")
        return self.yOctave

    def _get_soundattack(self):
        self._expdata.printoutput("Class variable soundattack requested.")
        return self.soundattack

    def _get_sounddecay(self):
        self._expdata.printoutput("Class variable sounddecay requested.")
        return self.sounddecay

    def _get_soundsustain(self):
        self._expdata.printoutput("Class variable soundsustain requested.")
        return self.soundsustain

    def _get_soundrelease(self):
        self._expdata.printoutput("Class variable soundrelease requested.")
        return self.soundrelease
    
    def getenvelope(self):
        self._expdata.printoutput("Class variable soundenv requested.")
        return self.soundenv

    """
    This section below contain the own methods of GUI operation.
    """

    def set_cutplot_sliderlimits (self, xOrigin, yOrigin, x, y):
        
        """
        This method update the slider limits dedicated to cut the plot axis.
        The vertical cut has not been enabled yet.
        """
        self._expdata.printoutput("Update cut slider limits.")
        # In the cut plot functionality we have to update two things:
        # 1) Show the limit values instead of array position at the slider 
        # limits (Here)
        # 2) Enable vertical limits cut with tickmarks (in other methods)
        
        # try:
        #     # Set lower vertical slider limits
        #     self._lVLimitSlider.SetMax()
        #     self._lVLimitSlider.SetMin()
        #     self._lVLimitSlider.SetValue()
        # except Exception as e:
        #     self._expdata.writeexception(e)
        # try:
        #     # Set upper vertical slider limits
        #     self._uVLimitSlider.SetMax()
        #     self._uVLimitSlider.SetMin()
        #     self._uVLimitSlider.SetValue()
        # except Exception as e:
        #     self._expdata.writeexception(e)
        try:
            # Set lower horizontal slider limits
            self._lHLimitSlider.SetMax(xOrigin.size)
            self._lHLimitSlider.SetMin(0)
            self._lHLimitSlider.SetValue(self._getHoriLower())
        except Exception as e:
            self._expdata.writeexception(e)
        try:
            # Set upper horizontal slider limits
            self._uHLimitSlider.SetMax(xOrigin.size)
            self._uHLimitSlider.SetMin(0)
            self._uHLimitSlider.SetValue(self._getHoriUpper())
        except Exception as e:
            self._expdata.writeexception(e)
        # Send a size event to update the GUI
        self.SendSizeEvent()

    def set_xslider_limits (self, x):
        
        """
        This method update the x limits slider and the actual position.
        The values shown at slider are the array values.
        We named the x axis as abscissa.
        """
        self._expdata.printoutput("Setting the x slider limits.")
        try:
            # Set the element slider min and max value with the number of
            # elements in the array.
            self._abspos_slider.SetMax(x.size-1)
            self._abspos_slider.SetMin(0)
            # Set x slider textctrls which indicates the min and max value
            # and the actual position above the slider
            self._absminlabel_textctrl.SetValue(
                value=str(round(x[0],4))
                )
            self._absmaxlabel_textctrl.SetValue(
                value=str(round(x[x.size-1],4))
                )
            self._absposlabel_textctrl.SetValue(
                value=str(round(x[self._abspos_slider.GetValue()],4))
                )
        except Exception as e:
            self._expdata.writeexception(e)
        # Send a size event to update the GUI and show the changes
        self.SendSizeEvent()
            
    def set_plottitles(self):
        
        """
        This method put the titles and labels of the data on the plot
        """
        self._expdata.printoutput("Setting the titles and labels of the plot.")
        try:
            self.panel.set_title(self._titleEdDataTextCtrl.GetValue())
            self.panel.set_xlabel(self.getXName())
            self.panel.set_ylabel(self.getYName())
        except Exception as e:
            self._expdata.writeexception(e)

    def plot_xy(self, x, y):
        
        """
        This method plot one column against x axis.
        """
        self._expdata.printoutput("Plot one column against x axis.")
        # Check if the plot grid is enabled or not to plot it
        try:
            if self._gridChoice.IsChecked():
                self.panel.grid(
                    color=self._getGridColor(), 
                    linestyle=self._getGridLinestyle(), 
                    linewidth=self._getGridLinewidth()
                    )
        except Exception as e:
            self._expdata.writeexception(e)
        # Plot y against x
        try:
            # The line ploted is not used yet, but the idea is that some lines
            # change constantly, like position line, and others not.
            self._line_xy = self.panel.plot(x, y, self._getPlotStile())
            # This counter allow as to know how many lines are plotted on the
            # graph
            self._plotcounter = self._plotcounter + 1
        except Exception as e:
            self._expdata.writeexception(e)
        # This variable indicates when the plot was updated, to send to octave
        # the new data when the user enter a new command to that interface
        self._datasenttooctave = True
        # Finally, update the plot figure to visualize the new plot
        if self._redraw_panel:
            self._figure.tight_layout()
            self._figure.canvas.draw()

    def plot_positionline (self, abscisa, ordenada):
        
        """
        This method plot the vertical position line on the plot.
        """
        self._expdata.printoutput("Plot the position line.")
        try:
            # If the line doesn't exist change the state variable to True,
            # if the line exist, erase the previous line to plot the next one.
            if not self._posline_exist:
                self._posline_exist = True
            else:
                self.panel.lines.remove(self._positionline_reference())
            # Plot the position line
            self.panel.plot(abscisa, ordenada, 'r')
            # Generate the reference to erase the position line next time
            self._positionline_reference = ref(
                self.panel.lines[self._plotcounter]
                )
        except Exception as e:
            self._expdata.writeexception(e)
        # Finally, update the plot figure to visualize the new plot
        if self._redraw_panel:
            self._figure.tight_layout()
            self._figure.canvas.draw()

    def plot_markline(self, abs_markpoint, ord_markpoint):
        
        """
        This method plot the line to mark a point.
        """
        self._expdata.printoutput("Plot a mark line.")
        try:
            # Plot a mark and add one to the plot counter variable
            self.panel.plot(abs_markpoint, ord_markpoint, 'k')
            self._plotcounter = self._plotcounter + 1
        except Exception as e:
            self._expdata.writeexception(e)
        # Finally, update the plot figure to visualize the new plot
        if self._redraw_panel:
            self._figure.tight_layout()
            self._figure.canvas.draw()

    def replot_xy (self, x, y):
        
        """
        This method erase the plot and draw it again.
        """
        # If data don't exist throw a message to log output
        # If data exist continue with the tasks
        if x.any()==None or y.any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            try:
                self._expdata.printoutput("Clean and plot the graph")
                # Set position line flag
                self._posline_exist = False
                # Erase the plot
                self.panel.cla()
                self._figure.canvas.draw()
                # Restore the lines array and plot counter to cero
                self.panel.lines = []
                self._plotcounter = 0
            except Exception as e:
                self._expdata.writeexception(e)
            # If inverse function is selected, invert the y axis
            if self._inversefunc:
                self.panel.invert_yaxis()
            # Set an state value to not refresh the plot when draw each line
            self._redraw_panel = False
            # Draw the data file
            try:
                self.set_plottitles()
                self.plot_xy(x, y)
            except Exception as e:
                self._expdata.writeexception(e)
            # Draw the position line
            try:
                timerIndex = self._getTimerIndex()
                if not timerIndex==0: 
                    if np.isnan(x[timerIndex]) or np.isnan(y[timerIndex]):
                        self._expdata.writeinfo(
                            "This point is a nan value, for that the red line"
                            + " is not updated."
                            )
                    else:
                        # The function np.nanmin is used to not consider the
                        # nan values as minimum or maximum value
                        ordenada = np.array(
                            [float(np.nanmin(y)), float(np.nanmax(y))]
                            )
                        abscisa = np.array(
                            [float(x[timerIndex]), float(x[timerIndex])]
                            )
                        self.plot_positionline(abscisa, ordenada)
            except Exception as e:
                self._expdata.writeexception(e)
            # Draw the marks that was made on the data
            try:
                marks_on_x = self._get_markedpoints_xcoord()
                for i in range (0, marks_on_x.size):
                    abs_markpoint = np.array(
                        [float(marks_on_x[i]), float(marks_on_x[i])]
                        )
                    ord_markpoint = np.array(
                        [float(np.nanmin(y)), float(np.nanmax(y))]
                        )
                    self.plot_markline(abs_markpoint, ord_markpoint)
            except Exception as e:
                self._expdata.writeexception(e)
            # Finally, update the plot figure to visualize the new plot
            self._figure.tight_layout()
            self._figure.canvas.draw()
            self.SendSizeEvent()
            # Restore the value of the flag to redraw the plot on other methods
            self._redraw_panel = True

    def _sonificationloop_event (self, event):
        
        """
        This method sonify the data plotted when the user presses the button 
        play and updates the position mark on the plot.
        In addition, first it checks if the data exist and check to reset 
        time for loop functionality after play the tickmark.
        """
        if self._timer.GetInterval()==self._waitonloop and self.playinloop_state:
            self._timer.Start((self._getVelocity()*2) + 10)
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            self._expdata.printoutput("Generate the sound and refresh plot.")
            # Get the current timer index setted on the last loop
            timer_index = self._getTimerIndex()
            # Get the x and y array plotted
            x=self.getXActual()
            y=self.getYActual()
            # If the current point to sonify is a nan value don't sonify and
            # don't update the plot
            if np.isnan(x[timer_index]) or np.isnan(y[timer_index]):
                self._expdata.writeinfo(
                    ("This point is a nan value, for that the position line "
                     + "and sound is not updated.")
                    )
            else:
                # If the current position is not nan, check the distance
                # between notes
                if timer_index > 0:
                    # If the distance is lower or the same than 
                    # self._minspace_x continue with sonification, if not
                    # add empty space
                    if self._minspace_x_array[timer_index-1] > self._minspace_x:
                        cycles = int(self._minspace_x_array[timer_index-1] 
                            / self._minspace_x)
                        
                        
                        
                        if cycles != self._timerindex_space:
                            self._timerindex_space = self._timerindex_space + 1
                            
                            # Try to update red line to make a continuous advance
                            # Update the plot (make only one redline update)
                            try:
                                ordenada = np.array(
                                    [float(np.nanmin(y)), float(np.nanmax(y))]
                                    )
                                new_abscisa = (x[timer_index-1] 
                                               + (self._minspace_x 
                                                  * self._timerindex_space))
                                abscisa = np.array(
                                    [float(new_abscisa), float(new_abscisa)]
                                    )
                                self.plot_positionline(abscisa, ordenada)
                            except Exception as e:
                                self._expdata.writeexception(e)
                            return
                        else:
                            self._timerindex_space = 0
                # Update the plot
                try:
                    ordenada = np.array(
                        [float(np.nanmin(y)), float(np.nanmax(y))]
                        )
                    abscisa = np.array(
                        [float(x[timer_index]), float(x[timer_index])]
                        )
                    self.plot_positionline(abscisa, ordenada)
                except Exception as e:
                    self._expdata.writeexception(e)
                # Sonify the current point of the normalized array
                try:
                    self._datasound.make_sound(
                        self._getNormY()[timer_index], 
                        timer_index
                        )
                except Exception as e:
                    self._expdata.writeexception(e)
            # Update the abscisa position and its text control
            try:
                self._abspos_slider.SetValue(timer_index)
                self._absposlabel_textctrl.SetValue(
                    value=str(round(x[self._abspos_slider.GetValue()],4))
                    )
            except Exception as e:
                self._expdata.writeexception(e)
            # Increment the timer index
            self._set_timerindex(timer_index + 1)
            # Check if the timer index reach the end
            if timer_index==(x.size-1):
                # If loop is enable, play the tickmark and restart the 
                # sonification. If not, stop the reproduction.
                if self.playinloop_state:
                    self._tickmark.loop()
                    self._timer.Start(self._waitonloop)
                    self._set_timerindex(0)
                    self._abspos_slider.SetValue(0)
                    self._absposlabel_textctrl.SetValue(str(round(self.getXActual()[self._abspos_slider.GetValue()],4)))
                else:
                    self.stopMethod()
                
    def _playenvelope_event(self, event):
        
        """
        This method sonify the envelope plot located on sound settings.
        """
        # Get index, envelope array and samples array
        timer_index = self._gettimerenvelopeindex()
        env = self.getenvelope()
        n_samples = np.arange(0.0, env.size)
        # Get normalized array to sonify
        norm_x, norm_y, status = self._matfunc.normalize(n_samples, env)
        # Sonify the corresponding point
        self._datasound.make_sound(norm_y[timer_index], timer_index)
        # Increment timer index
        self._set_timerenvelopeindex(timer_index + 1)
        # Check if the envelope array reach the end and initialize variables
        if timer_index==(env.size-1):
            self._envelopeplaytogglebtn.SetLabel('Play envelope\nsound')
            self._envelopeplaytogglebtn.SetValue(False)
            self._set_timerenvelopeindex(0)
            self._timer_envelope.Stop()

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
                    self._opendata.set_datafilename(filedialog.GetFilename())
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
            self._expdata.writeexception(Error)
            return self._prevpath, self._prevfiletipe, False

    def open_method(self):
        
        """
        This method allow to open a dataset serching it on the computer file
        system.
        """
        # Check if the sonification loop is running to stop it
        if self._timer.IsRunning():
            self.stopMethod()
            wx.MessageBox(
                message=("The previous reproduction of the data has been "
                         + "stopped."),
                caption='Information', 
                style=wx.OK | wx.ICON_INFORMATION
                )
        # If there are unsaved marks on data, ask if the user want to save them
        if not self._ask_markpoints:
            self.askSavePoints()
        try:
            # Get the path where the datafile exist on the computer and the
            # type pf datafile to open
            pathName, fileTipe, pathstatus = self.get_datapath()
            # Open the dataset using the previous path
            data, status, msg = self._opendata.set_arrayfromfile(
                pathName, 
                fileTipe
                )
            # If the flag 'status' is False, show a message indicating that
            # there was a problem opening the datafile, if not continue with
            # the tasks.
            if not status:
                wx.MessageBox(
                    message=("The data file can't be opened, the software "
                        + "continue with the previous data if exist. \nCheck "
                        + "the problem and contact the development team if "
                        + "you need help.\n\nThe problem is:\n"+msg+"\n\n"
                        + "Contact mail: sonounoteam@gmail.com."),
                    caption='Information', 
                    style=wx.OK | wx.ICON_INFORMATION
                    )
            else:
                # Set datafile name on the specific text space on data
                # parameters panel
                self._titleEdDataTextCtrl.SetValue(
                    value=self._opendata.get_datafilename()[:-4]
                    )
                # Store dataframe on two specific class variable one to
                # modify and another to store the original dataset
                self.set_dataframe(data)
                self.set_dataframe_original(data)
                # Obtain the x and y array to plot, convert dataframe to numpy
                x, y, status1 = self.dataSelection(data)
                
                # Calculate the array with the space between each 
                # data point the first time (then this value is updated on
                # play())
                self._minspace_x_array = x[1:] - x[:x.size-1]
                # Calculate the minimum space between data points
                #self._minspace_x = np.nanmin(self._minspace_x_array)
                self._minspace_x = np.nanmin(
                    np.where(
                        self._minspace_x_array == 0, 
                        np.nan, 
                        self._minspace_x_array
                        )
                    )
                
                if status1:
                    self.set_actual_x(x)
                    self.set_actual_y(y)
                    self._set_original_x(x)
                    self._set_original_y(y)
                    self._setHoriLower(0)
                    self._setHoriUpper(x.size)
                    self.set_cutplot_sliderlimits(x, y, x, y)
                    # self.setArrayLimits(x, y)
                    self.set_xslider_limits(x)
                    self._sendAllToOctave()
                    self.replot_xy(x, y)
                    self._expdata.printoutput("Data imported and graphed.")
                else:
                    wx.MessageBox("The data file can't be opened, the software continue with the previous data if exist. \nCheck the file and contact the development team if you need help.\nContact mail: sonounoteam@gmail.com.",
                          'Information', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            self._expdata.writeexception(e)

    def _setdatagridpage(self, pos):
        data = self.get_dataframe()
        if data.shape[1]<2:
            return False

        # #Chequeo si los datos son menos de cierto valor
        # if self._dataperpage < data.shape[0]:
        #     rowNumber = self._dataperpage
        # else:
        #     rowNumber = data.shape[0]

        if pos == 1:
            if data.shape[0] < self._dataperpage :
                #los datos son menos de 100
                rows = data.shape[0]
                initialnumber = 0
                self._setgridsize(rows, data.shape[1])
                self._loadintogrid(data, initialnumber, rows, data.shape[1])
            else:
                #cargar los primeros 100 datos
                rows = 101
                initialnumber = 0
                self._setgridsize(rows, data.shape[1])
                self._loadintogrid(data, initialnumber, rows, data.shape[1])
        else:
            gridpages = int(data.shape[0]/self._dataperpage)
            if pos > gridpages:
                #cargar la ultima pagina
                rows = data.shape[0] - gridpages*100
                initialnumber = gridpages*100
                self._setgridsize(rows, data.shape[1])
                self._loadintogrid(data, initialnumber, rows, data.shape[1])
            else:
                #detectar pagina y cargar 100 datos
                rows = 101
                initialnumber = (pos-1)*100
                self._setgridsize(rows, data.shape[1])
                self._loadintogrid(data, initialnumber, rows, data.shape[1])

    def _setgridsize(self, rows, cols):
        #Redimencionamos la grilla
        if cols>self._dataGrid.GetNumberCols():
            self._dataGrid.AppendCols(cols-self._dataGrid.GetNumberCols())
        elif cols<self._dataGrid.GetNumberCols():
            self._dataGrid.DeleteCols( numCols=(self._dataGrid.GetNumberCols()-cols) )
        if rows>self._dataGrid.GetNumberRows():
            self._dataGrid.AppendRows(rows-self._dataGrid.GetNumberRows())
        elif rows<self._dataGrid.GetNumberRows():
            self._dataGrid.DeleteRows( numRows=(self._dataGrid.GetNumberRows()-rows) )

    def _loadintogrid(self, data, init, rows, cols):
        for j in range (init,(rows+init)): #recorre filas
            for i in range (0,cols): #recorre columnas
                self._dataGrid.SetCellValue (j-init, i, str(data.iloc[j,i]))
                if not j-init == 0:
                    self._dataGrid.SetReadOnly(j-init, i, isReadOnly=True)
                    self._dataGrid.SetRowLabelValue(j-init, str(j))
                else:
                    self._dataGrid.SetReadOnly(j-init, i, isReadOnly=False)
                    self._dataGrid.SetCellValue (j-init, i, str(data.iloc[j-init,i]))
                    self._dataGrid.SetRowLabelValue(j-init, ' ')

    def dataSelection(self, data):
        # if self._dataperpage < data.shape[0]:
        #     if wx.MessageBox("The data file have more than 5000 values, the software might delay to show all the data array on a grid element. Do you want to display all the values on the grid element anyway?\n\nNOTE: The other functionalities (plot, math fuctions, etc) use all the values of the array in any case.", "Information", wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
        #         rowNumber = self._dataperpage
        #     else:
        #         rowNumber = data.shape[0]
        # else:
        #     rowNumber = data.shape[0]

        if data.shape[1]<2:
            return None, None, False

        # #Chequeo si los datos son menos de cierto valor
        # if self._dataperpage < data.shape[0]:
        #     rowNumber = self._dataperpage
        # else:
        #     rowNumber = data.shape[0]

        #Limpio la grilla
        self._dataGrid.ClearGrid()
        pages = int(data.shape[0]/100)+1
        self._datagridslider.SetMax(pages)
        self._maxgridpagetextctrl.SetValue(str(pages))
        self._setdatagridpage(self._datagridslider.GetValue())
        # #Redimencionamos la grilla
        # if data.shape[1]>self._dataGrid.GetNumberCols():
        #     self._dataGrid.AppendCols(data.shape[1]-self._dataGrid.GetNumberCols())
        # elif data.shape[1]<self._dataGrid.GetNumberCols():
        #     self._dataGrid.DeleteCols( numCols=(self._dataGrid.GetNumberCols()-data.shape[1]) )
        # if rowNumber>self._dataGrid.GetNumberRows():
        #     self._dataGrid.AppendRows(rowNumber-self._dataGrid.GetNumberRows())
        # elif rowNumber<self._dataGrid.GetNumberRows():
        #     self._dataGrid.DeleteRows( numRows=(self._dataGrid.GetNumberRows()-rowNumber) )
#        #Lo coloco en la grilla
        #dlg = wx.ProgressDialog("Loading data to the grid", " ", maximum=data.shape[0], style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT)
        #dlg.Show()
        # table = DataTable(data)
        # self._dataGrid.SetTable(table, takeOwnership=True)
        # self._dataGrid.AutoSizeColumns()
        # self._dataGrid.HideCol(0)

        # if data.shape[0] < rowNumber:
        #     for j in range (0,data.shape[0]):
        #         for i in range (0,data.shape[1]):
        #             self._dataGrid.SetCellValue (j, i, str(data.iloc[j,i]))
        #             if not j == 0:
        #                 self._dataGrid.SetReadOnly(j, i, isReadOnly=True)
        #             else:
        #                 self._dataGrid.SetReadOnly(j, i, isReadOnly=False)
        #         dlg.Pulse("Loading data")
        #         #dlg.Update(j, "Loading data")
        #         #dlg.Update (j, "%i of %i"%(j, int(data.shape[0])))
        #         if dlg.WasCancelled():
        #             break
        # else:
        #     for j in range (0,rowNumber):
        #         for i in range (0,data.shape[1]):
        #             self._dataGrid.SetCellValue (j, i, str(data.iloc[j,i]))
        #             if not j == 0:
        #                 self._dataGrid.SetReadOnly(j, i, isReadOnly=True)
        #             else:
        #                 self._dataGrid.SetReadOnly(j, i, isReadOnly=False)
        #         #dlg.Update(j, "Loading data")
        #         dlg.Pulse("Loading data")
        #         #dlg.Update (j, "%i of %i"%(j, int(data.shape[0])))
        #         if dlg.WasCancelled():
        #             break
        #dlg.Destroy()
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
            self._expdata.writeexception(e)

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
                self._expdata.writeexception(e)
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
                                  'Information', wx.OK | wx.ICON_INFORMATION)
                    delNum=False
                    xnumpy=np.delete(xnumpy, self.del_xy)
                    ynumpy=np.delete(ynumpy, self.del_xy)
            except Exception as e:
                self._expdata.writeexception(e)

        return xnumpy, ynumpy, status

    def pandasToNumpy(self, x):
        #Se generan los numpy array de las primeras dos columnas y se devuelven
        try:
            xnumpy = x.values.astype(np.float64)
            status=True
        except Exception as e:
            status=False
            xnumpy=np.array(None)
            self._expdata.writeexception(e)

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
                self._expdata.writeexception(e)
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
                self._expdata.writeexception(e)

        return xnumpy, status

    def titleEdData(self):
        #Fijarse si es aquí donde se pierden los labels
        self.panel.set_title(self._titleEdDataTextCtrl.GetValue())
        self._figure.tight_layout()
        self._figure.canvas.draw()

    # def askLabelData(self):
    #     if self.get_dataframe() is not None:
    #         data = self.get_dataframe()
    #         if not self._askLabelDataCheckBox.IsChecked():
    #             self._dataGrid.InsertRows()
    #             for i in range (0,data.shape[1]):
    #                 self._dataGrid.SetReadOnly(1, i, isReadOnly=True)
    #         else:
    #             if self._dataGrid.GetNumberRows() > self._dataperpage:
    #                 self._dataGrid.DeleteRows()
    #                 for i in range (0,data.shape[1]):
    #                     self._dataGrid.SetReadOnly(0, i, isReadOnly=False)
    #     else:
    #         self._expdata.writeinfo("The data has not been opened yet.")
    #         wx.MessageBox("The data has not been opened yet.",
    #                       'Info', wx.OK | wx.ICON_INFORMATION)

    def dataGridChange(self):
        #Cambia los nombres de columnas modificados en la grilla, pero aun no los
        #guarda en el array de datos
        if self.get_dataframe() is not None:
            data = self.get_dataframe()
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
                self.set_plottitles()
                self._figure.tight_layout()
                self._figure.canvas.draw()
            else:
                wx.MessageBox("The column numbers of data and grid don't match.",
                    'Info', wx.OK | wx.ICON_INFORMATION)

    def _loadintogrid_array(self, x, y, init, rows):
        for j in range (1+init,rows+init):
            self._dataGrid.SetCellValue (j-init, 0, str(x[j-1]))
            self._dataGrid.SetCellValue (j-init, 1, str(y[j-1]))
            self._dataGrid.SetReadOnly(j-init, 0, isReadOnly=True)
            self._dataGrid.SetReadOnly(j-init, 1, isReadOnly=True)

        # for j in range (init,(rows+init)): #recorre filas
        #     for i in range (0,cols): #recorre columnas
        #         self._dataGrid.SetCellValue (j-init, i, str(data.iloc[j,i]))
        #         if not j-init == 0:
        #             self._dataGrid.SetReadOnly(j-init, i, isReadOnly=True)
        #         else:
        #             self._dataGrid.SetReadOnly(j-init, i, isReadOnly=False)
        #             self._dataGrid.SetCellValue (j-init, i, str(data.iloc[j-init,i]))

    def dataGridUpdate(self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            x = self.getXActual()
            y = self.getYActual()

            # if self._dataperpage < x.shape[0]:
            #     if wx.MessageBox("The data file have more than 5000 values, the software might delay to show all the data array on a grid element. Do you want to display all the values on the grid element anyway?\n\nNOTE: The other functionalities (plot, math fuctions, etc) use all the values of the array in any case.", "Information", wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
            #         rowNumber = self._dataperpage
            #     else:
            #         rowNumber = x.shape[0]
            # else:
            #     rowNumber = x.shape[0]

            #Limpio la grilla
            self._dataGrid.ClearGrid()

            pos = self._datagridslider.GetValue()
            if pos == 1:
                if x.shape[0] < self._dataperpage :
                    #los datos son menos de 100
                    rows = x.shape[0]
                    initialnumber = 0
                    self._setgridsize(rows, 2)
                    self._loadintogrid_array(x, y, initialnumber, rows)
                else:
                    #cargar los primeros 100 datos
                    rows = 101
                    initialnumber = 0
                    self._setgridsize(rows, 2)
                    self._loadintogrid_array(x, y, initialnumber, rows)
            else:
                gridpages = int(x.shape[0]/self._dataperpage)
                if pos > gridpages:
                    #cargar la ultima pagina
                    rows = x.shape[0] - gridpages*100
                    initialnumber = gridpages*100
                    self._setgridsize(rows, 2)
                    self._loadintogrid_array(x, y, initialnumber, rows)
                else:
                    #detectar pagina y cargar 100 datos
                    rows = 101
                    initialnumber = (pos-1)*100
                    self._setgridsize(rows, 2)
                    self._loadintogrid_array(x, y, initialnumber, rows)

            #Redimencionamos la grilla

            # if 2>self._dataGrid.GetNumberCols():
            #     self._dataGrid.AppendCols(2-self._dataGrid.GetNumberCols())
            # elif 2<self._dataGrid.GetNumberCols():
            #     self._dataGrid.DeleteCols( numCols=(self._dataGrid.GetNumberCols()-2) )
            # if rowNumber>self._dataGrid.GetNumberRows():
            #     self._dataGrid.AppendRows(rowNumber-self._dataGrid.GetNumberRows())
            # elif rowNumber<self._dataGrid.GetNumberRows():
            #     self._dataGrid.DeleteRows( numRows=(self._dataGrid.GetNumberRows()-rowNumber) )

            #Detectar los titulos de columna
            data = self.get_dataframe()
            self._dataGrid.SetCellValue (0, 0, str(data.iloc[0,self._axisChoiceX.GetSelection()]))
            self._dataGrid.SetCellValue (0, 1, str(data.iloc[0,self._axisChoiceY.GetSelection()]))
            self._dataGrid.SetReadOnly(0, 0, isReadOnly=True)
            self._dataGrid.SetReadOnly(0, 1, isReadOnly=True)

            #Lo coloco en la grilla

            # dlg = wx.ProgressDialog("Loading data to the grid", " ", maximum=data.shape[0], style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT)
            # dlg.Show()
            # if x.shape[0] < rowNumber:
            #     for j in range (1,x.shape):
            #         self._dataGrid.SetCellValue (j, 0, str(x[j-1]))
            #         self._dataGrid.SetCellValue (j, 1, str(y[j-1]))
            #         self._dataGrid.SetReadOnly(j, 0, isReadOnly=True)
            #         self._dataGrid.SetReadOnly(j, 1, isReadOnly=True)
            #         dlg.Pulse("Loading data")
            #         #dlg.Update(j, "Loading data")
            #         #dlg.Update (j, "%i of %i"%(j, int(data.shape[0])))
            #         if dlg.WasCancelled():
            #             break
            # else:
            #     for j in range (1,rowNumber):
            #         self._dataGrid.SetCellValue (j, 0, str(x[j-1]))
            #         self._dataGrid.SetCellValue (j, 1, str(y[j-1]))
            #         self._dataGrid.SetReadOnly(j, 0, isReadOnly=True)
            #         self._dataGrid.SetReadOnly(j, 1, isReadOnly=True)
            #         dlg.Pulse("Loading data")
            #         #dlg.Update(j, "Loading data")
            #         #dlg.Update (j, "%i of %i"%(j, int(data.shape[0])))
            #         if dlg.WasCancelled():
            #             break
            # dlg.Destroy()

    def dataGridOriginal(self):
        if self.get_dataframe() is not None:
            data = self.get_dataframe()

            if self._dataperpage < data.shape[0]:
                if wx.MessageBox("The data file have more than 5000 values, the software might delay to show all the data array on a grid element. Do you want to display all the values on the grid element anyway?\n\nNOTE: The other functionalities (plot, math fuctions, etc) use all the values of the array in any case.", "Information", wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                    rowNumber = self._dataperpage
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
        if self.get_dataframe() is not None:
            if not self._ask_markpoints:
                self.askSavePoints()
            data = self.get_dataframe()
            self._setXLabel(self._axisChoiceX.GetSelection())
            self._setXName(self._axisChoiceX.GetString(self._axisChoiceX.GetSelection()))
            #wx.MessageBox(self.getXName(), 'Info', wx.OK | wx.ICON_INFORMATION)
            x1 = data.loc[1:,self._axisChoiceX.GetSelection()]
            x = x1.values.astype(np.float64)
            self.set_actual_x(x)
            self._set_original_x(x)
            y = self.getYOriginal()
            self._setHoriLower(0)
            self._setHoriUpper(x.size)
            self.set_cutplot_sliderlimits(x, y, x, y)
            # self.setArrayLimits(x, y)
            self.set_xslider_limits(x)
            self.replot_xy(x, y)

    def axisChoiceYMethod(self):
        if self.getXOriginal().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            if self.get_dataframe() is not None:
                if not self._ask_markpoints:
                    self.askSavePoints()
                data = self.get_dataframe()
                self._setYLabel(self._axisChoiceY.GetSelection())
                self._setYName(self._axisChoiceY.GetString(self._axisChoiceY.GetSelection()))
                #wx.MessageBox(self.getYName(), 'Info', wx.OK | wx.ICON_INFORMATION)
                y1 = data.loc[1:,self._axisChoiceY.GetSelection()]
                y = y1.values.astype(np.float64)
                self.set_actual_y(y)
                self._set_original_y(y)
                x = self.getXOriginal()
                self._setHoriLower(0)
                self._setHoriUpper(x.size)
                self.set_cutplot_sliderlimits(x, y, x, y)
                # self.setArrayLimits(x, y)
                self.set_xslider_limits(x)
                self.replot_xy(x, y)
                
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

    def eSound (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            #wx.MessageBox('The software do not save the sound for the moment, the development team are working on that.',
            #              'Problem saving the sound:', wx.OK | wx.ICON_INFORMATION)
            
            eSoundPath = self.setpath("Save sound file", "Sound files |*.wav")
            x = self.getXActual()
            y = self.getYActual()
            try:
                #Cuando llegue a modificar aqui ver si agregando la linea comentada
                #reconoce instrumentos al salvar sonido.
                #self._datasound.reproductor.setInstrument(self._get_waveformnumber())
                norm_x, norm_y, status = self._matfunc.normalize(x, y)
                self._datasound.save_sound(eSoundPath, norm_x, norm_y)
            except AttributeError as e:
                self._expdata.writeinfo("The data has not been imported yet.")
                self._expdata.writeexception(e)
            except Exception as e:
                self._expdata.r(e)

    def savePlot(self):
        plotPath = self.setpath("Save plot file", "Image files |*.png")
        try:
            self._figure.savefig(plotPath)
        except Exception as e:
            self._expdata.writeexception(e)

    def play(self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            if self._timer_envelope.IsRunning():
                self._timer_envelope.Stop()
                self._set_timerenvelopeindex(0)
                self._envelopeplaytogglebtn.SetLabel('Play envelope\nsound')
                self._envelopeplaytogglebtn.SetValue(False)
            if not self._timer.IsRunning():
                # try:
                #     waveform = self._swaveformlistbox.GetString(self._swaveformlistbox.GetSelection())
                #     self._datasound.reproductor.set_waveform(waveform)
                # except Exception as e:
                #     self._expdata.writeexception(e)
                try:
                    x = self.getXActual()
                    y = self.getYActual()
                    # Store the previous x-y array to restore after 
                    # reproduction
                    self.prev_setted_time_x = x
                    self.prev_setted_time_y = y
                    norm_x, norm_y, status = self._matfunc.normalize(x, y)
                    self._expdata.printoutput("Normalize the input data.")
                    self._setNormXY(norm_x, norm_y)
                    
                    # Calculate the array with the space between each 
                    # data point
                    self._minspace_x_array = x[1:] - x[:x.size-1]
                    # Calculate the minimum space between data points
                    #self._minspace_x = np.nanmin(self._minspace_x_array)
                    self._minspace_x = np.nanmin(
                        np.where(
                            self._minspace_x_array == 0, 
                            np.nan, 
                            self._minspace_x_array
                            )
                        )
                    
                    
                    # Check if maximum time is setted
                    if self.playwithtime_status:
                        # First we set tempo at maximum
                        self.selecttempo_command(100)
                        # We check that 1500 sonifications loops take to the  
                        # software about one minute to sonify.
                        # First we calculate the number of sonification loops
                        # for this dataset.
                        min_x_inarray = np.nanmin(x)
                        max_x_inarray = np.nanmax(x)
                        total_number_of_loops = ((max_x_inarray - min_x_inarray) 
                                            / self._minspace_x)
                        # If the number of loop is higher than the time setted
                        # by the user promediate the closest values
                        setted_number_of_loops = (self.playwithtime_value
                            * self.number_1min_loops
                            )
                        if setted_number_of_loops < total_number_of_loops:
                            # new_x, new_y = self._matfunc.prom_closest_values(x, y)
                            
                            # Print message indicating the delay and asking if
                            # the user want to continue
                            
                            # Find the min distance between points according
                            # the max_time
                            actual_number_of_loops = total_number_of_loops
                            count = 0
                            new_minspace_x_array = self._minspace_x_array
                            while actual_number_of_loops > setted_number_of_loops:
                                # Create array to compare if all elements are
                                # the same as minspace
                                comp_array = np.zeros(new_minspace_x_array.size)
                                comp_array = comp_array + self._minspace_x
                                if new_minspace_x_array.all() == comp_array.all():
                                    # If all spaces are the same, we set new
                                    # min space based on setted number of loops
                                    self._minspace_x = (self._minspace_x
                                        * (actual_number_of_loops
                                           / setted_number_of_loops
                                           )
                                        )
                                    min_x_inarray = np.nanmin(x)
                                    max_x_inarray = np.nanmax(x)
                                    actual_number_of_loops = ((max_x_inarray - min_x_inarray) 
                                                / self._minspace_x)
                                    count = count + 1
                                else:
                                    # Delete the actual min space between point
                                    new_minspace_x_array = np.delete(
                                        arr = new_minspace_x_array,
                                        obj = np.where(
                                            new_minspace_x_array == self._minspace_x
                                            )
                                        )
                                    # Find the new min space between points
                                    self._minspace_x = np.nanmin(
                                        np.where(
                                            new_minspace_x_array == 0, 
                                            np.nan, 
                                            new_minspace_x_array
                                            )
                                        )
                                    min_x_inarray = np.nanmin(x)
                                    max_x_inarray = np.nanmax(x)
                                    actual_number_of_loops = ((max_x_inarray - min_x_inarray) 
                                                / self._minspace_x)
                                    count = count + 1
                                    # if count == 100:
                                    #     break
                            # We made it here, then we paste this lines on
                            # math function class
                            new_x = np.array([x[0]])
                            new_y = np.array([y[0]])
                            for i in range(1, x.size-1):
                                if (x[i]-x[i-1]) > self._minspace_x:
                                    new_x = np.append(new_x, x[i])
                                    new_y = np.append(new_y, y[i])
                                else:
                                    find_next = x[i-1] + self._minspace_x
                                    final_index_to_prom = (np.abs(x-find_next)).argmin()
                                    x_sum=0
                                    y_sum=0
                                    for j in range(i-1,final_index_to_prom):
                                        x_sum = x_sum + x[j]
                                        y_sum = y_sum + y[j]
                                    prom_x = x_sum/(final_index_to_prom-(i-1))
                                    prom_y = y_sum/(final_index_to_prom-(i-1))
                                    new_x = np.append(new_x, prom_x)
                                    new_y = np.append(new_y, prom_y)
                                    i = final_index_to_prom
                            self.set_actual_x(new_x)
                            self.set_actual_y(new_y)
                            self.replot_xy(self.getXActual(), self.getYActual())
                            norm_x, norm_y, status = self._matfunc.normalize(new_x, new_y)
                            self._expdata.printoutput("Normalize the input data.")
                            self._setNormXY(norm_x, norm_y)
                except AttributeError as e:
                    self._expdata.writeinfo("The data has not been imported yet.")
                    self._expdata.writeexception(e)
                except Exception as e:
                    self._expdata.writeexception(e)
                    
                #Seteo el tempo dependiendo del tiempo del timer
                self._timer.Start((self._getVelocity()*2) + 10)
                self._datasound.reproductor.set_time_base(self._timer.GetInterval()/1000.0)
            else:
                self._expdata.printoutput("The timer is alredy on when the user press Play button.")

    def _playenvelope(self):
        env = self.getenvelope()
        if env.size == 0:
            self._expdata.writeinfo("The data has not been sonified yet.")
            wx.MessageBox("Any data set was sonified, you need to import and sonify a dataset to enable this functionality.",
                              'Information', wx.OK | wx.ICON_INFORMATION)
            self._envelopeplaytogglebtn.SetLabel('Play envelope\nsound')
            self._envelopeplaytogglebtn.SetValue(False)
        else:
            if self._timer.IsRunning():
                self.stopMethod()
                wx.MessageBox("The previous reproduction of the data has been stopped to reproduce the envelope of the sound.",
                              'Information', wx.OK | wx.ICON_INFORMATION)
            if not self._timer_envelope.IsRunning():
                self._timer_envelope.Start(10)
                self._datasound.reproductor.set_time_base(self._timer_envelope.GetInterval()/1000.0)
            else:
                self._expdata.printoutput("The envelope sound is alredy on when the user press Play envelope.")

    def playMethod(self):
        if self.getXActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
            self._playButton.SetValue(False)
            self._playmenuitem.Check(False)
        else:
            if not self._timer.IsRunning():
                self._expdata.printoutput("Play button is pressed.")
                self._playButton.SetLabel("Pause")
                self._playButton.SetValue(True)
                self._playmenuitem.SetItemLabel('Pause' + '\t' + 'Alt+Shift+P')
                self._playmenuitem.Check(True)
                self.play()
            elif self._timer.IsRunning():
                self._expdata.printoutput("Pause button is pressed.")
                self._playButton.SetLabel("Play")
                self._playButton.SetValue(False)
                self._playmenuitem.SetItemLabel('Play' + '\t' + 'Alt+Shift+P')
                self._playmenuitem.Check(False)
                #self._datasound.make_sound(0, -1)
                self._timer.Stop()
            else:
                self._expdata.writeinfo("Error con el contador del botón Play-Pausa")
    
    def playinloop(self):
        self.playinloop_state = True
        self.playwithtime_status = False
        self.playMethod()
        
    def playonce(self):
        self.playinloop_state = False
        self.playwithtime_status = False
        self.playMethod()
    
    def play_with_time(self, time):
        
        """
        This method set the flag to allow to set maximun time for data 
        sonification.
        """
        self.playwithtime_status = True
        self.playinloop_state = False
        self.playwithtime_value = float(time)
        self.playMethod()
        
    def play_with_time_inloop(self, time):
        
        """
        This method set the flag to allow to set maximun time for data 
        sonification and play in loop.
        """
        self.playwithtime_status = True
        self.playinloop_state = True
        self.playwithtime_value = float(time)
        self.playMethod()

    def set_number_1min_loops(self, num):
        
        """
        This method set the number of loops to take into account as the 
        number of loops that take 1 minute of sonification.
        """
        self.number_1min_loops = int(num)

    def stopMethod(self):
        self._playButton.SetValue(False)
        self._playmenuitem.Check(False)
        self._playButton.SetLabel("Play")
        self._playmenuitem.SetItemLabel('Play' + '\t' + 'Alt+Shift+P')
        
        # After reproduction the non reduce array x-y was setted
        self.set_actual_x(self.prev_setted_time_x)
        self.set_actual_y(self.prev_setted_time_y)

        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            if self._timer.IsRunning():
                #self._datasound.make_sound(0, -1)
                self._timer.Stop()
            self._timerindex_space = 0
            self._set_timerindex(0)
            self._abspos_slider.SetValue(0)
            self._absposlabel_textctrl.SetValue(str(round(self.getXActual()[self._abspos_slider.GetValue()],4)))
            self.replot_xy(self.getXActual(), self.getYActual())

    def markPoints (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            #Se eliminarán los datos cada vez que se guardan o que se ingresa un archivo de datos nuevo.
            x = self.getXActual()
            y = self.getYActual()
            xp = self._get_markedpoints_xcoord()
            yp = self._get_markedpoints_ycoord()
            
            if (self._getTimerIndex()==x.size) or (self._getTimerIndex()==0):
                self._expdata.writeinfo("The position of the cursor is at the beginning or end of the array.")
                return 0
            
            try:
                index = self._getTimerIndex() - 1
                xp = np.append(xp, x[index])
                yp = np.append(yp, y[index])
                self._set_markedpoints_xcoord(xp)
                self._set_markedpoints_ycoord(yp)
            except Exception as e:
                self._expdata.writeexception(e)
            self._ask_markpoints = False
            #para graficar una línea
            try:
                abs_markpoint = np.array([float(x[index]), float(x[index])])
                ord_markpoint = np.array([float(np.nanmin(y)), float(np.nanmax(y))])
            except AttributeError as e:
                self._expdata.writeinfo("The data has not been imported yet.")
                self._expdata.writeexception(e)
            except Exception as e:
                self._expdata.writeexception(e)
            self.plot_markline(abs_markpoint, ord_markpoint)

    def deleteLastMark (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            try:
                xp = self._get_markedpoints_xcoord()
                yp = self._get_markedpoints_ycoord()
                xp = xp[:-1].copy()
                yp = yp[:-1].copy()
                self._set_markedpoints_xcoord(xp)
                self._set_markedpoints_ycoord(yp)
                self.replot_xy(self.getXActual(),self.getYActual())
            except Exception as e:
                self._expdata.writeexception(e)

    def deleteAllMark (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            xp = self._get_markedpoints_xcoord()
            yp = self._get_markedpoints_ycoord()
            try:
                index = [i for i in range(0, len(xp))]
            except Exception as e:
                self._expdata.writeexception(e)
            try:
                self._set_markedpoints_xcoord(np.delete(xp,index))
                self._set_markedpoints_ycoord(np.delete(yp,index))
            except Exception as e:
                self._expdata.writeexception(e)
            try:
                self.replot_xy(self.getXActual(), self.getYActual())
            except Exception as e:
                self._expdata.writeexception(e)

    def saveData (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            x = self.getXActual()
            y = self.getYActual()
            try:
                path = self.setpath('Save data file', 'Data files |*.csv')
                self._expdata.writepointfile(x, y, path)
            except Exception as e:
                self._expdata.writeexception(e)

    def saveMarks (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            xp = self._get_markedpoints_xcoord()
            yp = self._get_markedpoints_ycoord()
            try:
                path = self.setpath('Save data file', 'Data files |*.csv')
                self._expdata.writepointfile(xp, yp, path)
            except AttributeError as e:
                self._expdata.writeinfo("The array with numbers of interest has not been created yet.")
                self._expdata.writeexception(e)
            except Exception as e:
                self._expdata.writeexception(e)
            index = [i for i in range(0, len(xp))]
            self._set_markedpoints_xcoord(np.delete(xp,index))
            self._set_markedpoints_ycoord(np.delete(yp,index))
            self.replot_xy(self.getXActual(), self.getYActual())

    def absPosSetting (self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        elif np.isnan(self.getXActual()[self._abspos_slider.GetValue()]) or np.isnan(self.getYActual()[self._abspos_slider.GetValue()]):
            self._expdata.writeinfo("This point is a nan value, for that the red line is not updated.")
        else:
            #Set the red line to mark de points in the graph
            x = self.getXActual()
            y = self.getYActual()
            ordenada = np.array([float(np.nanmin(y)), float(np.nanmax(y))])
            abscisa = np.array([float(x[self._abspos_slider.GetValue()]), float(x[self._abspos_slider.GetValue()])])
            self.plot_positionline(abscisa, ordenada)
            # Update the space cycle timer
            self._timerindex_space = 0

    def tempo(self):
        if self._timer.IsRunning():
            self._timer.Stop()
            self._timer.Start((self._getVelocity()*2) + 10)
            self._datasound.reproductor.sound.stop()
            self._datasound.reproductor.set_time_base(self._timer.GetInterval()/1000.0)

#    def cutVertical(self):
#        self.askSavePoints()
#        #Se debe realizar todo el mapeo para que reproduzca tick marks en los valores que exeden el límite y que se remapee el resto que si está en los límites.
#        try:
#            self.limitVLower = float(self._lVLimitSlider.GetValue())
#        except Exception as e:
#            self._expdata.writeexception(e)
#        try:
#            self.limitVUpper = float(self._uVLimitSlider.GetValue())
#        except Exception as e:
#            self._expdata.writeexception(e)

    def cutHorizontal (self):
        if self.getXOriginal().any()==None or self.getYOriginal().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            if not self._ask_markpoints:
                self.askSavePoints()
            try:
                lower = (self._lHLimitSlider.GetValue())
                self._setHoriLower(lower)
            except Exception as e:
                self._expdata.writeexception(e)
            try:
                upper = (self._uHLimitSlider.GetValue())
                self._setHoriUpper(upper)
            except Exception as e:
                self._expdata.writeexception(e)
            xo = self.getXOriginal()
            yo = self.getYOriginal()
            try:
                x = xo[lower:(upper+1)]
                y = yo[lower:(upper+1)]
                self.set_actual_x(x)
                self.set_actual_y(y)
            except AttributeError as e:
                self._expdata.writeinfo("The data has not been imported yet.")
                self._expdata.writeexception(e)
            except Exception as e:
                self._expdata.writeexception(e)
            try:
                self.set_cutplot_sliderlimits(xo, yo, x, y)
                # self.setArrayLimits(x, y)
                self.set_xslider_limits(x)
                self.replot_xy(x, y)
            except AttributeError as e:
                self._expdata.writeinfo("The data has not been imported yet.")
                self._expdata.writeexception(e)
            except Exception as e:
                self._expdata.writeexception(e)

    #Maybe we add soundfont in the future
    """def _soundFontChoice(self):
        if self._sFontLabel == 'gm':
            self._expdata.printoutput("The choice of sound font is general midi, that's the default sound font.")
            if platform.system() == 'Windows':
                self._sFontChoice = "soundModule\soundFont\FluidR3_GM.sf2"
            else:
                if platform.system() == 'Linux':
                    self._sFontChoice = "soundModule/soundFont/FluidR3_GM.sf2"
                else:
                    if platform.system() == 'Darwin':
                        self._sFontChoice = "soundModule/soundFont/FluidR3_GM.sf2"
                    else:
                        self._expdata.writeinfo("The operative system is unknown, the software can't open the sound font.")
        elif self._sFontLabel == 'other':
            self._expdata.printoutput("The choice of sound font is look on the operative system.")
            self._sFontChoice = self._opendata.getSFPath()
        else:
            self._expdata.printoutput("Error!: the sound font chosen is not correct!.")
            self._expdata.writeinfo("Error in 'soundFontChoice', on core.py!: the sound
            font chosen is not correct!.")"""

    def swaveformlistboxchoice(self):
        waveform = self._swaveformlistbox.GetString(self._swaveformlistbox.GetSelection())
        self._datasound.reproductor.set_waveform(waveform)
        # return waveform

    def matFcSelection(self):
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Last limits cut":
            self._avNPointsspinCtrl.Enable(False)
            self._expdata.printoutput("Last limits cut function is selected.")
            self._set_mathfunction("Last limits cut")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Original":
            self._avNPointsspinCtrl.Enable(False)
            self._expdata.printoutput("Original function is selected.")
            self._set_mathfunction("Original")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Inverse":
            self._avNPointsspinCtrl.Enable(False)
            self._expdata.printoutput("Inverse function is selected.")
            self._set_mathfunction("Inverse")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Play Backward":
            self._avNPointsspinCtrl.Enable(False)
            self._expdata.printoutput("Play Backward function is selected.")
            self._set_mathfunction("Play Backward")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Square":
            self._avNPointsspinCtrl.Enable(False)
            self._expdata.printoutput("Square function is selected.")
            self._set_mathfunction("Square")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Square root":
            self._avNPointsspinCtrl.Enable(False)
            self._expdata.printoutput("Square root function is selected.")
            self._set_mathfunction("Square root")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Logarithm":
            self._avNPointsspinCtrl.Enable(False)
            self._expdata.printoutput("Logarithm function is selected.")
            self._set_mathfunction("Logarithm")
        if self._matFcListBox.GetString(self._matFcListBox.GetSelection()) == "Average":
            self._avNPointsspinCtrl.SetValue(1)
            self._avNPointsspinCtrl.Enable(True)
            self._expdata.printoutput("Average function is selected.")
            self._set_mathfunction("Average")
        self.matFcExecutor()

    def matFcExecutor(self):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            if not self._ask_markpoints:
                self.askSavePoints()
            xo = self.getXOriginal()
            yo = self.getYOriginal()
#            xo, yo = self._matfunc.mfOriginal(self.getXOriginal(), self.getYOriginal())
            x = self.getXActual()
            y = self.getYActual()
#            x, y = self._matfunc.mfOriginal(self.getXActual(), self.getYActual())
            if self._getMatSelection() == "Last limits cut":
                self._lHLimitSlider.Enable(True)
                self._uHLimitSlider.Enable(True)
                x = xo[self._getHoriLower():(self._getHoriUpper()+1)]
                y = yo[self._getHoriLower():(self._getHoriUpper()+1)]
                self._expdata.printoutput("Last limits cut function is executed.")
                self._inversefunc = False
            if self._getMatSelection() == "Original":
                self._lHLimitSlider.Enable(True)
                self._uHLimitSlider.Enable(True)
                x = self.getXOriginal()
                y = self.getYOriginal()
#                x, y = self._matfunc.mfOriginal(self.getXOriginal(), self.getYOriginal())
                self._expdata.printoutput("Original function is executed.")
                self._inversefunc = False
            if self._getMatSelection() == "Inverse":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                #x, y = self._matfunc.mfInverse(self.getXOriginal(), self.getYOriginal())
                self._inversefunc = True
                self._expdata.printoutput("Inverse function is executed.")
            if self._getMatSelection() == "Play Backward":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                x, y = self._matfunc.mfPlayBack(self.getXOriginal(), self.getYOriginal())
                self._expdata.printoutput("Play Backward function is executed.")
                self._inversefunc = False
            if self._getMatSelection() == "Square":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                x, y, status = self._matfunc.square(self.getXOriginal(), self.getYOriginal())
                self._expdata.printoutput("Square function is executed.")
                self._inversefunc = False
            if self._getMatSelection() == "Square root":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                x, y, status = self._matfunc.squareroot(self.getXOriginal(), self.getYOriginal())
                self._expdata.printoutput("Square root function is executed.")
                self._inversefunc = False
            if self._getMatSelection() == "Logarithm":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                x, y, status = self._matfunc.logarithm(self.getXOriginal(), self.getYOriginal())
                self._expdata.printoutput("Logarithm function is executed.")
                self._inversefunc = False
            if self._getMatSelection() == "Average":
                self._lHLimitSlider.Enable(False)
                self._uHLimitSlider.Enable(False)
                x, y, status = self._matfunc.average(self.getXOriginal(), self.getYOriginal(), self._getavNPoints())
                self._expdata.printoutput("Average function is executed.")
                self._inversefunc = False
            try:
                self.set_actual_x(x)
                self.set_actual_y(y)
            except AttributeError as e:
                self._expdata.writeinfo("The data has not been imported yet.")
                self._expdata.writeexception(e)
            except Exception as e:
                self._expdata.writeexception(e)
            try:
                self.set_cutplot_sliderlimits(xo, yo, x, y)
                # self.setArrayLimits(x, y)
                self.set_xslider_limits(x)
                self.replot_xy(x, y)
            except AttributeError as e:
                self._expdata.writeinfo("The data has not been imported yet.")
                self._expdata.writeexception(e)
            except Exception as e:
                self._expdata.writeexception(e)

    def averageSelect(self):
        if self.getXActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            #seteo los límites de average
            x = self.getXActual()
            if x.any() == None:
                self._avNPointsspinCtrl.SetMax(x.size-1)
                self._avNPointsspinCtrl.SetMin(1)
                self._avNPointsspinCtrl.SetValue(2)
                self._set_average_numpoints(2)
                self._avNPointsspinCtrl.Enable(True)
                self._set_mathfunction("Average")
                self.matFcExecutor()

    def lineStyleConfig(self, index):
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            if index == 0:
                self._set_linechar('')
                if self._getMarkerStyleIndex()<1 or self._getMarkerStyleIndex()>21:
                    self._set_markerstyle_index(0)
                self.markerStyleConfig()
                self._expdata.printoutput("Discreet line was selected.")
            elif index == 1:
                self._set_linechar('-')
                self._set_markerchar('')
                self._set_markerstyle_index(22)
                self.replot_xy(self.getXActual(), self.getYActual())
                self.SendSizeEvent()
                self._expdata.printoutput("Solid line was selected.")
            elif index == 2:
                self._set_linechar('--')
                self._set_markerchar('')
                self._set_markerstyle_index(22)
                self.replot_xy(self.getXActual(), self.getYActual())
                self.SendSizeEvent()
                self._expdata.printoutput("Dashed line was selected.")
            elif index == 3:
                self._set_linechar('-.')
                self._set_markerchar('')
                self._set_markerstyle_index(22)
                self.replot_xy(self.getXActual(), self.getYActual())
                self.SendSizeEvent()
                self._expdata.printoutput("Dash-dot line was selected.")
            elif index == 4:
                self._set_linechar(':')
                self._set_markerchar('')
                self._set_markerstyle_index(22)
                self.replot_xy(self.getXActual(), self.getYActual())
                self.SendSizeEvent()
                self._expdata.printoutput("Dotted line was selected.")
            else:
                self._set_linechar('-')
                self._set_markerchar('')
                self._set_markerstyle_index(22)
                self.replot_xy(self.getXActual(), self.getYActual())
                self.SendSizeEvent()
                self._expdata.printoutput("The line style was unknow, solid line was selected by default.")

    def markerStyleConfig(self):
        if self._getMarkerStyleIndex() == 0:
            self._set_markerchar('.')
            self._expdata.printoutput("Point marker line was selected.")
        elif self._getMarkerStyleIndex() == 1:
            self._set_markerchar(',')
            self._expdata.printoutput("Pixel marker line was selected.")
        elif self._getMarkerStyleIndex() == 2:
            self._set_markerchar('o')
            self._expdata.printoutput("Circle marker line was selected.")
        elif self._getMarkerStyleIndex() == 3:
            self._set_markerchar('v')
            self._expdata.printoutput("Triangle down marker line was selected.")
        elif self._getMarkerStyleIndex() == 4:
            self._set_markerchar('^')
            self._expdata.printoutput("Triangle up marker line was selected.")
        elif self._getMarkerStyleIndex() == 5:
            self._set_markerchar('<')
            self._expdata.printoutput("Triangle left marker line was selected.")
        elif self._getMarkerStyleIndex() == 6:
            self._set_markerchar('>')
            self._expdata.printoutput("Triangle right marker line was selected.")
        elif self._getMarkerStyleIndex() == 7:
            self._set_markerchar('1')
            self._expdata.printoutput("Tri-down marker line was selected.")
        elif self._getMarkerStyleIndex() == 8:
            self._set_markerchar('2')
            self._expdata.printoutput("Tri-up marker line was selected.")
        elif self._getMarkerStyleIndex() == 9:
            self._set_markerchar('3')
            self._expdata.printoutput("Tri-left marker line was selected.")
        elif self._getMarkerStyleIndex() == 10:
            self._set_markerchar('4')
            self._expdata.printoutput("Tri-right marker line was selected.")
        elif self._getMarkerStyleIndex() == 11:
            self._set_markerchar('s')
            self._expdata.printoutput("Square marker line was selected.")
        elif self._getMarkerStyleIndex() == 12:
            self._set_markerchar('p')
            self._expdata.printoutput("Pentagon marker line was selected.")
        elif self._getMarkerStyleIndex() == 13:
            self._set_markerchar('*')
            self._expdata.printoutput("Star marker line was selected.")
        elif self._getMarkerStyleIndex() == 14:
            self._set_markerchar('h')
            self._expdata.printoutput("Hexagon (1) marker line was selected.")
        elif self._getMarkerStyleIndex() == 15:
            self._set_markerchar('H')
            self._expdata.printoutput("Hexagon (2) marker line was selected.")
        elif self._getMarkerStyleIndex() == 16:
            self._set_markerchar('+')
            self._expdata.printoutput("Plus marker line was selected.")
        elif self._getMarkerStyleIndex() == 17:
            self._set_markerchar('x')
            self._expdata.printoutput("X marker line was selected.")
        elif self._getMarkerStyleIndex() == 18:
            self._set_markerchar('D')
            self._expdata.printoutput("Diamond marker line was selected.")
        elif self._getMarkerStyleIndex() == 19:
            self._set_markerchar('d')
            self._expdata.printoutput("Thin diamond marker line was selected.")
        elif self._getMarkerStyleIndex() == 20:
            self._set_markerchar('|')
            self._expdata.printoutput("Vertical line marker of the line was selected.")
        elif self._getMarkerStyleIndex() == 21:
            self._set_markerchar('_')
            self._expdata.printoutput("Horizontal line marker of the line was selected.")
        elif self._getMarkerStyleIndex() == 22:
            self._set_markerchar('')
            self._expdata.printoutput("Any marker line was selected.")
        else:
            self._set_markerchar('')
            self._expdata.printoutput("The line marker style was unknow, any marker line was selected by default.")
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            self.replot_xy(self.getXActual(), self.getYActual())
            self.SendSizeEvent()

    def colorStyleConfig(self, index):
        if index == 0:
            self._set_colorchar('b')
            self._expdata.printoutput("Blue line color was selected.")
        elif index == 1:
            self._set_colorchar('g')
            self._expdata.printoutput("Green line color was selected.")
        elif index == 2:
            self._set_colorchar('r')
            self._expdata.printoutput("Red line color was selected.")
        elif index == 3:
            self._set_colorchar('c')
            self._expdata.printoutput("Cyan line color was selected.")
        elif index == 4:
            self._set_colorchar('m')
            self._expdata.printoutput("Magenta line color was selected.")
        elif index == 5:
            self._set_colorchar('y')
            self._expdata.printoutput("Yellow line color was selected.")
        elif index == 6:
            self._set_colorchar('k')
            self._expdata.printoutput("Black line color was selected.")
        else:
            self._set_colorchar('b')
            self._expdata.printoutput("The line color style was unknow, blue line color was selected by default.")
        if self.getXActual().any()==None or self.getYActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            self.replot_xy(self.getXActual(), self.getYActual())
            self.SendSizeEvent()

    def askSavePoints(self):
        self._ask_markpoints = True
        if self._timer.IsRunning():
            self.stopMethod()
        xp = self._get_markedpoints_xcoord()
        yp = self._get_markedpoints_ycoord()
        if not xp.size==0:
            if wx.MessageBox("Brands have been made on the data. Do you want to save them?.", "Please confirm",
                         wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                index = [i for i in range(0, len(xp))]
                self._set_markedpoints_xcoord(np.delete(xp,index))
                self._set_markedpoints_ycoord(np.delete(yp,index))
            else:
                self.saveMarks()

    def detectcommand(self):
        # yy
        text_original = self._writecommandtextctrl.GetLineText(0)
        #text_original = text_original.replace(' ','')
        cut = text_original.find('(')
        cut2 = text_original.rfind(')')
        if cut!=(-1):
            text = text_original[:cut]
        else:
            text_original = text_original.replace(' ','')
            text = text_original
        #Se chequea a que diccionario corresponde y se ejecuta el comando
        if text in self.command_dict_withoutparam:
            self.command_dict_withoutparam[text]()
        elif text in self.command_dict_withparam:
            if cut==(-1) or cut2==(-1):
                msg = ('You must enter the value between parentheses. '
                    +'Your command was: \n'+text_original)
                wx.MessageBox(
                    msg,
                    'Command error',
                    wx.OK | wx.ICON_INFORMATION
                    )
            else:
                value = text_original[cut+1:cut2]
                self.command_dict_withparam[text](value)
        else:
            msg = ('The command inserted do not match with the list of '
                + 'functionalities. The text inserted was: \n' + text)
            wx.MessageBox(msg,
                          'Command not found', wx.OK | wx.ICON_INFORMATION)
        self._writecommandtextctrl.Clear()

    def xposition_command(self, value):
        try:
            try:
                x_value = float(value)
            except Exception as e:
                wx.MessageBox(
                    'The typed number contains some caracter that do not match with a number.',
                    'Number Error',
                    wx.OK | wx.ICON_INFORMATION
                    )
                self.set_xslider_limits(self.getXActual())
                self._expdata.writeexception(e)
            x_array = self.getXActual()
            abs_val_array = np.abs(x_array - x_value)
            x_pos = abs_val_array.argmin()
            if x_value<np.nanmin(self.getXActual()) or x_value>np.nanmax(self.getXActual()):
                wx.MessageBox(
                    'The number indicated was out of the array bounds.',
                    'Out of bounds',
                    wx.OK | wx.ICON_INFORMATION
                    )
            else:
                self._abspos_slider.SetValue(x_pos)
                self._absposlabel_textctrl.SetValue(str(round(x_array[self._abspos_slider.GetValue()],4)))
                self._set_timerindex(x_pos)
                self.absPosSetting()
        except Exception as e:
            self._expdata.writeexception(e)

    def selecttempo_command(self, value):
        t = int(value)
        self._tempoposlabel_textctrl.SetValue(str(value))
        self._soundVelSlider.SetValue(t)
        self._set_velocity(t)
        self.tempo()

    def xlowerlimit_command(self, value):
        try:
            x_value = float(value)
            x_array = self.getXOriginal()
            abs_val_array = np.abs(x_array - x_value)
            if x_value<np.nanmin(self.getXOriginal()) or x_value>np.nanmax(self.getXOriginal()):
                wx.MessageBox(
                    'The number indicated was out of the array bounds.',
                    'Out of bounds',
                    wx.OK | wx.ICON_INFORMATION
                    )
            else:
                x_pos = abs_val_array.argmin()
                self._lHLimitSlider.SetValue(x_pos)
                self.cutHorizontal()
        except Exception as e:
            self._expdata.writeexception(e)

    def xupperlimit_command(self, value):
        try:
            x_value = float(value)
            x_array = self.getXOriginal()
            abs_val_array = np.abs(x_array - x_value)
            if x_value<np.nanmin(self.getXOriginal()) or x_value>np.nanmax(self.getXOriginal()):
                wx.MessageBox(
                    'The number indicated was out of the array bounds.',
                    'Out of bounds',
                    wx.OK | wx.ICON_INFORMATION
                    )
            else:
                x_pos = abs_val_array.argmin()
                self._uHLimitSlider.SetValue(x_pos)
                self.cutHorizontal()
        except Exception as e:
            self._expdata.writeexception(e)

    def originaldata_command(self):
        self._avNPointsspinCtrl.Enable(False)
        self._set_mathfunction("Original")
        self.matFcExecutor()

    def xlastcut_command(self):
        self._avNPointsspinCtrl.Enable(False)
        self._set_mathfunction("Last limits cut")
        self.matFcExecutor()

    def inverse_command(self):
        self._avNPointsspinCtrl.Enable(False)
        self._set_mathfunction("Inverse")
        self.matFcExecutor()

    def square_command(self):
        self._avNPointsspinCtrl.Enable(False)
        self._set_mathfunction("Square")
        self.matFcExecutor()

    def squareroot_command(self):
        self._avNPointsspinCtrl.Enable(False)
        self._set_mathfunction("Square root")
        self.matFcExecutor()

    def logarithm_command(self):
        self._avNPointsspinCtrl.Enable(False)
        self._set_mathfunction("Logarithm")
        self.matFcExecutor()

#Métodos para vincular con octave

    def _savePythonConsole(self):
        text = self._pythonShell.GetText()
        self._expdata.printoutput("Python console text: \n" + text)
        self._pythonShell.Execute("self._pythonShell.clear()")

    def _analizeOctaveOutput(self, show):
        text = self._pythonShell.GetText()
        self._expdata.printoutput("Python console text: \n" + text)

        indexError = text.find("Traceback")
        if not indexError == -1:
            text1 = text[indexError:-5]
            text2 = text1.rstrip('\n')
            wx.MessageBox(text2,
                          'Error from octave', wx.OK | wx.ICON_INFORMATION)
        else:
            if show:
                index1 = text.find(">>>")
                text3 = text[index1:]
                
                index_command = text.find('"')
                text_command = text3[index_command+1:]
                index_command = text_command.find('"')
                text_command = text_command[:index_command]
                self._octaveOutputTextCtrl.write('>>> '+text_command+'\n')
                
                index2 = text3.find("\n")
                text4 = text3[index2:]
                index3 = text4.find('>')
                text5 = text4[:index3-1]
                
                self._octaveOutputTextCtrl.write(text5+'\n')

        self._pythonShell.Execute("self._pythonShell.clear()")

    def _sendAllToOctave(self):
        if self.get_dataframe() is not None:
            self._expdata.printoutput("Sending imported data to octave.")
            try:

                #if data.shape[0] < rowNumber:
                data = self.get_dataframe()

                for i in range (0, data.shape[1]):
                    #text = "octave.push('" + data.iloc[0,i] + "', data.iloc[1:,i])"
                    #wx.MessageBox(text, " ", wx.OK | wx.ICON_INFORMATION)

                    self.dataToOctave, status = self.pandasToNumpy(data.iloc[1:,i])
                    if status:
                        col_name_status = re.search('[^a-zA-Z0-9 \n\.]', data.iloc[0,i])
                        if not col_name_status==None:
                            col_name = re.sub('[^a-zA-Z0-9 \n\.]', '', data.iloc[0,i])
                            msg = (
                                'The name of the octave variable for column number '
                                + str(i+1)
                                + ' was changed to:\n'
                                + col_name
                                )
                            wx.MessageBox(msg,
                              'Variable name', wx.OK | wx.ICON_INFORMATION)
                        else:
                            col_name = data.iloc[0,i]
                        #self._pythonShell.Execute("octave.push('x', self.getXActual())")
                        self._pythonShell.Execute("octave.push('" + col_name + "', self.dataToOctave)")
                        self._analizeOctaveOutput(False)
                    else:
                        wx.MessageBox("Problems sending data to octave.", " ", wx.OK | wx.ICON_INFORMATION)

#                self._pythonShell.Execute("octave.push('x', self.getXActual())")
#                self._analizeOctaveOutput()
#                self._pythonShell.Execute("octave.push('y', self.getYActual())")
#                self._analizeOctaveOutput()
#                self._pythonShell.Execute("octave.push('xoriginal', self.getXOriginal())")
#                self._analizeOctaveOutput()
#                self._pythonShell.Execute("octave.push('yoriginal', self.getYOriginal())")
#                self._analizeOctaveOutput()
            except Exception as e:
                    self._expdata.writeexception(e)

    def _sendToOctave(self):
        self._expdata.printoutput("Sending data to octave.")
        try:
            self._pythonShell.Execute("octave.push('x', self.getXActual())")
            self._analizeOctaveOutput(False)
            self._pythonShell.Execute("octave.push('y', self.getYActual())")
            self._analizeOctaveOutput(False)
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
                self._expdata.writeexception(e)

    def _octaveInput(self):
        if self._datasenttooctave:
            try:
                self._sendToOctave()
            except Exception as e:
                self._expdata.writeexception(e)
        self._expdata.printoutput("Sending commands to octave.")
        text = self._octaveInputTextCtrl.GetLineText(0)
        self._octaveInputTextCtrl.Clear()
        self._pythonShell.Execute('octave.eval("'+text+'", nout=1)')
        self._analizeOctaveOutput(True)

    def _octaveInput_command(self, value):
        if self._datasenttooctave:
            try:
                self._sendToOctave()
            except Exception as e:
                self._expdata.writeexception(e)
        self._expdata.printoutput("Sending commands to octave.")
        self._pythonShell.Execute('octave.eval("'+value+'", nout=1)')
        self._analizeOctaveOutput(True)

    def _xFromOctave(self, x):
        self._expdata.printoutput("Receiving x from octave.")
        self._pythonShell.Execute("self.xOctave = octave.pull('"+x+"')")
        self._analizeOctaveOutput(True)
        self.xOctave = self.xOctave[0]

    def _yFromOctave(self, y):
        self._expdata.printoutput("Receiving y from octave.")
        self._pythonShell.Execute("self.yOctave = octave.pull('"+y+"')")
        self._analizeOctaveOutput(True)
        self.yOctave = self.yOctave[0]

    def _octaveReplot(self):

        self._leftpanel.Hide()
        self._rightpanel.Hide()
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
            self._expdata.writeinfo("The two arrays from Octave has not been retrieved.")
            wx.MessageBox("The two arrays from Octave has not been retrieved. You must to complete the 'Name of x array' text box and the 'Name of y array' text box, located before the 'Refresh Plot' button.",
                          'Information', wx.OK | wx.ICON_INFORMATION)
        else:
            self._setXName(self._xFromOctaveTextCtrl.GetLineText(0))
            self._setYName(self._yFromOctaveTextCtrl.GetLineText(0))

            self.replot_xy(x, y)
            self.set_actual_x(x)
            self.set_actual_y(y)

        self._xFromOctaveTextCtrl.Clear()
        self._yFromOctaveTextCtrl.Clear()
#        self._leftpanel.Show()
#        self._rightpanel.Show()
#        self.retrieveFromOctavePanel.Hide()
        self._absPosTextCtrl.SetFocus()

    def _retrieveFromOctave_command(self, value):

        cut = value.find(',')
        value1 = value[:cut]
        value2 = value[cut+1:]

        if not value1 == "":
            self._xFromOctave(value1)
        else:
            self.xOctave = np.array(None)
        if not value2 == "":
            self._yFromOctave(value2)
        else:
            self.yOctave = np.array(None)

        x = self.getXOctave()
        y = self.getYOctave()

        if x.any()==None or y.any()==None:
            self._expdata.writeinfo("The two arrays from Octave has not been retrieved.")
            wx.MessageBox("The two arrays from Octave has not been retrieved. You must to complete the 'Name of x array' text box and the 'Name of y array' text box, located before the 'Refresh Plot' button.",
                          'Information', wx.OK | wx.ICON_INFORMATION)
        else:
            self._setXName(value1)
            self._setYName(value2)

            self.replot_xy(x, y)
            self.set_actual_x(x)
            self.set_actual_y(y)

        self._absPosTextCtrl.SetFocus()
        
    # def get_m_filepath(self):
        
    #     """
    #     This method return the path to one m file selected by the user.
        
    #     Check if the string is None (the user change their mind) or 'Error'
    #     (the method through an error.).
    #     """
    #     try:
    #         with wx.FileDialog(
    #                 parent = None, 
    #                 message = 'Open M file', 
    #                 wildcard = 'Data files |*.m', 
    #                 style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    #                 ) as filedialog:
    #             if filedialog.ShowModal() == wx.ID_CANCEL:
    #                 return None
    #             else:
    #                 path = filedialog.GetPath()
    #                 filename = filedialog.GetFilename()
    #                 return path, filename
    #     except Exception as Error:
    #         self._expdata.writeexception(Error)
    #         return 'Error'
    
    # def get_m_dirpath(self):
        
    #     """
    #     This method return the path to the directory that the user select.
        
    #     Check if the string is empty (the user change his mind and is the
    #     first time that the software open a directory of m files) or 'Error'
    #     (the method through an error.).
    #     """
    #     try:
    #         with wx.DirDialog(
    #                 parent = None, 
    #                 message = 'Choose m files folder.', 
    #                 defaultPath = '', 
    #                 style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
    #                 ) as dirdialog:
    #             if dirdialog.ShowModal() == wx.ID_CANCEL:
    #                 return self._prev_m_filepath
    #             else:
    #                 path = dirdialog.GetPath()
    #                 self._prev_m_filepath = path
    #                 return path
    #     except Exception as Error:
    #         self._expdata.writeexception(Error)
    #         return 'Error'

    # def addPathToOctave(self):
    #     path = self._opendata.get_m_dirpath()
    #     self._pythonShell.Execute('octave.addpath("'+path+'")')

    # def octave_loadmfunc_command(self):
    #     path, self.octavefuncfilename = self.get_m_filepath()
    #     path='C:/Users/johi-/Desktop'
    #     self._pythonShell.Execute('octave.addpath("'+path+'")')
    #     #self._pythonShell.Execute('out = octave.'+filename[:-2]+'()')
    #     self._analizeOctaveOutput()
        
    # def octave_mfunc_command(self, value):
    #     self._pythonShell.Execute('out = octave.'+value+')')
    #     self._analizeOctaveOutput()
        
    # def octave_mfile_command(self):
    #     path, filename = self.get_m_filepath()
    #     #path='C:/Users/johi-/Desktop'
    #     try:
    #         with open(path, "r") as f:
    #             list_lines = f.readlines()
    #             for line in list_lines:
    #                 cut = line.find("%")
    #                 self._pythonShell.Execute('octave.eval("'+line[:cut]+'", nout=1)')
    #                 self._analizeOctaveOutput()
                    
    #     except Exception as e:
    #         self._expdata.writeexception(e)
    #         wx.MessageBox("An error occurred while trying to run the M file in Octave.",
    #                       'Information', wx.OK | wx.ICON_INFORMATION)

    def _setspecialsoundconfig(self):
        self._datasound.reproductor.set_adsr(
            self._get_soundattack(),
            self._get_sounddecay(),
            self._get_soundsustain(),
            self._get_soundrelease()
            )

    def _check_adr(self):
        a = self._soundattackslider.GetValue()/100
        d = self._sounddecayslider.GetValue()/100
        r = self._soundreleaseslider.GetValue()/100
        if a+d+r>1:
            return False
        else:
            return True

    def plotsoundenvelope(self):
        self._axesenvelopegraph.cla()
        #self._envelopefigure.canvas.draw()
        env = self._datasound.reproductor.get_envelope()
        n_samples = np.arange(0.0, env.size)
        self.setenvelope(env)
        self._axesenvelopegraph.plot(n_samples, env)
        self._envelopefigure.tight_layout()
        self._envelopefigure.canvas.draw()

#Displays configs!!!
    #Muestra o esconde el panel de la grilla con los botones correspondientes.
    def displayGridChoice(self):
        if self._gridChoice.IsChecked():
            self._plotGridPanel.Show()
            self.panel.grid(color=self._getGridColor(), linestyle=self._getGridLinestyle(), linewidth=self._getGridLinewidth())
            self._figure.tight_layout()
            self._figure.canvas.draw()
            self._splotgridoptionmenuitem.Check(True)
        else:
            self._plotGridPanel.Hide()
            self.panel.grid(False)
            self._splotgridoptionmenuitem.Check(False)
        self.SendSizeEvent()
    #Muestra o esconde el panel File con los botones correspondientes.
    def displayGFile(self):
        if self._filepanel.IsShown():
            self._filepanel.Hide()
            # self._fileToggleBtn.SetLabel("Show File")
            # self._fileToggleBtn.SetValue(False)
            self._cpfilemenuitem.Check(False)
            self.SendSizeEvent()
        else:
            self._filepanel.Show()
            # self._fileToggleBtn.SetLabel("Hide File")
            # self._fileToggleBtn.SetValue(True)
            self._cpfilemenuitem.Check(True)
            self.SendSizeEvent()
    #Muestra o esconde el panel Configuraciones, sin preocuparse por los paneles de sonido y gráfico porque contiene los toggle buttons.
    def displayGConfig(self):
        if self._congifpanel.IsShown():
            self._congifpanel.Hide()
            # self._configToggleBtn.SetLabel("Show Configuration")
            # self._configToggleBtn.SetValue(False)
            self._cpcallmenuitem.Check(False)
            self.SendSizeEvent()
        else:
            self._congifpanel.Show()
            # self._configToggleBtn.SetLabel("Hide Configuration")
            # self._configToggleBtn.SetValue(True)
            self._cpcallmenuitem.Check(True)
            self.SendSizeEvent()
    #Muestra o esconde el panel Display, es suficiente porque no se esconde ningún elemento de este panel.
    def displayData(self):
        if self._displaypanel.IsShown():
            self._displaypanel.Hide()
            # self._displayToggleBtn.SetLabel("Show Data Display")
            # self._displayToggleBtn.SetValue(False)
            self._cpdatadisplaymenuitem.Check(False)
            self.SendSizeEvent()
            if self._mainrightsizer.IsRowGrowable(0):
                self._mainrightsizer.RemoveGrowableRow(0)
        else:
            if not self._mainrightsizer.IsRowGrowable(0):
                self._mainrightsizer.AddGrowableRow(0)
            self._displaypanel.Show()
            # self._displayToggleBtn.SetLabel("Hide Data Display")
            # self._displayToggleBtn.SetValue(True)
            self._cpdatadisplaymenuitem.Check(True)
            self._absPosTextCtrl.SetFocus()
            self.SendSizeEvent()

    def displayDataOp(self):
        if not self._cpdataopmenuitem.IsChecked(): #self._operationpanel.IsShown():
            self._operationpanel.Hide()
            self._cpdataopmenuitem.Check(False)
            self._writecommandpanel.Hide()
            self._cpdo_writecommandmenuitem.Check(False)
            self._gnuOctavePanel.Hide()
            self._cpdooctavemenuitem.Check(False)
            self._sizersMFPanel.Hide()
            self._cpdocutslidermenuitem.Check(False)
            # self._gnuOctavePanel.Show()
            # self.displayOctave()
            # self._sizersMFPanel.Show()
            # self.displayFunctions()
            # self._writecommandpanel.Show()
            # self.displayWritefunc()
        else:
            self._operationpanel.Show()
            self._cpdataopmenuitem.Check(True)
            self._writecommandpanel.Show()
            self._cpdo_writecommandmenuitem.Check(True)
            self._gnuOctavePanel.Show()
            self._cpdooctavemenuitem.Check(True)
            self._sizersMFPanel.Show()
            self._cpdocutslidermenuitem.Check(True)
            # self._gnuOctavePanel.Hide()
            # self.displayOctave()
            # self._sizersMFPanel.Hide()
            # self.displayFunctions()
            # self._writecommandpanel.Hide()
            # self.displayWritefunc()
        self.SendSizeEvent()

    def displayWritefunc(self):
        if self._writecommandpanel.IsShown():
            self._writecommandpanel.Hide()
            self._cpdo_writecommandmenuitem.Check(False)
            if not self._sizersMFPanel.IsShown() and self._gnuOctavePanel.IsShown():
                self._operationpanel.Hide()
                if self._cpdataopmenuitem.IsChecked():
                    self._cpdataopmenuitem.Check(False)
            else:
                if self._cpdataopmenuitem.IsChecked():
                    self._cpdataopmenuitem.Check(False)
        else:
            self._operationpanel.Show()
            if self._sizersMFPanel.IsShown() and self._gnuOctavePanel.IsShown():
                self._cpdataopmenuitem.Check(True)
            self._writecommandpanel.Show()
            self._cpdo_writecommandmenuitem.Check(True)
        self.SendSizeEvent()

    def displayOctave(self):
        if self._gnuOctavePanel.IsShown():
            self._gnuOctavePanel.Hide()
            # self._octaveToggleBtn.SetLabel("Show Octave Operation")
            # self._octaveToggleBtn.SetValue(False)
            self._cpdooctavemenuitem.Check(False)
            if not self._sizersMFPanel.IsShown() and self._writecommandpanel.IsShown():
                self._operationpanel.Hide()
                if self._cpdataopmenuitem.IsChecked():
                    self._cpdataopmenuitem.Check(False)
            else:
                if self._cpdataopmenuitem.IsChecked():
                    self._cpdataopmenuitem.Check(False)
        else:
            self._operationpanel.Show()
            if self._sizersMFPanel.IsShown() and self._writecommandpanel.IsShown():
                self._cpdataopmenuitem.Check(True)
            self._gnuOctavePanel.Show()
            # self._octaveToggleBtn.SetLabel("Hide Octave Operation")
            # self._octaveToggleBtn.SetValue(True)
            self._cpdooctavemenuitem.Check(True)
        self.SendSizeEvent()

    def displayFunctions(self):
        if self._sizersMFPanel.IsShown():
            self._sizersMFPanel.Hide()
            # self._sliderToggleBtn.SetLabel("Show Sliders and Math Functions")
            # self._sliderToggleBtn.SetValue(False)
            self._cpdocutslidermenuitem.Check(False)
            if not self._gnuOctavePanel.IsShown() and self._writecommandpanel.IsShown():
                self._operationpanel.Hide()
                if self._cpdataopmenuitem.IsChecked():
                    self._cpdataopmenuitem.Check(False)
            else:
                if self._cpdataopmenuitem.IsChecked():
                    self._cpdataopmenuitem.Check(False)
        else:
            self._operationpanel.Show()
            if self._gnuOctavePanel.IsShown() and self._writecommandpanel.IsShown():
                self._cpdataopmenuitem.Check(True)
            self._sizersMFPanel.Show()
            # self._sliderToggleBtn.SetLabel("Hide Sliders and Math Functions")
            # self._sliderToggleBtn.SetValue(True)
            self._cpdocutslidermenuitem.Check(True)
        self.SendSizeEvent()

    def displaySoundFontConfig (self):
        if self._soundFontPanel.IsShown():
            self._soundFontPanel.Hide()
            self._configSoundToggleBtn.SetLabel("Show Sound\nConfigurations")
            self._configSoundToggleBtn.SetValue(False)
            self._cpconfigsoundmenuitem.Check(False)
        else:
            self._congifpanel.Show()
            # self._configToggleBtn.SetLabel("Hide Configuration")
            # self._configToggleBtn.SetValue(True)
            self._cpcallmenuitem.Check(True)
            self._soundFontPanel.Show()
            self._configSoundToggleBtn.SetLabel("Hide Sound\nConfigurations")
            self._configSoundToggleBtn.SetValue(True)
            self._cpconfigsoundmenuitem.Check(True)
        self.SendSizeEvent()

    def linvslog_soundscale(self):
        if self._linvslog_soundscale_togglebtn.GetValue():
            #Set logarithmic
            self._linvslog_soundscale_togglebtn.SetLabel('Set linear scale')
            self._linvslog_soundscale_togglebtn.SetValue(True)
            self._linvslog_soundscale_display_togglebtn.SetLabel('Set linear scale')
            self._linvslog_soundscale_display_togglebtn.SetValue(True)
            self._slinscale_menuitem.Check(False)
            self._slogscale_menuitem.Check(True)
            self._datasound.reproductor.set_logscale(True)
        else:
            #Set linear
            self._linvslog_soundscale_togglebtn.SetLabel('Set logarithmic scale')
            self._linvslog_soundscale_togglebtn.SetValue(False)
            self._linvslog_soundscale_display_togglebtn.SetLabel('Set logarithmic scale')
            self._linvslog_soundscale_display_togglebtn.SetValue(False)
            self._slinscale_menuitem.Check(True)
            self._slogscale_menuitem.Check(False)
            self._datasound.reproductor.set_logscale(False)
        self.SendSizeEvent()
        
    def linvslog_soundscale_display(self):
        if self._linvslog_soundscale_display_togglebtn.GetValue():
            #Set logarithmic
            self._linvslog_soundscale_togglebtn.SetLabel('Set linear scale')
            self._linvslog_soundscale_togglebtn.SetValue(True)
            self._linvslog_soundscale_display_togglebtn.SetLabel('Set linear scale')
            self._linvslog_soundscale_display_togglebtn.SetValue(True)
            self._slinscale_menuitem.Check(False)
            self._slogscale_menuitem.Check(True)
            self._datasound.reproductor.set_logscale(True)
        else:
            #Set linear
            self._linvslog_soundscale_togglebtn.SetLabel('Set logarithmic scale')
            self._linvslog_soundscale_togglebtn.SetValue(False)
            self._linvslog_soundscale_display_togglebtn.SetLabel('Set logarithmic scale')
            self._linvslog_soundscale_display_togglebtn.SetValue(False)
            self._slinscale_menuitem.Check(True)
            self._slogscale_menuitem.Check(False)
            self._datasound.reproductor.set_logscale(False)
        self.SendSizeEvent()

    def setlinsoundscale(self):
        if self._slinscale_menuitem.IsChecked():
            #Set linear
            self._linvslog_soundscale_togglebtn.SetLabel('Set logarithmic scale')
            self._linvslog_soundscale_togglebtn.SetValue(False)
            self._linvslog_soundscale_display_togglebtn.SetLabel('Set logarithmic scale')
            self._linvslog_soundscale_display_togglebtn.SetValue(False)
            self._slogscale_menuitem.Check(False)
            #self.dataSound.reproductor.()
        else:
            #Set logarithmic
            self._linvslog_soundscale_togglebtn.SetLabel('Set linear scale')
            self._linvslog_soundscale_togglebtn.SetValue(True)
            self._linvslog_soundscale_display_togglebtn.SetLabel('Set linear scale')
            self._linvslog_soundscale_display_togglebtn.SetValue(True)
            self._slogscale_menuitem.Check(True)
            #self.dataSound.reproductor.()
        self.SendSizeEvent()

    def setlogsoundscale(self):
        if self._slogscale_menuitem.IsChecked():
            #Set logarithmic
            self._linvslog_soundscale_togglebtn.SetLabel('Set linear scale')
            self._linvslog_soundscale_togglebtn.SetValue(True)
            self._linvslog_soundscale_display_togglebtn.SetLabel('Set linear scale')
            self._linvslog_soundscale_display_togglebtn.SetValue(True)
            self._slinscale_menuitem.Check(False)
            #self.dataSound.reproductor.()
        else:
            #Set linear
            self._linvslog_soundscale_togglebtn.SetLabel('Set logarithmic scale')
            self._linvslog_soundscale_togglebtn.SetValue(False)
            self._linvslog_soundscale_display_togglebtn.SetLabel('Set logarithmic scale')
            self._linvslog_soundscale_display_togglebtn.SetValue(False)
            self._slinscale_menuitem.Check(True)
            #self.dataSound.reproductor.()
        self.SendSizeEvent()

    def cont_vs_discrete_sound(self):
        if self._contdiscsoundToggleBtn.GetValue():
            #Set continuous
            self._contdiscsoundToggleBtn.SetLabel("Set discrete sound")
            self._contdiscsoundToggleBtn.SetValue(True)
            self._contdiscsound_display_ToggleBtn.SetLabel("Set discrete sound")
            self._contdiscsound_display_ToggleBtn.SetValue(True)
            self._scontmenuitem.Check(True)
            self._sdiscretemenuitem.Check(False)
            self._datasound.reproductor.set_continuous()
        else:
            #Set discrete
            self._contdiscsoundToggleBtn.SetLabel("Set continuous sound")
            self._contdiscsoundToggleBtn.SetValue(False)
            self._contdiscsound_display_ToggleBtn.SetLabel("Set continuous sound")
            self._contdiscsound_display_ToggleBtn.SetValue(False)
            self._scontmenuitem.Check(False)
            self._sdiscretemenuitem.Check(True)
            self._datasound.reproductor.set_discrete()
        self.SendSizeEvent()
        
    def cont_vs_discrete_sound_display(self):
        if self._contdiscsound_display_ToggleBtn.GetValue():
            #Set continuous
            self._contdiscsoundToggleBtn.SetLabel("Set discrete sound")
            self._contdiscsoundToggleBtn.SetValue(True)
            self._contdiscsound_display_ToggleBtn.SetLabel("Set discrete sound")
            self._contdiscsound_display_ToggleBtn.SetValue(True)
            self._scontmenuitem.Check(True)
            self._sdiscretemenuitem.Check(False)
            self._datasound.reproductor.set_continuous()
        else:
            #Set discrete
            self._contdiscsoundToggleBtn.SetLabel("Set continuous sound")
            self._contdiscsoundToggleBtn.SetValue(False)
            self._contdiscsound_display_ToggleBtn.SetLabel("Set continuous sound")
            self._contdiscsound_display_ToggleBtn.SetValue(False)
            self._scontmenuitem.Check(False)
            self._sdiscretemenuitem.Check(True)
            self._datasound.reproductor.set_discrete()
        self.SendSizeEvent()

    def setcontsound(self):
        if self._scontmenuitem.IsChecked():
            #Set continuous
            self._contdiscsoundToggleBtn.SetLabel("Set discrete sound")
            self._contdiscsoundToggleBtn.SetValue(True)
            self._contdiscsound_display_ToggleBtn.SetLabel("Set discrete sound")
            self._contdiscsound_display_ToggleBtn.SetValue(True)
            # self._scontmenuitem.Check(True)
            self._sdiscretemenuitem.Check(False)
            self._datasound.reproductor.set_continuous()
        else:
            #Set discrete
            self._contdiscsoundToggleBtn.SetLabel("Set continuous sound")
            self._contdiscsoundToggleBtn.SetValue(False)
            self._contdiscsound_display_ToggleBtn.SetLabel("Set continuous sound")
            self._contdiscsound_display_ToggleBtn.SetValue(False)
            # self._scontmenuitem.Check(False)
            self._sdiscretemenuitem.Check(True)
            self._datasound.reproductor.set_discrete()
        self.SendSizeEvent()

    def setdiscretesound(self):
        if self._sdiscretemenuitem.IsChecked():
            #Set discrete
            self._contdiscsoundToggleBtn.SetLabel("Set continuous sound")
            self._contdiscsoundToggleBtn.SetValue(False)
            self._contdiscsound_display_ToggleBtn.SetLabel("Set continuous sound")
            self._contdiscsound_display_ToggleBtn.SetValue(False)
            self._scontmenuitem.Check(False)
            # self._sdiscretemenuitem.Check(True)
            self._datasound.reproductor.set_discrete()
        else:
            #Set continuous
            self._contdiscsoundToggleBtn.SetLabel("Set discrete sound")
            self._contdiscsoundToggleBtn.SetValue(True)
            self._contdiscsound_display_ToggleBtn.SetLabel("Set discrete sound")
            self._contdiscsound_display_ToggleBtn.SetValue(True)
            self._scontmenuitem.Check(True)
            # self._sdiscretemenuitem.Check(False)
            self._datasound.reproductor.set_continuous()
        self.SendSizeEvent()

    def displayfreqmapping(self):
        if self._freqmappingCheckBox.IsChecked():
            self._freqmappingPanel.Show()
            self._volmappingCheckBox.SetValue(False)
            self._volmappingPanel.Hide()
            self._ssvolmappingmenuitem.Check(False)
            self._ssfreqmappingmenuitem.Check(True)
        else:
            self._freqmappingPanel.Hide()
            self._volmappingCheckBox.SetValue(True)
            self._volmappingPanel.Show()
            self._ssvolmappingmenuitem.Check(True)
            self._ssfreqmappingmenuitem.Check(False)
        self.SendSizeEvent()

    def displayfreqmapping_menuitem(self):
        if self._ssfreqmappingmenuitem.IsChecked():
            self._freqmappingPanel.Show()
            self._volmappingCheckBox.SetValue(False)
            self._volmappingPanel.Hide()
            self._ssvolmappingmenuitem.Check(False)
            self._freqmappingCheckBox.SetValue(True)
        else:
            self._freqmappingPanel.Hide()
            self._volmappingCheckBox.SetValue(True)
            self._volmappingPanel.Show()
            self._ssvolmappingmenuitem.Check(True)
            self._freqmappingCheckBox.SetValue(False)
        self.SendSizeEvent()

    def displayvolmapping(self):
        if self._volmappingCheckBox.IsChecked():
            self._freqmappingPanel.Hide()
            self._freqmappingCheckBox.SetValue(False)
            self._volmappingPanel.Show()
            self._ssfreqmappingmenuitem.Check(False)
            self._ssvolmappingmenuitem.Check(True)
        else:
            self._freqmappingPanel.Show()
            self._freqmappingCheckBox.SetValue(True)
            self._volmappingPanel.Hide()
            self._ssfreqmappingmenuitem.Check(True)
            self._ssvolmappingmenuitem.Check(False)
        self.SendSizeEvent()

    def displayvolmapping_menuitem(self):
        if self._ssvolmappingmenuitem.IsChecked():
            self._freqmappingPanel.Hide()
            self._freqmappingCheckBox.SetValue(False)
            self._volmappingPanel.Show()
            self._ssfreqmappingmenuitem.Check(False)
            self._volmappingCheckBox.SetValue(True)
        else:
            self._freqmappingPanel.Show()
            self._freqmappingCheckBox.SetValue(True)
            self._volmappingPanel.Hide()
            self._ssfreqmappingmenuitem.Check(True)
            self._volmappingCheckBox.SetValue(False)
        self.SendSizeEvent()

    def displayPlotConfig(self):
        if self._configPlotPanel.IsShown():
            self._configPlotPanel.Hide()
            self._configPlotToggleBtn.SetLabel("Show Plot\nConfigurations")
            self._configPlotToggleBtn.SetValue(False)
            self._cpconfigplotmenuitem.Check(False)
        else:
            self._congifpanel.Show()
            # self._configToggleBtn.SetLabel("Hide Configuration")
            # self._configToggleBtn.SetValue(True)
            self._cpcallmenuitem.Check(True)
            self._configPlotPanel.Show()
            self._configPlotToggleBtn.SetLabel("Hide Plot\nConfigurations")
            self._configPlotToggleBtn.SetValue(True)
            self._cpconfigplotmenuitem.Check(True)
        self.SendSizeEvent()

    def displayVisualConfig(self):
        #under construction
        self.SendSizeEvent()

    def displayDataParamPanel(self):
        if self._openPanel.IsShown():
            self._openPanel.Hide()
            #self._dataParamPlotToggleBtn.SetValue( False )
            self._cpdataparamplotmenuitem.Check(False)
        else:
            self._openPanel.Show()
            #self._dataParamPlotToggleBtn.SetValue( True )
            self._cpdataparamplotmenuitem.Check(True)
        self._displaypanel.SendSizeEvent()

    def displayspecialsoundconfig(self):
        if self._ssspecialconfigmenuitem.IsChecked():
            self._congifpanel.Show()
            self.displaySoundFontConfig()
            # self._configToggleBtn.SetLabel("Hide Configuration")
            # self._configToggleBtn.SetValue(True)
            # self._cpcallmenuitem.Check(True)
            self._specialsoundcongifpanel.Show()
            # self._specialConfigSoundToggleBtn.SetValue(True)
            # self._specialConfigSoundToggleBtn.SetLabel("Hide Special Sound\nConfigurations")
            self._ssspecialconfigmenuitem.Check(True)
            self._envelope_checkbox.SetValue(True)
            self._soundattacktextctrl.SetFocus()
        else:
            self._specialsoundcongifpanel.Hide()
            # self._specialConfigSoundToggleBtn.SetValue(False)
            # self._specialConfigSoundToggleBtn.SetLabel("Show Special Sound\nConfigurations")
            self._ssspecialconfigmenuitem.Check(False)
            self._envelope_checkbox.SetValue(False)
            self._envelope_checkbox.SetFocus()
        self.SendSizeEvent()

    def displayenvelopegraph(self):
        if self._envelopegraphpanel.IsShown():
            self._envelopegraphpanel.Hide()
            self._envelopegraphtogglebtn.SetValue(False)
            self._envelopegraphtogglebtn.SetLabel('Show envelope\nplot')
        else:
            self._envelopegraphpanel.Show()
            self._envelopegraphtogglebtn.SetValue(True)
            self._envelopegraphtogglebtn.SetLabel('Hide envelope\nplot')
        self.SendSizeEvent()

    def soundFontSelect(self):
        self._soundFontPanel.Hide()
        self.displaySoundFontConfig()
        # self._soundFontTextCtrl.SetFocus()

    def panelSSInstSelect(self):
        self._soundFontPanel.Hide()
        self.displaySoundFontConfig()
        self._soundwaveformtextctrl.SetFocus()

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
    def _onclose(self, event):
        self.Close()

    def _eventabout( self, event ):
        message = "SonoUno is a Sonification Software for astronomical data in two column files. \n\nThis software is being developed by Bioing. Johanna Casado on her PhD tesis framework, under direction of Dr. Beatriz García. With general collaboration of Dr. Wanda Diaz Merced, and the collaboration on software development of Aldana Palma, Bioing. Julieta Carricondo Robino and Mg. Ing. Gonzalo A. de la Vega.\n\nThe email contact of the SonoUno team is: sonounoteam@gmail.com"
        wx.MessageBox(message, 'Information', wx.OK | wx.ICON_INFORMATION)

    def _eventmanual( self, event ):
        # message = "The user manual of the software is located in the software root folder in PDF format, or in the next link (copy and paste on the browser): \n"
        # url = "https://drive.google.com/file/d/1RtI1bG5Q-PjpT3LBcmWJfW88YfbqCCg1/view?usp=sharing"
        # dialogs.scrolledMessageDialog(parent=self, message=message+url, title='Information', pos=wx.DefaultPosition, size=(500, 150))
        webbrowser.open("http://sion.frm.utn.edu.ar/sonoUno/", new=2, autoraise=True)

    def _eventclose( self, event ):
#        try:
#            text = self._pythonShell.GetText()
#            #text.encode('utf-8')
#            self._expdata.printoutput("Python console text: \n" + text.encode('utf-8'))
#        except Exception as e:
#            self._expdata.writeexception(e)
        self._timer.Stop()
        self._timer_envelope.Stop()
        if self._filesaved: #cambiar a 'if not' para que pregunte cuando no ha sido salvado.
            if wx.MessageBox("The file has not been saved... continue closing?",
                                 "Please confirm",
                                 wx.ICON_QUESTION | wx.YES_NO, self) != wx.YES:
                return
            else:
                event.Skip()
        else:
            event.Skip()

    def _eventopen( self, event ):
        self._expdata.printoutput("Open button pressed.")
        self.open_method()

    def _eventTitleEdData( self, event ):
        self._expdata.printoutput("Enter key pressed on the text box of data title.")
        self.titleEdData()

    def _eventdatagridpage(self, event):
        self._expdata.printoutput("The display page of the grid was changed.")
        #Escribir set y get para esta variable
        if self.getXActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
        else:
            self._actualgridpagetextctrl.SetValue(str(self._datagridslider.GetValue()))
            if self.originaldataselected:
                self._setdatagridpage(self._datagridslider.GetValue())
            else:
                self.dataGridUpdate()
        event.Skip()

    def _eventAskLabelData( self, event ):
        self._expdata.printoutput("The check box to set if the data have the labels on the fisrt row, is selected.")
        self.askLabelData()

    def _eventAddGridChanges( self, event ):
        self._expdata.printoutput("Apply changes button of the grid is pressed.")
        self.dataGridChange()

    def _eventUpdateGrid( self, event ):
        self._expdata.printoutput("Update button of the grid is pressed.")
        self.originaldataselected = False
        self.dataGridUpdate()

    def _eventOriginalGrid( self, event ):
        self._expdata.printoutput("Original Array button of the grid is pressed.")
        self.originaldataselected = True
        self._setdatagridpage(self._datagridslider.GetValue())
        # self.dataGridOriginal()

    def _eventAxisChoiceX( self, event ):
        self._expdata.printoutput("A new choice on the X axis is selected.")
        self.axisChoiceXMethod()

    def _eventAxisChoiceY( self, event ):
        self._expdata.printoutput("A new choice on the Y axis is selected.")
        self.axisChoiceYMethod()

    def _eventdeleteallmark( self, event ):
        self._expdata.printoutput("Delete all marks button is pressed.")
        self.deleteAllMark()

    def _eventsaveplot( self, event ):
        self._expdata.printoutput("Export Plot button is pressed.")
        self.savePlot()

    def _eventsavesound( self, event ):
        self._expdata.printoutput("Export Sound button is pressed.")
        self.eSound()

    def _eventplay( self, event ):
        self.playinloop_state = False
        self.playwithtime_status = False
        self.playMethod()

#    def _eventPause( self, event ):
#        self._expdata.printoutput("Pause button is pressed.")
#        self._datasound.make_sound(0, -1)
#        self._timer.Stop()

    def _eventstop( self, event ):
        self._expdata.printoutput("Stop button is pressed.")
        self.stopMethod()

    def _eventmarkpoint( self, event ):
        self._expdata.printoutput("Mark point button is pressed.")
        self.markPoints()

    def _eventdeletelastmark( self, event ):
        self._expdata.printoutput("Delete last mark button is pressed.")
        self.deleteLastMark()

    def _eventcpdataparamplot( self, event ):
        self.displayDataParamPanel()

    def _eventsavedata( self, event ):
        self._expdata.printoutput("Export Data button is pressed.")
        self.saveData()

    def _eventsavemarks( self, event ):
        self._expdata.printoutput("Export Points button is pressed.")
        self.saveMarks()

    def _eventAbsPos( self, event ):
        self._expdata.printoutput("Position Slider Bar is modified.")
        self._set_timerindex(self._abspos_slider.GetValue())
        if self.getXActual().any()==None:
            self._expdata.writeinfo("The data has not been imported yet.")
            self._abspos_slider.SetValue(0)
        else:
            self._absposlabel_textctrl.SetValue(str(round(self.getXActual()[self._abspos_slider.GetValue()],4)))
            self.absPosSetting()
        event.Skip()

    def _eventabsposition(self, event):
        value=(self._absposlabel_textctrl.GetLineText(0))
        self.xposition_command(value)
        event.Skip()

    def _eventtempoposition(self, event):
        value = (self._tempoposlabel_textctrl.GetLineText(0))
        self.selecttempo_command(value)
        event.Skip()

    def _eventSoundVel( self, event ):
        self._expdata.printoutput("Sound Velocity Slider Bar is modified.")
        self._tempoposlabel_textctrl.SetValue(str(self._soundVelSlider.GetValue()))
        self._set_velocity(self._soundVelSlider.GetValue())
        self.tempo()

#    def _eventLVLimitSlider( self, event ):
#        self._expdata.printoutput("Horizontal lower limit is setted.")
#        self.cutVertical()

#    def _eventUVLimitSlider( self, event ):
#        self._expdata.printoutput("Horizontal upper limit is setted.")
#        self.cutVertical()

    def _eventLHLimitSlider( self, event ):
        self._expdata.printoutput("Horizontal lower limit is setted.")
        self.cutHorizontal()

    def _eventUHLimitSlider( self, event ):
        self._expdata.printoutput("Horizontal upper limit is setted.")
        self.cutHorizontal()

    def _eventConfigSound(self, event):
        self._expdata.printoutput("Event configuration sound is setted.")
        self.displaySoundFontConfig()

    def _event_linvslog_soundscalechoice(self, event):
        self.linvslog_soundscale()
        event.Skip()
        
    def _event_linvslog_soundscalechoice_display(self, event):
        self.linvslog_soundscale_display()
        event.Skip()

    def _eventcontdiscsoundchoice(self, event):
        self.cont_vs_discrete_sound()
        event.Skip()
    
    def _eventcontdiscsoundchoice_display(self, event):
        self.cont_vs_discrete_sound_display()
        event.Skip()

    def _eventsoundvolumn(self, event):
        self._expdata.printoutput("Event sound volume is setted.")
        # self.set_soundvolumn(self._soundvolumnslider.GetValue())
        self._datasound.reproductor.set_volume(self._soundvolumnslider.GetValue())

    def _eventshow_soundfreqmin(self, event):
        if self._soundfreqmin_checkbox.IsChecked():
            self._soundfreqmin_panel.Show()
        else:
            self._soundfreqmin_panel.Hide()
        self.SendSizeEvent()
        event.Skip()

    def _eventsoundfreqmin(self, event):
        self._expdata.printoutput("Event sound min frequency is setted.")
        value = (int(self._minsoundfreqmintextctrl.GetLineText(0))
            + self._soundfreqminslider.GetValue())
        self._actualsoundfreqmintextctrl.SetValue(str(value))
        self._datasound.reproductor.set_min_freq(value)
        event.Skip()
        
    def _eventshow_soundfreqmax(self, event):
        if self._soundfreqmax_checkbox.IsChecked():
            self._soundfreqmax_panel.Show()
        else:
            self._soundfreqmax_panel.Hide()
        self.SendSizeEvent()
        event.Skip()

    def _eventsoundfreqmax(self, event):
        self._expdata.printoutput("Event sound max frequency is setted.")
        value = (int(self._minsoundfreqmaxtextctrl.GetLineText(0))
            + self._soundfreqmaxslider.GetValue())
        self._actualsoundfreqmaxtextctrl.SetValue(str(value))
        self._datasound.reproductor.set_max_freq(value)
        event.Skip()

    def _eventfreqmapping(self, event):
        self.displayfreqmapping()
        self._datasound.reproductor.set_mapping('frequency')
        event.Skip()

    def _eventvolmapping(self, event):
        self.displayvolmapping()
        self._datasound.reproductor.set_mapping('volume')
        event.Skip()
        
    def _eventshow_soundvolmin(self, event):
        if self._soundvolmin_checkbox.IsChecked():
            self._soundvolmin_panel.Show()
        else:
            self._soundvolmin_panel.Hide()
        self.SendSizeEvent()
        event.Skip()

    def _eventsoundvolmin(self, event):
        value = self._soundvolminslider.GetValue()
        self._actualsoundvolmintextctrl.SetValue(str(value))
        self._datasound.reproductor.set__volume(value)
        event.Skip()
        
    def _eventshow_soundvolmax(self, event):       
        if self._soundvolmax_checkbox.IsChecked():
            self._soundvolmax_panel.Show()
        else:
            self._soundvolmax_panel.Hide()
        self.SendSizeEvent()
        event.Skip()

    def _eventsoundvolmax(self, event):
        value = self._soundvolmaxslider.GetValue()
        self._actualsoundvolmaxtextctrl.SetValue(str(value))
        self._datasound.reproductor.set_max_volume(value)
        event.Skip()
        
    def _eventshow_soundvolfreq(self, event):
        if self._soundvolfreq_checkbox.IsChecked():
            self._soundvolfreq_panel.Show()
        else:
            self._soundvolfreq_panel.Hide()
        self.SendSizeEvent()
        event.Skip()

    def _eventsoundvolfreq(self, event):
        self._expdata.printoutput("Event frequency of volume mapping is setted.")
        value = (int(self._minsoundvolfreqtextctrl.GetLineText(0))
                 + self._soundvolfreq_slider.GetValue())
        self._actualsoundvolfreq_textctrl.SetValue(str(value))
        self._datasound.reproductor.set_fixed_freq(value)
        event.Skip()

    def _eventswaveform(self, event):
        self._expdata.printoutput("Event select waveform choice on the main display is setted.")
        self.swaveformlistboxchoice()
    
    def _eventshowenvelope(self, event):
        if self._envelope_checkbox.GetValue():
            self._specialsoundcongifpanel.Show()
            self._ssspecialconfigmenuitem.Check(True)
        else:
            self._specialsoundcongifpanel.Hide()
            self._ssspecialconfigmenuitem.Check(False)
        self.SendSizeEvent()
        event.Skip()

    def _eventsoundattack(self, event):
        if not self._check_adr():
            value = float(self._actualattacktextctrl.GetValue())
            self._soundattackslider.SetValue(100*value)

        self._expdata.printoutput("Event sound envelope attack is setted.")
        value = self._soundattackslider.GetValue()/100
        self._actualattacktextctrl.SetValue(str(value))
        self._set_soundattack(value)
        self._setspecialsoundconfig()
        self.plotsoundenvelope()
        event.Skip()

    def _eventsounddecay(self, event):
        if not self._check_adr():
            value = float(self._actualdecaytextctrl.GetValue())
            self._sounddecayslider.SetValue(100*value)
        self._expdata.printoutput("Event sound envelope decay is setted.")
        value = self._sounddecayslider.GetValue()/100
        self._actualdecaytextctrl.SetValue(str(value))
        self._set_sounddecay(value)
        self._setspecialsoundconfig()
        self.plotsoundenvelope()
        event.Skip()

    def _eventsoundsustain(self, event):
        self._expdata.printoutput("Event sound envelope sustain is setted.")
        value = self._soundsustainslider.GetValue()
        self._actualsustaintextctrl.SetValue(str(value))
        self._set_soundsustain(value)
        self._setspecialsoundconfig()
        self.plotsoundenvelope()
        event.Skip()

    def _eventsoundrelease(self, event):
        if not self._check_adr():
            value = float(self._actualreleasetextctrl.GetValue())
            self._soundreleaseslider.SetValue(100*value)
        self._expdata.printoutput("Event sound envelope release is setted.")
        value = self._soundreleaseslider.GetValue()/100
        self._actualreleasetextctrl.SetValue(str(value))
        self._set_soundrelease(value)
        self._setspecialsoundconfig()
        self.plotsoundenvelope()
        event.Skip()

    def _eventSpecialSoundConfig( self, event ):
        self.displayspecialsoundconfig()
        event.Skip()

    def _eventenvelopegraph(self, event):
        self.displayenvelopegraph()
        event.Skip()
        
    def _eventenvelopeplay(self, event):
        if self._envelopeplaytogglebtn.GetValue():
            #play the sound
            self._envelopeplaytogglebtn.SetLabel('Stop envelope\nsound')
            self._playenvelope()
        else:
            #Stop the sound
            self._envelopeplaytogglebtn.SetLabel('Play envelope\nsound')
            if self._timer_envelope.IsRunning():
                self._timer_envelope.Stop()
                self._set_timerenvelopeindex(0)

    def _eventGFile(self, event):
        self._expdata.printoutput("Event File Panel is setted.")
        self.displayGFile()

    def _eventGConfig(self, event):
        self._expdata.printoutput("Event Config Panel is setted.")
        self.displayGConfig()

    def _eventGDisplay(self, event):
        self._expdata.printoutput("Event data display is setted.")
        self.displayData()

    def _eventOctaveToggle( self, event ):
        self._expdata.printoutput("Event octave panel is setted.")
        self.displayOctave()

    def _eventSliderToggle( self, event ):
        self._expdata.printoutput("Event cut sliders panel is setted.")
        self.displayFunctions()

    def _eventMatFc(self, event):
        self._expdata.printoutput("Event mathematical function is setted.")
        self.matFcSelection()

    def _eventAvNPoints(self, event):
        self._expdata.printoutput("Event average number of points is setted.")
        self._set_average_numpoints(self._avNPointsspinCtrl.GetValue())
        self.matFcExecutor()

    def _eventlastcutmf(self, event):
        self._avNPointsspinCtrl.Enable(False)
        self._expdata.printoutput("Last limits cut function is selected.")
        self._set_mathfunction("Last limits cut")
        self.matFcExecutor()

    def _eventoriginalmf(self, event):
        self._avNPointsspinCtrl.Enable(False)
        self._expdata.printoutput("Original function is selected.")
        self._set_mathfunction("Original")
        self.matFcExecutor()

    def _eventinversemf(self, event):
        self._avNPointsspinCtrl.Enable(False)
        self._expdata.printoutput("Inverse function is selected.")
        self._set_mathfunction("Inverse")
        self.matFcExecutor()

#    def _eventMFPlayBack(self, event):
#        self._avNPointsspinCtrl.Enable(False)
#        self._expdata.printoutput("Play Backward function is selected.")
#        self._set_mathfunction("Play Backward")
#        self.matFcExecutor()

    def _eventsquaremf(self, event):
        self._avNPointsspinCtrl.Enable(False)
        self._expdata.printoutput("Square function is selected.")
        self._set_mathfunction("Square")
        self.matFcExecutor()

    def _eventsquarerootmf( self, event ):
        self._avNPointsspinCtrl.Enable(False)
        self._expdata.printoutput("Square root function is selected.")
        self._set_mathfunction("Square root")
        self.matFcExecutor()

    def _eventlogmf(self, event):
        self._avNPointsspinCtrl.Enable(False)
        self._expdata.printoutput("Logarithm function is selected.")
        self._set_mathfunction("Logarithm")
        self.matFcExecutor()

    def _eventaveragemf(self, event):
        self._sizersMFPanel.Hide()
        self.displayFunctions()
        self._expdata.printoutput("Average function is selected.")
        self._avNPointsspinCtrl.SetValue(1)
        self._avNPointsspinCtrl.Enable(True)
        self.averageSelect()

    def _eventabsposselect(self, event):
        self._expdata.printoutput("Set the focus on the abscisa position.")
        self._displaypanel.Hide()
        self.displayData()
        self._absPosTextCtrl.SetFocus()

    def _eventtemposelect(self, event):
        self._expdata.printoutput("Set the focus on the tempo.")
        self._displaypanel.Hide()
        self.displayData()
        self._soundVelTextCtrl.SetFocus()

#    def _eventvlowerlimitselect(self, event):
#        self._expdata.printoutput("Set the focus on the vertical lower limit.")
#        self._sizersMFPanel.Hide()
#        self.displayFunctions()
#        self._lvLimitTextCtrl.SetFocus()

#    def _eventvupperlimitselect(self, event):
#        self._expdata.printoutput("Set the focus on the vertical upper limit.")
#        self._sizersMFPanel.Hide()
#        self.displayFunctions()
#        self._uvLimitTextCtrl.SetFocus()

    def _eventhlowerlimitselect(self, event):
        self._expdata.printoutput("Set the focus on the horizontal lower limit.")
        self._sizersMFPanel.Hide()
        self.displayFunctions()
        self._lhLimitTextCtrl.SetFocus()

    def _eventhupperlimitselect(self, event):
        self._expdata.printoutput("Set the focus on the horizontal upper limit.")
        self._sizersMFPanel.Hide()
        self.displayFunctions()
        self._uhLimitTextCtrl.SetFocus()

    def _eventavnumpointselect(self, event):
        self._expdata.printoutput("The average function is selected.")
        self._sizersMFPanel.Hide()
        self.displayFunctions()
        self._avNPointsTextCtrl.SetFocus()
        self._avNPointsspinCtrl.SetValue(1)
        self._avNPointsspinCtrl.Enable(True)
        self.averageSelect()

    def _eventoctaveselect(self, event):
        self._expdata.printoutput("The octave output was selected.")
        self._gnuOctavePanel.Hide()
        self.displayOctave()
        self._pythonShell.SetFocus()
#
    def _eventsswaveformselect(self, event):
        self._expdata.printoutput("The waveform select on panel was selected.")
        self.panelSSInstSelect()

    def _eventcpfileselect(self, event):
        self._expdata.printoutput("The panel file was selected.")
        self.displayGFile()
        self._openButton.SetFocus()

    def _eventcpdatadisplayselect(self, event):
        self._expdata.printoutput("The panel data display was selected.")
        self.displayData()
        self._absPosTextCtrl.SetFocus()

    def _eventcpdataopselect(self, event):
        self._expdata.printoutput("The panel data operation was selected.")
        self.displayDataOp()
        self._pythonShell.SetFocus()

    def _eventcpdo_writecommandselect(self, event):
        self._expdata.printoutput("The panel write functionalities was selected.")
        self.displayWritefunc()
        self._writecommandtextctrl.SetFocus()
        event.Skip()

    def _eventcpdooctaveselect( self, event ):
        self._expdata.printoutput("The panel octave was selected.")
        self.displayOctave()
        self._pythonShell.SetFocus()

    def _eventcpdocutsliderselect( self, event ):
        self._expdata.printoutput("The panel sliders and mathematical functions was selected.")
        self.displayFunctions()
#        self._vAxisTextCtrl.SetFocus()

    def _eventcpcallselect(self, event):
        self._expdata.printoutput("The panel configurations was selected.")
        self.displayGConfig()
        self._configSoundToggleBtn.SetFocus()

    def _eventcpconfigsoundselect(self, event):
        self._expdata.printoutput("The panel configuration sound was selected.")
        self.displaySoundFontConfig()
        self._configSoundToggleBtn.SetFocus()

    def _eventcpconfigplotselect(self, event):
        self._expdata.printoutput("The panel configuration plot was selected.")
        self.displayPlotConfig()
        self._configPlotToggleBtn.SetFocus()

    def _eventcpconfigvisualselect(self, event):
        self._expdata.printoutput("The panel configuration visual was selected.\nUNDER CONSTRUCTION.")
        self.displayVisualConfig()
##Set focus cuando se generen los objetos

    def _eventlinsoundscalechoice(self, event):
        self.setlinsoundscale()
        event.Skip()

    def _eventlogsoundscalechoice(self, event):
        self.setlogsoundscale()
        event.Skip()

    def _eventcontsoundchoice(self, event):
        self.setcontsound()
        event.Skip()

    def _eventdiscsoundchoice(self, event):
        self.setdiscretesound()
        event.Skip()

    def _eventssvolumeselect( self, event ):
        self._expdata.printoutput("The volume button was selected.")
        #Cambiar para setear el volumen
        self.soundFontSelect()
        self._volumeTextCtrl.SetFocus()
        event.Skip()

    def _eventssfreqmappingselect(self, event):
        self._expdata.printoutput("The frequency mapping was selected.")
        self.soundFontSelect()
        self.displayfreqmapping_menuitem()
        self._soundfreqmin_checkbox.SetFocus()
        event.Skip()

    def _eventssvolmappingselect(self, event):
        self._expdata.printoutput("The volume mapping was selected.")
        self.soundFontSelect()
        self.displayvolmapping_menuitem()
        self._soundvolmin_checkbox.SetFocus()
        event.Skip()

    def _eventConfigPlot( self, event ):
        self._expdata.printoutput("Plot configurations panel was modified.")
        self.displayPlotConfig()
        self._configPlotToggleBtn.SetFocus()

    def _eventLineStyleConfig( self, event ):
        self._expdata.printoutput("Line style of the plot was modified.")
        index = self._lineStyleChoice.GetSelection()
        self.lineStyleConfig(index)

    def _eventMarkerStyleConfig( self, event ):
        self._expdata.printoutput("Marker style of the plot was modified.")
        self._set_markerstyle_index(self._markerStyleChoice.GetSelection())
        self.markerStyleConfig()

    def _eventColorStyleConfig( self, event ):
        self._expdata.printoutput("Color style of the plot was modified.")
        index = self._colorStyleChoice.GetSelection()
        self.colorStyleConfig(index)

    def _eventsplotlineselect( self, event ):
        self._expdata.printoutput("The line style configuration is selected.")
        self.lineStyleSelect()

    def _eventsplotmarkerselect( self, event ):
        self._expdata.printoutput("The line marker style configuration is selected.")
        self.markerStyleSelect()

    def _eventsplotcolorselect( self, event ):
        self._expdata.printoutput("The line color style configuration is selected.")
        self.colorStyleSelect()

    def _eventsplotgridoptionselect( self, event ):
        self._expdata.printoutput("The grid option configurations is selected.")
        self.gridOpSelect()
        if self._gridChoice.IsChecked():
            self._gridChoice.SetValue(False)
        else:
            self._gridChoice.SetValue(True)
        self.displayGridChoice()

    def _eventGridChoice( self, event ):
        self._expdata.printoutput("The grid check box is selected.")
        self.displayGridChoice()

    def _eventGridColorChoice( self, event ):
        self._expdata.printoutput("The grid color style is modified.")
        self._set_gridcolor(self._gridColorChoice.GetString(self._gridColorChoice.GetSelection()))
        self.displayGridChoice()

    def _eventGridLineChoice( self, event ):
        self._expdata.printoutput("The grid line style is modified.")
        self._set_gridlinestyle(self._gridLineChoice.GetString(self._gridLineChoice.GetSelection()))
        self.displayGridChoice()

    def _eventGridWidthSpinCtrl( self, event ):
        self._expdata.printoutput("The grid width is modified.")
        self._set_gridlinewidth(self._gridWidthSpinCtrl.GetValue())
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
        self._leftpanel.Show()
        self._rightpanel.Show()
        self.retrieveFromOctavePanel.Hide()

    def _eventwritecommand(self, event):
        self._expdata.printoutput("One command was introduced.")
        self.detectcommand()
        event.Skip()

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

#Se conservan por si llega a surgir un error, se ha duplicado este código por uno de los merge realizados.
#    def _eventabout( self, event ):
#        message = "SonoUno is a Sonification Software for astronomical data in two column files. \n\nThis software is being developed by Bioing. Johanna Casado on her PhD tesis framework, under direction of Dr. Beatriz García. With general collaboration of Dr. Wanda Diaz Merced, and the collaboration on software development of Aldana Palma and Bioing. Julieta Carricondo Robino.\n\nThe email contact of the SonoUno team is: sonounoteam@gmail.com"
#        wx.MessageBox(message, 'Information', wx.OK | wx.ICON_INFORMATION)
#
#    def _eventmanual( self, event ):
#        message = "The user manual of the software is located in the software root folder in PDF format, or in the next link (copy and paste on the browser): \n"
#        url = "https://docs.google.com/document/d/11_mTYgqX7OdgvkuxYaXB6G3Hd4U0YRFLd9mjISAO688/edit?usp=sharing"
#        dialogs.scrolledMessageDialog(parent=self, message=message+url, title='Information', pos=wx.DefaultPosition, size=(500, 150))


# if __name__ == "__main__":
#     app = wx.App()
#     frame = SonoUnoCore()
#     frame.Show()
#     app.MainLoop()