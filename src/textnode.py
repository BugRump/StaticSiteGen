from enum import Enum
from htmlnode import HTMLNode

class TextType(Enum):
    PLAIN = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text: str, text_type: TextType, link_url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = link_url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode(text='{self.text}', text_type={self.text_type}, url='{self.url}')"
    
def text_node_to_html_node(text_node: TextNode):
    # create an HTMLNode based on the TextNode's type and content, use constructors for HTMLnode: (self, tag, value, children=None, props=None)
    if text_node.text_type == TextType.PLAIN:
        return HTMLNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return HTMLNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return HTMLNode(tag="i", value=text_node.text)  
    elif text_node.text_type == TextType.CODE:
        return HTMLNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return HTMLNode(tag="a", value=text_node.text, props={"href": text_node.url})   
    elif text_node.text_type == TextType.IMAGE:
        return HTMLNode(tag="img", value=None, props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")