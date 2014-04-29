#!/bin/bash

cd $HOME

sudo apt-get install python-pip
sudo pip install virtualenv
sudo apt-get install git

sudo apt-get install python-dev libxml2-dev libxslt1-dev

git clone http://git.gmu.edu/jrouly/cs484project.git

cd cs484project

virtualenv-2.7 venv
source venv/bin/activate

pip install -r requirements.txt
