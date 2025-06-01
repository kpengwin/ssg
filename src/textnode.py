from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODETEXT = "codetext"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str|None=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text_type == other.text_type) and (self.text == other.text) and (self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

