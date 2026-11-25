#!/usr/bin/env python3
"""Write the 24 November 2026 world-news image to the output directory.

Standard library only. The image is committed in this repository as
entry.png; this program copies it byte for byte to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output).
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    # Create the output directory (and parents) if needed. Never remove,
    # rename, chmod or chown the directory itself: only write the file
    # inside it, so the run is safe on a grader-owned mount.
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, dest)
    print("wrote", dest)


if __name__ == "__main__":
    sys.exit(main())
