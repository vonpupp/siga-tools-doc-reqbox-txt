# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys #as __sys
import logging
import traceback

class vlogger:
    def __init__(self, verbosity = 0, log = sys.stderr):
        self.__verbosity = verbosity
        self.__log = log
        #self.__log = logging.StreamHandler(log)
    
    def __call__(self, verbosity, msg):
        if verbosity <= self.__verbosity:
            #print(self.__log, '*' * verbosity)
            #string = '*' * verbosity
            #string = string + msg
            #self.__log.emit(string)
            #string = '*' * verbosity + msg
            #self.__log.write(string)
            print('*' * verbosity)
            print(msg)