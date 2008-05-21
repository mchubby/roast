from twisted.trial import unittest

import sys, os
import subprocess

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
            l = ["Directories are not equal according to xmldiff."]
            for line in out.splitlines():
                l.append("%s" % line)
            for line in err.splitlines():
                l.append("xmldiff error: %s" % line)
            if p.returncode!=1:
                l.append("xmldiff exited with status %d" % p.returncode)
            raise unittest.FailTest('\n'.join(l))

    else:
        got_data = file(got, 'rb').read()
        want_data = file(want, 'rb').read()
        if got_data != want_data:
            raise unittest.FailTest('Files are not equal: %s' % got)

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
        path = self.mktemp()
        os.mkdir(path)
        path = os.path.join(path, 'got.html')
        f = file(path, 'w')
        f.write(got)
        f.close()

        wantpath = self.path(*segments)
        compare_files(
            got=path,
            want=wantpath,
            )
