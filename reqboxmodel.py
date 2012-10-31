#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Project:			SIGA
#   Component Name:		ReqBoxModel
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

def fixmschr(s):
    s = s.replace('\r\n\n\r\n','\r\n\r\n')
    s = s.replace('\r\no ','\r\n  - ')
    s = s.replace(u'\x96', u'-')
    s = s.replace(u'–', u'-')
    s = s.replace(u'\xe2\x80\x93', u'-')
    return s

class ReqModel():
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
        
    def fixreqbody(self):
        self.reqbody = fixmschr(self.reqbody)
        #self.reqbody = self.reqbody.replace('\r\n\n\r\n','\r\n\r\n')
        #self.reqbody = self.reqbody.replace('\r\no ','\r\n  - ')
        #self.reqname = self.reqname.replace(u'\x96', u'-')
        #pass
    
    def fixreqname(self):
        self.reqname = fixmschr(self.reqname)
        #tmp = self.reqname.replace(u'\xc296', u'-')
        #self.reqname = self.reqname.replace(u'\x96', u'-')
        #self.reqname = self.reqname.replace(u'\xe2\x80\x93', u'-')
        #
        #pass
    
class FunModel():
    """ Functionalities model
    Attributes:
        rfi, rfn, rnf, rgn: dict
    """
    
    def __init__(self, funid, funname, funstart, funend):
        # Public
        self.fun = ReqModel(funid, funname, funstart, funend)
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

