from nose.tools import (
    eq_ as eq,
    )

import errno
import os
import shutil
import subprocess
import sys

def find_test_name():
    try:
        from nose.case import Test
        from nose.suite import ContextSuite
        import types
        def get_nose_name(its_self):
            if isinstance(its_self, Test):
                file_, module, class_ = its_self.address()
                name = '%s:%s' % (module, class_)
                return name
            elif isinstance(its_self, ContextSuite):
                if isinstance(its_self.context, types.ModuleType):
                    return its_self.context.__name__
    except ImportError:
        # older nose
        from nose.case import FunctionTestCase, MethodTestCase
        from nose.suite import TestModule
        from nose.util import test_address
        def get_nose_name(its_self):
            if isinstance(its_self, (FunctionTestCase, MethodTestCase)):
                file_, module, class_ = test_address(its_self)
                name = '%s:%s' % (module, class_)
                return name
            elif isinstance(its_self, TestModule):
                return its_self.moduleName

    i = 0
    while True:
        i += 1
        frame = sys._getframe(i)
        # kludge, hunt callers upwards until we find our nose
        if (frame.f_code.co_varnames
            and frame.f_code.co_varnames[0] == 'self'):
            its_self = frame.f_locals['self']
            name = get_nose_name(its_self)
            if name is not None:
                return name

def mkdir(*a, **kw):
    try:
        os.mkdir(*a, **kw)
    except OSError, e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise

def maketemp():
    tmp = os.path.join(os.path.dirname(__file__), 'tmp')
    mkdir(tmp)

    name = find_test_name()
    tmp = os.path.join(tmp, name)
    try:
        shutil.rmtree(tmp)
    except OSError, e:
        if e.errno == errno.ENOENT:
            pass
        else:
            raise
    os.mkdir(tmp)
    return tmp

def compare_files(got, want):
    base, ext = os.path.splitext(got)

    if ext == '.html':
        p = subprocess.Popen(
            args=[
                'xmldiff',
                got,
                want,
                ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )

        (out, err) = p.communicate()
        if err or p.returncode!=0:
            l = ["Files are not equal according to xmldiff:",
                 "got  %s" % got,
                 "want %s" % want,
                 ]
            for line in out.splitlines():
                l.append("%s" % line)
            for line in err.splitlines():
                l.append("xmldiff error: %s" % line)
            if p.returncode!=1:
                l.append("xmldiff exited with status %d" % p.returncode)
            raise AssertionError('\n'.join(l))

    else:
        got_data = file(got, 'rb').read()
        want_data = file(want, 'rb').read()
        eq(
            got_data,
            want_data,
            'Files are not equal: %s' % got,
            )

class TestFormattingMixin(object):
    def path(self, *segments):
        module = sys.modules[self.__class__.__module__]
        path = os.path.dirname(module.__file__)
        path = os.path.join(path, *segments)
        return path

    def open(self, *segments):
        path = self.path(*segments)
        return file(path)

    def slurp(self, *segments):
        f = self.open(*segments)
        data = f.read()
        f.close()
        return data

    def verify(self, got, *segments):
        tmp = maketemp()
        path = os.path.join(tmp, 'got.html')
        f = file(path, 'w')
        f.write(got)
        f.close()

        wantpath = self.path(*segments)
        compare_files(
            got=path,
            want=wantpath,
            )
