import re
import textwrap

from htmlnode import HTMLNode
from textnode import TextNode
from blocktype import BlockType
from textnode import TextType
from parentnode import ParentNode
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
            children_nodes.append(process_paragraph(process_block(block)))
        elif block_type == BlockType.HEADING:
            children_nodes.append(process_heading(process_block(block)))
        elif block_type == BlockType.QUOTE:
            children_nodes.append(process_quote(process_block(block)))
        elif block_type == BlockType.ORDERED_LIST:
            children_nodes.append(process_ol(process_block(block)))
        elif block_type == BlockType.UNORDERED_LIST:
            children_nodes.append(process_ul(process_block(block)))
        elif block_type == BlockType.CODE:
            block = re.sub(r'^```(\w+)?\n?', '', block)   # remove opening ```
            block = re.sub(r'\n?```$', '', block)         # remove closing ```
            block = textwrap.dedent(block)
            children_nodes.append(process_code(block))
    return ParentNode('div', children_nodes)

def process_block(block: str) -> HTMLNode:
    lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
    block = " ".join(lines)
    return block

def process_code(block: str) -> HTMLNode:
    block = block.rstrip('\n') + '\n'
    node = TextNode(block, TextType.CODE)
    node = text_node_to_html_node(node)
    return ParentNode('pre', [node])

def process_ul(block: str) -> HTMLNode:
    list_items = []
    li = process_list_items(block)
    for item in li:
        list_items.append(ParentNode('li', text_to_children(item)))
    return ParentNode('ul', list_items)

def process_ol(block: str) -> HTMLNode:
    list_nodes = []
    li = process_list_items(block)
    for item in li:
        list_nodes.append(ParentNode('li', text_to_children(item)))
    return ParentNode('ol', list_nodes)

def process_paragraph(block: str) -> HTMLNode:
    return ParentNode('p', text_to_children(block))

def process_quote(block: str) -> HTMLNode:
    return ParentNode('blockquote', text_to_children(block))

def process_heading(block: str) -> HTMLNode:
    heading_level = block.count('#')
    return ParentNode(f'h{heading_level}', text_to_children(block))

def text_to_children(text: str) -> list:
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
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