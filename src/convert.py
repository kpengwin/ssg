import re
from textnode import TextNode, TextType as T, BlockType as B
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
            continue

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


# takes raw markdown text and returns a list of tuples.
# Each tuple should contain the alt text and the URL of any markdown images.
def extract_markdown_images(text: str):
    matches = re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)
    return matches

# takes raw markdown text and returns a list of tuples.
# Each tuple should contain the anchor text and the URL of any markdown links.
def extract_markdown_links(text: str):
    matches = re.findall(r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)", text)
    return matches

def split_nodes_image(nodes: list[TextNode]):
    split_nodes = []
    for node in nodes:
        matches = extract_markdown_images(node.text)
        if (node.text_type != T.NORMAL) or (len(matches) == 0):
            split_nodes.append(node)
            continue

        nodetext = node.text
        for match in matches:
            alt = match[0]
            link = match[1]
            texts = nodetext.split(f"![{alt}]({link})", 1)
            split_nodes.append(TextNode(texts[0], T.NORMAL))
            split_nodes.append(TextNode(alt, T.IMAGE, link))
            if len(texts) == 2:
                nodetext = texts[1]

        if nodetext:
            split_nodes.append(TextNode(nodetext, T.NORMAL))
    return split_nodes

def split_nodes_link(nodes: list[TextNode]):
    split_nodes = []
    for node in nodes:
        matches = extract_markdown_links(node.text)
        if (node.text_type != T.NORMAL) or (len(matches) == 0):
            split_nodes.append(node)
            continue

        nodetext = node.text
        for match in matches:
            anchor = match[0]
            link = match[1]
            texts = nodetext.split(f"[{anchor}]({link})", 1)
            split_nodes.append(TextNode(texts[0], T.NORMAL))
            split_nodes.append(TextNode(anchor, T.LINK, link))
            if len(texts) == 2:
                nodetext = texts[1]

        if nodetext:
            split_nodes.append(TextNode(nodetext, T.NORMAL))
    return split_nodes

def text_to_text_nodes(text: str):
    textNodes = [TextNode(text, T.NORMAL)]
    delimiters = {
        "**": T.BOLD,
        "_": T.ITALIC,
        "`": T.CODETEXT
    }
    for d in delimiters:
        textNodes = split_nodes_delimiter(textNodes, d, delimiters[d])

    textNodes = split_nodes_image(textNodes)
    textNodes = split_nodes_link(textNodes)

    return textNodes

def markdown_to_blocks(text:str):
    blocks = text.split("\n\n")
    blocks = [b.strip() for b in blocks if b.strip()]

    return blocks

def block_to_block_type(block: str):
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    if re.match(r"#{1,6} .*", block):
        return B.HEADING
    # Code blocks must start with 3 backticks and end with 3 backticks.
    if block[:3] == '```' and block[-3:] == "```":
        return B.CODE
    # Every line in a quote block must start with a > character.
    quote_block = True
    for line in block.split("\n"):
        if not(line) or line[0] != ">":
            quote_block = False
            break
    if quote_block:
        return B.QUOTE
    # Every line in an unordered list block must start with a - character, followed by a space.
    ul_block = True
    for line in block.split("\n"):
        if len(line)<2 or line[:2] != "- ":
            ul_block = False
            break
    if ul_block:
        return B.UNORDERED_LIST
    # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    ol_block = True
    for line in block.split("\n"):
        if len(line)<3 or not(re.match(r"\d\. ", line)):
            ol_block = False
            break
    if ol_block:
        return B.ORDERED_LIST

    # If none of the above conditions are met, the block is a normal paragraph.
    return B.PARAGRAPH


def markdown_to_html_node():
    pass
