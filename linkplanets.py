#!/usr/bin/python
import urllib
import os, glob
import xml.etree.ElementTree as ET 

aliases = {}

for filename in glob.glob("open_exoplanet_catalogue/systems/*.xml"):
    # Parse file
    root = ET.parse(filename).getroot()
    # Construct a parent map
    # parent = {c:p for p in root.iter() for c in p}
    
    # Do loop on a per planet basis (the other catalogues don't understand binaries)
    for planet in root.findall(".//planet"):
        planetid = planet.findtext("name") # first element is id
        for name in planet.findall("name"):
            aliases[name.text] =planetid
            aliases[name.text.lower()] =planetid
            aliases[name.text.replace(" ","")] =planetid
            aliases[name.text.lower().replace(" ","")] =planetid

catalogues = ["exoplaneteu", "exoplanetarchive"]
for catalogue in catalogues:
    for filename in glob.glob("systems_exoplanetarchive/*.xml"):
        # Parse file
        root = ET.parse(filename).getroot()

        for planet in root.findall(".//planet"):
            planetid = planet.findtext("name") # first element is id
            key = None

            # Try various ways to find a similar name in our planet list
            if planetid in aliases:
                key = planetid
            elif planetid.lower() in aliases:
                key = planetid.lower()
            elif planetid.replace(" ","") in aliases:
                key = planetid.replace(" ","")
            elif planetid.lower().replace(" ","") in aliases:
                key = planetid.lower().replace(" ","")
            else:
                print "No link to OEC found: \"\033[1m"+planetid+"\033[0m\"  (" + catalogue +")"

                


