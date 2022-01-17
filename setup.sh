#!/bin/bash

sudo apt update
sudo apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
sudo apt upgrade
sudo apt install -y python3 python3-pip build-essential libssl-dev libffi-dev python3-dev
sudo apt-get install -y vim less
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt

wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install
pip install TA-Lib
rm -R ta-lib ta-lib-0.4.0-src.tar.gz
