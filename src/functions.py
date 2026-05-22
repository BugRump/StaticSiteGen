from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *
from blocktype import *
import re
import os

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    fenced_code_pattern = re.compile(r"```[\s\S]*?```")

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if fenced_code_pattern.fullmatch(node.text):
                new_nodes.append(node)
                continue

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

def text_to_textnodes(text):
    new_nodes = []
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_image([node])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        if block != "":
            result.append(block.strip())
    return result

def block_to_blocktype(block):
    new_lines = block.split("\n")
    heading = new_lines[0].startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))
    code = len(new_lines) > 1 and new_lines[0].startswith("```") and new_lines[-1].startswith("```")
    quote = all(line.startswith(">") for line in new_lines)
    un_list = all(line.startswith("- ") for line in new_lines)
    ord_list = all(line.startswith(f"{i}. ") for i, line in enumerate(new_lines, start=1))
    
    if heading:
        return BlockType.HEADING
    elif code:
        return BlockType.CODE
    elif quote:
        return BlockType.QUOTE
    elif un_list:
        return BlockType.UNORDERED_LIST
    elif ord_list:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    result = []
    for node in text_nodes:
        result.append(text_node_to_html_node(node))
    return result

def quote_strip(text):
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()
        if line.startswith(">"):
            line = line[1:].strip()
        if line:
            cleaned.append(line)
    return " ".join(cleaned)

def parse_list_items(text):
    lines = text.split("\n")
    cleaned = []
    children = []
    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if line.startswith("-"):
            line = line[1:].strip()
        elif line.startswith(f"{i}."):
            prefix_len = len(f"{i}.")
            line = line[prefix_len:].strip()

        if line:
            cleaned.append(line)

    for j in cleaned:
        kids = text_to_children(j)
        node = ParentNode("li", kids)
        children.append(node)

    return children

def parse_code_block(text):
    text = text.removeprefix("```\n")
    text = text.removesuffix("```")
    text_node = TextNode(text, TextType.TEXT)
    child = LeafNode(None, text_node.text)
    return child

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    list = []

    for block in markdown_blocks:
        block_type = block_to_blocktype(block)

        if block_type == BlockType.PARAGRAPH:
            spaces = block.replace("\n", " ")
            children = text_to_children(spaces)
            node = ParentNode("p", children)
            list.append(node)
            continue
        elif block_type == BlockType.HEADING:
            split = block.split(" ", 1)
            hash_count = len(split[0])
            children = text_to_children(split[1])
            node = ParentNode(f"h{hash_count}", children)
            list.append(node)
            continue
        elif block_type == BlockType.CODE:
            child = parse_code_block(block)
            node = ParentNode("code", [child])
            parent = ParentNode("pre", [node])
            list.append(parent)
            continue
        elif block_type == BlockType.QUOTE:
            stripped = quote_strip(block)
            children = text_to_children(stripped)
            node = ParentNode("blockquote", children)
            list.append(node)
            continue
        elif block_type == BlockType.UNORDERED_LIST:
            children = parse_list_items(block)
            node = ParentNode("ul", children)
            list.append(node)
            continue
        elif block_type == BlockType.ORDERED_LIST:
            children = parse_list_items(block)
            node = ParentNode("ol", children)
            list.append(node)
            continue
    
    
    return ParentNode("div", list)

def extract_title(markdown):
    lines = markdown.split("\n")
    hash_list = []
    for line in lines:
        if line.startswith("# "):
            hash_list.append(line)
    if len(hash_list) == 0:
        raise Exception("No header contained within markdown text.")
    return hash_list[0][1:].strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    html_template = ""
    markdown_content = ""

    with open(from_path, 'r') as markdown:
        markdown_content = markdown.read()
    
    with open(template_path, 'r') as html:
        html_template = html.read()

    new_html = markdown_to_html_node(markdown_content)
    new_html_string = new_html.to_html()

    page_title = extract_title(markdown_content)

    template = html_template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", new_html_string)

    new_path = os.path.dirname(dest_path)
    os.makedirs(new_path, exist_ok=True)

    with open(dest_path, 'w') as new_content:
        new_content.write(template)

    


