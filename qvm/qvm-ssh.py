import os
import sys
import ssh
import cmd
import util
import time
import network

# User cache
user = None
vm_name = sys.argv[1]

if len(sys.argv) > 2:
    remote_cmd = ' '.join(sys.argv[2:])
else:
    remote_cmd = None

# Get username for the session
user, vm_name = ssh.get_username(vm_name)

# Get IP
ip = network.get_ip(vm_name)
if not ip:
    print "ERROR: Could not get the IP of %s"%(vm_name)
    raise SystemExit

# SSH command line
command = ssh.build_ssh_command(ip, user)
if remote_cmd:
    command += ' %s'%(remote_cmd)

# Start the VM if it isn't running
if not util.vm_is_running(vm_name):
	cmd.run("qvm start %s"%(vm_name))

# Make sure the SSH service is ready
network.wait_vm_net_service (vm_name, 22)

# Execute
if not sys.stdin.isatty():
    cmd.run_command(command, stdin=sys.stdin.read())
else:
    cmd.run(command)
