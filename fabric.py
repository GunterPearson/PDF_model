#!/usr/bin/env python3
"""convert pdf to markdown"""
from fabric.api import local

local("cd model/")
local("curl -LO https://storage.googleapis.com/tfhub-modules/google/universal-sentence-encoder/4.tar.gz")
local("tar xfz 4.tar.gz")
local("rm 4.tar.gz")
