import os
import shutil
from copy_static import *

static_dir = "./static"
public_dir = "./public"

def main():
    recreate_dir(public_dir)
    copy_tree(static_dir, public_dir)




if __name__ == "__main__":
    main()