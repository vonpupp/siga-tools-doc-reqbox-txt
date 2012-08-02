# -*- coding: utf-8 -*-
#!/usr/bin/python3.1

#   Project:			SIGA
#   Component Name:		reqboxfileparse
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
    Create a CSV file with the wireframe data based on a hierarchy.

    Command Line Usage:
        reqbox-fileparse {<option> <argument>}

    Options:
        -h, --help              Print this help and exit.
        
    Examples:
"""

import logging, sys, mmap, shutil, contextlib, codecs, re
from vlog import vlogger

#sys.setdefaultencoding('utf-8')

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

ISWORD = 1

def utf8(s):
    return s.encode('utf-8')
#    return unicode(s, "utf-8")
    
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

class reqboxfileparser():
    """ Requirements doc file parsing
    Attributes:
        - file: string
    """
    
    def __init__(self, filename):
        # Public
        self.filename = filename
        self.funlist = []
        self.fundict = {}
        
        # Init vlogger
        self.__verbosity = VERB_MAX
        self.vlog = vlogger(self.__verbosity, sys.stdout)
        #self.vlog = self.__log()
        
        # Init mmap
        self.__file = codecs.open(filename, encoding='utf-8', mode='r') # open(filename, 'r')
        self.vlog(VERB_MIN, "opening file: %s" % filename)
        self.__f = mmap.mmap(self.__file.fileno(), 0, access=mmap.ACCESS_READ)
        self.__f.seek(0) # rewind
        pass
    
    def __del__(self):
        self.fundict.clear()
        self.__f.close()
        self.__file.close()
        del self.funlist
        del self.fundict
        del self.__f
        del self.__file
        pass
    
    #---- internal support stuff
    
    def __cleanfunfromindex_oo(self, s):
        """
        Returns a clean string from unwanted things at the index, ex:
        s = '183.Gerar Relatório de Arquivo de Retorno (Bancos)	67'
        result = 'Gerar Relatório de Arquivo de Retorno (Bancos)'
        
        Args:
            s -- the string
        """
        result = s.strip()
        result = result.split(utf8("\t"))[0]
        if result is not utf8(""):
            result = result.split(utf8("."))[1]
            result = result.rstrip() # Trim leading spaces (Ex: FUN 43)
            result = result.lstrip()
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
        if result is not utf8(""):
            self.vlog(VERB_MED, "len = '%d'" % len(result.split(utf8("\t"))))
            self.vlog(VERB_MED, "result = '%s'" % result)
            if result != b'\xe2\x80\x83':
                result = result.split(utf8("\t"))[1]
                self.vlog(VERB_MED, "RESULT IS CRAP = '%s'" % result)
            #result = result.split(".")[1]
            result = result.rstrip() # Trim leading spaces (Ex: FUN 43)
            result = result.lstrip()
        return result
    
    def __cleanfunfromindex(self, s):
        if ISWORD:
            return self.__cleanfunfromindex_msw(s)
        else:
            return self.__cleanfunfromindex_oo(s)

    def __cleanfunfrombody_oo(self, s):
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

    def __cleanfunfrombody_msw(self, s):
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
        if result is not utf8(""):
            #result = result.split(utf8(".\t"))[1]
            result = result.split(utf8(".\t"))[1]
        return result
    
    def __cleanfunfrombody(self, s):
        if ISWORD:
            return self.__cleanfunfrombody_msw(s)
        else:
            return self.__cleanfunfrombody_oo(s)

    def __getfunid(self, s):
        """
        Returns the index of a funstr s, ex:
        s = '183. Gerar Relatório de Arquivo de Retorno (Bancos)	67'
        result = '183'
        
        Args:
            s -- the string
        """        
        result = s.split(utf8("."))[0]
        result = result.strip()
        return result
    
    def bodystartloc(self):
        # Find the position of the begining tag
        self.__f.seek(0)
        begintag = utf8("Lista Completa de Funcionalidades")
        beginloc = self.__f.find(begintag)
        # Find the position of the end tag
        endtag = "Lista Completa de Funcionalidades"
        if ISWORD:
            endtag = endtag.upper() #"LISTA COMPLETA DE FUNCIONALIDADES"
        endtag = utf8(endtag)
        endloc = self.__f.find(endtag, beginloc+1)
        # Set the cursor at the begining tag & skip the first line
        self.__f.seek(endloc)
        #self.__f.readline()
        #loc = self.__f.tell()
        return endloc
    
    def getfunlist(self):
        """
        Fills the funlist list with all the parsed functionalities based on the index.
        """
        self.vlog(VERB_MED, "-> %s" % __name__)
        
        # Find the position of the begining tag
        #begintag = "Lista Completa de Funcionalidades"
        #beginloc = self.__f.find(begintag)
        ## Find the position of the end tag
        #endtag = "LISTA COMPLETA DE FUNCIONALIDADES"
        #endloc = self.__f.find(endtag, beginloc+1)
        ## Set the cursor at the begining tag & skip the first line
        #self.__f.seek(beginloc)
        self.__f.seek(0)
        begintag = utf8("Lista Completa de Funcionalidades")
        beginloc = self.__f.find(begintag)
        endloc = self.bodystartloc()
        self.__f.seek(beginloc)
        self.__f.readline()
        loc = self.__f.tell()
        
        #self.vlog(VERB_MAX, "beginloc = %d" % beginloc)
        #self.vlog(VERB_MAX, "endloc = %d" % endloc)
        
        self.funlist = []
        count = 0
        while (loc < endloc):
            line = self.__f.readline()
            loc = self.__f.tell()
            self.vlog(VERB_MAX, "reading line '%s' bytes = %d" % (line, loc))
            line = self.__cleanfunfromindex(line)
            
            self.vlog(VERB_MAX, "cleaned line '%s'" % (line))
            if line is not utf8("") and (line != b'\xe2\x80\x83'):
                self.funlist += [line]
                count += 1
                #if ISWORD:
                #    self.funlist += [line.decode('utf-8').upper().encode('utf-8')]
                #else:
                #    self.funlist += [line]
        
        #self.vlog(VERB_MED, "<- getfunlist()")
        self.vlog(VERB_MED, "<- %s" % __name__)
        self.vlog(VERB_MAX, "result = %s" % (self.funlist))
        #self.funlist += [result]
        return self.funlist
    
    def getfundict(self):
        """
        Fills the fundict property with a dict where each element is indexed
        by the fun name and each value is a tuple with the (begining, end)
        positions on the file.
        """
        self.vlog(VERB_MED, "-> getfundict()")
        self.__fundict = {}
        
        beginloc = self.bodystartloc()
        finalloc = self.__f.size() - 1
        endloc = finalloc
        self.__f.seek(beginloc)
        self.vlog(VERB_MAX, "bytes = %d" % (beginloc))
        count = len(self.funlist)
        
        # Iterate on the file backwards, it's more natural and easier...
        for idx, funstr in enumerate(reversed(self.funlist)):
            newidx = count - idx
            #newfunstr = "%s. %s" % (newidx, funstr)
            #newfunstr = utf8(str(newidx) + ".\t") + funstr
            if ISWORD:
                #newfunstr = newfunstr.decode('utf-8')
                #newfunstr = utf8(newfunstr.upper())
                #newfunstr = utf8("\n" + str(newidx) + ".\t") + funstr
                fieldterm = "\r\n"
                fieldsize = 101
                #newfunstr = utf8(fieldterm + str(newidx) + ".\t") + funstr
                newfunstr = utf8(fieldterm + str(newidx) + ".\t")
                #newfunstr = utf8(str(newidx) + ".\t") + funstr
                #if len(funstr) >= fieldsize:
                #    #TODO: BREAKPOINT HERE
                #    newfunstr = newfunstr[:fieldsize] + utf8(fieldterm) # + newfunstr[fieldsize:len(newfunstr)]
                #    #newfunstr = utf8(fieldterm) + newfunstr[:fieldsize-2] + utf8(fieldterm) # + newfunstr[fieldsize:len(newfunstr)]
                #    #newfunstr = newfunstr[:fieldsize-2] # + newfunstr[fieldsize:len(newfunstr)]
                #    #newfunstr = funstr[:99]
                #newfunstr = newfunstr.decode('utf-8').upper().encode('utf-8')
                #newfunstr = newfunstr.upper()
                #utf8(str(newfunstr.upper()))#.encode('utf-8')
            else:
                newfunstr = utf8("\n" + str(newidx) + ". ") + funstr
                #newfunstr = utf8(newfunstr)
                pass
            self.vlog(VERB_MAX, "looking for: '%s'" % (newfunstr))
            #beginloc = self.__f.rfind(newfunstr, beginloc, endloc)
            beginloc = 0
            beginloc = self.__f.rfind(newfunstr, beginloc, endloc)
            if beginloc != -1:
                beginloc += 2
                self.__f.seek(beginloc)
                line = self.__f.readline()
                fieldsize = 85
                if ISWORD:
                    if len(line.strip()) > fieldsize:
                        print("-----------------------------------MULTILINE")
                funid = self.__getfunid(line)
                line = self.__cleanfunfrombody(line)
                self.vlog(VERB_MAX, "found from %d to %d out of %d | '%s. %s'" % (beginloc, endloc, finalloc, funid, line))
                #self.fundict[funstr] = (beginloc, endloc, funid)
                # I switched the dict keys from uppercase (body) to as they are
                # on the index (capitalized as they are)
                self.fundict[funstr] = (beginloc, endloc, funid)
                endloc = beginloc - 1
                beginloc = 0
            else:
                # TODO: An exception should be raised here
                pass
        
        self.vlog(VERB_MED, "<- getfundict()")
        pass
    
    def funhassection(self, funstr, secstr):
        """
        Returns the position in bytes if a funstr has an secstr section within,
        or -1 if it is not found.
        It also moves the caret on the section start
        
        Args:
            funstr -- the string
            secstr -- the string
        """
        beginloc = self.funbeginloc(funstr)
        endloc = self.funendloc(funstr)
        self.__f.seek(beginloc)
        header = secstr
        if ISWORD:
            header = header.upper()
            #header = header.decode('utf-8').upper().encode('utf-8')
        # Secstr is always going to be a str, so it needs to be converted to utf8
        header = utf8(header)
        found = self.__f.find(header, beginloc, endloc)
        if not found in range(beginloc, endloc):
            return -1
        else:
            return found
        #return found in range(beginloc, endloc)
        
    def funhasrfi(self, funstr):
        header = "Requisitos Funcionais de Interface"
        return self.funhassection(funstr, header) != -1
        
    def funhasrfn(self, funstr):
        header = "Requisitos Funcionais de Negócio"
        return self.funhassection(funstr, header) != -1
        
    def funhasrnf(self, funstr):
        header = "Requisitos Não Funcionais"
        return self.funhassection(funstr, header) != -1
        
    def funhasrng(self, funstr):
        header = "Regras de Negócio"
        return self.funhassection(funstr, header) != -1
        
    def funbeginloc(self, funstr):
        return self.fundict[funstr][0]
        
    def funendloc(self, funstr):
        return self.fundict[funstr][1]
        
    def funid(self, funstr):
        return self.fundict[funstr][2]
        
    def funidname(self, funstr):
        funid = self.fundict[funstr][2]
        return "%s. %s" % (funid, funstr)
        
    def search_file(self, pattern, boffset, eoffset):
        self.__f.seek(boffset)
        #line = f.readline()
        for line in self.__f:
            #m = patter.search(line)
            self.vlog(VERB_MAX, "line: '%s'" % (line))
            m = re.match(pattern, line)
            if m:
                self.vlog(VERB_MAX, "FOUND: '%s'" % (line))
                search_offset = self.__f.tell() - len(line) - 1
                return search_offset + m.start(), search_offset + m.end()

    def getrfidic(self, funstr):
        if self.funhasrfi(funstr):
            beginloc = self.funbeginloc(funstr)
            endloc = self.funendloc(funstr)
            funid = self.funid(funstr)
            funidstr = self.funidname(funstr)
            self.__f.seek(beginloc)
            loc = beginloc #self.__f.tell()
            cond = 1
            #findstr = "\nNome\nAlias\nDescrição\nCriticidade"
            #findstr = funidstr
            findstr = "^RFI.*"
            findstr = utf8(findstr)
            self.vlog(VERB_MAX, "finding from %d... '%s'" % (loc, findstr))
            while cond:
                #self.search_file(findstr, beginloc, endloc)
                #m = re.search(findstr, self.__f)
                #print("found error", m.)
                #if m:
                #    print("found error", m.group(1))
                #loc = self.__f.find(findstr, loc, endloc)
                line = self.__f.readline()
                loc += len(line)
                self.__f.seek(loc)
                cond = loc < endloc
                self.vlog(VERB_MAX, "line: '%s'" % (line))
                if cond:
                    #line = self.__f.readline()
                    #self.vlog(VERB_MAX, "found on location %d | '%s'" % (m.start(), m.group()))
                    pass    
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
            beginloc = self.funbeginloc(funstr)
            endloc = self.funendloc(funstr)
            funid = self.funid(funstr)
            funname = funstr #.upper()
            result = "FUN %s: '%s' [%d | %d]\n" % (funid, funname, beginloc, endloc)
            if self.funhasrfi(funstr):
                result = result + "RFIs\n"
            #if self.funhasrfn(funstr):
            #    result = result + "RFNs\n"
            #if self.funhasrnf(funstr):
            #    result = result + "RNFs\n"
            #if self.funhasrng(funstr):
            #    result = result + "RNGs\n"
        return result
        
    def __str__(self):
        result = ""
        for idx, funstr in enumerate(self.funlist):
            result = result + self.printfun(idx + 1, funstr)
        return result
    
    #---- mainline

def main(argv):
    if ISWORD:
        #rfp = reqboxfileparser("./data/LRCv12-utf8-win.txt") # SAVE AS UTF-8 in Win!!
        #rfp = reqboxfileparser("./data/LRCv12-utf8-win-dos2unix.txt") # SAVE AS UTF-8 in Win!!
        rfp = reqboxfileparser("./data/LRCv12-utf8-crlf.txt") # SAVE AS UTF-8 in Win!!
        #rfp = reqboxfileparser("./data/Rv12w.txt")
    else:
        #rfp = reqboxfileparser("./data/Rv12.txt")
        pass
    print("INPUT:   " + rfp.filename)
    
    rfp.getfunlist()
    #rfp.vlog(VERB_MED, "fun = %s" % (rfp.funstr))
    rfp.vlog(VERB_MED, "len(fun) = %d" % (len(rfp.funlist)))
    rfp.getfundict()
    rfp.vlog(VERB_MED, "fundict = %s" % (rfp.fundict))
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
