#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 logo 说明图版面：OCR 文字位置 + 彩色/深色连通块位置（均归一化，原点左上）
用法: python analyze.py <image> [...]
"""
import sys
import numpy as np
import Vision
from Foundation import NSURL
from PIL import Image
from scipy import ndimage
from pathlib import Path


def blocks(path, maxside=1800):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    s = min(1.0, maxside / max(W, H))
    sm = im.resize((int(W*s), int(H*s)), Image.LANCZOS)
    a = np.asarray(sm).astype(np.float32) / 255.0
    mx, mn = a.max(2), a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    m = ((sat > 0.30) & (mx > 0.25)) | (mx < 0.30)
    dil = ndimage.binary_dilation(m, structure=np.ones((7, 7)))
    lab, n = ndimage.label(dil)
    h, w = lab.shape
    res = []
    if n:
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        order = np.argsort(sizes)[::-1][:12]
        for k in order:
            ys, xs = np.where(lab == int(k) + 1)
            x0, x1, y0, y1 = xs.min()/w, xs.max()/w, ys.min()/h, ys.max()/h
            sub = a[int(ys.min()):int(ys.max())+1, int(xs.min()):int(xs.max())+1]
            col = (sub.mean(axis=(0, 1)) * 255).astype(int)
            res.append((float(sizes[int(k)])/(h*w), x0, y0, x1-x0, y1-y0,
                        '#%02X%02X%02X' % tuple(col)))
    return res


def ocr(path):
    url = NSURL.fileURLWithPath_(str(path))
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    req = Vision.VNRecognizeTextRequest.alloc().init()
    req.setRecognitionLanguages_(["zh-Hans", "en-US"])
    req.setUsesLanguageCorrection_(True)
    ok, err = handler.performRequests_error_([req], None)
    if not ok:
        return []
    out = []
    for o in req.results():
        bb = o.boundingBox()
        txt = o.topCandidates_(1)[0].string()
        out.append((txt, bb.origin.x, 1 - bb.origin.y - bb.size.height,
                    bb.size.width, bb.size.height))
    return sorted(out, key=lambda t: (t[2], t[1]))


if __name__ == '__main__':
    for p in sys.argv[1:]:
        im = Image.open(p)
        print(f'===== {Path(p).name}  {im.size[0]}x{im.size[1]}')
        for txt, x, y, w, h in ocr(p):
            print(f'  TXT [{x:.2f},{y:.2f} {w:.2f}x{h:.2f}] {txt}')
        for i, (area, x, y, w, h, col) in enumerate(blocks(p)):
            print(f'  BLK#{i} area={area*100:5.1f}% [{x:.2f},{y:.2f} {w:.2f}x{h:.2f}] {col}')
