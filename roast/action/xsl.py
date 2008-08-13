from __future__ import with_statement
from lxml import etree

def process(op, args=None):
    assert args is not None, \
        "XSL action needs one argument: path to XSLT file."

    l = args.split(None, 1)
    assert len(l) == 1
    (xslt_path,) = l

    with op.open_input(xslt_path) as f:
        xslt_doc = etree.parse(f)

    transform = etree.XSLT(xslt_doc)

    doc = etree.parse(op.input)
    result_tree = transform(doc)
    html = etree.tostring(result_tree)

    with op.open_output(op.path) as f:
        try:
            f.write(html)
            f.write('\n')
        finally:
            f.close()
