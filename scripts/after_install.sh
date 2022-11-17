#!/usr/bin/env bash

cd /home/ubuntu/OnlineCV || exit

python3 -m pip install -r requirements.txt

# set up flask ENV variables
export FLASK_APP=autoapp.py
export FLASK_DEBUG=0
