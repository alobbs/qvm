#!/usr/bin/env python

from _utils import run

# RDO installation
run ("sudo yum install -y https://rdo.fedorapeople.org/rdo-release.rpm")
run ("sudo yum install -y openstack-packstack")

# Packstack
run ("sudo setenforce permissive")
run ("sudo -i packstack --allinone")
