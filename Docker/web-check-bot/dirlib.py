import shutil
import os


def reinit_dir(dir):
    if os.path.exists(dir) and os.path.isdir(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)