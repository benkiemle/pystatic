import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.textnode import TextNode, TextType
from src.processing import *

class TestProcessing(unittest.TestCase):

    def test_split_nodes_delimiter(self):
        test_cases = [
            {
                "input": { 
                    "text": "This is text with a `code block` word",
                    "delimiter": "`",
                    "text_type": TextType.CODE
                },
                "expected_result": [
                    TextNode("This is text with a ", TextType.NORMAL),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.NORMAL),
                ]
            },
            {
                "input": { 
                    "text": "This **is** text with a `code block` word",
                    "delimiter": "`",
                    "text_type": TextType.CODE
                },
                "expected_result": [
                    TextNode("This **is** text with a ", TextType.NORMAL),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.NORMAL),
                ]
            },
            {
                "input": { 
                    "text": "This **is** text with a `code block` word",
                    "delimiter": "**",
                    "text_type": TextType.BOLD
                },
                "expected_result": [
                    TextNode("This ", TextType.NORMAL),
                    TextNode("is", TextType.BOLD),
                    TextNode(" text with a `code block` word", TextType.NORMAL),
                ]
            },
            {
                "input": { 
                    "text": "This **is** text with a `code block` word",
                    "delimiter": "_",
                    "text_type": TextType.ITALIC
                },
                "expected_result": [
                    TextNode("This **is** text with a `code block` word", TextType.NORMAL),
                ]
            },
        ]

        for test_case in test_cases:
            with self.subTest(tcase = test_case):
                node = TextNode(test_case["input"]["text"], TextType.NORMAL)
                new_nodes = split_nodes_delimiter([node], test_case["input"]["delimiter"], test_case["input"]["text_type"])

                self.assertEqual(new_nodes, test_case["expected_result"])

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        result = extract_markdown_images(text)

        self.assertListEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links_exclude_image(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        result = extract_markdown_links(text)

        self.assertListEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images2(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is **text** with an _italic_ word and a `code block` and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a [link](https://boot.dev)", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links2(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) is the best place to be",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is the best place to be", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode(
            "This is the best place to be",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is the best place to be", TextType.NORMAL)
            ],
            new_nodes,
        )
        
    def test_split_links_duplicates(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to boot dev](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes,
                             [
                                TextNode("This is ", TextType.NORMAL),
                                TextNode("text", TextType.BOLD),
                                TextNode(" with an ", TextType.NORMAL),
                                TextNode("italic", TextType.ITALIC),
                                TextNode(" word and a ", TextType.NORMAL),
                                TextNode("code block", TextType.CODE),
                                TextNode(" and an ", TextType.NORMAL),
                                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                TextNode(" and a ", TextType.NORMAL),
                                TextNode("link", TextType.LINK, "https://boot.dev"),
                            ])
        
    
    def test_text_to_textnodes2(self):
        text = "**This** **is** **text** with an _italic_ word and a `code block` _and_ an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes,
                             [
                                TextNode("This", TextType.BOLD),
                                TextNode(" ", TextType.NORMAL),
                                TextNode("is", TextType.BOLD),
                                TextNode(" ", TextType.NORMAL),
                                TextNode("text", TextType.BOLD),
                                TextNode(" with an ", TextType.NORMAL),
                                TextNode("italic", TextType.ITALIC),
                                TextNode(" word and a ", TextType.NORMAL),
                                TextNode("code block", TextType.CODE),
                                TextNode(" ", TextType.NORMAL),
                                TextNode("and", TextType.ITALIC),
                                TextNode(" an ", TextType.NORMAL),
                                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                TextNode(" and a ", TextType.NORMAL),
                                TextNode("link", TextType.LINK, "https://boot.dev"),
                            ])
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_remove_empty(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_header(self):
        md = "# This is header"
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_header6(self):
        md = "###### This is header"
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_header_too_long(self):
        md = "####### This is header"
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_codeblock(self):
        md = "```This is header```"
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.CODEBLOCK)

    def test_block_to_block_type_codeblock2(self):
        md = """```
Does this codeblock work?
I certainly hope so
```"""
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.CODEBLOCK)

    def test_block_to_block_type_quote(self):
        md = """> Does this codeblock work?
> I certainly hope so"""
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        md = """- Does this codeblock work?
- I certainly hope so"""
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list(self):
        md = """1. Does this codeblock work?
2. I certainly hope so"""
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_unordered_list_bad(self):
        md = """1. Does this codeblock work?
1. I certainly hope so"""
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_markdown_to_html_node(self):
        md = """
##### This is the heading! #

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

```
Some Code goes here
```

- This is a list
- with items
"""
        result = markdown_to_html_node(md)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_ordered_list(self):
        md = """
1. Number One
2. Number Two
3. Number Three
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Number One</li><li>Number Two</li><li>Number Three</li></ol></div>",
        )

    def test_extract_title(self):
        md = "# Please find me"
        title = extract_title(md)
        self.assertEqual(title, "Please find me")

    def test_extract_title2(self):
        md = """
Is there a title somewhere? Maybe, who is to say

> Here perhaps?
> Nope, I don't think so

### Here? No luck here, buddy!

# Aw dang, you found me
"""
        title = extract_title(md)
        self.assertEqual(title, "Aw dang, you found me")

    def test_extract_title_raises_error(self):
        md = "Please find me"
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()