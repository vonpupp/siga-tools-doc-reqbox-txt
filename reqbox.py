#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
#   Description:		This script will create EA importable files
#                               from .txt (.doc) and .csv (.xls) requirements files
#
#   Limitations:		Error handling is correctly implemented, time constraints
#	The code is not clean and elegant as it should, again, time constraints
#   Database tables used:	None 
#   Thread Safe:	        No
#   Extendable:			No
#   Platform Dependencies:	Linux (openSUSE used)
#   Compiler Options:

__version__ = "8.0"
__author__ = "Albert De La Fuente (vonpupp@gmail.com)"
__copyright__ = "(C) 2012 Albert De La Fuente. GNU GPL 3."

"""
    Requirements parser multifunctional tool.
    
    This program will load from a doc file an implied hierarchy or relations and will produce several ouputs

    Command Line Usage:
        reqbox {<option> <argument>}

    Options:
        -h, --help                          Print this help and exit.
        -a, --export-all                    Parse all
        --parse-v1 / --parse-v2             Prints items in that level
        
    Examples:
        reqbox.py -a --parse-v2 ./data/LFv14.ms.default.fixed.txt
        
    Note:
        Please note that the csv files dir is hardcoded into the application
        to make command line arguments easier.
        
        The csv files are:
            - in-rfn-objects.csv
            - in-rgn-objects.csv
            - in-rnf-objects.csv
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
from reqbox.lib.vlog import vlogger
import reqbox.models.rbmodel7 as rbm1
import reqbox.models.rbmodel8 as rbm2
import reqbox.parsers.rbfileparser7 as rfp1
import reqbox.parsers.rbfileparser8 as rfp2
from reqbox.models.rbmodel7 import ReqBoxModel
from reqbox.models.rbmodel8 import ReqBoxModelNG
import reqbox.tests.rbmodel8_tests as rbt
import unittest
#import reqbox.models.rbmodel7 as rbm

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

class ReqBox():
    """ Reqbox
    Attributes:
    """
    
    def __init__(self):
        # Public
        # Init structures
        self.model = None
        self.inputfile = None
        self.inputdir = None
        self.parseall = 0
        self.parsefun = 0
        self.parserfi = 0
        self.parserfn = 0
        self.parsernf = 0
        self.parsergn = 0
        self.parseext = 0
        self.parseinc = 0
        self.parseimp = 0
        self.parserverion = 0
        self.runtests = 0
        self.stricttests = 0
        self.tests = None
        
        # Init vlogger
        self.__verbosity = VERB_MAX
        self.logv = vlogger(self.__verbosity, sys.stdout)
        #self.vlog = self.__log()
        
    def initparser(self, ModelClass):#, ParserClass):
        # Public
        # Init structures
        if ModelClass == rbm1.ReqBoxModel:
            ParserClass = rfp1.ReqBoxFileParser
        elif ModelClass is ReqBoxModelNG:
            ParserClass = rfp2.ReqBoxFileParserNG
        self.model = ModelClass(ParserClass)
        #self.model = rbm.ReqBoxModel(ParserClass)
        if ParserClass is rfp2.ReqBoxFileParserNG:
            self.model.fp.importsdir = self.inputdir
        
    def __del__(self):
        #del self.rfi
        del self.model

    def parsefunobjects(self, fn):
        fh = open(fn, 'wb')
        self.model.funobjectsexporter(fh)
        print "FUN objects exported to:\t" + fn
        
    def parserfiobjects(self, fn):
        fh = open(fn, 'wb')
        self.model.rfiobjectsexporter(fh)
        print "RFI objects exported to:\t" + fn
        
    def parserfnobjects(self, fn):
        self.model.builduniquerfndict()
        fh = open(fn, 'wb')
        self.model.rfnobjectsexporter(fh)
        print "RFN objects exported to:\t" + fn

    def parsernfobjects(self, fn):
        self.model.builduniquernfdict()
        fh = open(fn, 'wb')
        self.model.rnfobjectsexporter(fh)
        print "RFN objects exported to:\t" + fn
    
    def parsergnobjects(self, fn):
        self.model.builduniquergndict()
        fh = open(fn, 'wb')
        self.model.rgnobjectsexporter(fh)
        print "RNF objects exported to:\t" + fn
    
    def parsefunrfilinks(self, fn):
        fh = open(fn, 'wb')
        self.model.funrfilinksexporter(fh)
        print "FUN-RFI links exported to:\t" + fn

    def parserfifunlinks(self, fn):
        fh = open(fn, 'wb')
        self.model.rfifunlinksexporter(fh)
        print "RFI-FUN links exported to:\t" + fn

    def parsefunrfnlinks(self, fn):
        fh = open(fn, 'wb')
        self.model.funrfnlinksexporter(fh)
        print "FUN-RFN links exported to:\t" + fn

    def parserfnfunlinks(self, fn):
        fh = open(fn, 'wb')
        self.model.rfnfunlinksexporter(fh)
        print "RFN-FUN links exported to:\t" + fn

    def parsefunrgnlinks(self, fn):
        fh = open(fn, 'wb')
        self.model.funrgnlinksexporter(fh)
        print "FUN-RGN links exported to:\t" + fn

    def parsergnfunlinks(self, fn):
        fh = open(fn, 'wb')
        self.model.rgnfunlinksexporter(fh)
        print "RGN-FUN links exported to:\t" + fn

    def parsefunrnflinks(self, fn):
        fh = open(fn, 'wb')
        self.model.funrnflinksexporter(fh)
        print "FUN-RNF links exported to:\t" + fn

    def parsernffunlinks(self, fn):
        fh = open(fn, 'wb')
        self.model.rnffunlinksexporter(fh)
        print "RNF-FUN links exported to:\t" + fn

    # NG PARSER METHODS    
        
    def exportobjects(self, fn, d, exportercallback, objtype):
        fh = open(fn, 'wb')
        #fh = codecs.open(fn, encoding='utf-8', mode='w')
        self.model.objectsexporter(fh, d, exportercallback, objtype)
        print "Objects exported to:\t" + fn
        
    def exportobjectlinks(self, fname, direction, header, dictcallback, linktype):
        return self.model.exportobjectlinks(fname, direction, header, dictcallback,
                                            linktype)

    def exportrellinks(self, fname, direction, header, dictcallback, linktype):
        return self.model.exportrellinks(fname, direction, header, dictcallback,
                                            linktype)
        
def main(argv):
    try:
        optlist, args = getopt.getopt(argv, 'hv:aingo:t', ['help', 'verbose',
            'export-all', 'export-rfi', 'export-rfn', 'in-objects',
            'parse-v7', 'parse-v8', 'run-tests', 'strict-tests'])
    except getopt.GetoptError, msg:
        sys.stderr.write("reqbox: error: %s" % msg)
        sys.stderr.write("See 'reqbox --help'.\n")
        return 1
    
#    if len(args) is not 1:
#        sys.stderr.write("Not enough arguments. See 'reqbox --help'.\n")
#        return 1
    
    rb = ReqBox()
    rbm = rbm1.ReqBoxModel # Default parser
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
        elif opt in ('--parse-v7'):
            rbm = rbm1.ReqBoxModel
            #rbp = rfp1.ReqBoxFileParser
            rb.parserverion = 7
        elif opt in ('--parse-v8'):
            rbm = rbm2.ReqBoxModelNG
            #rbp = rfp2.ReqBoxFileParserNG
            rb.parserverion = 8
        elif opt in ('-o', '--in-objects'):
            rb.inputdir = optarg
        
        rb.inputfile = args[0]
        rb.parseall = rb.parseall or opt in ('-a', '--export-all')
        rb.parsefun = rb.parseall or rb.parsefun or opt in ('-f', '--export-fun')
        rb.parserfi = rb.parseall or rb.parserfi or opt in ('-i', '--export-rfi')
        rb.parserfn = rb.parseall or rb.parserfn or opt in ('-r', '--export-rfn')
        rb.parsernf = rb.parseall or rb.parsernf or opt in ('-n', '--export-rnf')
        rb.parsergn = rb.parseall or rb.parsergn or opt in ('-g', '--export-rgn')
        rb.parseext = rb.parseall or rb.parseext or opt in ('-e', '--export-ext')
        rb.parseinc = rb.parseall or rb.parseinc or opt in ('-n', '--export-inc')
        rb.parseimp = rb.parseall or rb.parseimp or opt in ('-m', '--export-imp')
        rb.runtests = rb.runtests or opt in ('-t', '--run-tests')
        rb.stricttests = rb.stricttests or opt == '--strict-tests'
        #rb.inobjects = rb.inobjects or opt in ('-o', '--in-objects')
            #if wfl.isVerbose:
                #wfl.setLogger('/home/afu/Dropbox/mnt-ccb/siga/siga-tools/siga-tools-wf2ea/myapp.log')

    #rb.parsefun = rb.parsefun or rb.parseall
    #rb.parserfi = rb.parserfi or rb.parseall
    #rb.parserfn = rb.parserfn or rb.parseall
    #rb.parsernf = rb.parsernf or rb.parseall
    #rb.parsergn = rb.parsergn or rb.parseall
    
    rb.initparser(rbm)
    rb.model.parsefile(rb.inputfile)
    
    if rb.parsefun and rb.parserverion == 7:
        rb.parsefunobjects("out-fun-objects.csv")
        rb.parsefunrfilinks("out-fun-rfi-links.csv")
        rb.parsefunrfnlinks("out-fun-rfn-links.csv")
        rb.parsefunrgnlinks("out-fun-rgn-links.csv")
        rb.parsefunrnflinks("out-fun-rnf-links.csv")
    elif rb.parsefun and rb.parserverion == 8:
        rb.exportobjects("out2-utf8-obj-fun.csv", rb.model.fp.fundict,
                         rb.model.funexportercallback, 'UseCase')
        rb.model.removereqcontent()
        #rb.parsefunrfilinks("out-fun-rfi-links.csv")
        #rb.parsefunrfnlinks("out-fun-rfn-links.csv")
        #rb.parsefunrgnlinks("out-fun-rgn-links.csv")
        #rb.parsefunrnflinks("out-fun-rnf-links.csv")
    
    if rb.parserfi and rb.parserverion == 7:
        rb.parserfiobjects("out-rfi-objects.csv")
        rb.parserfifunlinks("out-rfi-fun-links.csv")
    elif rb.parserfi and rb.parserverion == 8:
        rficount = rb.model.builduniquerfidict()
        rb.exportobjects("out2-utf8-obj-rfi.csv", rb.model.uniquerfi,
                         rb.model.childexportercallback, 'Requirement')
        header = ["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)",
                  "SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Funcionais de Interface (RFI)|Comum - Requisitos Funcionais de Interface (RFI)",
                  "Name", "Type"]
        rb.exportobjectlinks("out2-utf8-rel-fun-rfi.csv", 1,
                       header, rb.model.exportrfilinksdictcallback, "Realization")
        rb.exportobjectlinks("out2-utf8-rel-rfi-fun.csv", -1,
                       [header[1], header[0], header[2]],
                       rb.model.exportrfilinksdictcallback, "Realization")
    
    if rb.parserfn and rb.parserverion == 7:
        rb.parserfnobjects("out-rfn-objects.csv")
        rb.parserfnfunlinks("out-rfn-fun-links.csv")
    elif rb.parserfn and rb.parserverion == 8:
        rfncount = rb.model.builduniquerfndict()
        rb.exportobjects("out2-utf8-obj-rfn.csv", rb.model.uniquerfn,
                         rb.model.childexportercallback, 'Requirement')
        header = ["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)",
                  "SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Funcionais (RFN)|Comum - Requisitos Funcionais (RFN)",
                  "Name", "Type"]
        rb.exportobjectlinks("out2-utf8-rel-fun-rfn.csv", 1,
                       header, rb.model.exportrfnlinksdictcallback, "Realization")
        rb.exportobjectlinks("out2-utf8-rel-rfn-fun.csv", -1,
                       [header[1], header[0], header[2]],
                       rb.model.exportrfnlinksdictcallback, "Realization")

    if rb.parsergn and rb.parserverion == 7:
        rb.parsergnobjects("out-rgn-objects.csv")
        rb.parsergnfunlinks("out-rgn-fun-links.csv")
    elif rb.parsergn and rb.parserverion == 8:
        rgncount = rb.model.builduniquergndict()
        rb.exportobjects("out2-utf8-obj-rgn.csv", rb.model.uniquergn,
                         rb.model.childexportercallback, 'Requirement')
        header = ["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)",
                  "SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Regras de Negocio (RGN)|Comum - Regras de Negocio (RGN)",
                  "Name", "Type"]
        rb.exportobjectlinks("out2-utf8-rel-fun-rgn.csv", 1,
                       header, rb.model.exportrgnlinksdictcallback, "Realization")
        rb.exportobjectlinks("out2-utf8-rel-rgn-fun.csv", -1,
                       [header[1], header[0], header[2]],
                       rb.model.exportrgnlinksdictcallback, "Realization")
    
    if rb.parsernf and rb.parserverion == 7:
        rb.parsernfobjects("out-rnf-objects.csv")
        rb.parsernffunlinks("out-rnf-fun-links.csv")
    elif rb.parsernf and rb.parserverion == 8:
        rnfcount = rb.model.builduniquernfdict()
        rb.exportobjects("out2-utf8-obj-rnf.csv", rb.model.uniquernf,
                         rb.model.childexportercallback, 'Requirement')
        header = ["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)",
                  "SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Nao Funcionais (RNF)|Comum - Nao Funcionais (RNF)",
                  "Name", "Type"]
        rb.exportobjectlinks("out2-utf8-rel-fun-rnf.csv", 1,
                       header, rb.model.exportrnflinksdictcallback, "Realization")
        rb.exportobjectlinks("out2-utf8-rel-rnf-fun.csv", -1,
                       [header[1], header[0], header[2]],
                       rb.model.exportrnflinksdictcallback, "Realization")

    if rb.parseext and rb.parserverion == 8:
        #rnfcount = rb.model.builduniquernfdict()
        #rb.exportobjects("out2-utf8-obj-rnf.csv", rb.model.uniquernf, rb.model.childexportercallback)
        header = ["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)",
                  "SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)",
                  "Name", "Type"]
        rb.exportrellinks("out2-utf8-rel-uc-fun-ext.csv", 1, header,
                          rb.model.exportextlinksdictcallback, "Extends")
        
    if rb.parseinc and rb.parserverion == 8:
        #rnfcount = rb.model.builduniquernfdict()
        #rb.exportobjects("out2-utf8-obj-rnf.csv", rb.model.uniquernf, rb.model.childexportercallback)
        header = ["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)",
                  "SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)",
                  "Name", "Type"]
        rb.exportrellinks("out2-utf8-rel-uc-fun-inc.csv", 1, header,
                          rb.model.exportinclinksdictcallback, "Includes")
        
    if rb.parseimp and rb.parserverion == 8:
        #rnfcount = rb.model.builduniquernfdict()
        #rb.exportobjects("out2-utf8-obj-rnf.csv", rb.model.uniquernf, rb.model.childexportercallback)
        header = ["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)",
                  "SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)",
                  "Name", "Type"]
        rb.exportrellinks("out2-utf8-rel-uc-fun-imp.csv", 1, header,
                          rb.model.exportimplinksdictcallback, "Implements")
    
    if rb.runtests:
        #rb.tests = rbt.ReqBoxTest()
        #rb.tests.test01()
        rbt.rb = rb
        #sys.argv[1:] = args.unittest_args
        #unittest.main()
        suiteFew = unittest.TestSuite()
        unittest.TextTestRunner(verbosity=2).run(rbt.parsingsuite())

    #del rb
#    print "wfl.verbosity=" + str(wfl.__verbosity)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))