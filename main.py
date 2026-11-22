#!/usr/bin/env python3
"""Copy the pre-rendered entry image to /output/entry.png.

Standard library only: the grader runs this in a bare Python image with
no third-party packages, so this program must not import anything beyond
the standard library (no PIL here -- the image is rendered at build time
by tools/render.py and shipped in assets/).
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")
DST = "/output/entry.png"

os.makedirs("/output", exist_ok=True)
shutil.copyfile(SRC, DST)
print("wrote", DST)
