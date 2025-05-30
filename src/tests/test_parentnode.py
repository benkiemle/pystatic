import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"class": "text-bold"})
        child_node = ParentNode("span", [grandchild_node], {"class": "float-right"})
        parent_node = ParentNode("div", [child_node], {"class":"header"})
        self.assertEqual(
            parent_node.to_html(),
            "<div class=\"header\"><span class=\"float-right\"><b class=\"text-bold\">grandchild</b></span></div>",
        )

    def test_missing_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_missing_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_empty_children(self):
        parent_node = ParentNode("div", [])
        parent_node.to_html()

        self.assertEqual(parent_node.to_html(), "<div></div>")

if __name__ == "__main__":
    unittest.main()