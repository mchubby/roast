from docutils.parsers import rst

def comment(name, arguments, options, content, lineno,
            content_offset, block_text, state, state_machine):
    pass
comment.content = 1

def install():
    rst.directives.register_directive('comment', comment)
