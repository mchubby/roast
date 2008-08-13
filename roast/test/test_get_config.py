from nose.tools import (
    eq_ as eq,
    )

from cStringIO import StringIO

from roast import (
    ordered_config_parser,
    get_config,
    )

def test_example():
    cfg = ordered_config_parser.OrderedRawConfigParser()
    cfg.readfp(StringIO("""\
[foo]
# i am here to trigger bugs

[input *.rst]
action = rst
s5-theme-url = /s5-themes/default

[input *.jpg]
action = copy

#TODO
# # this should not match foo/baz.jpg
# [file /*.jpg]
# action = frob

# overrides!
#TODO
# [file /foo/index.rst]
[input foo/index.rst]
s5-theme-url = /s5-themes/foo
"""))

    got = get_config.get_config(cfg, 'input', 'bar.rst')
    eq(got, {'action': 'rst', 's5-theme-url': '/s5-themes/default'})

    got = get_config.get_config(cfg, 'input', 'foo/bar.rst')
    eq(got, {'action': 'rst', 's5-theme-url': '/s5-themes/default'})

    got = get_config.get_config(cfg, 'input', 'foo/index.rst')
    eq(got, {'action': 'rst', 's5-theme-url': '/s5-themes/foo'})

    got = get_config.get_config(cfg, 'input', 'foo/baz.jpg')
    eq(got, {'action': 'copy'})

#TODO
#     got = get_config.get_config(cfg, 'toplevel.jpg')
#     eq(got, {'action': 'frob'})

    got = get_config.get_config(cfg, 'input', 'does-not-match.quux')
    eq(got, None)
