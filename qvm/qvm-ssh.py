import os
import sys
import ssh
import cmd
import pickle
import network

# User cache
user = None
host = sys.argv[1]

if '@' in host:
    user, host = host.split('@')

if not os.path.exists(ssh.USER_CACHE_FILE):
    pickle.dump ({}, open(ssh.USER_CACHE_FILE,'w+'))

user_cache = pickle.load(open(ssh.USER_CACHE_FILE,'r'))
if user:
    user_cache[host] = user
elif host in user_cache:
    user = user_cache[host]
    print "[INFO] Using %s from cache"%(user)
else:
    user = None

pickle.dump (user_cache, open(ssh.USER_CACHE_FILE,'w+'))

# Get IP
ip = network.get_ip(host)
if not ip:
    print "ERROR: Could not get the IP of %s"%(host)
    raise SystemExit

# SSH command line
command = 'ssh -o "UserKnownHostsFile /dev/null" -o "StrictHostKeyChecking=no" '
if user:
    command += "%s@"%(user)
command += ip

# Execute
cmd.run(command)
