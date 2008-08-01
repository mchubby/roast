import errno
import ConfigParser
import os
import re

from roast import rst

def _fixLinks(tree, depth):
    assert depth >= 0
    work = [tree]
    while work:
        node = work.pop(0)
        if hasattr(node, 'getAttribute'):
            for attr in ['href', 'src']:
                path = node.getAttribute(attr)
                if path is not None:
                    if path.startswith('/'):
                        new = '../' * depth + path[1:]
                        if new == '':
                            new = './'
                        node.setAttribute(attr, new)

        work[:0] = node.childNodes

def _lookUp(op, target):
    relative = os.path.dirname(op.path)

    while True:
        path = os.path.join(relative, target)

        try:
            f = op.open_input(path)
        except IOError, e:
            if e.errno == errno.ENOENT:
                pass
            else:
                raise
        else:
            return f

        if not relative:
            break

        relative = os.path.dirname(relative)

def process(op):
    text = op.input.read()

    kwargs = dict(
        navigation=op.navigation,
        source_path=op.path,
        operation=op,
        )
    if re.search(
        r'^\.\.\s+include::\s+<s5defs.txt>\s*$',
        text,
        flags=re.MULTILINE,
        ):
        kwargs['flavor'] = 's5'
        try:
            theme = op.config.get(
                section='file %s' % op.path,
                option='s5-theme-url',
                )
        except (
            ConfigParser.NoSectionError,
            ConfigParser.NoOptionError,
            ):
            theme = '/s5-themes/medium-white' #TODO
        kwargs['s5_theme_url'] = theme
    else:
        kwargs['flavor'] = 'html'
        template = _lookUp(op, '_template.html')
        if template is not None:
            try:
                kwargs['template'] = template.read()
            finally:
                template.close()

    tree = rst.asDOM(text, **kwargs)

    depth = op.path.count('/')
    _fixLinks(tree, depth)

    html = tree.toxml('utf-8')

    base, ext = os.path.splitext(op.path)
    dst = '%s.html' % base
    f = op.open_output(dst)
    try:
        f.write(html)
        f.write('\n')
    finally:
        f.close()
