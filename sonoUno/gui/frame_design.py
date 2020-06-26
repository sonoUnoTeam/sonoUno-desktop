#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Dec 12 2017

@author: sonounoteam (view licence)
"""

import wx
import wx.stc
import wx.xrc
import wx.grid
from wx import py
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np


EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'

class DataTable(wx.grid.GridTableBase):
    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)
        self.headerRows = 1
        if data is None:
            data = pd.DataFrame()
        self.data = data

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data.columns) + 1

    def GetValue(self, row, col):
        if col == 0:
            return self.data.index[row]
        return self.data.iloc[row, col - 1]

    def SetValue(self, row, col, value):
        self.data.iloc[row, col - 1] = value

    def GetColLabelValue(self, col):
        if col == 0:
            if self.data.index.name is None:
                return 'Index'
            else:
                return self.data.index.name
        return str(self.data.columns[col - 1])

    def GetTypeName(self, row, col):
        return wx.grid.GRID_VALUE_STRING

    def GetAttr(self, row, col, prop):
        attr = wx.grid.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)
        return attr


class FrameDesign( wx.Frame ):


    def __init__(self):

        """
        This class generate the framework of the software using wxPython. This
        is only the design, the functionalities are programmed in sonouno.py
        """
        # Create principal frame
        wx.Frame.__init__(self,
            parent = None,
            id = -1,
            title = u'SonoUno',
            pos = (1, 1),
            size=(850, 550),
            style = (wx.CAPTION | wx.DEFAULT_FRAME_STYLE | wx.SYSTEM_MENU
                | wx.TAB_TRAVERSAL)
            )
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        # Create the menu bar
        self._createmenubar()
        # Create status bar
        self._statusbar = self.CreateStatusBar(
            number = 1,
            style = 0,
            id = wx.ID_ANY,
            name = 'Status Bar'
            )
        self._statusbar.SetStatusText('')
        # Create the principal sizer
        _mainsizer = wx.BoxSizer(wx.VERTICAL)
        # Create the main panel, this panel contain scroll bars.
        self._mainscrolledwindow = wx.ScrolledWindow(
            parent = self,
            id = wx.ID_ANY,
            pos = wx.DefaultPosition,
            size = wx.DefaultSize,
            style = wx.HSCROLL | wx.VSCROLL | wx.TAB_TRAVERSAL,
            name = 'Principal scrolled window.'
            )
        self._mainscrolledwindow.SetScrollRate(5, 5)
        # Create the sizer of _mainscrolledwindow -> row(1) col(2),
        # divided in left and right. The right column is growable.
        _mainfgsizer = wx.FlexGridSizer(
            rows = 1,
            cols = 2,
            vgap = 0,
            hgap = 0
            )
        _mainfgsizer.AddGrowableCol(1)
        _mainfgsizer.AddGrowableRow(0)
        _mainfgsizer.SetFlexibleDirection(wx.BOTH)

        # Create the left panel with its sizer -> row(2) cols(1).
        self._leftpanel = wx.Panel(
            parent = self._mainscrolledwindow,
            id = wx.ID_ANY,
            pos = wx.DefaultPosition,
            size = wx.DefaultSize,
            style = wx.TAB_TRAVERSAL,
            name = 'Left panel contain file and configurations \
                functionalities.'
            )
        _mainleftsizer = wx.FlexGridSizer(
            rows = 2,
            cols = 1,
            vgap = 0,
            hgap = 0
            )
        _mainleftsizer.SetFlexibleDirection(wx.BOTH)
        # Create the file panel with its own method.
        self._filepanel = self._createfilepanel(self._leftpanel)
        _mainleftsizer.Add(
            window = self._filepanel,
            proportion = 1,
            flag = wx.EXPAND | wx.ALL,
            border = 5
            )
        self._filepanel.Hide()
        # Create the configuration panel with its own method.
        self._congifpanel = self._createconfigpanel(self._leftpanel)
        _mainleftsizer.Add(
            window = self._congifpanel,
            proportion = 1,
            flag = wx.EXPAND | wx.ALL,
            border = 5
            )
        self._congifpanel.Hide()
        self._leftpanel.SetSizer(_mainleftsizer)
        self._leftpanel.Layout()
        _mainleftsizer.Fit(self._leftpanel)
        _mainfgsizer.Add(
            window = self._leftpanel,
            proportion = 1,
            flag = wx.EXPAND | wx.ALL,
            border = 5
            )

        # Create the right panel with its sizer -> row(2) col(1),
        # the first box is growable.
        self._rightpanel = wx.Panel(
            parent = self._mainscrolledwindow,
            id = wx.ID_ANY,
            pos = wx.DefaultPosition,
            size = wx.DefaultSize,
            style = wx.TAB_TRAVERSAL,
            name = 'Right panel contain the plot, display functionalities,\
                octave and predefined mathematical functions.'
            )
        self._mainrightsizer = wx.FlexGridSizer(
            rows = 2,
            cols = 1,
            vgap = 0,
            hgap = 0
            )
        self._mainrightsizer.AddGrowableCol(0)
        self._mainrightsizer.AddGrowableRow(0)
        self._mainrightsizer.SetFlexibleDirection(wx.BOTH)
        # Create the display panel
        self._displaypanel = self._createdisplaypanel(self._rightpanel)
        self._mainrightsizer.Add(
            window = self._displaypanel,
            proportion = 1,
            flag = wx.EXPAND | wx.ALL,
            border = 5
            )
        # Create the operation panel
        self._operationpanel = self._createoperationpanel(self._rightpanel)
        self._mainrightsizer.Add(
            window = self._operationpanel,
            proportion = 1,
            flag = wx.ALL | wx.EXPAND,
            border = 5
            )
        #self._operationpanel.Hide()
        self._rightpanel.SetSizer(self._mainrightsizer)
        self._rightpanel.Layout()
        self._mainrightsizer.Fit(self._rightpanel)
        _mainfgsizer.Add(
            self._rightpanel,
            1,
            wx.EXPAND | wx.ALL,
            5
            )

        self._mainscrolledwindow.SetSizer(_mainfgsizer)
        self._mainscrolledwindow.Layout()
        _mainfgsizer.Fit(self._mainscrolledwindow)
        _mainsizer.Add(
            window = self._mainscrolledwindow,
            proportion = 1,
            flag = wx.EXPAND | wx.ALL,
            border = 5
            )
        self.SetSizer(_mainsizer)
        self.Layout()
        self.Centre(wx.BOTH)

        # Create the shortcut key table, here the buttons and functions not
        # set on the menu bar can be added.
        # self.shortcuttable = wx.AcceleratorTable(
        #     [(wx.ACCEL_NORMAL, wx.WXK_SPACE, self._playmenuitem.GetId())]
        #     )
        # self.SetAcceleratorTable(self.shortcuttable)
        #This are commented, we decide change the shortcut

    def _createmenubar(self):

        """
        This method design the sonouno menu bar, this bar contain 6 items:
        File, Data display, Data operations, Panels, Setting and Help.
        """
        # Create the menuBar
        self._menubar = wx.MenuBar(style = 0)
        # Create the menu item File
        self._menufile = wx.Menu()
        # Create the menu item open and append it to file menu
        self._openmenuitem = wx.MenuItem(
            parentMenu = self._menufile,
            id = wx.ID_ANY,
            text = ('&Open' + '\t' + 'Ctrl+Alt+O'),
            helpString = ('Open a window where you can search the data file '
                + 'on the operative system.'),
            kind = wx.ITEM_NORMAL
            )
        self._menufile.Append(self._openmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventopen,
            id = self._openmenuitem.GetId()
            )
        # Create the delete all marks menu item and append it to file menu
        self._deleteallmarksmenuitem = wx.MenuItem(
            parentMenu = self._menufile,
            id = wx.ID_ANY,
            text = ('D&elete all marks' + '\t' + 'Ctrl+Alt+E'),
            helpString = ('Delete all the marks on the data without save.'),
            kind = wx.ITEM_NORMAL
            )
        self._menufile.Append(self._deleteallmarksmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventdeleteallmark,
            id = self._deleteallmarksmenuitem.GetId()
            )
        # Create the submenu save
        self._savesubmenu = wx.Menu()
        # Create the save data menu item and append it to save submenu
        self._savedatamenuitem = wx.MenuItem(
            parentMenu = self._savesubmenu,
            id = wx.ID_ANY,
            text = ('S&ave Data' + '\t' + 'Ctrl+Alt+A'),
            helpString = ('Save the data with the modifications done by the '
                + 'user.'),
            kind = wx.ITEM_NORMAL
            )
        self._savesubmenu.Append(self._savedatamenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsavedata,
            id = self._savedatamenuitem.GetId()
            )
        #Create the save marks menu item and append it to save submenu
        self._savemarksmenuitem = wx.MenuItem(
            parentMenu = self._savesubmenu,
            id = wx.ID_ANY,
            text = ('Save &Marks' + '\t' + 'Ctrl+Alt+M'),
            helpString = ('Save the marks made by the user.'),
            kind = wx.ITEM_NORMAL
            )
        self._savesubmenu.Append(self._savemarksmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsavemarks,
            id = self._savemarksmenuitem.GetId()
            )
        # Create the save sound menu item and append it to save submenu
        self._savesoundmenuitem = wx.MenuItem(
            parentMenu = self._savesubmenu,
            id = wx.ID_ANY,
            text = ('Save &Sound' + '\t' + 'Ctrl+Alt+S'),
            helpString = ('Save the sound performed with the data opened.'),
            kind = wx.ITEM_NORMAL
            )
        self._savesubmenu.Append(self._savesoundmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsavesound,
            id = self._savesoundmenuitem.GetId()
            )
        # Create the save plot menu item and append it to save submenu
        self._saveplotmenuitem = wx.MenuItem(
            parentMenu = self._savesubmenu,
            id = wx.ID_ANY,
            text = ('Save &Plot' + '\t' + 'Ctrl+Alt+P'),
            helpString = ('Save the plot performed with the data opened.'),
            kind = wx.ITEM_NORMAL
            )
        self._savesubmenu.Append(self._saveplotmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsaveplot,
            id = self._saveplotmenuitem.GetId()
            )
        # Append the save submenu to the file menu
        self._menufile.AppendSubMenu(
            submenu = self._savesubmenu,
            text = 'Save',
            help = ('Show the things you can save on the application.')
            )
        # Create the close item Close and append it to file menu
        self._closemenuitem = wx.MenuItem(
            parentMenu = self._menufile,
            id = wx.ID_ANY,
            text = ('&Quit' + '\t' + 'Ctrl+Alt+Q'),
            helpString = ('Close the application.'),
            kind = wx.ITEM_NORMAL
            )
        self._menufile.Append(self._closemenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._onclose,
            id = self._closemenuitem.GetId()
            )
        self.Bind(
            event = wx.EVT_CLOSE,
            handler = self._eventclose
            )
        # Append file menu to menu bar
        self._menubar.Append(
            menu = self._menufile,
            title = 'File'
            )

        # Create data display menu
        self._menudisplay = wx.Menu()
        # Create the abscissa position menu item and append it to data
        # display menu
        self._absposmenuitem = wx.MenuItem(
            parentMenu = self._menudisplay,
            id = wx.ID_ANY,
            text = ('Abscissa Position (&x)' + '\t' + 'Alt+Shift+X'),
            helpString = ('Set the keyboard focus on the abscissa slider '
                + 'text label.'),
            kind = wx.ITEM_NORMAL
            )
        self._menudisplay.Append(self._absposmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventabsposselect,
            id = self._absposmenuitem.GetId()
            )
        # Create the tempo menu item and append it to data display menu
        self._tempomenuitem = wx.MenuItem(
            parentMenu = self._menudisplay,
            id = wx.ID_ANY,
            text = ('&Tempo' + '\t' + 'Alt+Shift+T'),
            helpString = ('Set the keyboard focus on the tempo slider text '
                + 'label.'),
            kind = wx.ITEM_NORMAL
            )
        self._menudisplay.Append(self._tempomenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventtemposelect,
            id = self._tempomenuitem.GetId()
            )
        # Create the play menu item and append it to data display menu
        self._playmenuitem = wx.MenuItem(
            parentMenu = self._menudisplay,
            id = wx.ID_ANY,
            text = ('Play' + '\t' + 'Alt+Shift+P'),
            helpString = ('Start the reproduction of the sonifyed data.'),
            kind = wx.ITEM_CHECK
            )
        self._menudisplay.Append(self._playmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventplay,
            id = self._playmenuitem.GetId()
            )
        # Create the stop menu item and append it to data display menu
        self._stopmenuitem = wx.MenuItem(
            parentMenu = self._menudisplay,
            id = wx.ID_ANY,
            text = ('&Stop' + '\t' + 'Alt+Shift+S'),
            helpString = ('Stop the sound.'),
            kind = wx.ITEM_NORMAL
            )
        self._menudisplay.Append(self._stopmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventstop,
            id = self._stopmenuitem.GetId()
            )
        # Create the mark point menu item and append it to data display menu
        self._markmenuitem = wx.MenuItem(
            parentMenu = self._menudisplay,
            id = wx.ID_ANY,
            text = ('&Mark Point' + '\t' + 'Alt+Shift+M'),
            helpString = ('Mark a point on the current position of the data.'),
            kind = wx.ITEM_NORMAL
            )
        self._menudisplay.Append(self._markmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventmarkpoint,
            id = self._markmenuitem.GetId()
            )
        # Create the delete last mark menu item and append it to data display
        # menu.
        self._deletelastmarkmenuitem = wx.MenuItem(
            parentMenu = self._menudisplay,
            id = wx.ID_ANY,
            text = ('&Delete last mark' + '\t' + 'Alt+Shift+D'),
            helpString = ('Delete the last mark plotted on the data.'),
            kind = wx.ITEM_NORMAL
            )
        self._menudisplay.Append(self._deletelastmarkmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventdeletelastmark,
            id = self._deletelastmarkmenuitem.GetId()
            )
        # Append the data display menu to the menu bar
        self._menubar.Append(
            menu = self._menudisplay,
            title = 'Data Display'
            )

        # Create the data operations menu
        self._menudataop = wx.Menu()
        # # Create the vertical limit submenu
        # self._vertlimitsubmenu = wx.Menu()
        # # Create the lower limit menu item and append it to vertical limit
        # # submenu
        # self._vlowerlimitmenuitem = wx.MenuItem(
        #     parentMenu = self._vertlimitsubmenu,
        #     id = wx.ID_ANY,
        #     text = ('Lower Limit' + '\t' + 'Alt+Shift+V'),
        #     helpString = ('Set the focus keyboard on the text label of'
        #         + ' lower vertical limit slider.'),
        #     kind = wx.ITEM_NORMAL
        #     )
        # self._vertlimitsubmenu.Append(self._vlowerlimitmenuitem)
        # self.Bind(
        #     event = wx.EVT_MENU,
        #     handler = self._eventvlowerlimitselect,
        #     id = self._vlowerlimitmenuitem.GetId()
        #     )
        # # Create the upper limit menu item and append it to vertical limit
        # # submenu
        # self._vupperlimitmenuitem = wx.MenuItem(
        #     parentMenu = self._vertlimitsubmenu,
        #     id = wx.ID_ANY,
        #     text = ('Upper Limit' + '\t' + 'Alt+Shift+V'),
        #     helpString = ('Set focus keyboard on the text label of upper '
        #         + 'vertical limit slider.'),
        #     kind = wx.ITEM_NORMAL
        #     )
        # self._vertlimitsubmenu.Append(self._vupperlimitmenuitem)
        # self.Bind(
        #     event = wx.EVT_MENU,
        #     handler = self._eventvupperlimitselect,
        #     id = self._vupperlimitmenuitem.GetId()
        #     )
        # # Append vertical limit submenu to data operations menu
        # self._menudataop.AppendSubMenu(
        #     menu = self._vertlimitsubmenu,
        #     title = 'Vertical Limit',
        #     help = 'Show the vertical limits items.'
        #     )
        # Create horizontal limit submenu
        self._horilimitsubmenu = wx.Menu()
        # Create the lower limit menu item and append it to horizontal limit
        # submenu
        self._hlowerlimitmenuitem = wx.MenuItem(
            parentMenu = self._horilimitsubmenu,
            id = wx.ID_ANY,
            text = ('Lower Limit' + '\t' + 'Alt+Shift+H'),
            helpString = ('Set focus keyboard on the text label of lower'
                + ' horizontal limit slider.'),
            kind = wx.ITEM_NORMAL
            )
        self._horilimitsubmenu.Append(self._hlowerlimitmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventhlowerlimitselect,
            id = self._hlowerlimitmenuitem.GetId()
            )
        # Create the upper limit menu item and append it to horizontal limit
        # submenu
        self._hupperlimitmenuitem = wx.MenuItem(
            parentMenu = self._horilimitsubmenu,
            id = wx.ID_ANY,
            text = ('Upper Limit' + '\t' + 'Alt+Shift+H'),
            helpString = ('Set focus keyboard on the text label of upper '
                + 'horizontal limit slider'),
            kind = wx.ITEM_NORMAL
            )
        self._horilimitsubmenu.Append(self._hupperlimitmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventhupperlimitselect,
            id = self._hupperlimitmenuitem.GetId()
            )
        # Append horizontal limit submenu to data operations menu
        self._menudataop.AppendSubMenu(
            submenu = self._horilimitsubmenu,
            text = 'Horizontal Limit',
            help = 'Show the horizontal limits items.'
            )
        # Create the mathematical functions submenu
        self._matfuncsubmenu = wx.Menu()
        # Create original menu item and append it to mathematical functions
        # submenu
        self._originalmfmenuitem = wx.MenuItem(
            parentMenu = self._matfuncsubmenu,
            id = wx.ID_ANY,
            text = ('&Original' + '\t' + 'Alt+Shift+O'),
            helpString = ('Plot the original data on the graph section.'),
            kind = wx.ITEM_NORMAL
            )
        self._matfuncsubmenu.Append(self._originalmfmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventoriginalmf,
            id = self._originalmfmenuitem.GetId()
            )
        # Create last cut menu item and append it to mathematical functions
        # submenu.
        self._lastcutmfmenuitem = wx.MenuItem(
            parentMenu = self._matfuncsubmenu,
            id = wx.ID_ANY,
            text = ('Previous &Cut' + '\t' + 'Alt+Shift+C'),
            helpString = ('Plot the previous cutted data on the graph '
                + 'section.'),
            kind = wx.ITEM_NORMAL
            )
        self._matfuncsubmenu.Append(self._lastcutmfmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventlastcutmf,
            id = self._lastcutmfmenuitem.GetId()
            )
        # Create the inverse menu item and append it to mathematical functions
        # submenu
        self._inversemfmenuitem = wx.MenuItem(
            parentMenu = self._matfuncsubmenu,
            id = wx.ID_ANY,
            text = ('&Inverse' + '\t' + 'Alt+Shift+I'),
            helpString = 'Invert the y axis on the plot.',
            kind = wx.ITEM_NORMAL
            )
        self._matfuncsubmenu.Append(self._inversemfmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventinversemf,
            id = self._inversemfmenuitem.GetId()
            )
        # Create the square menu item and append it to mathematical functions
        # submenu
        self._squaremfmenuitem = wx.MenuItem(
            parentMenu = self._matfuncsubmenu,
            id = wx.ID_ANY,
            text = ('Square'+ '\t' + 'Alt+Shift+2'),
            helpString = ('Perform the square function to the data and plot '
                + 'the results on the graph section.'),
            kind = wx.ITEM_NORMAL
            )
        self._matfuncsubmenu.Append(self._squaremfmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsquaremf,
            id = self._squaremfmenuitem.GetId()
            )
        # Create the square root menu item and append it to mathematical
        # functions submenu
        self._squarerootmfmenuitem = wx.MenuItem(
            parentMenu = self._matfuncsubmenu,
            id = wx.ID_ANY,
            text = ('Square root' + '\t' + 'Alt+Shift+R'),
            helpString = ('Perform the square root function to the data and '
                + 'plot the results on the graph section.'),
            kind = wx.ITEM_NORMAL
            )
        self._matfuncsubmenu.Append(self._squarerootmfmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsquarerootmf,
            id = self._squarerootmfmenuitem.GetId()
            )
        # Create the logarithm menu item and append it to mathematical
        # functions submenu
        self._logmfmenuitem = wx.MenuItem(
            parentMenu = self._matfuncsubmenu,
            id = wx.ID_ANY,
            text = ('Logarithm' + '\t' + 'Alt+Shift+L'),
            helpString = ('Perform the logarithm function to the data and '
                + 'plot the results on the graph section.'),
            kind = wx.ITEM_NORMAL
            )
        self._matfuncsubmenu.Append(self._logmfmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventlogmf,
            id = self._logmfmenuitem.GetId()
            )
        # Create the octave menu item and append it to mathematical functions
        # submenu
        self._octavemenuitem = wx.MenuItem(
            parentMenu = self._matfuncsubmenu,
            id = wx.ID_ANY,
            text = ('Octave' + '\t' + 'Alt+Shift+Y'),
            helpString = ('Enable the octave panel and set the keyboard focus '
                + 'on the octave commands text label.'),
            kind = wx.ITEM_NORMAL
            )
        self._matfuncsubmenu.Append(self._octavemenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventoctaveselect,
            id = self._octavemenuitem.GetId()
            )
        # Create the average submenu
        self._averagesubmenu = wx.Menu()
        # Create the number of points menu item and append it to average
        # submenu
        self._avnumpointmenuitem = wx.MenuItem(
            parentMenu = self._averagesubmenu,
            id = wx.ID_ANY,
            text = ('Number of points' + '\t' + 'Alt+Shift+N'),
            helpString = ('Enable the panel and the element to set the number'
                + ' of points to apply the average function.'),
            kind = wx.ITEM_NORMAL
            )
        self._averagesubmenu.Append(self._avnumpointmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventavnumpointselect,
            id = self._avnumpointmenuitem.GetId()
            )
        # Create the apply average menu item and append it to average submenu
        self._averagemfmenuitem = wx.MenuItem(
            parentMenu = self._averagesubmenu,
            id = wx.ID_ANY,
            text = ('Apply average' + '\t' + 'Alt+Shift+A'),
            helpString = ('Enable the panel and the element to set the number'
                + ' of points to apply the average function.'),
            kind = wx.ITEM_NORMAL
            )
        self._averagesubmenu.Append(self._averagemfmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventaveragemf,
            id = self._averagemfmenuitem.GetId()
            )
        # Append the average submenu to mathematical functions submenu
        self._matfuncsubmenu.AppendSubMenu(
            submenu = self._averagesubmenu,
            text = 'Average',
            help = ('Show the items to set the number of points and apply '
                + 'the average function.')
            )
        # Append the mathematical functions submenu to data operations menu.
        self._menudataop.AppendSubMenu(
            submenu = self._matfuncsubmenu,
            text = 'Mathematical Functions',
            help = ('Show the items to apply predefined mathematical '
                + 'functions.')
            )
        # Append the data operations menu to the menu bar
        self._menubar.Append(
            menu = self._menudataop,
            title = 'Data Operations'
            )
        # Create the panels menu
        self._menuconfigpanels = wx.Menu()
        # Create the file menu item and append it to panels menu
        self._cpfilemenuitem = wx.MenuItem(
            parentMenu = self._menuconfigpanels,
            id = wx.ID_ANY,
            text = ('File' + '\t' + 'Ctrl+Alt+F'),
            helpString = ('Enable the file panel, which contain the file menu'
                + ' elements.'),
            kind = wx.ITEM_CHECK
            )
        self._menuconfigpanels.Append(self._cpfilemenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpfileselect,
            id = self._cpfilemenuitem.GetId()
            )
        # Create the data display menu item and append it to panels menu
        self._cpdatadisplaymenuitem = wx.MenuItem(
            parentMenu = self._menuconfigpanels,
            id = wx.ID_ANY,
            text = ('Data Display' + '\t' + 'Ctrl+Alt+D'),
            helpString = ('Enable the display panel, which contain the plot '
                + 'and the reproduction buttons.'),
            kind = wx.ITEM_CHECK
            )
        self._menuconfigpanels.Append(self._cpdatadisplaymenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpdatadisplayselect,
            id = self._cpdatadisplaymenuitem.GetId()
            )
        self._cpdatadisplaymenuitem.Check(True)
        # Create the data parameters menu item and append it to panels menu
        self._cpdataparamplotmenuitem = wx.MenuItem(
            parentMenu = self._menuconfigpanels,
            id = wx.ID_ANY,
            text = ('Data Parameters' + '\t' + 'Alt+Shift+G'),
            helpString = ('Enable the data parameters panel.'),
            kind = wx.ITEM_CHECK
            )
        self._menuconfigpanels.Append(self._cpdataparamplotmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpdataparamplot,
            id = self._cpdataparamplotmenuitem.GetId()
            )
        # Create data operations submenu
        self._cpdataopsubmenu = wx.Menu()
        # Create all data operations submenu and append it to data operations
        # submenu
        self._cpdataopmenuitem = wx.MenuItem(
            parentMenu = self._cpdataopsubmenu,
            id = wx.ID_ANY,
            text = ('All Data Operations'+ '\t' + 'Ctrl+Alt+T'),
            helpString = ('Enable the data operation panel, which contain '
                + 'octave, cut sliders and mathematical functions panels.'),
            kind = wx.ITEM_CHECK
            )
        self._cpdataopsubmenu.Append(self._cpdataopmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpdataopselect,
            id = self._cpdataopmenuitem.GetId()
            )
        # Create write funtionalities menu item and append it to data operation submenu
        self._cpdo_writecommandmenuitem = wx.MenuItem(
            parentMenu = self._cpdataopsubmenu,
            id = wx.ID_ANY,
            text = ('Write functionalities' + '\t' + ''),
            helpString = 'Enable the write command panel.',
            kind = wx.ITEM_CHECK
            )
        self._cpdataopsubmenu.Append(self._cpdo_writecommandmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpdo_writecommandselect,
            id = self._cpdo_writecommandmenuitem.GetId()
            )
        self._cpdo_writecommandmenuitem.Check(True)
        # Create octave menu item and append it to data operation submenu
        self._cpdooctavemenuitem = wx.MenuItem(
            parentMenu = self._cpdataopsubmenu,
            id = wx.ID_ANY,
            text = ('Octave' + '\t' + 'Alt+Shift+Y'),
            helpString = 'Enable the octave panel.',
            kind = wx.ITEM_CHECK
            )
        self._cpdataopsubmenu.Append(self._cpdooctavemenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpdooctaveselect,
            id = self._cpdooctavemenuitem.GetId()
            )
        # Create slider and mathematical functions menu item and append it to
        # data operations submenu
        self._cpdocutslidermenuitem = wx.MenuItem(
            parentMenu = self._cpdataopsubmenu,
            id = wx.ID_ANY,
            text = ('Sliders and Mathematical Functions' + '\t'
                + 'Ctrl+Alt+X'),
            helpString = ('Enable the cut sliders and mathematical functions '
                + 'panel.'),
            kind = wx.ITEM_CHECK
            )
        self._cpdataopsubmenu.Append(self._cpdocutslidermenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpdocutsliderselect,
            id = self._cpdocutslidermenuitem.GetId()
            )
        # Append data operation submenu to panels menu
        self._menuconfigpanels.AppendSubMenu(
            submenu = self._cpdataopsubmenu,
            text = 'Data Operations',
            help = 'Contain octave and mathematical functions panels items.'
            )
        # Create configuration submenu
        self._cpconfigsubmenu = wx.Menu()
        # Create all configurations menu item and append it to configuration
        # submenu
        self._cpcallmenuitem = wx.MenuItem(
            parentMenu = self._cpconfigsubmenu,
            id = wx.ID_ANY,
            text = ('All configurations' + '\t' + 'Ctrl+Alt+C'),
            helpString = 'Enable sound and plot configurations panels.',
            kind = wx.ITEM_CHECK
            )
        self._cpconfigsubmenu.Append(self._cpcallmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpcallselect,
            id = self._cpcallmenuitem.GetId()
            )
        # Create sound configurations menu item and append it to configurations
        # submenu
        self._cpconfigsoundmenuitem = wx.MenuItem(
            parentMenu = self._cpconfigsubmenu,
            id = wx.ID_ANY,
            text = ('Sound Configurations' + '\t' + 'Ctrl+Alt+L'),
            helpString = 'Enable sound configurations panel.',
            kind = wx.ITEM_CHECK
            )
        self._cpconfigsubmenu.Append(self._cpconfigsoundmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpconfigsoundselect,
            id = self._cpconfigsoundmenuitem.GetId()
            )
        # Create special sound configurations menu item and append it to
        # configurations submenu
        # self._cpspecialconfigsoundmenuitem = wx.MenuItem(
        #     parentMenu = self._cpconfigsubmenu,
        #     id = wx.ID_ANY,
        #     text = ('Special Sound Configurations' + '\t' + 'Ctrl+Alt+1'),
        #     helpString = 'Enable special sound configurations panel.',
        #     kind = wx.ITEM_CHECK
        #     )
        # self._cpconfigsubmenu.Append(self._cpspecialconfigsoundmenuitem)
        # self.Bind(
        #     event = wx.EVT_MENU,
        #     handler = self._eventSpecialSoundConfig,
        #     id = self._cpspecialconfigsoundmenuitem.GetId()
        #     )
        # Create plot configurations menu item and append it to configurations
        # submenu
        self._cpconfigplotmenuitem = wx.MenuItem(
            parentMenu = self._cpconfigsubmenu,
            id = wx.ID_ANY,
            text = ('Plot Configurations' + '\t' + 'Ctrl+Alt+G'),
            helpString = 'Enable plot configurations panel.',
            kind = wx.ITEM_CHECK
            )
        self._cpconfigsubmenu.Append(self._cpconfigplotmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpconfigplotselect,
            id = self._cpconfigplotmenuitem.GetId()
            )
        # Create visual configurations menu item and append it to
        # configuration submenu (this part is not implemented yet)
        self._cpconfigvisualmenuitem = wx.MenuItem(
            parentMenu = self._cpconfigsubmenu,
            id = wx.ID_ANY,
            text = ('Visual configuratons' + '\t' + 'Ctrl+Alt+V'),
            helpString = 'Enable visual configurations panel.',
            kind = wx.ITEM_CHECK
            )
        # self._cpconfigsubmenu.Append(self._cpconfigvisualmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcpconfigvisualselect,
            id = self._cpconfigvisualmenuitem.GetId()
            )
        # Append configuration submenu to panels menu
        self._menuconfigpanels.AppendSubMenu(
            submenu = self._cpconfigsubmenu,
            text = 'Configuration',
            help = 'Contain sound and plot configurations items.'
            )
        # Append panels menu to menu bar
        self._menubar.Append(
            menu = self._menuconfigpanels,
            title = 'Panels'
            )

        # Create settings menu
        self._menusettings = wx.Menu()
        # Create sound submenu
        self._soundsubmenu = wx.Menu()
        # Create volume menu item and append it to sound submenu
        self._ssvolumemenuitem = wx.MenuItem(
            parentMenu = self._soundsubmenu,
            id = wx.ID_ANY,
            text = 'Set Volume',
            helpString = ('Set the keyboard focus on volume slider text '
                + 'label.'),
            kind = wx.ITEM_NORMAL
            )
        self._soundsubmenu.Append(self._ssvolumemenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventssvolumeselect,
            id = self._ssvolumemenuitem.GetId()
            )
        #Create linear vs log sound scale menu items
        self._slinscale_menuitem = wx.MenuItem(
            parentMenu = self._soundsubmenu,
            id = wx.ID_ANY,
            text = 'Linear scale',
            helpString = ('Set linear sound scale for the data sonification.'),
            kind = wx.ITEM_CHECK
            )
        self._soundsubmenu.Append(self._slinscale_menuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventlinsoundscalechoice,
            id = self._slinscale_menuitem.GetId()
            )
        self._slinscale_menuitem.Check()
        #Create linear vs log sound scale menu items
        self._slogscale_menuitem = wx.MenuItem(
            parentMenu = self._soundsubmenu,
            id = wx.ID_ANY,
            text = 'Logarithmic scale',
            helpString = ('Set logarithmic sound scale for the data sonification.'),
            kind = wx.ITEM_CHECK
            )
        self._soundsubmenu.Append(self._slogscale_menuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventlogsoundscalechoice,
            id = self._slogscale_menuitem.GetId()
            )
        # Create cont vs disc sound menu item and append it to sound submenu
        self._scontmenuitem = wx.MenuItem(
            parentMenu = self._soundsubmenu,
            id = wx.ID_ANY,
            text = 'Continuous sound',
            helpString = ('Set continuous sound for the data sonification.'),
            kind = wx.ITEM_CHECK
            )
        self._soundsubmenu.Append(self._scontmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventcontsoundchoice,
            id = self._scontmenuitem.GetId()
            )
        # Create cont vs disc sound menu item and append it to sound submenu
        self._sdiscretemenuitem = wx.MenuItem(
            parentMenu = self._soundsubmenu,
            id = wx.ID_ANY,
            text = 'Discrete sound',
            helpString = ('Set discrete sound for the data sonification.'),
            kind = wx.ITEM_CHECK
            )
        self._soundsubmenu.Append(self._sdiscretemenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventdiscsoundchoice,
            id = self._sdiscretemenuitem.GetId()
            )
        self._sdiscretemenuitem.Check()
        # Create min frequency menu item and append it to sound submenu
        self._ssfreqmappingmenuitem = wx.MenuItem(
            parentMenu = self._soundsubmenu,
            id = wx.ID_ANY,
            text = 'Set frequency mapping',
            helpString = ('Set the keyboard focus on minimum frequency slider '
                + 'text label.'),
            kind = wx.ITEM_CHECK
            )
        self._soundsubmenu.Append(self._ssfreqmappingmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventssfreqmappingselect,
            id = self._ssfreqmappingmenuitem.GetId()
            )
        self._ssfreqmappingmenuitem.Check(True)
        # Create max frequency menu item and append it to sound submenu
        self._ssvolmappingmenuitem = wx.MenuItem(
            parentMenu = self._soundsubmenu,
            id = wx.ID_ANY,
            text = 'Set volume mapping',
            helpString = ('Set the keyboard focus on minimum volume slider '
                + 'text label.'),
            kind = wx.ITEM_CHECK
            )
        self._soundsubmenu.Append(self._ssvolmappingmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventssvolmappingselect,
            id = self._ssvolmappingmenuitem.GetId()
            )
        # Create waveform menu item and append it to sound submenu
        self._sswaveformmenuitem = wx.MenuItem(
            parentMenu = self._soundsubmenu,
            id = wx.ID_ANY,
            text = 'Select sound type',
            helpString = ('Set the keyboard focus on sound type dropdown '
                + 'element text label.'),
            kind = wx.ITEM_NORMAL
            )
        self._soundsubmenu.Append(self._sswaveformmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsswaveformselect,
            id = self._sswaveformmenuitem.GetId()
            )
        # Create special config menu item and append it to sound submenu
        self._ssspecialconfigmenuitem = wx.MenuItem(
            parentMenu = self._soundsubmenu,
            id = wx.ID_ANY,
            text = 'Sound envelope configuration',
            helpString = ('Set the keyboard focus on Sound envelope sliders '
                + 'Panel.'),
            kind = wx.ITEM_CHECK
            )
        self._soundsubmenu.Append(self._ssspecialconfigmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventSpecialSoundConfig,
            id = self._ssspecialconfigmenuitem.GetId()
            )
        # Append sound submenu to settings menu
        self._menusettings.AppendSubMenu(
            submenu = self._soundsubmenu,
            text = 'Sound',
            help = 'Contain the sound posible settings items.'
            )
        # Create plot submenu
        self._plotsubmenu = wx.Menu()
        # Create plot line style menu item and append it to plot style submenu
        self._splotlinemenuitem = wx.MenuItem(
            parentMenu = self._plotsubmenu,
            id = wx.ID_ANY,
            text = 'Plot line style',
            helpString = ('Set the keyboard focus on plot line style dropdown'
                + ' element text label.'),
            kind = wx.ITEM_NORMAL
            )
        self._plotsubmenu.Append(self._splotlinemenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsplotlineselect,
            id = self._splotlinemenuitem.GetId()
            )
        # Create plot marker style menu item and append it to plot style
        # submenu
        self._splotmarkermenuitem = wx.MenuItem(
            parentMenu = self._plotsubmenu,
            id = wx.ID_ANY,
            text = 'Plot marker style',
            helpString = ('Set the keyboard focus on plot marker style '
                + 'dropdown element text label.'),
            kind = wx.ITEM_NORMAL
            )
        self._plotsubmenu.Append(self._splotmarkermenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsplotmarkerselect,
            id = self._splotmarkermenuitem.GetId()
            )
        # Create the plot color style menu item and append it to plot style
        # submenu
        self._splotcolormenuitem = wx.MenuItem(
            parentMenu = self._plotsubmenu,
            id = wx.ID_ANY,
            text = 'Plot color style',
            helpString = ('Set the keyboard focus on plot color style '
                + 'dropdown element text label.'),
            kind = wx.ITEM_NORMAL
            )
        self._plotsubmenu.Append(self._splotcolormenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsplotcolorselect,
            id = self._splotcolormenuitem.GetId()
            )
        # Create grid option menu item and append it to plot style submenu
        self._splotgridoptionmenuitem = wx.MenuItem(
            parentMenu = self._plotsubmenu,
            id = wx.ID_ANY,
            text = 'Grid option',
            helpString = ('Set the keyboard focus on grid option check item '
                + 'text label.'),
            kind = wx.ITEM_CHECK
            )
        self._plotsubmenu.Append(self._splotgridoptionmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventsplotgridoptionselect,
            id = self._splotgridoptionmenuitem.GetId()
            )
        # Append plot style submenu to settings menu
        self._menusettings.AppendSubMenu(
            submenu = self._plotsubmenu,
            text = 'Plot Styles',
            help = 'Contain the plot style posible settings items.'
            )
        # Append setting menu to menu bar
        self._menubar.Append(
            menu = self._menusettings,
            title = 'Settings'
            )
        # Create help menu
        self._menuhelp = wx.Menu()
        # Create about menu item and append it to help menu
        self._aboutmenuitem = wx.MenuItem(
            parentMenu = self._menuhelp,
            id = wx.ID_ANY,
            text = ('About' + '\t' + 'Ctrl+Alt+H'),
            helpString = ('Show a message box with information about the '
                + 'application.'),
            kind = wx.ITEM_NORMAL
            )
        self._menuhelp.Append(self._aboutmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventabout,
            id = self._aboutmenuitem.GetId()
            )
        # Create user manual menu item and append it to help menu
        self._manualmenuitem = wx.MenuItem(
            parentMenu = self._menuhelp,
            id = wx.ID_ANY,
            text = ('User manual' + '\t' + 'Ctrl+Alt+U'),
            helpString = ('Show a message box with the location and a link '
                + 'of the user manual file.'),
            kind = wx.ITEM_NORMAL
            )
        self._menuhelp.Append(self._manualmenuitem)
        self.Bind(
            event = wx.EVT_MENU,
            handler = self._eventmanual,
            id = self._manualmenuitem.GetId()
            )
        # Append help menu to menu bar
        self._menubar.Append(
            menu = self._menuhelp,
            title = 'Help'
            )
        # Set the menu bar
        self.SetMenuBar(self._menubar)

    def _createfilepanel(self, panel):

        """
        We have to continue with the code modification from here!
        """
        #crea el panel File con su sizer(row(5)col(2)) sin seccion expandida
        filepanel = wx.Panel( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _fileFgSizer = wx.FlexGridSizer( 6, 1, 0, 0 )
        _fileFgSizer.SetFlexibleDirection( wx.BOTH )
        _fileFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
    #Crea el boton Open y lo agrega al sizer del panel File
        self._openButton = wx.Button( filepanel, wx.ID_ANY, u"&Open", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._openButton.Bind( wx.EVT_BUTTON, self._eventopen )
        _fileFgSizer.Add( self._openButton, 0, wx.ALL, 5 )
    #Crea el boton Delete all marks y lo agrega al sizer del panel File
        self._deleteAllMarksButton = wx.Button( filepanel, wx.ID_ANY, u"&Delete all marks", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._deleteAllMarksButton.Bind( wx.EVT_BUTTON, self._eventdeleteallmark )
        _fileFgSizer.Add( self._deleteAllMarksButton, 0, wx.ALL, 5 )
    #Crea el boton Save Data y lo agrega al sizer del panel File
        self._saveDataButton = wx.Button( filepanel, wx.ID_ANY, u"Save &Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._saveDataButton.Bind( wx.EVT_BUTTON, self._eventsavedata )
        _fileFgSizer.Add( self._saveDataButton, 0, wx.ALL, 5 )
    #Crea el boton Save Marks y lo agrega al sizer del panel File
        self._saveMarksButton = wx.Button( filepanel, wx.ID_ANY, u"Save &Marks", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._saveMarksButton.Bind( wx.EVT_BUTTON, self._eventsavemarks )
        _fileFgSizer.Add( self._saveMarksButton, 0, wx.ALL, 5 )
    #Crea el boton Save Sound y lo agrega al sizer del panel File
        self._saveSoundButton = wx.Button( filepanel, wx.ID_ANY, u"Save &Sound", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._saveSoundButton.Bind( wx.EVT_BUTTON, self._eventsavesound )
        _fileFgSizer.Add( self._saveSoundButton, 0, wx.ALL, 5 )
        #self._saveSoundButton.Hide()
    #Crea el boton Save Plot y lo agrega al sizer del panel File
        self._savePlotButton = wx.Button( filepanel, wx.ID_ANY, u"Save &Plot", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._savePlotButton.Bind( wx.EVT_BUTTON, self._eventsaveplot )
        _fileFgSizer.Add( self._savePlotButton, 0, wx.ALL, 5 )
    #Relaciona el sizer con el panel File y lo agrega al sizer del panel izquierdo
        filepanel.SetSizer( _fileFgSizer )
        filepanel.Layout()
        _fileFgSizer.Fit( filepanel )
        return filepanel

    def _createconfigpanel(self, panel):
        #crea el panel Configuraciones con su sizer(row(2)col(2)) sin seccion expandida
        congifpanel = wx.Panel( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _configFgSizer = wx.FlexGridSizer( 3, 2, 0, 0 )
        _configFgSizer.SetFlexibleDirection( wx.BOTH )
        _configFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
    #Crea el boton de dos estados Sound Configurations, lo setea como presionado y lo agrega al sizer del panel Configuraciones
        self._configSoundToggleBtn = wx.ToggleButton( congifpanel, wx.ID_ANY, u"Show Sound\nConfiguraton", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._configSoundToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventConfigSound )
        self._configSoundToggleBtn.SetValue( False )
        _configFgSizer.Add( self._configSoundToggleBtn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL , 5 )
    #Crea el panel para desplegar las configuraciones de sonido y su sizer(row(8)col(1)) sin seccion expandida
        self._soundFontPanel = wx.Panel(congifpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _soundFontFgSizer = wx.FlexGridSizer( 9, 1, 0, 0 )
        _soundFontFgSizer.SetFlexibleDirection( wx.BOTH )

        #Crea el espacio de texto con el label Volume y lo agrega al sizer del panel de configuración de sonido
        self._volumeTextCtrl = wx.TextCtrl( self._soundFontPanel, wx.ID_ANY, u"Volume:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._volumeTextCtrl.SetEditable(0)
        _soundFontFgSizer.Add( self._volumeTextCtrl, 0, wx.ALL, 5 )
        #Crea la slider para el volumen
        self._soundvolumnslider = wx.Slider( self._soundFontPanel, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL | wx.SL_LABELS )
        self._soundvolumnslider.Bind( wx.EVT_KEY_UP, self._eventsoundvolumn )
        self._soundvolumnslider.Bind( wx.EVT_SCROLL, self._eventsoundvolumn )
        _soundFontFgSizer.Add( self._soundvolumnslider, 0, wx.ALL|wx.EXPAND, 5 )
        
        #Crea el boton de dos estados lineal vs logaritmic scale
        self._linvslog_soundscale_togglebtn = wx.ToggleButton( self._soundFontPanel, wx.ID_ANY, u"Set logarithmic scale", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._linvslog_soundscale_togglebtn.Bind( wx.EVT_TOGGLEBUTTON, self._event_linvslog_soundscalechoice )
        self._linvslog_soundscale_togglebtn.SetValue( False )
        _soundFontFgSizer.Add( self._linvslog_soundscale_togglebtn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL , 5 )


        #Crea el boton 
        self._contdiscsoundToggleBtn = wx.ToggleButton( self._soundFontPanel, wx.ID_ANY, u"Set continuous sound", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._contdiscsoundToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventcontdiscsoundchoice )
        self._contdiscsoundToggleBtn.SetValue( False )
        _soundFontFgSizer.Add( self._contdiscsoundToggleBtn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL , 5 )


        #Genero una sizer para poner el selector y las sliders
        _mappingFgSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
        _mappingFgSizer.SetFlexibleDirection( wx.BOTH )
        
        #Check box para elegir el mapeo en frecuencia
        self._freqmappingCheckBox = wx.CheckBox(
            parent=self._soundFontPanel, 
            id=wx.ID_ANY, 
            label='Set frequency mapping',
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=0, 
            validator=wx.DefaultValidator, 
            name='This check box set the sound mapping with frequency variation.'
            )
        self._freqmappingCheckBox.Bind(
            event=wx.EVT_CHECKBOX,
            handler=self._eventfreqmapping
            )
        _mappingFgSizer.Add(
            window=self._freqmappingCheckBox,
            proportion=0,
            flag=wx.ALL,
            border=5
            )
        self._freqmappingCheckBox.SetValue(True)
        
        #Panel y sizer para setear frecuencia mínima y máxima
        #crea el panel freq mapping con su sizer(row(2)col(2)) sin seccion expandida
        self._freqmappingPanel = wx.Panel( self._soundFontPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _freqmappingFgSizer = wx.FlexGridSizer( 6, 1, 0, 0 )
        _freqmappingFgSizer.SetFlexibleDirection( wx.BOTH )

        #Crea el espacio de texto con el label frecuencia min y lo agrega al sizer del panel de configuración de sonido
        # self._soundfreqmintextctrl = wx.TextCtrl( self._freqmappingPanel, wx.ID_ANY, u"Min frequency:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        # self._soundfreqmintextctrl.SetEditable(0)
        # _freqmappingFgSizer.Add( self._soundfreqmintextctrl, 0, wx.ALL, 5 )
        
        #Crea la checkbox para la frecuencia maxima
        self._soundfreqmin_checkbox = wx.CheckBox(
            parent=self._freqmappingPanel, 
            id=wx.ID_ANY, 
            label='Set min frequency:',
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=0, 
            validator=wx.DefaultValidator, 
            name='This check box show the min frequency slider.'
            )
        self._soundfreqmin_checkbox.Bind(
            event=wx.EVT_CHECKBOX,
            handler=self._eventshow_soundfreqmin
            )
        _freqmappingFgSizer.Add(
            window=self._soundfreqmin_checkbox,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
            )
        
        #Creo panel y sizer para poder esconder la slider
        self._soundfreqmin_panel = wx.Panel( 
            parent=self._freqmappingPanel, 
            id=wx.ID_ANY, 
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=wx.TAB_TRAVERSAL 
            )
        _soundfreqmin_fgsizer = wx.FlexGridSizer(2, 1, 0, 0)
        _soundfreqmin_fgsizer.SetFlexibleDirection(wx.BOTH)
        
        
        #Crea la slider para la frecuencia
        self._soundfreqminslider = wx.Slider( self._soundfreqmin_panel, wx.ID_ANY, 400, 0, 2900, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        self._soundfreqminslider.Bind( wx.EVT_KEY_UP, self._eventsoundfreqmin )
        self._soundfreqminslider.Bind( wx.EVT_SCROLL, self._eventsoundfreqmin )
        _soundfreqmin_fgsizer.Add( self._soundfreqminslider, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea el sizer para contener las etiquetas de la slider de frecuencia
        _soundfreqminlabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _soundfreqminlabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        _soundfreqminlabelsfgsizer.AddGrowableCol(1)
        #Creo el primer label de la slider de freq
        self._minsoundfreqmintextctrl = wx.TextCtrl( self._soundfreqmin_panel, wx.ID_ANY, u"100", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._minsoundfreqmintextctrl.SetEditable(0)
        _soundfreqminlabelsfgsizer.Add( self._minsoundfreqmintextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        #Creo el segundo label de la slider de freq
        self._actualsoundfreqmintextctrl = wx.TextCtrl( self._soundfreqmin_panel, wx.ID_ANY, u"500", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._actualsoundfreqmintextctrl.SetEditable(0)
        _soundfreqminlabelsfgsizer.Add( self._actualsoundfreqmintextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        #Creo el tercer label de la slider de freq
        self._maxsoundfreqmintextctrl = wx.TextCtrl( self._soundfreqmin_panel, wx.ID_ANY, u"3000", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        self._maxsoundfreqmintextctrl.SetEditable(0)
        _soundfreqminlabelsfgsizer.Add( self._maxsoundfreqmintextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        #Relaciona el sizer con el sizer del sonido
        _soundfreqmin_fgsizer.Add( _soundfreqminlabelsfgsizer, 1, wx.EXPAND, 5 )
        
        #Relaciona el sizer con el panel
        self._soundfreqmin_panel.SetSizer( _soundfreqmin_fgsizer )
        self._soundfreqmin_panel.Layout()
        _soundfreqmin_fgsizer.Fit( self._soundfreqmin_panel )
        _freqmappingFgSizer.Add( self._soundfreqmin_panel, 1, wx.EXPAND |wx.ALL, 5 )
        self._soundfreqmin_panel.Hide()


        #Crea el espacio de texto con el label frecuencia max y lo agrega al sizer del panel de configuración de sonido
        # self._soundfreqmaxtextctrl = wx.TextCtrl( self._freqmappingPanel, wx.ID_ANY, u"Max frequency:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        # self._soundfreqmaxtextctrl.SetEditable(0)
        # _freqmappingFgSizer.Add( self._soundfreqmaxtextctrl, 0, wx.ALL, 5 )
        
        #Crea la checkbox para la frecuencia maxima
        self._soundfreqmax_checkbox = wx.CheckBox(
            parent=self._freqmappingPanel, 
            id=wx.ID_ANY, 
            label='Set max frequency:',
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=0, 
            validator=wx.DefaultValidator, 
            name='This check box show the max frequency slider.'
            )
        self._soundfreqmax_checkbox.Bind(
            event=wx.EVT_CHECKBOX,
            handler=self._eventshow_soundfreqmax
            )
        _freqmappingFgSizer.Add(
            window=self._soundfreqmax_checkbox,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
            )
        
        #Creo panel y sizer para poder esconder la slider
        self._soundfreqmax_panel = wx.Panel( 
            parent=self._freqmappingPanel, 
            id=wx.ID_ANY, 
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=wx.TAB_TRAVERSAL 
            )
        _soundfreqmax_fgsizer = wx.FlexGridSizer(2, 1, 0, 0)
        _soundfreqmax_fgsizer.SetFlexibleDirection(wx.BOTH)
        
        #Crea la slider para la frecuencia
        self._soundfreqmaxslider = wx.Slider( self._soundfreqmax_panel, wx.ID_ANY, 2500, 0, 2500, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        self._soundfreqmaxslider.Bind( wx.EVT_KEY_UP, self._eventsoundfreqmax )
        self._soundfreqmaxslider.Bind( wx.EVT_SCROLL, self._eventsoundfreqmax )
        _soundfreqmax_fgsizer.Add( self._soundfreqmaxslider, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea el sizer para contener las etiquetas de la slider de frecuencia
        _soundfreqmaxlabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _soundfreqmaxlabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        _soundfreqmaxlabelsfgsizer.AddGrowableCol(1)
        #Creo el primer label de la slider de freq
        self._minsoundfreqmaxtextctrl = wx.TextCtrl( self._soundfreqmax_panel, wx.ID_ANY, u"500", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._minsoundfreqmaxtextctrl.SetEditable(0)
        _soundfreqmaxlabelsfgsizer.Add( self._minsoundfreqmaxtextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        #Creo el segundo label de la slider de freq
        self._actualsoundfreqmaxtextctrl = wx.TextCtrl( self._soundfreqmax_panel, wx.ID_ANY, u"3000", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._actualsoundfreqmaxtextctrl.SetEditable(0)
        _soundfreqmaxlabelsfgsizer.Add( self._actualsoundfreqmaxtextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        #Creo el tercer label de la slider de freq
        self._maxsoundfreqmaxtextctrl = wx.TextCtrl( self._soundfreqmax_panel, wx.ID_ANY, u"3000", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        self._maxsoundfreqmaxtextctrl.SetEditable(0)
        _soundfreqmaxlabelsfgsizer.Add( self._maxsoundfreqmaxtextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        #Relaciona el sizer con el sizer del sonido
        _soundfreqmax_fgsizer.Add( _soundfreqmaxlabelsfgsizer, 1, wx.EXPAND, 5 )

        #Relaciona el sizer con el panel
        self._soundfreqmax_panel.SetSizer( _soundfreqmax_fgsizer )
        self._soundfreqmax_panel.Layout()
        _soundfreqmax_fgsizer.Fit( self._soundfreqmax_panel )
        _freqmappingFgSizer.Add( self._soundfreqmax_panel, 1, wx.EXPAND |wx.ALL, 5 )
        self._soundfreqmax_panel.Hide()

        #Relaciona el sizer con el panel
        self._freqmappingPanel.SetSizer( _freqmappingFgSizer )
        self._freqmappingPanel.Layout()
        _freqmappingFgSizer.Fit( self._freqmappingPanel )
        _mappingFgSizer.Add( self._freqmappingPanel, 1, wx.EXPAND |wx.ALL, 5 )
        
        #Check box para elegir el mapeo en volumen
        self._volmappingCheckBox = wx.CheckBox(
            parent=self._soundFontPanel, 
            id=wx.ID_ANY, 
            label='Set volume mapping',
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=0, 
            validator=wx.DefaultValidator, 
            name='This check box set the sound mapping with volume variation.'
            )
        self._volmappingCheckBox.Bind(
            event=wx.EVT_CHECKBOX,
            handler=self._eventvolmapping
            )
        _mappingFgSizer.Add(
            window=self._volmappingCheckBox,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
            )
        
        #Panel y sizer para setear volumen mínima y máxima
        #crea el panel vol mapping con su sizer(row(2)col(2)) sin seccion expandida
        self._volmappingPanel = wx.Panel( self._soundFontPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _volmappingFgSizer = wx.FlexGridSizer( 9, 1, 0, 0 )
        _volmappingFgSizer.SetFlexibleDirection( wx.BOTH )

        #Crea el espacio de texto con el label frecuencia para mapeo en volumen 
        #y lo agrega al sizer del panel de configuración de sonido
        # self._soundvolfreqtextctrl = wx.TextCtrl( 
        #     parent=self._volmappingPanel, 
        #     id=wx.ID_ANY, 
        #     value='Frequency of volume mapping:', 
        #     pos=wx.DefaultPosition, 
        #     size=wx.Size( 170,15 ), 
        #     style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL 
        #     )
        # self._soundvolfreqtextctrl.SetEditable(0)
        # _volmappingFgSizer.Add( self._soundvolfreqtextctrl, 0, wx.ALL, 5 )
        
        #Crea la checkbox para la variacion en freq del volumen
        self._soundvolfreq_checkbox = wx.CheckBox(
            parent=self._volmappingPanel, 
            id=wx.ID_ANY, 
            label='Set frequency of volume mapping:',
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=0, 
            validator=wx.DefaultValidator, 
            name='This check box show the frequency slider of volume mapping.'
            )
        self._soundvolfreq_checkbox.SetValue(True)
        self._soundvolfreq_checkbox.Bind(
            event=wx.EVT_CHECKBOX,
            handler=self._eventshow_soundvolfreq
            )
        _volmappingFgSizer.Add(
            window=self._soundvolfreq_checkbox,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
            )
        
        #Creo panel y sizer para poder esconder la slider
        self._soundvolfreq_panel = wx.Panel( 
            parent=self._volmappingPanel, 
            id=wx.ID_ANY, 
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=wx.TAB_TRAVERSAL 
            )
        _soundvolfreq_fgsizer = wx.FlexGridSizer(2, 1, 0, 0)
        _soundvolfreq_fgsizer.SetFlexibleDirection(wx.BOTH)
        
        
        #Crea la slider para la frecuencia del mapeo en volumen
        self._soundvolfreq_slider = wx.Slider( 
            self._soundvolfreq_panel, 
            wx.ID_ANY, 
            500, 
            0, 
            2900, 
            wx.DefaultPosition, 
            wx.DefaultSize, 
            wx.SL_HORIZONTAL 
            )
        self._soundvolfreq_slider.Bind( wx.EVT_KEY_UP, self._eventsoundvolfreq )
        self._soundvolfreq_slider.Bind( wx.EVT_SCROLL, self._eventsoundvolfreq )
        _soundvolfreq_fgsizer.Add( self._soundvolfreq_slider, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea el sizer para contener las etiquetas de la slider de frecuencia
        _soundvolfreqlabels_fgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _soundvolfreqlabels_fgsizer.SetFlexibleDirection( wx.BOTH )
        _soundvolfreqlabels_fgsizer.AddGrowableCol(1)
        #Creo el primer label de la slider de freq
        self._minsoundvolfreqtextctrl = wx.TextCtrl( self._soundvolfreq_panel, wx.ID_ANY, u"100", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._minsoundvolfreqtextctrl.SetEditable(0)
        _soundvolfreqlabels_fgsizer.Add( self._minsoundvolfreqtextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        #Creo el segundo label de la slider de freq
        self._actualsoundvolfreq_textctrl = wx.TextCtrl( self._soundvolfreq_panel, wx.ID_ANY, u"600", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._actualsoundvolfreq_textctrl.SetEditable(0)
        _soundvolfreqlabels_fgsizer.Add( self._actualsoundvolfreq_textctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        #Creo el tercer label de la slider de freq
        self._maxsoundvolfreq_textctrl = wx.TextCtrl( self._soundvolfreq_panel, wx.ID_ANY, u"3000", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        self._maxsoundvolfreq_textctrl.SetEditable(0)
        _soundvolfreqlabels_fgsizer.Add( self._maxsoundvolfreq_textctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        #Relaciona el sizer con el sizer del sonido
        _soundvolfreq_fgsizer.Add( _soundvolfreqlabels_fgsizer, 1, wx.EXPAND, 5 )
        
        #Relaciona el sizer con el panel
        self._soundvolfreq_panel.SetSizer( _soundvolfreq_fgsizer )
        self._soundvolfreq_panel.Layout()
        _soundvolfreq_fgsizer.Fit( self._soundvolfreq_panel )
        _volmappingFgSizer.Add( self._soundvolfreq_panel, 1, wx.EXPAND |wx.ALL, 5 )
        # self._soundvolfreq_panel.Hide()
        

        #Crea el espacio de texto con el label vol min y 
        # self._soundvolmintextctrl = wx.TextCtrl( 
        #     self._volmappingPanel, 
        #     wx.ID_ANY, 
        #     u"Min volume:", 
        #     wx.DefaultPosition, 
        #     wx.Size( 90,15 ), 
        #     style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL 
        #     )
        # self._soundvolmintextctrl.SetEditable(0)
        # _volmappingFgSizer.Add( self._soundvolmintextctrl, 0, wx.ALL, 5 )
        
        #Crea la checkbox para el volumen minimo
        self._soundvolmin_checkbox = wx.CheckBox(
            parent=self._volmappingPanel, 
            id=wx.ID_ANY, 
            label='Set min volume:',
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=0, 
            validator=wx.DefaultValidator, 
            name='This check box show the min volume slider.'
            )
        self._soundvolmin_checkbox.Bind(
            event=wx.EVT_CHECKBOX,
            handler=self._eventshow_soundvolmin
            )
        _volmappingFgSizer.Add(
            window=self._soundvolmin_checkbox,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
            )
        
        #Creo panel y sizer para poder esconder la slider
        self._soundvolmin_panel = wx.Panel( 
            parent=self._volmappingPanel, 
            id=wx.ID_ANY, 
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=wx.TAB_TRAVERSAL 
            )
        _soundvolmin_fgsizer = wx.FlexGridSizer(2, 1, 0, 0)
        _soundvolmin_fgsizer.SetFlexibleDirection(wx.BOTH)
        
        
        #Crea la slider para el volumen min
        self._soundvolminslider = wx.Slider( 
            self._soundvolmin_panel, 
            wx.ID_ANY, 
            0, 
            0, 
            100, 
            wx.DefaultPosition, 
            wx.DefaultSize, 
            wx.SL_HORIZONTAL 
            )
        self._soundvolminslider.Bind( wx.EVT_KEY_UP, self._eventsoundvolmin )
        self._soundvolminslider.Bind( wx.EVT_SCROLL, self._eventsoundvolmin )
        _soundvolmin_fgsizer.Add( self._soundvolminslider, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea el sizer para contener las etiquetas de la slider de volumen
        _soundvolminlabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _soundvolminlabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        _soundvolminlabelsfgsizer.AddGrowableCol(1)
        #Creo el primer label de la slider de freq
        self._minsoundvolmintextctrl = wx.TextCtrl( self._soundvolmin_panel, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._minsoundvolmintextctrl.SetEditable(0)
        _soundvolminlabelsfgsizer.Add( self._minsoundvolmintextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        #Creo el segundo label de la slider de freq
        self._actualsoundvolmintextctrl = wx.TextCtrl( self._soundvolmin_panel, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._actualsoundvolmintextctrl.SetEditable(0)
        _soundvolminlabelsfgsizer.Add( self._actualsoundvolmintextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        #Creo el tercer label de la slider de freq
        self._maxsoundvolmintextctrl = wx.TextCtrl( self._soundvolmin_panel, wx.ID_ANY, u"100", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        self._maxsoundvolmintextctrl.SetEditable(0)
        _soundvolminlabelsfgsizer.Add( self._maxsoundvolmintextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        #Relaciona el sizer con el sizer del sonido
        _soundvolmin_fgsizer.Add( _soundvolminlabelsfgsizer, 1, wx.EXPAND, 5 )
        
        #Relaciona el sizer con el panel
        self._soundvolmin_panel.SetSizer( _soundvolmin_fgsizer )
        self._soundvolmin_panel.Layout()
        _soundvolmin_fgsizer.Fit( self._soundvolmin_panel )
        _volmappingFgSizer.Add( self._soundvolmin_panel, 1, wx.EXPAND |wx.ALL, 5 )
        self._soundvolmin_panel.Hide()
        

        #Crea el espacio de texto con el label frecuencia max y lo agrega al sizer del panel de configuración de sonido
        # self._soundvolmaxtextctrl = wx.TextCtrl( self._volmappingPanel, wx.ID_ANY, u"Max volume:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        # self._soundvolmaxtextctrl.SetEditable(0)
        # _volmappingFgSizer.Add( self._soundvolmaxtextctrl, 0, wx.ALL, 5 )
        
        #Check box para elegir el volumen maximo
        self._soundvolmax_checkbox = wx.CheckBox(
            parent=self._volmappingPanel, 
            id=wx.ID_ANY, 
            label='Set max volume:', 
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=0, 
            validator=wx.DefaultValidator, 
            name='This check box show the max volume slider.'
            )
        self._soundvolmax_checkbox.Bind(
            event=wx.EVT_CHECKBOX,
            handler=self._eventshow_soundvolmax
            )
        _volmappingFgSizer.Add(
            window=self._soundvolmax_checkbox,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
            )
        
        #Creo panel y sizer para poder esconder la slider
        self._soundvolmax_panel = wx.Panel( 
            parent=self._volmappingPanel, 
            id=wx.ID_ANY, 
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=wx.TAB_TRAVERSAL 
            )
        _soundvolmax_fgsizer = wx.FlexGridSizer(2, 1, 0, 0)
        _soundvolmax_fgsizer.SetFlexibleDirection(wx.BOTH)
        
        #Crea la slider para la frecuencia
        self._soundvolmaxslider = wx.Slider( 
            self._soundvolmax_panel, 
            wx.ID_ANY, 
            100, 
            0, 
            100, 
            wx.DefaultPosition, 
            wx.DefaultSize, 
            wx.SL_HORIZONTAL 
            )
        self._soundvolmaxslider.Bind( wx.EVT_KEY_UP, self._eventsoundvolmax )
        self._soundvolmaxslider.Bind( wx.EVT_SCROLL, self._eventsoundvolmax )
        _soundvolmax_fgsizer.Add( self._soundvolmaxslider, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea el sizer para contener las etiquetas de la slider de frecuencia
        _soundvolmaxlabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _soundvolmaxlabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        _soundvolmaxlabelsfgsizer.AddGrowableCol(1)
        #Creo el primer label de la slider de freq
        self._minsoundvolmaxtextctrl = wx.TextCtrl( self._soundvolmax_panel, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._minsoundvolmaxtextctrl.SetEditable(0)
        _soundvolmaxlabelsfgsizer.Add( self._minsoundvolmaxtextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        #Creo el segundo label de la slider de freq
        self._actualsoundvolmaxtextctrl = wx.TextCtrl( self._soundvolmax_panel, wx.ID_ANY, u"100", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._actualsoundvolmaxtextctrl.SetEditable(0)
        _soundvolmaxlabelsfgsizer.Add( self._actualsoundvolmaxtextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        #Creo el tercer label de la slider de freq
        self._maxsoundvolmaxtextctrl = wx.TextCtrl( self._soundvolmax_panel, wx.ID_ANY, u"100", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        self._maxsoundvolmaxtextctrl.SetEditable(0)
        _soundvolmaxlabelsfgsizer.Add( self._maxsoundvolmaxtextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        
        #Relaciona el sizer con el sizer del sonido
        _soundvolmax_fgsizer.Add( _soundvolmaxlabelsfgsizer, 1, wx.EXPAND, 5 )
        
        #Relaciona el sizer con el panel
        self._soundvolmax_panel.SetSizer( _soundvolmax_fgsizer )
        self._soundvolmax_panel.Layout()
        _soundvolmax_fgsizer.Fit( self._soundvolmax_panel )
        _volmappingFgSizer.Add( self._soundvolmax_panel, 1, wx.EXPAND |wx.ALL, 5 )
        self._soundvolmax_panel.Hide()
        

        #Relaciona el sizer con el panel
        self._volmappingPanel.SetSizer( _volmappingFgSizer )
        self._volmappingPanel.Layout()
        _volmappingFgSizer.Fit( self._volmappingPanel )
        _mappingFgSizer.Add( self._volmappingPanel, 1, wx.EXPAND |wx.ALL, 5 )
        self._volmappingPanel.Hide()

        _soundFontFgSizer.Add( _mappingFgSizer, 0, wx.ALL , 5 )

        #Aqui abajo se pondra la forma de onda
        #Crea el espacio de texto con el label forma de onda y lo agrega al sizer del panel de configuración de sonido
        self._soundwaveformtextctrl = wx.TextCtrl( self._soundFontPanel, wx.ID_ANY, u"Select sound type:", wx.DefaultPosition, wx.Size( 130,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._soundwaveformtextctrl.SetEditable(0)
        _soundFontFgSizer.Add( self._soundwaveformtextctrl, 0, wx.ALL, 5 )
        #Crea un panel desplegable con una lista para poder seleccionar entre las formas de onda disponibles, y lo agrega al sizer del panel de configuración de sonido
        _swaveformlistboxchoices = [  ]
        self._swaveformlistbox = wx.ListBox( self._soundFontPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, _swaveformlistboxchoices, wx.LB_ALWAYS_SB )
        self._swaveformlistbox.Bind( wx.EVT_LISTBOX, self._eventswaveform )
        _soundFontFgSizer.Add( self._swaveformlistbox, 0, wx.ALL|wx.EXPAND, 5 )
        
        # Aquí se colocará el checkbox para la envolvente y el panel de la envolvente
        #Check box para elegir la envolvente
        self._envelope_checkbox = wx.CheckBox(
            parent=self._soundFontPanel, 
            id=wx.ID_ANY, 
            label='Sound envelope configuration:', 
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=0, 
            validator=wx.DefaultValidator, 
            name='This check box show the envelope panel.'
            )
        self._envelope_checkbox.Bind(
            event=wx.EVT_CHECKBOX,
            handler=self._eventshowenvelope
            )
        _soundFontFgSizer.Add(
            window=self._envelope_checkbox,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
            )
        
        #crea el panel Configuraciones especiales de sonido con su sizer(row(2)col(2)) sin seccion expandida
        #self._specialsoundcongifpanel = wx.Panel( self._soundFontPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self._specialsoundcongifpanel = wx.ScrolledWindow(
        parent = self._soundFontPanel,
        id = wx.ID_ANY,
        pos = wx.DefaultPosition,
        size = wx.DefaultSize,
        style = wx.HSCROLL | wx.VSCROLL | wx.TAB_TRAVERSAL,
        name = 'Principal scrolled window.'
        )
        _specialsoundconfigFgSizer = wx.FlexGridSizer( 14, 1, 0, 0 )
        _specialsoundconfigFgSizer.SetFlexibleDirection( wx.BOTH )
        # #Crea el label sound envelope and append it to sound font config panel
        # self._soundspecialconfigtextctrl = wx.TextCtrl(
        #     self._specialsoundcongifpanel,
        #     wx.ID_ANY,
        #     u"Sound envelop configuration:",
        #     wx.DefaultPosition,
        #     wx.Size( 160,15 ),
        #     style = wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL
        #     )
        # self._soundspecialconfigtextctrl.SetEditable(0)
        # _specialsoundconfigFgSizer.Add( self._soundspecialconfigtextctrl, 0, wx.ALL, 5 )

        #Crea el espacio de texto con el label attack y lo agrega al sizer del panel de configuración de sonido
        self._soundattacktextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"Attack:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._soundattacktextctrl.SetEditable(0)
        _specialsoundconfigFgSizer.Add( self._soundattacktextctrl, 0, wx.ALL, 5 )
        #Crea la slider para el parametro attack
        self._soundattackslider = wx.Slider( self._specialsoundcongifpanel, wx.ID_ANY, 25, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        self._soundattackslider.Bind( wx.EVT_KEY_UP, self._eventsoundattack )
        self._soundattackslider.Bind( wx.EVT_SCROLL, self._eventsoundattack )
        _specialsoundconfigFgSizer.Add( self._soundattackslider, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea el sizer para contener las etiquetas de la slider de attack
        _soundattacklabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _soundattacklabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        _soundattacklabelsfgsizer.AddGrowableCol(1)
        #Creo el primer label de la slider de attack
        self._minattacktextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.01", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._minattacktextctrl.SetEditable(0)
        _soundattacklabelsfgsizer.Add( self._minattacktextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        #Creo el segundo label de la slider de attack
        self._actualattacktextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.25", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._actualattacktextctrl.SetEditable(0)
        _soundattacklabelsfgsizer.Add( self._actualattacktextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        #Creo el tercer label de la slider de attack
        self._maxattacktextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        self._maxattacktextctrl.SetEditable(0)
        _soundattacklabelsfgsizer.Add( self._maxattacktextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        #Relaciona el sizer con el sizer del sonido
        _specialsoundconfigFgSizer.Add( _soundattacklabelsfgsizer, 1, wx.EXPAND, 5 )
        #Crea el espacio de texto con el label decay y lo agrega al sizer del panel de configuración de sonido
        self._sounddecaytextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"Decay:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._sounddecaytextctrl.SetEditable(0)
        _specialsoundconfigFgSizer.Add( self._sounddecaytextctrl, 0, wx.ALL, 5 )
        #Crea la slider para el parametro decay
        self._sounddecayslider = wx.Slider( self._specialsoundcongifpanel, wx.ID_ANY, 25, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        self._sounddecayslider.Bind( wx.EVT_KEY_UP, self._eventsounddecay )
        self._sounddecayslider.Bind( wx.EVT_SCROLL, self._eventsounddecay )
        _specialsoundconfigFgSizer.Add( self._sounddecayslider, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea el sizer para contener las etiquetas de la slider de decay
        _sounddecaylabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _sounddecaylabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        _sounddecaylabelsfgsizer.AddGrowableCol(1)
        #Creo el primer label de la slider de decay
        self._mindecaytextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.01", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._mindecaytextctrl.SetEditable(0)
        _sounddecaylabelsfgsizer.Add( self._mindecaytextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        #Creo el segundo label de la slider de decay
        self._actualdecaytextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.25", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._actualdecaytextctrl.SetEditable(0)
        _sounddecaylabelsfgsizer.Add( self._actualdecaytextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        #Creo el tercer label de la slider de decay
        self._maxdecaytextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        self._maxdecaytextctrl.SetEditable(0)
        _sounddecaylabelsfgsizer.Add( self._maxdecaytextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        #Relaciona el sizer con el sizer del sonido
        _specialsoundconfigFgSizer.Add( _sounddecaylabelsfgsizer, 1, wx.EXPAND, 5 )
        #Crea el espacio de texto con el label sustain y lo agrega al sizer del panel de configuración de sonido
        self._soundsustaintextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"Sustain:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._soundsustaintextctrl.SetEditable(0)
        _specialsoundconfigFgSizer.Add( self._soundsustaintextctrl, 0, wx.ALL, 5 )
        #Crea la slider para el parametro sustain
        self._soundsustainslider = wx.Slider( self._specialsoundcongifpanel, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        self._soundsustainslider.Bind( wx.EVT_KEY_UP, self._eventsoundsustain )
        self._soundsustainslider.Bind( wx.EVT_SCROLL, self._eventsoundsustain )
        _specialsoundconfigFgSizer.Add( self._soundsustainslider, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea el sizer para contener las etiquetas de la slider de sustain
        _soundsustainlabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _soundsustainlabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        _soundsustainlabelsfgsizer.AddGrowableCol(1)
        #Creo el primer label de la slider de sustain
        self._minsustaintextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._minsustaintextctrl.SetEditable(0)
        _soundsustainlabelsfgsizer.Add( self._minsustaintextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        #Creo el segundo label de la slider de sustain
        self._actualsustaintextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"50", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._actualsustaintextctrl.SetEditable(0)
        _soundsustainlabelsfgsizer.Add( self._actualsustaintextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        #Creo el tercer label de la slider de sustain
        self._maxsustaintextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"100", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        self._maxsustaintextctrl.SetEditable(0)
        _soundsustainlabelsfgsizer.Add( self._maxsustaintextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        #Relaciona el sizer con el sizer del sonido
        _specialsoundconfigFgSizer.Add( _soundsustainlabelsfgsizer, 1, wx.EXPAND, 5 )
        #Crea el espacio de texto con el label release y lo agrega al sizer del panel de configuración de sonido
        self._soundreleasetextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"Release:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._soundreleasetextctrl.SetEditable(0)
        _specialsoundconfigFgSizer.Add( self._soundreleasetextctrl, 0, wx.ALL, 5 )
        #Crea la slider para el parametro release
        self._soundreleaseslider = wx.Slider( self._specialsoundcongifpanel, wx.ID_ANY, 25, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        self._soundreleaseslider.Bind( wx.EVT_KEY_UP, self._eventsoundrelease )
        self._soundreleaseslider.Bind( wx.EVT_SCROLL, self._eventsoundrelease )
        _specialsoundconfigFgSizer.Add( self._soundreleaseslider, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea el sizer para contener las etiquetas de la slider de release
        _soundreleaselabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _soundreleaselabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        _soundreleaselabelsfgsizer.AddGrowableCol(1)
        #Creo el primer label de la slider de release
        self._minreleasetextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.01", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._minreleasetextctrl.SetEditable(0)
        _soundreleaselabelsfgsizer.Add( self._minreleasetextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        #Creo el segundo label de la slider de release
        self._actualreleasetextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.25", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._actualreleasetextctrl.SetEditable(0)
        _soundreleaselabelsfgsizer.Add( self._actualreleasetextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        #Creo el tercer label de la slider de release
        self._maxreleasetextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        self._maxreleasetextctrl.SetEditable(0)
        _soundreleaselabelsfgsizer.Add( self._maxreleasetextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        #Relaciona el sizer con el sizer del sonido
        _specialsoundconfigFgSizer.Add( _soundreleaselabelsfgsizer, 1, wx.EXPAND, 5 )
        
        #Crea el sizer para contener las etiquetas de la slider de attack
        _soundenvelopebuttonsfgsizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        _soundenvelopebuttonsfgsizer.SetFlexibleDirection( wx.BOTH )
        #Crea el boton de dos estados para ocultar la grafica de la envolvente
        self._envelopegraphtogglebtn = wx.ToggleButton(
            parent = self._specialsoundcongifpanel,
            id = wx.ID_ANY,
            label = 'Hide envelope\nplot',
            pos = wx.DefaultPosition,
            size = wx.DefaultSize,
            style = 0,
            name = 'Envelope plot toggle button'
            )
        self._envelopegraphtogglebtn.Bind(
            event = wx.EVT_TOGGLEBUTTON,
            handler = self._eventenvelopegraph
            )
        self._envelopegraphtogglebtn.SetValue(True)
        _soundenvelopebuttonsfgsizer.Add(
            window = self._envelopegraphtogglebtn,
            proportion = 1,
            flag = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,
            border = 5
            )
        
        #Crea el boton de dos estados para reproducir la grafica de la envolvente
        self._envelopeplaytogglebtn = wx.ToggleButton(
            parent = self._specialsoundcongifpanel,
            id = wx.ID_ANY,
            label = 'Play envelope\nsound',
            pos = wx.DefaultPosition,
            size = wx.DefaultSize,
            style = 0,
            name = 'Play/Stop envelope toggle button'
            )
        self._envelopeplaytogglebtn.Bind(
            event = wx.EVT_TOGGLEBUTTON,
            handler = self._eventenvelopeplay
            )
        self._envelopeplaytogglebtn.SetValue(False)
        _soundenvelopebuttonsfgsizer.Add(
            window = self._envelopeplaytogglebtn,
            proportion = 1,
            flag = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,
            border = 5
            )
        
        _specialsoundconfigFgSizer.Add( _soundenvelopebuttonsfgsizer, 1, wx.EXPAND, 5 )
        
        # Crea el panel para contener el grafico de la envolvente y un sizer
        # para contenerlo
        self._envelopegraphpanel = wx.Panel(
            parent = self._specialsoundcongifpanel,
            id = wx.ID_ANY,
            pos = wx.DefaultPosition,
            size = wx.Size(300,150),
            style = wx.TAB_TRAVERSAL,
            name = 'Envelope graph panel'
            )
        _envelopegraphsizer = wx.FlexGridSizer(
            rows = 1,
            cols = 1,
            vgap = 0,
            hgap = 0
            )
        _envelopegraphsizer.AddGrowableCol(0)
        _envelopegraphsizer.AddGrowableRow(0)
        _envelopegraphsizer.SetFlexibleDirection(direction = wx.BOTH)
        # Crea la figura, el canvas que la contiene y agrega un subplot llamado
        # axes que se utilizara en el codigo principal
        self._envelopefigure = Figure()
        self._axesenvelopegraph = self._envelopefigure.add_subplot(111)
        self._envelopecanvas = FigureCanvas(self._envelopegraphpanel, -1, self._envelopefigure)
        self._envelopecanvas.SetMinSize(wx.Size(10,10))
        self._envelopecanvas.SetToolTip('Displays the envelope of the sound setted by the user.')
        #Agrega el canvas que relaciona la figura con el panel al sizer del panel del grafico
        _envelopegraphsizer.Add( self._envelopecanvas, 1, wx.EXPAND |wx.ALL, 5 )
        #Relaciona el panel del grafico con su propio sizer y lo agrega al sizer del panel Display
        self._envelopegraphpanel.SetSizer( _envelopegraphsizer )
        self._envelopegraphpanel.Layout()
        _envelopegraphsizer.Fit( self._envelopegraphpanel )
        _specialsoundconfigFgSizer.Add( self._envelopegraphpanel, 1, wx.EXPAND |wx.ALL, 5 )

        #Relaciona el panel de configuraciones con su propio sizer y lo agrega al sizer del panel izquierdo
        self._specialsoundcongifpanel.SetSizer( _specialsoundconfigFgSizer )
        self._specialsoundcongifpanel.Layout()
        _specialsoundconfigFgSizer.Fit( self._specialsoundcongifpanel )
        _soundFontFgSizer.Add( self._specialsoundcongifpanel, 1, wx.EXPAND |wx.ALL, 5 )
        self._specialsoundcongifpanel.Hide()


        #Relaciona el sizer con el panel de las configuraciones de sonido y lo agrega al sizer del panel de configuraciones
        self._soundFontPanel.SetSizer( _soundFontFgSizer )
        self._soundFontPanel.Layout()
        _soundFontFgSizer.Fit( self._soundFontPanel )
        _configFgSizer.Add( self._soundFontPanel, 1, wx.EXPAND |wx.ALL, 5 )
        self._soundFontPanel.Hide()

        # #Crea el boton de dos estados para abrir el panel de configuracion
        # #especial de sonido
        # self._specialConfigSoundToggleBtn = wx.ToggleButton( congifpanel, wx.ID_ANY, u"Show Special Sound\nConfigurations", wx.DefaultPosition, wx.DefaultSize, 0 )
        # self._specialConfigSoundToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventSpecialSoundConfig )
        # self._specialConfigSoundToggleBtn.SetValue( False )
        # _configFgSizer.Add( self._specialConfigSoundToggleBtn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL , 5 )

        # #crea el panel Configuraciones especiales de sonido con su sizer(row(2)col(2)) sin seccion expandida
        # self._specialsoundcongifpanel = wx.Panel( congifpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        # _specialsoundconfigFgSizer = wx.FlexGridSizer( 15, 1, 0, 0 )
        # _specialsoundconfigFgSizer.SetFlexibleDirection( wx.BOTH )
        # _specialsoundconfigFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        # #Crea el label sound envelope and append it to sound font config panel
        # self._soundspecialconfigtextctrl = wx.TextCtrl(
        #     self._specialsoundcongifpanel,
        #     wx.ID_ANY,
        #     u"Sound envelop configuration:",
        #     wx.DefaultPosition,
        #     wx.Size( 160,15 ),
        #     style = wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL
        #     )
        # self._soundspecialconfigtextctrl.SetEditable(0)
        # _specialsoundconfigFgSizer.Add( self._soundspecialconfigtextctrl, 0, wx.ALL, 5 )

        # #Crea el espacio de texto con el label attack y lo agrega al sizer del panel de configuración de sonido
        # self._soundattacktextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"Attack:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        # self._soundattacktextctrl.SetEditable(0)
        # _specialsoundconfigFgSizer.Add( self._soundattacktextctrl, 0, wx.ALL, 5 )
        # #Crea la slider para el parametro attack
        # self._soundattackslider = wx.Slider( self._specialsoundcongifpanel, wx.ID_ANY, 25, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        # self._soundattackslider.Bind( wx.EVT_KEY_UP, self._eventsoundattack )
        # self._soundattackslider.Bind( wx.EVT_SCROLL, self._eventsoundattack )
        # _specialsoundconfigFgSizer.Add( self._soundattackslider, 0, wx.ALL|wx.EXPAND, 5 )
        # #Crea el sizer para contener las etiquetas de la slider de attack
        # _soundattacklabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        # _soundattacklabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        # _soundattacklabelsfgsizer.AddGrowableCol(1)
        # #Creo el primer label de la slider de attack
        # self._minattacktextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.01", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        # self._minattacktextctrl.SetEditable(0)
        # _soundattacklabelsfgsizer.Add( self._minattacktextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        # #Creo el segundo label de la slider de attack
        # self._actualattacktextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.25", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        # self._actualattacktextctrl.SetEditable(0)
        # _soundattacklabelsfgsizer.Add( self._actualattacktextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        # #Creo el tercer label de la slider de attack
        # self._maxattacktextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        # self._maxattacktextctrl.SetEditable(0)
        # _soundattacklabelsfgsizer.Add( self._maxattacktextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        # #Relaciona el sizer con el sizer del sonido
        # _specialsoundconfigFgSizer.Add( _soundattacklabelsfgsizer, 1, wx.EXPAND, 5 )
        # #Crea el espacio de texto con el label decay y lo agrega al sizer del panel de configuración de sonido
        # self._sounddecaytextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"Decay:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        # self._sounddecaytextctrl.SetEditable(0)
        # _specialsoundconfigFgSizer.Add( self._sounddecaytextctrl, 0, wx.ALL, 5 )
        # #Crea la slider para el parametro decay
        # self._sounddecayslider = wx.Slider( self._specialsoundcongifpanel, wx.ID_ANY, 25, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        # self._sounddecayslider.Bind( wx.EVT_KEY_UP, self._eventsounddecay )
        # self._sounddecayslider.Bind( wx.EVT_SCROLL, self._eventsounddecay )
        # _specialsoundconfigFgSizer.Add( self._sounddecayslider, 0, wx.ALL|wx.EXPAND, 5 )
        # #Crea el sizer para contener las etiquetas de la slider de decay
        # _sounddecaylabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        # _sounddecaylabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        # _sounddecaylabelsfgsizer.AddGrowableCol(1)
        # #Creo el primer label de la slider de decay
        # self._mindecaytextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.01", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        # self._mindecaytextctrl.SetEditable(0)
        # _sounddecaylabelsfgsizer.Add( self._mindecaytextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        # #Creo el segundo label de la slider de decay
        # self._actualdecaytextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.25", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        # self._actualdecaytextctrl.SetEditable(0)
        # _sounddecaylabelsfgsizer.Add( self._actualdecaytextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        # #Creo el tercer label de la slider de decay
        # self._maxdecaytextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        # self._maxdecaytextctrl.SetEditable(0)
        # _sounddecaylabelsfgsizer.Add( self._maxdecaytextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        # #Relaciona el sizer con el sizer del sonido
        # _specialsoundconfigFgSizer.Add( _sounddecaylabelsfgsizer, 1, wx.EXPAND, 5 )
        # #Crea el espacio de texto con el label sustain y lo agrega al sizer del panel de configuración de sonido
        # self._soundsustaintextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"Sustain:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        # self._soundsustaintextctrl.SetEditable(0)
        # _specialsoundconfigFgSizer.Add( self._soundsustaintextctrl, 0, wx.ALL, 5 )
        # #Crea la slider para el parametro sustain
        # self._soundsustainslider = wx.Slider( self._specialsoundcongifpanel, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        # self._soundsustainslider.Bind( wx.EVT_KEY_UP, self._eventsoundsustain )
        # self._soundsustainslider.Bind( wx.EVT_SCROLL, self._eventsoundsustain )
        # _specialsoundconfigFgSizer.Add( self._soundsustainslider, 0, wx.ALL|wx.EXPAND, 5 )
        # #Crea el sizer para contener las etiquetas de la slider de sustain
        # _soundsustainlabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        # _soundsustainlabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        # _soundsustainlabelsfgsizer.AddGrowableCol(1)
        # #Creo el primer label de la slider de sustain
        # self._minsustaintextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        # self._minsustaintextctrl.SetEditable(0)
        # _soundsustainlabelsfgsizer.Add( self._minsustaintextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        # #Creo el segundo label de la slider de sustain
        # self._actualsustaintextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"50", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        # self._actualsustaintextctrl.SetEditable(0)
        # _soundsustainlabelsfgsizer.Add( self._actualsustaintextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        # #Creo el tercer label de la slider de sustain
        # self._maxsustaintextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"100", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        # self._maxsustaintextctrl.SetEditable(0)
        # _soundsustainlabelsfgsizer.Add( self._maxsustaintextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        # #Relaciona el sizer con el sizer del sonido
        # _specialsoundconfigFgSizer.Add( _soundsustainlabelsfgsizer, 1, wx.EXPAND, 5 )
        # #Crea el espacio de texto con el label release y lo agrega al sizer del panel de configuración de sonido
        # self._soundreleasetextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"Release:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        # self._soundreleasetextctrl.SetEditable(0)
        # _specialsoundconfigFgSizer.Add( self._soundreleasetextctrl, 0, wx.ALL, 5 )
        # #Crea la slider para el parametro release
        # self._soundreleaseslider = wx.Slider( self._specialsoundcongifpanel, wx.ID_ANY, 25, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        # self._soundreleaseslider.Bind( wx.EVT_KEY_UP, self._eventsoundrelease )
        # self._soundreleaseslider.Bind( wx.EVT_SCROLL, self._eventsoundrelease )
        # _specialsoundconfigFgSizer.Add( self._soundreleaseslider, 0, wx.ALL|wx.EXPAND, 5 )
        # #Crea el sizer para contener las etiquetas de la slider de release
        # _soundreleaselabelsfgsizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        # _soundreleaselabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        # _soundreleaselabelsfgsizer.AddGrowableCol(1)
        # #Creo el primer label de la slider de release
        # self._minreleasetextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.01", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        # self._minreleasetextctrl.SetEditable(0)
        # _soundreleaselabelsfgsizer.Add( self._minreleasetextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        # #Creo el segundo label de la slider de release
        # self._actualreleasetextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"0.25", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        # self._actualreleasetextctrl.SetEditable(0)
        # _soundreleaselabelsfgsizer.Add( self._actualreleasetextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        # #Creo el tercer label de la slider de release
        # self._maxreleasetextctrl = wx.TextCtrl( self._specialsoundcongifpanel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_RIGHT )
        # self._maxreleasetextctrl.SetEditable(0)
        # _soundreleaselabelsfgsizer.Add( self._maxreleasetextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        # #Relaciona el sizer con el sizer del sonido
        # _specialsoundconfigFgSizer.Add( _soundreleaselabelsfgsizer, 1, wx.EXPAND, 5 )
        # #Crea el boton de dos estados para ocultar la grafica de la envolvente
        # self._envelopegraphtogglebtn = wx.ToggleButton(
        #     parent = self._specialsoundcongifpanel,
        #     id = wx.ID_ANY,
        #     label = 'Hide envelope\nplot',
        #     pos = wx.DefaultPosition,
        #     size = wx.DefaultSize,
        #     style = 0,
        #     name = 'Envelope plot toggle button'
        #     )
        # self._envelopegraphtogglebtn.Bind(
        #     event = wx.EVT_TOGGLEBUTTON,
        #     handler = self._eventenvelopegraph
        #     )
        # self._envelopegraphtogglebtn.SetValue(True)
        # _specialsoundconfigFgSizer.Add(
        #     window = self._envelopegraphtogglebtn,
        #     proportion = 1,
        #     flag = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,
        #     border = 5
        #     )
        # # Crea el panel para contener el grafico de la envolvente y un sizer
        # # para contenerlo
        # self._envelopegraphpanel = wx.Panel(
        #     parent = self._specialsoundcongifpanel,
        #     id = wx.ID_ANY,
        #     pos = wx.DefaultPosition,
        #     size = wx.Size(300,150),
        #     style = wx.TAB_TRAVERSAL,
        #     name = 'Envelope graph panel'
        #     )
        # _envelopegraphsizer = wx.FlexGridSizer(
        #     rows = 1,
        #     cols = 1,
        #     vgap = 0,
        #     hgap = 0
        #     )
        # _envelopegraphsizer.SetFlexibleDirection(direction = wx.BOTH)
        # # Crea la figura, el canvas que la contiene y agrega un subplot llamado
        # # axes que se utilizara en el codigo principal
        # self._envelopefigure = Figure()
        # self._axesenvelopegraph = self._envelopefigure.add_subplot(111)
        # self._envelopecanvas = FigureCanvas(self._envelopegraphpanel, -1, self._envelopefigure)
        # self._envelopecanvas.SetToolTip('Displays the envelope of the sound setted by the user.')
        # #Agrega el canvas que relaciona la figura con el panel al sizer del panel del grafico
        # _envelopegraphsizer.Add( self._envelopecanvas, 1, wx.EXPAND |wx.ALL, 5 )
        # #Relaciona el panel del grafico con su propio sizer y lo agrega al sizer del panel Display
        # self._envelopegraphpanel.SetSizer( _envelopegraphsizer )
        # self._envelopegraphpanel.Layout()
        # _envelopegraphsizer.Fit( self._envelopegraphpanel )
        # _specialsoundconfigFgSizer.Add( self._envelopegraphpanel, 1, wx.EXPAND |wx.ALL, 5 )

        # #Relaciona el panel de configuraciones con su propio sizer y lo agrega al sizer del panel izquierdo
        # self._specialsoundcongifpanel.SetSizer( _specialsoundconfigFgSizer )
        # self._specialsoundcongifpanel.Layout()
        # _specialsoundconfigFgSizer.Fit( self._specialsoundcongifpanel )
        # _configFgSizer.Add( self._specialsoundcongifpanel, 1, wx.EXPAND |wx.ALL, 5 )
        # self._specialsoundcongifpanel.Hide()

    #Crea el boton de dos estados Plot Configurations, lo setea como presionado y lo agrega al sizer del panel Configuraciones
        self._configPlotToggleBtn = wx.ToggleButton( congifpanel, wx.ID_ANY, u"Show Plot\nConfigurations", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._configPlotToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventConfigPlot )
        self._configPlotToggleBtn.SetValue( False )
        _configFgSizer.Add( self._configPlotToggleBtn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL , 5 )
    #Crea el panel para desplegar las configuraciones del grafico y su sizer(row(4)col(2)) sin seccion expandida
        self._configPlotPanel = wx.Panel( congifpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _configPlotFgSizer = wx.FlexGridSizer( 4, 2, 0, 0 )
        _configPlotFgSizer.SetFlexibleDirection( wx.BOTH )
        _configPlotFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea el texto estatico Line Style y lo agrega al sizer del panel de configuraciones del grafico
        self._lineStileTextCtrl = wx.TextCtrl( self._configPlotPanel, wx.ID_ANY, u"Line Style:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._lineStileTextCtrl.SetEditable(0)
        _configPlotFgSizer.Add( self._lineStileTextCtrl, 0, wx.ALL, 5 )
        #Crea el cuadro de seleccion entre opciones de estilo de linea para el grafico, setea una eleccion por defecto y lo agrega al sizer del panel de configuraciones del grafico
        _lineStyleChoiceChoices = [ u"Discreet", u"Solid line", u"Dashed line", u"Dash-dot line", u"Dotted line" ]
        self._lineStyleChoice = wx.Choice( self._configPlotPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, _lineStyleChoiceChoices, 0 )
        self._lineStyleChoice.Bind( wx.EVT_CHOICE, self._eventLineStyleConfig )
        self._lineStyleChoice.SetSelection( 1 )
        _configPlotFgSizer.Add( self._lineStyleChoice, 0, wx.ALL, 5 )
        #Crea el texto estatico Marker Style y lo agrega al sizer del panel de configuraciones del grafico
        self._markerTextCtrl = wx.TextCtrl( self._configPlotPanel, wx.ID_ANY, u"Marker Style:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._markerTextCtrl.SetEditable(0)
        _configPlotFgSizer.Add( self._markerTextCtrl, 0, wx.ALL, 5 )
        #Crea el cuadro de seleccion entre opciones de estilo de marcadores para el grafico, setea una eleccion por defecto y lo agrega al sizer del panel de configuraciones del grafico
        _markerStyleChoiceChoices = [ u"Point", u"Pixel", u"Circle", u"Triangle down", u"Triangle up", u"Triangle left", u"Triangle right", u"Tri down", u"Tri up", u"Tri left", u"Tri right", u"Square", u"Pentagon", u"Star", u"Hexagon 1", u"Hexagon 2", u"Plus", u"X", u"Diamond", u"Thin diamond", u"Vertical line", u"Horizontal line", u"Any" ]
        self._markerStyleChoice = wx.Choice( self._configPlotPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, _markerStyleChoiceChoices, 0 )
        self._markerStyleChoice.Bind( wx.EVT_CHOICE, self._eventMarkerStyleConfig )
        self._markerStyleChoice.SetSelection( 22 )
        _configPlotFgSizer.Add( self._markerStyleChoice, 0, wx.ALL, 5 )
        #Crea el texto estatico Color Style y lo agrega al sizer del panel de configuraciones del grafico
        #Cambiar static text
        self._colorTextCtrl = wx.TextCtrl( self._configPlotPanel, wx.ID_ANY, u"Color Style:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._colorTextCtrl.SetEditable(0)
        _configPlotFgSizer.Add( self._colorTextCtrl, 0, wx.ALL, 5 )
        #Crea el cuadro de seleccion entre opciones de colores para el grafico, setea una eleccion por defecto y lo agrega al sizer del panel de configuraciones del grafico
        _colorStyleChoiceChoices = [ u"Blue", u"Green", u"Red", u"Cyan", u"Magenta", u"Yellow", u"Black" ]
        self._colorStyleChoice = wx.Choice( self._configPlotPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, _colorStyleChoiceChoices, 0 )
        self._colorStyleChoice.Bind( wx.EVT_CHOICE, self._eventColorStyleConfig )
        self._colorStyleChoice.SetSelection( 0 )
        _configPlotFgSizer.Add( self._colorStyleChoice, 0, wx.ALL, 5 )
        #Agregamos configuración para la Grid
        self._gridChoice = wx.CheckBox( self._configPlotPanel, wx.ID_ANY, label=u"Grid option: ", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.ALIGN_RIGHT, name=u"Grid check box")
        self._gridChoice.Bind( wx.EVT_CHECKBOX, self._eventGridChoice )
        _configPlotFgSizer.Add( self._gridChoice, 0, wx.ALL, 5)
        self._gridChoice.SetValue(False)
        #Panel de los stylos de grid
        self._plotGridPanel = wx.Panel( self._configPlotPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _plotGridFgSizer = wx.FlexGridSizer( 3, 2, 0, 0 )
        _plotGridFgSizer.SetFlexibleDirection( wx.BOTH )
        _plotGridFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Color style
        self._gridColorTextCtrl = wx.TextCtrl( self._plotGridPanel, wx.ID_ANY, u"Color:", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._gridColorTextCtrl.SetEditable(0)
        _plotGridFgSizer.Add( self._gridColorTextCtrl, 0, wx.ALL, 5 )
        _gridColorChoiceChoices = [ u"Blue", u"Green", u"Red", u"Cyan", u"Magenta", u"Yellow", u"Black", u"White" ]
        self._gridColorChoice = wx.Choice( self._plotGridPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, _gridColorChoiceChoices, 0 )
        self._gridColorChoice.Bind( wx.EVT_CHOICE, self._eventGridColorChoice )
        self._gridColorChoice.SetSelection( 6 )
        _plotGridFgSizer.Add( self._gridColorChoice, 0, wx.ALL, 5 )
        #Line style
        self._gridLineTextCtrl = wx.TextCtrl( self._plotGridPanel, wx.ID_ANY, u"Line:", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._gridLineTextCtrl.SetEditable(0)
        _plotGridFgSizer.Add( self._gridLineTextCtrl, 0, wx.ALL, 5 )
        _gridLineChoiceChoices = [ u"Solid line", u"Dashed line", u"Dash-dot line", u"Dotted line" ]
        self._gridLineChoice = wx.Choice( self._plotGridPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, _gridLineChoiceChoices, 0 )
        self._gridLineChoice.Bind( wx.EVT_CHOICE, self._eventGridLineChoice )
        self._gridLineChoice.SetSelection( 1 )
        _plotGridFgSizer.Add( self._gridLineChoice, 0, wx.ALL, 5 )
        #Ancho
        self._gridWidthTextCtrl = wx.TextCtrl( self._plotGridPanel, wx.ID_ANY, u"Width:", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._gridWidthTextCtrl.SetEditable(0)
        _plotGridFgSizer.Add( self._gridWidthTextCtrl, 0, wx.ALL, 5 )
        self._gridWidthSpinCtrl = wx.SpinCtrlDouble( self._plotGridPanel, wx.ID_ANY, u" ", wx.DefaultPosition, wx.Size( 100,-1 ), wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0, 100, 0.5, 0.1, name=u"Grid width spin control" )
        self._gridWidthSpinCtrl.Bind( wx.EVT_SPINCTRLDOUBLE, self._eventGridWidthSpinCtrl )
        _plotGridFgSizer.Add( self._gridWidthSpinCtrl, 0, wx.ALL, 5 )
        #Relaciona el sizer con el panel
        self._plotGridPanel.SetSizer( _plotGridFgSizer )
        self._plotGridPanel.Layout()
        _plotGridFgSizer.Fit( self._plotGridPanel )
        _configPlotFgSizer.Add( self._plotGridPanel, 1, wx.EXPAND |wx.ALL, 5 )
        self._plotGridPanel.Hide()
        #Relaciona el sizer con el panel de las configuraciones del grafico y lo agrega al sizer del panel de configuraciones
        self._configPlotPanel.SetSizer( _configPlotFgSizer )
        self._configPlotPanel.Layout()
        _configPlotFgSizer.Fit( self._configPlotPanel )
        _configFgSizer.Add( self._configPlotPanel, 1, wx.EXPAND |wx.ALL, 5 )
        self._configPlotPanel.Hide()
        #Relaciona el panel de configuraciones con su propio sizer y lo agrega al sizer del panel izquierdo
        congifpanel.SetSizer( _configFgSizer )
        congifpanel.Layout()
        _configFgSizer.Fit( congifpanel )
        return congifpanel

    def _createdisplaypanel(self, panel):
        # Create the display panel with its sizer (row(3)col(1))
        # the frame (row(0)col(0)) is expanded
        displaypanel = wx.Panel( 
            parent = panel, 
            id = wx.ID_ANY, 
            pos = wx.DefaultPosition, 
            size = wx.DefaultSize, 
            style = wx.TAB_TRAVERSAL 
            )
        _displayFgSizer = wx.FlexGridSizer(
            rows = 3, 
            cols = 1, 
            vgap = 0, 
            hgap = 0 
            )
        _displayFgSizer.AddGrowableCol(idx=0)
        _displayFgSizer.AddGrowableRow(idx=0)
        _displayFgSizer.SetFlexibleDirection(direction=wx.BOTH)
        # Create the graphic panel with its sizer 
        self._graphicPanel = wx.Panel(
            parent = displaypanel, 
            id = wx.ID_ANY, 
            pos = wx.DefaultPosition, 
            size = wx.Size(400,200),
            style = wx.TAB_TRAVERSAL 
            )
        _matplotlibSizer = wx.FlexGridSizer(
            rows = 1, 
            cols = 2, 
            vgap = 0, 
            hgap = 0 
            )
        _matplotlibSizer.AddGrowableCol(idx=1)
        _matplotlibSizer.AddGrowableRow(idx=0)
        _matplotlibSizer.SetFlexibleDirection(direction=wx.BOTH)
        # Create input data panel and its elements inside a function
        self._createInputDataDisplayPanel(self._graphicPanel)
        # Add the panel to the sizer
        _matplotlibSizer.Add(
            window = self._openPanel, 
            proportion = 1, 
            flag = wx.EXPAND|wx.ALL, 
            border = 5 
            )
        self._openPanel.Hide()

        self._plotPanel = wx.ScrolledWindow(
            parent = displaypanel,
            id = wx.ID_ANY,
            pos = wx.DefaultPosition,
            size = wx.Size(400,200),
            style = wx.HSCROLL | wx.VSCROLL | wx.TAB_TRAVERSAL
            )
        _plotSizer = wx.FlexGridSizer(
            rows = 1,
            cols = 1,
            vgap = 0,
            hgap = 0
            )
        _plotSizer.AddGrowableCol(idx=0)
        _plotSizer.AddGrowableRow(idx=0)
        #Crea la figura, el canvas que la contiene y agrega un subplot llamado axes que se utilizara el en codigo principal
        self._figure = Figure()
        self._axes = self._figure.add_subplot(111)
        self._canvas = FigureCanvas(self._plotPanel, -1, self._figure)
        self._canvas.SetMinSize(wx.Size(1,1))
        self._canvas.SetToolTip( u"Displays the plot of the data opened by the user." )
        #Agrega el canvas que relaciona la figura con el panel al sizer del panel del grafico
        _plotSizer.Add( self._canvas, 1, wx.EXPAND |wx.ALL, 5 )
        
        self._plotPanel.SetSizer( _plotSizer )
        self._plotPanel.Layout()
        _plotSizer.Fit( self._plotPanel )
        _matplotlibSizer.Add( self._plotPanel, 1, wx.EXPAND |wx.ALL, 5 )
        
        #Relaciona el panel del grafico con su propio sizer y lo agrega al sizer del panel Display
        self._graphicPanel.SetSizer( _matplotlibSizer )
        self._graphicPanel.Layout()
        _matplotlibSizer.Fit( self._graphicPanel )
        _displayFgSizer.Add( self._graphicPanel, 1, wx.EXPAND |wx.ALL, 5 )

    #Crea el sizer de las slider de abscisas y tempo sin panel contenedor (row(1)col(2))
        _sliderDisplayGSizer = wx.GridSizer( 1, 2, 0, 0 )
        #Crea un sizer para contener el label y la slider de la posicion en abscisas(row(1)col(2)), con la seccion (row(0)col(1)) expandida
        _absPosFgSizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        _absPosFgSizer.AddGrowableCol( 1 )
        _absPosFgSizer.SetFlexibleDirection( wx.BOTH )
        _absPosFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea un espacio de texto con el label Abscissa Position y lo agrega al sizer de objetos relacionados con la posicion de abscisas.
        self._absPosTextCtrl = wx.TextCtrl( displaypanel, wx.ID_ANY, u"Abscissa Position:", wx.DefaultPosition, wx.Size( 125,30 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_READONLY )
        #self._absPosTextCtrl.SetEditable(0)
        self._absPosTextCtrl.SetToolTip( u"Abscissa position label." )
        _absPosFgSizer.Add( self._absPosTextCtrl, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
        
        # Genero un sizer con 3 filas para el label superior, la slider y el
        # label inferior
        _abslabels_fgsizer = wx.FlexGridSizer(
            rows=3, 
            cols=1,
            vgap=0,
            hgap=0
            )
        _abslabels_fgsizer.AddGrowableCol(0)
        
        # Create the element to show the position and allow to change it
        self._absposlabel_textctrl = wx.TextCtrl(
            parent = displaypanel,
            id = wx.ID_ANY,
            value = '0',
            pos = wx.DefaultPosition,
            size = wx.Size( 125,15 ),
            style = (wx.TE_PROCESS_ENTER 
                | wx.TE_CENTRE 
                | wx.BORDER_NONE 
                | wx.TE_NO_VSCROLL
                ),
            name = 'Text element where you can set the x position.'
            )
        self._absposlabel_textctrl.SetBackgroundColour(
            colour = displaypanel.GetBackgroundColour()
            )
        self._absposlabel_textctrl.Bind(
            event = wx.EVT_TEXT_ENTER,
            handler = self._eventabsposition
            )
        _abslabels_fgsizer.Add(
            window=self._absposlabel_textctrl,
            proportion=0,
            flag=wx.ALIGN_CENTER,
            border=5
            )
        self._absposlabel_textctrl.SetToolTip('Text element'
                + ' where you can set the x position.')
        
        # Create the abscisa position slider ans append it to its sizer
        self._abspos_slider = wx.Slider(
            parent=displaypanel, 
            id=wx.ID_ANY, 
            value=0, 
            minValue=0, 
            maxValue=100, 
            pos=wx.DefaultPosition, 
            size=wx.Size( -1,-1 ), 
            style=wx.SL_HORIZONTAL,
            name='Abscisa position slider'
            )
        self._abspos_slider.SetToolTip(
            'Abscisa position slider'
            )
        self._abspos_slider.Bind(
            event=wx.EVT_SCROLL, 
            handler=self._eventAbsPos 
            )
        self._abspos_slider.Bind(
            event=wx.EVT_SLIDER, 
            handler=self._eventAbsPos 
            )
        self._abspos_slider.Bind( 
            event=wx.EVT_KEY_DOWN, 
            handler=self._eventAbsPos 
            )
        _abslabels_fgsizer.Add( 
            window=self._abspos_slider, 
            proportion=0, 
            flag=wx.ALL|wx.EXPAND, 
            border=5 
            )
        
        # Create a sizer to min and max abscisa value
        _absminmaxlabel_fgsizer = wx.GridSizer(
            rows=1,
            cols=2,
            vgap=0,
            hgap=0
            )
        # Create min abscisa value element, read only
        self._absminlabel_textctrl = wx.TextCtrl(
            parent = displaypanel,
            id = wx.ID_ANY,
            value = '0',
            pos = wx.DefaultPosition,
            size = wx.Size( 100,15 ),
            style = ( 
                wx.TE_LEFT 
                | wx.BORDER_NONE 
                | wx.TE_MULTILINE 
                | wx.TE_NO_VSCROLL
                ),
            name = 'Text element where you can find the x min position.'
            )
        self._absminlabel_textctrl.SetBackgroundColour(
            colour = displaypanel.GetBackgroundColour()
            )
        _absminmaxlabel_fgsizer.Add(
            window=self._absminlabel_textctrl,
            proportion=0,
            flag=wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,
            border=1
            )
        self._absminlabel_textctrl.SetToolTip(
            'Text element where you can find the x min position.'
            )
        
        # Create max abscisa value element, read only
        self._absmaxlabel_textctrl = wx.TextCtrl(
            parent = displaypanel,
            id = wx.ID_ANY,
            value = '100',
            pos = wx.DefaultPosition,
            size = wx.Size( 100,15 ),
            style = ( 
                wx.TE_RIGHT 
                | wx.BORDER_NONE 
                | wx.TE_MULTILINE 
                | wx.TE_NO_VSCROLL
                ),
            name = 'Text element where you can find the x max position.'
            )
        self._absmaxlabel_textctrl.SetBackgroundColour(
            colour = displaypanel.GetBackgroundColour()
            )
        _absminmaxlabel_fgsizer.Add(
            window=self._absmaxlabel_textctrl,
            proportion=0,
            flag=wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL,
            border=1
            )
        self._absmaxlabel_textctrl.SetToolTip(
            'Text element where you can find the x max position.'
            )
        
        # Add minmax labels sizer to the labels sizer
        _abslabels_fgsizer.Add(
            sizer=_absminmaxlabel_fgsizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL,
            border=1
            )
        
        #Relaciona el sizer de filas con el sizer general de abscisas.
        _absPosFgSizer.Add( _abslabels_fgsizer, 1, wx.EXPAND, 5 )
        
        #Relaciona el sizer de abscisas con el sizer de abscisas y tempo.
        _sliderDisplayGSizer.Add( _absPosFgSizer, 1, wx.EXPAND, 5 )
        #Crea el sizer para contener el label y la slider del tempo (row(1)col(2)), con la seccion (row(0)col(1)) expandida
        _soundVelFgSizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        _soundVelFgSizer.AddGrowableCol( 1 )
        _soundVelFgSizer.SetFlexibleDirection( wx.BOTH )
        _soundVelFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea un espacio de texto con el label Tempo y lo agrega al sizer contenedor de los objetos tempo
        self._soundVelTextCtrl = wx.TextCtrl( displaypanel, wx.ID_ANY, u"Tempo:", wx.DefaultPosition, wx.Size( 60,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        self._soundVelTextCtrl.SetEditable(0)
        self._soundVelTextCtrl.NavigateIn()
        self._soundVelTextCtrl.SetToolTip('This is the label of the tempo slider.')
        _soundVelFgSizer.Add( self._soundVelTextCtrl, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
        
        
        # Genero un sizer con 3 filas para el label superior, la slider y el
        # label inferior
        _tempolabels_fgsizer = wx.FlexGridSizer(
            rows=3, 
            cols=1,
            vgap=0,
            hgap=0
            )
        _tempolabels_fgsizer.AddGrowableCol(0)
        
        # Create the element to show the position and allow to change it
        self._tempoposlabel_textctrl = wx.TextCtrl(
            parent = displaypanel,
            id = wx.ID_ANY,
            value = '50',
            pos = wx.DefaultPosition,
            size = wx.Size( 125,15 ),
            style = (wx.TE_PROCESS_ENTER 
                | wx.TE_CENTRE 
                | wx.BORDER_NONE 
                | wx.TE_NO_VSCROLL
                ),
            name = 'Text element where you can set the tempo position.'
            )
        self._tempoposlabel_textctrl.SetBackgroundColour(
            colour = displaypanel.GetBackgroundColour()
            )
        self._tempoposlabel_textctrl.Bind(
            event = wx.EVT_TEXT_ENTER,
            handler = self._eventtempoposition
            )
        _tempolabels_fgsizer.Add(
            window=self._tempoposlabel_textctrl,
            proportion=0,
            flag=wx.ALIGN_CENTER,
            border=5
            )
        self._tempoposlabel_textctrl.SetToolTip('Text element'
                + ' where you can set the tempo position.')
        
        
        #Crea una slider para modificar el tempo y la agrega al sizer contenedor de los objetos tempo
        self._soundVelSlider = wx.Slider( displaypanel, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        self._soundVelSlider.Bind( wx.EVT_KEY_UP, self._eventSoundVel )
        self._soundVelSlider.Bind( wx.EVT_SCROLL, self._eventSoundVel )
        self._soundVelSlider.SetToolTip('Tempo slider')
        _tempolabels_fgsizer.Add( self._soundVelSlider, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        # Create a sizer to min and max abscisa value
        _tempominmaxlabel_fgsizer = wx.GridSizer(
            rows=1,
            cols=2,
            vgap=0,
            hgap=0
            )
        # Create min abscisa value element, read only
        self._tempominlabel_textctrl = wx.TextCtrl(
            parent = displaypanel,
            id = wx.ID_ANY,
            value = '0',
            pos = wx.DefaultPosition,
            size = wx.Size( 100,15 ),
            style = ( 
                wx.TE_LEFT 
                | wx.BORDER_NONE 
                | wx.TE_MULTILINE 
                | wx.TE_NO_VSCROLL
                ),
            name = 'Text element where you can find the tempo min value.'
            )
        self._tempominlabel_textctrl.SetBackgroundColour(
            colour = displaypanel.GetBackgroundColour()
            )
        _tempominmaxlabel_fgsizer.Add(
            window=self._tempominlabel_textctrl,
            proportion=0,
            flag=wx.ALIGN_LEFT|wx.EXPAND|wx.ALL,
            border=1
            )
        self._tempominlabel_textctrl.SetToolTip(
            'Text element where you can find the tempo min value.'
            )
        
        # Create max abscisa value element, read only
        self._tempomaxlabel_textctrl = wx.TextCtrl(
            parent = displaypanel,
            id = wx.ID_ANY,
            value = '100',
            pos = wx.DefaultPosition,
            size = wx.Size( 100,15 ),
            style = ( 
                wx.TE_RIGHT 
                | wx.BORDER_NONE 
                | wx.TE_MULTILINE 
                | wx.TE_NO_VSCROLL
                ),
            name = 'Text element where you can find the tempo max value.'
            )
        self._tempomaxlabel_textctrl.SetBackgroundColour(
            colour = displaypanel.GetBackgroundColour()
            )
        _tempominmaxlabel_fgsizer.Add(
            window=self._tempomaxlabel_textctrl,
            proportion=0,
            flag=wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL,
            border=1
            )
        self._tempomaxlabel_textctrl.SetToolTip(
            'Text element where you can find the tempo max value.'
            )
        
        # Add minmax labels sizer to the labels sizer
        _tempolabels_fgsizer.Add(
            sizer=_tempominmaxlabel_fgsizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL,
            border=1
            )
        
        
        #Relaciona el sizer de filas con el sizer general de abscisas.
        _soundVelFgSizer.Add( _tempolabels_fgsizer, 1, wx.EXPAND, 5 )
        
        #Relaciona el sizer del tempo con el sizer de abscisas y tempo.
        _sliderDisplayGSizer.Add( _soundVelFgSizer, 1, wx.EXPAND, 5 )
        #Relaciona el sizer de las abscisas y tempo con el sizer del panel Display
        _displayFgSizer.Add( _sliderDisplayGSizer, 1, wx.EXPAND, 5 )

    #Crea el sizer de los botones de control de reproduccion sin panel contenedor (row(1)col(5))
        _buttonDisplayFgSizer = wx.FlexGridSizer( 1, 6, 0, 0 )
        _buttonDisplayFgSizer.SetFlexibleDirection( wx.BOTH )
        _buttonDisplayFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea el boton Play y lo agrega al sizer de botones de control de reproduccion
        self._playButton = wx.ToggleButton( displaypanel, wx.ID_ANY, u"Play", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._playButton.SetValue(False)
        self._playButton.Bind( wx.EVT_TOGGLEBUTTON, self._eventplay )
        self._playButton.SetToolTip('This button allow to play and pause the sound.')
        _buttonDisplayFgSizer.Add( self._playButton, 0, wx.ALL, 5 )
#        #Crea el boton Pause y lo agrega al sizer de botones de control de reproduccion
#        self._pauseButton = wx.Button( displaypanel, wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.DefaultSize, 0 )
#        self._pauseButton.Bind( wx.EVT_BUTTON, self._eventPause )
#        _buttonDisplayFgSizer.Add( self._pauseButton, 0, wx.ALL, 5 )
        #Crea el boton Stop y lo agrega al sizer de botones de control de reproduccion
        self._stopButton = wx.Button( displaypanel, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._stopButton.Bind( wx.EVT_BUTTON, self._eventstop )
        self._stopButton.SetToolTip('This button allow to stop the sound.')
        _buttonDisplayFgSizer.Add( self._stopButton, 0, wx.ALL, 5 )
        #Crea el boton Mark Point y lo agrega al sizer de botones de control de reproduccion
        self._markPtButton = wx.Button( displaypanel, wx.ID_ANY, u"Mark Point", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._markPtButton.Bind( wx.EVT_BUTTON, self._eventmarkpoint )
        self._markPtButton.SetToolTip('This button allow to mark a point on the current position of the x slider bar.')
        _buttonDisplayFgSizer.Add( self._markPtButton, 0, wx.ALL, 5 )
        #Crea el boton Delete last mark y lo agrega al sizer de botones de control de reproduccion
        self._deleteLastPtButton = wx.Button( displaypanel, wx.ID_ANY, u"Delete last mark", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._deleteLastPtButton.Bind( wx.EVT_BUTTON, self._eventdeletelastmark )
        self._deleteLastPtButton.SetToolTip('This button allow to delete the last mark done on the data.')
        _buttonDisplayFgSizer.Add( self._deleteLastPtButton, 0, wx.ALL, 5 )

        #Crea el boton de dos estados lineal vs logaritmic scale
        self._linvslog_soundscale_display_togglebtn = wx.ToggleButton( displaypanel, wx.ID_ANY, u"Set logarithmic scale", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._linvslog_soundscale_display_togglebtn.Bind( wx.EVT_TOGGLEBUTTON, self._event_linvslog_soundscalechoice_display )
        self._linvslog_soundscale_display_togglebtn.SetValue( False )
        _buttonDisplayFgSizer.Add( self._linvslog_soundscale_display_togglebtn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL , 5 )

        #Crea el boton 
        self._contdiscsound_display_ToggleBtn = wx.ToggleButton( displaypanel, wx.ID_ANY, u"Set continuous sound", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._contdiscsound_display_ToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventcontdiscsoundchoice_display )
        self._contdiscsound_display_ToggleBtn.SetValue( False )
        _buttonDisplayFgSizer.Add( self._contdiscsound_display_ToggleBtn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL , 5 )


        # #Crea el boton Plot Data Options y lo agrega al sizer de botones de control de reproduccion
        # self._dataParamPlotToggleBtn = wx.ToggleButton( displaypanel, wx.ID_ANY, u"Data Parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
        # self._dataParamPlotToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventcpdataparamplot )
        # self._dataParamPlotToggleBtn.SetToolTip('This button allow to show and hide the data information panel.')
        # _buttonDisplayFgSizer.Add( self._dataParamPlotToggleBtn, 0, wx.ALL, 5 )

        #Relaciona el sizer de botones de control de reproduccion con el sizer del panel Display
        _displayFgSizer.Add( _buttonDisplayFgSizer, 1, wx.ALIGN_CENTER, 5 )
        #Relaciona el panel Display con su propio sizer y lo agrega en el sizer del panel derecho
        displaypanel.SetSizer( _displayFgSizer )
        displaypanel.Layout()
        _displayFgSizer.Fit( displaypanel )
        return displaypanel

    def _createoperationpanel(self, panel):
        #Crea el panel Operation con su sizer(row(2)col(1)) y con el cuadro (row(0)col(0)) expandido
        operationpanel = wx.Panel( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _operationFgSizer = wx.FlexGridSizer( 4, 1, 0, 0 )
        _operationFgSizer.AddGrowableCol( 0 )
        _operationFgSizer.AddGrowableRow( 1 )
        _operationFgSizer.SetFlexibleDirection( wx.BOTH )
        _operationFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

    #Crea el panel de la shell que se mantendrá oculto.
        self._pythonShellPanel = wx.Panel( operationpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _pythonShellFgSizer = wx.FlexGridSizer( 1, 1, 0, 0 )
        _pythonShellFgSizer.AddGrowableCol( 0 )
        _pythonShellFgSizer.SetFlexibleDirection( wx.BOTH )
        _pythonShellFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self._createShell(self._pythonShellPanel)
        _pythonShellFgSizer.Add( self._pythonShell, 1, wx.EXPAND |wx.ALL, 5 )
        self._pythonShellPanel.Hide()
        #Relaciona el panel de operaciones con su sizer y lo agrega al sizer del panel principal derecho
        self._pythonShellPanel.SetSizer( _pythonShellFgSizer )
        self._pythonShellPanel.Layout()
        _pythonShellFgSizer.Fit( self._pythonShellPanel )
        _operationFgSizer.Add( self._pythonShellPanel, 1, wx.EXPAND |wx.ALL, 5 )

    #Crea el panel de la linea de comandos.
        self._writecommandpanel = wx.Panel( operationpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _writecommandfgsizer = wx.FlexGridSizer(1, 2, 0, 0)
        _writecommandfgsizer.AddGrowableCol(1)
        _writecommandfgsizer.SetFlexibleDirection(wx.BOTH)
        #Aquí generamos los elementos, por ahora un text control que permite el
        #ingreso de texto
        self._writecommandlabeltextctrl = wx.TextCtrl(
            parent = self._writecommandpanel,
            id = wx.ID_ANY,
            value = 'Write functionality:',
            pos = wx.DefaultPosition,
            size = wx.Size(130, 20),
            style = wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT,
            name = ('Label of the text element where you can write the ')
                + ('functionalities.')
            )
        _writecommandfgsizer.Add(
            window = self._writecommandlabeltextctrl,
            proportion = 0,
            flag = wx.EXPAND|wx.ALL,
            border = 5
            )
        self._writecommandlabeltextctrl.SetToolTip('Label of the text element'
                + ' where you can write the functionalities.')
        self._writecommandlabeltextctrl.SetEditable(0)
        self._writecommandtextctrl = wx.TextCtrl(
            parent = self._writecommandpanel,
            id = wx.ID_ANY,
            value = '',
            pos = wx.DefaultPosition,
            size = wx.DefaultSize,
            style = wx.TE_PROCESS_ENTER,
            name = 'Text element where you can write the functionalities.'
            )
        self._writecommandtextctrl.Bind(
            event = wx.EVT_TEXT_ENTER,
            handler = self._eventwritecommand
            )
        _writecommandfgsizer.Add(
            window = self._writecommandtextctrl,
            proportion = 0,
            flag = wx.EXPAND|wx.ALL,
            border = 5
            )
        self._writecommandtextctrl.SetToolTip('Text element'
                + ' where you can write the functionalities.')

        #self._writecommandpanel.Hide()
        #Relaciona el panel de operaciones con su sizer y lo agrega al sizer del panel principal derecho
        self._writecommandpanel.SetSizer( _writecommandfgsizer )
        self._writecommandpanel.Layout()
        _writecommandfgsizer.Fit( self._writecommandpanel )
        _operationFgSizer.Add( self._writecommandpanel, 1, wx.EXPAND |wx.ALL, 5 )

    #Crea el panel Gnu Octave con su sizer (row(1)col(2)) y con el cuadro (row(1)col(0)) expandido
        self._gnuOctavePanel = wx.Panel( operationpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _octaveFgSizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        _octaveFgSizer.AddGrowableCol( 0 )
        _octaveFgSizer.SetFlexibleDirection( wx.BOTH )
        _octaveFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        #Crea el sizer de los elementos izquierdos
        _octaveLeftFgSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
        _octaveLeftFgSizer.AddGrowableCol( 1 )
        _octaveLeftFgSizer.AddGrowableRow( 1 )
        _octaveLeftFgSizer.SetFlexibleDirection( wx.BOTH )
        _octaveLeftFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea el espacio de texto con el label Octave y lo agrega al sizer de GNU Octave
        self._octaveLabelInputTextCtrl = wx.TextCtrl( self._gnuOctavePanel, wx.ID_ANY, u"Octave command:", wx.DefaultPosition, wx.Size( 120,20 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        _octaveLeftFgSizer.Add( self._octaveLabelInputTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )
        self._octaveLabelInputTextCtrl.SetToolTip( u"" )
        self._octaveLabelInputTextCtrl.SetEditable(0)
        self._octaveInputTextCtrl = wx.TextCtrl( self._gnuOctavePanel, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self._octaveInputTextCtrl.Bind( wx.EVT_TEXT_ENTER, self._eventOctaveInput )
        _octaveLeftFgSizer.Add( self._octaveInputTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )
        self._octaveLabelInputTextCtrl.Hide()
        self._octaveInputTextCtrl.Hide()
        self._octaveLabelOutputTextCtrl = wx.TextCtrl( self._gnuOctavePanel, wx.ID_ANY, u"Octave info:", wx.DefaultPosition, wx.Size( 120,20 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        _octaveLeftFgSizer.Add( self._octaveLabelOutputTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )
        self._octaveLabelOutputTextCtrl.SetToolTip( u"" )
        self._octaveLabelOutputTextCtrl.SetEditable(0)
        self._octaveOutputTextCtrl = wx.TextCtrl( self._gnuOctavePanel, wx.ID_ANY, u" ", wx.DefaultPosition, wx.Size( -1,60 ), style=wx.TE_MULTILINE )
        _octaveLeftFgSizer.Add( self._octaveOutputTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )
        self._octaveOutputTextCtrl.SetEditable(0)
        #Relaciona el sizer de la izquierda con el de octave
        _octaveFgSizer.Add( _octaveLeftFgSizer, 1, wx.EXPAND | wx.ALL, 5 )

#Se descartará esta parte por el momento para probar una forma más facil de comunicación.
        #Crea el sizer de los elementos derechos
        _octaveRightFgSizer = wx.FlexGridSizer( 3, 1, 0, 0 )
        _octaveRightFgSizer.SetFlexibleDirection( wx.BOTH )
        _octaveRightFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

#        #Crea el sizer para la parte superior
#        _octaveTopRightFgSizer = wx.FlexGridSizer( 1, 2, 0, 0 )
#        _octaveTopRightFgSizer.SetFlexibleDirection( wx.BOTH )
#        _octaveTopRightFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
#        #Crea los elementos para push
#        self._sendToOctaveLabelTextCtrl = wx.TextCtrl( self._gnuOctavePanel, wx.ID_ANY, u"Send to octave: ", wx.DefaultPosition, wx.Size( -1,30 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
#        _octaveTopRightFgSizer.Add( self._sendToOctaveLabelTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )
#        self._sendToOctaveLabelTextCtrl.SetEditable(0)
#        self._sendToOctaveListBox = wx.ListBox( self._gnuOctavePanel, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1,40), [""], 0 )
##        self._sendToOctaveListBox.Bind( wx.EVT_LISTBOX, self._eventSendToOctave )
#        self._sendToOctaveListBox.SetSelection( 0 )
#        _octaveTopRightFgSizer.Add( self._sendToOctaveListBox, 0, wx.ALL|wx.FIXED_MINSIZE, 5 )
#        #Relaciona el sizer de la parte superior con el de la derecha
#        _octaveRightFgSizer.Add( _octaveTopRightFgSizer, 1, wx.EXPAND | wx.ALL, 5 )

        #Crea el label de la parte central
        self._retFromOctaveLabelTextCtrl = wx.TextCtrl( self._gnuOctavePanel, wx.ID_ANY, u"Retrieve from octave:", wx.DefaultPosition, wx.Size( 120,20 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        _octaveRightFgSizer.Add( self._retFromOctaveLabelTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )
        self._retFromOctaveLabelTextCtrl.SetEditable(0)

        #Crea el sizer para la parte central
        _octaveCenterRightFgSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
        _octaveCenterRightFgSizer.SetFlexibleDirection( wx.BOTH )
        _octaveCenterRightFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea los elementos para pull
        self._xFromOctaveLabelTextCtrl = wx.TextCtrl( self._gnuOctavePanel, wx.ID_ANY, u"Name of x array: ", wx.DefaultPosition, wx.Size( 120,20 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        _octaveCenterRightFgSizer.Add( self._xFromOctaveLabelTextCtrl, 0, wx.ALL, 5 )
        self._xFromOctaveLabelTextCtrl.SetEditable(0)
        self._xFromOctaveTextCtrl = wx.TextCtrl( self._gnuOctavePanel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self._xFromOctaveTextCtrl.Bind( wx.EVT_TEXT_ENTER, self._eventXFromOctave )
        _octaveCenterRightFgSizer.Add( self._xFromOctaveTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )
        self._yFromOctaveLabelTextCtrl = wx.TextCtrl( self._gnuOctavePanel, wx.ID_ANY, u"Name of y array: ", wx.DefaultPosition, wx.Size( 120,20 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        _octaveCenterRightFgSizer.Add( self._yFromOctaveLabelTextCtrl, 0, wx.ALL, 5 )
        self._yFromOctaveLabelTextCtrl.SetEditable(0)
        self._yFromOctaveTextCtrl = wx.TextCtrl( self._gnuOctavePanel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self._yFromOctaveTextCtrl.Bind( wx.EVT_TEXT_ENTER, self._eventYFromOctave )
        _octaveCenterRightFgSizer.Add( self._yFromOctaveTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )
        #Relaciona el sizer de la parte central con el de la derecha
        _octaveRightFgSizer.Add( _octaveCenterRightFgSizer, 1, wx.EXPAND | wx.ALL, 5 )

        #Crea el botón para reiniciar la session
        self._octaveReplotButton = wx.Button( self._gnuOctavePanel, wx.ID_ANY, u"Refresh the plot", wx.DefaultPosition, wx.DefaultSize, 0 )
#        self._octaveReplotButton.Bind( wx.EVT_BUTTON, self._eventOctaveReplot )
        self._octaveReplotButton.Bind( wx.EVT_BUTTON, self._eventContinueReplotFromOctave )
        _octaveRightFgSizer.Add( self._octaveReplotButton, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        #Realciona el sizer de la derecha con el de octave
        _octaveFgSizer.Add( _octaveRightFgSizer, 1, wx.EXPAND | wx.ALL, 5 )

#        #Crea el botón para reiniciar la session
#        self._octaveReplotButton = wx.Button( self._gnuOctavePanel, wx.ID_ANY, u"Refresh the plot", wx.DefaultPosition, wx.DefaultSize, 0 )
#        self._octaveReplotButton.Bind( wx.EVT_BUTTON, self._eventOctaveReplot )
#        _octaveFgSizer.Add( self._octaveReplotButton, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        #Relaciona el panel GNU Octave con su sizer y lo agrega al sizer del panel operaciones
        self._gnuOctavePanel.SetSizer( _octaveFgSizer )
        self._gnuOctavePanel.Layout()
        _octaveFgSizer.Fit( self._gnuOctavePanel )
        _operationFgSizer.Add( self._gnuOctavePanel, 1, wx.EXPAND | wx.ALL, 5 )
        self._gnuOctavePanel.Hide()

    #Crea el panel de las funciones matematicas, se llama sizer porque contendra sizers dentro de sizers, crea el sizer correspondiente(row(1)col(2)) y con el cuadro (row(0)col(0)) expandido
        self._sizersMFPanel = wx.Panel( operationpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _itemsOpFgSizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        _itemsOpFgSizer.AddGrowableCol( 0 )
        _itemsOpFgSizer.AddGrowableRow( 0 )
        _itemsOpFgSizer.SetFlexibleDirection( wx.BOTH )
        _itemsOpFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea un panel para contener las slider de corte de ejes cartesianos y el sizer correspondiente (row(4)col(1)) con la col(0) expandida
        self._sizersPanel = wx.Panel( self._sizersMFPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _axisFgSizer = wx.FlexGridSizer( 2, 1, 0, 0 )
        _axisFgSizer.AddGrowableCol( 0 )
        _axisFgSizer.SetFlexibleDirection( wx.BOTH )
        _axisFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
#        #Crea el cuadro de texto con el label Vertical Axis y lo agrega al sizer del panel de las sliders
#        self._vAxisTextCtrl = wx.TextCtrl( self._sizersPanel, wx.ID_ANY, u"Vertical Axis:", wx.DefaultPosition, wx.Size( -1,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
#        _axisFgSizer.Add( self._vAxisTextCtrl, 0, wx.ALL, 5 )
#        #Crea un sizer (row(2)col(2)) para contener las slider del limite vertical, con la col(1) expandida
#        _vAxisFgSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
#        _vAxisFgSizer.AddGrowableCol( 1 )
#        _vAxisFgSizer.SetFlexibleDirection( wx.BOTH )
#        _vAxisFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
#        #Crea un cuadro de texto con el label Lower Limit y lo agrega al sizer del limite vertical
#        self._lvLimitTextCtrl = wx.TextCtrl( self._sizersPanel, wx.ID_ANY, u"Lower Limit:", wx.DefaultPosition, wx.Size( -1,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
#        _vAxisFgSizer.Add( self._lvLimitTextCtrl, 0, wx.ALL, 5 )
#        #Crea una slider para indicar el parametro minimo de corte vertical y lo agrega al sizer del limite vertical
#        self._lVLimitSlider = wx.Slider( self._sizersPanel, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL | wx.SL_LABELS)
#        self._lVLimitSlider.Bind( wx.EVT_KEY_UP, self._eventLVLimitSlider )
#        self._lVLimitSlider.Bind( wx.EVT_SCROLL, self._eventLVLimitSlider )
#        _vAxisFgSizer.Add( self._lVLimitSlider, 0, wx.EXPAND, 5 )
#        #Crea un cuadro de texto con el label Upper Limit y lo agrega al sizer del limite vertical
#        self._uvLimitTextCtrl = wx.TextCtrl( self._sizersPanel, wx.ID_ANY, u"Upper Limit:", wx.DefaultPosition, wx.Size( -1,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
#        _vAxisFgSizer.Add( self._uvLimitTextCtrl, 0, wx.ALL, 5 )
#        #Crea una slider para indicar el parametro maximo de corte vertical y lo agrega al sizer del limite vertical
#        self._uVLimitSlider = wx.Slider( self._sizersPanel, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL | wx.SL_LABELS)
#        self._uVLimitSlider.Bind( wx.EVT_KEY_UP, self._eventUVLimitSlider )
#        self._uVLimitSlider.Bind( wx.EVT_SCROLL, self._eventUVLimitSlider )
#        _vAxisFgSizer.Add( self._uVLimitSlider, 0, wx.EXPAND, 5 )
#        #Relaciona el sizer de corte vertical con el sizer que contiene todas las slider de corte
#        _axisFgSizer.Add( _vAxisFgSizer, 1, wx.EXPAND, 5 )

        #Crea el cuadro de texto con el label Horizontal Axis y lo agrega al sizer del panel de las sliders de corte
        self._hAxisTextCtrl = wx.TextCtrl( self._sizersPanel, wx.ID_ANY, u"Horizontal Axis:", wx.DefaultPosition, wx.Size( 110,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        self._hAxisTextCtrl.SetEditable(0)
        _axisFgSizer.Add( self._hAxisTextCtrl, 0, wx.ALL, 5 )
        #Crea un sizer (row(2)col(2)) para contener las slider del limite horizontal, con la col(1) expandida
        _hAxisFgSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
        _hAxisFgSizer.AddGrowableCol( 1 )
        _hAxisFgSizer.SetFlexibleDirection( wx.BOTH )
        _hAxisFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea un cuadro de texto con el label Lower Limit y lo agrega al sizer del limite horizontal
        self._lhLimitTextCtrl = wx.TextCtrl( self._sizersPanel, wx.ID_ANY, u"Lower Limit:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        self._lhLimitTextCtrl.SetEditable(0)
        _hAxisFgSizer.Add( self._lhLimitTextCtrl, 0, wx.ALL, 5 )
        #Crea una slider para indicar el parametro minimo de corte horizontal y lo agrega al sizer del limite horizontal
        self._lHLimitSlider = wx.Slider( self._sizersPanel, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL | wx.SL_LABELS )
        self._lHLimitSlider.Bind( wx.EVT_KEY_UP, self._eventLHLimitSlider )
        self._lHLimitSlider.Bind( wx.EVT_SCROLL, self._eventLHLimitSlider )
        _hAxisFgSizer.Add( self._lHLimitSlider, 0, wx.EXPAND, 5 )
        #Crea un cuadro de texto con el label Upper Limit y lo agrega al sizer del limite horizontal
        self._uhLimitTextCtrl = wx.TextCtrl( self._sizersPanel, wx.ID_ANY, u"Upper Limit:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        self._uhLimitTextCtrl.SetEditable(0)
        _hAxisFgSizer.Add( self._uhLimitTextCtrl, 0, wx.ALL, 5 )
        #Crea una slider para indicar el parametro maximo de corte horizontal y lo agrega al sizer del limite horizontal
        self._uHLimitSlider = wx.Slider( self._sizersPanel, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL | wx.SL_LABELS )
        self._uHLimitSlider.Bind( wx.EVT_KEY_UP, self._eventUHLimitSlider )
        self._uHLimitSlider.Bind( wx.EVT_SCROLL, self._eventUHLimitSlider )
        _hAxisFgSizer.Add( self._uHLimitSlider, 0, wx.EXPAND, 5 )
        #Relaciona el sizer de corte horizontal con el sizer que contiene todas las slider de corte
        _axisFgSizer.Add( _hAxisFgSizer, 1, wx.EXPAND, 5 )
        #Relaciona el panel de las slider con su sizer y lo agrega al sizer del panel de las funciones matematicas
        self._sizersPanel.SetSizer( _axisFgSizer )
        self._sizersPanel.Layout()
        _axisFgSizer.Fit( self._sizersPanel )
        _itemsOpFgSizer.Add( self._sizersPanel, 1, wx.EXPAND |wx.ALL, 5 )
        #Crea un panel para contener las funciones matematicas predefinidas y el sizer correspondiente (row(4)col(1)) con el cuadro (col(0)row(1)) expandido
        self._matFcPanel = wx.Panel( self._sizersMFPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _matFcFgSizer = wx.FlexGridSizer( 4, 1, 0, 0 )
        _matFcFgSizer.AddGrowableCol( 0 )
        _matFcFgSizer.AddGrowableRow( 1 )
        _matFcFgSizer.SetFlexibleDirection( wx.BOTH )
        _matFcFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea un cuadro de texto con el label Mathematical Functions y lo agrega al sizer de las funciones matematicas predefinidas
        self._matFcTextCtrl = wx.TextCtrl( self._matFcPanel, wx.ID_ANY, u"Mathematical Functions:", wx.DefaultPosition, wx.Size( 170,30 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_LEFT )
        self._matFcTextCtrl.SetEditable(0)
        _matFcFgSizer.Add( self._matFcTextCtrl, 0, wx.ALL, 5 )
        #Crea una lista de funciones matematicas predefinidas, las carga en una lista desplegable y la agrega al sizer de las funciones matematicas predefinidas
        _matFcListBoxChoices = [ u"Last limits cut", u"Original", u"Inverse", u"Square", u"Square root", u"Logarithm", u"Average" ] #u"Play Backward",
        self._matFcListBox = wx.ListBox( self._matFcPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, _matFcListBoxChoices, wx.LB_ALWAYS_SB )
        self._matFcListBox.Bind( wx.EVT_LISTBOX, self._eventMatFc )
        _matFcFgSizer.Add( self._matFcListBox, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea un cuadro de texto con el label Average number of points y lo agrega al sizer de las funciones matematicas predefinidas
        self._avNPointsTextCtrl = wx.TextCtrl( self._matFcPanel, wx.ID_ANY, u"Average number of points:", wx.DefaultPosition, wx.Size( 120,30 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_LEFT )#, u"Average number of points:" )
        self._avNPointsTextCtrl.SetEditable(0)
        _matFcFgSizer.Add( self._avNPointsTextCtrl, 0, wx.ALL, 5 )
        #Crea un campo de texto editable con botones para subir y bajar el valor, lo presetea en 1 y lo agrega al sizer de las funciones matematicas predefinidas
        self._avNPointsspinCtrl = wx.SpinCtrl( self._matFcPanel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 1, 1000, 0 )
        self._avNPointsspinCtrl.Bind( wx.EVT_SPINCTRL, self._eventAvNPoints )
        self._avNPointsspinCtrl.Bind( wx.EVT_TEXT_ENTER, self._eventAvNPoints )
        self._avNPointsspinCtrl.Enable(False)
        _matFcFgSizer.Add( self._avNPointsspinCtrl, 0, wx.ALL, 5 )
        #Relaciona el panel de las funciones matematicas con el propio sizer y lo agrega en el sizer del panel de sizers y funciones matematicas
        self._matFcPanel.SetSizer( _matFcFgSizer )
        self._matFcPanel.Layout()
        _matFcFgSizer.Fit( self._matFcPanel )
        _itemsOpFgSizer.Add( self._matFcPanel, 1, wx.EXPAND |wx.ALL, 5 )
        #Relaciona el panel de los sizer y las funciones matematicas con su sizer y lo agrega al sizer del panel de operaciones
        self._sizersMFPanel.SetSizer( _itemsOpFgSizer )
        self._sizersMFPanel.Layout()
        _itemsOpFgSizer.Fit( self._sizersMFPanel )
        _operationFgSizer.Add( self._sizersMFPanel, 1, wx.EXPAND |wx.ALL, 5 )
        self._sizersMFPanel.Hide()
        #Relaciona el panel de operaciones con su sizer y lo agrega al sizer del panel principal derecho
        operationpanel.SetSizer( _operationFgSizer )
        operationpanel.Layout()
        _operationFgSizer.Fit( operationpanel )
        return operationpanel

    def replotFromOctavePanel(self, panel):
        #Crea el panel
        self.retrieveFromOctavePanel = wx.Panel( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #Crea el sizer para todo el dialog
        _retrieveFgSizer = wx.FlexGridSizer( 3, 2, 0, 0 )
        _retrieveFgSizer.SetFlexibleDirection( wx.BOTH )
        _retrieveFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        #Crea los elementos para pull
        self._xFromOctaveLabelTextCtrl = wx.TextCtrl( self.retrieveFromOctavePanel, wx.ID_ANY, u"Name of x array: ", wx.DefaultPosition, wx.Size( 130,30 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        _retrieveFgSizer.Add( self._xFromOctaveLabelTextCtrl, 0, wx.ALL, 5 )
        self._xFromOctaveLabelTextCtrl.SetEditable(0)
        self._xFromOctaveTextCtrl = wx.TextCtrl( self.retrieveFromOctavePanel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self._xFromOctaveTextCtrl.Bind( wx.EVT_TEXT_ENTER, self._eventXFromOctave )
        _retrieveFgSizer.Add( self._xFromOctaveTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )
        self._yFromOctaveLabelTextCtrl = wx.TextCtrl( self.retrieveFromOctavePanel, wx.ID_ANY, u"Name of y array: ", wx.DefaultPosition, wx.Size( 130,30 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        _retrieveFgSizer.Add( self._yFromOctaveLabelTextCtrl, 0, wx.ALL, 5 )
        self._yFromOctaveLabelTextCtrl.SetEditable(0)
        self._yFromOctaveTextCtrl = wx.TextCtrl( self.retrieveFromOctavePanel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self._yFromOctaveTextCtrl.Bind( wx.EVT_TEXT_ENTER, self._eventYFromOctave )
        _retrieveFgSizer.Add( self._yFromOctaveTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )

        #Crea el botón ok
        self._continueButton = wx.Button( self.retrieveFromOctavePanel, wx.ID_ANY, u"Continue", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._continueButton.Bind( wx.EVT_BUTTON, self._eventContinueReplotFromOctave )
        _retrieveFgSizer.Add( self._continueButton, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        #Crea el botón Close
        self._closeButton = wx.Button( self.retrieveFromOctavePanel, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._closeButton.Bind( wx.EVT_BUTTON, self._eventCloseReplotFromOctave )
        _retrieveFgSizer.Add( self._closeButton, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        #Relaciona el panel GNU Octave con su sizer y lo agrega al sizer del panel operaciones
        self.retrieveFromOctavePanel.SetSizer( _retrieveFgSizer )
        self.retrieveFromOctavePanel.Layout()
        _retrieveFgSizer.Fit( self.retrieveFromOctavePanel )


    def _createInputDataDisplayPanel(self, panel):
        # Create the panel which contain the input data elements
        self._openPanel = wx.ScrolledWindow( 
            parent = panel, 
            id = wx.ID_ANY, 
            pos = wx.DefaultPosition, 
            size = wx.DefaultSize, 
            style = wx.HSCROLL|wx.VSCROLL|wx.TAB_TRAVERSAL 
            )
        self._openPanel.SetScrollRate(5,5)
        self._openPanel.SetMinSize(wx.Size(350,200))
        _openButFgSizer = wx.FlexGridSizer( 
            rows = 5, 
            cols = 1, 
            vgap = 0, 
            hgap = 0 
            )
        _openButFgSizer.SetFlexibleDirection(direction=wx.BOTH)
        # Create the sizer for data title.
        _titleDataFgSizer = wx.FlexGridSizer( 
            rows = 1, 
            cols = 2, 
            vgap = 0, 
            hgap = 0 
            )
        _titleDataFgSizer.AddGrowableCol(idx=1)
        _titleDataFgSizer.SetFlexibleDirection(direction=wx.BOTH)
        # Create data title label
        self._titleDataTextCtrl = wx.TextCtrl( 
            parent = self._openPanel, 
            id = wx.ID_ANY, 
            value = 'Data title:', 
            pos = wx.DefaultPosition, 
            size = wx.Size(70,15), 
            style = wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL,
            name = 'Data title label')
        self._titleDataTextCtrl.SetEditable(0)
        self._titleDataTextCtrl.SetToolTip(
            'This is the label of the data title element.'
            )
        _titleDataFgSizer.Add(
            window = self._titleDataTextCtrl, 
            proportion = 0, 
            flag = wx.ALL, 
            border = 5 
            )
        # Create the data title element
        self._titleEdDataTextCtrl = wx.TextCtrl(
            parent = self._openPanel, 
            id = wx.ID_ANY, 
            value = wx.EmptyString, 
            pos = wx.DefaultPosition, 
            size = wx.DefaultSize, 
            style = wx.TE_PROCESS_ENTER, 
            name = 'Data title element'
            )
        self._titleEdDataTextCtrl.SetToolTip('Here you can find the data '
            + 'title and change it if you want.')
        self._titleEdDataTextCtrl.Bind(
            event = wx.EVT_TEXT_ENTER, 
            handler = self._eventTitleEdData 
            )
        _titleDataFgSizer.Add(
            window = self._titleEdDataTextCtrl, 
            proportion = 0, 
            flag = wx.EXPAND|wx.ALL, 
            border = 5 
            )
        _openButFgSizer.Add(
            sizer = _titleDataFgSizer, 
            proportion = 0, 
            flag = wx.EXPAND, 
            border = 5 
            )
        # Create a sizer for the grid elements.
        _gridboxfgsizer = wx.FlexGridSizer( 
            rows = 1, 
            cols = 3, 
            vgap = 0, 
            hgap = 0 
            )
        _gridboxfgsizer.SetFlexibleDirection( wx.BOTH )
        # Create the grid panel and its sizer.
        self._datagridpanel = wx.ScrolledWindow( self._openPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.TAB_TRAVERSAL )
        self._datagridpanel.SetScrollRate( 5, 5 )
        self._datagridpanel.SetMinSize( wx.Size( 250,150 ) )
        _datagridfgsizer = wx.FlexGridSizer( 1, 1, 0, 0 )
        _datagridfgsizer.SetFlexibleDirection( wx.BOTH )
        #Create the grid for the original data
        self._dataGrid = wx.grid.Grid( self._datagridpanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 240,140 ), 0 )
        # df = pd.DataFrame(data=np.zeros((10,5)))
        # table = DataTable(df)
        # self._dataGrid.SetTable(table, takeOwnership=True)
        # self._dataGrid.AutoSizeColumns()
        # _datagridfgsizer.Add( self._dataGrid, 0, wx.EXPAND | wx.ALL, 5 )
        # self._dataGrid.HideCol(0)
        # self._dataGrid.HideColLabels()
        # self._dataGrid.SetRowLabelSize(wx.grid.GRID_AUTOSIZE)

        # #Create the grid for the data update
        # self._dataupdategrid = wx.grid.Grid( self._datagridpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        # self._dataupdategrid.SetTable(table, takeOwnership=True)
        # self._dataupdategrid.AutoSizeColumns()
        # _datagridfgsizer.Add( self._dataupdategrid, 0, wx.EXPAND | wx.ALL, 5 )
        # self._dataupdategrid.Hide()

        self._dataGrid.SetTabBehaviour(2)
        # Grid
        self._dataGrid.CreateGrid( 11, 2 )
        self._dataGrid.EnableEditing( True )
        self._dataGrid.EnableGridLines( True )
        self._dataGrid.EnableDragGridSize( False )
        self._dataGrid.SetMargins( 0, 0 )
        # Columns
        self._dataGrid.EnableDragColMove( False )
        self._dataGrid.EnableDragColSize( True )
        self._dataGrid.SetColLabelSize( 0 )
        self._dataGrid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        # Rows
        self._dataGrid.EnableDragRowSize( True )
        self._dataGrid.SetRowLabelSize( 50 )
        self._dataGrid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        # Label Appearance
        # Cell Defaults
        self._dataGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        self._dataGrid.SetMaxSize( wx.Size( 300,100 ) )
        
        self._dataGrid.SetToolTip('This is a grid element which contain tha data.')

        _datagridfgsizer.Add( self._dataGrid, 0, wx.EXPAND | wx.ALL, 5 )

        #Relaciona el sizer con el panel y lo agrega al sizer
        self._datagridpanel.SetSizer( _datagridfgsizer )
        self._datagridpanel.Layout()
        _datagridfgsizer.Fit( self._datagridpanel )
        _gridboxfgsizer.Add(self._datagridpanel, 0, wx.EXPAND | wx.ALL, 5)

        #Crea la slider para el parametro sustain
        self._datagridslider = wx.Slider( self._openPanel, wx.ID_ANY, 1, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_VERTICAL )
        self._datagridslider.Bind( wx.EVT_KEY_UP, self._eventdatagridpage )
        self._datagridslider.Bind( wx.EVT_SCROLL, self._eventdatagridpage )
        self._datagridslider.SetToolTip('This slider bar allows to chage between data pages, each page contain 100 values.')
        _gridboxfgsizer.Add( self._datagridslider, 0, wx.ALL|wx.EXPAND, 5 )
        #Crea el sizer para contener las etiquetas de la slider de sustain
        _datagridsliderlabelsfgsizer = wx.FlexGridSizer( 3, 1, 0, 0 )
        _datagridsliderlabelsfgsizer.SetFlexibleDirection( wx.BOTH )
        _datagridsliderlabelsfgsizer.AddGrowableRow(1)
        #Creo el primer label de la slider de sustain
        self._mingridpagetextctrl = wx.TextCtrl( self._openPanel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._mingridpagetextctrl.SetEditable(0)
        self._mingridpagetextctrl.SetToolTip('This is the min value of the data grid slider bar.')
        _datagridsliderlabelsfgsizer.Add( self._mingridpagetextctrl, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        #Creo el segundo label de la slider de sustain
        self._actualgridpagetextctrl = wx.TextCtrl( self._openPanel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._actualgridpagetextctrl.SetEditable(0)
        self._actualgridpagetextctrl.SetToolTip('This is the actual value of the data grid slider bar.')
        _datagridsliderlabelsfgsizer.Add( self._actualgridpagetextctrl, 0, wx.ALL | wx.ALIGN_CENTRE, 5 )
        #Creo el tercer label de la slider de sustain
        self._maxgridpagetextctrl = wx.TextCtrl( self._openPanel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.ALIGN_LEFT )
        self._maxgridpagetextctrl.SetEditable(0)
        self._maxgridpagetextctrl.SetToolTip('This is the max value of the data grid slider bar.')
        _datagridsliderlabelsfgsizer.Add( self._maxgridpagetextctrl, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        #Relaciona el sizer con el sizer del sonido
        _gridboxfgsizer.Add( _datagridsliderlabelsfgsizer, 1, wx.EXPAND, 5 )


        _openButFgSizer.Add(_gridboxfgsizer, 0, wx.EXPAND | wx.ALL, 5)

        #Crea el sizer para los botones de la grilla
        _buttonsDataFgSizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _buttonsDataFgSizer.SetFlexibleDirection( wx.BOTH )
        _buttonsDataFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self._addGridChangesButton = wx.Button( self._openPanel, wx.ID_ANY, u"Update Column\n Names", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._addGridChangesButton.Bind( wx.EVT_BUTTON, self._eventAddGridChanges )
        self._addGridChangesButton.SetToolTip('This button update the columns names with the modification made on the grid element.')
        _buttonsDataFgSizer.Add( self._addGridChangesButton, 0, wx.ALL, 5 )

        self._addGridUpdateButton = wx.Button( self._openPanel, wx.ID_ANY, u"Update Grid", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._addGridUpdateButton.Bind( wx.EVT_BUTTON, self._eventUpdateGrid )
        self._addGridUpdateButton.SetToolTip('This button update the data gris with the x and y axis plotted.')
        _buttonsDataFgSizer.Add( self._addGridUpdateButton, 0, wx.ALL, 5 )

        self._addGridOriginalButton = wx.Button( self._openPanel, wx.ID_ANY, u"Original Array", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._addGridOriginalButton.Bind( wx.EVT_BUTTON, self._eventOriginalGrid )
        self._addGridOriginalButton.SetToolTip('This button load the original data on the data grid element.')
        _buttonsDataFgSizer.Add( self._addGridOriginalButton, 0, wx.ALL, 5 )

        _openButFgSizer.Add( _buttonsDataFgSizer, 0, wx.EXPAND, 5 )

    #Crea el sizer de los desplegables para elegir los ejes
        _axisChoiceFgSizer = wx.FlexGridSizer( 2, 2, 0, 0 )

        _axisChoiceFgSizer.SetFlexibleDirection( wx.BOTH )
        _axisChoiceFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self._axisChoiceXTextCtrl = wx.TextCtrl( self._openPanel, wx.ID_ANY, u"Axis X selection:", wx.DefaultPosition, wx.Size( 120,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        self._axisChoiceXTextCtrl.SetEditable(0)
        self._axisChoiceXTextCtrl.NavigateIn()
        self._axisChoiceXTextCtrl.SetToolTip('This is the label of the x selection element.')
        _axisChoiceFgSizer.Add( self._axisChoiceXTextCtrl, 0, wx.ALL|wx.FIXED_MINSIZE, 5 )

        self._axisChoiceX = wx.ListBox( self._openPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size(120,60), [""], 0 )
        self._axisChoiceX.Bind( wx.EVT_LISTBOX, self._eventAxisChoiceX )
        self._axisChoiceX.SetSelection( 0 )
        self._axisChoiceX.SetToolTip('This element allow to choose between the columns to set as x values.')
        _axisChoiceFgSizer.Add( self._axisChoiceX, 0, wx.ALL|wx.FIXED_MINSIZE, 5 )

        self._axisChoiceYTextCtrl = wx.TextCtrl( self._openPanel, wx.ID_ANY, u"Axis Y selection:", wx.DefaultPosition, wx.Size( 120,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        self._axisChoiceYTextCtrl.SetEditable(0)
        self._axisChoiceYTextCtrl.NavigateIn()
        self._axisChoiceYTextCtrl.SetToolTip('This is the label of the y selection element.')
        _axisChoiceFgSizer.Add( self._axisChoiceYTextCtrl, 0, wx.ALL|wx.FIXED_MINSIZE, 5 )

        self._axisChoiceY = wx.ListBox( self._openPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size(120,60), [""], 0 )
        self._axisChoiceY.Bind( wx.EVT_LISTBOX, self._eventAxisChoiceY )
        self._axisChoiceY.SetSelection( 0 )
        self._axisChoiceY.SetToolTip('This element allow to choose between the columns to set as y values.')
        _axisChoiceFgSizer.Add( self._axisChoiceY, 0, wx.ALL|wx.FIXED_MINSIZE, 5 )

        _openButFgSizer.Add( _axisChoiceFgSizer, 1, wx.ALL|wx.FIXED_MINSIZE, 5 )

        #Relaciona el sizer con el panel File y lo agrega al sizer del panel izquierdo
        self._openPanel.SetSizer( _openButFgSizer )
        self._openPanel.Layout()
        _openButFgSizer.Fit( self._openPanel )
        return self._openPanel

    def _createShell(self, panel):
        #Crea la shell
        all = dict(globals())
        all.update(locals())
        self._pythonShell = py.shell.Shell(panel, -1, introText="", locals=all, style=wx.RESIZE_BORDER)
        self._pythonShell.Execute("self._pythonShell.clear()")

    # Virtual event handlers, overide them in your derived class
    def _eventopen( self, event ):
        event.Skip()

    def _eventTitleEdData( self, event ):
        event.Skip()

    def _eventAskLabelData( self, event ):
        event.Skip()

    def _eventdatagridpage(self, event):
        event.Skip()

    def _eventAxisChoiceX( self, event ):
        event.Skip()

    def _eventAxisChoiceY( self, event ):
        event.Skip()

    def _eventAddGridChanges( self, event ):
        event.Skip()

    def _eventUpdateGrid( self, event ):
        event.Skip()

    def _eventOriginalGrid( self, event ):
        event.Skip()

    def _eventdeleteallmark( self, event ):
        event.Skip()

    def _eventsavedata( self, event ):
        event.Skip()

    def _eventsavemarks( self, event ):
        event.Skip()

    def _eventsavesound( self, event ):
        event.Skip()

    def _eventsaveplot( self, event ):
        event.Skip()

    def _onclose( self, event ):
        event.Skip()

    def _eventclose( self, event ):
        event.Skip()

    def _eventabsposselect( self, event ):
        event.Skip()

    def _eventtemposelect( self, event ):
        event.Skip()

    def _eventplay( self, event ):
        event.Skip()

#    def _eventPause( self, event ):
#        event.Skip()

    def _eventstop( self, event ):
        event.Skip()

    def _eventmarkpoint( self, event ):
        event.Skip()

    def _eventdeletelastmark( self, event ):
        event.Skip()

    def _eventcpdataparamplot( self, event ):
        event.Skip()

#    def _eventvlowerlimitselect( self, event ):
#        event.Skip()

#    def _eventvupperlimitselect( self, event ):
#        event.Skip()

    def _eventhlowerlimitselect( self, event ):
        event.Skip()

    def _eventhupperlimitselect( self, event ):
        event.Skip()

    def _eventoriginalmf( self, event ):
        event.Skip()

    def _eventinversemf( self, event ):
        event.Skip()

#    def _eventMFPlayBack( self, event ):
#        event.Skip()

    def _eventsquaremf( self, event ):
        event.Skip()

    def _eventsquarerootmf( self, event ):
        event.Skip()

    def _eventlogmf( self, event ):
        event.Skip()

    def _eventavnumpointselect( self, event ):
        event.Skip()

    def _eventaveragemf( self, event ):
        event.Skip()

    def _eventlastcutmf( self, event ):
        event.Skip()

    def _eventoctaveselect( self, event ):
        event.Skip()

    def _eventcpfileselect( self, event ):
        event.Skip()

    def _eventcpdatadisplayselect( self, event ):
        event.Skip()

    def _eventcpdataopselect( self, event ):
        event.Skip()

    def _eventcpdo_writecommandselect(self, event):
        event.Skip()

    def _eventcpdooctaveselect( self, event ):
        event.Skip()

    def _eventcpdocutsliderselect( self, event ):
        event.Skip()

    def _eventcpcallselect( self, event ):
        event.Skip()

    def _eventcpconfigsoundselect( self, event ):
        event.Skip()

    def _eventcpconfigplotselect( self, event ):
        event.Skip()

    def _eventcpconfigvisualselect( self, event ):
        event.Skip()
        
    def _eventlinsoundscalechoice(self, event):
        event.Skip()
        
    def _eventlogsoundscalechoice(self, event):
        event.Skip()

    def _eventcontsoundchoice(self, event):
        event.Skip()

    def _eventdiscsoundchoice(self, event):
        event.Skip()

    def _eventssvolumeselect( self, event ):
        event.Skip()

    def _eventssfreqmappingselect(self, event):
        event.Skip()

    def _eventssvolmappingselect(self, event):
        event.Skip()

    def _eventsswaveformselect( self, event ):
        event.Skip()

    def _eventsplotlineselect( self, event ):
        event.Skip()

    def _eventsplotmarkerselect( self, event ):
        event.Skip()

    def _eventsplotcolorselect( self, event ):
        event.Skip()

    def _eventsplotgridoptionselect( self, event ):
        event.Skip()

    def _eventabout( self, event ):
        event.Skip()

    def _eventmanual( self, event ):
        event.Skip()

    def _eventGFile( self, event ):
        event.Skip()

    def _eventGConfig( self, event ):
        event.Skip()

    def _eventGDisplay( self, event ):
        event.Skip()

#    def _eventOctaveToggle( self, event ):
#        event.Skip()

    def _eventSliderToggle( self, event ):
        event.Skip()

    def _eventConfigSound( self, event ):
        event.Skip()

    def _eventswaveform( self, event ):
        event.Skip()
        
    def _eventabsposition(self, event):
        event.Skip()

    def _eventAbsPos( self, event ):
        event.Skip()
        
    def _eventtempoposition(self, event):
        event.Skip()

    def _eventSoundVel( self, event ):
        event.Skip()
        
    def _event_linvslog_soundscalechoice(self, event):
        event.Skip()
        
    def _event_linvslog_soundscalechoice_display(self, event):
        event.Skip()

    def _eventcontdiscsoundchoice(self, event):
        event.Skip()
        
    def _eventcontdiscsoundchoice_display(self, event):
        event.Skip()

    def _eventsoundvolumn(self, event):
        event.Skip()
        
    def _eventfreqmapping(self, event):
        event.Skip()
        
    def _eventshow_soundfreqmin(self, event):
        event.Skip()

    def _eventsoundfreqmin(self, event):
        event.Skip()
        
    def _eventshow_soundfreqmax(self, event):
        event.Skip()

    def _eventsoundfreqmax(self, event):
        event.Skip()
        
    def _eventvolmapping(self, event):
        event.Skip()
        
    def _eventshow_soundvolmin(self, event):
        event.Skip()
        
    def _eventsoundvolmin(self, event):
        event.Skip()
        
    def _eventshow_soundvolmax(self, event):
        event.Skip()
        
    def _eventsoundvolmax(self, event):
        event.Skip()
        
    def _eventshow_soundvolfreq(self, event):
        event.Skip()
        
    def _eventsoundvolfreq(self, event):
        event.Skip()
        
    def _eventshowenvelope(self, event):
        event.Skip()

    def _eventsoundattack(self, event):
        event.Skip()

    def _eventsounddecay(self, event):
        event.Skip()

    def _eventsoundsustain(self, event):
        event.Skip()

    def _eventsoundrelease(self, event):
        event.Skip()

    def _eventenvelopegraph(self, event):
        event.Skip()
        
    def _eventenvelopeplay(self, event):
        event.Skip()

#    def _eventLVLimitSlider( self, event ):
#        event.Skip()

#    def _eventUVLimitSlider( self, event ):
#        event.Skip()

    def _eventLHLimitSlider( self, event ):
        event.Skip()

    def _eventUHLimitSlider( self, event ):
        event.Skip()

    def _eventMatFc( self, event ):
        event.Skip()

    def _eventAvNPoints( self, event ):
        event.Skip()

    def _eventSpecialSoundConfig( self, event ):
        event.Skip()

    def _eventConfigPlot( self, event ):
        event.Skip()

    def _eventLineStyleConfig( self, event ):
        event.Skip()

    def _eventMarkerStyleConfig( self, event ):
        event.Skip()

    def _eventColorStyleConfig( self, event ):
        event.Skip()

    def _eventGridChoice( self, event ):
        event.Skip()

    def _eventGridColorChoice( self, event ):
        event.Skip()

    def _eventGridLineChoice( self, event ):
        event.Skip()

    def _eventGridWidthSpinCtrl( self, event ):
        event.Skip()

#    def _eventSendToOctave( self, event ):
#        event.Skip()

    def _eventOctaveReplot( self, event ):
        event.Skip()

    def _eventXFromOctave( self, event ):
        event.Skip()

    def _eventYFromOctave( self, event ):
        event.Skip()

    def _eventwritecommand(self, event):
        event.Skip()

    def _eventOctaveInput( self, event ):
        event.Skip()

    def _eventContinueReplotFromOctave(self, event):
        event.Skip()

    def _eventCloseReplotFromOctave(self, event):
        event.Skip()


class ReplotFromOctave(wx.Dialog):

    def __init__(self, *args, **kw):
        super(ReplotFromOctave, self).__init__(*args, **kw)
        self.SetSize((250, 200))
        self.SetTitle("Retrieve data from Octave and replot")

        _mainsizer = wx.BoxSizer( wx.VERTICAL )

        #Crea el panel
        self.retrievePanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #Crea el sizer para todo el dialog
        _retrieveFgSizer = wx.FlexGridSizer( 3, 2, 0, 0 )
        _retrieveFgSizer.SetFlexibleDirection( wx.BOTH )
        _retrieveFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        #Crea los elementos para pull
        self._xFromOctaveLabelTextCtrl = wx.TextCtrl( self.retrievePanel, wx.ID_ANY, u"Name of x array: ", wx.DefaultPosition, wx.Size( -1,30 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        _retrieveFgSizer.Add( self._xFromOctaveLabelTextCtrl, 0, wx.ALL, 5 )
        self._xFromOctaveLabelTextCtrl.SetEditable(0)
        self._xFromOctaveTextCtrl = wx.TextCtrl( self.retrievePanel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self._xFromOctaveTextCtrl.Bind( wx.EVT_TEXT_ENTER, self._eventXFromOctave )
        _retrieveFgSizer.Add( self._xFromOctaveTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )
        self._yFromOctaveLabelTextCtrl = wx.TextCtrl( self.retrievePanel, wx.ID_ANY, u"Name of y array: ", wx.DefaultPosition, wx.Size( -1,30 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        _retrieveFgSizer.Add( self._yFromOctaveLabelTextCtrl, 0, wx.ALL, 5 )
        self._yFromOctaveLabelTextCtrl.SetEditable(0)
        self._yFromOctaveTextCtrl = wx.TextCtrl( self.retrievePanel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self._yFromOctaveTextCtrl.Bind( wx.EVT_TEXT_ENTER, self._eventYFromOctave )
        _retrieveFgSizer.Add( self._yFromOctaveTextCtrl, 0, wx.EXPAND | wx.ALL, 5 )

        #Crea el botón ok
        self._continueButton = wx.Button( self.retrievePanel, wx.ID_ANY, u"Continue", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._continueButton.Bind( wx.EVT_BUTTON, self._eventContinue )
        _retrieveFgSizer.Add( self._continueButton, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        #Crea el botón Close
        self._closeButton = wx.Button( self.retrievePanel, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._closeButton.Bind( wx.EVT_BUTTON, self.OnClose )
        _retrieveFgSizer.Add( self._closeButton, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        #Relaciona el panel GNU Octave con su sizer y lo agrega al sizer del panel operaciones
        self.retrievePanel.SetSizer( _retrieveFgSizer )
        self.retrievePanel.Layout()
        _retrieveFgSizer.Fit( self.retrievePanel )

        self.Bind( wx.EVT_CLOSE, self.OnClose )

        _mainsizer.Add( self.retrievePanel, 1, wx.EXPAND |wx.ALL, 5 )
        #Setea el sizer inicial
        self.SetSizer( _mainsizer )
        self.Layout()
        self.Centre( wx.BOTH )

    def OnClose(self, event):
        self.SetReturnCode(0)
        self.Destroy()

    def _eventContinue(self, event):
        self.SetReturnCode(1)
        self.Destroy()
        #event.Skip()

    def _eventXFromOctave( self, event ):
        event.Skip()

    def _eventYFromOctave( self, event ):
        event.Skip()
