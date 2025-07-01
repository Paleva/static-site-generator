import os.path
from MDtoHTML import markdown_to_html_node

def extract_title(markdown: str):
    blocks = markdown.split('\n')
    if blocks[0].startswith('#') and blocks[0].count("#", 0, 6) == 1:
        return blocks[0].strip("#").strip()
    else:
        raise ValueError("Wrong header level for a title")


def generate_pages(src_path: str, template_path: str, dst_path: str, basepath: str):
    print(f"Generating page from {src_path} to {dst_path} using {template_path}")
    

    dir_items = os.listdir(src_path)
    for item in dir_items:
        if os.path.isdir(os.path.join(src_path, item)):
            os.mkdir(os.path.join(dst_path, item))
            generate_pages(os.path.join(src_path, item), template_path, os.path.join(dst_path, item), basepath)
        else:
            generate_page(src_path, template_path, dst_path, basepath)
    # src_path = os.path.join(src_path, "index.md") 
    
    # with open(src_path, "r") as md_file:
    #     md_str = md_file.read()
    # with open(template_path, "r") as template_file:
    #     template_str = template_file.read()

    # html_node = markdown_to_html_node(md_str)
    # html_str = html_node.to_html()
    # title = extract_title(md_str)
    # template_str = template_str.replace("{{ Title }}", title)
    # template_str = template_str.replace("{{ Content }}", html_str)
    
    # try:
    #     with open(f"{dst_path}/index.html", "w") as html_file:
    #         html_file.write(template_str)
    #     return 
    # except (OSError, IOError) as e:
    #     print(f"Error writting HTML file {e}")
    #     raise


def generate_page(src_path: str, template_path: str, dst_path: str, basepath: str):
    src_path = os.path.join(src_path, "index.md") 
    
    with open(src_path, "r") as md_file:
        md_str = md_file.read()
    with open(template_path, "r") as template_file:
        template_str = template_file.read()

    html_node = markdown_to_html_node(md_str)
    html_str = html_node.to_html()
    title = extract_title(md_str)
    template_str = template_str.replace("{{ Title }}", title)
    template_str = template_str.replace("{{ Content }}", html_str)
    template_str = template_str.replace('href="/', f'href="{basepath}')
    template_str = template_str.replace('src="/', f'src="{basepath}')
    
    try:
        with open(f"{dst_path}/index.html", "w") as html_file:
            html_file.write(template_str)
        return 
    except (OSError, IOError) as e:
        print(f"Error writting HTML file {e}")
        raise