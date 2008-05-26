import errno
import os
import re
import shutil
import ConfigParser
from zope.interface import implements

from roast import rst, explicit_navi

class Tree(object):
    def __init__(self, path, _root=None, _navigation=None):
        self.path = path
        if _root is None:
            _root = path
        self.root = _root
        self._read_config()
        if _navigation is None:
            _navigation = list(self._read_navigation())
        self.navigation = _navigation

    def _read_config(self):
        cfg = ConfigParser.RawConfigParser()
        path = os.path.join(self.root, '_roast.conf')
        try:
            f = file(path)
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

    def _read_navigation(self):
        try:
            f = file(os.path.join(self.root, '_navigation.rst'))
        except IOError, e:
            if e.errno == errno.ENOENT:
                return []
            else:
                raise
        else:
            try:
                text = f.read()
            finally:
                f.close()
            return explicit_navi.get_navigation(text=text)

    def lookUp(self, path, filename):
        while True:
            c = os.path.join(path, filename)
            if os.path.isfile(c):
                return c
            if path == self.root:
                break

            path = os.path.dirname(path)

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
        f = file(src)
        try:
            text = f.read()
        finally:
            f.close()
        kwargs = dict(
            navigation=self.navigation,
            )
        if re.search(
            r'^\.\.\s+include::\s+<s5defs.txt>\s*$',
            text,
            flags=re.MULTILINE,
            ):
            kwargs['flavor'] = 's5'
            assert src.startswith(self.root + '/')
            relative = src[len(self.root + '/'):]
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
            template = self.lookUp(os.path.dirname(src), '_template.html')
            if template is not None:
                f = file(template)
                try:
                    kwargs['template'] = f.read()
                finally:
                    f.close()

        tree = rst.asDOM(text, **kwargs)

        self._fixLinks(tree, depth)

        html = tree.toxml('utf-8')
        tmp = '%s.tmp' % dst
        f = file(tmp, 'w')
        try:
            f.write(html)
        finally:
            f.close()
        os.rename(tmp, dst)

    def _exportFileByCopy(self, src, dst):
        shutil.copyfile(src, dst)

    def export(self, destination, depth=0):
        index = os.path.join(self.path, 'index.rst')
        if os.path.isfile(index):
            self._exportFile(index, os.path.join(destination, 'index.html'), depth=depth)

        for childName in self.listChildren():
            child = os.path.join(self.path, childName)

            if os.path.isdir(child):
                t = self.__class__(
                    child,
                    _root=self.root,
                    _navigation=self.navigation,
                    )
                dstDir = os.path.join(destination, childName)
                os.mkdir(dstDir)
                t.export(dstDir, depth=depth+1)
            else:
                base, ext = os.path.splitext(childName)
                if ext == '':
                    dstFile = os.path.join(destination, base+'.html')
                    child = child+'.rst'
                    if os.path.isfile(child):
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
                    dstFile = os.path.join(destination, childName)
                    self._exportFileByCopy(child, dstFile)

    def listChildren(self):
        for name in os.listdir(self.path):
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
                child = os.path.join(self.path, name)
                if os.path.isdir(child):
                    yield name
