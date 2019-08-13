# -*- coding: utf-8 -*- 

###########################################################################
##
###########################################################################

import wx
import wx.stc
import wx.xrc
import wx.grid
from wx import py

import matplotlib

# uncomment the following to use wx rather than wxagg
#matplotlib.use('WX')
#from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas

# comment out the following to use wx rather than wxagg
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

#from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from matplotlib.figure import Figure

###########################################################################
## Class Sonorizador
###########################################################################

class Sonorizador ( wx.Frame ):
	
    def __init__( self ):
        #crea la ventana principal | create principal windows
        wx.Frame.__init__ ( self, None, -1, title = u" Sono Uno", pos = ( 1, 1 ), size=( 850,550 ), style = wx.CAPTION|wx.DEFAULT_FRAME_STYLE|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        self._createMenuBar()
        self._createToolBar()
        self._statusBar = self.CreateStatusBar( 1, 0, wx.ID_ANY )

        #crea el sizer principal del wxframe
        _mainSizer = wx.BoxSizer( wx.VERTICAL )
        #crea la ventana principal, se elije una que tenga las barras verticales y horizontales para que entren todos los elementos en cualquier ventana
        self._mainScrolledWindow = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.TAB_TRAVERSAL )
        self._mainScrolledWindow.SetScrollRate( 5, 5 )
        #crea el sizer de la ventana principal y setea como expandida la columna(1)-fila(0) | Se dividira en panel izquierdo y derecho
        _mainFgSizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        _mainFgSizer.AddGrowableCol( 1 )
        _mainFgSizer.AddGrowableRow( 0 )
        _mainFgSizer.SetFlexibleDirection( wx.BOTH )
        _mainFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
#crea el panel Izquierdo con su sizer(row(2)col(1)) sin seccion expandido
        self._leftPanel = wx.Panel( self._mainScrolledWindow, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _mainLeftSizer = wx.FlexGridSizer( 2, 1, 0, 0 )
        _mainLeftSizer.SetFlexibleDirection( wx.BOTH )
        _mainLeftSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea el panel File
        self._createFilePanel(self._leftPanel)
        _mainLeftSizer.Add( self._filePanel, 1, wx.EXPAND |wx.ALL, 5 )
        self._filePanel.Hide()
        #Crea el panel configuraciones
        self._createConfigPanel(self._leftPanel)
        _mainLeftSizer.Add( self._congifPanel, 1, wx.EXPAND |wx.ALL, 5 )
        self._congifPanel.Hide()
        #Relaciona el panel izquierdo con su propio sizer y lo agrega al sizer de la ventana principal
        self._leftPanel.SetSizer( _mainLeftSizer )
        self._leftPanel.Layout()
        _mainLeftSizer.Fit( self._leftPanel )
        _mainFgSizer.Add( self._leftPanel, 1, wx.EXPAND |wx.ALL, 5 )

#Crea el panel derecho con su sizer(row(2)col(1)) y con el cuadro (row(0)col(0)) expandido
        self._rightPanel = wx.Panel( self._mainScrolledWindow, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self._mainRightSizer = wx.FlexGridSizer( 2, 1, 0, 0 )
        self._mainRightSizer.AddGrowableCol( 0 )
        self._mainRightSizer.AddGrowableRow( 0 )
        self._mainRightSizer.SetFlexibleDirection( wx.BOTH )
        self._mainRightSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea el panel display
        self._createDisplayPanel(self._rightPanel)
        self._mainRightSizer.Add( self._displayPanel, 1, wx.EXPAND |wx.ALL, 5 )
        #Crea el panel operaciones
        self._createOperationPanel(self._rightPanel)
        self._mainRightSizer.Add( self._operationPanel, 1, wx.ALL|wx.EXPAND, 5 )
        self._operationPanel.Hide()
        #Relaciona el panel principal derecho con su sizer y lo agrega al sizer de la ventana principal
        self._rightPanel.SetSizer( self._mainRightSizer )
        self._rightPanel.Layout()
        self._mainRightSizer.Fit( self._rightPanel )
        _mainFgSizer.Add( self._rightPanel, 1, wx.EXPAND |wx.ALL, 5 )
        
##Crea el panel de Retrieve from octave expandido
#        self.replotFromOctavePanel(self._mainScrolledWindow)
#        _mainFgSizer.Add( self.retrieveFromOctavePanel, 1, wx.EXPAND|wx.ALL, 5)
#        self.retrieveFromOctavePanel.Hide()
        
        #Relaciona la ventana principal con su sizer y la agrega al sizer inicial
        self._mainScrolledWindow.SetSizer( _mainFgSizer )
        self._mainScrolledWindow.Layout()
        _mainFgSizer.Fit( self._mainScrolledWindow )
        _mainSizer.Add( self._mainScrolledWindow, 1, wx.EXPAND |wx.ALL, 5 )
        #Setea el sizer inicial
        self.SetSizer( _mainSizer )
        self.Layout()
        self.Centre( wx.BOTH )
        
        #Crea la tabla de atajos de teclado, aquí se pueden agregar botones o funciones que no estén en el menu
        self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_SPACE, self._playMenuItem.GetId())
                                             ])
        self.SetAcceleratorTable(self.accel_tbl)

    
    def _createMenuBar(self):
        #crea menuBar | create menuBar
        self._menubar = wx.MenuBar( 0 )
#crea el menu File | create menu File
        self._menuFile = wx.Menu()
        #crea el menuItem Open y lo agrega a menu File | create menuItem Open and append this to menu File
        self._openMenuItem = wx.MenuItem( self._menuFile, wx.ID_ANY, u"&Open"+ u"\t" + u"Ctrl+Alt+O", wx.EmptyString, wx.ITEM_NORMAL )
        self._menuFile.Append( self._openMenuItem )
        self.Bind( wx.EVT_MENU, self._eventOpen, id = self._openMenuItem.GetId() )
        #crea el menuItem Open y lo agrega a menu File | create menuItem Open and append this to menu File
        self._deleteAllMarksMenuItem = wx.MenuItem( self._menuFile, wx.ID_ANY, u"Delete all marks"+ u"\t" + u"Ctrl+Alt+E", wx.EmptyString, wx.ITEM_NORMAL )
        self._menuFile.Append( self._deleteAllMarksMenuItem )
        self.Bind( wx.EVT_MENU, self._eventDeleteAllMark, id = self._deleteAllMarksMenuItem.GetId() )
    #crea el submenu Save | create submenu Save
        self._saveSubMenu = wx.Menu()
        #crea el menuItem Save Marks y lo agrega al submenu Save | create menuItem Save Marks and append this to submenu Save
        self._saveDataMenuItem = wx.MenuItem( self._saveSubMenu, wx.ID_ANY, u"&Save Data"+ u"\t" + u"Ctrl+Alt+A", wx.EmptyString, wx.ITEM_NORMAL )
        self._saveSubMenu.Append( self._saveDataMenuItem )
        self.Bind( wx.EVT_MENU, self._eventSaveData, id = self._saveDataMenuItem.GetId() )
        #crea el menuItem Save Marks y lo agrega al submenu Save | create menuItem Save Marks and append this to submenu Save
        self._saveMarksMenuItem = wx.MenuItem( self._saveSubMenu, wx.ID_ANY, u"&Save Marks"+ u"\t" + u"Ctrl+Alt+M", wx.EmptyString, wx.ITEM_NORMAL )
        self._saveSubMenu.Append( self._saveMarksMenuItem )
        self.Bind( wx.EVT_MENU, self._eventSaveMarks, id = self._saveMarksMenuItem.GetId() )
        #crea el menuItem Save Sound y lo agrega al submenu Save | create menuItem Save Sound and append this to submenu Save
        self._saveSoundMenuItem = wx.MenuItem( self._saveSubMenu, wx.ID_ANY, u"&Save Sound"+ u"\t" + u"Ctrl+Alt+S", wx.EmptyString, wx.ITEM_NORMAL )
        self._saveSubMenu.Append( self._saveSoundMenuItem )
        self.Bind( wx.EVT_MENU, self._eventSaveSound, id = self._saveSoundMenuItem.GetId() )
        #crea el menuItem Save Plot y lo agrega al submenu Save | create menuItem Save Plot and append this to submenu Save
        self._savePlotMenuItem = wx.MenuItem( self._saveSubMenu, wx.ID_ANY, u"&Save Plot"+ u"\t" + u"Ctrl+Alt+P", wx.EmptyString, wx.ITEM_NORMAL )
        self._saveSubMenu.Append( self._savePlotMenuItem )
        self.Bind( wx.EVT_MENU, self._eventSavePlot, id = self._savePlotMenuItem.GetId() )
    #Agrega el submenu Save al menu File | Append the submenu Save to the menu File
        self._menuFile.AppendSubMenu( self._saveSubMenu, u"Save" )
        #crea el menuItem Close y lo agrega al menu File
        self._closeMenuItem = wx.MenuItem( self._menuFile, wx.ID_ANY, u"&Exit"+ u"\t" + u"Ctrl+Alt+Q", wx.EmptyString, wx.ITEM_NORMAL )
        self._menuFile.Append( self._closeMenuItem )
        self.Bind( wx.EVT_MENU, self._OnClose, id = self._closeMenuItem.GetId() )
        self.Bind( wx.EVT_CLOSE, self._eventClose )
