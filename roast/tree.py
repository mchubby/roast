import errno
import os
import pkg_resources
from zope.interface import implements

from roast import (
    explicit_navi,
    navi_current,
    ordered_config_parser,
    get_config,
    )

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
        cfg = ordered_config_parser.OrderedRawConfigParser()
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

    def export(self, destination):
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
                t.export(dstDir)
            else:
                assert child.startswith(self.root + '/')
                current = child[len(self.root + '/'):]
                dst_root = destination
                if current.count('/') > 0:
                    dst_root = '/'.join(destination.split('/')[:-current.count('/')])

                cfg = get_config.get_config(
                    cfg=self.config,
                    path=current,
                    )
                if cfg is None:
                    continue
                action = cfg.get('action')
                if action is None:
                    continue

                # special case index.html; link points to dir itself
                base, ext = os.path.splitext(current)
                if base.endswith('/index'):
                    base = base[:-len('/index')]
                navigation = navi_current.navi_mark_current(
                    navigation=self.navigation,
                    current='/'+base,
                    )

                found = False
                for entrypoint in pkg_resources.iter_entry_points(
                    'roast.action',
                    action,
                    ):
                    fn = entrypoint.load()
                    fn(
                        config=self.config,
                        src_root=self.root,
                        src_relative=current,
                        dst_root=dst_root,
                        navigation=navigation,
                        )
                    found = True
                    break
                if not found:
                    raise RuntimeError('Unknown action: %r' % action)

    def listChildren(self):
        for name in os.listdir(self.path):
            if (name.startswith('.')
                or name.startswith('_')
                or name.startswith('#')
                ):
                continue
            if name.endswith('~'):
                continue

            yield name
