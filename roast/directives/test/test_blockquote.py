from twisted.trial import unittest

from roast import rst
from roast.test import util

class Blockquote(unittest.TestCase, util.TestFormattingMixin):
    def test_simple(self):
        src = self.slurp('data', 'blockquote', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'blockquote', 'output', 'index.html')

    def test_author(self):
        src = self.slurp('data', 'blockquote-author', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'blockquote-author', 'output', 'index.html')

    def test_author_cite(self):
        src = self.slurp('data', 'blockquote-author-cite', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'blockquote-author-cite', 'output', 'index.html')
    test_author_cite.todo = """want to put options['cite'] in <blockquote cite="...">"""

    def test_cite(self):
        src = self.slurp('data', 'blockquote-cite', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'blockquote-cite', 'output', 'index.html')
    test_cite.todo = """want to put options['cite'] in <blockquote cite="...">"""