#Agrega el menu File a la menuBar
        self._menubar.Append( self._menuFile, u"File" ) 
#Crea el menu Data Display
        self._menuDisplay = wx.Menu()
        #Crea el menuItem Abscissa Position y lo agrega al menu Data Display
        self._absPosMenuItem = wx.MenuItem( self._menuDisplay, wx.ID_ANY, u"&Abscissa Position"+ u"\t" + u"Alt+Shift+X", wx.EmptyString, wx.ITEM_NORMAL )
        self._menuDisplay.Append( self._absPosMenuItem )
        self.Bind( wx.EVT_MENU, self._eventAbsPosSelect, id = self._absPosMenuItem.GetId() )
        #Crea el menuItem Tempo y lo agrega al menu Data Display
        self._tempoMenuItem = wx.MenuItem( self._menuDisplay, wx.ID_ANY, u"&Tempo"+ u"\t" + u"Alt+Shift+T", wx.EmptyString, wx.ITEM_NORMAL )
        self._menuDisplay.Append( self._tempoMenuItem )
        self.Bind( wx.EVT_MENU, self._eventTempoSelect, id = self._tempoMenuItem.GetId() )
        #Crea el menuItem Play y lo agrega al menu Data Display
        self._playMenuItem = wx.MenuItem( self._menuDisplay, wx.ID_ANY, u"&Play", wx.EmptyString, wx.ITEM_CHECK )
        self._menuDisplay.Append( self._playMenuItem )
        self.Bind( wx.EVT_MENU, self._eventPlay, id = self._playMenuItem.GetId() )
#        #Crea el menuItem Pause y lo agrega al menu Data Display
#        self._pauseMenuItem = wx.MenuItem( self._menuDisplay, wx.ID_ANY, u"Paus&e"+ u"\t" + u"Alt+Shift+E", wx.EmptyString, wx.ITEM_NORMAL )
#        self._menuDisplay.Append( self._pauseMenuItem )
#        self.Bind( wx.EVT_MENU, self._eventPause, id = self._pauseMenuItem.GetId() )
        #Crea el menuItem Stop y lo agrega al menu Data Display
        self._stopMenuItem = wx.MenuItem( self._menuDisplay, wx.ID_ANY, u"&Stop"+ u"\t" + u"Alt+Shift+S", wx.EmptyString, wx.ITEM_NORMAL )
        self._menuDisplay.Append( self._stopMenuItem )
        self.Bind( wx.EVT_MENU, self._eventStop, id = self._stopMenuItem.GetId() )
        #Crea el menuItem Mark Point y lo agrega al menu Data Display
        self._markMenuItem = wx.MenuItem( self._menuDisplay, wx.ID_ANY, u"&Mark Point"+ u"\t" + u"Alt+Shift+M", wx.EmptyString, wx.ITEM_NORMAL )
        self._menuDisplay.Append( self._markMenuItem )
        self.Bind( wx.EVT_MENU, self._eventMarkPt, id = self._markMenuItem.GetId() )
        #Crea el menuItem Delete last mark y lo agrega al menu Data Display
        self._deleteLastMarkMenuItem = wx.MenuItem( self._menuDisplay, wx.ID_ANY, u"&Delete last mark"+u"\t"+u"Alt+Shift+D", wx.EmptyString, wx.ITEM_NORMAL )
        self._menuDisplay.Append( self._deleteLastMarkMenuItem )
        self.Bind( wx.EVT_MENU, self._eventDeleteLastMark, id = self._deleteLastMarkMenuItem.GetId() )
        #Crea el menuItem Stop y lo agrega al menu Data Display
        self._dataGridMenuItem = wx.MenuItem( self._menuDisplay, wx.ID_ANY, u"&Data Grid"+ u"\t" + u"Alt+Shift+G", wx.EmptyString, wx.ITEM_CHECK )
        self._menuDisplay.Append( self._dataGridMenuItem )
        self.Bind( wx.EVT_MENU, self._eventDataParamPlot, id = self._dataGridMenuItem.GetId() )
        
#Agrega el menu Data Display a la menuBar
        self._menubar.Append( self._menuDisplay, u"Data Display" ) 
#Crea el menu Data Operations
        self._menuDataOp = wx.Menu()
#    #Crea el submenu Vertical Limit
#        self._vertLimitSubMenu = wx.Menu()
#        #Crea el menuItem Lower Limit y lo agrega al submenu Vertical Limit
#        self._vLLimitMenuItem = wx.MenuItem( self._vertLimitSubMenu, wx.ID_ANY, u"Lower Limit"+ u"\t" + u"Alt+Shift+V", wx.EmptyString, wx.ITEM_NORMAL )
#        self._vertLimitSubMenu.Append( self._vLLimitMenuItem )
#        self.Bind( wx.EVT_MENU, self._eventVLLimitSelect, id = self._vLLimitMenuItem.GetId() )
#        #Crea el menuItem Upper Limit y lo agrega al submenu Vertical Limit
#        self._vULimitMenuItem = wx.MenuItem( self._vertLimitSubMenu, wx.ID_ANY, u"Upper Limit"+ u"\t" + u"Alt+Shift+V", u"Set focus on the upper vertical limit slider bar.", wx.ITEM_NORMAL )
#        self._vertLimitSubMenu.Append( self._vULimitMenuItem )
#        self.Bind( wx.EVT_MENU, self._eventVULimitSelect, id = self._vULimitMenuItem.GetId() )
#    #Agrega el submenu Vertical Limit al menu Data Operations
#        self._menuDataOp.AppendSubMenu( self._vertLimitSubMenu, u"Vertical Limit" )
    #Crea el submenu Horizontal Limit
        self._horLimitSubMenu = wx.Menu()
        #Crea el menuItem Lower Limit y lo agrega al submenu Horizontal Limit
        self._hLLimitMenuItem = wx.MenuItem( self._horLimitSubMenu, wx.ID_ANY, u"Lower Limit"+ u"\t" + u"Alt+Shift+H", wx.EmptyString, wx.ITEM_NORMAL )
        self._horLimitSubMenu.Append( self._hLLimitMenuItem )
        self.Bind( wx.EVT_MENU, self._eventHLLimitSelect, id = self._hLLimitMenuItem.GetId() )
        #Crea el menuItem Upper Limit y lo agrega al submenu Horizontal Limit
        self._hULimitMenuItem = wx.MenuItem( self._horLimitSubMenu, wx.ID_ANY, u"Upper Limit"+ u"\t" + u"Alt+Shift+H", wx.EmptyString, wx.ITEM_NORMAL )
        self._horLimitSubMenu.Append( self._hULimitMenuItem )
        self.Bind( wx.EVT_MENU, self._eventHULimitSelect, id = self._hULimitMenuItem.GetId() )
    #Agrega el submenu Horizontal Limit al menu Data Operations
        self._menuDataOp.AppendSubMenu( self._horLimitSubMenu, u"Horizontal Limit" )
    #Crea el submenu Mathematical Functions
        self._matFuncSubMenu = wx.Menu()
        #Crea el menuItem Original y lo agrega al submenu Mathematical Functions
        self._originalMFMenuItem = wx.MenuItem( self._matFuncSubMenu, wx.ID_ANY, u"&Original"+ u"\t" + u"Alt+Shift+O", wx.EmptyString, wx.ITEM_NORMAL )
        self._matFuncSubMenu.Append( self._originalMFMenuItem )
        self.Bind( wx.EVT_MENU, self._eventMFOriginal, id = self._originalMFMenuItem.GetId() )
        #Crea el menuItem last cut y lo agrega al subsubmenu Mathematical Functions
        self._lastCutMenuItem = wx.MenuItem( self._matFuncSubMenu, wx.ID_ANY, u"Previous Cut"+ u"\t" + u"Alt+Shift+C", wx.EmptyString, wx.ITEM_NORMAL )
        self._matFuncSubMenu.Append( self._lastCutMenuItem )
        self.Bind( wx.EVT_MENU, self._eventMFLastCut, id = self._lastCutMenuItem.GetId() )
        #Crea el menuItem Inverse y lo agrega al submenu Mathematical Functions
        self._inverseMFMenuItem = wx.MenuItem( self._matFuncSubMenu, wx.ID_ANY, u"&Inverse"+ u"\t" + u"Alt+Shift+I", wx.EmptyString, wx.ITEM_NORMAL )
        self._matFuncSubMenu.Append( self._inverseMFMenuItem )
        self.Bind( wx.EVT_MENU, self._eventMFInverse, id = self._inverseMFMenuItem.GetId() )
        #Crea el menuItem Play Backward y lo agrega al submenu Mathematical Functions
