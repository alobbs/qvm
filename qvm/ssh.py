import os
import pickle

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
