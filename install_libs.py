#!/usr/bin/env python3
"""install needed library"""
from fabric.api import local, sudo

sudo("pip3 install PyPDF2")
sudo("pip3 install tensorflow")
sudo("pip3 install tensorflow_hub")
sudo("pip3 install numpy")
sudo("pip3 install pytesseract")
sudo("pip3 install pdf2image")
sudo("apt-get install tesseract-ocr")
sudo("apt install poppler-utils")

