from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        """
        Initialize a ParentNode with a tag name, a list of child nodes, and optional HTML properties.
        
        Parameters:
            tag (str): The HTML tag name for this node.
            children (list): List of child nodes to be nested within this parent node.
            props (dict, optional): Dictionary of HTML attributes for the tag.
        """
        super().__init__(tag, None, children, props)

    def to_html(self):
        """
        Generate the HTML string representation of the parent node and its children.
        
        Raises:
            ValueError: If the tag or children are None.
        
        Returns:
            str: The HTML markup for this node and its children, including any properties as attributes.
        """
        if self.tag is None:
            raise ValueError("Tag cannot be None for ParentNode")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        """
        Return a string representation of the ParentNode, including its tag, value, and children.
        """
        return f"ParentNode({self.tag}, {self.value}, {self.children})"
