#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Project:			SIGA
#   Component Name:		reqbox
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
#   Description:		This script will create EA importable files
#                               from .txt (.doc) and .csv (.xls) requirements files
#
#   Limitations:		Error handling is correctly implemented, time constraints
#	The code is not clean and elegant as it should, again, time constraints
#   Database tables used:	None 
#   Thread Safe:	        No
#   Extendable:			No
#   Platform Dependencies:	Linux (openSUSE used)
#   Compiler Options:

import unittest
import random
import sys
import inspect
import codecs
import csv

class ReqBoxTest():
    """ Reqbox
    Attributes:
    """
    
    def __init__(self):
        # Public
        # Init structures
        rb = None
        pass
        
    def initobject(self, rb):#, ParserClass):
        self.rb = rb
        
    def test01(self):
        """ Test01: UC number missing
        Type: offline
        Attributes:
        """
        itemsnumber = rb.model
        
#- rodar a matriz de relacionamento;
#- verificar se tem RFN sem utilização;
#- verificar se tem RFI sem utilização;
#- verificar se aparece o mesmo RFI mais de uma vez no documento de funcionalidades;
#- verificar se aparece o mesmo UC mais de uma vez no documento de funcionalidades;
#- verificar se há o mesmo número de RFN com nome diferente no documento de funcionalidades;
#- verificar se há o mesmo número de RFI com nome diferente no documento de funcionalidades;
#- verificar se há o mesmo número de UC com nome diferente no documento de funcionalidades;
#- verificar se há funcionalidade sem um código UC; (este item só pode ser feito quando eu terminar a conversão dos casos de uso)
#- Verificar se há caso de uso que não é extendido nem implementado por ninguém;

rb = None

class TestMissingObjects(unittest.TestCase):
    """ 
    Attributes:
        - rb: ReqBox
    """
    rb = None
    filename = 'test-missing-objects.test'
    fh = codecs.open(filename, encoding='utf-8', mode='w') # open(filename, 'r')
    csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)

    def setUp(self):
        self.rb = rb
        #self.seq = range(10)

    def uckeymeasure(self, key):
        #result = self.rb.model.fp.fundict[key][1:] #and key
        #result = key[2:] #and key
        result = key #and key
        return result
    
    def tagcheck(self, d, tagstr):
        itemscount = len(d)
        maxid = max(d)
        if maxid.startswith(tagstr):
            maxid = maxid[len(tagstr):]
        #item = max(d, key=self.uckeymeasure)
        #maxid = max(self.uckeymeasure(k) for k in d.keys())
        self.csvhdlr.writerow(["ID", "Type", "Status"])
        for number in range(1, int(maxid) + 1):
            item = tagstr + '%03d' % number
            reqid = item
            reqname = ''
            reqtype = tagstr
            reqbody = ''
            try:
                self.assertIn(item, d)
                status = 'ok'
            except:
                status = 'FAILED'
            row = [reqid, reqtype, status]
            self.csvhdlr.writerow(row)

    def test_missing_uc_objects(self):
        # make sure the shuffled sequence does not lose any elements
        #itemcount = self.rb.model.
        d = self.rb.model.fp.fundict
        tagstr = 'UC'
        self.tagcheck(d, tagstr)
        
    def test_missing_rfi_objects(self):
        # make sure the shuffled sequence does not lose any elements
        #itemcount = self.rb.model.
        d = self.rb.model.uniquerfi
        tagstr = 'RFI'
        self.tagcheck(d, tagstr)
        
        #itemscount = len(d)
        #maxid = max(d)
        #if maxid.startswith(formatstr):
        #    maxid = maxid[len(formatstr):]
        ##item = max(d, key=self.uckeymeasure)
        ##maxid = max(self.uckeymeasure(k) for k in d.keys())
        #self.csvhdlr.writerow(["ID", "Type", "Status"])
        #for number in range(1, int(maxid) + 1):
        #    item = formatstr + '%03d' % number
        #    reqid = item
        #    reqname = ''
        #    reqtype = formatstr
        #    reqbody = ''
        #    try:
        #        self.assertIn(item, d)
        #        status = 'ok'
        #    except:
        #        status = 'FAILED'
        #    row = [reqid, reqtype, status]
        #    self.csvhdlr.writerow(row)
        #self.assertEqual(3, 5)

        # should raise an exception for an immutable sequence
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))

    #def test_shuffle(self):
    #    # make sure the shuffled sequence does not lose any elements
    #    random.shuffle(self.seq)
    #    self.seq.sort()
    #    self.assertEqual(self.seq, range(10))
    #
    #    # should raise an exception for an immutable sequence
    #    self.assertRaises(TypeError, random.shuffle, (1,2,3))
    #
    #def test_choice(self):
    #    element = random.choice(self.seq)
    #    self.assertTrue(element in self.seq)
    #
    #def test_sample(self):
    #    with self.assertRaises(ValueError):
    #        random.sample(self.seq, 20)
    #    for element in random.sample(self.seq, 5):
    #        self.assertTrue(element in self.seq)
    
class TestEAIntegrity(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

def parsingsuite():
    #args = sys.argv[1:]
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMissingObjects))
    return suite

def EAsuite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestEAIntegrity))
    return suite

if __name__ == '__main__':
#    unittest.main(verbosity=2)
    
    
    suiteFew = unittest.TestSuite()
    #suiteFew.addTest(TestMissingObjects("test_01_UC_missing"))
    #suiteFew.addTest(TestMissingObjects("test_shuffle"))
    #unittest.TextTestRunner(verbosity=2).run(suiteFew)
    unittest.TextTestRunner(verbosity=2).run(parsingsuite())
    
#suite1 = unittest.TestSuite(MyTestCase1(), MyTestCase2())
#suite2 = unittest.TestSuite()
#suite2.addTest(MyOtherTestCase())
#
#big_suite = unittest.TestSuite(suite1)
#big_suite.addTest(suite2)