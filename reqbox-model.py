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

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

def site_struct():
    return defaultdict(board_struct)
    
def board_struct():
    return defaultdict(user_struct)
    
def user_struct():
    return dict(pageviews=0,username='',comments=0)
    

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

s = {
  'fun001': 'FUNManter Tipo de Verificacao de Item de Checklist',
  'fun001': {'rfi234' : 'RFIManter Tipo de Verificacao de Item de Checklist', 'rfn001' : 'Permissao de acesso por perfil de seguranca',
             'rfn366' : 'Busca e retorno de dados de tipo de verificao de item de checklist', 'rnf001' : '...', 'rng001' : '...',
             'wrf001' : '...'}
}

def main(argv):
    print s
#    print s['fun001']
    print s['fun001']['rfi234']
    print s['fun001']
    
    myDict = {'Apple': {'American':'16', 'Mexican':10, 'Chinese':5},
              'Grapes':{'Arabian':'25','Indian':'20'} }


    print myDict['Apple']['American']
    
    
    userdict = defaultdict(site_struct)
    userdict['site1']['board1']['username'] = 'tommy'
    #userdict['site1']['board1']['username']['pageviews'] += 1
    print userdict
    print userdict['site1']['board1']['username']



if __name__ == "__main__":
    sys.exit(main(sys.argv))