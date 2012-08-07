# -*- coding: utf-8 -*-
#!/usr/bin/env python

#   Project:			SIGA
#   Component Name:		reqboxmodel
#   Language:			Python
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
#   Description:		This script it is a higher level wrapper of
#       reqboxfileparse for easier structures iteration
#
#   Limitations:		Error handling is not correctly implemented, time constraints
#	The code is not clean and elegant as it should, again, time constraints
#   Database tables used:	None 
#   Thread Safe:	        No
#   Extendable:			No
#   Platform Dependencies:	Linux (openSUSE used)
#   Compiler Options:

"""
    Requirements parser multifunctional tool.
    
    This program will load from a doc file an implied hierarchy or relations and will produce several ouputs

    Command Line Usage:
        reqbox {<option> <argument>}

    Options:
        -h, --help                          Print this help and exit.
        -l, --list <level>                  Prints items in that level
        
    Examples:
        reqbox.py --list-fun *
                                            Output: (Level 1)
                                            - 001 Manter Tipo de Verificacao de Item de Checklist
                                            - 002 Manter Carta de Convocacao / Comunicado
                                            - 003 Manter Remessa de Cartao de Identificacao
        reqbox.py --list-fun * list RFI *
                                            Output: (Level 2)
                                            - 001 Manter Tipo de Verificacao de Item de Checklist
                                                - RFI234. Manter tipo de verifica??o de item de checklist
                                            - 002 Manter Carta de Convocacao / Comunicado
                                            - 003 Manter Remessa de Cartao de Identificacao
        reqbox.py --list RFI *
                                            Output: (Level 2)
                                            - 001 Manter Tipo de Verificacao de Item de Checklist
                                                - RFI234. Manter tipo de verifica??o de item de checklist
                                            - 002 Manter Carta de Convocacao / Comunicado
                                            - 003 Manter Remessa de Cartao de Identificacao

        reqbox.py --list RFN
        reqbox.py --list RNF
        reqbox.py --list RNG
        reqbox.py --list WRF
"""

from collections import defaultdict
#from reqbox-model import defaultdict

#import defaultdict
import getopt
import logging
import sys
import os
import csv
import codecs
from vlog import vlogger
import reqboxfileparse as rfp
#from reqboxfileparse import reqboxfileparser

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

class reqmodel():
    """ Functionalities model
    Attributes:
        funid, funname, funbody: str
        funstart, funend: int
    """
    
    #def __init__(self):
    #    # Public
    #    self.reqid = None
    #    self.reqname = None
    #    self.reqbody = None
    #    self.reqstart = None
    #    self.reqend = None
    
    def __init__(self, funid, funname, funstart, funend):
        # Public
        self.reqid = funid
        self.reqname = funname
        self.reqbody = None
        self.reqstart = funstart
        self.reqend = funend
    
class funmodel():
    """ Functionalities model
    Attributes:
        rfi, rfn, rnf, rgn: dict
    """
    
    def __init__(self, funid, funname, funstart, funend):
        # Public
        self.fun = reqmodel(funid, funname, funstart, funend)
        self.rfi = {}
        self.rfistart = -1
        self.rfiend = -1
        self.rfn = {}
        self.rfnstart = -1
        self.rfnend = -1
        self.rnf = {}
        self.rnfstart = -1
        self.rnfend = -1
        self.rgn = {}
        self.rgnstart = -1
        self.rgnend = -1
        self.wrf = {}
        pass

