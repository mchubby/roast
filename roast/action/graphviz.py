import os

from roast import format_dot

def process_dot(config, src_root, src_relative, dst_root, navigation):
    base, ext = os.path.splitext(src_relative)
    pdf = os.path.join(dst_root, base+'.pdf')
    png = os.path.join(dst_root, base+'.png')
    format_dot.format_dot(
        dot=os.path.join(src_root, src_relative),
        pdf=pdf,
        png=png,
        )
