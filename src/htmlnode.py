

class HTMLNode:
    def __init__(self, tag, value, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __repr__(self):
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"

    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html method")

    def props_to_html(self):
        if self.props == None:
            return ''
        else:
            return ''.join(f' {key}="{value}"' for key, value in self.props.items())