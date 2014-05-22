import hashlib
import xml.etree.ElementTree as ET
import xmltools
import time
from os import listdir
from os.path import isfile

def store_hash(filepath, catalogue):
    """ Generates and stores the has value for the file and catalogue"""


    # generate hash
    m = hashlib.sha1()
    m.update(open(filepath).read())
    
    # get hash tree
    tree = ET.parse("hashes/systemhashes.xml")
    hashes = tree.getroot()

    filename = filepath[filepath.rfind("/")+1:]
    system = hashes.find(".//system[filename='"+filename+"']")
    if system is None:
        # add the new hash for the file
        system = ET.Element("system")
        system_filename = ET.Element("filename")
        system_filename.text = filename
        system.append(system_filename)
        hashes.append(system)

    # update the hash
    planet_catalogue = system.find(".//catalogue[name='"+catalogue+"']")
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
        system.append(planet_catalogue)

    planet_catalogue_hash = planet_catalogue.find("./hash")
    if planet_catalogue_hash.text != m.hexdigest():
        # hash is new, update it and change date 
        planet_catalogue_hash.text = m.hexdigest()
        planet_catalogue_date = planet_catalogue.find(".//date")
        planet_catalogue_date.text = time.strftime("%d/%m/%y")
        xmltools.indent(system)
        tree.write("hashes/systemhashes.xml")
        print "stored hash for: " + filename

def openexohash():
    for f in listdir("open_exoplanet_catalogue/systems"):
        store_hash("open_exoplanet_catalogue/systems/"+f, "open exoplanet catalogue")

def euhash():
    for f in listdir("systems_exoplaneteu"):
        store_hash("systems_exoplaneteu/"+f, "exoplaneteu")

def archivehash():
    for f in listdir("systems_exoplanetarchive"):
        store_hash("systems_exoplanetarchive/"+f, "exoplanet archive")

if __name__ == "__main__":
    openexohash()
    euhash()
    archivehash()


