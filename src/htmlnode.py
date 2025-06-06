from typing import List, Union

class HTMLNode:
    def __init__(self,
                 tag : str|None = None,
                 value : str|None = None,
                 children : List[Union["ParentNode", "LeafNode"]]|None = None,
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

    def _format_tag_and_props(self):
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
        return tag_f


class LeafNode(HTMLNode):
   def __init__(self,
                 tag : str|None,
                 value : str,
                 props : dict|None = None
                 ):
        super().__init__(tag, value, None, props)

   def to_html(self):
        if not self.value and not(self.tag == "img"):
            raise ValueError(f"All leaf nodes MUST have a value - {self}")

        tag_f = self._format_tag_and_props()

        return f"{tag_f[0]}{self.value}{tag_f[1]}"

class ParentNode(HTMLNode):
    def __init__(self,
                 tag : str|None,
                 children: List[Union["ParentNode", "LeafNode"]],
                 props : dict|None = None
                 ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        elif not self.children or len(self.children) == 0:
            raise ValueError("ParentNode must have children")

        tag_f = self._format_tag_and_props()
        child_values = [x.to_html() for x in self.children]
        return f"{tag_f[0]}{"".join(child_values)}{tag_f[1]}"

