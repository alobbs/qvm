import os
import cmd
import ssh
import util
import stat
import network
import argparse

REMOTE_TMP = "/var/tmp/recipes"

# Parse known parameters
parser = argparse.ArgumentParser(description='Run recipe')
parser.add_argument('name',   action='store', help="Virtual Machine's name")
parser.add_argument('recipe', action='store', help="Recipe name")
args,vargs = parser.parse_known_args()

# Recipe
recipe_dir = os.path.join (os.path.dirname(__file__), "recipes")

# Make sure the VM is shut down
cmd.run("qvm stop %s"%(args.name))

# Copy recipes
g = util.get_guestfs_vm_handler (args.name)
g.mkdir_p (REMOTE_TMP)

for filename in os.listdir(recipe_dir):
	if filename.endswith(".py"):
		fp_local = os.path.join (recipe_dir, filename)
		fp_vm    = os.path.join (REMOTE_TMP, filename)
		print "+ cp %s %s:%s" % (fp_local, args.name, fp_vm)
		g.upload (fp_local, fp_vm)
		g.chmod (stat.S_IMODE(os.stat(fp_local).st_mode), fp_vm)

util.close_guestfs_vm_handler(g)

# Execute recipe
cmd.run("qvm start %s"%(args.name))
network.wait_vm_net_service (args.name, 22)
ssh.run (args.name, os.path.join(REMOTE_TMP, '%s.py'%(args.recipe)), ' '.join(vargs))
cmd.run("qvm stop %s"%(args.name))
