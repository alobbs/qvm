import os
import re
import cmd
import sys
import time
import util

host = sys.argv[1]
cmd.run ("virsh shutdown %s"%(host))

while util.vm_is_running(host):
	time.sleep(1)
