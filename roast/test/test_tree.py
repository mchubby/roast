from twisted.trial import unittest

import os, sets

from twisted.python import filepath

from roast import tree
from roast.test.util import compare_files

class _PathMixin(object):
    def path(self, *segments):
        path = os.path.dirname(__file__)
        path = os.path.join(path, *segments)
        return path

class Navigation(unittest.TestCase, _PathMixin):
    def test_simple_list(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'simple', 'input')))
        got = t.listChildren()
        got = list(got)
        self.assertEquals(got, [])

    def test_template_list(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'with-template', 'input')))
        got = t.listChildren()
        got = sets.ImmutableSet(got)
        want = sets.ImmutableSet(['one', 'two'])
        self.assertEquals(got, want)

    def test_misc_files(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'copy', 'input')))
        got = t.listChildren()
        got = sets.ImmutableSet(got)
        want = sets.ImmutableSet([
                'something.css',
                'scripts.js',
                'picture.png',
                'ie-hacks.htc',
                'boring.txt',
                'another.jpg',
                ])
        self.assertEquals(got, want)

class Export(unittest.TestCase, _PathMixin):
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
        self.assertEquals(got_dirs, want_dirs)
        self.assertEquals(got_files, want_files)

        for path in got_files:
            compare_files(
                got=os.path.join(got, path),
                want=os.path.join(want, path),
                )


    def test_simple(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'simple', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        self.verify(got, self.path('data', 'simple', 'output'))

    def test_template(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'with-template', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        self.verify(got, self.path('data', 'with-template', 'output'))

    def test_link_rewrite(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'link-rewrite', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        self.verify(got, self.path('data', 'link-rewrite', 'output'))

    def test_copy(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'copy', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        self.verify(got, self.path('data', 'copy', 'output'))

    def test_s5(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 's5', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        self.verify(got, self.path('data', 's5', 'output'))

    def test_s5_theme(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 's5-theme', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        self.verify(got, self.path('data', 's5-theme', 'output'))
