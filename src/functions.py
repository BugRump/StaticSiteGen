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

def split_nodes_image(old_nodes):
    new_nodes = []
    image_pattern = re.compile(r"(!\[[^\[\]]*\]\([^\(\)]*\))")

    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = image_pattern.split(node.text)
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        for part in parts:
            if not part:
                continue

            image_match = re.fullmatch(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", part)
            if image_match:
                alt_text, url = image_match.groups()
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    link_pattern = re.compile(r"(?<!!)(\[[^\[\]]*\]\([^\(\)]*\))")

    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = link_pattern.split(node.text)
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        for part in parts:
            if not part:
                continue

            link_match = re.fullmatch(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", part)
            if link_match:
                link_text, url = link_match.groups()
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))

    return new_nodes

## Function that takes raw markdown text and makes use of all other split functions.

#example input:
# This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)


# example output:
#[
#    TextNode("This is ", TextType.TEXT),
#    TextNode("text", TextType.BOLD),
#    TextNode(" with an ", TextType.TEXT),
#    TextNode("italic", TextType.ITALIC),
#    TextNode(" word and a ", TextType.TEXT),
#    TextNode("code block", TextType.CODE),
#    TextNode(" and an ", TextType.TEXT),
#    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
#    TextNode(" and a ", TextType.TEXT),
#    TextNode("link", TextType.LINK, "https://boot.dev"),
#]

def text_to_textnodes(text):
    new_nodes = []
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_image([node])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes

