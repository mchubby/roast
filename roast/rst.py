from docutils.core import publish_programmatically
from docutils import io
from docutils.writers import html4css1, s5_html
from xml.dom import minidom
from nevow import rend, loaders, tags, flat

from roast import htmlutil

from roast.directives import python
python.install()

from roast.directives import blockquote
blockquote.install()

from roast.directives import comment
comment.install()

class Template(rend.Fragment):
    def __init__(self, **kw):
        self.title = kw.pop('title')
        super(Template, self).__init__(**kw)

    def render_title(self, ctx, data):
        return ctx.tag.clear()[self.title]

    def render_content(self, ctx, data):
        l = [tags.xml(node.toxml('utf-8')) for node in self.original.childNodes]
        return ctx.tag.clear()[l]

    def __repr__(self):
        return '%s(title=%r)' % (self.__class__.__name__,
                                 self.title)

def asDOM(
    text,
    template=None,
    flavor=None,
    s5_theme_url=None,
    ):
    if flavor is None:
        flavor = 'html'

    settings = dict(
        input_encoding='utf-8',
        output_encoding='utf-8',
        embed_stylesheet=False,
        stylesheet_path=htmlutil.KLUDGE_KILL_CSS,
        generator=False,
        )

    if flavor == 's5':
        writer = s5_html.Writer()
        assert template is None
        assert s5_theme_url is not None
        settings.update(dict(
                theme=None,
                theme_url=s5_theme_url,
                current_slide=True,
                ))
    elif flavor == 'html':
        writer = html4css1.Writer()
    else:
        raise 'Unknown RST flavor: %r' % flavor

    html, publisher = publish_programmatically(
        source_class=io.StringInput,
        source=text,
        source_path=None,
        destination_class=io.StringOutput,
        destination=None,
        destination_path=None,
        reader=None,
        reader_name='standalone',
        parser=None,
        parser_name='restructuredtext',
        writer=writer,
        writer_name=None,
        settings=None,
        settings_spec=None,
        settings_overrides=settings,
        config_section=None,
        enable_exit_status=None)

    tree = minidom.parseString(html)
    title = htmlutil.getTitle(tree)
    title = htmlutil.getNodeContentsAsText(title)

    # kill generator meta tag
    htmlutil.killGeneratorMetaTags(tree)

    # kill stylesheet
    htmlutil.killLinkedStylesheet(tree)

    if flavor == 'html':
        body = htmlutil.getOnlyElementByTagName(tree, 'body')

        docs = htmlutil.getElementsByClass(body, 'document')
        if len(docs) == 1:
            body = docs[0]

        # remove the headings rst promoted to top level,
        # the template will take care of that
        for h1 in body.getElementsByTagName('h1'):
            if htmlutil.elementHasClass(h1, 'title'):
                h1.parentNode.removeChild(h1)
                break

        if template is not None:
            template = Template(original=body,
                                docFactory=loaders.xmlstr(template),
                                title=title,
                                )
            html = flat.flatten(template)
            tree = minidom.parseString(html)

    htmlutil.fixXMLTags(tree)
    return tree
