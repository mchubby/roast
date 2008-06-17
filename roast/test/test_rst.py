from roast import rst
from roast.test import util

class HTML_Test(util.TestFormattingMixin):
    def test_simple(self):
        src = self.slurp('data', 'simple', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'simple', 'output', 'index.html')

    def test_template(self):
        src = self.slurp('data', 'with-template', 'input', 'index.rst')
        template = self.slurp('data', 'with-template', 'input', '_template.html')
        dom = rst.asDOM(src, template=template)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'with-template', 'output', 'index.html')

    def test_entities(self):
        src = self.slurp('data', 'entities', 'input', 'index.rst')
        dom = rst.asDOM(src)
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'entities', 'output', 'index.html')

    def test_subdir_include(self):
        src = self.slurp('data', 'subdir-include', 'input', 'subdir', 'index.rst')
        dom = rst.asDOM(
            text=src,
            source_path=self.path('data', 'subdir-include', 'input', 'subdir', 'index.rst')
            )
        got = dom.toxml('utf-8')
        self.verify(got, 'data', 'subdir-include', 'output', 'subdir', 'index.html')
