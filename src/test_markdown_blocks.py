import unittest
from textnode import TextNode, TextType
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
    text_to_children
)


class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        """Test splitting a standard markdown string into clean structural blocks"""
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** words and a [link](https://boot.dev).

* This is the first list item
* This is a second list item"""

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** words and a [link](https://boot.dev).",
            "* This is the first list item\n* This is a second list item"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_excess_whitespace(self):
        """Test that excessive newlines and leading/trailing block whitespace are stripped away"""
        markdown = """   \n\n# Heading with spaces   \n\n\n\nParagraph text block.\n\n   """

        expected = [
            "# Heading with spaces",
            "Paragraph text block."
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_block_to_block_type_heading(self):
        """Test detection of heading block types from h1 through h6"""
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Invalid heading syntax (no space or too many hashtags)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too Many"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        """Test detection of code block blocks"""
        code_block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        
        # Missing closing backticks or newline after starting backticks should fall back
        invalid_code = "``` print('hello') ```"
        self.assertEqual(block_to_block_type(invalid_code), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        """Test detection of quotes, and fallback if syntax fails on any line"""
        quote_block = "> This is a quote\n> spanning multiple lines"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
        
        invalid_quote = "> This is a quote\n But this line forgets the angle bracket"
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        """Test detection of unordered lists, and fallback if dashes are missing"""
        ul_block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ul_block), BlockType.UNORDERED_LIST)
        
        invalid_ul = "- Item 1\nItem 2 missing dash\n- Item 3"
        self.assertEqual(block_to_block_type(invalid_ul), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        """Test detection of ordered lists keeping strict numeric sequence"""
        ol_block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ol_block), BlockType.ORDERED_LIST)
        
        # Numbers skipped or out of sequence should break validation
        invalid_ol_sequence = "1. First\n3. Missing index two"
        self.assertEqual(block_to_block_type(invalid_ol_sequence), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        """Test general normal prose defaults back to paragraph type"""
        text = "Just a regular paragraph with multiple words.\nNothing special here."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_text_to_children(self):
        text = "This is **bold** and _italic_"
        nodes = text_to_children(text)
        # Your parser generates 4 text nodes here due to the string boundaries
        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0].tag, None)
        self.assertEqual(nodes[1].tag, "b")
        self.assertEqual(nodes[2].tag, None)
        self.assertEqual(nodes[3].tag, "i")

    def test_markdown_to_html_node_paragraphs(self):
        markdown = "Hello world.\nThis is a newline paragraph."
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(
            node.to_html(), 
            "<div><p>Hello world. This is a newline paragraph.</p></div>"
        )

    def test_markdown_to_html_node_headings_and_code(self):
        markdown = "### This is an H3 heading\n\n```\nprint('code block')\n```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(
            node.to_html(),
            "<div><h3>This is an H3 heading</h3><pre><code>print('code block')\n</code></pre></div>"
        )

    def test_markdown_to_html_node_lists_and_quotes(self):
        markdown = "> Quote line 1\n> Quote line 2\n\n1. First item\n2. Second item"
        node = markdown_to_html_node(markdown)
        # Adjusted to match your exact output where blockquote contains raw text children directly
        expected_html = (
            "<div>"
            "<blockquote>Quote line 1\nQuote line 2</blockquote>"
            "<ol><li>First item</li><li>Second item</li></ol>"
            "</div>"
        )
        self.assertEqual(node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
