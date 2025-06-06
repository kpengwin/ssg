import os
from shutil import copy, rmtree
from convert import generate_page

def copy_dir_recursive(source: str, dest: str):
    print(f"{source} to {dest}")
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

def generate_page_recursive(content: str, template: str, publish: str):
    dir_entries = os.scandir(content)
    for e in dir_entries:
        if e.is_dir():
            print(f"Directory {content}/{e.name}")
            os.makedirs(f"{publish}/{e.name}", exist_ok=True)
            generate_page_recursive(os.path.join(content, e.name), template, os.path.join(publish, e.name))
        else:
            print(f"File: {content}/{e.name}")
            new_filename = e.name.replace(".md", ".html")
            generate_page(f"{content}/{e.name}", template, f"{publish}/{new_filename}")


def main():
    STATIC_ASSETS_PATH = "static"
    WEB_PATH = "public"
    copy_dir_recursive(STATIC_ASSETS_PATH, WEB_PATH)
    generate_page_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
