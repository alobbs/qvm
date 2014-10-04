#!/usr/bin/env python

from _utils import run

# Yum updates
run ("sudo yum install -y yum-fastestmirror yum-presto deltarpm")
run ("sudo yum update -y")
