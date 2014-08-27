import os
import re
import util
import network

# Run virsh list
cmd = "virsh list --all"
with os.popen(cmd) as f:
    cont = [l.strip() for l in f.read().split('\n') if l]

# Skip header
cont = cont[2:]

# VMs
VMs = []
for line in cont:
    line = line.replace ('shut off', 'shut_off')
    VMs.append([f for f in line.split(' ') if f])

# Get IPs
for vm in VMs:
    vm_name = vm[1]
    vm.append(network.get_ip(vm_name))

# Print
print util.format_table (["VM", "Status", "IP"],
                         [[vm[1], vm[2], vm[3]] for vm in VMs])
