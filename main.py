#!/usr/bin/env python3
"""make.fun bounty entry runner (news-image-20261126).

Copies the pre-rendered front-page image into the output directory
expected by the make.fun scoring sandbox. Standard library only --
no PIL, no network, no relative paths.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news-frontpage.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        dst = os.path.join(out_dir, "entry.png")
    else:
        dst = os.path.join(HERE, "output.png")
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    shutil.copyfile(SRC, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
