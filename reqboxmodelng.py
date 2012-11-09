#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import reqboxmodel as model
import reqboxfileparseng as rfp
from vlog import vlogger
#from reqboxfileparse import reqboxfileparser

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3
   
class FunModelNG(model.FunModel):
    """ Functionalities model
    Attributes:
        rfi, rfn, rnf, rgn: dict
    """
    
    def __init__(self, funid, funname, funstart, funend):
        # Public
        FunModel.__init__(self)
        self.relstart = -1
        self.relend = -1
        self.extends = {}
        self.implements = {}
        pass
    
class ReqBoxModelNG(model.ReqBoxModel):
    """ Reqbox model
    Attributes:
    """
    
    def funexportercallback(self, d, reqstr):
        return d[reqstr].fun
        
    def childexportercallback(self, d, reqstr):
        return d[reqstr]

    def objectsexporter(self, fh, d, exportercallback):
        """
        Refactored method for exporting objects: FUN (UC), RFI, RFN, RNG, RNF
        """
        
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["Name", "Alias", "Type", "Notes", "Priority", "Author", ])
        
        #for idx, funstr in enumerate(self.fp.funlist):
            # d = self.fp.fundict[funstr].rfi
        for idx, reqstr in enumerate(sorted(d)):
            #r = d[reqstr].fun
            r = exportercallback(d, reqstr)
            reqid = r.reqid.decode('utf-8')
            reqname = ''
            if r.reqname is not None:
                reqname = r.reqname.encode('utf-8')
            reqbody = ''
            if r.reqbody is not None:
                reqbody = r.reqbody.encode('utf-8')
            #row = [r.reqname.encode('utf-8'), r.reqid.encode('utf-8')]
            row = [reqname, reqid, 'Requirement', reqbody, "Medium", "Albert De La Fuente"]
            
            #Name    Alias   Type    Notes   Priority        Author
            #RFI001. MANTER HOSPEDAGEM       RFI001. Requirement     "
            #O sistema deve disponibilizar uma interface para incluir, alterar, excluir e consultar hospedagens, contemplando os seguintes atributos:
            #* Código da hospedagem
            #* ...
            #"       Medium  Albert De La Fuente
            print("Writing...%s [%s]" % (r.reqid, type(r.reqname)))
            csvhdlr.writerow(row)

    def removereqcontentdict(self, d):
        for idx, reqstr in enumerate(sorted(d)):
            req = d[reqstr]
            req.reqbody = ''
            req.reqname = ''
    
    def removereqcontent(self):
        for idx, funstr in enumerate(self.fp.fundict):
            fun = self.fp.fundict[funstr]
            self.removereqcontentdict(fun.rfn)
            self.removereqcontentdict(fun.rgn)
            self.removereqcontentdict(fun.rnf)
   
    def loaduniquecsvdict(self, d, fname):
        """
        Loads a dict with ReqModel objects from a csv file
        
        Args:
            d -- the dict to be filled
            fname -- the csv file name to be parsed
        """
        fh = open(fname, 'rb')
        f = csv.reader(fh, delimiter=',')
        items = []
        headers = f.next()
        
        idx = 0
        for items in f:
            if items[1] is not '':
                reqid = items[1].split('.')[0].decode('utf-8')
                r = model.ReqModel(reqid,
                                   model.fixmschr(items[0].decode('utf-8')), 0, 0)
                r.reqbody = model.fixmschr(items[2].decode('utf-8'))
                d[reqid] = r
                idx += 1
        return idx
    
    def builduniquerfidict(self):
        #return self.loaduniquecsvdict(self.uniquerfi, self.fp.importsdir + 'in-rfi-objects.csv')
        for funstr in enumerate(sorted(self.fp.fundict)):
            d = self.fp.fundict[funstr[1]].rfi
            for rfistr in enumerate(d):
                rfi = self.fp.fundict[funstr[1]].rfi[rfistr[1]]
                if rfistr[1] not in self.uniquerfi:
                    self.uniquerfi[rfistr[1]] = rfi
                    self.uniquerfi[rfistr[1]].reqname = '%s. %s' % (rfi.reqid, rfi.reqname)

    def builduniquerfndict(self):
        return self.loaduniquecsvdict(self.uniquerfn, self.fp.importsdir + 'in-rfn-objects.csv')

    def builduniquergndict(self):
        return self.loaduniquecsvdict(self.uniquergn, self.fp.importsdir + 'in-rgn-objects.csv')

    def builduniquernfdict(self):
        return self.loaduniquecsvdict(self.uniquernf, self.fp.importsdir + 'in-rnf-objects.csv')
    
#    def funexportercallback(self, d, reqstr):
#        return d[reqstr].fun
        
    def exportrfilinksdictcallback(self, d, reqstr):
        return d.rfi
    
    def exportrfnlinksdictcallback(self, d, reqstr):
        return d.rfn
    
    def exportrgnlinksdictcallback(self, d, reqstr):
        return d.rgn
    
    def exportrnflinksdictcallback(self, d, reqstr):
        return d.rnf
    
    def exportlinks(self, fname, direction, header, dictcallback, linktype):
        fh = open(fname, 'wb')
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        #csvhdlr.writerow(["SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)", "SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Funcionais de Interface (RFI)|Comum - Requisitos Funcionais de Interface (RFI)", "Name"])
        csvhdlr.writerow(header)
        
        fd = self.fp.fundict
        for i0, funstr in enumerate(sorted(fd)):
            fun = fd[funstr]
            funalias = fun.fun.reqid # "UC" + r.reqid.zfill(3)
            
            #rd = fd[funstr].rfi
            rd = dictcallback(fun, funstr)
            for i1, reqstr in enumerate(sorted(rd)):
                reqalias = rd[reqstr].reqid
                
                if direction == 1:
                    row = [funalias, reqalias, "rel-%s-%s" % (funalias, reqalias),
                           linktype]
                    print("Writing... rel-%s-%s" % (funalias, reqalias))
                else:
                    row = [reqalias, funalias, "rel-%s-%s" % (reqalias, funalias),
                           linktype]
                    print("Writing... rel-%s-%s" % (reqalias, funalias))
                
                csvhdlr.writerow(row)
                
    #def rfifunlinksexporter(self, fh):
    #    csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
    #    csvhdlr.writerow(["SIGA stable|Biblioteca de Requisitos (RFI / RFN / RNF / RGN)|Requisitos Funcionais de Interface (RFI)|Comum - Requisitos Funcionais de Interface (RFI)", "SIGA stable|Biblioteca de Casos de Uso (UC)|Comum - Casos de Uso (UC)", "Name"])
    #    
    #    fd = self.fp.fundict
    #    for i0, funstr in enumerate(self.fp.funlist):
    #        fun = fd[funstr].fun
    #        funalias = self.uclabel(fun.reqid) # "UC" + r.reqid.zfill(3)
    #        
    #        rd = fd[funstr].rfi
    #        for i1, reqstr in enumerate(sorted(rd)):
    #            reqalias = rd[reqstr].reqid
    #            
    #            row = [reqalias, funalias, "rel-%s-%s" % (reqalias, funalias)]
    #            print("Writing... rel-%s-%s" % (reqalias, funalias))
    #            csvhdlr.writerow(row)
    
    def remapbodies(self, d):
        pass

    # TODO: Export report
    def exportreport(self, d):
        pass

def main(argv):
    #rbm = model.ReqBoxModel(rfp.ReqBoxFileParserNG)
    #rbm.parsefile("./input/LRCv13-mod.utf8.fix.txt")
    #rbm.printf()
    pass

if __name__ == "__main__":
    sys.exit(main(sys.argv))