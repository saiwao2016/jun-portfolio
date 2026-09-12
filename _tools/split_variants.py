#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""投影切分各 logo 说明图变体 → work-pages/_tmp/variants/（规范命名）"""
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path

DL = Path('/Users/jamchou/Downloads')
WP = Path('/Users/jamchou/WorkBuddy/2026-09-07-10-36-15/work-pages')
OUT = WP / '_tmp' / 'variants'
OUT.mkdir(parents=True, exist_ok=True)

def load(f):
    im = Image.open(f)
    if im.mode == 'CMYK': im = im.convert('RGB')
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3]); im = bg
    return im.convert('RGB')

def segments(profile, thresh, min_len):
    on = profile > thresh
    segs, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        elif not v and s is not None:
            if i - s >= min_len: segs.append((s, i))
            s = None
    if s is not None and len(on) - s >= min_len: segs.append((s, len(on)))
    return segs

def split(im, box, axis, n, thresh=3):
    """box 为比例 (x0,y0,x1,y1)；axis 0=按行切 1=按列切，返回绝对像素 bbox（无外扩，防残影）"""
    W, H = im.size
    x0, y0, x1, y1 = [int(v*d) for v, d in zip(box, (W, H, W, H))]
    a = np.asarray(im.crop((x0, y0, x1, y1)).convert('L')).astype(np.int16)
    prof = (a < 246).sum(axis=1-axis)
    min_len = int(((y1-y0) if axis == 0 else (x1-x0)) * 0.03)
    segs = sorted(sorted(segments(prof.astype(float), thresh, min_len),
                   key=lambda s: s[1]-s[0], reverse=True)[:n])
    out = []
    for s, e in segs:
        out.append((x0, y0+s, x1, y0+e) if axis == 0 else (x0+s, y0, x0+e, y1))
    return out

def trim(c, pad_frac=0.04, bg=246):
    a = np.asarray(c).astype(np.int16)
    ys, xs = np.where(a.mean(2) < bg)
    if len(xs) == 0: return c
    pad = int(max(xs.max()-xs.min(), ys.max()-ys.min()) * pad_frac) + 8
    return c.crop((max(0,xs.min()-pad), max(0,ys.min()-pad),
                   min(c.width,xs.max()+pad), min(c.height,ys.max()+pad)))

def cut(im, bbox, name, pad_frac=0.04, max_side=2200):
    if max(v for v in bbox) <= 1.0:   # 比例转像素
        W, H = im.size
        bbox = (int(bbox[0]*W), int(bbox[1]*H), int(bbox[2]*W), int(bbox[3]*H))
    c = trim(im.crop(bbox), pad_frac)
    if c.width < 10 or c.height < 10:
        print(f'{name:24s} EMPTY'); return None
    c.thumbnail((max_side, max_side), Image.LANCZOS)
    c.save(OUT / f'{name}.png')
    print(f'{name:24s} {c.size}')

for f in OUT.glob('*.png'): f.unlink()

# ---- 榴心社工 ----
im = load(DL/'榴心社工logo设计说明.jpg')
rows = split(im, (0.0, 0.0, 1.0, 0.62), 0, 3)
r1 = split(im, (rows[0][0]/im.width, rows[0][1]/im.height, rows[0][2]/im.width, rows[0][3]/im.height), 1, 3)
cut(im, r1[0], 'liuxin-mark-grad')       # 图形·渐变
cut(im, r1[2], 'liuxin-mark-red')        # 图形·红
cut(im, rows[1], 'liuxin-rev-dark')      # 反白·深灰底（整行）
cut(im, (rows[0][0], rows[2][1], rows[0][2], rows[2][3]), 'liuxin-elem')  # 元素行整行
im2 = load(DL/'榴心社工logo设计说明.jpg')
cut(im2, (0.66, 0.02, 1.0, 0.30), 'liuxin-std')   # 标准组合（红心+红字）

# ---- 我以我言做你眼 ----
big = load(DL/'我以我言做你言logoRGB.jpg')
cut(big, (0.02, 0.02, 0.98, 0.90), 'yan-std')
cut(big, (0.06, 0.04, 0.82, 0.58), 'yan-mark')
spec = load(DL/'我以我言做你言logo说明.jpg')
rows = split(spec, (0.55, 0.02, 1.0, 0.55), 0, 3)
cut(spec, rows[0], 'yan-line-blue')
cut(spec, rows[1], 'yan-line-rev')
cut(spec, rows[2], 'yan-elem')

# ---- 安全健康保护伞 ----
um = load(DL/'安全健康保护伞logo说明.jpg')
cut(um, (0.0, 0.0, 0.43, 0.50), 'umbrella-badge')
rows = split(um, (0.43, 0.0, 1.0, 0.52), 0, 3)
cut(um, rows[0], 'umbrella-line-color')
cut(um, rows[1], 'umbrella-line-gray')
cut(um, rows[2], 'umbrella-line-rev')
r = split(um, (0.0, 0.50, 1.0, 0.75), 0, 1)
if r: cut(um, r[0], 'umbrella-elem')

# ---- 和美乡村 / 幸福食光（用户提供的单图拆 标准组合+图形）----
hex_im = load(DL/'1(1).png')
cut(hex_im, (0.0, 0.0, 1.0, 1.0), 'hexiang-std')
cut(hex_im, (0.0, 0.0, 0.40, 1.0), 'hexiang-mark')
sg_im = load(DL/'1.png')
cut(sg_im, (0.0, 0.0, 1.0, 1.0), 'shiguang-std')
cut(sg_im, (0.0, 0.0, 0.34, 1.0), 'shiguang-mark')

# ---- 预览 ----
files = sorted(OUT.glob('*.png'))
cols_n, cw, ch = 5, 380, 240
rows_n = (len(files)+cols_n-1)//cols_n
s = Image.new('RGB', (cols_n*cw, rows_n*(ch+20)), '#e5e5e5')
dr = ImageDraw.Draw(s)
for i, f in enumerate(files):
    p = Image.open(f).convert('RGB'); p.thumbnail((cw-10, ch-10))
    x, y = (i % cols_n)*cw, (i//cols_n)*(ch+20)
    s.paste(p, (x+5, y+5)); dr.text((x+6, y+ch+2), f.stem, fill='black')
s.save('/Users/jamchou/WorkBuddy/2026-09-07-10-36-15/portfolio-site/_tmp/variants3.png')
print('preview ok,', len(files), 'variants')
