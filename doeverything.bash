#!/bin/bash
pushd oec_external
git pull
popd
python linkplanets.py
python genhtml.py
