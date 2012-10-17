# -*- coding: utf-8 -*-

#standard library imports
import logging
import sys

#related third party imports
from PyQt4 import QtGui, QtCore

#local application/library specific imports
import BBAgui #from BBAgui import Ui_BBA
import Settingsui #from Settingsui import Ui_Settings
from Plotterui import Ui_Plotterui
from progHandler import BBA

#import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
#import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax
#from pylab import *              # Matplotlib's pylab interface
#ion()                            # Turned on Matplotlib's interactive mode

#from matplotlib.figure import Figure
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from mplwidget import *

class guiHandler(QtGui.QMainWindow):
    """ Handler for function calls from gui
    
    """
    def __init__(self, parent=None):
        """ Simple initializsation
        
        """
        QtGui.QWidget.__init__(self, parent)
        self.ui = BBAgui.Ui_BBA()
        self.ui.setupUi(self)
        self.show()
        
        self.bba = BBA()
        
    
    def raysFunc(self):
        """ my testfunc
        
        now obsolete more or less
        
        """
        x = int(self.ui.lineEditX.text())
        y = int(self.ui.lineEditY.text())
        self.ui.lineEditZ.setText(str(x+y))

    def openImages(self):
        """ Responds to dialog to open images
        
        """
        _msg = 'Select one or more images to open'
        _prepath = 'D:/Raimund Buero/Python/testbilder'
        _Imagetypes = 'Images (*.bmp *.png *.jpg)'
        filepaths = QtGui.QFileDialog.getOpenFileNames(self, 
                                                      _msg,
                                                      _prepath, 
                                                      _Imagetypes)
        for filepath in filepaths:
            self.bba.add_image_bd(str(filepath))
        _nL = self.bba.get_imageName_list()
        for name in _nL:
            _fp = QtGui.QListWidgetItem(name, self.ui.ImageList)
            self.ui.ImageList.addItem(_fp)
            
        #Set Image settings
        try:
            self.setImageSettings()
        except:
            logging.error('Fehler beim schreiben der Settings beim \
            oeffnen der Datei')
            

    def filepathClicked(self):
        """ Responds to clicked image
        
        """
        _tmp = self.ui.ImageList.currentItem()
        _tmp = QtGui.QListWidgetItem.text(_tmp)
        #print _tmp
        self.ui.currentImage.setText(_tmp)
        _fp = self.bba.get_imageByName(str(_tmp)).pfad
        self.update_ImageDisplay(_fp)
        
    def update_ImageDisplay(self, pfad):
        """ updates the Image Display
        
        is called from self.filepathClicked()
        pfad (str): filepath for image to be displayed
        
        """
        image = QtGui.QPixmap(pfad)
        view = self.ui.BildViewer
        scene = QtGui.QGraphicsScene()
        item = QtGui.QGraphicsPixmapItem(image)
        scene.addItem(item)
        view.setScene(scene)
        view.show()
        
    #Settings function
    def openSettings(self, parent = None):
        """ Responds to open Settings call from Settings.ui
        
        """
        QtGui.QWidget.__init__(self, parent)
        self.sui = Settingsui.Ui_Settings()
        self.sui.setupUi(self)
        self.show()
        
        #Initialize values by reading Settings.ini
        self.loadSettings()

    def loadSettings(self):
        """ Respond to load settings call
        
        Reads values out of Settings.ini and sends them to gui
        
        """
        _setDict = self.bba.get_settings() #gets dict
        #Write to GUI
        try:
            #Nullpunkt
            _val = int(_setDict['nullpunkt'])
            self.sui.Nullhoehe.setValue(_val)
            #Flammenmitte
            _val = int(_setDict['flammenmitte'])
            self.sui.Flammenmitte.setValue(_val)
            #Grad zwischen den Bildern
            _val = int(_setDict['gradprobild'])
            self.sui.GradZwischenBildern.setValue(_val)
            #Aufloesung
            _val = float(_setDict['aufloesung'])
            self.sui.Aufloesung.setValue(_val)
            #Workspace
            _val = _setDict['workspace']
            self.sui.WorkspaceShow_label.setText(_val)
        except:
            logging.ERROR('Settings konnten nicht gesetzt werden')
    
    def saveSettings(self):
        """ Save current Settings in Settings.ini
        
        """
        _setDict = {}
        try:
            _setDict['nullpunkt'] = str(self.sui.Nullhoehe.value())
            _setDict['flammenmitte'] = str(self.sui.Flammenmitte.value())
            _setDict['gradprobild'] = str(self.sui.GradZwischenBildern.value())
            _setDict['aufloesung'] = str(self.sui.Aufloesung.value())
            _tmp = self.sui.WorkspaceShow_label.text()
            _tmp = str(_tmp)
            _setDict['workspace'] = _tmp
        except:
            logging.error('Settings konnten nicht von ui gelesen werden')
        
        try:
            self.bba.set_settings(_setDict)
        except:
            logging.error('Settings konnten nicht geschrieben werden')
            
    def setImageSettings(self):
        """ Send Settings to each Bild instance
        
        """
        self.bba.setImageSettings()
    
    def chooseWorkspace(self):
        """ File Dialog to choose current workspace
        
        """
        #_file = QtGui.QFileDialog.getOpenFileName(self, _msg, _prepath, _type)
        _dir = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        self.sui.WorkspaceShow_label.setText(_dir)
    
    #Plotter functions
    def openPlotter(self):
        """ Responds to open Plotter call from Plotter.ui
        
        """
        QtGui.QWidget.__init__(self, parent = None)
        self.pui = Ui_Plotterui()
        self.pui.setupUi(self)
        self.show()
        
        
    def updatePlot(self, x, y):
        """ Updates plot window
        
        x (arr): x values
        y (arr): y values
        
        """
        self.pui.MPLArea.qmc.updatePlot(x,y)
        
    def update_plot_verrbar(self, x, y, verrbar):
        """ update plot with vertical errorbars
        
        """
        self.pui.MPLArea.qmc.update_plot_verrbar(x, y, verrbar)
        
    def myPlot(self):
        # checked = 2 unchecked = 0
        if self.pui.checkTotalInt.checkState() == 2:
            self.plot_totalInt()
        elif self.pui.checkFlammenhoehe.checkState() == 2:
            self.plot_flammenhoehe()
        elif self.pui.checkFlammenhoeheGauss.checkState() == 2:
            self.plot_flammenhoeheGauss()
        else:
            self.test_plotter()
        
    def test_plotter(self):
        """ my testplotter func"""
        _x = [0,1]
        _y = [0,0]
        self.updatePlot(_x,_y)
        
    def plot_totalInt(self):
        """ Responds to plot total Int call
        
        """
        _x, _y = self.bba.get_totalInt_list()
        self.updatePlot(_x,_y)
        
    def plot_flammenhoehe(self):
        """ Responds to plot flammenhoehe call
        
        """
        _x, _y = self.bba.get_flammenhoehe_list()
        self.updatePlot(_x,_y)
        
    def plot_flammenhoeheGauss(self):
        """ Responds to plot flammenhoehe call
        
        """
        _x, _y, _yerr = self.bba.get_flammenhoeheGauss_list()
        self.update_plot_verrbar(_x,_y, _yerr)

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   myapp = guiHandler()
   sys.exit(app.exec_())
