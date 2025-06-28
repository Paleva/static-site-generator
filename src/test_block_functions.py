import unittest
from block_functions import markdown_to_blocks

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




if __name__ == "__main__":
    unittest.main()