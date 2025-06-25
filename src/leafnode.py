from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props):
        if value is None:
            raise Exception("Value is required")
        super().__init__(tag, value, None, props)