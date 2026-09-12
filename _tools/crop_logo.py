#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 logo 说明图里切出「标志主体」
方法：高饱和/深色像素做掩膜 → 膨胀合并 → 最大连通块 → 外扩裁切
输出：work-pages/_tmp/logo_crops/<id>.png
"""
import numpy as np
from PIL import Image
from scipy import ndimage
from pathlib import Path

WP = Path('/Users/jamchou/WorkBuddy/2026-09-07-10-36-15/work-pages')
OUT = WP / '_tmp' / 'logo_crops'
OUT.mkdir(parents=True, exist_ok=True)

ITEMS = [
    ('logo-liuxin',     'logo-liuxin/shots/liuxin.png'),
    ('logo-yan',        'logo-yan/shots/yan.png'),
    ('logo-umbrella',   'logo-umbrella/shots/umbrella.png'),
    ('logo-hexiang',    'logo-hexiang/shots/hexiang.png'),
    ('logo-shiguang',   'logo-shiguang/shots/shiguang.png'),
    ('logo-pingyuan',   'logo-pingyuan/shots/lyx-01.png'),
    ('logo-weixiaoxin', 'logo-weixiaoxin/shots/wx-spec1-01.png'),
]

def mask_of(im):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(2), a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    val = mx
    m = (sat > 0.30) & (val > 0.25)          # 彩色标志
    m |= (val < 0.30)                         # 深色/黑色部分
    return m

def main():
    for wid, rel in ITEMS:
        src = WP / rel
        im = Image.open(src).convert('RGB')
        W, H = im.size
        scale = min(1.0, 700 / max(W, H))
        sm = im.resize((max(1, int(W*scale)), max(1, int(H*scale))), Image.LANCZOS)
        m = mask_of(sm)
        dil = ndimage.binary_dilation(m, structure=np.ones((9, 9)))
        lab, n = ndimage.label(dil)
        if n == 0:
            print(f'{wid}: no mask'); continue
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n+1))
        k = int(np.argmax(sizes)) + 1
        ys, xs = np.where(lab == k)
        # 回到原图坐标
        inv = 1.0 / scale
        x0, x1 = xs.min()*inv, xs.max()*inv
        y0, y1 = ys.min()*inv, ys.max()*inv
        bw, bh = x1-x0, y1-y0
        pad = 0.06
        x0 = max(0, x0 - bw*pad); x1 = min(W, x1 + bw*pad)
        y0 = max(0, y0 - bh*pad); y1 = min(H, y1 + bh*pad)
        crop = im.crop((int(x0), int(y0), int(x1), int(y1)))
        crop.save(OUT / f'{wid}.png')
        print(f'{wid:16s} src={W}x{H}  blocks={n}  bbox=({x0/W:.2f},{y0/H:.2f})-({x1/W:.2f},{y1/H:.2f})  crop={crop.size}')

if __name__ == '__main__':
    main()
