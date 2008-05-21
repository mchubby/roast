from roast import rst
from roast.test import util

class Comment_Test(util.TestFormattingMixin):
    def test_simple(self):
        src = self.slurp('data', 'comment', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'comment', 'output', 'index.html')