class ReqBoxModel():
    """ Reqbox model
    Attributes:
    """
    
    def __init__(self, ParserClass):
        # Public
        # Init structures
        #self.fp = rfp.ReqBoxFileParser()
        self.fp = ParserClass()
        #self.fp.parsefile("./data/LRCv12.txt")
        self.uniquerfi = {}
        self.uniquerfn = {}
        self.uniquernf = {}
        self.uniquergn = {}
        
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
        #self.fp = rfp.reqboxfileparser()
        #rfp.VERB_MAX = 10
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
    
    def builduniquerfndict(self):
        for idx, funstr in enumerate(self.fp.funlist):
            d = self.fp.fundict[funstr].rfn
            for idx, reqstr in enumerate(sorted(d)):
                r = d[reqstr]
                
                if not reqstr in self.uniquerfn:
                    self.uniquerfn[reqstr] = ReqModel(r.reqid, r.reqname, r.reqstart, r.reqend)
                    self.uniquerfn[reqstr].reqbody = r.reqbody
                    print("inserting %s" % (r.reqid))
                else:
                    print("skipping %s" % (r.reqid))

    def builduniquernfdict(self):
        for idx, funstr in enumerate(self.fp.funlist):
            d = self.fp.fundict[funstr].rnf
            for idx, reqstr in enumerate(sorted(d)):
                r = d[reqstr]
                
                if not reqstr in self.uniquerfn:
                    self.uniquernf[reqstr] = ReqModel(r.reqid, r.reqname, r.reqstart, r.reqend)
                    self.uniquernf[reqstr].reqbody = r.reqbody
                    print("inserting %s" % (r.reqid))
                else:
                    print("skipping %s" % (r.reqid))

    def builduniquergndict(self):
        for idx, funstr in enumerate(self.fp.funlist):
            d = self.fp.fundict[funstr].rgn
            for idx, reqstr in enumerate(sorted(d)):
                r = d[reqstr]
                
                if not reqstr in self.uniquerfn:
                    self.uniquergn[reqstr] = ReqModel(r.reqid, r.reqname, r.reqstart, r.reqend)
                    self.uniquergn[reqstr].reqbody = r.reqbody
                    print("inserting %s" % (r.reqid))
                else:
                    print("skipping %s" % (r.reqid))

    def rfiobjectsexporter(self, fh):
        
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

    def rfnobjectsexporter(self, fh):
        
        #if self.outfile != "":
        #    fh = open(self.outfile, 'wb')
        #else:
        #    fh = sys.stdout
            
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["Name", "Alias", "Type", "Notes", "Priority", "Author"])
        
        d = self.uniquerfn
        for idx, reqstr in enumerate(sorted(d)):
            r = d[reqstr]
                
                #if self.uniquerfn
                
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

    def rnfobjectsexporter(self, fh):
        
        #if self.outfile != "":
        #    fh = open(self.outfile, 'wb')
        #else:
        #    fh = sys.stdout
            
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["Name", "Alias", "Type", "Notes", "Priority", "Author"])
        
        d = self.uniquernf
        for idx, reqstr in enumerate(sorted(d)):
            r = d[reqstr]
                
                #if self.uniquerfn
                
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

    def rgnobjectsexporter(self, fh):
        
        #if self.outfile != "":
        #    fh = open(self.outfile, 'wb')
        #else:
        #    fh = sys.stdout
            
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["Name", "Alias", "Type", "Notes", "Priority", "Author"])
        
        d = self.uniquergn
        for idx, reqstr in enumerate(sorted(d)):
            r = d[reqstr]
                
                #if self.uniquerfn
                
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
            print("Writing... %s" % (r.reqid))
            csvhdlr.writerow(row)

    def uclabel(self, ucid):
        return "UC" + ucid.zfill(3)
    
    def funobjectsexporter(self, fh):
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["Name", "Alias", "Type", "Notes", "Priority", "Author"])
        
        d = self.fp.fundict
        for idx, reqstr in enumerate(self.fp.funlist):
            if reqstr in d:
                r = d[reqstr].fun
                alias = self.uclabel(r.reqid) # "UC" + r.reqid.zfill(3)
                row = [alias + ". " + r.reqname, alias, 'UseCase', r.reqbody, "Medium", "Albert De La Fuente"]
                print("Writing... %s" % (r.reqid))
                csvhdlr.writerow(row)
            else:
                print("NOT FOUND... %s" % (reqstr))
            
    def fixsecondlevelbullets(self):
        pass
    
    def funrfilinksexporter(self, fh):
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)", "SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Funcionais de Interface (RFI)|Comum - Requisitos Funcionais de Interface (RFI)", "Name"])
        
        fd = self.fp.fundict
        for i0, funstr in enumerate(self.fp.funlist):
            fun = fd[funstr].fun
            funalias = self.uclabel(fun.reqid) # "UC" + r.reqid.zfill(3)
            
            rd = fd[funstr].rfi
            for i1, reqstr in enumerate(sorted(rd)):
                reqalias = rd[reqstr].reqid
                
                row = [funalias, reqalias, "rel-%s-%s" % (funalias, reqalias)]
                print("Writing... rel-%s-%s" % (funalias, reqalias))
                csvhdlr.writerow(row)

    def rfifunlinksexporter(self, fh):
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Funcionais de Interface (RFI)|Comum - Requisitos Funcionais de Interface (RFI)", "SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)", "Name"])
        
        fd = self.fp.fundict
        for i0, funstr in enumerate(self.fp.funlist):
            fun = fd[funstr].fun
            funalias = self.uclabel(fun.reqid) # "UC" + r.reqid.zfill(3)
            
            rd = fd[funstr].rfi
            for i1, reqstr in enumerate(sorted(rd)):
                reqalias = rd[reqstr].reqid
                
                row = [reqalias, funalias, "rel-%s-%s" % (reqalias, funalias)]
                print("Writing... rel-%s-%s" % (reqalias, funalias))
                csvhdlr.writerow(row)

    def funrfnlinksexporter(self, fh):
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)", "SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Funcionais (RFN)|Comum - Requisitos Funcionais (RFN)", "Name"])
        
        fd = self.fp.fundict
        for i0, funstr in enumerate(self.fp.funlist):
            fun = fd[funstr].fun
            funalias = self.uclabel(fun.reqid) # "UC" + r.reqid.zfill(3)
            
            rd = fd[funstr].rfn
            for i1, reqstr in enumerate(sorted(rd)):
                reqalias = rd[reqstr].reqid
                
                row = [funalias, reqalias, "rel-%s-%s" % (funalias, reqalias)]
                print("Writing... rel-%s-%s" % (funalias, reqalias))
                csvhdlr.writerow(row)

    def rfnfunlinksexporter(self, fh):
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Funcionais (RFN)|Comum - Requisitos Funcionais (RFN)", "SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)", "Name"])
        
        fd = self.fp.fundict
        for i0, funstr in enumerate(self.fp.funlist):
            fun = fd[funstr].fun
            funalias = self.uclabel(fun.reqid) # "UC" + r.reqid.zfill(3)
            
            rd = fd[funstr].rfn
            for i1, reqstr in enumerate(sorted(rd)):
                reqalias = rd[reqstr].reqid
                
                row = [reqalias, funalias, "rel-%s-%s" % (reqalias, funalias)]
                print("Writing... rel-%s-%s" % (reqalias, funalias))
                csvhdlr.writerow(row)

    def funrgnlinksexporter(self, fh):
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)", "SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Regras de Negocio (RGN)|Comum - Regras de Negocio (RGN)", "Name"])
        
        fd = self.fp.fundict
        for i0, funstr in enumerate(self.fp.funlist):
            fun = fd[funstr].fun
            funalias = self.uclabel(fun.reqid) # "UC" + r.reqid.zfill(3)
            
            rd = fd[funstr].rgn
            for i1, reqstr in enumerate(sorted(rd)):
                reqalias = rd[reqstr].reqid
                
                row = [funalias, reqalias, "rel-%s-%s" % (funalias, reqalias)]
                print("Writing... rel-%s-%s" % (funalias, reqalias))
                csvhdlr.writerow(row)

    def rgnfunlinksexporter(self, fh):
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Regras de Negocio (RGN)|Comum - Regras de Negocio (RGN)", "SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)", "Name"])
        
        fd = self.fp.fundict
        for i0, funstr in enumerate(self.fp.funlist):
            fun = fd[funstr].fun
            funalias = self.uclabel(fun.reqid) # "UC" + r.reqid.zfill(3)
            
            rd = fd[funstr].rgn
            for i1, reqstr in enumerate(sorted(rd)):
                reqalias = rd[reqstr].reqid
                
                row = [reqalias, funalias, "rel-%s-%s" % (reqalias, funalias)]
                print("Writing... rel-%s-%s" % (reqalias, funalias))
                csvhdlr.writerow(row)

    def funrnflinksexporter(self, fh):
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)", "SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Nao Funcionais (RNF)|Comum - Nao Funcionais (RNF)", "Name"])
        
        fd = self.fp.fundict
        for i0, funstr in enumerate(self.fp.funlist):
            fun = fd[funstr].fun
            funalias = self.uclabel(fun.reqid) # "UC" + r.reqid.zfill(3)
            
            rd = fd[funstr].rnf
            for i1, reqstr in enumerate(sorted(rd)):
                reqalias = rd[reqstr].reqid
                
                row = [funalias, reqalias, "rel-%s-%s" % (funalias, reqalias)]
                print("Writing... rel-%s-%s" % (funalias, reqalias))
                csvhdlr.writerow(row)

    def rnffunlinksexporter(self, fh):
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Nao Funcionais (RNF)|Comum - Nao Funcionais (RNF)", "SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)", "Name"])
        
        fd = self.fp.fundict
        for i0, funstr in enumerate(self.fp.funlist):
            fun = fd[funstr].fun
            funalias = self.uclabel(fun.reqid) # "UC" + r.reqid.zfill(3)
            
            rd = fd[funstr].rnf
            for i1, reqstr in enumerate(sorted(rd)):
                reqalias = rd[reqstr].reqid
                
                row = [reqalias, funalias, "rel-%s-%s" % (reqalias, funalias)]
                print("Writing... rel-%s-%s" % (reqalias, funalias))
                csvhdlr.writerow(row)

def main(argv):
    rbm = ReqBoxModel(rfp.ReqBoxFileParser)
    rbm.parsefile("./data/LFv14.ms.default.fixed.txt")
    #rbm.printf()
    
    #rbm.fixsecondlevelbullets()
    
    fh = open("rfi-objects.csv", 'wb')
    rbm.rfiobjectsexporter(fh)
    
    rbm.builduniquerfndict()
    fh = open("rfn-objects.csv", 'wb')
    rbm.rfnobjectsexporter(fh)
    
    rbm.builduniquernfdict()
    fh = open("rnf-objects.csv", 'wb')
    rbm.rnfobjectsexporter(fh)

    rbm.builduniquergndict()
    fh = open("rgn-objects.csv", 'wb')
    rbm.rgnobjectsexporter(fh)
    
    fh = open("fun-objects.csv", 'wb')
    rbm.funobjectsexporter(fh)
    
    fh = open("fun-rfi-relationships.csv", 'wb')
    rbm.funrfilinksexporter(fh)
    
    fh = open("rfi-fun-relationships.csv", 'wb')
    rbm.rfifunlinksexporter(fh)

if __name__ == "__main__":
    sys.exit(main(sys.argv))