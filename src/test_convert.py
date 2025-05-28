import unittest

from textnode import TextNode, TextType
# from htmlnode import LeafNode
from convert import text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_normal(self):
        node = TextNode("This is a normal text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a normal text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is an italic node")


    def test_codetext(self):
        node = TextNode("This is a code node", TextType.CODETEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://www.google.com")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://imgur.com/lolcat")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props["src"], "https://imgur.com/lolcat")
        self.assertEqual(html_node.props["alt"], "This is an image node")



class TestSplitDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODETEXT)
        expected_result = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODETEXT),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_result)

if __name__ == "__main__":
    unittest.main()
