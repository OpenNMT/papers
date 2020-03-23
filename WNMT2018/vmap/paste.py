"""Paste source and target lines with the ||| separator."""

from __future__ import print_function

import sys

with open(sys.argv[1], "rb") as src_file, open(sys.argv[2], "rb") as tgt_file:
    for src, tgt in zip(src_file, tgt_file):
        print("%s ||| %s" % (src.strip(), tgt.strip()))
