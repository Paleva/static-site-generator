import unittest

from functions import text_node_to_html_node
from textnode import TextNode, TextType

class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_bold(self):
        # Test converting bold text node
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_node_to_html_node_italic(self):
        # Test converting italic text node
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_node_to_html_node_code(self):
        # Test converting code text node
        text_node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>print('hello')</code>")

    def test_text_node_to_html_node_link(self):
        # Test converting link text node
        text_node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.example.com">Click me</a>')

    def test_text_node_to_html_node_image(self):
        # Test converting image text node
        text_node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="image.png" alt="Alt text"></img>')

    def test_text_node_to_html_node_invalid_type(self):
        # Test invalid text type
        text_node = TextNode("Invalid", "INVALID_TYPE")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

if __name__ == "__main__":
    unittest.main()