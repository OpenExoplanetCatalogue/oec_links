#!/usr/bin/python
import xml.etree.ElementTree as ET
import xmltools
import time
import subprocess 
import os

hashes = None
updatedsystemids = []

def store_hash(filepath, catalogue, filehash):
    global hashes
    global systemid
    """ Generates and stores the has value for the file and catalogue"""

    filename = filepath[filepath.rfind("/")+1:]
    planetname = ET.parse(filepath).findtext(".//planet/name")
    
    if planetname not in systemid:
        print "Skipping " + filename
        return

    updatedsystemids.append(systemid[planetname])
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
    if planet_catalogue_hash.text != filehash:
        # hash is new, update it and change date 
        planet_catalogue_hash.text = filehash
        planet_catalogue_date = planet_catalogue.find(".//date")
        planet_catalogue_date.text = time.strftime("%y/%m/%d")

catalogues = ["open_exoplanet_catalogue", "exoplaneteu", "exoplanetarchive"]

if __name__ == "__main__":
    hashfilename = "hashes/systemhashes.xml"
    if not os.path.isfile(hashfilename):
        hashes = ET.Element("hashes")
    else:
        hashes = ET.parse(hashfilename).getroot()

    systemid = {}
    f = open("systemid.txt")
    for line in f:
        s = [x.strip() for x in line.split(":::")]
        systemid[s[0]] = s[1]

    os.chdir("oec_external/")
    for cat in catalogues:
        filesincat = subprocess.Popen(["git", "ls-files", "-s", "systems_"+cat], stdout=subprocess.PIPE).communicate()[0].strip().split("\n")
        for f in filesincat:
            f = f.split("\t")
            filename = f[1]
            filehash = f[0].split(" ")[1]
            store_hash(filename, cat, filehash)
    os.chdir("../")

    oldsystems = []

    systems = hashes.findall("./system")
    for system in systems:
        if system.findtext("./id") not in updatedsystemids:
            oldsystems.append(system)
            print "Found old system with id='" + system.findtext("./id")+"'. Will be removed."

    for oldsystem in oldsystems:
        hashes.remove(oldsystem)

    xmltools.indent(hashes)
    ET.ElementTree(hashes).write("hashes/systemhashes.xml")
