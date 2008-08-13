import os
import subprocess

def export_dia(dia_fp, png_fp):
    # dia insists on outputting a "src -> dst" text to stdout,
    # and subprocess can't pass other fds than stdin/out/err,
    # so we need to jump through hoops

    r, w = os.pipe()

    def prepare():
        os.dup2(w, 100)
        os.close(w)
        os.close(r)

    p = subprocess.Popen(
        args=[
            'dia',
            '--filter=png-libart',
            # this is probably too linux-specific
            '--export=/proc/self/fd/100',
            '/dev/stdin',
            ],
        stdin=dia_fp,
        close_fds=False,
        preexec_fn=prepare,
        )

    os.close(w)

    tmp_fp = os.fdopen(r, 'rb')
    while True:
        data = tmp_fp.read(8192)
        if not data:
            break
        png_fp.write(data)

    returncode = p.wait()
    if returncode!=0:
        raise RuntimeError('dia failed with status %d' % returncode)

def process(op):
    base, ext = os.path.splitext(op.path)
    png_fp = op.open_output(base+'.png')
    export_dia(
        dia_fp=op.input,
        png_fp=png_fp,
        )
    png_fp.close()
