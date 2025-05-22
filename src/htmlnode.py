

class HTMLNode:
    def __init__(self,
                 tag : str|None = None,
                 value : str|None = None,
                 children : list["HTMLNode"]|None = None,
                 props : dict|None = None
                 ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("subclass must override")

    def props_to_html(self):
        if not(self.props):
            return ""
        #     raise Exception(
        #         "Cannot convert to html if props is None"
        #     )


        return " ".join([f'{k}="{self.props[k]}"' for k in self.props])

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
   def __init__(self,
                 tag : str|None,
                 value : str,
                 props : dict|None = None
                 ):

        super().__init__(tag, value, None, props)

   def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes MUST have a value")

        tag_f: list[str]
        props_prefix: str
        if self.props:
            props_prefix = " "
        else:
            props_prefix = ""

        if self.tag:
            tag_f = [f"<{self.tag}{props_prefix}{self.props_to_html()}>",f"</{self.tag}>"]
        else:
            tag_f = ["",""]

        return f"{tag_f[0]}{self.value}{tag_f[1]}"
