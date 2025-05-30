from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    CODEBLOCK = "codeblock"
    PARAGRAPH = "paragraph"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"