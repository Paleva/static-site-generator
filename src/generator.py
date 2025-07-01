import os
from MDtoHTML import markdown_to_html_node
def extract_title(markdown: str):
    blocks = markdown.split('\n')
    if blocks[0].startswith('#') and blocks[0].count("#", 0, 6) == 1:
        return blocks[0].strip("#").strip()
    else:
        raise ValueError("Wrong header level for a title")


def generate_page(src_path: str, template_path: str, dst_path: str):
    print(f"Generating page from {src_path} to {dst_path} using {template_path}")
    
    md_file = open(src_path, "r")
    template_file = open(template_path, "r")
    md_str = md_file.read()
    template_str = template_file.read()
    
    md_file.close()
    template_file.close()
    
    html_node = markdown_to_html_node(md_str)
    html_str = html_node.to_html()
    title = extract_title(md_str)
    template_str = template_str.replace("{{ Title }}", title)
    template_str = template_str.replace("{{ Content }}", html_str)

    html_file = open(f"{dst_path}/index.html", "w")
    html_file.write(template_str)
