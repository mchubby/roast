from docutils.parsers import rst
from docutils import nodes

def blockquote(name, arguments, options, content, lineno,
               content_offset, block_text, state, state_machine):
    q = nodes.block_quote('')

    for text in content:
        # TODO use nested_parse to allow rst markup inside of the
        # blockquote
        q += nodes.Text(text)

    if options.get('author'):
        addr = nodes.Element()
        if options.get('cite'):
            addr += nodes.raw('', '<a href="', format='html')
            addr += nodes.Text(options.get('cite'))
            addr += nodes.raw('', '">', format='html')
        addr += nodes.Text(options['author'])
        if options.get('cite'):
            addr += nodes.raw('', '</a>', format='html')
        q += nodes.raw('', '<address>', format='html')
        q += addr.children
        q += nodes.raw('', '</address>', format='html')

    return [q]
blockquote.arguments = (0, 0, True)
blockquote.options = dict(cite=rst.directives.uri,
                          author=str,
                          )
blockquote.content = True

def install():
    rst.directives.register_directive('blockquote', blockquote)
