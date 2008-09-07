from pygments import formatters

def process_css(op, args=None):
    """
    Generate CSS for source code listings.

    TODO: There needs to be an input file that triggers the execution
    of this action, but the content of the input file is discarded.
    Some day add new rules, in addition to [input ...] and [output
    ...] have [generate ...] too?
    """
    assert args is not None, \
        "pygments-css action needs argument: CSS selector."

    css_selector = args

    formatter = formatters.HtmlFormatter()
    text =  formatter.get_style_defs(arg=css_selector)
    f = op.open_output(op.path)
    f.write(text)
    f.write("\n")
    f.close()