#        self._playBackMFMenuItem = wx.MenuItem( self._matFuncSubMenu, wx.ID_ANY, u"&Play Backward"+ u"\t" + u"", wx.EmptyString, wx.ITEM_NORMAL )
#        self._matFuncSubMenu.Append( self._playBackMFMenuItem )
#        self.Bind( wx.EVT_MENU, self._eventMFPlayBack, id = self._playBackMFMenuItem.GetId() )
        #Crea el menuItem Square y lo agrega al submenu Mathematical Functions
        self._squareMFMenuItem = wx.MenuItem( self._matFuncSubMenu, wx.ID_ANY, u"Square"+ u"\t" + u"Alt+Shift+2", wx.EmptyString, wx.ITEM_NORMAL )
        self._matFuncSubMenu.Append( self._squareMFMenuItem )
        self.Bind( wx.EVT_MENU, self._eventMFSquare, id = self._squareMFMenuItem.GetId() )
        #Crea el menuItem Square y lo agrega al submenu Mathematical Functions
        self._squareRotMFMenuItem = wx.MenuItem( self._matFuncSubMenu, wx.ID_ANY, u"Square root"+ u"\t" + u"Alt+Shift+R", wx.EmptyString, wx.ITEM_NORMAL )
        self._matFuncSubMenu.Append( self._squareRotMFMenuItem )
        self.Bind( wx.EVT_MENU, self._eventMFSquareRot, id = self._squareRotMFMenuItem.GetId() )
        #Crea el menuItem Logarithm y lo agrega al submenu Mathematical Functions
        self._logMFMenuItem = wx.MenuItem( self._matFuncSubMenu, wx.ID_ANY, u"Logarithm"+ u"\t" + u"Alt+Shift+L", wx.EmptyString, wx.ITEM_NORMAL )
        self._matFuncSubMenu.Append( self._logMFMenuItem )
        self.Bind( wx.EVT_MENU, self._eventMFLog, id = self._logMFMenuItem.GetId() )
        #Crea el menuItem Octave y lo agrega al submenu Mathematical Functions
        self._octaveMenuItem = wx.MenuItem( self._matFuncSubMenu, wx.ID_ANY, u"Octave"+ u"\t" + u"Alt+Shift+Y", wx.EmptyString, wx.ITEM_NORMAL )
        self._matFuncSubMenu.Append( self._octaveMenuItem )
        self.Bind( wx.EVT_MENU, self._eventOctaveSelect, id = self._octaveMenuItem.GetId() )
        #Crea el subsubmenu Average
        self._avFuncSubMenu = wx.Menu()
        #Crea el menuItem Number of Points y lo agrega al subsubmenu Average
        self._avNumPtsMFMenuItem = wx.MenuItem( self._avFuncSubMenu, wx.ID_ANY, u"Number of points"+ u"\t" + u"Alt+Shift+N", wx.EmptyString, wx.ITEM_NORMAL )
        self._avFuncSubMenu.Append( self._avNumPtsMFMenuItem )
        self.Bind( wx.EVT_MENU, self._eventAvNumPtsSelect, id = self._avNumPtsMFMenuItem.GetId() )
        #Crea el menuItem Apply average y lo agrega al subsubmenu Average
        self._averageMenuItem = wx.MenuItem( self._avFuncSubMenu, wx.ID_ANY, u"Apply average"+ u"\t" + u"Alt+Shift+A", wx.EmptyString, wx.ITEM_NORMAL )
        self._avFuncSubMenu.Append( self._averageMenuItem )
        self.Bind( wx.EVT_MENU, self._eventMFAverage, id = self._averageMenuItem.GetId() )
        #Agrega el subsubmenu Average al submenu Mathematical Functions
        self._matFuncSubMenu.AppendSubMenu( self._avFuncSubMenu, u"Average" )
#        #Crea el subsubmenu Octave
#        self._octaveSubMenu = wx.Menu()
#        #Crea el menuItem Output y lo agrega al subsubmenu Octave
#        self._octaveMenuItem = wx.MenuItem( self._octaveSubMenu, wx.ID_ANY, u"Output"+ u"\t" + u"Alt+Shift+Y", wx.EmptyString, wx.ITEM_NORMAL )
#        self._octaveSubMenu.Append( self._octaveMenuItem )
#        self.Bind( wx.EVT_MENU, self._eventOctaveSelect, id = self._octaveMenuItem.GetId() )
#        #Agrega el subsubmenu Octave al submenu Mathematical Functions
#        self._matFuncSubMenu.AppendSubMenu( self._octaveSubMenu, u"Octave" )
    #Agrega el submenu Mathematical Functions al menu Data Operations
        self._menuDataOp.AppendSubMenu( self._matFuncSubMenu, u"Mathematical Functions" )
#Agrega el menu Data Operations a la menubar
        self._menubar.Append( self._menuDataOp, u"Data Operations" ) 
