import cmd
import sys

host = sys.argv[1]
cmd.run ("virsh start %s"%(host))
