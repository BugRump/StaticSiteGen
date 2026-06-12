import os
import shutil
import sys
from copy_static import *
from functions import *

content_dir = "./content"
static_dir = "./static"
public_dir = "./docs"
template_path = "./template.html"

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

def main():
    recreate_dir(public_dir)
    copy_tree(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_path, public_dir, basepath)




if __name__ == "__main__":
    main()