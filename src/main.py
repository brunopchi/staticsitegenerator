import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive


def main():
    path_static = "./static"
    path_public = "./public"
    if os.path.exists(path_public):
        shutil.rmtree(path_public)
    copy_files_recursive(path_static, path_public)

    generate_pages_recursive("./content", "template.html", "./public")

if __name__ == "__main__":
    main()
