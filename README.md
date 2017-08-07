# Instructions to build Python environment

## Linux, using Python 2.7, system packages, tested on Ubuntu 16.04 Vagrant box

    sudo apt-get update
    sudo apt-get install python python-nose-parameterized python-numpy python-sklearn python-pip python-bs4 python-pandas
    sudo pip install --upgrade pip
    sudo pip install theanets

or use provided Vagrantfile to setup VM.

## Linux, using Python 2.7, virtualenv

Install system packages

    sudo apt-get install python python-pip python-virtualenv python-tk

Install remaining packages in virtualenv

    virtualenv venv27
    venv27/bin/pip install -r requirements27.txt

## Linux, using Python 3.5, system packages, tested on Ubuntu 16.04 Vagrant box

    sudo apt-get update
    sudo apt-get install python3 python3-nose-parameterized python3-numpy python3-sklearn python3-pip python3-bs4 python3-pandas
    sudo pip3 install --upgrade pip
    sudo pip3 install theanets

or use provided Vagrantfile to setup VM.

## Linux, using Python 3.5, virtualenv

Install system packages

    sudo apt-get install python3 python3-pip python3-virtualenv python3-tk

Install remaining packages in virtualenv

    virtualenv -p `which python3` venv35
    venv27/bin/pip3 install -r requirements27.txt

## MS Windows, using Python 2.7, anaconda

Download from continuum.io and install Anaconda for Python 2.7 (tested for Anaconda 4.4 on Windows 10)

The Anaconda Python installation contains required packages for all chapters except Artificial neuron networks.

For the last one, we need to install Theano and nose-parameterized by Conda and then theanets by pip.

In Anaconda prompt:

    conda install nose-parameterized theano
    pip install theanets

## MS Windows, using Python 3.6, anaconda

Download from continuum.io and install Anaconda for Python 3.6 (tested for Anaconda 4.4 on Windows 10)

The Anaconda Python installation contains required packages for all chapters except Artificial neuron networks.

First try the procedure for Python 2.7, if it does not work (due to version incompatibility between pygpu and theano, perhaps) then the following.

Install theano with dependencies and nose-parameterized by conda, deinstall pygpu and theano from conda, install theano and theanets by pip.

In Anaconda prompt:

    conda install nose-parameterized theano
    conda uninstall pygpu
    pip install theano
    pip install theanets

## Run tests in command line

Run from the directory of a chapter (not repository root directory).

    python -m unittest discover tests

or

    ../venv35/bin/python3 -m unittest discover tests

  or

    ../venv27/bin/python -m unittest discover tests

## Run tests in PyCharm

If you PyCharm project is the repository, then mark directory of the chapter as sources root (in Project panel, in the context menu of directory "Mark Directory As" -> "Sources Root").

For the single test in Project panel, in the context menu of file "Create Unittests in test_corpus_parser" and make sure that working directory is "something/hidden_markov_model", but not "something/hidden_markov_model/tests".

For all tests do the same in the context menu of the "tests" directory.
