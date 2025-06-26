
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

            

if __name__ == "__main__":
    unittest.main()
