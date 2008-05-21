from roast import rst
from roast.test import util
from roast.test.nosetodo import todo

class Blockquote_Test(util.TestFormattingMixin):
    def test_simple(self):
        src = self.slurp('data', 'blockquote', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'blockquote', 'output', 'index.html')

    def test_author(self):
        src = self.slurp('data', 'blockquote-author', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'blockquote-author', 'output', 'index.html')

    def test_author_cite(self):
        from nose.exc import SkipTest
        raise SkipTest("""TODO want to put options['cite'] in <blockquote cite="...">""")
        src = self.slurp('data', 'blockquote-author-cite', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'blockquote-author-cite', 'output', 'index.html')

    def test_cite(self):
        from nose.exc import SkipTest
        raise SkipTest("""TODO want to put options['cite'] in <blockquote cite="...">""")
        src = self.slurp('data', 'blockquote-cite', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'blockquote-cite', 'output', 'index.html')
