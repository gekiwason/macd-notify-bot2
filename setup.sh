#!/bin/bash

sudo apt update
sudo apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
sudo apt upgrade
sudo apt install -y python3 python3-pip
sudo apt-get install -y vim less
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt
