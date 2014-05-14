#!/bin/python 
import urllib
import os
import xml.etree.ElementTree as ET 
import xmltools

#####################
# Exoplanet Archive
#####################
url_exoplanetarchive = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=pl_hostname,ra,dec&order=dec&format=csv"

def get():
    xmltools.ensure_empty_dir("exoplanetarchive")
    urllib.urlretrieve (url_exoplanetarchive, "exoplanetarchive/exoplanetarchive.csv")

def parse():
    # delete old data
    xmltools.ensure_empty_dir("systems_exoplanetarchive")

    # parse data into default xml format
    f = open("exoplanetarchive/exoplanetarchive.csv")
    header = [x.strip() for x in f.readline().split(",")]
    for line in f:
        p = dict(zip(header, [x.strip() for x in line.split(",")]))
        
        # TODO: Check that system already exists. If so, add planets.
        system = ET.Element("system")
        ET.SubElement(system, "name").text = p["pl_hostname"]
        # TODO: Convert ra and dec to hh mm ss format.
        ET.SubElement(system, "rightascension").text = p["ra"]
        ET.SubElement(system, "declination").text = p["dec"]

        star = ET.SubElement(system,"star")
        ET.SubElement(star, "name").text = p["pl_hostname"]
        # TODO: Add remaining stellar parameters

        # TODO: Add planet.

        # Cleanup and write file
        xmltools.removeemptytags(system)
        xmltools.indent(system)
        outputfilename = "systems_exoplanetarchive/"+p["pl_hostname"]+".xml"
        ET.ElementTree(system).write(outputfilename) 



