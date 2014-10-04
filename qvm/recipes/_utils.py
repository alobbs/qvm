import os
import sys

def run(cmd, fatal=True):
    print >> sys.stderr, "+ %s"%(cmd)
    re = os.system(cmd)
    if fatal and re != 0:
        print >> sys.stderr, "[FATAL] Command failed"
        sys.exit(re)
    return re
