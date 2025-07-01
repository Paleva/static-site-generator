from textnode import TextNode
from FSoperations import copy_files, delete_files
from generator import generate_page
import os.path

CONTENT_DIR = "./content"
STATIC_DIR = "./static"
PUBLIC_DIR = "./public"
TEMPLATE_DIR = "./template.html"


def main():
    delete_files(PUBLIC_DIR)
    copy_files(STATIC_DIR, PUBLIC_DIR)
    generate_page(os.path.join(CONTENT_DIR, "index.md"), "template.html", PUBLIC_DIR)


if __name__ == "__main__":
    main()