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

################################################################################
# Takes a list of "old nodes", a delimiter, and a text type.
# Returns a new list of nodes, where any "text" type nodes 
# in the input list are (potentially) split into multiple nodes
# based on the syntax. For example, given the following input:
#
# node = TextNode("This is text with a `code block` word", TextType.NORMAL)
# new_nodes = split_nodes_delimiter([node], "`", TextType.CODETEXT)
#
# new_nodes becomes:
#
# [
#     TextNode("This is text with a ", TextType.NORMAL),
#     TextNode("code block", TextType.CODETEXT),
#     TextNode(" word", TextType.NORMAL),
# ]
################################################################################
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: T):

    split_nodes = []
    for node in old_nodes:
        if node.text_type != T.NORMAL:
            split_nodes.append(node)
        if node.text.count(delimiter)%2:
            raise Exception(f"unmatched delimiters: {delimiter}, invalid markdown")

        texts = node.text.split(delimiter)
        odd=True
        for t in texts:
            tt = T.NORMAL if odd else text_type
            odd = not(odd)
            if t:
                split_nodes.append(TextNode(t, tt))

    return split_nodes

