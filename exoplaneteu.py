#!/usr/bin/python 
import urllib
import os
import xml.etree.ElementTree as ET 
import xmltools
#####################
# Exoplanet.eu
#####################
url_exoplaneteu = "http://exoplanet.eu/catalog/csv/"

def get():
    xmltools.ensure_empty_dir("exoplaneteu")
    urllib.urlretrieve (url_exoplaneteu, "exoplaneteu/exoplanet.eu_catalog.csv")

def parse():
    # delete old data
    xmltools.ensure_empty_dir("systems_exoplaneteu")

    # parse data into default xml format
    f = open("exoplaneteu/exoplanet.eu_catalog.csv")
    header = [x.strip() for x in f.readline()[1:].split(",")]
    for line in f:
        p = dict(zip(header, [x.strip() for x in line.split(",")]))
        outputfilename = "systems_exoplaneteu/"+p["star_name"]+".xml"
        if os.path.exists(outputfilename):
            system = ET.parse(outputfilename).getroot()
            star = system.find(".//star")
        else:
            system = ET.Element("system")

            # TODO: Check that system already exists. If so, add planets.
            ET.SubElement(system, "name").text = p["star_name"]
            # TODO: Convert ra and dec to hh mm ss format.
            ET.SubElement(system, "rightascension").text = p["ra"]
            ET.SubElement(system, "declination").text = p["dec"]
            ET.SubElement(system, "distance").text = p["star_distance"]

            star = ET.SubElement(system,"star")
            ET.SubElement(star, "name").text = p["star_name"]
            ET.SubElement(star, "age").text = p["star_age"]
            ET.SubElement(star, "radius").text = p["star_radius"]
            ET.SubElement(star, "mass").text = p["star_mass"]
            ET.SubElement(star, "spectraltype").text = p["star_sp_type"]
            ET.SubElement(star, "temperature").text = p["star_teff"]
            ET.SubElement(star, "metallicity").text = p["star_metallicity"]


        # TODO: Add planet.
        planet = ET.SubElement(star,"planet")
        ET.SubElement(planet, "name").text = p["name"]

        # Cleanup and write file
        xmltools.removeemptytags(system)
        xmltools.indent(system)
        ET.ElementTree(system).write(outputfilename) 


if __name__=="__main__":
    get()
    parse()
