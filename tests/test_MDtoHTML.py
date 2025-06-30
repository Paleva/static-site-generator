import unittest
from MDtoHTML import markdown_to_html_node

class TestMDtoHTML(unittest.TestCase):
    def test_paragraphs(self):
        """
        Tests that Markdown paragraphs with bold, italic, and inline code formatting are correctly converted to HTML paragraphs with appropriate tags.
        """
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        # print(html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        """
        Test that a fenced code block in Markdown is correctly converted to an HTML <pre><code> block, preserving all original formatting and content.
        """
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        # print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_headings(self):
        """
        Tests that Markdown headings are correctly converted to their corresponding HTML heading tags within a div container.
        """
        md = """
        # Heading 1
        ## Heading 2
        ### Heading 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        # print(html)
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        )

    def test_blockquote(self):
        """
        Tests that a multi-line Markdown blockquote with inline italic formatting is correctly converted to an HTML <blockquote> element within a <div>.
        """
        md = """
    > This is a blockquote
    > with multiple lines
    > and _italic_ text
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        # print(html)
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines and <i>italic</i> text</blockquote></div>"
        )

    def test_unordered_list(self):
        """
        Tests that an unordered Markdown list with inline formatting is correctly converted to an HTML unordered list with appropriate tags for bold and code.
        """
        md = """
    - First item
    - Second item with **bold**
    - Third item with `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        # print(html)
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <code>code</code></li></ul></div>"
        )

    def test_ordered_list(self):
        """
        Test that an ordered Markdown list with inline formatting is correctly converted to HTML.
        
        Verifies that numbered list items, including those with italic and inline code formatting, are rendered as an HTML `<ol>` with `<li>` elements containing appropriate `<i>` and `<code>` tags, all wrapped in a `<div>`.
        """
        md = """
    1. First item
    2. Second item with _emphasis_
    3. Third item with `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        # print(html)
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>emphasis</i></li><li>Third item with <code>code</code></li></ol></div>"
        )

    def test_mixed_content(self):
        """
        Tests conversion of complex Markdown input with mixed content types to HTML.
        
        Verifies that headings, paragraphs with inline formatting, blockquotes with inline code, unordered lists, and fenced code blocks are all correctly converted and nested within a single HTML `<div>`.
        """
        md = """
    # Main Title

    This is a paragraph with **bold** and _italic_ text.

    > A quote with `code`

    - List item 1
    - List item 2

    ```
    Code block
    with multiple
    lines
    ```
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><h1>Main Title</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><blockquote>A quote with <code>code</code></blockquote><ul><li>List item 1</li><li>List item 2</li></ul><pre><code>Code block\nwith multiple\nlines\n</code></pre></div>"
        )
if __name__ == "__main__":
    unittest.main()