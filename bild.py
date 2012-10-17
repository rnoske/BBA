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
        
    def fit_Gauss(self, y, centerguess = 100, fitEnabled = False):
        """ Fit 1D Gauss function to Data
        
        y (npArray): Numpy array with equally spaced y data
        fitEnabled (bool): optional to plot data with pylab
        
        Returns:
            fitapramter (array)
            
        """
        B = 53 #B noise
        A = 150 #A Amplitude
        mu = centerguess # mu center
        sigma = 20 #sigma width
        coeffs = [B, A, mu, sigma]
        
        _max = len(y)-1
        x = np.linspace(0,_max, len(y))
        y = np.array(y)
        
        from scipy.optimize import curve_fit

        gauss = lambda x , b, a, mu, sigma: b+a*np.exp(-((x-mu)/sigma)**2)
        p, cov = curve_fit(gauss, x, y, p0=np.array(coeffs))
        
        #if fitting is neccessary
        if fitEnabled == True:
            myfit = lambda x: p[0]+p[1]*np.exp(-((x-p[2])/p[3])**2)
            import pylab as pl
            #pl.plot(x,y,'b.', x, myfit(x), 'r-')
            pl.plot(x,y)
            pl.plot(x,myfit(x))
            pl.show()
        return p

        
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
        #alt:
        _posMax = self.fit_Gauss(_roi, centerguess = _guessMax)
        #print _posMax
        _posMax = _posMax[2]
        #print _posMax

        #neu:
        """
        y = _roi
        _max = len(y)-1
        x = np.linspace(0,_max, len(y))
        n = 1 #1 gauss
        m = [_guessMax] #da nur ein gaus nur ein eintrag
        s = [10]
        
        param = self.fitter.multiGaussFit(x, y, n, m, s, plotflag = False)
        print param
        print type(param)
        """
        self.att['flammenhoeheGauss'] = (nullpunkt - _posMax) / aufloesung
        self.att['flammenhoeheGaussIndex'] = _posMax
        
class ColorBild(Bild):
    """
    Image class for handling color images. Inherits from Bild class
    """
        