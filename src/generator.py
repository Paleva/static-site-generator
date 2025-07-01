
def extract_title(markdown: str):
    blocks = markdown.split('\n')
    if blocks[0].startswith('#') and blocks[0].count("#", 0, 6) == 1:
        return blocks[0].strip("#").strip()
    else:
        raise ValueError("Wrong header level for a title")


def generate_page(src_path: str, template_path: str, dst_path: str):
    print(f"Generating page from {src_path} to {dst_path} using {template_path}")