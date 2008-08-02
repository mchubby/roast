import os
from docutils.parsers import rst
from docutils import nodes, utils
from cStringIO import StringIO
from pygments import lexers, formatters, highlight

def sourcecode(
    name, arguments, options, content, lineno,
    content_offset, block_text, state, state_machine,
    ):
    filename = options.get('filename', None)
    if filename is None:
        code = u'\n'.join(content)
    else:
        source = state_machine.input_lines.source(
            lineno - state_machine.input_offset - 1)
        source_dir = os.path.dirname(os.path.abspath(source))
        filename = os.path.normpath(os.path.join(source_dir, filename))
        filename = utils.relative_path(None, filename)
        state.document.settings.record_dependencies.add(filename)
        op = state.document.settings.roast_operation
        inp = op.open_input(filename)
        code = inp.read().decode('utf-8')
        inp.close()

    if arguments:
        (syntax,) = arguments
    else:
        syntax = 'text'
    lexer = lexers.get_lexer_by_name(syntax)
    formatter = formatters.HtmlFormatter()
    html = highlight(
        code=code,
        lexer=lexer,
        formatter=formatter,
        )

    title_text = options.get('title')
    if title_text:
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

sourcecode.arguments = (0, 1, True)
sourcecode.options = dict(
    filename=rst.directives.path,
    title=rst.directives.unchanged,
    )
sourcecode.content = 1

def install():
    rst.directives.register_directive('sourcecode', sourcecode)
