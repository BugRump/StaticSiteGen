import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected_repr = "TextNode(text='This is a text node', text_type=TextType.BOLD, url='None')"
        self.assertEqual(repr(node), expected_repr)

    def test_valid_text_types(self):
        for text_type in TextType:
            node = TextNode("Sample text", text_type)
            self.assertEqual(node.text_type, text_type)

    def test_link_url(self):
        url = "https://example.com"
        node = TextNode("This is a link", TextType.LINK, link_url=url)
        self.assertEqual(node.url, url)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")    

    def test_text_node_to_html_node(self):
        node = TextNode("Hello", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "Hello")

        node = TextNode("Click here", TextType.LINK, link_url="https://example.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "Click here")
        self.assertEqual(html.props, {"href": "https://example.com"})

if __name__ == "__main__":
    unittest.main()