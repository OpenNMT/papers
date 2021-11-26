"""Filter lines when either the source or the target have no content."""

import sys
import os

src_path = sys.argv[1]
tgt_path = sys.argv[2]
out_dir = sys.argv[3]

src_path_out = os.path.join(out_dir, os.path.basename(src_path))
tgt_path_out = os.path.join(out_dir, os.path.basename(tgt_path))

with open(src_path) as src_in, \
     open(tgt_path) as tgt_in, \
     open(src_path_out, "w") as src_out, \
     open(tgt_path_out, "w") as tgt_out:
    for src, tgt in zip(src_in, tgt_in):
        if not src.strip() or not tgt.strip():
            continue
        src_out.write(src)
        tgt_out.write(tgt)
