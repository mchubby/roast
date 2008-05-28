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
