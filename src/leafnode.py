from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        
        final_html = f"<{self.tag}"
        if self.props:
            props = self.props_to_html()
            final_html += props + ">"
        else:
            final_html += ">"

        final_html += self.value
        final_html += f"</{self.tag}>"

        return final_html
        