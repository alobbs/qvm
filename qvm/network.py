import os, re

def get_ip(vm_name):
    # Read VM info
    cont = os.popen('virsh dumpxml %s'%(vm_name)).read()
    macs = re.findall(r"mac address='(.+?)'", cont, re.I)

    # MAC to IP address
    cont = open('/var/lib/libvirt/dnsmasq/default.leases','r').read().split('\n')
    lines = [l.split(' ') for l in cont if l]

    for line in lines:
        if line[1] == macs[0]:
            return line[2]

    return ''

def get_image(vm_name):
    # Read VM info
    cont = os.popen('virsh dumpxml %s'%(vm_name)).read()

    # Get image
    hds = re.findall(r"source file='(.+?)'", cont, re.I)
    return hds[0]
