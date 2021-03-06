# CS484 Project: Mining StackExchange
#### Michel Rouly & Joshua Wells

Data dump URL: https://archive.org/details/stackexchange

## Environment Setup

Setup your Amazon AWS credentials for `boto` (see https://code.google.com/p/boto/wiki/BotoConfig)

    export AWS_ACCESS_KEY_ID=...
    export AWS_SECRET_ACCESS_KEY=...

Clone down this repository

    git clone git@git.gmu.edu:jrouly/cs484project
    cd cs484project

Add a link to your data directory

    ln -s /path/to/data/dir data

Install Python and `pip` (Python package manager)

    sudo apt-get install python python-pip

Install `virtualenv` (Virtual environment manager)

    sudo pip install virtualenv

Create and enable a virtual environment named `venv`

    virtualenv venv
    source venv/bin/activate

Install dependencies

    pip install -r requirements.txt

## Running Clustering

Navigate to the code directory

    cd code

Initialize the appropriate configuration files

    cp config/cluster.ini.sample config/cluster.ini
    cp config/classifier.ini.sample config/classifier.ini
    cp config/input.ini.sample config/input.ini

Run the clustering script

    python cluster.py config/input.ini config/cluster.ini [algorithm]


Run the classifier script

    python classifier.py config/input.ini config/classifier.ini [algorithm]
