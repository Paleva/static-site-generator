import re

from htmlnode import HTMLNode
from textnode import TextNode
from blocktype import BlockType
from textnode import TextType
from inline_functions import text_to_textnodes, text_node_to_html_node
from block_functions import markdown_to_blocks, block_to_block_type


# quote <quoteblock>
# unordered list <ul><li>
# ordered list <ol><li>
# code <code> nested in <pre>
# heading <h1> <h2> <h3> <h4> <h5> <h6>
# paragraph <p>
def markdown_to_html_node(markdown: str) -> HTMLNode:
    md_blocks: list[str] = markdown_to_blocks(markdown)
    children_nodes = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children_nodes.append(HTMLNode('p', None, text_to_children(block)))
        elif block_type == BlockType.HEADING:
            heading_level = block.count('#')
            children_nodes.append(HTMLNode(f'h{heading_level}', None, text_to_children(block)))
        elif block_type == BlockType.QUOTE:
            children_nodes.append(HTMLNode('blockquote',None , text_to_children(block)))
        elif block_type == BlockType.ORDERED_LIST:
            list_nodes = []
            li = process_list_items(block)
            for item in li:
                list_nodes.append(HTMLNode('li', None, text_to_children(item)))
            children_nodes.append(HTMLNode('ol', None, list_nodes))
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = []
            li = process_list_items(block)
            for item in li:
                list_items.append(HTMLNode('li', None, text_to_children(item)))
            children_nodes.append(HTMLNode('ul', None, list_items))
        elif block_type == BlockType.CODE:
            node = TextNode(block, TextType.CODE)
            node = text_node_to_html_node(node)
            children_nodes.append(HTMLNode('pre', None, [node]))
        print(children_nodes)

    return HTMLNode('div', None, children_nodes)

def text_to_children(text: str) -> list:
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    print(html_nodes)
    return html_nodes


def process_list_items(list_items: str) -> list[str]:
    block_type = block_to_block_type(list_items)
    lines = list_items.split('\n')
    processed_lines = []
    if block_type == BlockType.UNORDERED_LIST:
        for line in lines:
            processed_lines.append(re.sub(r'^\s*(\.\s*|\*\s*|-\s*)', '', line))
    elif block_type == BlockType.ORDERED_LIST:
        for line in lines:
            processed_lines.append(re.sub(r'^\d+\.\s*', '', line))
    return processed_lines