class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html_self(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if (self.props == None):
            return ""
        
        result = []

        for key in self.props:
            result.append(f"{key}=\"{self.props[key]}\"")

        return " ".join(result)