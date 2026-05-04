from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        
        if self.tag is None:
            return self.value
        
        props_str = self.props_to_html()
        opening_tag = f'<{self.tag} {props_str}>'.strip()
        closing_tag = f'</{self.tag}>'
        return f'{opening_tag}{self.value}{closing_tag}'
    
    def __repr__(self):
        return f"LeafNode(tag='{self.tag}', value='{self.value}', props={self.props})"