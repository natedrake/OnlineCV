#!/usr/bin/env bash

cd /home/ubuntu/OnlineCV
waitress-serve --listen=0.0.0.0:80 --threads=8 --call 'autoapp:create_app'
