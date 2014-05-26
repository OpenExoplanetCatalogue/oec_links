#!/usr/bin/python
import cgi, os
import subprocess
print "Content-type: text/html"
print ""
data = cgi.FieldStorage()
filepath = data["filename"].value

os.chdir("../oec_external/") # to date git context
gitlog = subprocess.Popen(["git", "log", "-1", "-p", "--format=%ad", "--date=short","--numstat",filepath], stdout=subprocess.PIPE).communicate()[0]
gitlines = [cgi.escape(x) for x in  gitlog.split("\n") ]
print "<div style='background-color:white;overflow:auto;'>"
print "<pre style=''>"
for line in gitlines[10:]:
    if len(line)>1:
        if line[0]=="+":
            print "<span style='color:green;'>",
        elif line[0]=="-":
            print "<span style='color:red;'>",

        print line,
        if line[0]=="+" or line[0]=="-":
            print "</span>"
        else:
            print 
    else:
        print line
print "</pre>"
print "</div>"
