from __future__ import with_statement

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

class Operation(object):
    def __init__(self, **kw):
        self.src_root = kw.pop('src_root')
        self.dst_root = kw.pop('dst_root')
        self.path = kw.pop('path')
        self.config = kw.pop('config')
        self.navigation = kw.pop('navigation')

        self.input = file(
            os.path.join(self.src_root, self.path),
            'rb',
            )

        self.output_files = {}

        super(Operation, self).__init__(**kw)

    def open_input(self, path):
        # TODO better checks..
        assert not path.startswith('/')
        assert not path.startswith('.')
        assert '/.'not in path
        fullpath = os.path.join(self.src_root, path)
        return file(fullpath, 'rb')

    def kludgy_translate_pathname(self, path):
        # TODO get rid of me

        # TODO better checks..
        assert not path.startswith('/')
        assert not path.startswith('.')
        assert '/.'not in path
        fullpath = os.path.join(self.src_root, path)
        return fullpath

    def open_output(self, path):
        # TODO better checks..
        assert not path.startswith('/')
        assert not path.startswith('.')
        assert '/.'not in path
        fullpath = os.path.join(self.dst_root, path)
        if os.path.exists(fullpath):
            raise RuntimeError(
                'Output file exists already: %r' % fullpath,
                )
        if path in self.output_files:
            raise RuntimeError(
                'Output file opened already: %r' % fullpath,
                )

        f = os.tmpfile()
        self.output_files[path] = f

        # dup the fd so the action freely .close()
        fd = os.dup(f.fileno())
        f2 = os.fdopen(fd, 'w')
        return f2

    def close(self):
        self.input.close()

        for path, tempfile in self.output_files.items():
            tempfile.seek(0)
            dst = os.path.join(self.dst_root, path)
            with file(dst, 'wb') as f:
                while True:
                    data = tempfile.read(8192)
                    if not data:
                        break
                    f.write(data)
                tempfile.close()

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
        def safe_names(names):
            return [
                name
                for name in names
                if not (name.startswith('.')
                        or name.startswith('_')
                        or name.startswith('#')
                        )
                and not name.endswith('~')
                ]

        for dirpath, dirnames, filenames in os.walk(self.path):
            dirnames[:] = safe_names(dirnames)
            filenames[:] = safe_names(filenames)

            if dirpath == self.root:
                relative_dir = ''
            else:
                assert dirpath.startswith(self.root + '/')
                relative_dir = dirpath[len(self.root)+1:]
                os.mkdir(os.path.join(destination, relative_dir))

            for filename in filenames:
                current = os.path.join(relative_dir, filename)

                cfg = get_config.get_config(
                    cfg=self.config,
                    type_='input',
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

                g = pkg_resources.iter_entry_points(
                    'roast.action',
                    action,
                    )
                try:
                    entrypoint = g.next()
                except StopIteration:
                    raise RuntimeError('Unknown action: %r' % action)

                op = Operation(
                    src_root=self.root,
                    dst_root=destination,
                    path=current,
                    config=self.config,
                    navigation=navigation,
                    )

                fn = entrypoint.load()
                fn(op)

                op.close()
