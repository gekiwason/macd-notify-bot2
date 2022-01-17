#!/bin/bash

sudo apt-get update && sudo apt-get upgrade y
sudo apt install -y python3 python3-pip build-essential libssl-dev libffi-dev python3-dev
pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install -r requirements.txt

wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -zxvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install
pip3 install TA-Lib
