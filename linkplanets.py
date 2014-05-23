#!/usr/bin/python
import urllib
import os, glob
import xml.etree.ElementTree as ET 
import xmltools

aliases = {}
uniquelist = {}
systemid = {}

for filename in glob.glob("open_exoplanet_catalogue/systems/*.xml"):
    # Parse file
    root = ET.parse(filename).getroot()
    # Construct a parent map
    # parent = {c:p for p in root.iter() for c in p}
    
    # Do loop on a per planet basis (the other catalogues don't understand binaries)
    for planet in root.findall(".//planet"):
        planetid = planet.findtext("name") # first element is id
        if root.findtext(".//name") !="Sun":  # ignore solar system
            uniquelist[planetid] = 0
            systemid[planetid] = os.path.basename("".join(filename.split(".")[:-1]))
        for name in planet.findall("name"):
            aliases[name.text] =planetid
            aliases[name.text.lower()] =planetid
            aliases[name.text.replace(" ","")] =planetid
            aliases[name.text.lower().replace(" ","")] =planetid
            aliases[name.text.lower().replace(" ","").replace("-","")] =planetid

name_except = xmltools.get_exceptions()

#catalogues = ["exoplaneteu"]
catalogues = ["exoplaneteu", "exoplanetarchive"]
for catalogue in catalogues:
    uniquelist_cat = uniquelist
    exception_count = 0
    missingplanet_count = 0
    for filename in glob.glob("systems_"+catalogue+"/*.xml"):
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
            elif planetid.lower().replace(" ","").replace("-","") in aliases:
                key = planetid.lower().replace(" ","").replace("-","")
            elif name_except.has_key(planetid):
                key = name_except[planetid]
                print "Using exception for:\033[93m", planetid,"->", name_except[planetid],"\033[0m"
                exception_count += 1
            if key is not None:
                # planet identified
                uniquelist_cat[aliases[key]] = 1
                systemid[planetid] = systemid[aliases[key]]
            else:
                # planet not identified
                missingplanet_count += 1
                systemid[planetid] =  planetid


    notaccountedfor = []
    exceptionslist=[]
    for key in uniquelist_cat:
        if uniquelist_cat[key]==0:
            notaccountedfor.append(key)
                
    print "OEC contains \033[1m%d\033[0m planets which are not in %s." %(len(notaccountedfor),catalogue)
    print "OEC misses   \033[91m%d\033[0m planets which are in %s." %(missingplanet_count,catalogue)
    print "OEC contains \033[93m%d\033[0m planets which require exceptions when compared to %s." %(exception_count,catalogue)

with open('systemid.txt', 'wb') as af:
    for key in systemid:
        af.write(key+":::"+systemid[key]+"\n")

af.close()
