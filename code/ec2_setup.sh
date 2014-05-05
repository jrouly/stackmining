#!/bin/bash

cd $HOME

# System setup
sudo apt-get -y update
sudo apt-get -y upgrade

sudo apt-get -y install python-dev libxml2-dev libxslt1-dev gfortran lib32z1-dev
sudo apt-get -y install git python-pip vim
sudo pip install virtualenv

# Get code
git clone http://git.gmu.edu/jrouly/cs484project.git

cd cs484project

virtualenv-2.7 venv
source venv/bin/activate

sudo apt-get -y build-dep python-scipy

pip install -r requirements.txt

# ec2 creds
#cd $HOME
#wget https://michel.rouly.net/public/cs484/ec2.tar.gz
#tar xzvf ec2.tar.gz
#mv ec2 .ec2
#source $HOME/.ec2/config
