import os
import sys
from shutil import copy, rmtree
from convert import generate_page

def copy_dir_recursive(source: str, dest: str):
    print(f"{source} to {dest}")
    if os.path.exists(dest):
        print(f"Clearing {dest}")
        rmtree(dest)
    os.mkdir(dest)
    dir_entries = os.scandir(source)
    for e in dir_entries:
        if e.is_dir():
            print(f"Directory {source}/{e.name}")
            os.mkdir(f"{dest}/{e.name}")
            copy_dir_recursive(f"{source}/{e.name}", f"{dest}/{e.name}")
        else:
            print(f"File: {source}/{e.name}")
            copy(f"{source}/{e.name}", f"{dest}/{e.name}")

def generate_page_recursive(content: str, template: str, publish: str, basepath: str):
    dir_entries = os.scandir(content)
    for e in dir_entries:
        if e.is_dir():
            print(f"Directory {content}/{e.name}")
            os.makedirs(f"{publish}/{e.name}", exist_ok=True)
            generate_page_recursive(os.path.join(content, e.name), template, os.path.join(publish, e.name), basepath)
        else:
            print(f"File: {content}/{e.name}")
            new_filename = e.name.replace(".md", ".html")
            generate_page(f"{content}/{e.name}", template, f"{publish}/{new_filename}", False, basepath)


def main():
    print(sys.argv)
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        basepath = '/'
    STATIC_ASSETS_PATH = "static"
    WEB_PATH = "docs"
    copy_dir_recursive(STATIC_ASSETS_PATH, WEB_PATH)
    generate_page_recursive("content", "template.html", WEB_PATH, basepath)

if __name__ == "__main__":
    main()
