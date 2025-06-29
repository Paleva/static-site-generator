
import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello world", {"color": "red"})
        self.assertEqual(node.to_html(), '<div color="red">Hello world</div>')
    
    def test_leaf_no_value(self):
        node = LeafNode("p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_init(self):
        node = LeafNode("p", "This is a paragraph of text.", {"class": "my-class"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph of text.")
        self.assertEqual(node.props, {"class": "my-class"})

    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is some raw text.")
        self.assertEqual(node.to_html(), "This is some raw text.")

    def test_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

            

if __name__ == "__main__":
    unittest.main()
