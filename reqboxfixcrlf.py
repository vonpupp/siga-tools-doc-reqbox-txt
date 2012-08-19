# -*- coding: utf-8 -*-
#   Project:			SIGA
#   Component Name:		reqboxfixcrlf
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
#   Description:		This script it is a format fixing tool.
#       MS files sometimes have '\r' character only instead of '\r\n'. This tool
#       fixes those cases for properly parsing the file
#
#   Limitations:		Error handling is not correctly implemented, time constraints
#	The code is not clean and elegant as it should, again, time constraints
#   Database tables used:	None 
#   Thread Safe:	        No
#   Extendable:			No
#   Platform Dependencies:	Linux (openSUSE used)
#   Compiler Options:
"""
    Fixes *\r* patterns from MS Word files, converting them to *\r\n* 

    Command Line Usage:
        reqboxfixcrlf {<option> <argument>}

    Options:
        -i, --input                 Input file
        -o, --output                Output file
        
    Examples:
"""

import logging, sys, mmap, shutil, contextlib, codecs, re
from vlog import vlogger
    
VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

def utf8(s):
    return s.encode('utf-8')

def fixcrlf(sourcefile, destinationfile):
    vlog = vlogger(2, sys.stdout)
    vlog(VERB_MIN, "Inputfile: %s" % sourcefile)
    print("1")
    
    sf = codecs.open(sourcefile, encoding='latin-1', mode='r') # open(filename, 'r')
    #sf = open(sourcefile, 'r')
    sm = mmap.mmap(sf.fileno(), 0, access=mmap.ACCESS_READ)
    
    #df = codecs.open(destinationfile, encoding='utf-8', mode='wb') # open(filename, 'r')
    df = open(destinationfile, 'wb')
    #dm = mmap.mmap(df.fileno(), 0)#, access=mmap.ACCESS_DEFAULT)

    loc = 0
    end = sm.size()
    terminator = b'\r\n'
    linecounter = 0
    totallines = 0
    while loc < end:
        fileline = sm.readline()
        vlog(VERB_MED, "parsing line: %d" % linecounter)
#        fileline = fileline.encode('utf-8')
        loc = loc + len(fileline)
        count = fileline.count(b'\r')
        if count == 1:
            print(type(fileline))
            df.write(fileline)
            totallines += 1
        else:
            vlog(VERB_MED, "FIXING multiline: %d lines on source line %d" % (count, linecounter))
            fileline = fileline.replace(b'\r', b'\r\n')
            df.write(fileline)
            totallines += count
        linecounter += 1
    vlog(VERB_MIN, "Inputfile: %s" % sourcefile)
    vlog(VERB_MIN, "  * Total number of lines: %d" % linecounter)
    vlog(VERB_MIN, "Outfile: %s" % destinationfile)
    vlog(VERB_MIN, "  * Total number of lines: %d" % totallines)
        
    def fixdoublecrlf(sourcefile, destinationfile):
        # HEX pattern to match: 0D0A0A0D0A
        # Idea: just remove 0A0D0A
        pass

def main(argv):
    if len(argv) == 3:
        fixcrlf(argv[1], argv[2] + ".tmp")
        fixdoublecrlf(argv[2] + ".tmp", argv[2])

if __name__ == "__main__":
    sys.exit(main(sys.argv))