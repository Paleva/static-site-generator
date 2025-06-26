from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children: list, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be None for ParentNode")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        print(f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>")
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"