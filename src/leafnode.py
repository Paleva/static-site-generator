from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value : str = None , props: dict = None):
        """
        Initialize a LeafNode with a specified HTML tag, optional value, and optional properties.
        
        Parameters:
            tag (str): The HTML tag for the node.
            value (str, optional): The content of the node. Defaults to None.
            props (dict, optional): Additional HTML attributes for the tag. Defaults to None.
        """
        super().__init__(tag, value, None, props)

    def to_html(self):
        """
        Generate the HTML string representation of the leaf node.
        
        Returns:
            str: The HTML representation of the node, or the node's value if no tag is set.
        
        Raises:
            ValueError: If the node's value is None.
        """
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        """
        Return a string representation of the LeafNode showing its tag and value.
        """
        return f"LeafNode({self.tag}, {self.value})"

        
        