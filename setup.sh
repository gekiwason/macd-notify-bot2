#!/bin/bash

sudo apt-get update && sudo apt-get upgrade y
sudo apt install -y python3 python3-pip build-essential libssl-dev libffi-dev python3-dev
pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install -r macd-notify-bot2/requirements.txt

wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -zxvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install
pip3 install TA-Lib

cd macd-notify-bot2
touch .env
echo "please input userID: "
read STR1
echo "LINE_NOTIFY_ID = '${STR1}'" 1>>.env
echo "please input token: "
read STR2
echo "LINE_NOTIFY_TOKEN = '${STR2}'" 1>>.env
nohup python3 notify.py &
