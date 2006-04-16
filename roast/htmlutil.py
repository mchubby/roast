from StringIO import StringIO
from xml.dom import minidom

def getOnlyElementByTagName(iNode, name):
    elem = iNode.getElementsByTagName(name)
    assert len(elem)==1
    return elem[0]

def getHead(top):
    html = getOnlyElementByTagName(top, 'html')
    head = getOnlyElementByTagName(html, 'head')
    return head

def getTitle(top):
    head = getHead(top)
    title = getOnlyElementByTagName(head, 'title')
    return title

def getNodeContentsAsText(node):
    buf = StringIO()
    for t in node.childNodes:
        assert (isinstance(t, minidom.Text)
                or isinstance(t, minidom.Entity)), \
                "Node contents must be text: %r" % t
        t.writexml(buf)
    s = buf.getvalue()
    return s

def elementHasClass(node, name):
    if hasattr(node, 'getAttribute'):
        classes = node.getAttribute("class")
        if classes and name in classes.split(None):
            return True
    return False

def getElementsByClass(iNode, name):
    """Return list of elements with CSS class name."""
    matches = []
    matches_append = matches.append # faster lookup. don't do this at home
    slice=[iNode]
    while len(slice)>0:
        c = slice.pop(0)
        if elementHasClass(c, name):
            matches_append(c)
        slice[:0] = c.childNodes
    return matches
