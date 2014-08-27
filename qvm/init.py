import os
import util

def init():
    # Create ~/.qvm
    base_dir = util.get_basedir()
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Subdirectories
    for d in ('image_cache',):
        new_dir = os.path.join (base_dir, d)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
