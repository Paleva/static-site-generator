
import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_string(self):
        node = HTMLNode('<a>', 'aaaa', [], { "href": "example.org"})
        node2 = HTMLNode('<b>', 'aaaa', [], { "href": "example.org"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
    
    def test_prop_to_string(self):
        node = HTMLNode('<div>', 'a', [], {"aria-on-disable": "True"})
        result = ' aria-on-disable="True"'
        self.assertEqual(node.props_to_html(), result)

    def test_props(self):
        node = HTMLNode('<div>', 'a', [], { "href": "example.org"})
        node2 = HTMLNode('<div>', 'a', [], {"aria-on-disable": "True"})
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())

if __name__ == "__main__":
    unittest.main()
