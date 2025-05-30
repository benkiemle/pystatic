import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node but not the same", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq3(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK, "http://go.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "http://www.google.com")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "http://www.google.com"})

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "http://www.google.com/src.jpg")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://www.google.com/src.jpg", "alt": "This is a text node"})

    def test_invalid_text_type(self):
        node = TextNode("This is a text node", "badtype")
        with self.assertRaises(Exception):
            html_node = node.to_html_node()

if __name__ == "__main__":
    unittest.main()