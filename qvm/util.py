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
