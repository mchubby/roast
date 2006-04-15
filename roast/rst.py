from docutils.core import publish_programmatically
from docutils import io
from docutils.writers import html4css1

def asHTML(text):
    html, publisher = publish_programmatically(
        source_class=io.StringInput,
        source=text,
        source_path=None,
        destination_class=io.StringOutput,
        destination=None,
        destination_path=None,
        reader=None,
        reader_name='standalone',
        parser=None,
        parser_name='restructuredtext',
        writer=html4css1.Writer(),
        writer_name=None,
        settings=None,
        settings_spec=None,
        settings_overrides={'input_encoding': 'utf-8',
                            'output_encoding': 'utf-8',
                            },
        config_section=None,
        enable_exit_status=None)
    return html
