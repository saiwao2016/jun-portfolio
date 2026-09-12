#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从高清 logo 原件按粗框+自动 trim 切出各变体 → work-pages/_tmp/variants/"""
from PIL import Image
import numpy as np
from pathlib import Path

DL = Path('/Users/jamchou/Downloads')
WP = Path('/Users/jamchou/WorkBuddy/2026-09-07-10-36-15/work-pages')
OUT = WP / '_tmp' / 'variants'
OUT.mkdir(parents=True, exist_ok=True)

def load(f):
    im = Image.open(f)
    if im.mode == 'CMYK':
        im = im.convert('RGB')
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        im = bg
    return im.convert('RGB')

def crop_frac(im, box, pad_frac=0.03, max_side=2200, bg_thresh=246):
    """box=(x0,y0,x1,y1) 比例；框内找 ink bbox 再加 pad"""
    W, H = im.size
    x0, y0, x1, y1 = [int(v * d) for v, d in zip(box, (W, H, W, H))]
    c = im.crop((x0, y0, x1, y1))
    a = np.asarray(c).astype(np.int16)
    ink = a.mean(2) < bg_thresh
    ys, xs = np.where(ink)
    if len(xs) == 0:
        raise RuntimeError('empty crop')
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    bw, bh = bx1 - bx0, by1 - by0
    pad = int(max(bw, bh) * pad_frac) + 8
    c = c.crop((max(0, bx0 - pad), max(0, by0 - pad),
                min(c.width, bx1 + pad), min(c.height, by1 + pad)))
    c.thumbnail((max_side, max_side), Image.LANCZOS)
    return c

LIUXIN = DL / '榴心社工logo设计说明.jpg'
YAN_BIG = DL / '我以我言做你言logoRGB.jpg'
YAN_SPEC = DL / '我以我言做你言logo说明.jpg'
UMB = DL / '安全健康保护伞logo说明.jpg'
HEX = DL / '1(1).png'
SG = DL / '1.png'

JOBS = {
  # ---- 榴心社工：5 变体 + 设计元素 ----
  'liuxin-v1-std':     (LIUXIN, (0.68, 0.02, 1.00, 0.30)),   # 白底标准红
  'liuxin-v2-rev-red': (LIUXIN, (0.00, 0.02, 0.34, 0.30)),   # 红底反白
  'liuxin-v3-gray':    (LIUXIN, (0.34, 0.02, 0.68, 0.30)),   # 单色灰
  'liuxin-v4-rev-dark':(LIUXIN, (0.34, 0.28, 0.68, 0.50)),   # 深灰底反白
  'liuxin-v5-gold':    (LIUXIN, (0.68, 0.28, 1.00, 0.50)),   # 单色金黄
  'liuxin-v6-elem':    (LIUXIN, (0.50, 0.47, 1.00, 0.62)),   # 设计元素拆解
  # ---- 我以我言做你眼 ----
  'yan-v1-std':   (YAN_BIG,  (0.02, 0.02, 0.98, 0.90)),       # 标准组合(图+字)
  'yan-v2-mark':  (YAN_BIG,  (0.06, 0.04, 0.82, 0.58)),       # 图形标志
  'yan-v3-blue':  (YAN_SPEC, (0.60, 0.05, 1.00, 0.14)),       # 横排·标准蓝
  'yan-v4-rev':   (YAN_SPEC, (0.60, 0.14, 1.00, 0.23)),       # 反白·深灰底
  'yan-v5-elem':  (YAN_SPEC, (0.60, 0.24, 1.00, 0.36)),       # 设计元素
  # ---- 安全健康保护伞 ----
  'umbrella-v1-badge': (UMB, (0.02, 0.02, 0.43, 0.52)),       # 主徽标(盾+渐变字)
  'umbrella-v2-color': (UMB, (0.44, 0.02, 1.00, 0.20)),       # 横排·彩色
  'umbrella-v3-gray':  (UMB, (0.44, 0.18, 1.00, 0.34)),       # 横排·单色灰
  'umbrella-v4-rev':   (UMB, (0.44, 0.32, 1.00, 0.50)),       # 反白·深灰底
  'umbrella-v5-elem':  (UMB, (0.02, 0.50, 1.00, 0.70)),       # 设计元素
  # ---- 和美乡村 ----
  'hexiang-v1-std':  (HEX, (0.00, 0.00, 1.00, 1.00)),         # 标准组合
  'hexiang-v2-mark': (HEX, (0.00, 0.00, 0.40, 1.00)),         # 图形标志
  # ---- 幸福食光 ----
  'shiguang-v1-std':  (SG, (0.00, 0.00, 1.00, 1.00)),         # 标准组合
  'shiguang-v2-mark': (SG, (0.00, 0.00, 0.34, 1.00)),         # 图形标志
}

for name, (src, box) in JOBS.items():
    im = load(src)
    c = crop_frac(im, box)
    c.save(OUT / f'{name}.png')
    print(f'{name:22s} {c.size}')
print('done ->', OUT)
