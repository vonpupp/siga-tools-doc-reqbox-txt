# -*- coding: utf-8 -*-
#!/usr/bin/python3.1

#   Project:			SIGA
#   Component Name:		reqboxfileparse-ng
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
#   Description:		Next generation of reqboxfileparse.py
#
#   Limitations:		Error handling is not correctly implemented, time constraints
#	The code is not clean and elegant as it should, again, time constraints
#   Database tables used:	None 
#   Thread Safe:	        No
#   Extendable:			No
#   Platform Dependencies:	Linux (openSUSE used)
#   Compiler Options:		

"""
    Physical data parsing model... The next generation.
    This is not intended to be used directly on the commandline.
"""

import logging, sys, mmap, shutil, contextlib, codecs, re, csv
import reqboxmodel as model
from vlog import vlogger
from reqboxfileparse import reqboxfileparser

#sys.setdefaultencoding('utf-8')

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

PARSETYPE = 'utf8-win'
#PARSETYPE = 'utf8-win-crlf'

class reqboxfileparserng(reqboxfileparser):
    """ Requirements doc file parsing
    Attributes:
        - dir: objects imports dir
        - file: string
    """
    
    def __init__(self):
        # Public
        self.filename = ''
        self.funlist = []
        self.fundict = {}
        self.importsdir = ''
        
        # Init vlogger
        self.__verbosity = VERB_MAX
        self.vlog = vlogger(self.__verbosity, sys.stdout)
        #self.vlog = self.__log()
        
        # Init mmap
        self.__file = None
        self.__f = None
        pass

    def getfunlist(self):
        """
        Overrided method to load from a CSV file
        """
        self.vlog(VERB_MED, "-> %s" % __name__)
        
        self.funlist = []
        
        fh = open(self.importsdir + 'in-uc-objects.csv', 'rb')
        f = csv.reader(fh, delimiter=',')
        
        headers = f.next()
        #headers['workers', 'constant', 'age']
        #column = {}
        #for header in headers:
        #    column[header] = []
        #
        #for row in f:
        #    for header, value in zip(headers, row):
        #        column[header].append(value)

        for line in f:
            self.funlist += [line[2]]
            
        self.vlog(VERB_MED, "<- %s" % __name__)
        self.vlog(VERB_MAX, "result = %s" % (self.funlist))
        return self.funlist
    
    #---- mainline

def main(argv):
    rfp = reqboxfileparserng()
    rfp.importsdir = './data/'
    if rfp.parsingasutf8_win():# rfp.parsingasutf8_win():
        #rfp.parsefile("./data/LRCv12-utf8-win.txt") # SAVE AS UTF-8 in Win!!
        #rfp.parsefile("./data/LRCv12-utf8-dow2unix-l.txt")
        #rfp.parsefile("./data/LRCv12-win.txt")
        rfp.parsefile("./data/LRCv12.txt")
    elif self.parsingasutf8_win_crlf():
        #rfp = reqboxfileparser("./data/LRCv12-utf8-win.txt") # SAVE AS UTF-8 in Win!!
        #rfp = reqboxfileparser("./data/LRCv12-utf8-win-dos2unix.txt") # SAVE AS UTF-8 in Win!!
        rfp = reqboxfileparser("./data/LRCv12-utf8-crlf.txt") # SAVE AS UTF-8 in Win!!
        # Error on the body:
            #1.	MANTER TABELA DE RETENÇÃO TRIBUTÁRIA       
            #REQUISITOS FUNCIONAIS DE INTERFACE
            #Nome
            #Alias
            #Descrição
            #Critici
            #dade
            #RFI251. MANTER TABELA DE 
            #RETENÇÃO TRIBUTÁRIA
            #RFI25
            #1.
        #rfp = reqboxfileparser("./data/Rv12w.txt")
    else:
        #rfp = reqboxfileparser("./data/Rv12.txt")
        pass
    print("INPUT:   " + rfp.filename)
    
    #rfp.vlog(VERB_MED, "%d" % (rfp.fundict['Gerar Etiqueta de Destino']))
    #rfp.vlog(VERB_MED, "%d" % (rfp.fundict['Provisão para despesas futuras']))
    #rfp.printmap(rfp.fundict)
    #rfp.printfun("18", utf8("Manter Prontuário"))
    #rfp.printfun("43", utf8("Manter Plano de Ação"))
    rfp.vlog(VERB_MED, "rfp = \n%s" % (rfp))
    #rfp.getrfidic(utf8("Manter Tabela de Retenção Tributária"))
    del rfp

if __name__ == "__main__":
    sys.exit(main(sys.argv))
