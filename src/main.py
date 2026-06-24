import sys
import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    path_static = "./static"
    path_public = "./docs"
    if os.path.exists(path_public):
        shutil.rmtree(path_public)
    copy_files_recursive(path_static, path_public)

    generate_pages_recursive("./content", "./template.html", path_public, basepath)

if __name__ == "__main__":
    main()
