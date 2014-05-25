#!/usr/bin/python
import cgi, os
import subprocess
print "Content-type: text/html"
print ""
data = cgi.FieldStorage()
filepath = data["filename"].value

os.chdir("../oec_external/") # to date git context
print "<div style='background-color:white;overflow:auto;'>"
print "<pre style=''>"
for line in open(filepath).readlines():
    print cgi.escape(line),
print "</pre>"
print "</div>"
