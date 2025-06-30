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
            result = process_heading(block)
            if isinstance(result, list):
                children_nodes.extend(result)
            else:
                children_nodes.append(result)
        elif block_type == BlockType.QUOTE:
            children_nodes.append(process_quote(block))
        elif block_type == BlockType.ORDERED_LIST:
            children_nodes.append(process_ol(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children_nodes.append(process_ul(block))
        elif block_type == BlockType.CODE:
            children_nodes.append(process_code(block))
    return ParentNode('div', children_nodes)

def process_block(block: str) -> str:
    lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
    processed_block = " ".join(lines)
    return processed_block

def process_code(block: str) -> HTMLNode:
    block = re.sub(r'^```[^\n]*\n?', '', block)   # remove opening ```
    block = re.sub(r'\n?```$', '', block)         # remove closing ```
    block = textwrap.dedent(block) # dedent the block
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
    split = block.split('\n')
    if len(split) == 1:
        return ParentNode("blockquote", text_to_children(block.replace("> ", '').strip()))
    else:
        joined = ""
        for line in split:
            joined += f"{line.replace("> ", "").strip()} "
        
        return ParentNode("blockquote", text_to_children(joined.rstrip()))


def process_heading(block: str) -> HTMLNode:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    
    # single heading
    if len(lines) == 1:
        heading_level = lines[0].count('#')
        heading_text = lines[0].lstrip('#').strip()
        return ParentNode(f'h{heading_level}', text_to_children(heading_text))
    
    # multiple headings
    heading_node = []
    for line in lines:
        if line.startswith('#'):
            heading_level = line.count('#')
            heading_text = line.lstrip('#').strip()
            heading_node.append(ParentNode(f'h{heading_level}', text_to_children(heading_text)))
    
    return heading_node[0] if len(heading_node) == 1 else heading_node

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
            processed_lines.append(re.sub(r'^\s*\d+\.\s*', '', line))
    return processed_lines