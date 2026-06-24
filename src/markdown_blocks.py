from enum import Enum
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in markdown_blocks:
        if not block.strip():
            continue
        cleaned_blocks.append(block.strip())
    return cleaned_blocks


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        lines = block.split("\n")
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            paragraph_node = ParentNode("p", text_to_children(text))
            children.append(paragraph_node)
        elif block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            heading_text = block[level+1:]
            heading_node = ParentNode(f"h{level}", text_to_children(heading_text))
            children.append(heading_node)
        elif block_type == BlockType.CODE:
            code_text = block[4:-3]
            code_node = LeafNode("code", code_text)
            pre_node = ParentNode("pre", [code_node])
            children.append(pre_node)
        elif block_type == BlockType.QUOTE:
            quote_lines = []
            for line in block.split("\n"):
                cleaned_line = line[1:]
                # if cleaned_line starts with " ", remove that space too
                if cleaned_line.startswith(" "):
                    cleaned_line = cleaned_line[1:]
                quote_lines.append(cleaned_line)
            quote_text = "\n".join(quote_lines)
            quote_node = ParentNode("blockquote", text_to_children(quote_text))
            children.append(quote_node)
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = []
            for line in block.split("\n"):
                item_text = line[2:]
                item_node = ParentNode("li", text_to_children(item_text))
                list_items.append(item_node)
            ul_node = ParentNode("ul", list_items)
            children.append(ul_node)
        elif block_type == BlockType.ORDERED_LIST:
            list_items = []
            for line in block.split("\n"):
                parts = line.split(". ", 1)
                item_text = parts[1]
                item_node = ParentNode("li", text_to_children(item_text))
                list_items.append(item_node)
            ol_node = ParentNode("ol", list_items)
            children.append(ol_node)
    return ParentNode("div", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

