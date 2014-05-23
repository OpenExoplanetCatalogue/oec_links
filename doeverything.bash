#!/bin/bash
pushd open_exoplanet_catalogue
git pull
popd
python get_external.py
python linkplanets.py
python genhash.py 
python genhtml.py
