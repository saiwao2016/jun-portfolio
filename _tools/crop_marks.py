#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 logo 说明原图中裁出「单个标志主体」，并按背景色精修白边。
输出：work-pages/_tmp/marks/<id>.png
"""
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path

HOME = Path('/Users/jamchou/Downloads')
WP = Path('/Users/jamchou/WorkBuddy/2026-09-07-10-36-15/work-pages')
OUT = WP / '_tmp' / 'marks'
OUT.mkdir(parents=True, exist_ok=True)

# id, 源图, 粗框(归一化 x0,y0,x1,y1)
ITEMS = [
    ('logo-liuxin',     HOME/'榴心社工logo设计说明.jpg',      (0.66, 0.03, 0.98, 0.30)),
    ('logo-yan',        HOME/'我以我言做你言logo说明.jpg',    (0.06, 0.14, 0.44, 0.44)),
    ('logo-umbrella',   HOME/'安全健康保护伞logo说明.jpg',    (0.10, 0.05, 0.48, 0.44)),
    ('logo-shiguang',   HOME/'设计说明.png',                  (0.02, 0.08, 0.24, 0.40)),
    ('logo-pingyuan',   HOME/'平原来喜logo.jpg',              (0.28, 0.079, 0.72, 0.145)),
    ('logo-hexiang',    WP/'logo-hexiang/shots/hexiang.png',  (0.02, 0.06, 0.26, 0.40)),
    ('logo-weixiaoxin', WP/'logo-weixiaoxin/shots/wx-spec1-01.png', (0.0, 0.0, 1.0, 0.84)),
]


def trim(im, pad=0.04):
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    h, w, _ = a.shape
    corners = np.vstack([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1],
                         a[h//2, 0], a[h//2, -1]])
    bg = np.median(corners, axis=0)
    d = np.abs(a - bg).sum(2)
    m = d > 34
    if m.mean() < 0.005:
        return im, bg
    ys, xs = np.where(m)
    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()
    bw, bh = x1-x0, y1-y0
    x0 = max(0, int(x0 - bw*pad)); x1 = min(w, int(x1 + bw*pad))
    y0 = max(0, int(y0 - bh*pad)); y1 = min(h, int(y1 + bh*pad))
    return im.crop((x0, y0, x1, y1)), bg


def main():
    for wid, src, box in ITEMS:
        im = Image.open(src).convert('RGB')
        W, H = im.size
        x0, y0, x1, y1 = box
        c = im.crop((int(x0*W), int(y0*H), int(x1*W), int(y1*H)))
        c2, bg = trim(c)
        # 限制最大边，避免超大文件
        c2.save(OUT / f'{wid}.png')
        print(f'{wid:16s} src={src.name} {W}x{H}  crop={c.size} -> trim={c2.size}  bg=#{int(bg[0]):02X}{int(bg[1]):02X}{int(bg[2]):02X}')


if __name__ == '__main__':
    main()
