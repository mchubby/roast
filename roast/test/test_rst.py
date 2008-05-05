from twisted.trial import unittest

from roast import rst
from roast.test import util

class HTML(unittest.TestCase, util.TestFormattingMixin):
    def test_simple(self):
        src = self.slurp('data', 'simple', 'input', 'index.rst')
        got = rst.asHTML(src)
        d = self.verify(got, 'data', 'simple', 'output', 'index.html')
        return d

    def test_template(self):
        src = self.slurp('data', 'with-template', 'input', 'index.rst')
        template = self.slurp('data', 'with-template', 'input', '_template.html')
        got = rst.asHTML(src, template=template)

        d = self.verify(got, 'data', 'with-template', 'output', 'index.html')
        return d

    def test_entities(self):
        src = self.slurp('data', 'entities', 'input', 'index.rst')
        got = rst.asHTML(src)
        d = self.verify(got, 'data', 'entities', 'output', 'index.html')
        return d
