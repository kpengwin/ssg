from textnode import TextNode, TextType as T
from htmlnode import LeafNode

def text_node_to_html_node(text_node: TextNode):
    match(text_node.text_type):
        # TextType.NORMAL: This should return a LeafNode with no tag, just a raw text value.
        case(T.NORMAL):
            return LeafNode(None,text_node.text)
        # TextType.BOLD: This should return a LeafNode with a "b" tag and the text
        case(T.BOLD):
            return LeafNode('b', text_node.text)
        # TextType.ITALIC: "i" tag, text
        case(T.ITALIC):
            return LeafNode('i', text_node.text)
        # TextType.CODETEXT: "code" tag, text
        case(T.CODETEXT):
            return LeafNode('code', text_node.text)
        # TextType.LINK: "a" tag, anchor text, and "href" prop
        case(T.LINK):
            return LeafNode('a', text_node.text, {"href": text_node.url})
        # TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
        case(T.IMAGE):
            return LeafNode('img', "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Type {text_node.text_type} not an allowable value")
