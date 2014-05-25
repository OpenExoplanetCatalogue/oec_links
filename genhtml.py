#!/usr/bin/python
import hashlib
import xml.etree.ElementTree as ET
import xmltools
import time
import os
import subprocess
import cgi

catalogues = ["open_exoplanet_catalogue", "exoplaneteu", "exoplanetarchive"]
basedate = "2014/05/23"

# setup html
html = ET.Element("html")
head = ET.SubElement(html,"head")
link = ET.SubElement(head,"link")
link.attrib["rel"] ="stylesheet"
link.attrib["type"]="text/css"
link.attrib["href"]="style.css"
script = ET.SubElement(head,"script")
script.attrib["src"]="jquery-2.1.1.min.js"
script.text=" "
script = ET.SubElement(head,"script")
script.attrib["src"]="jquery.tinysort.min.js"
script.text=" "
script = ET.SubElement(head,"script")
script.attrib["src"]="jscript.js"
script.text=" "
body = ET.SubElement(html,"body")
table = ET.SubElement(body,"table")
tr = ET.SubElement(table,"tr")
ET.SubElement(tr,"th").text = "systemid"
for cat in catalogues:
    ET.SubElement(tr,"th").text = cat




systemids = {}
f = open("systemids.txt")
for line in f:
    s = [x.strip() for x in line.split(":::")]
    systemids[s[0]] = s[1]

os.chdir("oec_external/") # to date git context
for cat in catalogues:
    filesincat = subprocess.Popen(["git", "ls-files", "-s", "systems_"+cat], stdout=subprocess.PIPE).communicate()[0].strip().split("\n")
    for f in filesincat:
        f = f.split("\t")
        filepath = f[1]
        filename = filepath[filepath.rfind("/")+1:]
        planetname = ET.parse(filepath).findtext(".//planet/name")
        
        try:
            systemid = systemids[planetname]
        except:
            print "Skipping " + filename
            continue

        # get git info
        gitlog = subprocess.Popen(["git", "log", "-1", "-p", "--format=%ad", "--date=short","--numstat",filepath], stdout=subprocess.PIPE).communicate()[0]
        gitlines = gitlog.split("\n")
        gitdate  = gitlines[0].split(" ")[-1].strip().replace("-","/")
        gitstats = "/".join(gitlines[2].split("\t")[0:2])

        # put data in html format
        tr = table.find("./tr[@id='"+systemid+"']")
        if tr is None:
            tr = ET.SubElement(table,"tr")
            tr.attrib["id"] = systemid
            th = ET.SubElement(tr,"th")
            th.text = systemid
            for cat2 in catalogues:
                td = ET.SubElement(tr,"td")
                td.attrib["id"] = cat2

        td = tr.find("./td[@id='"+cat+"']") 
        td.attrib["date"] = gitdate # for coloring and sorting
        dl = ET.SubElement(td,"dl")
        ET.SubElement(dl,"dt").text = "last updated"
        ET.SubElement(dl,"dd").text = gitdate
        ET.SubElement(dl,"dt").text = "filename"
        ET.SubElement(dl,"dd").text = filename
        ET.SubElement(dl,"dt").text = "change +/-"
        ET.SubElement(dl,"dd").text = gitstats
        ET.SubElement(dl,"dt").text = "show diff"
        dd = ET.SubElement(dl,"dd")
        div = ET.SubElement(dd,"div")
        ET.SubElement(dd,"pre").text = "\n".join(gitlines[10:]).decode("utf-8")

    

os.chdir("../")


# decorate
for tr in table.findall("./tr"):
    newestdate = ""
    significance = 3                # system not in oec
    for td in tr.findall("./td[@id]"):
        if "date" not in td.attrib:
            td.attrib["class"] = "missing"
    for td in tr.findall("./td[@date]"):
        date = td.attrib["date"]
        if date > newestdate:
            newestdate  = date
    for td in tr.findall("./td[@date]"):
        date = td.attrib["date"]
        if date == basedate and newestdate == basedate:
            td.attrib["class"] = "basedate"
            if td.attrib["id"] == "open_exoplanet_catalogue":
                significance = 1    # oec and external on basedate
        elif date == newestdate:
            td.attrib["class"] = "newest"
            if td.attrib["id"] == "open_exoplanet_catalogue":
                significance = 0    # oec up-to-date
        else:
            td.attrib["class"] = "notnewest"
            if td.attrib["id"] == "open_exoplanet_catalogue":
                significance = 2    # oec not up-to-date
    tr.attrib["significance"] = "%d" % significance

xmltools.indent(html)
ET.ElementTree(html).write("status.html")
