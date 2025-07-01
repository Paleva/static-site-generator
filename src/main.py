from textnode import TextNode
from FSoperations import copy_files, delete_files
from generator import generate_page

def main():
    delete_files('public')
    copy_files('static', 'public')
    generate_page("./content/index.md", "template.html", "public")


if __name__ == "__main__":
    main()