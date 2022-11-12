#!/usr/bin/env bash

# get ssh keys for github account
aws s3 cp s3://onlinecv-codepipeline/ssh-keys/id_ed25519 ~/.ssh/.
chmod 600 ~/.ssh/id_ed25519
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# create directory for web app
mkdir /home/ubuntu/OnlineCV

# set up flask ENV variables
export FLASK_APP=autoapp.py
export FLASK_DEBUG=0
export FLASK_SECRET=43aba0906f530b74291ba22bb7eb034d728322f58ac68ad00e645314618eb3d9
