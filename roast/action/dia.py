import os

from roast import export_dia

def process(config, src_root, src_relative, dst_root, navigation):
    base, ext = os.path.splitext(src_relative)
    png = os.path.join(dst_root, base+'.png')
    export_dia.export_dia(
        dia=os.path.join(src_root, src_relative),
        png=png,
        )
