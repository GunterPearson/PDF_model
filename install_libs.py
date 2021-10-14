#!/usr/bin/env python3
"""install needed library"""
from fabric.api import local, sudo

sudo("pip3 install PyPDF2")
sudo("pip3 install tensorflow")
sudo("pip3 install tensorflow_hub")
sudo("pip3 install numpy")
