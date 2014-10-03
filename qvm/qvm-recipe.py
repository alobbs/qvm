import os
import ssh
import argparse

# Parse known parameters
parser = argparse.ArgumentParser(description='Run recipe')
parser.add_argument('name',   action='store', help="Virtual Machine's name")
parser.add_argument('recipe', action='store', help="Recipe name")
args,vargs = parser.parse_known_args()

# Recipe
recipe_fp = os.path.join (os.path.dirname(__file__), "recipes", "%s.py"%(args.recipe))

# Execute recipe
ssh.execute_file_over_ssh(args.name, recipe_fp, ' '.join(vargs))
