#!/usr/bin/env python3
"""Copy entry.png to the output directory and verify it byte-for-byte.

Standard library only. The output directory comes from the
MAKEFUN_OUTPUT_DIR environment variable, or /output when unset.
Exits non-zero if the copied file differs from the source.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png not found in %s" % HERE, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(src, "rb") as f:
        original = f.read()
    with open(dst, "rb") as f:
        copied = f.read()
    if copied != original:
        print("error: copied entry.png differs from %s "
              "(%d vs %d bytes)" % (src, len(copied), len(original)),
              file=sys.stderr)
        return 1
    print("ok: %s (%d bytes, byte-identical)" % (dst, len(copied)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
