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
        self.__file = open(filename, 'r')
        self.vlog(VERB_MIN, "opening file: %s" % filename)
        self.__f = mmap.mmap(self.__file.fileno(), 0, access=mmap.ACCESS_READ)
        self.__f.seek(0) # rewind
        self.funlist = []
        self.funlocmap = {}
        pass
    
    #---- internal support stuff
    
    def cleanfunfromindex(self, s):
        result = s.strip()
        result = result.split("\t")[0]
        if result is not "":
            result = result.split(".")[1]
        return result
    
    def getfunlist(self):
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
        
        result = []
        while (loc < endloc):
            line = self.__f.readline()
            loc = self.__f.tell()
            self.vlog(VERB_MAX, "reading line '%s' bytes = %d" % (line, loc))
            line = self.cleanfunfromindex(line)
            self.vlog(VERB_MAX, "cleaned line '%s'" % (line))
            if line is not "":
                result.append(line)
        
        #self.vlog(VERB_MED, "<- getfunlist()")
        self.vlog(VERB_MED, "<- %s" % __name__)
        #self.vlog(VERB_MAX, "result = %s" % (result))
        self.funlist.append(result)
        return result
    
    def getfunlocmap(self, funstr):
        self.vlog(VERB_MED, "-> %s" % __name__)
        self.__funlocmap = {}
        
        # Find the position of the begining tag
        self.__f.seek(0)
        beginloc = self.__f.find(funstr)
        beginloc = self.__f.find(funstr, beginloc+1)
        endloc = self.__f.size()
        #endtag = begintag
        # Set the cursor at the begining tag & skip the first line
        self.__f.seek(beginloc)
        self.__f.readline()
        loc = self.__f.tell()
        
        self.vlog(VERB_MAX, "beginloc = %d" % beginloc)
        self.vlog(VERB_MAX, "endloc = %d" % endloc)
        
        #result = []
        #while (loc < endloc):
        #    line = self.__f.readline()
        #    loc = self.__f.tell()
        #    self.vlog(VERB_MAX, "reading line '%s' bytes = %d" % (line, loc))
        #    line = self.cleanfunfromindex(line)
        #    self.vlog(VERB_MAX, "cleaned line '%s'" % (line))
        #    if line is not "":
        #        result.append(line)
        
        self.vlog(VERB_MED, "<- getfunlist()")
        pass
    
    def close(self):
        self.__f.close()
        self.__f.close()

    #---- mainline

def main(argv):
    rfp = reqboxfileparser("./Rv10.txt")
    print "INPUT:   " + rfp.filename
    
    fun = rfp.getfunlist()
    #rfp.vlog(VERB_MED, "fun = %s" % (fun))
    rfp.vlog(VERB_MED, "len(fun) = %d" % (len(fun)))
    rfp.getfunlocmap(fun[0])
    
    rfp.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
