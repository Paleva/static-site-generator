from textnode import TextNode
from FSoperations import copy_files, delete_files
from generator import generate_page
import os.path

CONTENT_DIR = "./content"
STATIC_DIR = "./static"
PUBLIC_DIR = "./public"
TEMPLATE_PATH = "./template.html"


def main():
    try:
        delete_files(PUBLIC_DIR)
        copy_files(STATIC_DIR, PUBLIC_DIR)
        generate_page(os.path.join(CONTENT_DIR, "index.md"), TEMPLATE_PATH, PUBLIC_DIR)
    except Exception as e:
        print(f"Error during site generation {e}")

if __name__ == "__main__":
    main()