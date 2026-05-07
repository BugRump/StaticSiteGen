from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *

# It takes a list of "old nodes", a delimiter, and a text type. It should return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax. For example, given the following input:

# node = TextNode("This is text with a `code block` word", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

# new_nodes then becomes:

# [
#     TextNode("This is text with a ", TextType.TEXT),
#     TextNode("code block", TextType.CODE),
#     TextNode(" word", TextType.TEXT),
# ]

# the .split() and .extemd() methods will be useful.

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if not node.text.count(delimiter) % 2 == 0:
                raise Exception(f"Unmatched delimiter '{delimiter}' in text: '{node.text}'")
        
            parts = node.text.re.split((delimiter))

            for part in parts:
                sig = [False, 0]
                if part == delimiter:
                    if sig[1] % 2 == 0:
                        continue
                    else:
                        sig[0] = True
                        continue
                if sig:
                    sig = False
                    sig[1] += 1
                    new_nodes.append(TextNode(part, text_type))
                else:
                    new_nodes.append(TextNode(part, TextType.TEXT))

        else:
            new_nodes.append(node)
    return new_nodes