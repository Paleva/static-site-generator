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
    """
    Convert a Markdown string into an HTML node tree representing its structure.
    
    Parameters:
        markdown (str): The Markdown-formatted text to convert.
    
    Returns:
        HTMLNode: A root HTML node containing the parsed content as child nodes, preserving the structure and formatting of the original Markdown.
    """
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
    """
    Normalize a Markdown block by stripping whitespace and joining non-empty lines into a single string.
    
    Parameters:
        block (str): The Markdown block to process.
    
    Returns:
        str: The processed block as a single line of text with internal whitespace normalized.
    """
    lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
    processed_block = " ".join(lines)
    return processed_block

def process_code(block: str) -> HTMLNode:
    """
    Convert a Markdown code block into an HTML node tree wrapped in a <pre> element.
    
    Removes Markdown code fence markers and dedents the code block before wrapping it in a <code> node inside a <pre> parent node.
    Returns the resulting HTMLNode representing the code block.
    """
    block = re.sub(r'^```[^\n]*\n?', '', block)   # remove opening ```
    block = re.sub(r'\n?```$', '', block)         # remove closing ```
    block = textwrap.dedent(block) # dedent the block
    block = block.rstrip('\n') + '\n'
    node = TextNode(block, TextType.CODE)
    node = text_node_to_html_node(node)
    return ParentNode('pre', [node])

def process_ul(block: str) -> HTMLNode:
    """
    Convert a Markdown unordered list block into an HTML `<ul>` node with `<li>` children.
    
    Returns:
        HTMLNode: A parent node representing the unordered list, with each list item as a child `<li>` node.
    """
    list_items = []
    li = process_list_items(block)
    for item in li:
        list_items.append(ParentNode('li', text_to_children(item)))
    return ParentNode('ul', list_items)

def process_ol(block: str) -> HTMLNode:
    """
    Convert a Markdown ordered list block into an HTMLNode representing an ordered list.
    
    Parameters:
        block (str): The Markdown text block containing the ordered list.
    
    Returns:
        HTMLNode: A node tree with each list item wrapped in an <li> element, all contained within an <ol> element.
    """
    list_nodes = []
    li = process_list_items(block)
    for item in li:
        list_nodes.append(ParentNode('li', text_to_children(item)))
    return ParentNode('ol', list_nodes)

def process_paragraph(block: str) -> HTMLNode:
    """
    Converts a Markdown paragraph block into an HTML `<p>` node with child nodes representing the inline content.
    
    Returns:
        HTMLNode: A parent node representing the paragraph and its inline elements.
    """
    return ParentNode('p', text_to_children(block))

def process_quote(block: str) -> HTMLNode:
    """
    Converts a Markdown blockquote block into a blockquote HTML node.
    
    Removes leading Markdown blockquote markers from each line, joins the lines into a single string, and wraps the result in a <blockquote> node with appropriate child nodes.
    """
    split = block.split('\n')
    if len(split) == 1:
        return ParentNode("blockquote", text_to_children(block.replace("> ", '').strip()))
    else:
        joined = ""
        for line in split:
            joined += f"{line.replace("> ", "").strip()} "
        
        return ParentNode("blockquote", text_to_children(joined.rstrip()))


def process_heading(block: str) -> HTMLNode:
    """
    Convert a Markdown heading block into one or more HTML heading nodes.
    
    If the block contains a single heading line, returns a ParentNode for the appropriate heading level (`<h1>` to `<h6>`). If multiple heading lines are present, returns a list of ParentNodes for each heading.
    """
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
    """
    Convert plain text into a list of HTMLNode objects representing its inline elements.
    
    Parameters:
        text (str): The input text to be converted into HTML nodes.
    
    Returns:
        list: A list of HTMLNode objects corresponding to the inline elements found in the input text.
    """
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def process_list_items(list_items: str) -> list[str]:
    """
    Extracts and cleans individual list items from a Markdown list block.
    
    Removes Markdown list markers (such as `*`, `-`, or numbered prefixes) from each line and returns the cleaned item strings.
    
    Parameters:
        list_items (str): The raw Markdown text representing a list block.
    
    Returns:
        list[str]: A list of cleaned list item strings with Markdown markers removed.
    """
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