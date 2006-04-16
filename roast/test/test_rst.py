from twisted.trial import unittest

import os

from twisted.internet import utils

from roast import rst

class HTML(unittest.TestCase):
    def path(self, *segments):
        path = os.path.dirname(__file__)
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

        d = utils.getProcessOutputAndValue(
            'xmldiff',
            args=[self.path(*segments), os.path.abspath(path)])

        def cb((out, err, code)):
            if out or err or code!=0:
                l = ["Files are not equal according to xmldiff."]
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
        src = self.slurp('data', 'simple', 'input', 'index.rst')
        got = rst.asHTML(src)
        d = self.verify(got, 'data', 'simple', 'output', 'index.html')
        return d

    def test_template(self):
        src = self.slurp('data', 'with-template', 'input', 'index.rst')
        template = self.slurp('data', 'with-template', 'input', '_template.html')
        got = rst.asHTML(src, template=template)

        d = self.verify(got, 'data', 'with-template', 'output', 'index.html')
        return d
