#!/usr/bin/python
# -*- coding: UTF-8 -*-
input=raw_input('> ').strip()
utf=[]
for i in input:
        utf.append("\\u00"+hex(ord(i)).split('x')[1])
print ''.join([i for i in utf])
