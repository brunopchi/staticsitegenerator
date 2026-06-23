import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_delim_code(self):
        """Test splitting code blocks with backticks"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_bold(self):
        """Test splitting bold text with double asterisks"""
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_italic(self):
        """Test splitting italic text with a single underscore"""
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes(self):
        """Test passing multiple old nodes where only some are TEXT type"""
        node1 = TextNode("Plain text", TextType.TEXT)
        node2 = TextNode("Already Bold", TextType.BOLD)
        node3 = TextNode("Text with `code` here", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        expected = [
            TextNode("Plain text", TextType.TEXT),
            TextNode("Already Bold", TextType.BOLD),
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_at_start(self):
        """Test edge case where delimiter is at the very beginning of the text"""
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_at_end(self):
        """Test edge case where delimiter is at the very end of the text"""
        node = TextNode("Ending with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Ending with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_exception_unclosed_delimiter(self):
        """Test that an exception is raised when a delimiter isn't closed"""
        node = TextNode("This is text with an unclosed **bold tag", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        """Test extraction of multiple markdown images with alt text and URLs"""
        text = "This is text with an ![image](https://storage.googleapis.com/qvna.png) and ![another](https://storage.googleapis.com/df3.png)"
        expected = [
            ("image", "https://storage.googleapis.com/qvna.png"),
            ("another", "https://storage.googleapis.com/df3.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        """Test extraction of multiple markdown links with anchor text and URLs"""
        text = "This is text with a link [to boot.dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot.dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_images_ignores_links(self):
        """Test that extract_markdown_images does not capture normal links"""
        text = "This has a normal link [boot.dev](https://boot.dev) and an image ![logo](logo.png)"
        expected = [("logo", "logo.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_links_ignores_images(self):
        """Test that extract_markdown_links does not capture images (thanks to negative lookbehind)"""
        text = "This has an image ![logo](logo.png) and a link [boot.dev](https://boot.dev)"
        expected = [("boot.dev", "https://boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_split_nodes_image(self):
        """Test splitting a single node containing multiple markdown images"""
        node = TextNode(
            "This is text with an ![image](https://boot.dev/pic.png) and another ![second](https://boot.dev/pic2.png) right here.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://boot.dev/pic.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "https://boot.dev/pic2.png"),
            TextNode(" right here.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link(self):
        """Test splitting a single node containing multiple markdown links"""
        node = TextNode(
            "Read [my blog](https://blog.dev) or search on [Google](https://google.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Read ", TextType.TEXT),
            TextNode("my blog", TextType.LINK, "https://blog.dev"),
            TextNode(" or search on ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_at_edges(self):
        """Test edge case where an image is at the very beginning or very end of the text"""
        node = TextNode("![start](start.png) mid text ![end](end.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start", TextType.IMAGE, "start.png"),
            TextNode(" mid text ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "end.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_ignores_images(self):
        """Test that split_nodes_link ignores images entirely, and vice versa"""
        node = TextNode(
            "This has a link [boot.dev](https://boot.dev) and an image ![logo](logo.png)",
            TextType.TEXT,
        )
        # Testing link splitter leaves the image syntax raw inside the text node
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This has a link ", TextType.TEXT),
            TextNode("boot.dev", TextType.LINK, "https://boot.dev"),
            TextNode(" and an image ![logo](logo.png)", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes_combined(self):
        """Test a mix of all markdown inline elements in a single string"""
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://boot.dev/pic.png) and a [link](https://boot.dev)"
        
        # Note: Your implementation checks for "_", so ensure your test input matches your parser's expectation
        text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://boot.dev/pic.png) and a [link](https://boot.dev)"
        
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://boot.dev/pic.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes_plain(self):
        """Test that plain text returns a single TEXT type node"""
        text = "Just plain old text with absolutely no markdown markdown markings."
        new_nodes = text_to_textnodes(text)
        expected = [TextNode(text, TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes_empty(self):
        """Test how the function handles an empty string"""
        new_nodes = text_to_textnodes("")
        # Depending on how split_nodes handles empty strings, it might return an empty list 
        # or a single empty text node. Based on your current code skips (not sections[i]), it yields empty:
        self.assertEqual(new_nodes, [])

    def test_text_to_textnodes_consecutive_elements(self):
        """Test handling back-to-back markdown elements without spaces"""
        text = "**BOLD**_ITALIC_`CODE`"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("BOLD", TextType.BOLD),
            TextNode("ITALIC", TextType.ITALIC),
            TextNode("CODE", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
