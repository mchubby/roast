from cStringIO import StringIO

from zope.interface import implements

from roast import rst, htmlutil

def get_sections(dom):
    # special case where a lone header is lifted to be
    # subtitle.. didn't really want that to happen, but
    # it's easier to work around.. who has a single
    # navigational element, anyway?
    for elem in htmlutil.getElementsByClass(dom, 'subtitle'):
        title = htmlutil.getNodeContentsAsText(elem)
        idx = elem.parentNode.childNodes.index(elem)
        description = None
        link = '/'+title.lower()

        while elem.parentNode.childNodes[idx+1:]:
            p = elem.parentNode.childNodes[idx+1]
            if p.nodeType == p.TEXT_NODE:
                buf = StringIO()
                p.writexml(buf)
                assert buf.getvalue().strip() == '', \
                    'Subtitle cannot be followed by plain text: %r' % buf.getvalue()
                idx += 1
            else:
                break

        if elem.parentNode.childNodes[idx+1:]:
            p = elem.parentNode.childNodes[idx+1]
            if (p.nodeType == p.ELEMENT_NODE
                and p.nodeName == 'table'):
                assert p.getAttribute('class') == 'docinfo'
                for field in htmlutil.getElementsByClass(p, 'field'):
                    # TODO use classes for locating th and td, just
                    # missing getOnlyElementByClass
                    th = htmlutil.getOnlyElementByTagName(field, 'th')
                    name = htmlutil.getNodeContentsAsText(th)
                    assert name == 'link:'
                    td = htmlutil.getOnlyElementByTagName(field, 'td')
                    link = htmlutil.getNodeContentsAsText(td)
                    if not link.startswith('/'):
                        link = '/'+link

                idx += 1

        while elem.parentNode.childNodes[idx+1:]:
            p = elem.parentNode.childNodes[idx+1]
            if p.nodeType == p.TEXT_NODE:
                buf = StringIO()
                p.writexml(buf)
                assert buf.getvalue().strip() == '', \
                    'Subtitle cannot be followed by plain text: %r' % buf.getvalue()
                idx += 1
            else:
                break

        if elem.parentNode.childNodes[idx+1:]:
            p = elem.parentNode.childNodes[idx+1]
            if (p.nodeType == p.ELEMENT_NODE
                and p.nodeName == 'p'):
                description = htmlutil.getNodeContentsAsText(p)

        yield dict(
            link=link,
            title=title,
            description=description,
            )

    for section in htmlutil.getElementsByClass(dom, 'section'):
        h1 = htmlutil.getOnlyElementByTagName(section, 'h1')
        a = htmlutil.getOnlyElementByTagName(h1, 'a')
        title = htmlutil.getNodeContentsAsText(a)
        link = '/'+title.lower()

        for table in htmlutil.getElementsByClass(section, 'field-list'):
            for field in htmlutil.getElementsByClass(table, 'field'):
                # TODO use classes for locating th and td, just
                # missing getOnlyElementByClass
                th = htmlutil.getOnlyElementByTagName(field, 'th')
                name = htmlutil.getNodeContentsAsText(th)
                assert name == 'link:'
                td = htmlutil.getOnlyElementByTagName(field, 'td')
                link = htmlutil.getNodeContentsAsText(td)
                if not link.startswith('/'):
                    link = '/'+link

        p = section.getElementsByTagName('p')
        if p:
            description = htmlutil.getNodeContentsAsText(p[0])
        else:
            description = None

        yield dict(
            link=link,
            title=title,
            description=description,
            )

def get_navigation(text):
    dom = rst.asDOM(text)
    return get_sections(dom)
