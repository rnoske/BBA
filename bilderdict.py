# -*- coding: utf-8 -*-

import logging
from bild import Bild
import collections

class bilderdict:
    """ Dict class for holding and managing bild objects
    
    """
    def __init__(self):
        """ Create an empty orderd dict
        
        Creates:
            bdict (ordered dict)
        
        """
        self.bdict = collections.OrderedDict()
        
    def add_image_to_array(self, pfad):
        """ Add given image to dict
        
        prad (str): complete file path to image
        
        """
        _Bild = Bild(pfad)
        _name = _Bild.att['name']
        self.bdict[_name] = _Bild
        logging.info('Bild hinzugefuegt')
        
    def calc_totalInt(self):
        """ Calculate total Intensity for every image in the array
        
        """
        for k, v in self.bdict.iteritems():
            v.calc_totalInt()
            _msg = 'Total Int von ' + str(k) + ' wurde berechnet'
            logging.debug(_msg)
                
    def calc_flammenhoehe(self):
        """ Calculate flame height for every image in the dict
        
        """
        for k, v in self.bdict.iteritems():
            v.calc_flammenhoehe()
            _msg = 'Flammenhoehe von ' + str(k) + ' wurde berechnet'
            logging.debug(_msg)
                
    def calc_flammenhoeheGauss(self):
        """ Calculate flame height with Gauss function for every image in the dict
        
        """
        for k, v in self.bdict.iteritems():
            v.calc_flammenhoeheGauss()
            _msg = 'FlammenhoeheFauss von ' + str(k) + ' wurde berechnet'
            logging.debug(_msg)
            
    def calc_flammenoberflaecheGauss(self):
        """ Calculate flame area with Gauss function for every image in the dict
        
        """
        for k, v in self.bdict.iteritems():
            v.calc_flammenoberflaecheGauss()
            _msg = 'FlammenoberflaecheGauss von ' + str(k) + ' wurde berechnet'
            logging.debug(_msg)
        
    def get_attList(self, attribute):
        """ Get attributes of images in the dict
        
        att (str): key of attribute which should be returned
        
        Return:
            array [bid, att]
            
        """
        #chooes which calculation to perform
        if attribute == 'totalInt':
            self.calc_totalInt()
        elif attribute == 'flammenhoehe':
            self.calc_flammenhoehe()
        elif attribute == 'flammenhoeheGauss':
            self.calc_flammenhoeheGauss()
        elif attribute == 'flammenoberflaecheGauss':
            self.calc_flammenoberflaecheGauss()
        
        _tmp = []
        #for every item in dictionary
        for k, v in self.bdict.iteritems():
            _entry = [v.att['bid'], v.att[attribute]]
            _tmp.append(_entry)
        return _tmp
        
    def setImageSettings(self, sdict):
        """ Set Image Settings for each Bild class instance
        
        sdict (dict): Settings dictionaray
        """
        for k, v in self.bdict.iteritems():
            try:
                v.sdict = sdict
            except:
                logging.error('Settings Dictionary konnte nicht zum Bild \
                hinzugefuegt werden')