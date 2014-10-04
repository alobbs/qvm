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

def wait_net_service(server, port, timeout=None):
    import errno
    import socket

    print "[INFO] Waiting for %s:%s to be available"%(server, port)

    s = socket.socket()
    if timeout:
        from time import time as now
        # time module is needed to calc timeout shared between two exceptions
        end = now() + timeout

    while True:
        try:
            if timeout:
                next_timeout = end - now()
                if next_timeout < 0:
                    return False
                else:
            	    s.settimeout(next_timeout)
            s.connect((server, port))

        except socket.timeout, err:
            # this exception occurs only if timeout is set
            if timeout:
                return False

        except socket.error, err:
            # catch timeout exception from underlying network library
            # this one is different from socket.timeout
            if type(err.args) != tuple or err[0] not in (errno.ETIMEDOUT, 111, 113):
                raise
        else:
            s.recv(1)
            print "[INFO] %s:%s is available now"%(server,port)
            s.close()
            return True

def wait_vm_net_service(vmname, port, timeout=None):
	ip = get_ip(vmname)
	return wait_net_service (ip, port, timeout)
