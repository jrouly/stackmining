#!/bin/bash

cd $HOME

# System setup
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python-dev libxml2-dev libxslt1-dev gfortran
sudo apt-get install git python-pip vim
sudo pip install virtualenv

# Get code
git clone http://git.gmu.edu/jrouly/cs484project.git

cd cs484project

virtualenv-2.7 venv
source venv/bin/activate

sudo apt-get build-dep python-scipy

pip install -r requirements.txt

# ec2 creds
source $HOME/.ec2/config
