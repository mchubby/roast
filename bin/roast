#!/usr/bin/python
import errno
import optparse
import os
import sys

from roast import tree

def main():
    parser = optparse.OptionParser()
    parser.set_usage('%prog SOURCE DEST')
    (options, args) = parser.parse_args()

    try:
        (source, dest) = args
    except ValueError:
        parser.error('Expected exactly two arguments.')

    try:
        os.mkdir(dest)
    except OSError, e:
        if e.errno == errno.EEXIST:
            sys.stderr.write(
                '%s: Destination must not exist: %r\n'
                % (parser.get_prog_name(), dest),
                )
        else:
            raise

    t = tree.Tree(path=source)
    t.export(dest)

if __name__ == '__main__':
    main()
