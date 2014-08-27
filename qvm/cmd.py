import os
import sys

def run(cmd):
    import os
    print >> sys.stderr, "+ %s"%(cmd)
    return os.system(cmd)
