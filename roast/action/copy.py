import os
import shutil

def process(config, src_root, src_relative, dst_root, navigation):
    src = os.path.join(src_root, src_relative)
    dst = os.path.join(dst_root, src_relative)
    shutil.copyfile(src, dst)
