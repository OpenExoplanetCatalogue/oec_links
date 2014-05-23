#!/usr/bin/python
import hashlib
import xml.etree.ElementTree as ET
import xmltools
import time
from os import listdir
from os.path import isfile

hashes = None

def store_hash(filepath, catalogue):
    global hashes
    global systemid
    """ Generates and stores the has value for the file and catalogue"""

    filename = filepath[filepath.rfind("/")+1:]
    contents = open(filepath).read()

    # generate hash
    m = hashlib.sha1()
    m.update(contents)
    fphash = m.hexdigest()
    
    planetname = ET.fromstring(contents).findtext(".//planet/name")
    
    if planetname not in systemid:
        print "Skipping " + filename
        return


    system = hashes.find("./system[id='"+systemid[planetname]+"']")
    if system is None:
        # add the new hash for the file
        system = ET.Element("system")
        ET.SubElement(system,"id").text = systemid[planetname]
        hashes.append(system)

    # update the hash
    planet_catalogue = system.find("./catalogue[name='"+catalogue+"']")
    if planet_catalogue is None:
        # create new catalogue tag
        planet_catalogue = ET.Element("catalogue")
        catalogue_name = ET.Element("name")
        catalogue_name.text = catalogue
        planet_catalogue.append(catalogue_name)
        planet_hash = ET.Element("hash")
        planet_catalogue.append(planet_hash)
        planet_date = ET.Element("date")
        planet_catalogue.append(planet_date)
        planet_filename = ET.Element("filename")
        planet_filename.text = filename
        planet_catalogue.append(planet_filename)
        system.append(planet_catalogue)

    planet_catalogue_hash = planet_catalogue.find("./hash")
    if planet_catalogue_hash.text != fphash:
        # hash is new, update it and change date 
        planet_catalogue_hash.text = fphash
        planet_catalogue_date = planet_catalogue.find(".//date")
        planet_catalogue_date.text = time.strftime("%d/%m/%y")

def openexohash():
    for f in listdir("open_exoplanet_catalogue/systems"):
        store_hash("open_exoplanet_catalogue/systems/"+f, "open_exoplanet_catalogue")

def euhash():
    for f in listdir("systems_exoplaneteu"):
        store_hash("systems_exoplaneteu/"+f, "exoplaneteu")

def archivehash():
    for f in listdir("systems_exoplanetarchive"):
        store_hash("systems_exoplanetarchive/"+f, "exoplanetarchive")

if __name__ == "__main__":
    hashfilename = "hashes/systemhashes.xml"
    if not isfile(hashfilename):
        hashes = ET.Element("hashes")
    else:
        hashes = ET.parse(hashfilename).getroot()

    systemid = {}
    f = open("systemid.txt")
    for line in f:
        s = [x.strip() for x in line.split(":::")]
        systemid[s[0]] = s[1]

    openexohash()
    euhash()
    archivehash()

    xmltools.indent(hashes)
    ET.ElementTree(hashes).write("hashes/systemhashes.xml")
