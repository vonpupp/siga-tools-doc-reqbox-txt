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

    def setUp(self):
        self.rb = rb
        #self.seq = range(10)

    #def uckeymeasure(self, key):
    #    #result = self.rb.model.fp.fundict[key][1:] #and key
    #    result = key #and key
    #    return result
    
    def tag_check(self, filename, d, tagstr):
        fh = codecs.open(filename, encoding='utf-8', mode='w') # open(filename, 'r')
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        
        itemscount = len(d)
        maxid = max(d)
        if maxid.startswith(tagstr):
            maxid = maxid[len(tagstr):]
        #item = max(d, key=self.uckeymeasure)
        #maxid = max(self.uckeymeasure(k) for k in d.keys())
        csvhdlr.writerow(["ID", "Type", "Status"])
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
                if self.rb.stricttests:
                    raise
            row = [reqid, reqtype, status]
            csvhdlr.writerow(row)

    def test_parser_missing_01_uc_objects(self):
        filename = sys._getframe().f_code.co_name + '.csv'
        d = self.rb.model.fp.fundict
        tagstr = 'UC'
        self.tag_check(filename, d, tagstr)

    def test_parser_missing_02_rfi_objects(self):
        filename = sys._getframe().f_code.co_name + '.csv'
        d = self.rb.model.uniquerfi
        tagstr = 'RFI'
        self.tag_check(filename, d, tagstr)
    
    def test_parser_missing_02_rfn_objects(self):
        filename = sys._getframe().f_code.co_name + '.csv'
        d = self.rb.model.uniquerfn
        tagstr = 'RFN'
        self.tag_check(filename, d, tagstr)
        
    def test_parser_missing_02_rgn_objects(self):
        filename = sys._getframe().f_code.co_name + '.csv'
        d = self.rb.model.uniquergn
        tagstr = 'RGN'
        self.tag_check(filename, d, tagstr)
        
    def test_parser_missing_02_rnf_objects(self):
        filename = sys._getframe().f_code.co_name + '.csv'
        d = self.rb.model.uniquernf
        tagstr = 'RNF'
        self.tag_check(filename, d, tagstr)
        
class TestOrphanObjects(unittest.TestCase):
    """ 
    Attributes:
        - rb: ReqBox
    """
    rb = None
    revrfi = {}
    revrfn = {}
    revrgn = {}
    revrnf = {}

    def setUp(self):
        self.rb = rb
        #self.seq = range(10)
        
    def reverse_dict(self, get_req_callback, set_req_callback, d):
        fundict = self.rb.model.fp.fundict
        for fid, funstr in enumerate(sorted(fundict)):
            funmodel = fundict[funstr]
            reqdict = get_req_callback(funmodel)
            for rid, reqstr in enumerate(sorted(reqdict)):
                reqmodel = reqdict[reqstr]
                set_req_callback(funmodel, reqmodel, d)
                #req = reqdict[reqstr]
                #reqid = reqstr.decode('utf-8')
                #reqname = ''
                #if req.reqname is not None:
                #    reqname = req.reqname.encode('utf-8')
                #reqbody = ''
                #if req.reqbody is not None:
                #    reqbody = req.reqbody.encode('utf-8')
        pass
    
    def get_rfi_dict(self, funmodel):
        return funmodel.rfi
   
    def get_rfn_dict(self, funmodel):
        return funmodel.rfn
    
    def get_rgn_dict(self, funmodel):
        return funmodel.rgn
    
    def get_rnf_dict(self, funmodel):
        return funmodel.rnf
    
    def set_rev_dict(self, fun, req, d):
        #d = self.revrfn
        if not req.reqid in d:
            d[req.reqid] = [fun]
        else:
            l = d[req.reqid]
            l += [fun]
        
    def orphan_check(self, filename, d, tagstr):
        fh = codecs.open(filename, encoding='utf-8', mode='w') # open(filename, 'r')
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        
        itemscount = len(d)
        maxid = max(d)
        if maxid.startswith(tagstr):
            maxid = maxid[len(tagstr):]
            
        csvhdlr.writerow(["ID", "Type", "Status"])
        for number in range(1, int(maxid) + 1):
            item = tagstr + '%03d' % number
            reqid = item
            reqname = ''
            reqtype = tagstr
            reqbody = ''
            try:
                self.assertIn(item, d)
                l = d[item]
                self.assertNotEqual(l, [])
                status = 'ok'
            except:
                status = 'FAILED'
                if self.rb.stricttests:
                    raise
            row = [reqid, reqtype, status]
            csvhdlr.writerow(row)

    def test_parser_orphan_01_rfi_objects(self):
        filename = sys._getframe().f_code.co_name + '.csv'
        d = self.revrfi
        tagstr = 'RFI'
        self.reverse_dict(self.get_rfi_dict, self.set_rev_dict, d)
        self.orphan_check(filename, d, tagstr)
        
    def test_parser_orphan_02_rfn_objects(self):
        filename = sys._getframe().f_code.co_name + '.csv'
        d = self.revrfn
        tagstr = 'RFN'
        self.reverse_dict(self.get_rfn_dict, self.set_rev_dict, d)
        self.orphan_check(filename, d, tagstr)
        
    def test_parser_orphan_03_rgn_objects(self):
        filename = sys._getframe().f_code.co_name + '.csv'
        d = self.revrgn
        tagstr = 'RGN'
        self.reverse_dict(self.get_rgn_dict, self.set_rev_dict, d)
        self.orphan_check(filename, d, tagstr)
        
    def test_parser_orphan_04_rnf_objects(self):
        filename = sys._getframe().f_code.co_name + '.csv'
        d = self.revrnf
        tagstr = 'RNF'
        self.reverse_dict(self.get_rnf_dict, self.set_rev_dict, d)
        self.orphan_check(filename, d, tagstr)

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
    suite.addTest(unittest.makeSuite(TestOrphanObjects))
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