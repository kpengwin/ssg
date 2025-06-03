import unittest

from textnode import TextNode, TextType, BlockType
# from htmlnode import LeafNode
from convert import (
                        text_node_to_html_node,
                        split_nodes_delimiter,
                        extract_markdown_images,
                        extract_markdown_links,
                        split_nodes_image,
                        split_nodes_link,
                        text_to_text_nodes,
                        markdown_to_blocks,
                        block_to_block_type,
                        markdown_to_html_node,
                    )


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
        self.assertListEqual(new_nodes, expected_result)

    def test_noop(self):
        nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODETEXT),
            TextNode(" word", TextType.NORMAL),
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected_result = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODETEXT),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertListEqual(new_nodes, expected_result)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract(self):
        markdown = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(extract_markdown_images(markdown), expected_result)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_not_images(self):
        markdown = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = []
        self.assertEqual(extract_markdown_links(markdown), expected_result)

    def test_extract_links(self):
        markdown = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(extract_markdown_links(markdown), expected_result)

class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_doesnt_lose_text_after_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and not another",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and not another", TextType.NORMAL),
            ],
            new_nodes,
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_doesnt_lose_text_after_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and not another",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and not another", TextType.NORMAL),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_bold_and_normal_line(self):
        text = "This is **text** with a bold word."
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with a bold word.", TextType.NORMAL),
        ]
        self.assertListEqual(expected, text_to_text_nodes(text))
 
    def test_varied_line(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODETEXT),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, text_to_text_nodes(text))
 
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_remove_blank_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line






- This is a list
- with items





"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlocksToBlockType(unittest.TestCase):
    def test_heading(self):
        md = """
## Heading
""".strip()
        blockType = block_to_block_type(md)
        self.assertEqual(blockType, BlockType.HEADING)

    def test_code(self):
        md = """
```
print(something)
```
""".strip()
        blockType = block_to_block_type(md)
        self.assertEqual(blockType, BlockType.CODE)

    def test_quote(self):
        md = \
"""
>Quote
>A great quote
>hopefully
""".strip()
        blockType = block_to_block_type(md)
        self.assertEqual(blockType, BlockType.QUOTE)

    def test_unordered_list(self):
        md = """
- one
- two
- three
""".strip()
        blockType = block_to_block_type(md)
        self.assertEqual(blockType, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        md = """
1. one
2. two
3. three
""".strip()
        blockType = block_to_block_type(md)
        self.assertEqual(blockType, BlockType.ORDERED_LIST)

    def test_paragraph(self):
        md = """
This is just a normal paragraph.
Could be interesting, or not.
"""
        blockType = block_to_block_type(md)
        self.assertEqual(blockType, BlockType.PARAGRAPH)




class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
