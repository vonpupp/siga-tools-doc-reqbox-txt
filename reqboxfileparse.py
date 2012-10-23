#!/usr/bin/python3.1
# -*- coding: utf-8 -*-
#
#   Project:			SIGA
#   Component Name:		reqboxfileparse
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
#   Description:		This script will parse tags within a utf8 converted
#       doc file. It is mainly to be used by reqboxmodel.py
#
#   Limitations:		Error handling is not correctly implemented, time constraints
#	The code is not clean and elegant as it should, again, time constraints
#   Database tables used:	None 
#   Thread Safe:	        No
#   Extendable:			No
#   Platform Dependencies:	Linux (openSUSE used)
#   Compiler Options:		

"""
    Physical data parsing model. This is not intended to be used directly on the commandline.
"""

import logging, sys, mmap, shutil, contextlib, codecs, re
from vlog import vlogger
import reqboxmodel as model

#sys.setdefaultencoding('utf-8')

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

PARSETYPE = 'utf8-win'
#PARSETYPE = 'utf8-win-crlf'

    
def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

class tagstruc():
    def __init__(self):
        # Public
        pass

class funstruc():
    def __init__(self):
        # Public
        pass

class ReqBoxFileParser(object):
    """ Requirements doc file parsing
    Attributes:
        - file: string
    """
    filename = ''
    funlist = []
    fundict = {}
    file = None
    f = None
    
    def __init__(self):
        # Public
        self.filename = ''
        self.funlist = []
        self.fundict = {}
        
        # Init vlogger
        self.__verbosity = VERB_MAX
        self.vlog = vlogger(self.__verbosity, sys.stdout)
        #self.vlog = self.__log()
        
        # Init mmap
        self.file = None
        self.f = None
        pass
    
    def get_f(self):
        return self.f
    
    def utf8(self, s):
        return s.encode('utf-8')
