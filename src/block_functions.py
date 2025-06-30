from blocktype import BlockType


# def markdown_to_blocks(markdown: str):
#     strings = markdown.split('\n')
#     paragraphs = []
#     temp = ''
#     for idx in range(len(strings)-1):
#         if len(strings[idx]) == 0 and idx == 0:
#             continue
#         if len(strings[idx]) == 0:
#             paragraphs.append(temp.strip())
#             temp = ''
#         else:
#             if strings[idx+1] == '':
#                 temp += strings[idx]
#             else:
#                 temp += strings[idx] + '\n'
    
    
#     return [paragraph for paragraph in paragraphs if len(paragraph)!=0]

def markdown_to_blocks(markdown):
    """
    Split a markdown string into a list of non-empty, trimmed blocks separated by double newlines.
    
    Parameters:
        markdown (str): The markdown text to be split into blocks.
    
    Returns:
        list[str]: A list of markdown blocks, each stripped of leading and trailing whitespace.
    """
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(markdown: str) -> BlockType:
    """
    Determine the type of a markdown block and return its corresponding BlockType.
    
    Returns:
        BlockType: The type of the markdown block, such as HEADING, CODE, QUOTE, UNORDERED_LIST, ORDERED_LIST, or PARAGRAPH.
    """
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        if markdown.count('#') > 6:
            return BlockType.PARAGRAPH
        return BlockType.HEADING
    
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    
    if markdown.startswith("> "):
        lines = markdown.split('\n')
        for line in lines:
            line = line.strip()
            if not line.startswith("> "):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if markdown.startswith("- "):
        lines = markdown.split('\n')
        for line in lines:
            line = line.strip()
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if markdown.startswith("1. "):
        list_items = markdown.split('\n')
        for idx, item in enumerate(list_items):
            item = item.strip()
            if not item.startswith(f"{idx+1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH