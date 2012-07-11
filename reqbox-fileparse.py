# -*- coding: utf-8 -*-
#!/usr/bin/env python

#   Project:			SIGA
#   Component Name:		wf2ea
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
    Create a CSV file with the wireframe data based on a hierarchy.

    Command Line Usage:
        wf2ea {<option> <argument>}

    Options:
        -h, --help              Print this help and exit.
        
    Examples:
"""

import logging
import sys
import mmap
import shutil
import contextlib
import codecs
from vlog import vlogger

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

class reqboxfileparser():
    """ Requirements doc file parsing
    Attributes:
        - file: string
    """
    
    def __init__(self, filename):
        # Public
        self.filename = filename
        
        # Init vlogger
        self.__verbosity = VERB_MAX
        self.vlog = vlogger(self.__verbosity, sys.stdout)
        #self.vlog = self.__log()
        
        # Init mmap
        self.__file = codecs.open(filename, "r", encoding="utf-8") # open(filename, 'r')
        self.vlog(VERB_MIN, "opening file: %s" % filename)
        self.__f = mmap.mmap(self.__file.fileno(), 0, access=mmap.ACCESS_READ)
        self.__f.seek(0) # rewind
        self.funlist = []
        self.funlocdict = {}
        pass
    
    #---- internal support stuff
    
    def cleanfunfromindex(self, s):
        """
        Returns a clean string from unwanted things at the index, ex:
        s = '183.Gerar Relatório de Arquivo de Retorno (Bancos)	67'
        result = 'Gerar Relatório de Arquivo de Retorno (Bancos)'
        
        Args:
            s -- the string
        """
        result = s.strip()
        result = result.split("\t")[0]
        if result is not "":
            result = result.split(".")[1]
#            result = result.rstrip()
#            result = result.lstrip()
        return result

    def cleanfunfrombody(self, s):
        """
        Returns a clean string from unwanted things at the body, ex:
        s = '183. Gerar Relatório de Arquivo de Retorno (Bancos)'
        result = 'Gerar Relatório de Arquivo de Retorno (Bancos)'
        
        Args:
            s -- the string
        """
        result = s.strip()
        #result = result.split("\n")[0]
        #if result is not "":
        #    result = result.split(".")[1]
        return result
    
    def getfunlist(self):
        """
        Returns a list with all the parsed functionalities based on the index.
        It will also store them in funlist.
        """
        self.vlog(VERB_MED, "-> %s" % __name__)
        
        # Find the position of the begining tag
        begintag = "Lista Completa de Funcionalidades"
        beginloc = self.__f.find(begintag)
        # Find the position of the end tag
        endtag = begintag
        endloc = self.__f.find(begintag, beginloc+1)
        # Set the cursor at the begining tag & skip the first line
        self.__f.seek(beginloc)
        self.__f.readline()
        loc = self.__f.tell()
        
        self.vlog(VERB_MAX, "beginloc = %d" % beginloc)
        self.vlog(VERB_MAX, "endloc = %d" % endloc)
        
        self.funlist = []
        while (loc < endloc):
            line = self.__f.readline()
            loc = self.__f.tell()
            self.vlog(VERB_MAX, "reading line '%s' bytes = %d" % (line, loc))
            line = self.cleanfunfromindex(line)
            self.vlog(VERB_MAX, "cleaned line '%s'" % (line))
            if line is not "":
                self.funlist += [line]
        
        #self.vlog(VERB_MED, "<- getfunlist()")
        self.vlog(VERB_MED, "<- %s" % __name__)
        self.vlog(VERB_MAX, "result = %s" % (self.funlist))
        #self.funlist += [result]
        return self.funlist
    
    def getfunlocdict(self):
        """
        Fills the funlocdict property with a dict where each element is indexed
        by the fun name and each value is a tuple with the (begining, end)
        positions on the file.
        """
        self.vlog(VERB_MED, "-> getfunlocdict()")
        self.__funlocdict = {}
        
        # Find the position of the begining tag
        #self.__f.seek(0)
        #funstr = "Lista Completa de Funcionalidades"
        #beginloc = self.__f.find(funstr)
        #self.vlog(VERB_MAX, "bytes = %d" % (beginloc))
        #beginloc = self.__f.find(funstr, beginloc+1)
        #endloc = beginloc
        #self.vlog(VERB_MAX, "bytes = %d" % (beginloc))
        #finalloc = self.__f.size()
        ## Set the cursor at the begining tag & skip the first line
        #self.__f.seek(beginloc)
        #line = self.__f.readline()
        #self.vlog(VERB_MAX, "byte = %d | line = %s" % (beginloc, line))
        
        #for funstr in self.funlist:
        #    beginloc = self.__f.find(funstr, endloc+1)
        #    self.__f.seek(beginloc)
        #    line = self.__f.readline()
        #    line = self.cleanfunfrombody(line)
        #    self.funlocdict[line] = (beginloc, endloc)
        #    #self.funlocdict[line] = beginloc
        #    self.vlog(VERB_MAX, "finding... '%s'" % (funstr))
        #    self.vlog(VERB_MAX, "found from %d to %d out of %d | %s" % (beginloc, endloc, finalloc, line))
        #    endloc = beginloc - 1
            
        # Find the position of the begining tag
        self.__f.seek(0)
        funstr = "Lista Completa de Funcionalidades"
        beginloc = self.__f.find(funstr)
        self.vlog(VERB_MAX, "bytes = %d" % (beginloc))
        beginloc = self.__f.find(funstr, beginloc+1)
        finalloc = self.__f.size() - 1
        endloc = finalloc
        self.__f.seek(beginloc)
        self.vlog(VERB_MAX, "bytes = %d" % (beginloc))
        count = len(self.funlist)
        
        # Iterate on the file backwards, it's more natural and easier...
        for idx, funstr in enumerate(reversed(self.funlist)):
            newidx = count - idx
            self.vlog(VERB_MAX, "finding... '%d. %s'" % (newidx, funstr))
            beginloc = self.__f.rfind(funstr, beginloc, endloc)
            self.__f.seek(beginloc)
            line = self.__f.readline()
            line = self.cleanfunfrombody(line)
            self.vlog(VERB_MAX, "found from %d to %d out of %d | %s" % (beginloc, endloc, finalloc, line))
            self.funlocdict[line] = (beginloc, endloc)
            endloc = beginloc - 1
            beginloc = 0
        
        self.vlog(VERB_MED, "<- getfunlocdict()")
        pass
    
    def funhassection(self, funstr, secstr):
        """
        Returns a bool with the result if a funstr has an secstr section within
        by the fun name and each value is a tuple with the (begining, end)
        positions on the file.
        
        Args:
            funstr -- the string
            secstr -- the string
        """
        beginloc = self.funlocdict[funstr][0]
        endloc = self.funlocdict[funstr][1]
        self.__f.seek(beginloc)
        found = self.__f.find(secstr, beginloc, endloc)
        return found in range(beginloc, endloc)
        
    def funhasrfi(self, funstr):
        return self.funhassection(funstr, "Requisitos Funcionais de Interface")
        
    def funhasrfn(self, funstr):
        return self.funhassection(funstr, "Requisitos Funcionais de Negócio")
        
    def funhasrnf(self, funstr):
        return self.funhassection(funstr, "Requisitos Não Funcionais")
        
    def funhasrng(self, funstr):
        return self.funhassection(funstr, "Regras de Negócio")
    
    def printmap(self, d):
        for k, v in d.items():
            self.vlog(VERB_MAX, "[%s] | %s" % (k, v))
            
    def printfun(self, idx, fun):
        if not self.funlocdict.has_key(fun):
            self.vlog(VERB_NON, "ERROR %d [%s] not found, and it should exist!!!" % (idx, fun))
        else:
            t = self.funlocdict[fun]
            beginloc = self.funlocdict[fun][0]
            endloc = self.funlocdict[fun][1]
            self.vlog(VERB_NON, "FUN %d [%s]" % (idx, fun))
            if self.funhasrfi(fun):
                self.vlog(VERB_NON, "RFIs")
            if self.funhasrfn(fun):
                self.vlog(VERB_NON, "RFNs")
            if self.funhasrnf(fun):
                self.vlog(VERB_NON, "RNFs")
            if self.funhasrng(fun):
                self.vlog(VERB_NON, "RNGs")
        
    def __str__(self):
        for idx, fun in enumerate(self.funlist):
            self.printfun(idx, fun)
    
    def close(self):
        self.__f.close()
        self.__f.close()

    #---- mainline

def main(argv):
    rfp = reqboxfileparser("./Rv10.txt")
    print "INPUT:   " + rfp.filename
    
    rfp.getfunlist()
    #rfp.vlog(VERB_MED, "fun = %s" % (fun))
    rfp.vlog(VERB_MED, "len(fun) = %d" % (len(rfp.funlist)))
    rfp.getfunlocdict()
    rfp.vlog(VERB_MED, "funlocdict = %s" % (rfp.funlocdict))
    #rfp.vlog(VERB_MED, "%d" % (rfp.funlocdict['Gerar Etiqueta de Destino']))
    #rfp.vlog(VERB_MED, "%d" % (rfp.funlocdict['Provisão para despesas futuras']))
    rfp.printmap(rfp.funlocdict)
#    rfp.printfun("Manter Prontuário")
    rfp.vlog(VERB_MED, "rfp = %s" % (rfp))
    rfp.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
