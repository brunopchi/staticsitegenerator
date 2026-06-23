from textnode import TextNode, TextType


def main():
    textnode_instance = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(textnode_instance)


if __name__ == "__main__":
    main()
