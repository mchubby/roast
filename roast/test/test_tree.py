from twisted.trial import unittest

import os, sets

from twisted.internet import utils
from twisted.python import filepath

from webut.navi import inavi

from roast import tree

class _PathMixin(object):
    def path(self, *segments):
        path = os.path.dirname(__file__)
        path = os.path.join(path, *segments)
        return path

class Navigation(unittest.TestCase, _PathMixin):
    def test_interface(self):
        t = tree.Tree(filepath.FilePath(self.path('data', 'simple', 'input')))
        self.failUnless(inavi.INavigable.providedBy(t), "Tree must implement INavigable")
        inavi.INavigable.validateInvariants(t)

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

class Export(unittest.TestCase, _PathMixin):
    def verify(self, got, want):
        d = utils.getProcessOutputAndValue(
            'xmldiff',
            args=['-r', got, want])

        def cb((out, err, code)):
            if err or code!=0:
                l = ["Directories are not equal according to xmldiff."]
                for line in out.splitlines():
                    l.append("%s" % line)
                for line in err.splitlines():
                    l.append("xmldiff error: %s" % line)
                if code!=1:
                    l.append("xmldiff exited with status %d" % code)
                raise unittest.FailTest('\n'.join(l))

        d.addCallback(cb)
        return d

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
