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

#def site_struct():
#    return defaultdict(board_struct)
#    
#def board_struct():
#    return defaultdict(user_struct)
#    
#def user_struct():
#    return dict(pageviews=0,username='',comments=0)

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
        #self.fun = reqmodel()
        #self.funid = funid
        #self.funname = funname
        #self.funbody = None
        #self.funstart = funstart
        #self.funend = funend
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
            #print(result)
#            if self.funhasrfi(funstr):
#                result = result + "- RFI id=%s [bytes=%d/%d]: '%s'\n" % (f.rfistart, f.rfiend)
            #if self.funhasrfn(funstr):
            #    result = result + "RFNs\n"
            #if self.funhasrnf(funstr):
            #    result = result + "RNFs\n"
            #if self.funhasrng(funstr):
            #    result = result + "RNGs\n"
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
        
#        self.fp.getfunlist()
        #count = len(fp.funlist)
#        for funidx, funname in enumerate(self.fp.funlist):
#            #newidx = count - funidx
#            funstart = self.fp.funstart(funname)
#            funend   = self.fp.funend(funname)
#            fun = funmodel(funidx + 1, funname, funstart, funend)
#            fun.funstart = funstart
#            fun.funend   = funend
#            fun.rfistart = self.fp.funrfistart(funname)
#            fun.rfiend   = self.fp.funrfiend(funname)
#            fun.rfnstart = self.fp.funrfnstart(funname)
#            fun.rfnend   = self.fp.funrfnend(funname)
#            fun.rnfstart = self.fp.funrnfstart(funname)
#            fun.rnfend   = self.fp.funrnfend(funname)
#            fun.rgnstart = self.fp.funrgnstart(funname)
#            fun.rgnend   = self.fp.funrgnend(funname)
#            self.fun[funname] = fun
#            self.vlog(VERB_MED, "%s" % (self.printfun(funidx+1, funname)))
##            self.fun[funname].rfi = self.fp.gettagdic(funname, 'RFI')
#            if funstart != -1:
                #self.fun[funname].rfi = self.fp.gettagdic(funname, 'RFI', rfistart, rfiend)
#                pass
                #for rfiidx, rfiname in enumerate(self.fun[funname].rfi):
                #    self.fun[funname].rfi = fp.getrfidic(funname)
            #if fp.funhasrfn(funname):
            #    self.fun[funname].rfn = fp.getrfndic(funname)
            #if fp.funhasrnf(funname):
            #    self.fun[funname].rnf = fp.getrnfdic(funname)
            #if fp.funhasrng(funname):
            #    self.fun[funname].rng = fp.getrngdic(funname)
            
            
        #fp.vlog(VERB_MED, "fun = %s" % (fun))
        #fp.vlog(VERB_MED, "len(fun) = %d" % (len(rfp.funlist)))
        #fp.getfundict()
        #fp.vlog(VERB_MED, "fundict = %s" % (rfp.fundict))
        #fp.vlog(VERB_MED, "%d" % (rfp.fundict['Gerar Etiqueta de Destino']))
        #fp.vlog(VERB_MED, "%d" % (rfp.fundict['Provisão para despesas futuras']))
        #fp.printmap(fp.fundict)
        #fp.printfun("18", "Manter Prontuário")
        #fp.printfun("43", "Manter Plano de Ação")
        #fp.vlog(VERB_MED, "rfp = \n%s" % (rfp))
        
        # Init

#s.fun[001] = 'Manter Tipo de Verificacao de Item de Checklist'
#s.fun[002] = ' Manter Carta de Convocacao / Comunicado'
#s.fun[003] = ' Manter Remessa de Cartao de Identificacao'
#s.fun.count = x
#
#s.fun[001].rfi[234] = 'Manter tipo de verificacao de item de checklist'
#s.fun.rfi.count = y
#
#s.fun[001].rfn[001] = 'Permissao de acesso por perfil de seguranca'
#s.fun[001].rfn[366] = 'Busca e retorno de dados de tipo de verificacao de item de checklist'

#--- FUN vs. XXX case

#m['fun001'] = 'Manter Tipo de Verificacao de Item de Checklist'
#
#m['fun001']['rfi234'] = 'Manter tipo de verificacao de item de checklist'
#
#m['fun001']['rfn001'] = 'Permissao de acesso por perfil de seguranca'
#m['fun001']['rfn366'] = 'Busca e retorno de dados de tipo de verificao de item de checklist'
#
#m['fun001']['rnf001'] = '...'
#m['fun001']['rng001'] = '...'
#
#m['fun001']['wrf001'] = '...'

#--- FUN vs. RFI vs. XXX case

#m['fun001'] = 'Manter Tipo de Verificacao de Item de Checklist'
#
#m['fun001']['rfi234'] = 'Manter tipo de verificacao de item de checklist'
#
#m['fun001']['rfi234']['rfn001'] = 'Permissao de acesso por perfil de seguranca'
#m['fun001']['rfi234']['rfn366'] = 'Busca e retorno de dados de tipo de verificao de item de checklist'
#
#m['fun001']['rfi234']['rnf001'] = '...'
#m['fun001']['rfi234']['rng001'] = '...'
#
#m['fun001']['rfi234']['wrf001'] = '...'
#

    def printdic(self, d):
        #if d == self.fp.fundict[funstr].rfi:
        #    prefix = "RFI"
        #elif d == self.fp.fundict[funstr].rfn:
        #    prefix = "RFN"        
        for idx, funstr in enumerate(sorted(d)):
            r = d[funstr]
            print("    - %s: '%s...' ('%s...', begin=%d, end=%d)" % (r.reqid, r.reqname[:20], r.reqbody[:15], r.reqstart, r.reqend))

    def printf(self):
        for idx, funstr in enumerate(self.fp.funlist):
            print("FUN %d: %s" % (idx + 1, funstr))
            d = self.fp.fundict[funstr].rfi
            count = len(d)
            print("  %s [%d]" % ("RFI", count))
            self.printdic(d)
            
            d = self.fp.fundict[funstr].rfn
            count = len(d)
            print("  %s [%d]" % ("RFI", count))
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

def main(argv):
#    r = reqboxmodel()
    #r.parsefile("./data/LRCv12-utf8-win.txt")
#    r.fp.parsefile("./data/LRCv12.txt")
    #r.vlog(VERB_MED, "r = \n%s" % (r))

    rbm = reqboxmodel()
    rbm.printf()

    
#    print s
##    print s['fun001']
#    print s['fun001']['rfi234']
#    print s['fun001']
#    
#    f.fid = xx
#    f.fname = yy
#    
#    fun['001'] = f
#    
#    fun['001'].fname = yy
#    
#    fun['001'].rfi['rfi001'] = zz
#    fun['001'].rfn['rfn001'] = yy
#    
#    rfi = fun.indexbyrfi
#    rfi['001'].fun
#    
#    myDict = {'Apple': {'American':'16', 'Mexican':10, 'Chinese':5},
#              'Grapes':{'Arabian':'25','Indian':'20'} }
#
#
#    print myDict['Apple']['American']
#    
#    
#    userdict = defaultdict(site_struct)
#    userdict['site1']['board1']['username'] = 'tommy'
#    #userdict['site1']['board1']['username']['pageviews'] += 1
#    print userdict
#    print userdict['site1']['board1']['username']



if __name__ == "__main__":
    sys.exit(main(sys.argv))