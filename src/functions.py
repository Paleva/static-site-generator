from textnode import TextType, TextNode
from leafnode import LeafNode
import re

def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type not in TextType:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")

    match text_node.text_type:
        case  TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', "", {"src": text_node.url, "alt": text_node.text})
        

def split_nodes_delimiter(old_nodes: list[TextNode], delim: str, text_type: TextType):
    new_nodes = []

    if len(old_nodes) == 0:
        return old_nodes

    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delim not in node.text:
            new_nodes.append(node)
            continue

        if node.text.count(delim) % 2 != 0:
            raise Exception(f"Markdown syntax error. Unclosed {text_type} element")

        parts = node.text.split(delim)

        for idx, part in enumerate(parts):
            if part == '':
                continue
            elif idx % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text: str):
    result: list[str] = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def extract_markdown_links(text: str):
    result: list[str] = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def split_nodes_image(old_nodes: list[TextNode]):
    image_links = []
    for node in old_nodes:
        result = extract_markdown_images(node.text)
        if len(result) != 0:
            image_links.append(result)
    
    print(image_links)

def split_nodes_link(old_nodes: list[TextNode]):
    pass