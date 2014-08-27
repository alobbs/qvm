import os
import re
import ssh
import cmd
import util

USER_DATA = """\
#cloud-config
hostname: %(hostname)s
manage_etc_hosts: true
password: fedora
chpasswd: {expire: False}
ssh_pwauth: True
ssh_authorized_keys:
  - ssh-rsa %(ssh_key)s
runcmd:
  - [ yum, -y, remove, cloud-init ]
  - [ poweroff ]
"""

META_DATA = """\
instance-id: %(hostname)s; local-hostname: %(hostname)s
"""

def get_latest_image_url():
    URL = 'http://dl.fedoraproject.org/pub/fedora/linux/updates/'

    # Get Fedora versions
    print "[INFO] Fetching Fedora versions"
    html = os.popen("wget -q -O - %s"%(URL),'r').read()

    vers_s = re.findall(r'<a href="(\d+)\/">', html, re.I)
    vers_i = [int(v) for v in vers_s]
    vers_i.sort(reverse=True)

    # Find qcow image
    for fed_ver in vers_i[:2]:
        dir_url = "%s%s/Images/x86_64/"%(URL,fed_ver)
        print "[INFO] Checking Fedora %s"%(fed_ver)

        html = os.popen("wget -q -O - %s"%(dir_url),'r').read()
        images = re.findall(r'(Fedora-x86_64-.+?\.qcow2)', html, re.I)
        if not images:
            continue

        image_url = "%s%s"%(dir_url,images[0])
        print "[INFO] Found: %s"%(images[0])
        return image_url

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
    files = [f for f in os.listdir(cache) if 'Fedora-x86_64' in f]
	if not files:
		return
    files.sort(reverse=True)
    return os.path.join (cache, files[0])

def cb_post_install(vm_name):
    ssh.cache_add_host_user (vm_name, 'fedora')
