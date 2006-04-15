from twisted.trial import unittest

import os

from roast import rst

class ReStructuredText(unittest.TestCase):
    def open(self, *segments):
        path = os.path.dirname(__file__)
        path = os.path.join(path, *segments)
        return file(path)

    def slurp(self, *segments):
        f = self.open(*segments)
        data = f.read()
        f.close()
        return data

    def test_simple(self):
        src = self.slurp('data', 'simple', 'input.rst')
        got = rst.asHTML(src)

        want = self.open('data', 'simple', 'output.html').read()
        self.assertEquals(got, want)
