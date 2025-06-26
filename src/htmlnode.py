
class HTMLNode():
    def __init__(self, tag=None, value=None, children: list = None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        final = ""
        for val in self.props:
            final += f' {val}="{self.props[val]}"'
        return final


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
