from textnode import TextNode
from FSoperations import copy_files, delete_files


def main():
    # node = TextNode("Hello, World!", "plain", None)
    # print(node)
    delete_files('public')
    copy_files('static', 'public')


if __name__ == "__main__":
    main()