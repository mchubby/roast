import os
import subprocess

def format_dot(dot, pdf, png):
    tmp = '%s.tmp' % pdf
    returncode = subprocess.call(
        args=[
            'dot',
            '-Tpdf',
            '-o', tmp,
            dot,
            ],
        )
    if returncode!=0:
        raise RuntimeError('dot failed with status %d' % returncode)
    os.rename(tmp, pdf)

    tmp = '%s.tmp' % png
    returncode = subprocess.call(
        args=[
            'convert',
            '-resize', '600x600>',
            'pdf:%s' % pdf,
            'png:%s' % tmp,
            ],
        )
    if returncode!=0:
        raise RuntimeError('convert failed with status %d' % returncode)
    os.rename(tmp, png)

def process_dot(config, src_root, src_relative, dst_root, navigation):
    base, ext = os.path.splitext(src_relative)
    pdf = os.path.join(dst_root, base+'.pdf')
    png = os.path.join(dst_root, base+'.png')
    format_dot(
        dot=os.path.join(src_root, src_relative),
        pdf=pdf,
        png=png,
        )
