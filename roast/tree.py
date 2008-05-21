import errno
import os
import re
import ConfigParser
from zope.interface import implements

from twisted.python import filepath

from roast import rst

class Tree(object):
    def __init__(self, path, _root=None):
        assert isinstance(path, filepath.FilePath)
        self.path = path
        if _root is None:
            _root = path
        self.root = _root
        self._read_config()

    def _read_config(self):
        cfg = ConfigParser.RawConfigParser()
        path = self.root.child('_roast.conf')
        try:
            f = path.open()
        except IOError, e:
            if e.errno == errno.ENOENT:
                pass
            else:
                raise
        else:
            try:
                cfg.readfp(f)
            finally:
                f.close()

        self.config = cfg

    def lookUp(self, path, filename):
        while True:
            c = path.child(filename)
            if c.isfile():
                return c
            if path == self.root:
                break

            path = path.parent()

    def _fixLinks(self, tree, depth):
        assert depth >= 0
        work = [tree]
        while work:
            node = work.pop(0)
            if hasattr(node, 'getAttribute'):
                for attr in ['href', 'src']:
                    path = node.getAttribute(attr)
                    if path is not None:
                        if path.startswith('/'):
                            new = '../' * depth + path[1:]
                            if new == '':
                                new = './'
                            node.setAttribute(attr, new)

            work[:0] = node.childNodes

    def _exportFile(self, src, dst, depth):
        text = src.getContent()
        kwargs = {}
        if re.search(
            r'^\.\.\s+include::\s+<s5defs.txt>\s*$',
            text,
            flags=re.MULTILINE,
            ):
            kwargs['flavor'] = 's5'
            assert src.path.startswith(self.root.path + '/')
            relative = src.path[len(self.root.path + '/'):]
            try:
                theme = self.config.get(
                    section='file %s' % relative,
                    option='s5-theme-url',
                    )
            except (
                ConfigParser.NoSectionError,
                ConfigParser.NoOptionError,
                ):
                theme = '/s5-themes/medium-white' #TODO
            kwargs['s5_theme_url'] = theme
        else:
            kwargs['flavor'] = 'html'
            template = self.lookUp(src.parent(), '_template.html')
            if template is not None:
                kwargs['template'] = template.getContent()

        tree = rst.asDOM(text, **kwargs)

        self._fixLinks(tree, depth)

        html = tree.toxml('utf-8')
        dst.setContent(html)

    def _exportFileByCopy(self, src, dst):
        src.copyTo(dst)

    def export(self, destination, depth=0):
        assert isinstance(destination, filepath.FilePath)

        index = self.path.child('index.rst')
        if index.isfile():
            self._exportFile(index, destination.child('index.html'), depth=depth)

        for childName in self.listChildren():
            child = self.path.child(childName)

            if child.isdir():
                t = self.__class__(child, _root=self.root)
                dstDir = destination.child(childName)
                dstDir.createDirectory()
                t.export(dstDir, depth=depth+1)
            else:
                base, ext = os.path.splitext(child.basename())
                if ext == '':
                    dstFile = destination.child(childName).siblingExtension('.html')
                    child = child.siblingExtension('.rst')
                    if child.isfile():
                        self._exportFile(child, dstFile, depth=depth)
                elif ext in [
                    '.css',
                    '.gif',
                    '.htc',
                    '.jpg',
                    '.js',
                    '.png',
                    '.txt',
                    ]:
                    dstFile = destination.child(childName)
                    self._exportFileByCopy(child, dstFile)

    def listChildren(self):
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
            elif ext in [
                '.css',
                '.gif',
                '.htc',
                '.jpg',
                '.js',
                '.png',
                '.txt',
                ]:
                yield name
            elif ext == '':
                child = self.path.child(name)
                if child.isdir():
                    yield name
