#!/usr/bin/env python3

r"""Paper Cutter

Installation:

    python3 -m pip install -r requirements.txt

Example usage:
    paper_cutter.py "path/image.png" 8.5 11 --grid=200 --output "path/output"
"""

from itertools import product
from pathlib import Path
from PIL import Image


def main(args):
    border_l = args.border_left or args.border_width or args.border
    border_r = args.border_right or args.border_width or args.border
    border_t = args.border_top or args.border_height or args.border
    border_b = args.border_bottom or args.border_height or args.border

    paper_w = int(args.width * args.grid)
    paper_h = int(args.height * args.grid)

    img = Image.open(args.image)
    iw, ih = img.size

    w = iw - border_l - border_r
    h = ih - border_t - border_b

    grid = product(
        list(range(border_l, w, paper_w)),
        list(range(border_t, h, paper_h)))

    Path(args.output).mkdir(parents=True, exist_ok=True)

    img_stem = Path(args.image).stem
    img_ext = Path(args.image).suffix

    for x, y in grid:
        row = (y - border_t) // paper_h
        col = (x - border_l) // paper_w

        box = (x, y, min(w, x + paper_w), min(h, y + paper_h))

        out = Path(args.output, f'{img_stem}_{row}_{col}{img_ext}')

        img.crop(box).save(out)


if __name__ == '__main__':
    import sys
    # print(sys.argv)
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('image')
    parser.add_argument('width', type=float)
    parser.add_argument('height', type=float)

    parser.add_argument('-s', '--grid', default=1, type=int)

    parser.add_argument('--border', default=0, type=int)
    parser.add_argument('--border_width',   '--bw', default=0, type=int)
    parser.add_argument('--border_height',  '--bh', default=0, type=int)
    parser.add_argument('--border_left',    '--bl', default=0, type=int)
    parser.add_argument('--border_right',   '--br', default=0, type=int)
    parser.add_argument('--border_top',     '--bt', default=0, type=int)
    parser.add_argument('--border_bottom',  '--bb', default=0, type=int)

    parser.add_argument('-o', '--output', required=True)

    args = parser.parse_args(sys.argv[1:])

    main(args)
