import unittest
from block_functions import markdown_to_blocks, block_to_block_type
from blocktype import BlockType

class TestBlockFunctions(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_basic(self):
        md = """
This is paragraph one

This is paragraph two
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is paragraph one",
                "This is paragraph two",
            ],
        )

    def test_markdown_to_blocks_lists(self):
        md = """
- List item 1
- List item 2
- List item 3

1. Numbered item 1
2. Numbered item 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- List item 1\n- List item 2\n- List item 3",
                "1. Numbered item 1\n2. Numbered item 2",
            ],
        )

    def test_markdown_to_blocks_code_blocks(self):
        md = """
Regular paragraph here

```
def hello_world():
    print('Hello, world!')
```

Another paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Regular paragraph here",
                "```\ndef hello_world():\n    print('Hello, world!')\n```",
                "Another paragraph",
            ],
        )

    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_multiple_empty_lines(self):
        md = """
First paragraph


Second paragraph



Third paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph",
            ],
        )

    def test_markdown_to_blocks_with_quotes(self):
        md = """
Regular paragraph

> This is a quote
> It continues here

Another paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Regular paragraph",
                "> This is a quote\n> It continues here",
                "Another paragraph",
            ],
        )

    def test_markdown_to_blocks_mixed_content(self):
        md = """
# Heading

Normal paragraph
With multiple lines
Still same paragraph

- List starts
- List continues
- List ends

Final paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Normal paragraph\nWith multiple lines\nStill same paragraph",
                "- List starts\n- List continues\n- List ends",
                "Final paragraph",
            ],
        )

    def test_block_to_block_type_paragraph(self):
        block = "This is a normal paragraph with text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        test_cases = {
            "# Heading 1": BlockType.HEADING,
            "## Heading 2": BlockType.HEADING,
            "### Heading 3": BlockType.HEADING,
            "#### Heading 4": BlockType.HEADING,
            "##### Heading 5": BlockType.HEADING,
            "###### Heading 6": BlockType.HEADING,
        }
        for block, expected in test_cases.items():
            self.assertEqual(block_to_block_type(block), expected)

    def test_block_to_block_type_code(self):
        block = """```
def hello():
    print('Hello, world!')
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        test_cases = [
            "> This is a quote",
            "> Multi-line\n> quote block",
            "> Quote with\n> multiple lines\n> in it"
        ]
        for block in test_cases:
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        test_cases = [
            "- Single item",
            "- Item 1\n- Item 2",
            "- Item 1\n- Item 2\n- Item 3"
        ]
        for block in test_cases:
            self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        test_cases = [
            "1. First item",
            "1. First item\n2. Second item",
            "1. First\n2. Second\n3. Third"
        ]
        for block in test_cases:
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_heading(self):
        test_cases = [
            "#Missing space",
            "##Not a heading",
            "###### More than 6 #s #######"
        ]
        for block in test_cases:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_lists(self):
        test_cases = [
            "-Missing space after dash",
            "1.Missing space after dot",
            "2. Wrong starting number\n3. Should start with 1",
            "1. Wrong order\n3. Skipped number"
        ]
        for block in test_cases:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_quote(self):
        test_cases = [
            ">Missing space",
            "Not a quote\n> Mixed with quote",
            "Missing arrow in second line\nThis is not quote format"
        ]
        for block in test_cases:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_code(self):
        test_cases = [
            "``\nNot enough backticks\n``",
            "```\nUnclosed code block",
            "`Single backticks`"
        ]
        for block in test_cases:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
if __name__ == "__main__":
    unittest.main()