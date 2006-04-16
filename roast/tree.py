import os
from zope.interface import implements

from twisted.internet import defer
from twisted.python import filepath

from webut.navi import inavi

from roast import rst

class Tree(object):
    implements(inavi.INavigable)

    def __init__(self, path, _root=None):
        assert isinstance(path, filepath.FilePath)
        self.path = path
        if _root is None:
            _root = path
        self.root = _root

    def lookUp(self, path, filename):
        while True:
            c = path.child(filename)
            if c.isfile():
                return c
            if path == self.root:
                break

            path = path.parent()

    def _exportFile(self, src, dst):
        template = self.lookUp(src.parent(), '_template.html')
        if template is not None:
            template = template.getContent()

        text = src.getContent()
        html = rst.asHTML(text, template=template)
        dst.setContent(html)

    def export(self, destination):
        assert isinstance(destination, filepath.FilePath)

        index = self.path.child('index.rst')
        if index.isfile():
            self._exportFile(index, destination.child('index.html'))

        for childName in self._listChildren():
            child = self.path.child(childName)
            dstDir = destination.child(childName)
            dstFile = dstDir.child('index.html')

            if child.isdir():
                t = self.__class__(child, _root=self.root)
                dstDir.createDirectory()
                t.export(dstDir)
            else:
                child = child.siblingExtension('.rst')
                if child.isfile():
                    dstDir.createDirectory()
                    self._exportFile(child, dstFile)

    def listChildren(self):
        d = defer.maybeDeferred(self._listChildren)
        d.addCallback(list)
        return d

    def _listChildren(self):
        for name in self.path.listdir():
            if (name.startswith('.')
                or name.startswith('_')
                or name.startswith('#')
                ):
                continue
            if name.endswith('~'):
                continue

            base, ext = os.path.splitext(name)
            if ext == '.rst':
                if base == 'index':
                    # index is implicitly used by the parent resource
                    continue
                yield base
            elif ext == '':
                child = self.path.child(name)
                if child.isdir():
                    yield name
