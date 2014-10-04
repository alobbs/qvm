import os
import cmd
import pickle
import network

SSH_CLI_PARAMS = '-o "UserKnownHostsFile /dev/null" ' +\
                 '-o "StrictHostKeyChecking=no"'

USER_CACHE_FILE = os.path.expanduser("~/.qvm_ssh.pickle")

def cache_add_host_user(host,username):
    # Read cache file
    if os.path.exists(USER_CACHE_FILE):
        user_cache = pickle.load(open(USER_CACHE_FILE,'r'))
    else:
        user_cache = {}

    # Add user
    user_cache[host] = username

    # Update cache file
    pickle.dump (user_cache, open(USER_CACHE_FILE,'w+'))

def get_username (vm_name):
    user = None

    if '@' in vm_name:
        user, vm_name = vm_name.split('@')

    if not os.path.exists(USER_CACHE_FILE):
        pickle.dump ({}, open(USER_CACHE_FILE,'w+'))

    user_cache = pickle.load(open(USER_CACHE_FILE,'r'))
    if user:
        user_cache[vm_name] = user
    elif vm_name in user_cache:
        user = user_cache[vm_name]
        print "[INFO] Using %s from cache"%(user)
    else:
        user = None

    pickle.dump (user_cache, open(USER_CACHE_FILE,'w+'))
    return (user, vm_name)

def build_hostname (ip, user=None):
    if user:
        return '%s@%s'%(user,ip)
    return host

def build_ssh_command (ip, user=None, binary="ssh", terminal=False):
    command = 'ssh %s '%(SSH_CLI_PARAMS)
    if terminal:
        command += '-tt '
    command += build_hostname (ip, user)
    return command

def execute_file_over_ssh (vm_name, fullpath, prog_args=None):
    user, host = get_username(vm_name)

    ip = network.get_ip(vm_name)
    if not ip:
        print "ERROR: Could not get the IP of %s"%(vm_name)
        raise SystemExit

    # Copy
    command = "scp %s %s %s:/tmp" % (SSH_CLI_PARAMS, fullpath, build_hostname(ip, user))
    cmd.run(command)

    # Execute
    command = build_ssh_command(ip, user, terminal=True)
    command += " /tmp/%s" %(os.path.basename(fullpath))
    if prog_args:
        command += ' %s'%(prog_args)
    cmd.run(command)

    # Clean up
    command = build_ssh_command(ip, user)
    command += " rm -fv /tmp/%s" %(os.path.basename(fullpath))
    cmd.run(command)

def run (vm_name, run_cmd, args=None):
	user, host = get_username(vm_name)

	ip = network.get_ip(vm_name)
	if not ip:
		print "ERROR: Could not get the IP of %s"%(vm_name)
		raise SystemExit

	command = build_ssh_command (ip, user, terminal=True)
	command += " %s"%(run_cmd)
	return cmd.run(command)
