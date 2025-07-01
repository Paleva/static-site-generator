from textnode import TextNode
import os
import shutil
from pathlib import Path


def copy_files(src: str, dst: str):
    if dir == None:
        return None
    cwd = Path.cwd()
    src_full_path = os.path.join(cwd, src)
    dst_full_path = os.path.join(cwd, dst)
    dir_items = os.listdir(src_full_path)
    for item in dir_items:
        file_path = os.path.join(src_full_path, item)
        if os.path.isdir(file_path):
            dst_file_path = os.path.join(dst_full_path, item)
            os.mkdir(dst_file_path)
            copy_files(f"{src}/{item}", f"{dst}/{item}")
            print(f"CREATED DIRECTORY: {dst_full_path}/{item}")
        elif os.path.isfile(file_path):
            shutil.copy(f"{file_path}", f"{dst_full_path}")
            print(f"COPIED FILE: {file_path} TO {src_full_path}")

def delete_files(dir: str = None):
    if dir == None:
        return None

    cwd = Path.cwd()
    full_path = os.path.join(cwd, dir)
    dir_items = os.listdir(full_path)
    for item in dir_items:
        file_path = os.path.join(full_path, item)
        if os.path.isdir(file_path):
            delete_files(f"{dir}/{item}")
            os.rmdir(file_path)
            print(f"DELETED DIRECTORY: {file_path}")
        elif os.path.isfile(file_path):
            os.remove(file_path)
            print(f"DELETED FILE: {file_path}")
def main():
    # node = TextNode("Hello, World!", "plain", None)
    # print(node)
    delete_files('public')
    copy_files('static', 'public')


if __name__ == "__main__":
    main()