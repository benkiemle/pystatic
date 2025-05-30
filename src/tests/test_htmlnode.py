import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode(props = { "href": "https://www.google.com", "target": "_blank"})

        self.assertEqual("href=\"https://www.google.com\" target=\"_blank\"", html_node.props_to_html())        

    def test_props_to_html_noprops(self):
        html_node = HTMLNode()

        self.assertEqual("", html_node.props_to_html())

    def test_props_to_html_empydict(self):
        html_node = HTMLNode(props = {})

        self.assertEqual("", html_node.props_to_html())

if __name__ == "__main__":
    unittest.main()