class reqboxmodel():
    """ Reqbox model
    Attributes:
    """
    
    def __init__(self):
        # Public
        # Init structures
        self.fp = rfp.reqboxfileparser()
        self.fp.parsefile("./data/LRCv12.txt")
        
        # Init vlogger
        self.__verbosity = VERB_MAX
        self.vlog = vlogger(self.__verbosity, sys.stdout)
        #self.vlog = self.__log()
        
    def __del__(self):
        #del self.rfi
        del self.fp
        
    def printfun(self, idx, funstr):
        result = ""
        if not funstr in self.fun:
            # idx is just for debugging, to easily check which one doesn't exist
            # on the dict
            result = "ERROR %s [%s] not found, and it should exist!!!\n" % (idx, funstr)
        else:
            f = self.fun[funstr]

            result = "FUN id=%s [bytes=%d/%d]:\t'%s'\n" % (f.funid, f.funstart, f.funend, f.funname)
        return result
        
    def __str__(self):
        result = ""
        for idx, funstr in enumerate(self.fp.funlist):
            result = result + self.printfun(idx + 1, funstr)
        return result
        
    def parsefile(self, fname):
        # Init structures
        self.fp = rfp.reqboxfileparser()
        rfp.VERB_MAX = 10
        self.fp.parsefile(fname)

    def printdic(self, d):
        #if d == self.fp.fundict[funstr].rfi:
        #    prefix = "RFI"
        #elif d == self.fp.fundict[funstr].rfn:
        #    prefix = "RFN"        
        for idx, funstr in enumerate(sorted(d)):
            r = d[funstr]
            print("    - %s: '%s...' ('%s...%s', begin=%d, end=%d)" % (r.reqid, r.reqname[:20], r.reqbody[:15], r.reqbody[len(r.reqbody)-17:len(r.reqbody)-2], r.reqstart, r.reqend))

    def printf(self):
        for idx, funstr in enumerate(self.fp.funlist):
            print("FUN %d: %s" % (idx + 1, funstr))
            d = self.fp.fundict[funstr].rfi
            count = len(d)
            print("  %s [%d]" % ("RFI", count))
            self.printdic(d)
            
            d = self.fp.fundict[funstr].rfn
            count = len(d)
            print("  %s [%d]" % ("RFN", count))
            self.printdic(d)
            
            d = self.fp.fundict[funstr].rnf
            count = len(d)
            print("  %s [%d]" % ("RNF", count))
            self.printdic(d)
            
            d = self.fp.fundict[funstr].rgn
            count = len(d)
            print("  %s [%d]" % ("RGN", count))
            self.printdic(d)
        pass
    
    def exporter_rfi(self, fh):
        
        #if self.outfile != "":
        #    fh = open(self.outfile, 'wb')
        #else:
        #    fh = sys.stdout
            
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["Name", "Alias", "Type", "Notes", "Priority", "Author", ])
        
        for idx, funstr in enumerate(self.fp.funlist):
            d = self.fp.fundict[funstr].rfi
            for idx, reqstr in enumerate(sorted(d)):
                r = d[reqstr]
                
                #self.vlog(VERB_MED, "len = '%d'" % len(result.split(utf8("\t"))))
                row = [r.reqid + ". " + r.reqname, r.reqid, 'Requirement', r.reqbody, "Medium", "Albert De La Fuente"]
                
                #Name    Alias   Type    Notes   Priority        Author
                #RFI001. MANTER HOSPEDAGEM       RFI001. Requirement     "
                #O sistema deve disponibilizar uma interface para incluir, alterar, excluir e consultar hospedagens, contemplando os seguintes atributos:
                #* Código da hospedagem
                #* ...
                #"       Medium  Albert De La Fuente

                    
                    #self.logv(2, "parsedir().wftuple=" + str(wftuple))
                    #self.logv(2, "parsedir().wftuple=%s" .join(map(str, wftuple)))
                print("Writing...%s" % (r.reqid))
                csvhdlr.writerow(row)

    def exporter_rfn(self, fh):
        
        #if self.outfile != "":
        #    fh = open(self.outfile, 'wb')
        #else:
        #    fh = sys.stdout
            
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["Name", "Alias", "Type", "Notes", "Priority", "Author", ])
        
        for idx, funstr in enumerate(self.fp.funlist):
            d = self.fp.fundict[funstr].rfn
            for idx, reqstr in enumerate(sorted(d)):
                r = d[reqstr]
                
                #self.vlog(VERB_MED, "len = '%d'" % len(result.split(utf8("\t"))))
                row = [r.reqid + ". " + r.reqname, r.reqid, 'Requirement', r.reqbody, "Medium", "Albert De La Fuente"]
                
                #Name    Alias   Type    Notes   Priority        Author
                #RFI001. MANTER HOSPEDAGEM       RFI001. Requirement     "
                #O sistema deve disponibilizar uma interface para incluir, alterar, excluir e consultar hospedagens, contemplando os seguintes atributos:
                #* Código da hospedagem
                #* ...
                #"       Medium  Albert De La Fuente

                    
                    #self.logv(2, "parsedir().wftuple=" + str(wftuple))
                    #self.logv(2, "parsedir().wftuple=%s" .join(map(str, wftuple)))
                print("Writing...%s" % (r.reqid))
                csvhdlr.writerow(row)

def main(argv):
    rbm = reqboxmodel()
    rbm.printf()
    
    fh = open("rfi.csv", 'wb')
    rbm.exporter_rfi(fh)
    
    fh = open("rfn.csv", 'wb')
    rbm.exporter_rfn(fh)

if __name__ == "__main__":
    sys.exit(main(sys.argv))