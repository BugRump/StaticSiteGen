import os
import shutil
from copy_static import *
from functions import *

content_dir = "./content"
static_dir = "./static"
public_dir = "./public"
template_path = "./template.html"

def main():
    recreate_dir(public_dir)
    copy_tree(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_path, public_dir)




if __name__ == "__main__":
    main()