#!/usr/bin/python
# -*- coding: utf-8 -*-

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