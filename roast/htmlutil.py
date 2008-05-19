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

def killGeneratorMetaTags(tree):
    head = getHead(tree)
    for meta in head.getElementsByTagName('meta'):
        name = meta.getAttribute('name')
        if name == 'generator':
            head.removeChild(meta)

KLUDGE_KILL_CSS = '___roast_kludge__kill_this_style.css'
def killLinkedStylesheet(tree):
    head = getHead(tree)
    for meta in head.getElementsByTagName('link'):
        type_ = meta.getAttribute('type')
        if type_ == 'text/css':
            href = meta.getAttribute('href')
            if href == KLUDGE_KILL_CSS:
                head.removeChild(meta)

def fixXMLTags(tree):
    """
    Fix XML-style tags where old-school HTML browsers
    just don't want to see them.

    E.g. this::

	<script ... />

    becomes this::

	<script ...></script>

    or a rought equivalent.

    This is a horrible kludge while I'm waiting for
    lxml 2.0, and lxml.html, to hit stable distros.
    """
    work=list(tree.childNodes)
    while len(work)>0:
        tag = work.pop(0)
        if tag.nodeType == tag.ELEMENT_NODE:
            if not tag.childNodes:
                tag.appendChild(tree.createTextNode(''))
        work[:0] = tag.childNodes
