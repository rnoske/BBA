# -*- coding: utf-8 -*-

"""
Basic bild class for handling taken images.
"""
"""
logging info:
DEBUG	Detailed information, typically of interest only when diagnosing problems.
INFO	Confirmation that things are working as expected.
WARNING	An indication that something unexpected happened, or indicative of 
    some problem in the near future (e.g. ‘disk space low’). The software is 
    still working as expected.
ERROR	Due to a more serious problem, the software has not been able to perform 
    some function.
CRITICAL	A serious error, indicating that the program itself may be unable 
    to continue running.
"""

#standard library imports
import logging
#import sys
import os
import threading
import math

#related third party imports
import numpy as np # NumPy (multidimensional arrays, linear algebra, ...)

#local application/library specific imports
import rnio
import fitter


#Scientific imports, idea taken from spyder

#import scipy as sp # SciPy (signal and image processing library)
#import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
#import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax
#from pylab import *              # Matplotlib's pylab interface
#ion()                            # Turned on Matplotlib's interactive mode



#Actual code
class Bild:
    """ Basic image class. All other images inherit from this class.
    
    Creates:
        bid (int) = bild id/number
    """
    lock = threading.Lock()
    bid_count = 0
    
    def __init__(self, pfad, **kwargs):
        """ Initialize attributes
        
        and example docstring
        Args:
            pfad (str): File path of image
        
        Kwargs:
            none (yet)
            
        Returns:
            nothing
            
        Creates:
            self.att (dic): empty dictionary for holding image attributes
            
        Raises:
            nothing
            
        Use me if you want to create an image
        
        """
        self.att = {} #attribute directory
        self.rnio = rnio.RnIo()
        self.fitter = fitter.Fitter()
        
        #checks if pfad is valid
        if os.path.exists(pfad) == True:
            self.pfad = str(pfad)
            logging.info('Image pfad was set: %s', pfad)
            self.calc_name()
            with Bild.lock:
                self.att['bid'] = Bild.bid_count
                Bild.bid_count += 1
        else:
            logging.warning('No file found under pfad %s. No image was opened',
                            pfad)
    
    def calc_name(self):
        """ Set a name for the image.
        
        """
        namen = str(self.pfad).split(os.sep)
        name = namen.pop()
        self.att['name']=name
        
    def open_image(self):
        """ Opens and returns an PIL image
        
        """
        #finde dateiendung
        _end = self.pfad.split('.')
        _end = _end.pop()
        
        #wenn Endung = .bmp, .jpg
        _endl1 = ['bmp', 'jpg']
        if _end in _endl1:
            _arr = self.rnio.read_Image_nparray(self.pfad)
            logging.info('Bild geoeffnet')
        else:
            logging.error('Dateiendung konnte nicht geoeffnet werden')
            
        return _arr
        
    def create_array(self):
        """ Create and numpy array from open image
        
        Returns:
            np.array
            
        """
        #self.att['hoehe'] = np.array(self.open_image()).shape[0]
        #self.att['breite'] = np.array(self.open_image()).shape[1]
        _arr = self.open_image()
        #_arr = _arr[0,:,:]
        return _arr
        
    def calc_totalInt(self):
        """ Calculate total Pixel count of image
        
        """
        _arr = self.create_array()
        self.att['totalInt'] = _arr.sum()
        hoehe = _arr.shape[0]
        breite = _arr.shape[1]
        _apx = breite * hoehe
        self.att['mittelint'] = self.att['totalInt'] / _apx
        
    def calc_flammenhoehe(self):
        """ Calculate flame height for image
        
        """
        #load needed Settings
        nullpunkt = int(self.sdict['nullpunkt'])
        flammenmitte = int(self.sdict['flammenmitte'])
        aufloesung = float(self.sdict['aufloesung'])
        _arr = self.create_array()
        
        #nehme nur blauen farbkanal
        if _arr.shape[2] > 1:
            _arr = _arr[:,:,2]
        
        #Check if nullpunkt and flammenmitte have valid values
        hoehe = _arr.shape[0]
        breite = _arr.shape[1]
        if nullpunkt < 0 or nullpunkt > hoehe:
            #print 'nullpunkt falsch'
            logging.error('Nullpunkt nicht innerhalb des Bildes')
        elif flammenmitte < 0 or flammenmitte > breite:
            #print 'flammenmitte falsch'
            logging.error('Flammenmitte nicht innerhalb des Bildes')

        #calculation
        #roi = arr[:,flammenmitte-breite:flammenmitte+breite]
        #roi = roi.sum(axis=1)
        _roi = _arr[:,flammenmitte]
        _posMax = np.argmax(_roi)
        #print _posMax
        self.att['flammenhoehe'] = (nullpunkt - _posMax) / aufloesung
        self.att['flammenhoeheIndex'] = _posMax

        
    def calc_flammenhoeheGauss(self):
        """ Calculate flame height with gauss fit
        
        """
        #load needed Settings
        nullpunkt = int(self.sdict['nullpunkt'])
        flammenmitte = int(self.sdict['flammenmitte'])
        aufloesung = float(self.sdict['aufloesung'])
        _arr = self.create_array()
        
        #nehme nur blauen farbkanal
        if _arr.shape[2] > 1:
            _arr = _arr[:,:,2]
        
        #Check if nullpunkt and flammenmitte have valid values
        hoehe = _arr.shape[0]
        breite = _arr.shape[1]
        if nullpunkt < 0 or nullpunkt > hoehe:
            #print 'nullpunkt falsch'
            logging.error('Nullpunkt nicht innerhalb des Bildes')
        elif flammenmitte < 0 or flammenmitte > breite:
            #print 'flammenmitte falsch'
            logging.error('Flammenmitte nicht innerhalb des Bildes')
        #Calculations
        _roi = _arr[:,flammenmitte]
        _guessMax = np.argmax(_roi)        
        # fitting process
        y = _roi
        _max = len(y)-1
        x = np.linspace(0,_max, len(y))
        n = 1 #1 gauss
        b = 1
        a = [50]
        m = [_guessMax] #da nur ein gaus nur ein eintrag
        s = [10]
        
        b, a, m, s = self.fitter.multi_gauss_fit(x, y, n, b, a, m, s, plotflag = False)
        #print b, a, m, s
        
        #defining flame attributes
        self.att['flammenhoeheGauss'] = (nullpunkt - m[0]) / aufloesung
        self.att['flammenhoeheGaussIndex'] = m[0] #_posMax
        self.att['flammenhoeheGaussVarianz'] = s[0] / aufloesung
        
    
    def calc_flammenbreite_single(self, roi):
        """ Calculate the flame width by fitting two gauss
        
        roi (np.array): horizontale roi des bildes
        """
        flammenmitte = int(self.sdict['flammenmitte'])
        
        guessleft = np.argmax(roi[:flammenmitte])
        guessright = np.argmax(roi[flammenmitte:]) + flammenmitte
        
        # fitting process
        y = roi
        _max = len(y)-1
        x = np.linspace(0,_max, len(y))
        n = 2 #2 gauss
        b = 10
        a = [50, 50]
        m = [guessleft, guessright] #da nur ein gaus nur ein eintrag
        s = [10, 10]
        
        b, a, m, s = self.fitter.multi_gauss_fit(x, y, n, b, a, m, s, plotflag = False)
        #print b, a, m, s
        print m, a
        return b, a, m, s
        
    
    def calc_flammenbreite(self):
        """ Calculate the flame width
        
        Creates:
            2D image
            
        """
        _arr = self.create_array()
        nullpunkt = int(self.sdict['nullpunkt'])
        
        if 'flammenhoeheIndex' in self.att.keys():
            flammenhoehe = self.att['flammenhoeheIndex']
        else:
            self.calc_flammenhoehe()
            flammenhoehe = self.att['flammenhoeheIndex']
        
        #nehme nur blauen farbkanal
        if _arr.shape[2] > 1:
            _arr = _arr[:,:,2]
            
        #schneide array zurecht:
        _arr = _arr[flammenhoehe:nullpunkt, :]
        
        #definiere testroi
        #print _arr.shape
        #troi = _arr[76, :]
        #b, a, m, s = self.calc_flammenbreite_single(troi)
        
        _tarea = [[0., 0.]]*_arr.shape[0]
        #print _arr.shape
        for i in xrange(_arr.shape[0]):
            #print i
            troi = _arr[i, :]
            b, a, m, s = self.calc_flammenbreite_single(troi)
            _tarea[i] = m
        
        return _tarea
      
    def calc_flammenoberflaecheGauss(self):
        """ Calculate the flame area
        
        """
        aufloesung = float(self.sdict['aufloesung'])
        
        _tarea = self.calc_flammenbreite()
        _tarea = np.array(_tarea)
        _left = _tarea[:,0]
        _right = _tarea[:,1]
        area = 0.0
        for i in xrange(len(_left)-1):
            area += math.sqrt((_left[i]-_left[i+1])**2 + 1)
            area += math.sqrt((_right[i]-_right[i+1])**2 + 1)
        area += _right[len(_right)-1] - _left[len(_left)-1]
        print area / aufloesung
        self.att['flammenoberflaecheGauss'] = area / aufloesung
        
        
class ColorBild(Bild):
    """
    Image class for handling color images. Inherits from Bild class
    """
        