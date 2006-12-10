from twisted.trial import unittest

from roast import rst
from roast.test import util

class Blockquote(unittest.TestCase, util.TestFormattingMixin):
    def test_simple(self):
        src = self.slurp('data', 'blockquote', 'input', 'index.rst')
        got = rst.asHTML(src)
        d = self.verify(got, 'data', 'blockquote', 'output', 'index.html')
        return d

    def test_author(self):
        src = self.slurp('data', 'blockquote-author', 'input', 'index.rst')
        got = rst.asHTML(src)
        d = self.verify(got, 'data', 'blockquote-author', 'output', 'index.html')
        return d

    def test_author_cite(self):
        src = self.slurp('data', 'blockquote-author-cite', 'input', 'index.rst')
        got = rst.asHTML(src)
        d = self.verify(got, 'data', 'blockquote-author-cite', 'output', 'index.html')
        return d
    test_author_cite.todo = """want to put options['cite'] in <blockquote cite="...">"""

    def test_cite(self):
        src = self.slurp('data', 'blockquote-cite', 'input', 'index.rst')
        got = rst.asHTML(src)
        d = self.verify(got, 'data', 'blockquote-cite', 'output', 'index.html')
        return d
    test_cite.todo = """want to put options['cite'] in <blockquote cite="...">"""
