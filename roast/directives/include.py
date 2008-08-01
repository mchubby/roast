import os

from docutils.parsers import rst
from docutils import nodes
from docutils.parsers.rst import languages

class Wrapper(object):
    def __init__(self, wrapped):
        self._wrapped = wrapped
        self.arguments = wrapped.arguments
        self.options = wrapped.options
        self.content = getattr(wrapped, 'content', None)

    def __call__(
        self,
        name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine,
        ):
        assert len(arguments) == 1
        (path,) = arguments

        if path.startswith('<') and  path.endswith('>'):
            # special built-ins
            fullpath = path
        else:
            # TODO better checks..
            assert not path.startswith('/')
            assert not path.startswith('.')
            assert '/.'not in path

            op = state.document.settings.roast_operation
            relative = os.path.join(
                os.path.dirname(op.path),
                path,
                )
            fullpath = op.kludgy_translate_pathname(relative)

            # it must be an absolute path or docutils include
            # directive will join source dirname in front
            fullpath = os.path.abspath(fullpath)

        return self._wrapped(
            name, [fullpath], options, content, lineno,
            content_offset, block_text, state, state_machine,
            )

def install():
    (old_include, messages) = rst.directives.directive(
        'include',
        languages.en,
        None,
        )
    assert messages == [], \
        'Directive "include" registration got errors: %r' % messages
    wrapper = Wrapper(old_include)
    rst.directives.register_directive('include', wrapper)
