import os
import sys
import ssh
import cmd
import pickle
import network

vm_name = sys.argv[1]
recipe  = sys.argv[2]
vargs   = sys.argv[3:]

# Recipe
recipe_fp = os.path.join (os.path.dirname(__file__), "recipes", "%s.py"%(recipe))

# Execute recipe
ssh.execute_file_over_ssh(vm_name, recipe_fp, ' '.join(vargs))
