import unittest

from functions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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
    
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_empty(self):
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 0)

    def test_split_nodes_delimiter_no_delims(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Just plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("Over `code` then `more code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Over ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " then ")
        self.assertEqual(new_nodes[3].text, "more code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

    def test_split_nodes_delimiter_unclosed(self):
        node = TextNode("Unclosed `delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimiter_preserve_others(self):
        node1 = TextNode("Text with `code`", TextType.TEXT)
        node2 = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, "Bold text")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_single(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(extract_markdown_images(text), expected)
    
    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(extract_markdown_images(text), expected)
    
    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        self.assertListEqual(extract_markdown_images(text), [])
    
    def test_extract_markdown_images_empty_string(self):
        self.assertListEqual(extract_markdown_images(""), [])
    
    def test_extract_markdown_images_with_special_chars(self):
        text = "![image with spaces](https://example.com/image%20with%20spaces.jpg)"
        expected = [("image with spaces", "https://example.com/image%20with%20spaces.jpg")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_single(self):
        text = "This is text with a [link](https://example.com)"
        expected = [("link", "https://example.com")]
        self.assertListEqual(extract_markdown_links(text), expected)
    
    def test_extract_markdown_links_multiple(self):
        text = "This is text with a [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(extract_markdown_links(text), expected)
    
    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        self.assertListEqual(extract_markdown_links(text), [])
    
    def test_extract_markdown_links_empty_string(self):
        self.assertListEqual(extract_markdown_links(""), [])
    
    def test_extract_markdown_links_with_special_chars(self):
        text = "[link with spaces](https://example.com/page%20with%20spaces)"
        expected = [("link with spaces", "https://example.com/page%20with%20spaces")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_nodes_image_basic(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/img.png)",
            TextType.TEXT,
        )
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "This is text with an ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/img.png")

    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "Start ![img1](url1) middle ![img2](url2) end",
            TextType.TEXT,
        )
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].text, "img1")
        self.assertEqual(nodes[1].url, "url1")
        self.assertEqual(nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(nodes[3].text, "img2")
        self.assertEqual(nodes[3].url, "url2")

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is text with no images")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_image_empty_list(self):
        self.assertEqual(split_nodes_image([]), [])

    def test_split_nodes_image_with_other_nodes(self):
        nodes = [
            TextNode("Start ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ![img](url) end", TextType.TEXT),
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text_type, TextType.IMAGE)
    
    def test_split_nodes_link_basic(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev)",
            TextType.TEXT,
        )
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "This is text with a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://boot.dev")

    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another](https://github.com)",
            TextType.TEXT,
        )
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0].text, "This is text with a ")
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].url, "https://boot.dev")
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[3].text, "another")
        self.assertEqual(nodes[3].url, "https://github.com")

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is text with no links")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_link_empty_list(self):
        self.assertEqual(split_nodes_link([]), [])

    def test_split_nodes_link_with_other_nodes(self):
        nodes = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" [link](https://boot.dev) end", TextType.TEXT),
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text_type, TextType.LINK)


if __name__ == "__main__":
    unittest.main()