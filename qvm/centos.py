import os
import re
import ssh
import cmd
import util

USER_DATA = """\
#cloud-config
hostname: %(hostname)s
manage_etc_hosts: true
password: centos
chpasswd: {expire: False}
ssh_pwauth: True
ssh_authorized_keys:
  - %(ssh_key)s
runcmd:
  - [ yum, -y, remove, cloud-init ]
  - [ poweroff ]
"""

META_DATA = """\
instance-id: %(hostname)s; local-hostname: %(hostname)s
"""

def get_latest_image_url():
    URL = 'http://cloud.centos.org/centos/7/devel/'

    # Get Fedora versions -
    print "[INFO] Fetching CentOS versions"
    html = os.popen("wget -q -O - %s?C=M;O=D"%(URL),'r').read()

    qcows2 = re.findall (r'<a href="(CentOS-7-x86_64-.*?\.qcow2)">', html)
    return URL + qcows2[-1]

def download_latest_image():
    # Remote
    latest_url = get_latest_image_url()

    # Local
    filename = os.path.basename(latest_url)
    cached_image = os.path.join (util.get_image_cache_dir(), filename)

    # Download
    cmd.run("wget -c -O %s %s" %(cached_image, latest_url))

def get_latest_cached_image():
    cache = util.get_image_cache_dir()
    files = [f for f in os.listdir(cache) if 'CentOS-7-x86_64' in f]
    if not files:
        return
    files.sort(reverse=True)
    return os.path.join (cache, files[0])

def cb_post_install(vm_name):
    ssh.cache_add_host_user (vm_name, 'centos')
