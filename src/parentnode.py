from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("parentnode requires tag")
        
        if self.children == None:
            raise ValueError("parentnode requires children")
        
        props_str = self.props_to_html()

        result = f"<{self.tag}{" " if len(props_str) > 0 else ""}{props_str}>"

        for child in self.children:
            result += child.to_html()

        result += f"</{self.tag}>"

        return result

        