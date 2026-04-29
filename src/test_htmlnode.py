import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_creation(self):
        node = HTMLNode(tag='div', value='Hello World', props={'class': 'container'})
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'Hello World')
        self.assertEqual(node.props, {'class': 'container'})
        self.assertEqual(node.children, [])

    def test_htmlnode_repr(self):
        node = HTMLNode(tag='p', value='Paragraph', props={'id': 'para1'})
        expected_repr = "HTMLNode(tag='p', value='Paragraph', children=[], props={'id': 'para1'})"
        self.assertEqual(repr(node), expected_repr)

    def test_props_to_html(self):
        node = HTMLNode(tag='span', value='', props={'style': 'color: red;', 'class': 'highlight'})
        expected_props_html = 'style="color: red;" class="highlight"'
        self.assertEqual(node.props_to_html(), expected_props_html)