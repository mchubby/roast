import os
import subprocess

def export_dia(dia, png):
    tmp = '%s.tmp' % png
    returncode = subprocess.call(
        args=[
            'dia',
            '--filter=png-libart',
            '--export=%s' % tmp,
            '%s' % dia,
            ],
        )
    if returncode!=0:
        raise RuntimeError('dia failed with status %d' % returncode)
    os.rename(tmp, png)

def process(config, src_root, src_relative, dst_root, navigation):
    base, ext = os.path.splitext(src_relative)
    png = os.path.join(dst_root, base+'.png')
    export_dia(
        dia=os.path.join(src_root, src_relative),
        png=png,
        )
