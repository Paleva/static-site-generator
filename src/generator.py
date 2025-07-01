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
    
    with open(src_path, "r") as md_file:
        md_str = md_file.read()
    with  open(template_path, "r") as template_file:
        template_str = template_file.read()
    
    md_file.close()
    template_file.close()
    
    html_node = markdown_to_html_node(md_str)
    html_str = html_node.to_html()
    title = extract_title(md_str)
    template_str = template_str.replace("{{ Title }}", title)
    template_str = template_str.replace("{{ Content }}", html_str)

    with open(f"{dst_path}/index.html", "w") as html_file:
        html_file.write(template_str)
