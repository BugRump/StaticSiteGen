import os
import shutil

def recreate_dir(dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)

def copy_tree(source_dir, dest_dir):
    for entry in os.listdir(source_dir):
        src_path = os.path.join(source_dir, entry)
        dst_path = os.path.join(dest_dir, entry)

        if os.path.isdir(src_path):
            os.makedirs(dst_path)
            copy_tree(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
            print(f'Copied: {src_path} -> {dst_path}')