from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextType, TextNode
from leafnode import LeafNode
from blocktype import BlockType
import re
        
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if (node.text_type == TextType.NORMAL):
            fragments = node.text.split(delimiter)
            for i in range(0, len(fragments)):
                if len(fragments[i]) > 0:
                    new_node = TextNode(fragments[i], TextType.NORMAL if i % 2 == 0 else text_type)
                    new_nodes.append(new_node)
        else:
            new_nodes.append(node)
            
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_images(old_nodes):
    return split_nodes(old_nodes, extract_markdown_images, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes(old_nodes, extract_markdown_links, TextType.LINK)

def split_nodes(old_nodes, extract_func, text_type):
    new_nodes = []
    text_type_nodes = []
    for node in old_nodes:
        if (node.text_type == TextType.NORMAL):
            elements = extract_func(node.text)
            for element in elements:
                text_type_nodes.append(TextNode(element[0], text_type, element[1]))

            remaining_text = node.text
            for ttn in text_type_nodes:
                fragments = remaining_text.split(f"{"!" if text_type == TextType.IMAGE else ""}[{ttn.text}]({ttn.url})", 1)
                if len(fragments[0]) > 0:
                    new_nodes.append(TextNode(fragments[0], TextType.NORMAL))
                new_nodes.append(ttn)

                if len(fragments) >= 2:
                    remaining_text = fragments[1]
                else:
                    remaining_text = ""

            if len(remaining_text) > 0:
                new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
        else:
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x: x.strip(), blocks))

    results_blocks = []
    for block in blocks:
        if len(block) > 0:
            results_blocks.append(block)

    return results_blocks

def block_to_block_type(markdown):
    if re.search(r"^#{1,6} .*", markdown):
        return BlockType.HEADING
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODEBLOCK
    if all_lines_startwith(markdown, ">"):
        return BlockType.QUOTE
    if all_lines_startwith(markdown, "- "):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(markdown):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
    
def all_lines_startwith(markdown, starter):
    for line in markdown.split("\n"):
        if not line.startswith(starter):
            return False
    return True

def is_ordered_list(markdown):
    lines = markdown.split("\n")
    for i in range(0, len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            return False
        
    return True

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = generate_htmlnode_by_block_type(block, block_type)
        nodes.append(node)

    parent_node = ParentNode("div", nodes)
    return parent_node

def generate_htmlnode_by_block_type(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return LeafNode("p", block)
    
    if block_type == BlockType.HEADING:
        matches = re.findall(r"(^#{1,6}) (.*)", block)
        return LeafNode(f"h{matches[0][0].count("#")}", matches[0][1])
    
    if block_type == BlockType.CODEBLOCK:
        fragments = block.split("```")
        return LeafNode("pre", fragments[1])
    
    if block_type == BlockType.UNORDERED_LIST:
        children = []
        for line in block.split("\n"):
            if len(line) > 0:
                children.append(LeafNode("li", line.replace("-", "").strip()))

        parent = ParentNode("ul", children)
        return parent
    
    if block_type == BlockType.ORDERED_LIST:
        ol_children = []
        for line in block.split("\n"):
            if len(line) > 0:
                ol_children.append(LeafNode("li"), re.findall(r"^\d{1}\. (.*?)")[0][0])

        return ParentNode("ol", children)


