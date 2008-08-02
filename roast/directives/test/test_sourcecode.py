import os

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

    def test_subdir_include(self):
        t = tree.Tree(self.path('data', 'python-subdir-include', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'python-subdir-include', 'output'))

    def test_subdir_include_relative(self):
        path = self.path('data', 'python-subdir-include', 'input')
        # make a relative path that points to path
        curdir = os.getcwd()
        prefix = curdir+'/'
        assert path.startswith(prefix)
        relative = path[len(prefix):]
        t = tree.Tree(relative)
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'python-subdir-include', 'output'))
