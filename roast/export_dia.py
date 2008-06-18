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
