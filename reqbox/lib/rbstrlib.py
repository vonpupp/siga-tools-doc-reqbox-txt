#!/usr/bin/python
# -*- coding: utf-8 -*-

import difflib

def fixmschr(s):
    s = s.replace('\r\n\n\r\n','\r\n\r\n')
    s = s.replace('\r\no ','\r\n  - ')
    s = s.replace(u'\x96', u'-')
    s = s.replace(u'–', u'-')
    s = s.replace(u'\xe2\x80\x93', u'-')
    s = s.replace(u'“', u'"')
    s = s.replace(u'”', u'"')
    s = s.replace(u'•', u'-')
    return s

def mystrfuzzycmp(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).ratio()