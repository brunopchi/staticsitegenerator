import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_basic_title(self):
        """Test extracting a simple H1 title"""
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_title_with_whitespace(self):
        """Test extracting a title with leading or trailing whitespaces"""
        markdown = "#    My Awesome Title   "
        self.assertEqual(extract_title(markdown), "My Awesome Title")

    def test_title_not_first_line(self):
        """Test extracting a title when it's not on the first line"""
        markdown = """
This is a paragraph.
Another paragraph.

# The Real Title

Some more content below.
"""
        self.assertEqual(extract_title(markdown), "The Real Title")

    def test_exception_no_title(self):
        """Test that an exception is raised when no H1 title exists"""
        markdown = """
## Subtitle
This is text without a main header.
"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found!")

    def test_no_space_after_hash(self):
        """Test that a line starting with '#' but no space does not count as a title"""
        markdown = "#TitleWithNoSpace"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_empty_markdown(self):
        """Test that an empty string raises an exception"""
        with self.assertRaises(Exception):
            extract_title("")


if __name__ == "__main__":
    unittest.main()
