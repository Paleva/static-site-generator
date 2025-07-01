import unittest
from generator import extract_title

class TestGenerator(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello, World!"
        self.assertEqual(extract_title(markdown), "Hello, World!")

    def test_extract_title_with_multiple_lines(self):
        markdown = """# Title
        This is a paragraph
        ## Subtitle
        Another paragraph"""
        self.assertEqual(extract_title(markdown), "Title")

    def test_extract_title_with_extra_whitespace(self):
        markdown = "#    Title with spaces    "
        self.assertEqual(extract_title(markdown), "Title with spaces")

    def test_extract_title_missing(self):
        markdown = "No title here\nJust some text"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_wrong_header_level(self):
        markdown = "## Wrong header level"
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()