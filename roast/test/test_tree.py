from twisted.trial import unittest

import os, sets
import subprocess

from twisted.internet import utils
from twisted.python import filepath

from roast import tree

class _PathMixin(object):
    def path(self, *segments):
        path = os.path.dirname(__file__)
        path = os.path.join(path, *segments)
        return path

class Navigation(unittest.TestCase, _PathMixin):
    def test_simple_list(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'simple', 'input')))
        d = t.listChildren()
        def verify(got):
            want = []
            self.assertEquals(got, want)
        d.addCallback(verify)
        return d

    def test_template_list(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'with-template', 'input')))
        d = t.listChildren()
        def verify(got):
            got = sets.ImmutableSet(got)
            want = sets.ImmutableSet(['one', 'two'])
            self.assertEquals(got, want)
        d.addCallback(verify)
        return d

    def test_misc_files(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'copy', 'input')))
        d = t.listChildren()
        def verify(got):
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
        d.addCallback(verify)
        return d

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
            base, ext = os.path.splitext(path)

            if ext == '.html':
                p = subprocess.Popen(
                    args=[
                        'xmldiff',
                        '-r',
                        os.path.join(got, path),
                        os.path.join(want, path),
                        ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    )

                (out, err) = p.communicate()
                if err or p.returncode!=0:
                    l = ["Directories are not equal according to xmldiff."]
                    for line in out.splitlines():
                        l.append("%s" % line)
                    for line in err.splitlines():
                        l.append("xmldiff error: %s" % line)
                    if p.returncode!=1:
                        l.append("xmldiff exited with status %d" % p.returncode)
                    raise unittest.FailTest('\n'.join(l))

            else:
                got_data = file(os.path.join(got, path), 'rb').read()
                want_data = file(os.path.join(want, path), 'rb').read()
                if got_data != want_data:
                    raise unittest.FailTest('Files are not equal: %s' % path)

    def test_simple(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'simple', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        d = self.verify(got, self.path('data', 'simple', 'output'))
        return d

    def test_template(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'with-template', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        d = self.verify(got, self.path('data', 'with-template', 'output'))
        return d

    def test_link_rewrite(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'link-rewrite', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        d = self.verify(got, self.path('data', 'link-rewrite', 'output'))
        return d

    def test_copy(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'copy', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        d = self.verify(got, self.path('data', 'copy', 'output'))
        return d

    def test_s5(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 's5', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        d = self.verify(got, self.path('data', 's5', 'output'))
        return d

    def test_s5_theme(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 's5-theme', 'input')))
        got = self.mktemp()
        os.mkdir(got)
        t.export(filepath.FilePath(got))
        d = self.verify(got, self.path('data', 's5-theme', 'output'))
        return d
