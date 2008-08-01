import os
import subprocess

def format_dot(dot_fp, pdf_fp, png_fp):
    returncode = subprocess.call(
        args=[
            'dot',
            '-Tpdf',
            ],
        stdin=dot_fp,
        stdout=pdf_fp,
        close_fds=True,
        )
    if returncode!=0:
        raise RuntimeError('dot failed with status %d' % returncode)

    # oh wow i'm allowed to read from a fd that was opened for write
    # only? might need to do something else later, like os.tmpfile..
    # actually, this only works because
    # roast.tree.Operation.open_output uses os.tmpfile as its
    # destination, so the write onlyness is only in os.fdopen, not on
    # kernel level.. and it needs to read them itself, so alternative
    # is only really named temp files.
    pdf_fp.seek(0)
    returncode = subprocess.call(
        args=[
            'convert',
            '-resize', '600x600>',
            'pdf:-',
            'png:-',
            ],
        stdin=pdf_fp,
        stdout=png_fp,
        close_fds=True,
        )
    if returncode!=0:
        raise RuntimeError('convert failed with status %d' % returncode)

def process_dot(op):
    base, ext = os.path.splitext(op.path)
    pdf_fp = op.open_output(base+'.pdf')
    png_fp = op.open_output(base+'.png')
    format_dot(
        dot_fp=op.input,
        pdf_fp=pdf_fp,
        png_fp=png_fp,
        )
    pdf_fp.close()
    png_fp.close()
