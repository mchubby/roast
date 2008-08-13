from nose.tools import eq_ as eq

import os, sets

from roast import tree
from roast.test.util import (
    compare_files,
    maketemp,
    TestTreeMixin,
    )


class Export_Test(TestTreeMixin):

    def test_simple(self):
        t = tree.Tree(self.path('data', 'simple', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'simple', 'output'))

    def test_template(self):
        t = tree.Tree(self.path('data', 'with-template', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'with-template', 'output'))

    def test_link_rewrite(self):
        t = tree.Tree(self.path('data', 'link-rewrite', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'link-rewrite', 'output'))

    def test_copy(self):
        t = tree.Tree(self.path('data', 'copy', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'copy', 'output'))

    def test_s5(self):
        t = tree.Tree(self.path('data', 's5', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 's5', 'output'))

    def test_s5_theme(self):
        t = tree.Tree(self.path('data', 's5-theme', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 's5-theme', 'output'))

    def test_navigation(self):
        t = tree.Tree(self.path('data', 'navigation', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'navigation', 'output'))

    def test_graphviz(self):
        t = tree.Tree(self.path('data', 'graphviz', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'graphviz', 'output'))

    def test_subdir_include(self):
        t = tree.Tree(self.path('data', 'subdir-include', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'subdir-include', 'output'))

    def test_subdir_include_relative(self):
        path = self.path('data', 'subdir-include', 'input')
        # make a relative path that points to path
        curdir = os.getcwd()
        prefix = curdir+'/'
        assert path.startswith(prefix)
        relative = path[len(prefix):]
        t = tree.Tree(relative)
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'subdir-include', 'output'))

    def test_ignore(self):
        t = tree.Tree(self.path('data', 'ignore', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'ignore', 'output'))

    def test_config_order(self):
        t = tree.Tree(self.path('data', 'config-order', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'config-order', 'output'))

    def test_dia(self):
        t = tree.Tree(self.path('data', 'dia', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'dia', 'output'))

    def test_entities(self):
        t = tree.Tree(self.path('data', 'entities', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'entities', 'output'))

    def test_xsl(self):
        t = tree.Tree(self.path('data', 'xslt', 'input'))
        tmp = maketemp()
        t.export(tmp)
        self.verify(tmp, self.path('data', 'xslt', 'output'))
