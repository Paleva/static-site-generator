from htmlnode import HTMLNode
from block_functions import markdown_to_blocks, block_to_block_type

def markdown_to_html_node(markdown: str) -> HTMLNode:
    md_blocks = markdown_to_blocks(markdown)
    print(md_blocks)