#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 macOS Vision 做 OCR，输出图片内文字及其归一化 bbox（用于判断版面结构）"""
import sys, argparse
import Vision
import Quartz
from PIL import Image
from pathlib import Path

def ocr(path):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    buf = img.tobytes()
    src = Quartz.CGDataProviderCreateWithData(None, buf, len(buf), None)
    cs = Quartz.CGColorSpaceCreateDeviceRGB()
    cg = Quartz.CGImageCreate(w, h, 8, 32, w*3, cs,
                              Quartz.kCGImageAlphaNoneSkipLast, src, None, True,
                              Quartz.kCGRenderingIntentDefault)
    handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(cg, None)
    req = Vision.VNRecognizeTextRequest.alloc().init()
    req.setRecognitionLevel_(0)          # accurate
    req.setRecognitionLanguages_(["zh-Hans", "en-US"])
    req.setUsesLanguageCorrection_(True)
    handler.performRequests_error_([req], None)
    out = []
    for obs in req.results():
        txt = obs.topCandidates_(1)[0].string()
        bb = obs.boundingBox()           # normalized, origin bottom-left
        x, y = bb.origin.x, bb.origin.y
        out.append((txt, round(x, 3), round(y, 3), round(bb.size.width, 3), round(bb.size.height, 3)))
    return (w, h), sorted(out, key=lambda t: (-t[2], t[1]))

if __name__ == '__main__':
    for p in sys.argv[1:]:
        (w, h), res = ocr(p)
        print(f'== {Path(p).name}  {w}x{h}')
        for txt, x, y, ww, hh in res:
            print(f'   [{x:.2f},{y:.2f} {ww:.2f}x{hh:.2f}]  {txt}')
