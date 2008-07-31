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

def _lookUp(root, relative, target):
    while True:
        path = os.path.join(relative, target)
        if os.path.isfile(os.path.join(root, path)):
            return path
        if not relative:
            break

        relative = os.path.dirname(relative)

def process(config, src_root, src_relative, dst_root, navigation):
    src = os.path.join(src_root, src_relative)
    base, ext = os.path.splitext(src_relative)
    dst = os.path.join(dst_root, base+'.html')

    f = file(src)
    try:
        text = f.read()
    finally:
        f.close()

    kwargs = dict(
        navigation=navigation,
        source_path=src,
        )
    if re.search(
        r'^\.\.\s+include::\s+<s5defs.txt>\s*$',
        text,
        flags=re.MULTILINE,
        ):
        kwargs['flavor'] = 's5'
        try:
            theme = config.get(
                section='file %s' % src_relative,
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
        template = _lookUp(
            root=src_root,
            relative=os.path.dirname(src_relative),
            target='_template.html',
            )
        if template is not None:
            f = file(os.path.join(src_root, template))
            try:
                kwargs['template'] = f.read()
            finally:
                f.close()

    tree = rst.asDOM(text, **kwargs)

    depth = src_relative.count('/')
    _fixLinks(tree, depth)

    html = tree.toxml('utf-8')
    tmp = '%s.tmp' % dst
    f = file(tmp, 'w')
    try:
        f.write(html)
        f.write('\n')
    finally:
        f.close()
    os.rename(tmp, dst)
