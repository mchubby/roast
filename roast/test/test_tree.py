from nose.tools import eq_ as eq

import os, sets

from roast import tree
from roast.test.util import (
    compare_files,
    maketemp,
    )

class _PathMixin(object):
    def path(self, *segments):
        path = os.path.dirname(__file__)
        path = os.path.join(path, *segments)
        return path

class Export_Test(_PathMixin):
    def verify(self, got, want):
        def walk(path):
            dirlist = []
            filelist = []
            for root, dirs, files in os.walk(path):
                assert root == path or root.startswith(path+'/')
                relative = root[len(path+'/'):]
                for name in dirs:
                    dirlist.append(os.path.join(relative, name))
                for name in files:
                    filelist.append(os.path.join(relative, name))
            return sorted(dirlist), sorted(filelist)

        got_dirs, got_files = walk(got)
        want_dirs, want_files = walk(want)
        eq(got_dirs, want_dirs)
        eq(got_files, want_files)

        for path in got_files:
            compare_files(
                got=os.path.join(got, path),
                want=os.path.join(want, path),
                )


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
