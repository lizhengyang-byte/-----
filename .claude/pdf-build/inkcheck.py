"""Analyze rendered PNG pages: report ink coverage and content bounding box,
so we can confirm pages aren't blank/corrupted and layout looks sane."""
import sys
from PIL import Image
from glob import glob

for path in sorted(glob('png/*.png')):
    im = Image.open(path).convert('L')
    w, h = im.size
    px = im.load()
    dark = 0
    minx, miny, maxx, maxy = w, h, -1, -1
    for y in range(h):
        for x in range(w):
            if px[x, y] < 200:
                dark += 1
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    cov = 100.0 * dark / (w * h)
    print('%s  %dx%d  ink=%.2f%%  bbox=(%d,%d)-(%d,%d)  margins L=%d R=%d T=%d B=%d' % (
        path, w, h, cov,
        minx, miny, maxx, maxy,
        minx, w-1-maxx, miny, h-1-maxy))
