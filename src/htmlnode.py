

class HTMLNode:
    def __init__(self,
                 tag : str|None = None,
                 value : str|None = None,
                 children : list["HTMLNode"] = [],
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
            raise Exception(
                "Cannot convert to html if props is None"
            )

        return " ".join([f'{k}="{self.props[k]}"' for k in self.props])

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

