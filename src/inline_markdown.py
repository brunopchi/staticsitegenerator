import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise Exception("Not a valid markdown syntax!")
            for i in range(0, len(sections)):
                if not sections[i]:
                    continue
                if i % 2 == 0:
                    new_node = TextNode(sections[i], TextType.TEXT)
                else:
                    new_node = TextNode(sections[i], text_type)
                new_nodes.append(new_node)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
        else:
            original_text = old_node.text
            for image in images:
                sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
                if sections[0]:
                    new_node = TextNode(sections[0], TextType.TEXT)
                    new_nodes.append(new_node)
                new_node = TextNode(image[0], TextType.IMAGE, image[1])
                new_nodes.append(new_node)
                original_text = sections[1]
            if original_text:
                new_node = TextNode(original_text, TextType.TEXT)
                new_nodes.append(new_node)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        else:
            original_text = old_node.text
            for link in links:
                sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
                if sections[0]:
                    new_node = TextNode(sections[0], TextType.TEXT)
                    new_nodes.append(new_node)
                new_node = TextNode(link[0], TextType.LINK, link[1])
                new_nodes.append(new_node)
                original_text = sections[1]
            if original_text:
                new_node = TextNode(original_text, TextType.TEXT)
                new_nodes.append(new_node)
    return new_nodes


def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    basic_delimiters = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE
    }
    for delimiter, text_type in basic_delimiters.items():
        text_nodes = split_nodes_delimiter(text_nodes, delimiter, text_type)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

