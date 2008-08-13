import errno
import os

def maybe_mkdir(*a, **kw):
    try:
        os.mkdir(*a, **kw)
    except OSError, e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise

def maybe_mkdir_from(root, path, *a, **kw):
    """
    Create directory, creating any necessary parent directories from
    C{root} onward.
    """
    assert not path.startswith('/')
    segments = path.split(os.path.sep)

    for seg in segments:
        root = os.path.join(root, seg)
        try:
            os.mkdir(root, *a, **kw)
        except OSError, e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise
