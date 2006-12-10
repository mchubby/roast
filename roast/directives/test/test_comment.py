from twisted.trial import unittest

from roast import rst
from roast.test import util

class Comment(unittest.TestCase, util.TestFormattingMixin):
    def test_simple(self):
        src = self.slurp('data', 'comment', 'input', 'index.rst')
        got = rst.asHTML(src)
        d = self.verify(got, 'data', 'comment', 'output', 'index.html')
        return d
