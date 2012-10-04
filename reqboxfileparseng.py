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
from reqboxfileparse import ReqBoxFileParser

#sys.setdefaultencoding('utf-8')

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

PARSETYPE = 'utf8-win'
#PARSETYPE = 'utf8-win-crlf'

class ReqBoxFileParserNG(ReqBoxFileParser, object):
    """ Requirements doc file parsing
    Attributes:
        - dir: objects imports dir
        - file: string
    """
    
    def __init__(self):
        # Public
        ReqBoxFileParser.__init__(self)
#        self.filename = ''
#        self.funlist = []
#        self.fundict = {}
        self.importsdir = ''
        
        # Init vlogger
#        self.__verbosity = VERB_MAX
#        self.vlog = vlogger(self.__verbosity, sys.stdout)
        #self.vlog = self.__log()
        
        # Init mmap
#        self.__file = None
#        self.__f = None
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
            self.funlist += [line[0]]
            
        self.vlog(VERB_MED, "<- %s" % __name__)
        self.vlog(VERB_MAX, "result = %s" % (self.funlist))
        return self.funlist
    
    #def getfundict(self):
    #    """
    #    Fills the fundict property with a dict where each element is indexed
    #    by the fun name and each value is an object from the model
    #    """
    #    self.vlog(VERB_MED, "-> getfundict()")
    #    self.fundict = {}
    #    
    #    beginloc = self.bodystartloc()
    #    test = issubclass(ReqBoxFileParserNG, object)
    #    test = issubclass(ReqBoxFileParserNG, ReqBoxFileParser)
    #    father = super(ReqBoxFileParserNG, self)
    #    finalloc = father.get_f().size() - 1
    #    finalloc = self.f.size() - 1
    #    endloc = finalloc
    #    self.__f.seek(beginloc)
    #    self.vlog(VERB_MAX, "bytes = %d" % (beginloc))
    #    count = len(self.funlist)
    #    
    #    # Iterate on the file backwards, it's more natural and easier...
    #    for idx, funstr in enumerate(reversed(self.funlist)):
    #        newidx = count - idx
    #        #newfunstr = "%s. %s" % (newidx, funstr)
    #        #newfunstr = utf8(str(newidx) + ".\t") + funstr
    #        fieldterm = "\r\n"
    #        if self.parsingasutf8_win_crlf():
    #            #newfunstr = newfunstr.decode('utf-8')
    #            #newfunstr = utf8(newfunstr.upper())
    #            #newfunstr = utf8("\n" + str(newidx) + ".\t") + funstr
    #            fieldsize = 101
    #            #newfunstr = utf8(fieldterm + str(newidx) + ".\t") + funstr
    #            newfunstr = utf8(fieldterm + str(newidx) + ".\t")
    #            #newfunstr = utf8(str(newidx) + ".\t") + funstr
    #            #if len(funstr) >= fieldsize:
    #            #    #TODO: BREAKPOINT HERE
    #            #    newfunstr = newfunstr[:fieldsize] + utf8(fieldterm) # + newfunstr[fieldsize:len(newfunstr)]
    #            #    #newfunstr = utf8(fieldterm) + newfunstr[:fieldsize-2] + utf8(fieldterm) # + newfunstr[fieldsize:len(newfunstr)]
    #            #    #newfunstr = newfunstr[:fieldsize-2] # + newfunstr[fieldsize:len(newfunstr)]
    #            #    #newfunstr = funstr[:99]
    #            #newfunstr = newfunstr.decode('utf-8').upper().encode('utf-8')
    #            #newfunstr = newfunstr.upper()
    #            #utf8(str(newfunstr.upper()))#.encode('utf-8')
    #        elif self.parsingasutf8_win():
    #            newfunstr = utf8(fieldterm + str(newidx) + ". ") # + funstr
    #            #newfunstr = utf8(newfunstr)
    #            pass
    #        self.vlog(VERB_MAX, "looking for: '%s'" % (newfunstr))
    #        #beginloc = self.__f.rfind(newfunstr, beginloc, endloc)
    #        beginloc = 0
    #        beginloc = self.__f.rfind(newfunstr, beginloc, endloc)
    #        if beginloc != -1:
    #            beginloc += 2
    #            self.__f.seek(beginloc)
    #            line = self.__f.readline()
    #            fieldsize = 85
    #            if self.parsingasutf8_win_crlf():
    #                if len(line.strip()) > fieldsize:
    #                    print("-----------------------------------MULTILINE")
    #            funid = self.__getfunid(line)
    #            line = self.__cleanfunfrombody(line)
    #            self.vlog(VERB_MAX, "found from %d to %d out of %d | '%s. %s'" % (beginloc, endloc, finalloc, funid, line))
    #            #self.fundict[funstr] = (beginloc, endloc, funid)
    #            # I switched the dict keys from uppercase (body) to as they are
    #            # on the index (capitalized as they are)
    #            
    #            currentpos = self.__f.tell()
    #            
    #            #newidx = count - funidx
    #            r = model.funmodel(funid, funstr, beginloc, endloc)
    #            r.fun.reqstart = beginloc
    #            r.fun.reqend   = endloc
    #            r.rfistart = self.funrfistart(funstr, beginloc, endloc)
    #            r.rfnstart = self.funrfnstart(funstr, beginloc, endloc)
    #            r.rnfstart = self.funrnfstart(funstr, beginloc, endloc)
    #            r.rgnstart = self.funrgnstart(funstr, beginloc, endloc)
    #            startmarkups = [r.fun.reqstart, r.rfistart, r.rfnstart, r.rnfstart, r.rgnstart, r.fun.reqend]
    #            startmarkups.sort()
    #            result = "FUN id=%s [bytes=%d/%d]:\t'%s'\n" % (r.fun.reqid, r.fun.reqstart, r.fun.reqend, r.fun.reqname)
    #            print(result)
    #            r.rfiend   = self.funsecend(funstr, r.rfistart, startmarkups)
    #            r.rfnend   = self.funsecend(funstr, r.rfnstart, startmarkups)
    #            r.rnfend   = self.funsecend(funstr, r.rnfstart, startmarkups)
    #            r.rgnend   = self.funsecend(funstr, r.rgnstart, startmarkups)
    #            #self.vlog(VERB_MED, "%s" % (self.printfun(funidx+1, funname)))
    ##            self.fun[funname].rfi = self.fp.gettagdic(funname, 'RFI')
    #            
    #            self.fundict[funstr] = r #(beginloc, endloc, funid)
    #            
    #            if r.rfistart != -1:
    #                r.rfi = self.gettagdic(funstr, 'RFI', r.rfistart, r.rfiend)
    #                pass
    #            if r.rfnstart != -1:
    #                r.rfn = self.gettagdic(funstr, 'RFN', r.rfnstart, r.rfnend)
    #            if r.rnfstart != -1:
    #                r.rnf = self.gettagdic(funstr, 'RNF', r.rnfstart, r.rnfend)
    #            if r.rgnstart != -1:
    #                r.rgn = self.gettagdic(funstr, 'RGN', r.rgnstart, r.rgnend)
    #            
    #            self.__f.seek(currentpos)
    #            
    #            endloc = beginloc - 1
    #            beginloc = 0
    #        else:
    #            # TODO: An exception should be raised here
    #            pass
    #    
    #    self.vlog(VERB_MED, "<- getfundict()")
    #    pass
    
    #---- mainline

def main(argv):
    rfp = ReqBoxFileParserNG()
    rfp.importsdir = './data/'
    if rfp.parsingasutf8_win():# rfp.parsingasutf8_win():
        #rfp.parsefile("./data/LRCv12-utf8-win.txt") # SAVE AS UTF-8 in Win!!
        #rfp.parsefile("./data/LRCv12-utf8-dow2unix-l.txt")
        #rfp.parsefile("./data/LRCv12-win.txt")
        rfp.parsefile("./data/LRCv12.txt")
    elif self.parsingasutf8_win_crlf():
        #rfp = ReqBoxFileParser("./data/LRCv12-utf8-win.txt") # SAVE AS UTF-8 in Win!!
        #rfp = ReqBoxFileParser("./data/LRCv12-utf8-win-dos2unix.txt") # SAVE AS UTF-8 in Win!!
        rfp = ReqBoxFileParser("./data/LRCv12-utf8-crlf.txt") # SAVE AS UTF-8 in Win!!
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
        #rfp = ReqBoxFileParser("./data/Rv12w.txt")
    else:
        #rfp = ReqBoxFileParser("./data/Rv12.txt")
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
