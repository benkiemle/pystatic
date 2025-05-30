from textnode import *
from leafnode import LeafNode

def main():
    text_node = TextNode("I am some text", TextType.BOLD)
    text_node2 = TextNode("Go here", TextType.LINK, "http://gohere.com")

main()
