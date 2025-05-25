import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        n = HTMLNode(None, "Simple text", [], None)
        self.assertEqual(n.__repr__(), "HTMLNode(None, Simple text, [], None)")

    def test_props_to_html(self):
        n = HTMLNode(None, None, [], {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(n.props_to_html(), 'href="https://www.google.com" target="_blank"')

    def test_to_html_exception(self):
        n = HTMLNode(None, "Simple text", [], None)
        with self.assertRaises(NotImplementedError):
            n.to_html()

    def test_leaf_to_html_p(self):
        n = LeafNode("p", "Hello, world!")
        self.assertEqual(n.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        n = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(n.to_html(), '<a href="https://www.google.com">Click me!</a>')

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
