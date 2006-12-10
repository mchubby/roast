from docutils.parsers import rst
from docutils import nodes
from cStringIO import StringIO
from twisted.python import htmlizer

def python(name, arguments, options, content, lineno,
           content_offset, block_text, state, state_machine):
    inp = StringIO('\n'.join(content).encode('utf-8'))
    outp = StringIO()
    htmlizer.filter(inp, outp, writer=htmlizer.SmallerHTMLWriter)
    html = outp.getvalue()

    if arguments:
        title_text = arguments[0]
        text_nodes, messages = state.inline_text(title_text, lineno)
        title = nodes.caption('', '# ', *text_nodes)
    else:
        messages = []
        title = None

    fig = nodes.figure('')
    fig['classes'].append('py-listing')
    if title is not None:
        fig += title

    fig += nodes.raw('', html, format='html')

    return [fig] + messages

python.arguments = (0, 1, True)
python.content = 1

def install():
    rst.directives.register_directive('python', python)
