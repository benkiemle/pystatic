import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href":"http://boot.dev", "target":"_blank"})
        self.assertEqual(node.to_html(), "<a href=\"http://boot.dev\" target=\"_blank\">Hello, world!</a>")
    
    def test_leaf_to_html_valueonly(self):
        node = LeafNode(None, "Hello, world!", None)
        self.assertEqual(node.to_html(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()