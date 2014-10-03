import os
import cmd
import sys
import util

host = sys.argv[1]

cmd.run ("virsh destroy %s"%(host))
cmd.run ("virsh undefine %s"%(host))
cmd.run ("virsh pool-destroy %s"%(host))

vm_dir = util.get_vm_install_dir(host)
cmd.run ("rm -rfv '%s'"%(vm_dir))

cmd.run ("virsh pool-undefine %s"%(host))
