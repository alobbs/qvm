import os
import sys
import ssh
import cmd
import pickle
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

# Execute
if not sys.stdin.isatty():
    cmd.run_command(command, stdin=sys.stdin.read())
else:
    cmd.run(command)
