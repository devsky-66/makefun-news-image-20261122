#!/usr/bin/env python3
"""Entry point for news-image-20261122.

Copies the pre-drawn infographic (entry.png, made by draw_infographic.py)
to $MAKEFUN_OUTPUT_DIR/entry.png. Standard library only, no network.
Every run writes the same bytes.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
