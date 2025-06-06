import os
import re
from typing import List, Union
from textnode import TextNode, TextType as T, BlockType as B
from htmlnode import HTMLNode, LeafNode, ParentNode

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
            if texts[0]:
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
            if texts[0]:
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


def text_to_children(text) -> List[Union[LeafNode, ParentNode]]:
    text_nodes = text_to_text_nodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

    # Split the markdown into blocks (you already have a function for this)
    # Loop over each block:
    #     Determine the type of block (you already have a function for this)
    #     Based on the type of block, create a new HTMLNode with the proper data
    #     Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
    #     The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.
    # Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        print(f"[\n\t{block.strip()}\n]")
        blocktype = block_to_block_type(block)
        print(f"^ Blocktype {blocktype}")
        match(blocktype):
            case (B.HEADING):
                header = re.match(r"#{1,6} ", block)
                if not header:
                    raise Exception("Something is broken")
                hnum = len(header.group())-1
                nodes.append(ParentNode("h"+str(hnum), text_to_children(block[header.span()[1]:])))
            case (B.CODE):
                nodes.append(ParentNode("pre", [text_node_to_html_node(TextNode(block[4:-3], T.CODETEXT))]))
            case (B.QUOTE):
                text = re.sub('>', '', block)
                nodes.append(ParentNode("blockquote", text_to_children(text.strip())))
            case (B.UNORDERED_LIST):
                li = []
                for line in block.split("\n"):
                    li.append(ParentNode("li", text_to_children(line[2:])))
                nodes.append(ParentNode("ul", li))
            case (B.ORDERED_LIST):
                li = []
                for line in block.split("\n"):
                    li.append(ParentNode("li", text_to_children(re.match(r"(\d* )(.*)", line.strip()[2:]).group(2))))
                nodes.append(ParentNode("ul", li))
            case (B.PARAGRAPH):
                text = " ".join(block.split("\n"))
                nodes.append(ParentNode("p", text_to_children(text)))
    return ParentNode("div", nodes)

def extract_title(md):
    for line in md.split('\n'):
        if line[:2] == "# ":
            return line[2:].strip()
    raise Exception("No title found")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_:
        source_md = from_.read()
    with open(template_path) as template:
        template_html = template.read()

    title = extract_title(source_md)
    converted_markdown = markdown_to_html_node(source_md)
    print(f"{converted_markdown}")
    converted_markdown = converted_markdown.to_html()
    template_html = template_html.replace("{{ Title }}", title)
    template_html = template_html.replace("{{ Content }}", converted_markdown)
    dirs = dest_path.split('/')
    if len(dirs) > 1:
        path = ""
        for dir in dirs[:-1]:
            if not os.path.exists(path+dir):
                os.mkdir(path+dir)
            path = path + dir + '/'

    with open(dest_path, "a+") as outfile:
        outfile.write(template_html)


