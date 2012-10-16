# -*- coding: utf-8 -*-
#!/usr/bin/env python

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
        self.wrf = {}
        pass

def main(argv):
    rbm = model.ReqBoxModel(rfp.ReqBoxFileParserNG)
    rbm.parsefile("./input/LRCv13-mod.utf8.fix.txt")
    rbm.printf()
    
    rbm.fixsecondlevelbullets()
    
    fh = open("rfi-objects.csv", 'wb')
    rbm.exporter_rfiobjects(fh)
    
    rbm.builduniquerfndict()
    fh = open("rfn-objects.csv", 'wb')
    rbm.exporter_rfnobjects(fh)
    
    rbm.builduniquernfdict()
    fh = open("rnf-objects.csv", 'wb')
    rbm.exporter_rnfobjects(fh)

    rbm.builduniquergndict()
    fh = open("rgn-objects.csv", 'wb')
    rbm.exporter_rgnobjects(fh)
    
    fh = open("fun-objects.csv", 'wb')
    rbm.exporter_funobjects(fh)
    
    fh = open("fun-rfi-relationships.csv", 'wb')
    rbm.exporter_funrfilinks(fh)
    
    fh = open("rfi-fun-relationships.csv", 'wb')
    rbm.exporter_rfifunlinks(fh)

if __name__ == "__main__":
    sys.exit(main(sys.argv))