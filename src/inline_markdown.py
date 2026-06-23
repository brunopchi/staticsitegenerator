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

