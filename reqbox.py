# -*- coding: utf-8 -*-
#!/usr/bin/env python

#   Project:			SIGA
#   Component Name:		reqbox
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
#   Description:		This script will parse a full hierarchy from a path
#        and build a csv representing the wireframes from the project
#
#   Limitations:		Error handling is correctly implemented, time constraints
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
import reqboxmodel as rbm

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

class reqbox():
    """ Reqbox
    Attributes:
    """
    
    def __init__(self):
        # Public
        # Init structures
        self.rbm = rbm.reqboxmodel()
        self.inputfile = None
        self.parseall = 0
        self.parsefun = 0
        self.parserfi = 0
        self.parserfn = 0
        self.parsernf = 0
        self.parsergn = 0
        
        # Init vlogger
        self.__verbosity = VERB_MAX
        self.logv = vlogger(self.__verbosity, sys.stdout)
        #self.vlog = self.__log()
        
    def __del__(self):
        #del self.rfi
        del self.rbm

    def parsefunobjects(self, fn):
        fh = open(fn, 'wb')
        self.rbm.exporter_funobjects(fh)
        print "FUN objects exported to:\t" + fn
        
    def parserfiobjects(self, fn):
        fh = open(fn, 'wb')
        self.rbm.exporter_rfiobjects(fh)
        print "RFI objects exported to:\t" + fn
        
    def parserfnobjects(self, fn):
        self.rbm.builduniquerfndict()
        fh = open(fn, 'wb')
        self.rbm.exporter_rfnobjects(fh)
        print "RFN objects exported to:\t" + fn

    def parsernfobjects(self, fn):
        self.rbm.builduniquernfdict()
        fh = open(fn, 'wb')
        self.rbm.exporter_rnfobjects(fh)
        print "RFN objects exported to:\t" + fn
    
    def parsergnobjects(self, fn):
        self.rbm.builduniquergndict()
        fh = open(fn, 'wb')
        self.rbm.exporter_rgnobjects(fh)
        print "RNF objects exported to:\t" + fn
    
    def parsefunrfilinks(self, fn):
        fh = open(fn, 'wb')
        self.rbm.exporter_funrfilinks(fh)
        print "FUN-RFI links exported to:\t" + fn

    def parserfifunlinks(self, fn):
        fh = open(fn, 'wb')
        self.rbm.exporter_rfifunlinks(fh)
        print "RFI-FUN links exported to:\t" + fn

    def parsefunrfnlinks(self, fn):
        fh = open(fn, 'wb')
        self.rbm.exporter_funrfnlinks(fh)
        print "FUN-RFN links exported to:\t" + fn

    def parserfnfunlinks(self, fn):
        fh = open(fn, 'wb')
        self.rbm.exporter_rfnfunlinks(fh)
        print "RFN-FUN links exported to:\t" + fn

    def parsefunrgnlinks(self, fn):
        fh = open(fn, 'wb')
        self.rbm.exporter_funrgnlinks(fh)
        print "FUN-RGN links exported to:\t" + fn

    def parsergnfunlinks(self, fn):
        fh = open(fn, 'wb')
        self.rbm.exporter_rgnfunlinks(fh)
        print "RGN-FUN links exported to:\t" + fn

    def parsefunrnflinks(self, fn):
        fh = open(fn, 'wb')
        self.rbm.exporter_funrnflinks(fh)
        print "FUN-RNF links exported to:\t" + fn

    def parsernffunlinks(self, fn):
        fh = open(fn, 'wb')
        self.rbm.exporter_rnffunlinks(fh)
        print "RNF-FUN links exported to:\t" + fn

def main(argv):
    rb = reqbox()
    try:
        optlist, args = getopt.getopt(argv[1:], 'hv:aingo:', ['help', 'verbose', 'export-all', 'export-rfi', 'export-rfn', 'in-objects'])
    except getopt.GetoptError, msg:
        sys.stderr.write("reqbox: error: %s" % msg)
        sys.stderr.write("See 'reqbox --help'.\n")
        return 1
    
    if len(args) is not 1:
        sys.stderr.write("Not enough arguments. See 'reqbox --help'.\n")
        return 1
    
    for opt, optarg in optlist:
        if opt in ('-h', '--help'):
            sys.stdout.write(__doc__)
            return 0
        elif opt in ('-v', '--verbose'):
            #wfl.setVerbosity(int(optarg))
            #wfl.logv(VERB_MED, "main.optarg[%d]" % len(optlist))
            #wfl.logv(VERB_MED, "main.optarg = " .join(map(str, optarg)))
            #wfl.logv(VERB_MED, "main.optlist = " .join(map(str, optlist)))
            pass
        #elif opt in ('-a', '--export-all',
        #             '-i', '--export-rfi'):
        rb.inputfile = args[0]
        rb.parseall = rb.parseall or opt in ('-a', '--export-all')
        rb.parsefun = rb.parseall or rb.parsefun or opt in ('-f', '--export-fun')
        rb.parserfi = rb.parseall or rb.parserfi or opt in ('-i', '--export-rfi')
        rb.parserfn = rb.parseall or rb.parserfn or opt in ('-r', '--export-rfn')
        rb.parsernf = rb.parseall or rb.parsernf or opt in ('-n', '--export-rnf')
        rb.parsergn = rb.parseall or rb.parsergn or opt in ('-g', '--export-rgn')
        rb.inobjects = opt in ('-o', '--in-objects')
            #if wfl.isVerbose:
                #wfl.setLogger('/home/afu/Dropbox/mnt-ccb/siga/siga-tools/siga-tools-wf2ea/myapp.log')

    #rb.parsefun = rb.parsefun or rb.parseall
    #rb.parserfi = rb.parserfi or rb.parseall
    #rb.parserfn = rb.parserfn or rb.parseall
    #rb.parsernf = rb.parsernf or rb.parseall
    #rb.parsergn = rb.parsergn or rb.parseall
    
    rb.rbm.parsefile(rb.inputfile)
    
    if rb.parsefun:
        rb.parsefunobjects("out-fun-objects.csv")
        rb.parsefunrfilinks("out-fun-rfi-links.csv")
        rb.parsefunrfnlinks("out-fun-rfn-links.csv")
        rb.parsefunrgnlinks("out-fun-rgn-links.csv")
        rb.parsefunrnflinks("out-fun-rnf-links.csv")
    
    if rb.parserfi:
        rb.parserfiobjects("out-rfi-objects.csv")
        rb.parserfifunlinks("out-rfi-fun-links.csv")
    
    if rb.parserfn:
        rb.parserfnobjects("out-rfn-objects.csv")
        rb.parserfnfunlinks("out-rfn-fun-links.csv")

    if rb.parsergn:
        rb.parsergnobjects("out-rgn-objects.csv")
        rb.parsergnfunlinks("out-rgn-fun-links.csv")
    
    if rb.parsernf:
        rb.parsernfobjects("out-rnf-objects.csv")
        rb.parsernffunlinks("out-rnf-fun-links.csv")
        
    del rb
#    print "wfl.verbosity=" + str(wfl.__verbosity)

if __name__ == "__main__":
    sys.exit(main(sys.argv))