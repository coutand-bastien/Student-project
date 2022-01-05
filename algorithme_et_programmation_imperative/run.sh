#!/bin/bash

echo -e "\n********************************* Start Test *********************************\n"

cd test/
python3 -m unittest discover

echo -e "********************************* End Test *********************************\n"

echo -e "\n********************************* Start virtual env *********************************\n"

cd ../
venv/bin/activate
python3 -m venv venv
venv/bin/pip install -r requirements.txt

venv/bin/python3 ./src/main.py

rm -rf __pycache__
rm -rf venv