import os
import cmd
import cli
import util
import fedora
import argparse

# Parse parameters
parser = argparse.ArgumentParser(description='New VM')
parser.add_argument('name',   action='store', help="VM name")
parser.add_argument('--os',   action='store', default="fedora", help="[fedora]")
parser.add_argument('--mem',  action='store', default="1024",   help="Mb of memory")
parser.add_argument('--cpus', action='store', default="2",      help="Number of CPUs")
parser.add_argument('--disk', action='store', default="10G",    help="Size of the image")
parser.add_argument('--refresh-img', action='store_true', default=False, help="Refresh base image")
args = parser.parse_args()

vm_dir = util.get_vm_install_dir(args.name)
vm_disk = os.path.join (vm_dir, "%s.qcow2"%(args.name))
vm_ci_iso = os.path.join (vm_dir, "%s-cidata.iso"%(args.name))

# OS
all_vars = locals()
all_vars.update(globals())
if args.os in all_vars:
    os_script = all_vars[args.os]
else:
    cli.FATAL_ERROR ("Unsupported OS: '%s'"%(args.os))

# Clean up
cmd.run ("rm -rf '%s'"%(vm_dir))
cmd.run ("mkdir -p '%s'"%(vm_dir))

cmd.run ("virsh destroy %s"%(args.name))
cmd.run ("virsh undefine %s"%(args.name))

# Initial image
if args.refresh_img:
    os_script.download_latest_image()

orig_img = os_script.get_latest_cached_image()
if not orig_img:
    # On first run there is no img
    os_script.download_latest_image()
    orig_img = os_script.get_latest_cached_image()

cmd.run ("cp %s %s"%(orig_img, vm_disk))

# Cloud-init
user_data_fp = os.path.join (vm_dir, "user-data")
meta_data_fp = os.path.join (vm_dir, "meta-data")

ssh_key = open (os.path.expanduser("~/.ssh/id_rsa.pub"),'r').read()

params = {'hostname':args.name, 'ssh_key': ssh_key}
open (user_data_fp, "w+").write(os_script.USER_DATA%(params))
open (meta_data_fp, "w+").write(os_script.META_DATA%(params))

cmd.run ("genisoimage -output %(vm_ci_iso)s -volid cidata -joliet -r %(user_data_fp)s %(meta_data_fp)s"%(locals()))

# Create the VM
cmd.run ("virt-install --import --os-type=linux --nographics" + \
     " --ram %s" %(args.mem) +\
     " --name %s" %(args.name) +\
     " --vcpus %s" %(args.cpus) +\
     " --disk %s,format=qcow2,bus=virtio" %(vm_disk) +\
     " --disk %s,device=cdrom" %(vm_ci_iso) +\
     " --network bridge=virbr0,model=virtio")

cmd.run("virsh change-media %s hda --eject --config" %(args.name))
cmd.run("rm %s %s %s"%(vm_ci_iso, user_data_fp, meta_data_fp))

# Resize
cmd.run("virt-filesystems --long -h --all -a %s" %(vm_disk))
cmd.run("qemu-img create -f qcow2 -o preallocation=metadata %s.new %s"%(vm_disk, args.disk))
cmd.run("virt-resize --quiet --expand /dev/sda1 %s %s.new"%(vm_disk, vm_disk))
cmd.run("mv %s.new %s"%(vm_disk, vm_disk))

# Start VM
cmd.run ("virsh start %s"%(args.name))

# Post install
os_script.cb_post_install(args.name)
