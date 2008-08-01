from roast import rst

from roast import tree
from roast.test.util import (
    compare_files,
    maketemp,
    TestTreeMixin,
    )

class Python_Test(TestTreeMixin):
    def test_simple(self):
        t = tree.Tree(self.path('data', 'python', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'python', 'output'))

    def test_comment(self):
        t = tree.Tree(self.path('data', 'python-comment', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'python-comment', 'output'))

    def test_include(self):
        t = tree.Tree(self.path('data', 'python-include', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'python-include', 'output'))