#Crea el menu Panels
        self._menuConfigPanels = wx.Menu()
        #Crea el menuItem File y lo agrega al menu Panels
        self._cpFileMenuItem = wx.MenuItem( self._menuConfigPanels, wx.ID_ANY, u"File"+ u"\t" + u"Ctrl+Alt+F", wx.EmptyString, wx.ITEM_CHECK )
        self._menuConfigPanels.Append( self._cpFileMenuItem )
        self.Bind( wx.EVT_MENU, self._eventCPFileSelect, id = self._cpFileMenuItem.GetId() )
        #crea el menuItem Data Display y lo agrega al menu Panels
        self._cpDataDisplayMenuItem = wx.MenuItem( self._menuConfigPanels, wx.ID_ANY, u"Data Display"+ u"\t" + u"Ctrl+Alt+D", wx.EmptyString, wx.ITEM_CHECK )
        self._menuConfigPanels.Append( self._cpDataDisplayMenuItem )
        self.Bind( wx.EVT_MENU, self._eventCPDataDisplaySelect, id = self._cpDataDisplayMenuItem.GetId() )
        self._cpDataDisplayMenuItem.Check(True)
        #Crea el data parameters panel
        self._dataParamPlotMenuItem = wx.MenuItem( self._menuConfigPanels, wx.ID_ANY, u"&Data Parameters"+ u"\t" + u"Alt+Shift+G", wx.EmptyString, wx.ITEM_CHECK )
        self._menuConfigPanels.Append( self._dataParamPlotMenuItem )
        self.Bind( wx.EVT_MENU, self._eventDataParamPlot, id = self._dataParamPlotMenuItem.GetId() )
    #Crea el submenu Data Operations
        self._cpDataOpSubMenu = wx.Menu()
        #Crea el menuItem All Data Operations y lo agrega al submenu Data Operations
        self._cpDataOpMenuItem = wx.MenuItem( self._cpDataOpSubMenu, wx.ID_ANY, u"All Data Operations"+ u"\t" + u"Ctrl+Alt+T", wx.EmptyString, wx.ITEM_CHECK )
        self._cpDataOpSubMenu.Append( self._cpDataOpMenuItem )
        self.Bind( wx.EVT_MENU, self._eventCPDataOpSelect, id = self._cpDataOpMenuItem.GetId() )
        #Crea el menuItem Octave y lo agrega al submenu Data Operations
        self._cpDOOctaveMenuItem = wx.MenuItem( self._cpDataOpSubMenu, wx.ID_ANY, u"Octave"+ u"\t" + u"Alt+Shift+Y", wx.EmptyString, wx.ITEM_CHECK )
        self._cpDataOpSubMenu.Append( self._cpDOOctaveMenuItem )
        self.Bind( wx.EVT_MENU, self._eventCPDOOctaveSelect, id = self._cpDOOctaveMenuItem.GetId() )
        #Crea el menuItem Sliders and Mathematical Functions y lo agrega al submenu Data Operations
        self._cpDOSliderMenuItem = wx.MenuItem( self._cpDataOpSubMenu, wx.ID_ANY, u"Sliders and Mathematical Functions"+ u"\t" + u"Ctrl+Alt+X", wx.EmptyString, wx.ITEM_CHECK )
        self._cpDataOpSubMenu.Append( self._cpDOSliderMenuItem )
        self.Bind( wx.EVT_MENU, self._eventCPDOSliderSelect, id = self._cpDOSliderMenuItem.GetId() )
    #Agrega el submenu Data Operation al menu Panels
        self._menuConfigPanels.AppendSubMenu( self._cpDataOpSubMenu, u"Data Operations" )
    #Crea el submenu Configuration
        self._cpConfigSubMenu = wx.Menu()
        #Crea el menuItem All configurations y lo agrega al submenu Configuration
        self._cpCAllMenuItem = wx.MenuItem( self._cpConfigSubMenu, wx.ID_ANY, u"All configurations"+ u"\t" + u"Ctrl+Alt+C", wx.EmptyString, wx.ITEM_CHECK )
        self._cpConfigSubMenu.Append( self._cpCAllMenuItem )
        self.Bind( wx.EVT_MENU, self._eventCPCAllSelect, id = self._cpCAllMenuItem.GetId() )
        #Crea el menuItem Sound Configurations y lo agrega al submenu Configuration
        self._cpCSoundMenuItem = wx.MenuItem( self._cpConfigSubMenu, wx.ID_ANY, u"Sound Configurations"+ u"\t" + u"Ctrl+Alt+L", wx.EmptyString, wx.ITEM_CHECK )
        self._cpConfigSubMenu.Append( self._cpCSoundMenuItem )
        self.Bind( wx.EVT_MENU, self._eventCPCSoundSelect, id = self._cpCSoundMenuItem.GetId() )
        #Crea el menuItem Plot Configurations y lo agrega al submenu Configuration
        self._cpCPlotMenuItem = wx.MenuItem( self._cpConfigSubMenu, wx.ID_ANY, u"Plot Configurations"+ u"\t" + u"Ctrl+Alt+G", wx.EmptyString, wx.ITEM_CHECK )
        self._cpConfigSubMenu.Append( self._cpCPlotMenuItem )
        self.Bind( wx.EVT_MENU, self._eventCPCPlotSelect, id = self._cpCPlotMenuItem.GetId() )
        #Crea el menuItem Visual configuratons y lo agrega al submenu Configuration **Todavia no se implementa
        self._cpCVisualMenuItem = wx.MenuItem( self._cpConfigSubMenu, wx.ID_ANY, u"Visual configuratons"+ u"\t" + u"Ctrl+Alt+V", wx.EmptyString, wx.ITEM_CHECK )
#        self._cpConfigSubMenu.Append( self._cpCVisualMenuItem )
        self.Bind( wx.EVT_MENU, self._eventCPCVisualSelect, id = self._cpCVisualMenuItem.GetId() )
    #Agrega el submenu Configuration al menu Panels
        self._menuConfigPanels.AppendSubMenu( self._cpConfigSubMenu, u"Configuration" )
#Agrega el menu Panels a la menubar
        self._menubar.Append( self._menuConfigPanels, u"Panels" ) 
#Crea el menu Settings
        self._menuSettings = wx.Menu()
    #crea el submenu Sound
        self._soundSubMenu = wx.Menu()
        #crea el menuItem Sound Font y lo agrega al submenu Sound
        self._soundFontMenuItem = wx.MenuItem( self._soundSubMenu, wx.ID_ANY, u"Sound Font", wx.EmptyString, wx.ITEM_NORMAL )
        self._soundSubMenu.Append( self._soundFontMenuItem )
        self.Bind( wx.EVT_MENU, self._eventSFSelect, id = self._soundFontMenuItem.GetId() )
        #crea el menuItem Instrument y lo agrega al submenu Sound
        self._instrumentMenuItem = wx.MenuItem( self._soundSubMenu, wx.ID_ANY, u"Instrument", wx.EmptyString, wx.ITEM_NORMAL )
        self._soundSubMenu.Append( self._instrumentMenuItem )
        self.Bind( wx.EVT_MENU, self._eventSSInstSelect, id = self._instrumentMenuItem.GetId() )
#        #crea el subsubmenu Instrument
#        self._instrumentSubMenu = wx.Menu()
#        #crea el menuItem Piano y lo agrega al subsubmenu Instrument
#        self._instPianoMenuItem = wx.MenuItem( self._instrumentSubMenu, wx.ID_ANY, u"Piano", wx.EmptyString, wx.ITEM_NORMAL )
#        self._instrumentSubMenu.Append( self._instPianoMenuItem )
#        self.Bind( wx.EVT_MENU, self._eventInstPiano, id = self._instPianoMenuItem.GetId() )
#        #crea el menuItem Other y lo agrega al subsubmenu Instrument
#        self._instOtherMenuItem = wx.MenuItem( self._instrumentSubMenu, wx.ID_ANY, u"Other", wx.EmptyString, wx.ITEM_NORMAL )
#        self._instrumentSubMenu.Append( self._instOtherMenuItem )
#        self.Bind( wx.EVT_MENU, self._eventInstOther, id = self._instOtherMenuItem.GetId() )
#        #crea el menuItem Select on Panel y lo agrega al subsubmenu Instrument
#        self._instSelectMenuItem = wx.MenuItem( self._instrumentSubMenu, wx.ID_ANY, u"Select on panel"+ u"\t" + u"Ctrl+Alt+I", wx.EmptyString, wx.ITEM_NORMAL )
#        self._instrumentSubMenu.Append( self._instSelectMenuItem )
#        self.Bind( wx.EVT_MENU, self._eventSSInstSelect, id = self._instSelectMenuItem.GetId() )
#        #Agrega el subsubmenu Instrument al submenu Sound
#        self._soundSubMenu.AppendSubMenu( self._instrumentSubMenu, u"Intrument" )
    #Agrega el submenu Sound al menu Settings
        self._menuSettings.AppendSubMenu( self._soundSubMenu, u"Sound" )
    #crea el submenu Plot
        self._plotSubMenu = wx.Menu()
        #crea el menuItem Plot line style y lo agrega al submenu Plot Styles
        self._plotLineMenuItem = wx.MenuItem( self._plotSubMenu, wx.ID_ANY, u"Plot line style", wx.EmptyString, wx.ITEM_NORMAL )
        self._plotSubMenu.Append( self._plotLineMenuItem )
        self.Bind( wx.EVT_MENU, self._eventLineStyleSelect, id = self._plotLineMenuItem.GetId() )
        #crea el menuItem Plot marker style y lo agrega al submenu Plot Styles
        self._plotMarkerMenuItem = wx.MenuItem( self._plotSubMenu, wx.ID_ANY, u"Plot marker style", wx.EmptyString, wx.ITEM_NORMAL )
        self._plotSubMenu.Append( self._plotMarkerMenuItem )
        self.Bind( wx.EVT_MENU, self._eventMarkerStyleSelect, id = self._plotMarkerMenuItem.GetId() )
        #crea el menuItem Plot color style y lo agrega al submenu Plot Styles
        self._plotColorMenuItem = wx.MenuItem( self._plotSubMenu, wx.ID_ANY, u"Plot color style", wx.EmptyString, wx.ITEM_NORMAL )
        self._plotSubMenu.Append( self._plotColorMenuItem )
        self.Bind( wx.EVT_MENU, self._eventColorStyleSelect, id = self._plotColorMenuItem.GetId() )
        #crea el menuItem grid option y lo agrega al submenu Plot Styles
        self._gridOpMenuItem = wx.MenuItem( self._plotSubMenu, wx.ID_ANY, u"Grid option", wx.EmptyString, wx.ITEM_CHECK )
        self._plotSubMenu.Append( self._gridOpMenuItem )
        self.Bind( wx.EVT_MENU, self._eventGridOpSelect, id = self._gridOpMenuItem.GetId() )
    #Agrega el submenu Plot Style al menu Settings
        self._menuSettings.AppendSubMenu( self._plotSubMenu, u"Plot Styles" )
