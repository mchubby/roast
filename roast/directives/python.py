import os
from docutils.parsers import rst
from docutils import nodes, utils
from cStringIO import StringIO
from twisted.python import htmlizer

def python(name, arguments, options, content, lineno,
           content_offset, block_text, state, state_machine):
    filename = options.get('filename', None)
    if filename is None:
        inp = StringIO('\n'.join(content).encode('utf-8'))
    else:
        source = state_machine.input_lines.source(
            lineno - state_machine.input_offset - 1)
        source_dir = os.path.dirname(os.path.abspath(source))
        filename = os.path.normpath(os.path.join(source_dir, filename))
        filename = utils.relative_path(None, filename)
        state.document.settings.record_dependencies.add(filename)
        inp = file(filename)
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
python.options = dict(filename=rst.directives.path,
                      )
python.content = 1

def install():
    rst.directives.register_directive('python', python)
