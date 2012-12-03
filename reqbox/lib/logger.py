#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Project:			SIGA
#   Component Name:		flog
#   Language:			Python2
#
#   License: 			GNU Public License
#       This file is part of the project.
#	This is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#       without even the implied warranty of MERCHANTABILITY or
#       FITNESS FOR A PARTICULAR PURPOSE.
#       See the GNU General Public License for more details.
#       <http://www.gnu.org/licenses/>
#
#   Author:			Albert De La Fuente (www.albertdelafuente.com)
#   E-Mail:			http://www.google.com/recaptcha/mailhide/d?k=01eb_9W_IYJ4Pm_Y9ALRIPug==&c=L15IEH_kstH8WRWfqnRyeW4IDQuZPzNDRB0KCzMTbHQ=
#
#   Description:		
#                               
import logging

LOG_FILENAME = 'log-reqbox.log'
VERBOSITY_LEVEL = 2

class FileLog():
    """
    """
    
    def __init__(self, filename):
        self.log = logging.getLogger('reqbox-file')
        self.log.setLevel(logging.DEBUG)
        
        # create formatter and add it to the handlers
        self.formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(module)-10s %(message)s')
        
        # create file handler which logs even debug messages
        #logging.basicConfig(level=logging.DEBUG,
        #                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        #                    datefmt='%m-%d %H:%M',
        #                    filename='ccbinfo-scraper.log',
        #                    filemode='w')
        self.fh = logging.FileHandler(filename)
        #fh = logging.Handler.RotatingFileHandler(LOG_FILENAME,
        #                                          maxBytes=20, backupCount=5)
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(self.formatter)
        
        # add the handlers to flog
        self.log.addHandler(self.fh)
        

class ConsoleLog():
    """
    """
    
    def __init__(self):
        self.verbosity_level = 2
        self.log = logging.getLogger('reqbox-console')
        self.log.setLevel(logging.INFO)
        
        # create formatter and add it to the handlers
        self.formatter = logging.Formatter('%(message)s')
        
        # create file handler which logs even debug messages
        #logging.basicConfig(level=logging.DEBUG,
        #                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        #                    datefmt='%m-%d %H:%M',
        #                    filename='ccbinfo-scraper.log',
        #                    filemode='w')
        # create console handler with a higher log level
        self.ch = logging.StreamHandler()
        
        self.ch.setLevel(logging.INFO)
        self.ch.setFormatter(self.formatter)
        
        # add the handlers to flog
        self.log.addHandler(self.ch)

def log_setverbosity(lvl):
    global flog
    global clog
    clog.verbosity_level = lvl

def log_debug(msg):
    global flog
    global clog
    flog.log.debug(msg)
    clog.log.debug(msg)
    
def log_info(lvl, msg):
    global flog
    global clog
    left = (clog.verbosity_level - lvl) * ' '
    right = lvl * '*'
    indent = ' ' + ((lvl-1) * '  ')
    newmsg = left + right + indent + msg
    if lvl <= clog.verbosity_level:
        clog.log.info(newmsg)
#        flog.log.info(newmsg)

def flog_warning(msg):
    flog.warn(msg)

def flog_error(msg):
    flog.error(msg)

def flog_critical(msg):
    flog.critical(msg)
    
def get_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    msg = ''.join('!! ' + line for line in lines)
    return msg

def fun():
    sys._getframe().f_code.co_name


flog = FileLog(LOG_FILENAME)
clog = ConsoleLog()

def init():
    #flog2 = FileLog(LOG_FILENAME)
    pass

if __name__ == "reqbox.lib.logger":
    init()

