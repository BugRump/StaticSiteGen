import os
import shutil
from copy_static import *
from functions import *

content_dir = "./content"
static_dir = "./static"
public_dir = "./public"
template_path = "./template.html"
md_paths = {
    "./content/index.md": "./public/index.html",
    "./content/blog/glorfindel/index.md": "./public/blog/glorfindel/index.html",
    "./content/blog/majesty/index.md": "./public/blog/majesty/index.html",
    "./content/blog/tom/index.md": "./public/blog/tom/index.html",
    "./content/contact/index.md": "./public/contact/index.html",
}

def main():
    recreate_dir(public_dir)
    copy_tree(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_path, public_dir)
    #for src, dst in md_paths.items():
    #    generate_page(src, template_path, dst)




if __name__ == "__main__":
    main()