#    return unicode(s, "utf-8")

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
        self.getfundict("\r\n") # No prefix, refactored parameter when this class became super of the ng version
        self.vlog(VERB_MED, "fundict = %s" % (self.fundict))
        pass
    
    def __del__(self):
        self.fundict.clear()
        if self.f:
            self.f.close()
        if self.file:
            self.file.close()
        del self.funlist
        del self.fundict
        del self.f
        del self.file
        pass
    
    #---- internal support stuff
    
    def parsingasutf8_win(self):
        return PARSETYPE == 'utf8-win'
    
    def parsingasutf8_win_crlf(self):
        return PARSETYPE == 'utf8-win-crlf'
    
    def __cleanfunfromindex_oo(self, s):
        """
        Returns a clean string from unwanted things at the index, ex:
        s = '183.Gerar Relatório de Arquivo de Retorno (Bancos)	67'
        result = 'Gerar Relatório de Arquivo de Retorno (Bancos)'
        
        Args:
            s -- the string
        """
        result = s.strip()
        result = result.split(self.utf8("\t"))[0]
        if result is not self.utf8(""):
            result = result.split(self.utf8("."))[1]
            result = result.rstrip() # Trim leading spaces (Ex: FUN 43)
            result = result.lstrip()
        return result
    
    def __cleanfunfromindex_utf8_win(self, s):
        """
        Returns a clean string from unwanted things at the index, ex:
        s = '4.	Manter Plano de Contas Padrão	6'
        result = 'Manter Plano de Contas Padrão'
        
        Args:
            s -- the string
        """
        result = s.strip()
        if len(result.split(self.utf8("\t"))) > 1:
            result = result.split(self.utf8("\t"))[1]
        if result is not self.utf8(""):
            result = result.strip()
        return result
    
    def __cleanfunfromindex_msw(self, s):
        """
        Returns a clean string from unwanted things at the index, ex:
        s = '183.Gerar Relatório de Arquivo de Retorno (Bancos)	67'
        result = 'Gerar Relatório de Arquivo de Retorno (Bancos)'
        
        Args:
            s -- the string
        """
        result = s.strip()
        #result = result.rstrip() # Trim leading spaces (Ex: FUN 43)
        #result = result.lstrip()
        if result is not self.utf8(""):
            self.vlog(VERB_MED, "len = '%d'" % len(result.split(self.utf8("\t"))))
            self.vlog(VERB_MED, "result = '%s'" % result)
            if result != b'\xe2\x80\x83':
                result = result.split(self.utf8("\t"))[1]
                self.vlog(VERB_MED, "RESULT IS CRAP = '%s'" % result)
            #result = result.split(".")[1]
            result = result.rstrip() # Trim leading spaces (Ex: FUN 43)
            result = result.lstrip()
        return result
    
    def __cleanfunfromindex(self, s):
        if self.parsingasutf8_win_crlf():
            return self.__cleanfunfromindex_msw(s)
        elif self.parsingasutf8_win():
            return self.__cleanfunfromindex_utf8_win(s)
        else:
            return self.__cleanfunfromindex_oo(s)

    def _cleanfunfrombody_oo(self, s):
        """
        Returns a clean string from unwanted things at the body, ex:
        s = '183. Gerar Relatório de Arquivo de Retorno (Bancos)'
        result = 'Gerar Relatório de Arquivo de Retorno (Bancos)'
        
        Args:
            s -- the string
        """
        result = self.__cleanfunfromindex(s)
        result = result.strip()
        #result = result.split("\n")[0]
        #if result is not "":
        #    result = result.split(".")[1]
        return result

    def _cleanfunfrombody_msw(self, s):
        """
        Returns a clean string from unwanted things at the body, ex:
        s = '183. Gerar Relatório de Arquivo de Retorno (Bancos)'
        result = 'Gerar Relatório de Arquivo de Retorno (Bancos)'
        
        Args:
            s -- the string
        """
        #result = self.__cleanfunfromindex(s)
        result = s.strip()
        #result = result.split("\n")[0]
        if result is not self.utf8(""):
            #result = result.split(self.utf8(".\t"))[1]
            result = result.split(self.utf8(".\t"))[1]
        return result
    
    def _cleanfunfrombody(self, s):
        if self.parsingasutf8_win_crlf():
            return self._cleanfunfrombody_msw(s)
        else:
            return self._cleanfunfrombody_oo(s)

    def getfunid(self, s):
        """
        Returns the index of a funstr s, ex:
        s = '183. Gerar Relatório de Arquivo de Retorno (Bancos)	67'
        result = '183'
        
        Args:
            s -- the string
        """        
        result = s.split(self.utf8("."))[0]
        result = result.strip()
        return result
    
    def getfunname(self, s):
        """
        Returns the index of a funstr s, ex:
        s = 'RFI227. MANTER REMESSA DE CARTÃO DE IDENTIFICAÇÃO'
        result = 'MANTER REMESSA DE CARTÃO DE IDENTIFICAÇÃO'
        
        Args:
            s -- the string
        """        
        result = s.split(self.utf8("."))[1]
        result = result.strip()
        return result
    
    def bodystartloc(self):
        # Find the position of the begining tag
        self.f.seek(0)
        begintag = self.utf8("Lista Completa de Funcionalidades")
        beginloc = self.f.find(begintag)
        # Find the position of the end tag
        endtag = "Lista Completa de Funcionalidades"
        if self.parsingasutf8_win_crlf() or self.parsingasutf8_win():
            endtag = endtag.upper() #"LISTA COMPLETA DE FUNCIONALIDADES"
        endtag = self.utf8(endtag)
        endloc = self.f.find(endtag, beginloc+1)
        # Set the cursor at the begining tag & skip the first line
        self.f.seek(endloc)
        #self.f.readline()
        #loc = self.f.tell()
        return endloc
    
    def getfunlist(self):
        """
        Fills the funlist list with all the parsed functionalities based on the index.
        """
        self.vlog(VERB_MED, "-> %s" % __name__)
        
        # Find the position of the begining tag
        #begintag = "Lista Completa de Funcionalidades"
        #beginloc = self.f.find(begintag)
        ## Find the position of the end tag
        #endtag = "LISTA COMPLETA DE FUNCIONALIDADES"
        #endloc = self.f.find(endtag, beginloc+1)
        ## Set the cursor at the begining tag & skip the first line
        #self.f.seek(beginloc)
        self.f.seek(0)
        begintag = self.utf8("Lista Completa de Funcionalidades")
        beginloc = self.f.find(begintag)
        endloc = self.bodystartloc()
        self.f.seek(beginloc)
        self.f.readline()
        loc = self.f.tell()
        
        #self.vlog(VERB_MAX, "beginloc = %d" % beginloc)
        #self.vlog(VERB_MAX, "endloc = %d" % endloc)
        
        self.funlist = []
        count = 0
        while (loc < endloc):
            line = self.f.readline()
            loc = self.f.tell()
            self.vlog(VERB_MAX, "reading line '%s' bytes = %d" % (line, loc))
            line = self.__cleanfunfromindex(line)
            
            self.vlog(VERB_MAX, "cleaned line '%s'" % (line))
            if line is not self.utf8("") and (line != b'\xe2\x80\x83'):
                self.funlist += [line]
                count += 1
                #if self.parsingasutf8_win_crlf():
                #    self.funlist += [line.decode('utf-8').upper().encode('utf-8')]
                #else:
                #    self.funlist += [line]
        
        #self.vlog(VERB_MED, "<- getfunlist()")
        self.vlog(VERB_MED, "<- %s" % __name__)
        self.vlog(VERB_MAX, "result = %s" % (self.funlist))
        #self.funlist += [result]
        return self.funlist
    
    def getfundict(self, prefix):
        """
        Fills the fundict property with a dict where each element is indexed
        by the fun name and each value is an object from the model
        """
        self.vlog(VERB_MED, "-> getfundict()")
        self.fundict = {}
        
        beginloc = self.bodystartloc()
        finalloc = self.f.size() - 1
        endloc = finalloc
        self.f.seek(beginloc)
        self.vlog(VERB_MAX, "bytes = %d" % (beginloc))
        count = len(self.funlist)
        
        # Iterate on the file backwards, it's more natural and easier...
        for idx, funstr in enumerate(reversed(self.funlist)):
            newidx = count - idx
            #newfunstr = "%s. %s" % (newidx, funstr)
            #newfunstr = self.utf8(str(newidx) + ".\t") + funstr
            fieldterm = "\r\n"
            if self.parsingasutf8_win_crlf():
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
            elif self.parsingasutf8_win():
                #newfunstr = self.utf8(fieldterm + prefix + str(newidx) + ". ") # + funstr
                # This doesn't seems to be very elegant, but I don't see another way of doing it
                # without overriding the whole method (which I prefeer not to do it)
                if isinstance(self.__class__, ReqBoxFileParser):
                    newfunstr = self.utf8(prefix + str(newidx) + ". ") # + funstr
                else:
                    stridx = str(newidx).zfill(3)
                    newfunstr = self.utf8(prefix + stridx + ". ") # + funstr
                #newfunstr = self.utf8(newfunstr)
                pass
            self.vlog(VERB_MAX, "looking for: '%s'" % (newfunstr))
            #beginloc = self.f.rfind(newfunstr, beginloc, endloc)
            beginloc = 0
            beginloc = self.f.rfind(newfunstr, beginloc, endloc)
            if beginloc != -1:
                beginloc += 2
                self.f.seek(beginloc)
                line = self.f.readline()
                fieldsize = 85
                if self.parsingasutf8_win_crlf():
                    if len(line.strip()) > fieldsize:
                        print("-----------------------------------MULTILINE")
                funid = self.getfunid(line)
                line = self._cleanfunfrombody(line)
                self.vlog(VERB_MAX, "found from %d to %d out of %d | '%s. %s'" % (beginloc, endloc, finalloc, funid, line))
                #self.fundict[funstr] = (beginloc, endloc, funid)
                # I switched the dict keys from uppercase (body) to as they are
                # on the index (capitalized as they are)
                
                currentpos = self.f.tell()
                
                #newidx = count - funidx
                r = model.FunModel(funid, funstr, beginloc, endloc)
                r.fun.reqstart = beginloc
                r.fun.reqend   = endloc
                r.rfistart = self.funrfistart(funstr, beginloc, endloc)
                r.rfnstart = self.funrfnstart(funstr, beginloc, endloc)
                r.rnfstart = self.funrnfstart(funstr, beginloc, endloc)
                r.rgnstart = self.funrgnstart(funstr, beginloc, endloc)
                startmarkups = [r.fun.reqstart, r.rfistart, r.rfnstart, r.rnfstart, r.rgnstart, r.fun.reqend]
                startmarkups.sort()
                result = "FUN id=%s [bytes=%d/%d]:\t'%s'\n" % (r.fun.reqid, r.fun.reqstart, r.fun.reqend, r.fun.reqname)
                print(result)
                r.rfiend   = self.funsecend(funstr, r.rfistart, startmarkups)
                r.rfnend   = self.funsecend(funstr, r.rfnstart, startmarkups)
                r.rnfend   = self.funsecend(funstr, r.rnfstart, startmarkups)
                r.rgnend   = self.funsecend(funstr, r.rgnstart, startmarkups)
                #self.vlog(VERB_MED, "%s" % (self.printfun(funidx+1, funname)))
    #            self.fun[funname].rfi = self.fp.gettagdic(funname, 'RFI')
                
                self.fundict[funstr] = r #(beginloc, endloc, funid)
                
                if r.rfistart != -1:
                    r.rfi = self.gettagdic(funstr, 'RFI', r.rfistart, r.rfiend)
                    pass
                if r.rfnstart != -1:
                    r.rfn = self.gettagdic(funstr, 'RFN', r.rfnstart, r.rfnend)
                if r.rnfstart != -1:
                    r.rnf = self.gettagdic(funstr, 'RNF', r.rnfstart, r.rnfend)
                if r.rgnstart != -1:
                    r.rgn = self.gettagdic(funstr, 'RGN', r.rgnstart, r.rgnend)
                
                self.f.seek(currentpos)
                
                endloc = beginloc - 1
                beginloc = 0
            else:
                # TODO: An exception should be raised here
                pass
        
        self.vlog(VERB_MED, "<- getfundict()")
        pass
    
    def funhassection(self, funstr, secstr, start=0, end=0):
        """
        Returns the position in bytes if a funstr has an secstr section within,
        or -1 if it is not found.
        It also moves the caret on the section start
        
        Args:
            funstr -- the string
            secstr -- the string
        """
        if start == 0:
            beginloc = self.funstart(funstr)
        else:
            beginloc = start
        if end == 0:
            endloc = self.funend(funstr)
        else:
            endloc = end
        #self.vlog(VERB_MAX, "pos = %d" % (self.f.tell()))
        self.f.seek(beginloc)
        #self.vlog(VERB_MAX, "pos = %d" % (self.f.tell()))
        header = secstr
        if self.parsingasutf8_win_crlf() or self.parsingasutf8_win():
            #header = header.upper()
            #header = self.utf8(header.decode('utf-8').upper())
            header = header.decode('utf-8').upper().encode('utf-8')
        # Secstr is always going to be a str, so it needs to be converted to utf8
        #header = self.utf8(header)
        found = self.f.find(header, beginloc+1, endloc-1)
        #self.vlog(VERB_MAX, "found = %d" % (found))
        if not found in range(beginloc, endloc):
            return -1
        else:
            return found
        #return found in range(beginloc, endloc)

    def getorderedstarts(self, funstr):
        funstart = self.funstart(funstr)
        funend   = self.funend(funstr)
        rfistart = self.funrfistart(funstr)
        rfnstart = self.funrfnstart(funstr)
        rnfstart = self.funrnfstart(funstr)
        rgnstart = self.funrgnstart(funstr)
        startmarkups = [funstart, rfistart, rfnstart, rnfstart, rgnstart, funend]
        startmarkups.sort()
        return startmarkups

    def funsecend(self, funstr, secstart, startmarkups):
        #startmarkups = self.getorderedstarts(funstr)
        result = -1
        #secstart = self.funrfistart(funstr)
        if secstart != -1:
            result = startmarkups[startmarkups.index(secstart)+1] -1
        return result
        
    def funrfistart(self, funstr, start=0, end=0):
        header = "Requisitos Funcionais de Interface"
        return self.funhassection(funstr, header, start, end)
        
    def funrfiend(self, funstr, secstart, startmarkups):
        #startmarkups = self.getorderedstarts(funstr)
        result = -1
        #secstart = self.funrfistart(funstr)
        if secstart != -1:
            result = startmarkups[startmarkups.index(secstart)+1]
        return result
        
    def funrfnstart(self, funstr, start=0, end=0):
        header = "REQUISITOS FUNCIONAIS DE NEG"
        #"Requisitos Funcionais de Negócio"
        return self.funhassection(funstr, header, start, end)

    def funrfnend(self, funstr, secstart, startmarkups):
        #startmarkups = self.getorderedstarts(funstr)
        result = -1
        #secstart = self.funrfnstart(funstr)
        if secstart != -1:
            result = startmarkups[startmarkups.index(secstart)+1]
        return result
        
    def funrnfstart(self, funstr, start=0, end=0):
        #header = "Requisitos Não Funcionais"
        header = "Requisitos N"
        return self.funhassection(funstr, header, start, end)
        
    def funrnfend(self, funstr, secstart, startmarkups):
        #startmarkups = self.getorderedstarts(funstr)
        result = -1
        #secstart = self.funrnfstart(funstr)
        if secstart != -1:
            result = startmarkups[startmarkups.index(secstart)+1]
        return result
        
    def funrgnstart(self, funstr, start=0, end=0):
        #header = "Regras de Negócio"
        header = "Regras de Neg"
        return self.funhassection(funstr, header, start, end)
        
    def funrgnend(self, funstr, secstart, startmarkups):
        #startmarkups = self.getorderedstarts(funstr)
        result = -1
        #secstart = self.funrgnstart(funstr)
        if secstart != -1:
            result = startmarkups[startmarkups.index(secstart)+1]
        return result
        
    def funstart(self, funstr):
        return self.fundict[funstr].fun.reqstart
        #self.fundict[funstr][0]
        
    def funend(self, funstr):
        return self.fundict[funstr].fun.reqend #[1]
        
    def funid(self, funstr):
        return self.fundict[funstr].fun.reqid #[2]
        
    def funidname(self, funstr):
        funid = self.funid(funstr)
        return "%s. %s" % (funid, funstr)
        
    def search_file(self, pattern, boffset, eoffset):
        self.f.seek(boffset)
        #line = f.readline()
        for line in self.f:
            #m = patter.search(line)
            self.vlog(VERB_MAX, "line: '%s'" % (line))
            m = re.match(pattern, line)
            if m:
                self.vlog(VERB_MAX, "FOUND: '%s'" % (line))
                search_offset = self.f.tell() - len(line) - 1
                return search_offset + m.start(), search_offset + m.end()

    def tagid(self, tagstr):
        return self.fundict[funstr][2]
        
    def tagidname(self, tagstr):
        funid = self.fundict[funstr][2]
        return "%s. %s" % (funid, funstr)
        
    def cleantagid(self, tagstr):
        return self.fundict[funstr][2]
        
    def cleantagbody(self, tagstr):
        funid = self.fundict[funstr][2]
        return "%s. %s" % (funid, funstr)

    def gettagdic(self, funstr, tag, start, end):
        if start != 0:
            beginloc = start
        else:
            beginloc = self.funstart(funstr)
        if end != 0:
            endloc = end
        else:
            endloc = self.funend(funstr)
        #funid = self.funid(funstr)
        #funidstr = self.funidname(funstr)
        self.f.seek(beginloc)
        loc = beginloc #self.f.tell()
        
        insection = 1
        findstr = "^" + tag + ".*"
        expr = re.compile(findstr)
        findstr = self.utf8(findstr)
        result = {}
        self.vlog(VERB_MAX, "finding from %d... '%s'" % (loc, findstr))
        
        #pos = 0
        #if endpos is None:
        #    endpos = len(text)
        #d = {}
        #while 1:
        #    m = entityRE.search(text,pos,endpos)
        #    if not m:
        #        break
        #    name,charcode,comment = m.groups()
        #    d[name] = charcode,comment
        #    pos = m.end()
        #return d

        isfirst = 1
        reqbody = ""
        while insection:
            line = self.f.readline()
            loc += len(line)
            #self.search_file(findstr, beginloc, endloc)   
            m = re.search(findstr, line)#, beginloc, endloc)
            #print("found error", m.)
            if m and len(m.group(0)) > 9:
                inbody = 1
                tagitem = m.group(0)#[:6]
                reqid = self.getfunid(tagitem)
                reqname = self.getfunname(tagitem)
                reqstart = self.f.tell()
                while inbody and insection:
                    line = self.f.readline()
                    loc += len(line)
                    m = re.search(findstr, line)
                    ended = re.search("^Media\r\n", line)
                    if (m == None or (m != None and len(m.group(0)) > 9)) and (ended == None):
                        reqbody += line
                    inbody = (m == None or (m != None and len(m.group(0)) == 8)) and (ended == None)
                    insection = loc < endloc
                reqend = self.f.tell()
                newreq = model.ReqModel(reqid, reqname, reqstart, reqend)
                newreq.reqbody = reqbody
                reqbody = ''
                result[reqid] = newreq
                #self.vlog(VERB_MAX, "M IS TRUE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                #print()
                #resultdict[] = 
                
                #print("found error", m.group(1))
            #loc = self.f.find(findstr, loc, endloc)
            self.f.seek(loc)
            insection = loc < endloc
            #self.vlog(VERB_MAX, "line: '%s'" % (line))
            #if cond:
            #    line = self.f.readline()
            #    if line:
            #        self.vlog(VERB_MAX, "found on location %d | '%s'" % (m.start(), m.group()))
            #    pass
        return result
        pass
    
    #def printmap(self, d):
    #    for k, v in d.items():
    #        self.vlog(VERB_MAX, "[%s] | %s" % (k, v))
                
            
    def printfun(self, idx, funstr):
        result = ""
        if not funstr in self.fundict:
            result = "ERROR %s [%s] not found, and it should exist!!!\n" % (idx, funstr)
        else:
            t = self.fundict[funstr]
            beginloc = self.funstart(funstr)
            endloc = self.funend(funstr)
            funid = self.funid(funstr)
            funname = funstr #.upper()
            result = "FUN %s: '%s' [%d | %d]\n" % (funid, funname, beginloc, endloc)
            if self.funrfistart(funstr) != -1:
                result = result + "RFIs\n"
                #rfidict = self.gettagdic(funstr, 'RFI')
            #if self.funhasrfn(funstr):
            #    result = result + "RFNs\n"
            #if self.funhasrnf(funstr):
            #    result = result + "RNFs\n"
            #if self.funhasrng(funstr):
            #    result = result + "RNGs\n"
        return result

    def printf(self):
        result = ""
        for idx, funstr in enumerate(self.funlist):
            result = result + self.printfun(idx + 1, funstr)
        
    def __str__(self):
        result = ""
        for idx, funstr in enumerate(self.funlist):
            result = result + self.printfun(idx + 1, funstr)
        return result
    
    #---- mainline

def main(argv):
    rfp = ReqBoxFileParser()
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
    #rfp.printfun("18", self.utf8("Manter Prontuário"))
    #rfp.printfun("43", self.utf8("Manter Plano de Ação"))
    rfp.vlog(VERB_MED, "rfp = \n%s" % (rfp))
    #rfp.getrfidic(self.utf8("Manter Tabela de Retenção Tributária"))
    del rfp

if __name__ == "__main__":
    sys.exit(main(sys.argv))
