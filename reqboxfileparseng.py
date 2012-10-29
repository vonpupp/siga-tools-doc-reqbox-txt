#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
import operator
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
        self.objectlist = []
        
        # Init vlogger
#        self.__verbosity = VERB_MAX
#        self.vlog = vlogger(self.__verbosity, sys.stdout)
        #self.vlog = self.__log()
        
        # Init mmap
#        self.file = None
#        self.f = None
        pass

    def getfunlist(self):
        """
        Overrided method to load from a CSV file as unicode objects
        """
        self.vlog(VERB_MED, "-> %s" % __name__)
        
        self.funlist = []
        
        #fh = codecs.open(self.importsdir + 'in-uc-objects.csv', encoding='utf-8', mode='r')
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
        idx = 0
        for line in f:
            self.funlist += [line[0].decode('utf-8')] # .decode('utf-8')
            idx += 1
            
        self.vlog(VERB_MED, "<- %s" % __name__)
        self.vlog(VERB_MAX, "result = %s" % (self.funlist))
        return self.funlist
    
    def parsefile(self, filename):
        # Public
        self.filename = filename
        
        # Init mmap
        self.file = codecs.open(filename, encoding='utf-8', mode='r') # open(filename, 'r')
        self.vlog(VERB_MIN, "opening file: %s" % filename)
        self.f = mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_READ)
        self.f.seek(0) # rewind
        
        # Parsing stuff
        self.getfunlist()
        #self.vlog(VERB_MED, "fun = %s" % (self.funstr))
        self.vlog(VERB_MED, "len(fun) = %d" % (len(self.funlist)))
        self.getfundict() # No prefix, refactored parameter when this class became super of the ng version
        self.vlog(VERB_MED, "fundict = %s" % (self.fundict))
        pass
   
    #def gettagidx(self, funstr):
    #    result = funstr.strip()
    #    result = result.split(self.utf8("."))[0]
    #    result = result.rstrip()
    #    result = result.lstrip()
    #    return result
    
    def funrelstart(self, funstr, start=0, end=0):
        #header = "Regras de Negócio"
        header = "RELACIONAMENTOS"
        return self.funhassection(funstr, header, start, end)
        
    def funrelend(self, funstr, start=0, end=0):
        #header = "Regras de Negócio"
        header = "RELACIONAMENTOS"
        return self.funhassection(funstr, header, start, end)
       
    def getobjectlist(self, prefix):
        """
        Fills the fundict property with a dict where each element is indexed
        by the fun name and each value is an object from the model
        """
        self.vlog(VERB_MED, "-> getfundict()")
        self.fundict = {}
        
        bodyloc = beginloc = self.bodystartloc()
        finalloc = self.f.size() - 1
        endloc = finalloc
        self.f.seek(beginloc)
        self.vlog(VERB_MAX, "body start at location %d" % (beginloc))
        count = len(self.funlist)
        
        #print('sys.stdout encoding is "' + sys.stdout.encoding + '"')
        #print('sys.getdefaultencoding() is "' + sys.getdefaultencoding() + '"')
        #str1 = 'lüelā'
        #print(str1)
        #reload(sys)
        #sys.setdefaultencoding( 'utf-8' )
        
        # Iterate on the file backwards, it's more natural and easier...
        for idx, funstr in enumerate(reversed(self.funlist)):
            newidx = count - idx
            newidx = self.getfunid(funstr)
            #newfunstr = "%s. %s" % (newidx, funstr)
            #newfunstr = self.utf8(str(newidx) + ".\t") + funstr
            fieldterm = "\r\n"
            if self.parsingasutf8wincrlf():
                #newfunstr = newfunstr.decode('utf-8')
                #newfunstr = self.utf8(newfunstr.upper())
                #newfunstr = self.utf8("\n" + str(newidx) + ".\t") + funstr
                fieldsize = 101
                #newfunstr = self.utf8(fieldterm + str(newidx) + ".\t") + funstr
                newfunstr = self.utf8(fieldterm + str(newidx) + ".\t")
                #newfunstr = self.utf8(str(newidx) + ".\t") + funstr
                #if len(funstr) >= fieldsize:
                #    #TODO: BREAKPOINT HERE
                #    newfunstr = newfunstr[:fieldsize] + self.utf8(fieldterm) # + newfunstr[fieldsize:len(newfunstr)]
                #    #newfunstr = self.utf8(fieldterm) + newfunstr[:fieldsize-2] + self.utf8(fieldterm) # + newfunstr[fieldsize:len(newfunstr)]
                #    #newfunstr = newfunstr[:fieldsize-2] # + newfunstr[fieldsize:len(newfunstr)]
                #    #newfunstr = funstr[:99]
                #newfunstr = newfunstr.decode('utf-8').upper().encode('utf-8')
                #newfunstr = newfunstr.upper()
                #self.utf8(str(newfunstr.upper()))#.encode('utf-8')
            elif self.parsingasutf8win():
                if isinstance(self.__class__, ReqBoxFileParser):
                    newfunstr = self.utf8(prefix + str(newidx) + ". ") # + funstr
                else:
                    stridx = str(newidx).zfill(3)
                    newfunstr = self.utf8(prefix + stridx + ". ") # + funstr
                #newfunstr = self.utf8(newfunstr)
                pass
            self.vlog(VERB_MAX, "looking for: '%s'" % (newfunstr))
            #beginloc = self.f.rfind(newfunstr, beginloc, endloc)
            #beginloc = 0
            beginloc = self.f.find(newfunstr, bodyloc, endloc)
            if beginloc != -1:
                beginloc += 2
                self.f.seek(beginloc)
                line = self.f.readline()
                #fieldsize = 85
                #if self.parsingasutf8wincrlf():
                #    if len(line.strip()) > fieldsize:
                #        print("-----------------------------------MULTILINE")
                funid = self.getfunid(line)
                line = self.cleanfunfrombody(line)
                self.vlog(VERB_MAX, "found from %d to %d out of %d | '%s. %s'" % (beginloc, endloc, finalloc, funid, line))
                # TODO: Assert: funstr == line.upper()
                #csv = funstr.decode('utf-8')
                csv = funstr #.decode('utf-8')
                doc = line.decode('latin1')
                if csv != doc:
                    self.vlog(VERB_MAX, "ASSERT. Fun names doesn't match:")
                    self.vlog(VERB_MAX, "  CSV = '%s'" % (csv)) # .decode('unicode_escape')
                    #print(csv)
                    self.vlog(VERB_MAX, "  DOC = '%s'" % (doc))
                    funstr = csv # self.getfunname(csv)
                    
                #endloc = 0
                # The endloc will be filled afterwards, I have to first order the list so
                # the end is the begining of the next one
                r = model.FunModel(funid, funstr, beginloc, 0)
                r.fun.reqstart = beginloc
                r.fun.reqend   = 0 
                    
                self.objectlist.append(r)
                    
                #self.fundict[funstr] = (beginloc, 0, funid)
                # I switched the dict keys from uppercase (body) to as they are
                # on the index (capitalized as they are)
                
                currentpos = self.f.tell()
                self.f.seek(currentpos)
                
                # endloc = beginloc - 1
                beginloc = bodyloc
            else:
                # TODO: An exception should be raised here
                pass
        
        self.vlog(VERB_MED, "<- getfundict()")
    
    def getfundict(self):
        self.getobjectlist(". ")
        self.objectlist.sort(key = operator.attrgetter('fun.reqstart'))
        # Fill the endloc property with the next beginloc
        nextbeginloc = 0
        for idx, r in enumerate(self.objectlist):
            if idx < len(self.objectlist)-1:
                nextbeginloc = self.objectlist[idx+1].fun.reqstart
            else:
                nextbeginloc = self.f.size()
            r.fun.reqend = nextbeginloc
            
            #newidx = count - funidx
            #r = model.FunModel(funid, funstr, beginloc, endloc)
            #r.fun.reqstart = beginloc
            #r.fun.reqend   = endloc
            r.rfistart = self.funrfistart(r.fun.reqname, r.fun.reqstart, r.fun.reqend)
            r.rfnstart = self.funrfnstart(r.fun.reqname, r.fun.reqstart, r.fun.reqend)
            r.rnfstart = self.funrnfstart(r.fun.reqname, r.fun.reqstart, r.fun.reqend)
            r.rgnstart = self.funrgnstart(r.fun.reqname, r.fun.reqstart, r.fun.reqend)
            r.relstart = self.funrelstart(r.fun.reqname, r.fun.reqstart, r.fun.reqend)
            startmarkups = [r.fun.reqstart, r.rfistart, r.rfnstart,
                            r.rnfstart, r.rgnstart, r.relstart,
                            r.fun.reqend]
            startmarkups.sort()
            #result = "FUN id=%s [bytes=%d/%d]:\t'%s'\n" % (r.fun.reqid, r.fun.reqstart, r.fun.reqend, r.fun.reqname)
            #print(result)
            r.rfiend   = self.funsecend(r.fun.reqname, r.rfistart, startmarkups)
            r.rfnend   = self.funsecend(r.fun.reqname, r.rfnstart, startmarkups)
            r.rnfend   = self.funsecend(r.fun.reqname, r.rnfstart, startmarkups)
            r.rgnend   = self.funsecend(r.fun.reqname, r.rgnstart, startmarkups)
            r.relend   = self.funsecend(r.fun.reqname, r.relstart, startmarkups)
            
            self.fundict[r.fun.reqid] = r
            
            if r.rfistart != -1:
                # NG parser uses reqid for indexing instead of reqname
                r.rfi = self.gettagdic(r.fun.reqid, 'RFI', r.rfistart, r.rfiend)
            if r.rfnstart != -1:
                r.rfn = self.gettagdic(r.fun.reqid, 'RFN', r.rfnstart, r.rfnend)
            if r.rnfstart != -1:
                r.rnf = self.gettagdic(r.fun.reqid, 'RNF', r.rnfstart, r.rnfend)
            if r.rgnstart != -1:
                r.rgn = self.gettagdic(r.fun.reqid, 'RGN', r.rgnstart, r.rgnend)
        pass
    
    #def gettagdic(self, funstr, tag, start, end):
    #    if start != 0:
    #        beginloc = start
    #    else:
    #        beginloc = self.funstart(funstr)
    #    if end != 0:
    #        endloc = end
    #    else:
    #        endloc = self.funend(funstr)
    #    #funid = self.funid(funstr)
    #    #funidstr = self.fundict[funid].reqname
    #    #funidstr = self.funidname(funstr)
    #    self.f.seek(beginloc)
    #    loc = beginloc #self.f.tell()
    #    
    #    insection = 1
    #    findstr = "^" + tag + ".*"
    #    expr = re.compile(findstr)
    #    findstr = self.utf8(findstr)
    #    result = {}
    #    self.vlog(VERB_MAX, "finding from %d... '%s'" % (loc, findstr))
    #    
    #    #pos = 0
    #    #if endpos is None:
    #    #    endpos = len(text)
    #    #d = {}
    #    #while 1:
    #    #    m = entityRE.search(text,pos,endpos)
    #    #    if not m:
    #    #        break
    #    #    name,charcode,comment = m.groups()
    #    #    d[name] = charcode,comment
    #    #    pos = m.end()
    #    #return d
    #
    #    isfirst = 1
    #    reqbody = ""
    #    while insection:
    #        line = self.f.readline()
    #        loc += len(line)
    #        #self.search_file(findstr, beginloc, endloc)   
    #        m = re.search(findstr, line)#, beginloc, endloc)
    #        #print("found error", m.)
    #        if m and len(m.group(0)) > 9:
    #            inbody = 1
    #            tagitem = m.group(0)#[:6]
    #            reqid = self.getfunid(tagitem)
    #            reqname = self.getfunname(tagitem)
    #            reqstart = self.f.tell()
    #            while inbody and insection:
    #                line = self.f.readline()
    #                loc += len(line)
    #                m = re.search(findstr, line)
    #                ended = re.search("^Media\r\n", line)
    #                if (m == None or (m != None and len(m.group(0)) > 9)) and (ended == None):
    #                    reqbody += line
    #                inbody = (m == None or (m != None and len(m.group(0)) == 8)) and (ended == None)
    #                insection = loc < endloc
    #            reqend = self.f.tell()
    #            newreq = model.ReqModel(reqid, reqname, reqstart, reqend)
    #            newreq.reqbody = reqbody
    #            reqbody = ''
    #            result[reqid] = newreq
    #            #self.vlog(VERB_MAX, "M IS TRUE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #            #print()
    #            #resultdict[] = 
    #            
    #            #print("found error", m.group(1))
    #        #loc = self.f.find(findstr, loc, endloc)
    #        self.f.seek(loc)
    #        insection = loc < endloc
    #        #self.vlog(VERB_MAX, "line: '%s'" % (line))
    #        #if cond:
    #        #    line = self.f.readline()
    #        #    if line:
    #        #        self.vlog(VERB_MAX, "found on location %d | '%s'" % (m.start(), m.group()))
    #        #    pass
    #    return result
    
    #---- mainline

def main(argv):
    rfp = ReqBoxFileParserNG()
    rfp.importsdir = './data/'
    if rfp.parsingasutf8win():# rfp.parsingasutf8win():
        #rfp.parsefile("./data/LRCv12-utf8-win.txt") # SAVE AS UTF-8 in Win!!
        #rfp.parsefile("./data/LRCv12-utf8-dow2unix-l.txt")
        #rfp.parsefile("./data/LRCv12-win.txt")
        rfp.parsefile("./data/LFv14.ms.default.txt")
    elif self.parsingasutf8wincrlf():
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
    #rfp.printfun("18", self.utf8("Manter Prontuário"))
    #rfp.printfun("43", self.utf8("Manter Plano de Ação"))
    rfp.vlog(VERB_MED, "rfp = \n%s" % (rfp))
    #rfp.getrfidic(self.utf8("Manter Tabela de Retenção Tributária"))
    del rfp

if __name__ == "__main__":
    sys.exit(main(sys.argv))
