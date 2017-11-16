#!/usr/bin/env python

import os
import sys
import errno

if len(sys.argv) != 3:
    print("WRONG OPTIONS!")
    print("\nUsage:")
    print("\tguten-fixer.py SOURCE_DIR DEST_DIR")
    sys.exit(1)

source_dir = sys.argv[1]
dest_dir = sys.argv[2]

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass

mkdir_p(dest_dir)

for (dirpath, _, filenames) in os.walk(source_dir):
    for filename in filenames:
        with open(os.path.join(dirpath, filename)) as fi:
            para = u""
            with open(os.path.join(dest_dir, filename), 'w') as fo:
                for l in fi:
                    s = l.strip()
                    if len(s) > 0:
                        para = para + s
                    else:
                        fo.write("{0}\n".format(para))
                        para = u""

