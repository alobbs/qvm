import os
from prettytable import PrettyTable

def format_table(headers,rows):
    x = PrettyTable(["VM", "Status", "IP"])
    for row in rows:
        x.add_row(row)
    return x

def get_basedir():
    return os.path.expanduser("~/qVM")

def get_image_cache_dir():
    return os.path.join (get_basedir(), 'image_cache')

def get_vm_install_dir(name):
    return os.path.join (get_basedir(), 'VMs', name)

def close_guestfs_vm_handler(g):
	g.sync()
	g.umount_all()
	g.close()

def get_guestfs_vm_handler(name):
	import guestfs

	vm_dir = get_vm_install_dir(name)
	vm_disk = os.path.join (vm_dir, "%s.qcow2"%(name))

	g = guestfs.GuestFS (python_return_dict=True)
	g.add_drive_opts (vm_disk, readonly=False)
	g.launch()

	roots = g.inspect_os()
	assert (len(roots) > 0)
	print roots

	for root in roots:
		# Print basic information about the operating system.
		print "  Product name: %s" % (g.inspect_get_product_name (root))
		print "  Version:      %d.%d" % \
			(g.inspect_get_major_version (root),
			 g.inspect_get_minor_version (root))
		print "  Type:         %s" % (g.inspect_get_type (root))
		print "  Distro:       %s" % (g.inspect_get_distro (root))

		mps = g.inspect_get_mountpoints(root)
		for mp_dev_target in mps:
			print "[INFO] mount", mps[mp_dev_target], mp_dev_target
			g.mount(mps[mp_dev_target], mp_dev_target)

	return g

def vm_is_running (vmname):
	cont = os.popen("virsh list --state-running --name").read()
	running_vms = [n.strip() for n in cont.split('\n') if n]
	return vmname in running_vms
