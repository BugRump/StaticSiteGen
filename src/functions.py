from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if not node.text.count(delimiter) % 2 == 0:
                raise Exception(f"Unmatched delimiter '{delimiter}' in text: '{node.text}'")
        
            parts = re.split(rf"({re.escape(delimiter)})", node.text)

            sig = False

            for part in parts:
                if part == delimiter:
                    if sig == False:
                        sig = True
                        continue
                    else:
                        sig = False
                        continue
                
                if sig == True:
                    new_nodes.append(TextNode(part, text_type))
                else:
                    new_nodes.append(TextNode(part, TextType.TEXT))

        else:
            new_nodes.append(node)
    return new_nodes

# Parse text for links and images using regex. Takes raw markdown text and returns a list of tuples.

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return links

# images mine: r"!\[(\w+)\]\((\w+)\)"
# actual: r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

# links mine: r"\[(\w+)\]\((\w+)\)"
# actual: r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