#Agrega el menu Settings a la menubar
        self._menubar.Append( self._menuSettings, u"Settings" ) 
#Crea el menu Help
        self._menuHelp = wx.Menu()
        #Crea el menuItem About y lo agrega al menu Help
        self._aboutMenuItem = wx.MenuItem( self._menuHelp, wx.ID_ANY, u"About"+u"\t"+u"Ctrl+Alt+H", wx.EmptyString, wx.ITEM_NORMAL )
        self._menuHelp.Append( self._aboutMenuItem )
        self.Bind( wx.EVT_MENU, self._eventHAbout, id = self._aboutMenuItem.GetId() )
        #Crea el menuItem User manual y lo agrega al menu Help
        self._manualMenuItem = wx.MenuItem( self._menuHelp, wx.ID_ANY, u"User manual"+u"\t"+u"Ctrl+Alt+U", wx.EmptyString, wx.ITEM_NORMAL )
        self._menuHelp.Append( self._manualMenuItem )
        self.Bind( wx.EVT_MENU, self._eventHManual, id = self._manualMenuItem.GetId() )
#Agrega el menu Help a la menubar
        self._menubar.Append( self._menuHelp, u"Help" ) 
#Setea la menubar
        self.SetMenuBar( self._menubar )
    
    def _createToolBar(self):
        #Toolbar!! No se está utilizando.
        self._toolBar = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
        self._toolBar.SetToolBitmapSize( wx.Size( -1,30 ) )
        self._fileToggleBtn = wx.ToggleButton( self._toolBar, wx.ID_ANY, u"Show File", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._fileToggleBtn.SetValue( False ) 
        self._fileToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventGFile )
        self._toolBar.AddControl( self._fileToggleBtn )
        self._toolBar.AddSeparator()
        self._configToggleBtn = wx.ToggleButton( self._toolBar, wx.ID_ANY, u"Show Configuration", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._configToggleBtn.SetValue( False ) 
        self._configToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventGConfig )
        self._toolBar.AddControl( self._configToggleBtn )
        self._toolBar.AddSeparator()
        self._displayToggleBtn = wx.ToggleButton( self._toolBar, wx.ID_ANY, u"Hide Data Display", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._displayToggleBtn.SetValue( True ) 
        self._displayToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventGDisplay )
        self._toolBar.AddControl( self._displayToggleBtn )
        self._toolBar.AddSeparator()
        self._octaveToggleBtn = wx.ToggleButton( self._toolBar, wx.ID_ANY, u"Show octave", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._octaveToggleBtn.SetValue( False ) 
        self._octaveToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventOctaveToggle)
        self._toolBar.AddControl( self._octaveToggleBtn )
        self._toolBar.AddSeparator()
        self._sliderToggleBtn = wx.ToggleButton( self._toolBar, wx.ID_ANY, u"Show Sliders and Math Functions", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._sliderToggleBtn.SetValue( False ) 
        self._sliderToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventSliderToggle)
        self._toolBar.AddControl( self._sliderToggleBtn )
        self._toolBar.AddSeparator()
        self._toolBar.Realize()
        self._toolBar.Hide()
    
    def _createFilePanel(self, panel):
        #crea el panel File con su sizer(row(5)col(2)) sin seccion expandida
        self._filePanel = wx.Panel( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _fileFgSizer = wx.FlexGridSizer( 6, 1, 0, 0 )
        _fileFgSizer.SetFlexibleDirection( wx.BOTH )
        _fileFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
    #Crea el boton Open y lo agrega al sizer del panel File
        self._openButton = wx.Button( self._filePanel, wx.ID_ANY, u"&Open", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._openButton.Bind( wx.EVT_BUTTON, self._eventOpen )
        _fileFgSizer.Add( self._openButton, 0, wx.ALL, 5 )   
    #Crea el boton Delete all marks y lo agrega al sizer del panel File
        self._deleteAllMarksButton = wx.Button( self._filePanel, wx.ID_ANY, u"&Delete all marks", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._deleteAllMarksButton.Bind( wx.EVT_BUTTON, self._eventDeleteAllMark )
        _fileFgSizer.Add( self._deleteAllMarksButton, 0, wx.ALL, 5 )
    #Crea el boton Save Data y lo agrega al sizer del panel File
        self._saveDataButton = wx.Button( self._filePanel, wx.ID_ANY, u"Save &Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._saveDataButton.Bind( wx.EVT_BUTTON, self._eventSaveData )
        _fileFgSizer.Add( self._saveDataButton, 0, wx.ALL, 5 )
    #Crea el boton Save Marks y lo agrega al sizer del panel File
        self._saveMarksButton = wx.Button( self._filePanel, wx.ID_ANY, u"Save &Marks", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._saveMarksButton.Bind( wx.EVT_BUTTON, self._eventSaveMarks )
        _fileFgSizer.Add( self._saveMarksButton, 0, wx.ALL, 5 )
    #Crea el boton Save Sound y lo agrega al sizer del panel File
        self._saveSoundButton = wx.Button( self._filePanel, wx.ID_ANY, u"Save &Sound", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._saveSoundButton.Bind( wx.EVT_BUTTON, self._eventSaveSound )
        _fileFgSizer.Add( self._saveSoundButton, 0, wx.ALL, 5 )
    #Crea el boton Save Plot y lo agrega al sizer del panel File
        self._savePlotButton = wx.Button( self._filePanel, wx.ID_ANY, u"Save &Plot", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._savePlotButton.Bind( wx.EVT_BUTTON, self._eventSavePlot )
        _fileFgSizer.Add( self._savePlotButton, 0, wx.ALL, 5 )
    #Relaciona el sizer con el panel File y lo agrega al sizer del panel izquierdo
        self._filePanel.SetSizer( _fileFgSizer )
        self._filePanel.Layout()
        _fileFgSizer.Fit( self._filePanel )
        
    def _createConfigPanel(self, panel):
        #crea el panel Configuraciones con su sizer(row(2)col(2)) sin seccion expandida
        self._congifPanel = wx.Panel( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _configFgSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
        _configFgSizer.SetFlexibleDirection( wx.BOTH )
        _configFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
    #Crea el boton de dos estados Sound Configurations, lo setea como presionado y lo agrega al sizer del panel Configuraciones
        self._configSoundToggleBtn = wx.ToggleButton( self._congifPanel, wx.ID_ANY, u"Show Sound\nConfiguraton", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._configSoundToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventConfigSound )
        self._configSoundToggleBtn.SetValue( False )
        _configFgSizer.Add( self._configSoundToggleBtn, 0, wx.ALL, 5 )
    #Crea el panel para desplegar las configuraciones de sonido y su sizer(row(4)col(1)) sin seccion expandida
        self._soundFontPanel = wx.Panel( self._congifPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _soundFontFgSizer = wx.FlexGridSizer( 4, 1, 0, 0 )
        _soundFontFgSizer.SetFlexibleDirection( wx.BOTH )
        _soundFontFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea el espacio de texto con el label Sound Font y lo agrega al sizer del panel de configuración de sonido
        self._soundFontTextCtrl = wx.TextCtrl( self._soundFontPanel, wx.ID_ANY, u"Sound Font:", wx.DefaultPosition, wx.Size( 90,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._soundFontTextCtrl.SetEditable(0)
        _soundFontFgSizer.Add( self._soundFontTextCtrl, 0, wx.ALL, 5 )
        #Crea el espacio de texto donde se indicara la fuente de sonido que utiliza el programa para generar sonido y lo agrega al sizer del panel de configuración de sonido
        self._sFontTextCtrl = wx.TextCtrl( self._soundFontPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
        _soundFontFgSizer.Add( self._sFontTextCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        #Crea el espacio de texto con el label Select Instrument y lo agrega al sizer del panel de configuración de sonido
        self._instTextCtrl = wx.TextCtrl( self._soundFontPanel, wx.ID_ANY, u"Select Instrument:", wx.DefaultPosition, wx.Size( 130,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._instTextCtrl.SetEditable(0)
        _soundFontFgSizer.Add( self._instTextCtrl, 0, wx.ALL, 5 )
        #Crea un panel desplegable con una lista para poder seleccionar entre los instrumentos disponibles, y lo agrega al sizer del panel de configuración de sonido
        _instListBoxChoices = [  ]
        self._instListBox = wx.ListBox( self._soundFontPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, _instListBoxChoices, wx.LB_ALWAYS_SB )
        self._instListBox.Bind( wx.EVT_LISTBOX, self._eventSelectInst )
        _soundFontFgSizer.Add( self._instListBox, 0, wx.ALL|wx.EXPAND, 5 )
        #Relaciona el sizer con el panel de las configuraciones de sonido y lo agrega al sizer del panel de configuraciones
        self._soundFontPanel.SetSizer( _soundFontFgSizer )
        self._soundFontPanel.Layout()
        _soundFontFgSizer.Fit( self._soundFontPanel )
        _configFgSizer.Add( self._soundFontPanel, 1, wx.EXPAND |wx.ALL, 5 )
        self._soundFontPanel.Hide()
    #Crea el boton de dos estados Plot Configurations, lo setea como presionado y lo agrega al sizer del panel Configuraciones
        self._configPlotToggleBtn = wx.ToggleButton( self._congifPanel, wx.ID_ANY, u"Show Plot\nConfigurations", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._configPlotToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventConfigPlot )
        self._configPlotToggleBtn.SetValue( False ) 
        _configFgSizer.Add( self._configPlotToggleBtn, 0, wx.ALL, 5 )
    #Crea el panel para desplegar las configuraciones del grafico y su sizer(row(4)col(2)) sin seccion expandida
        self._configPlotPanel = wx.Panel( self._congifPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
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
        self._gridWidthSpinCtrl = wx.SpinCtrlDouble( self._plotGridPanel, wx.ID_ANY, u" ", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0, 100, 0.5, 0.1, name=u"Grid width spin control" )
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
        self._congifPanel.SetSizer( _configFgSizer )
        self._congifPanel.Layout()
        _configFgSizer.Fit( self._congifPanel )
        
    def _createDisplayPanel(self, panel):
        #Crea el panel Display con su sizer(row(3)col(1)) y con el cuadro (row(0)col(0)) expandido
        self._displayPanel = wx.Panel( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _displayFgSizer = wx.FlexGridSizer( 3, 1, 0, 0 )
        _displayFgSizer.AddGrowableCol( 0 )
        _displayFgSizer.AddGrowableRow( 0 )
        _displayFgSizer.SetFlexibleDirection( wx.BOTH )
        _displayFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
    #Crea el panel del grafico y un sizer para contener el grafico que se realizara con matplotlib
        self._graphicPanel = wx.Panel( self._displayPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,200 ), wx.TAB_TRAVERSAL ) 
        _matplotlibSizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        _matplotlibSizer.AddGrowableCol( 1 )
        _matplotlibSizer.AddGrowableRow( 0 )
        _matplotlibSizer.SetFlexibleDirection( wx.BOTH )
        _matplotlibSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self._createInputDataDisplayPanel(self._graphicPanel)
        _matplotlibSizer.Add( self._openPanel, 1, wx.EXPAND |wx.ALL, 5 ) #Cambiar al sizer correspondiente!!
        self._openPanel.Hide()
        
        #Crea la figura, el canvas que la contiene y agrega un subplot llamado axes que se utilizara el en codigo principal
        self._figure = Figure()
        self._axes = self._figure.add_subplot(111)
        self._canvas = FigureCanvas(self._graphicPanel, -1, self._figure)
        #Agrega el canvas que relaciona la figura con el panel al sizer del panel del grafico
        _matplotlibSizer.Add( self._canvas, 1, wx.EXPAND |wx.ALL, 5 )
        
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
        self._absPosTextCtrl = wx.TextCtrl( self._displayPanel, wx.ID_ANY, u"Abscissa Position:", wx.DefaultPosition, wx.Size( 125,30 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._absPosTextCtrl.SetEditable(0)
        _absPosFgSizer.Add( self._absPosTextCtrl, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
        #Crea la slider para setear la posicion en abscisas y la agrega al sizer correspondiente.
        self._absPosSlider = wx.Slider( self._displayPanel, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SL_HORIZONTAL | wx.SL_LABELS )
        #self._absPosSlider.Bind( wx.EVT_KEY_UP, self._eventAbsPos )
        self._absPosSlider.Bind( wx.EVT_SCROLL, self._eventAbsPos )
        self._absPosSlider.Bind( wx.EVT_SLIDER, self._eventAbsPos )
        self._absPosSlider.Bind( wx.EVT_KEY_DOWN, self._eventAbsPos )
        _absPosFgSizer.Add( self._absPosSlider, 0, wx.ALL|wx.EXPAND, 5 )
        #Relaciona el sizer de abscisas con el sizer de abscisas y tempo.
        _sliderDisplayGSizer.Add( _absPosFgSizer, 1, wx.EXPAND, 5 )
        #Crea el sizer para contener el label y la slider del tempo (row(1)col(2)), con la seccion (row(0)col(1)) expandida
        _soundVelFgSizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        _soundVelFgSizer.AddGrowableCol( 1 )
        _soundVelFgSizer.SetFlexibleDirection( wx.BOTH )
        _soundVelFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea un espacio de texto con el label Tempo y lo agrega al sizer contenedor de los objetos tempo
        self._soundVelTextCtrl = wx.TextCtrl( self._displayPanel, wx.ID_ANY, u"Tempo:", wx.DefaultPosition, wx.Size( 60,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        self._soundVelTextCtrl.SetEditable(0)
        self._soundVelTextCtrl.NavigateIn()
        _soundVelFgSizer.Add( self._soundVelTextCtrl, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
        #Crea una slider para modificar el tempo y la agrega al sizer contenedor de los objetos tempo
        self._soundVelSlider = wx.Slider( self._displayPanel, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL | wx.SL_LABELS )
        self._soundVelSlider.Bind( wx.EVT_KEY_UP, self._eventSoundVel )
        self._soundVelSlider.Bind( wx.EVT_SCROLL, self._eventSoundVel )
        _soundVelFgSizer.Add( self._soundVelSlider, 0, wx.ALL|wx.EXPAND, 5 )
        #Relaciona el sizer del tempo con el sizer de abscisas y tempo.
        _sliderDisplayGSizer.Add( _soundVelFgSizer, 1, wx.EXPAND, 5 )
        #Relaciona el sizer de las abscisas y tempo con el sizer del panel Display
        _displayFgSizer.Add( _sliderDisplayGSizer, 1, wx.EXPAND, 5 )
        
    #Crea el sizer de los botones de control de reproduccion sin panel contenedor (row(1)col(5))
        _buttonDisplayFgSizer = wx.FlexGridSizer( 1, 5, 0, 0 )
        _buttonDisplayFgSizer.SetFlexibleDirection( wx.BOTH )
        _buttonDisplayFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #Crea el boton Play y lo agrega al sizer de botones de control de reproduccion
        self._playButton = wx.ToggleButton( self._displayPanel, wx.ID_ANY, u"Play", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._playButton.SetValue(False)
        self._playButton.Bind( wx.EVT_TOGGLEBUTTON, self._eventPlay )
        _buttonDisplayFgSizer.Add( self._playButton, 0, wx.ALL, 5 )
#        #Crea el boton Pause y lo agrega al sizer de botones de control de reproduccion
#        self._pauseButton = wx.Button( self._displayPanel, wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.DefaultSize, 0 )
#        self._pauseButton.Bind( wx.EVT_BUTTON, self._eventPause )
#        _buttonDisplayFgSizer.Add( self._pauseButton, 0, wx.ALL, 5 )
        #Crea el boton Stop y lo agrega al sizer de botones de control de reproduccion
        self._stopButton = wx.Button( self._displayPanel, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._stopButton.Bind( wx.EVT_BUTTON, self._eventStop )
        _buttonDisplayFgSizer.Add( self._stopButton, 0, wx.ALL, 5 )
        #Crea el boton Mark Point y lo agrega al sizer de botones de control de reproduccion
        self._markPtButton = wx.Button( self._displayPanel, wx.ID_ANY, u"Mark Point", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._markPtButton.Bind( wx.EVT_BUTTON, self._eventMarkPt )
        _buttonDisplayFgSizer.Add( self._markPtButton, 0, wx.ALL, 5 )
        #Crea el boton Delete last mark y lo agrega al sizer de botones de control de reproduccion
        self._deleteLastPtButton = wx.Button( self._displayPanel, wx.ID_ANY, u"Delete last mark", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._deleteLastPtButton.Bind( wx.EVT_BUTTON, self._eventDeleteLastMark )
        _buttonDisplayFgSizer.Add( self._deleteLastPtButton, 0, wx.ALL, 5 )
        
        #Crea el boton Plot Data Options y lo agrega al sizer de botones de control de reproduccion
        self._dataParamPlotToggleBtn = wx.ToggleButton( self._displayPanel, wx.ID_ANY, u"Data Parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._dataParamPlotToggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self._eventDataParamPlot )
        _buttonDisplayFgSizer.Add( self._dataParamPlotToggleBtn, 0, wx.ALL, 5 )
        
        #Relaciona el sizer de botones de control de reproduccion con el sizer del panel Display
        _displayFgSizer.Add( _buttonDisplayFgSizer, 1, wx.ALIGN_CENTER, 5 )
        #Relaciona el panel Display con su propio sizer y lo agrega en el sizer del panel derecho
        self._displayPanel.SetSizer( _displayFgSizer )
        self._displayPanel.Layout()
        _displayFgSizer.Fit( self._displayPanel )
        
    def _createOperationPanel(self, panel):
        #Crea el panel Operation con su sizer(row(2)col(1)) y con el cuadro (row(0)col(0)) expandido
        self._operationPanel = wx.Panel( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        _operationFgSizer = wx.FlexGridSizer( 3, 1, 0, 0 )
        _operationFgSizer.AddGrowableCol( 0 )
        _operationFgSizer.AddGrowableRow( 1 )
        _operationFgSizer.SetFlexibleDirection( wx.BOTH )
        _operationFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
    #Crea el panel de la shell que se mantendrá oculto.
        self._pythonShellPanel = wx.Panel( self._operationPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
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
        
    #Crea el panel Gnu Octave con su sizer (row(1)col(2)) y con el cuadro (row(1)col(0)) expandido
        self._gnuOctavePanel = wx.Panel( self._operationPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
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
        self._sizersMFPanel = wx.Panel( self._operationPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
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
#        self._vAxisTextCtrl = wx.TextCtrl( self._sizersPanel, wx.ID_ANY, u"Vertical Axis:", wx.DefaultPosition, wx.DefaultSize, style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
#        _axisFgSizer.Add( self._vAxisTextCtrl, 0, wx.ALL, 5 )
#        #Crea un sizer (row(2)col(2)) para contener las slider del limite vertical, con la col(1) expandida
#        _vAxisFgSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
#        _vAxisFgSizer.AddGrowableCol( 1 )
#        _vAxisFgSizer.SetFlexibleDirection( wx.BOTH )
#        _vAxisFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
#        #Crea un cuadro de texto con el label Lower Limit y lo agrega al sizer del limite vertical
#        self._lvLimitTextCtrl = wx.TextCtrl( self._sizersPanel, wx.ID_ANY, u"Lower Limit:", wx.DefaultPosition, wx.DefaultSize, style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
#        _vAxisFgSizer.Add( self._lvLimitTextCtrl, 0, wx.ALL, 5 )
#        #Crea una slider para indicar el parametro minimo de corte vertical y lo agrega al sizer del limite vertical
#        self._lVLimitSlider = wx.Slider( self._sizersPanel, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL | wx.SL_LABELS)
#        self._lVLimitSlider.Bind( wx.EVT_KEY_UP, self._eventLVLimitSlider )
#        self._lVLimitSlider.Bind( wx.EVT_SCROLL, self._eventLVLimitSlider )
#        _vAxisFgSizer.Add( self._lVLimitSlider, 0, wx.EXPAND, 5 )
#        #Crea un cuadro de texto con el label Upper Limit y lo agrega al sizer del limite vertical
#        self._uvLimitTextCtrl = wx.TextCtrl( self._sizersPanel, wx.ID_ANY, u"Upper Limit:", wx.DefaultPosition, wx.DefaultSize, style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
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
        self._operationPanel.SetSizer( _operationFgSizer )
        self._operationPanel.Layout()
        _operationFgSizer.Fit( self._operationPanel )
        
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
        #Crea el panel del botón Open
        #self._openPanel = wx.Panel( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self._openPanel = wx.ScrolledWindow( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.TAB_TRAVERSAL )
        self._openPanel.SetScrollRate( 5, 5 )
        #self._openPanel.SetScrollbars(1, 1, 1, 1)
        self._openPanel.SetMinSize( wx.Size( 350,200 ) )
        _openButFgSizer = wx.FlexGridSizer( 5, 1, 0, 0 )
        _openButFgSizer.SetFlexibleDirection( wx.BOTH )
        _openButFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        #Crea el sizer para el título de los datos.
        _titleDataFgSizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        _titleDataFgSizer.AddGrowableCol( 1 )
        _titleDataFgSizer.SetFlexibleDirection( wx.BOTH )
        _titleDataFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self._titleDataTextCtrl = wx.TextCtrl( self._openPanel, wx.ID_ANY, u"Data title:", wx.DefaultPosition, wx.Size( 70,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL )
        self._titleDataTextCtrl.SetEditable(0)
        _titleDataFgSizer.Add( self._titleDataTextCtrl, 0, wx.ALL, 5 )
        self._titleEdDataTextCtrl = wx.TextCtrl( self._openPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self._titleEdDataTextCtrl.Bind( wx.EVT_TEXT_ENTER, self._eventTitleEdData )
        _titleDataFgSizer.Add( self._titleEdDataTextCtrl, 0, wx.EXPAND|wx.ALL, 5 )
        _openButFgSizer.Add( _titleDataFgSizer, 0, wx.EXPAND, 5 )
        
        #Create the check box for first line
        self._askLabelDataCheckBox = wx.CheckBox( self._openPanel, wx.ID_ANY, u"Is the first line the columns title?", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._askLabelDataCheckBox.Bind( wx.EVT_CHECKBOX, self._eventAskLabelData )
        _openButFgSizer.Add( self._askLabelDataCheckBox, 0, wx.ALL, 5 )
        self._askLabelDataCheckBox.Hide()
        
        #Create the grid for the data
        self._dataGrid = wx.grid.Grid( self._openPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
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
        _openButFgSizer.Add( self._dataGrid, 0, wx.EXPAND | wx.ALL, 5 )
        
        #Crea el sizer para los botones de la grilla
        _buttonsDataFgSizer = wx.FlexGridSizer( 1, 3, 0, 0 )
        _buttonsDataFgSizer.SetFlexibleDirection( wx.BOTH )
        _buttonsDataFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self._addGridChangesButton = wx.Button( self._openPanel, wx.ID_ANY, u"Update Column\n Names", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._addGridChangesButton.Bind( wx.EVT_BUTTON, self._eventAddGridChanges )
        _buttonsDataFgSizer.Add( self._addGridChangesButton, 0, wx.ALL, 5 )
        
        self._addGridUpdateButton = wx.Button( self._openPanel, wx.ID_ANY, u"Update Grid", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._addGridUpdateButton.Bind( wx.EVT_BUTTON, self._eventUpdateGrid )
        _buttonsDataFgSizer.Add( self._addGridUpdateButton, 0, wx.ALL, 5 )
        
        self._addGridOriginalButton = wx.Button( self._openPanel, wx.ID_ANY, u"Original Array", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._addGridOriginalButton.Bind( wx.EVT_BUTTON, self._eventOriginalGrid )
        _buttonsDataFgSizer.Add( self._addGridOriginalButton, 0, wx.ALL, 5 )
        
        _openButFgSizer.Add( _buttonsDataFgSizer, 0, wx.EXPAND, 5 )
        
    #Crea el sizer de los desplegables para elegir los ejes
        _axisChoiceFgSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
        
        _axisChoiceFgSizer.SetFlexibleDirection( wx.BOTH )
        _axisChoiceFgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self._axisChoiceXTextCtrl = wx.TextCtrl( self._openPanel, wx.ID_ANY, u"Axis X selection:", wx.DefaultPosition, wx.Size( 120,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        self._axisChoiceXTextCtrl.SetEditable(0)
        self._axisChoiceXTextCtrl.NavigateIn()
        _axisChoiceFgSizer.Add( self._axisChoiceXTextCtrl, 0, wx.ALL|wx.FIXED_MINSIZE, 5 )
        
        self._axisChoiceX = wx.ListBox( self._openPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size(120,60), [""], 0 )
        self._axisChoiceX.Bind( wx.EVT_LISTBOX, self._eventAxisChoiceX )
        self._axisChoiceX.SetSelection( 0 )
        _axisChoiceFgSizer.Add( self._axisChoiceX, 0, wx.ALL|wx.FIXED_MINSIZE, 5 )
        
        self._axisChoiceYTextCtrl = wx.TextCtrl( self._openPanel, wx.ID_ANY, u"Axis Y selection:", wx.DefaultPosition, wx.Size( 120,15 ), style=wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_RIGHT )
        self._axisChoiceYTextCtrl.SetEditable(0)
        self._axisChoiceYTextCtrl.NavigateIn()
        _axisChoiceFgSizer.Add( self._axisChoiceYTextCtrl, 0, wx.ALL|wx.FIXED_MINSIZE, 5 )
        
        self._axisChoiceY = wx.ListBox( self._openPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size(120,60), [""], 0 )
        self._axisChoiceY.Bind( wx.EVT_LISTBOX, self._eventAxisChoiceY )
        self._axisChoiceY.SetSelection( 0 )
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
    
    # Virtual event handlers, overide them in your derived class
    def _eventOpen( self, event ):
        event.Skip()
        
    def _eventTitleEdData( self, event ):
        event.Skip()
    
    def _eventAskLabelData( self, event ):
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
    
    def _eventDeleteAllMark( self, event ):
        event.Skip()
        
    def _eventSaveData( self, event ):
        event.Skip()
        
    def _eventSaveMarks( self, event ):
        event.Skip()
        
    def _eventSaveSound( self, event ):
        event.Skip()
        
    def _eventSavePlot( self, event ):
        event.Skip()
        
    def _OnClose( self, event ):
        event.Skip()
        
    def _eventClose( self, event ):
        event.Skip()

    def _eventAbsPosSelect( self, event ):
        event.Skip()

    def _eventTempoSelect( self, event ):
        event.Skip()

    def _eventPlay( self, event ):
        event.Skip()

#    def _eventPause( self, event ):
#        event.Skip()
        
    def _eventStop( self, event ):
        event.Skip()

    def _eventMarkPt( self, event ):
        event.Skip()
        
    def _eventDeleteLastMark( self, event ):
        event.Skip()

    def _eventDataParamPlot( self, event ):
        event.Skip()

#    def _eventVLLimitSelect( self, event ):
#        event.Skip()

#    def _eventVULimitSelect( self, event ):
#        event.Skip()

    def _eventHLLimitSelect( self, event ):
        event.Skip()

    def _eventHULimitSelect( self, event ):
        event.Skip()

    def _eventMFOriginal( self, event ):
        event.Skip()

    def _eventMFInverse( self, event ):
        event.Skip()

#    def _eventMFPlayBack( self, event ):
#        event.Skip()

    def _eventMFSquare( self, event ):
        event.Skip()
        
    def _eventMFSquareRot( self, event ):
        event.Skip()

    def _eventMFLog( self, event ):
        event.Skip()

    def _eventAvNumPtsSelect( self, event ):
        event.Skip()

    def _eventMFAverage( self, event ):
        event.Skip()

    def _eventMFLastCut( self, event ):
        event.Skip()

    def _eventOctaveSelect( self, event ):
        event.Skip()

    def _eventCPFileSelect( self, event ):
        event.Skip()

    def _eventCPDataDisplaySelect( self, event ):
        event.Skip()

    def _eventCPDataOpSelect( self, event ):
        event.Skip()

    def _eventCPDOOctaveSelect( self, event ):
        event.Skip()

    def _eventCPDOSliderSelect( self, event ):
        event.Skip()

    def _eventCPCAllSelect( self, event ):
        event.Skip()

    def _eventCPCSoundSelect( self, event ):
        event.Skip()

    def _eventCPCPlotSelect( self, event ):
        event.Skip()

    def _eventCPCVisualSelect( self, event ):
        event.Skip()
        
    def _eventSFSelect( self, event ):
        event.Skip()

#    def _eventInstPiano( self, event ):
#        event.Skip()
#
#    def _eventInstOther( self, event ):
#        event.Skip()

    def _eventSSInstSelect( self, event ):
        event.Skip()
        
    def _eventLineStyleSelect( self, event ):
        event.Skip()
        
    def _eventMarkerStyleSelect( self, event ):
        event.Skip()
        
    def _eventColorStyleSelect( self, event ):
        event.Skip()
        
    def _eventGridOpSelect( self, event ):
        event.Skip()
        
    def _eventHAbout( self, event ):
        event.Skip()
        
    def _eventHManual( self, event ):
        event.Skip()

    def _eventGFile( self, event ):
        event.Skip()

    def _eventGConfig( self, event ):
        event.Skip()

    def _eventGDisplay( self, event ):
        event.Skip()
        
    def _eventOctaveToggle( self, event ):
        event.Skip()
        
    def _eventSliderToggle( self, event ):
        event.Skip()

    def _eventConfigSound( self, event ):
        event.Skip()

    def _eventSelectInst( self, event ):
        event.Skip()

    def _eventAbsPos( self, event ):
        event.Skip()

    def _eventSoundVel( self, event ):
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

        _mainSizer = wx.BoxSizer( wx.VERTICAL )
        
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
    
        _mainSizer.Add( self.retrievePanel, 1, wx.EXPAND |wx.ALL, 5 )
        #Setea el sizer inicial
        self.SetSizer( _mainSizer )
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
