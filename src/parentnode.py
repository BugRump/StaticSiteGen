from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.props = props if props is not None else {}
        self.children = children

    def add_child(self, child):
        self.children.append(child)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag cannot be None")
        
        if self.children == None:
            raise ValueError("Children cannot be None")
        
        props_str = self.props_to_html()
        opening_tag = f'<{self.tag}{props_str}>'.strip()
        closing_tag = f'</{self.tag}>'
        children_html = ''.join(child.to_html() for child in self.children)
        return f'{opening_tag}{children_html}{closing_tag}'