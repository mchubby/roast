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

[file *.rst]
action = rst
s5-theme-url = /s5-themes/default

[file *.jpg]
action = copy

#TODO
# # this should not match foo/baz.jpg
# [file /*.jpg]
# action = frob

# overrides!
#TODO
# [file /foo/index.rst]
[file foo/index.rst]
s5-theme-url = /s5-themes/foo
"""))

    got = get_config.get_config(cfg, 'bar.rst')
    eq(got, {'action': 'rst', 's5-theme-url': '/s5-themes/default'})

    got = get_config.get_config(cfg, 'foo/bar.rst')
    eq(got, {'action': 'rst', 's5-theme-url': '/s5-themes/default'})

    got = get_config.get_config(cfg, 'foo/index.rst')
    eq(got, {'action': 'rst', 's5-theme-url': '/s5-themes/foo'})

    got = get_config.get_config(cfg, 'foo/baz.jpg')
    eq(got, {'action': 'copy'})

#TODO
#     got = get_config.get_config(cfg, 'toplevel.jpg')
#     eq(got, {'action': 'frob'})

    got = get_config.get_config(cfg, 'does-not-match.quux')
    eq(got, None)
