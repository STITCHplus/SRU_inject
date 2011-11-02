#!/usr/bin/env python

##
## SRU_inject.py - SRU_inject
##
## copyright (c) 2011-2012 Koninklijke Bibliotheek - National library of the Netherlands.
##
## this program is free software: you can redistribute it and/or modify
## it under the terms of the gnu general public license as published by
## the free software foundation, either version 3 of the license, or
## (at your option) any later version.
##
## this program is distributed in the hope that it will be useful,
## but without any warranty; without even the implied warranty of
## merchantability or fitness for a particular purpose. see the
## gnu general public license for more details.
##
## you should have received a copy of the gnu general public license
## along with this program. if not, see <http://www.gnu.org/licenses/>.
##

import cgi
import ast
import urllib, simplejson
from pprint import pprint
from pymongo import Connection

__author__ = "Willem Jan Faber"

form = cgi.FieldStorage()

q = form.getvalue("q")

conn = Connection("192.87.165.3")

print "Content-Type: text; charset=utf-8\n\n"

data = False
found = False

if q:
    db_name = False

    if q.find('=') > -1:  # Works only with these two collections..
        t=q.split('=')[1]
        if t.lower().find('anp') > -1:
            db_name = "ANP"
        else:
            db_name = "DPO"

    if db_name: 
        data = ""
        db = conn["expand_test"][db_name]  # Connect to mongoDB and get the requested record..
        record=db.find({"id" : q})
        if record:
            for item in record:
                if "prefLabel" in item.keys():
                    data+=('<dc:subject xsi:type="dcx:Brinkman" xml:lang="nl" dcx:recordIdentifier="'+":".join(item["sameAs"].split(':')[1:])+'">'+item["prefLabel"]+'</dc:subject>') #Inject the identifiers into the SRU response.
                else:
                    label = simplejson.loads(urllib.urlopen('http://data.kbresearch.nl/'+item["sameAs"]+"?prefLabel").read())
                    label = label["preflabel"].encode('utf-8')
                    data+=('<dc:subject xsi:type="dcx:Brinkman" xml:lang="nl" dcx:recordIdentifier="'+":".join(item["sameAs"].split(':')[1:])+'">'+label+'</dc:subject>')

        db = conn["expand_test"][db_name+"_user"]
        record=db.find({"id" : q})
        if record:
            for item in record:
                data+=('<dc:subject xsi:type="dcx:Brinkman" xml:lang="nl" dcx:recordIdentifier="'+":".join(item["sameAs"].split(':')[1:])+'">'+item["prefLabel"]+'</dc:subject>')


if data:
    print(data.encode("utf-8", "xmlcharrefreplace"))
