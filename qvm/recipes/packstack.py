#!/usr/bin/env python

import os
import sys

def run(cmd, fatal=True):
    print >> sys.stderr, "+ %s"%(cmd)
    re = os.system(cmd)
    if fatal and re != 0:
        print >> sys.stderr, "[FATAL] Command failed"
        sys.exit(re)
    return re

# Yum updates
run ("sudo yum install -y yum-fastestmirror yum-presto deltarpm")
run ("sudo yum update -y")

# RDO installation
run ("sudo yum install -y https://rdo.fedorapeople.org/rdo-release.rpm")
run ("sudo yum install -y openstack-packstack")

# Packstack
run ("sudo setenforce permissive")
run ("sudo -i packstack --allinone")
