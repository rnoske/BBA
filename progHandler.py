# -*- coding: utf-8 -*-

"""
Handels the control of the underlying program
Excepts commands from guiHandler und translates them to
'useable' program function calls
"""
#from bilderarray import bilderarray
from bilderdict import bilderdict
from Config import Config

class BBA:
    """ Programm class that handles calls from guihandler
    
    """
    def __init__(self):
        """ Initialises bilderdict class
        
        """
        #self.ba = bilderarray()
        self.bd = bilderdict()
        self.cf = Config()
        
    def add_image_bd(self, filepath):
        """ Add one image to bilderarray class
        
        """
        self.bd.add_image_to_array(filepath)
        
    def get_imageName_list(self):
        """ Return Bild name list/array from a dict where a bild instance is 
            mapped to its bild name
            
        Return:
            array of bild names
        
        """
        _tmp = self.bd.bdict.keys()
        #_tmp = _tmp.values()
        return _tmp
        
    def get_imageByName(self, name):
        """ Return an Bild instance with the bild name as key
        
        """
        _tmp = self.bd.bdict[name]
        return _tmp
        
    def get_totalInt_list(self):
        """ Return an array with number and totalInt
        
        """
        _att = 'totalInt'
        _list = self.bd.get_attList(_att)
        _tmpX = []
        _tmpY = []
        for entry in _list:
            _tmpX.append(entry[0])
            _tmpY.append(entry[1])
        return _tmpX, _tmpY
        
    def get_flammenhoehe_list(self):
        """ Return an array with number and flammenhoehe
        
        """
        _att = 'flammenhoehe'
        _list = self.bd.get_attList(_att)
        _tmpX = []
        _tmpY = []
        for entry in _list:
            _tmpX.append(entry[0])
            _tmpY.append(entry[1])
        return _tmpX, _tmpY
        
    def get_flammenhoeheGauss_list(self):
        """ Return an array with number and flammenhoeheGauss
        
        """
        _att = 'flammenhoeheGauss'
        _list = self.bd.get_attList(_att)
        _tmpX = []
        _tmpY = []
        for entry in _list:
            _tmpX.append(entry[0])
            _tmpY.append(entry[1])
        return _tmpX, _tmpY
        
    #Settingsui handling
    def get_settings(self, section = 'FlameParameters'):
        """ Return an dictionaray of current Settings
        
        """
        self.cf.getConfigOptions(section) #reads config
        return self.cf.cfgdict #created dictionaray
        
    def set_settings(self, cfgdict, section = 'FlameParameters'):
        """ Save the dictionary to file
        
        """
        self.cf.writeConfigOptions(section, cfgdict)
        
    def setImageSettings(self):
        """ Set Settings to each Bild instance
        
        """
        _sdict = self.get_settings()
        self.bd.setImageSettings(_sdict)
        