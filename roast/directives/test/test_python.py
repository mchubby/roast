from twisted.trial import unittest

from roast import rst
from roast.test import util

class Python(unittest.TestCase, util.TestFormattingMixin):
    def test_simple(self):
        src = self.slurp('data', 'python', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'python', 'output', 'index.html')

    def test_comment(self):
        src = self.slurp('data', 'python-comment', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'python-comment', 'output', 'index.html')
