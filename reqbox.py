# -*- coding: utf-8 -*-
#!/usr/bin/env python

#   Project:			SIGA
#   Component Name:		reqbox
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
import reqboxmodel as rbm

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

def main(argv):
    wfl = WF()
    try:
        optlist, args = getopt.getopt(argv[1:], 'hp:r:f:o:v:l:s:', ['help', 'verbose', 'export-all', 'export-rfi', 'export-rfn'])
    except getopt.GetoptError, msg:
        sys.stderr.write("reqbox: error: %s" % msg)
        sys.stderr.write("See 'reqbox --help'.\n")
        return 1

    print str(optlist)
    for opt, optarg in optlist:
        if opt in ('-h', '--help'):
            sys.stdout.write(__doc__)
            return 0
        elif opt in ('-v', '--verbose'):
            #wfl.setVerbosity(int(optarg))
            #wfl.logv(VERB_MED, "main.optarg[%d]" % len(optlist))
            #wfl.logv(VERB_MED, "main.optarg = " .join(map(str, optarg)))
            #wfl.logv(VERB_MED, "main.optlist = " .join(map(str, optlist)))
            pass
        elif opt in ('-a', '--export-all'):
            wfl.logfile = optarg            
            wfl.logv(VERB_MED, "main.optarg = " .join(map(str, optarg)))
            if wfl.isVerbose:
                wfl.setLogger('/home/afu/Dropbox/mnt-ccb/siga/siga-tools/siga-tools-wf2ea/myapp.log')
            pass

    rbm = reqboxmodel()
    
    fh = open("out-rfi-objects.csv", 'wb')
    rbm.exporter_rfi(fh)
    
    rbm.builduniquerfndict()
    fh = open("out-rfn-objects.csv", 'wb')
    rbm.exporter_rfn(fh)
    
    rbm.builduniquernfdict()
    fh = open("out-rnf-objects.csv", 'wb')
    rbm.exporter_rnf(fh)

    rbm.builduniquergndict()
    fh = open("out-rgn-objects.csv", 'wb')
    rbm.exporter_rgn(fh)
    
    fh = open("out-fun-objects.csv", 'wb')
    rbm.exporter_funobjects(fh)
    
    fh = open("out-fun-rfi-relationships.csv", 'wb')
    rbm.exporter_funrfilinks(fh)
    
    fh = open("out-rfi-fun-relationships.csv", 'wb')
    rbm.exporter_rfifunlinks(fh)

    print "OUTPUT:  " + wfl.outfile
    print " * Replace:  " + wfl.replacepath
    print " * Fix with: " + wfl.prependpath
#    print "wfl.verbosity=" + str(wfl.__verbosity)

if __name__ == "__main__":
    sys.exit(main(sys.argv))