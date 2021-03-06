#!/usr/bin/env bash

# Create virtualenv
python3 -m venv venv
source ./venv/bin/activate

cd fet_server

# install dependencies
pip install -r requirements/develop.txt

# init:
# Prepare API_KEY for fixer.io
echo "FIXER_API_KEY = 'API_KEY'" > project/settings_local.py
./manage.py migrate

echo """
run:
 source ./venv/bin/activate
 cd fet_server
 ./manage.py runserver
"""
