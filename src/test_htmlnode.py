import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode("a", "click me", None, props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_pros_none(self):
        node = HTMLNode("This is a tag", "This is a value", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_empty_dict(self):
        node = HTMLNode("This is a tag", "This is a value", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode("a", "click me", None, props)
        self.assertRaises(NotImplementedError, node.to_html)

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')

    def test_leaf_to_html2(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')

    def test_leaf_to_html3(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()

