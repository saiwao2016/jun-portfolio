#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""渲染 logo 拆分内页：
- liuxin/yan/umbrella/hexiang/shiguang：统一变体卡（1920x1080@2x，一卡一变体）
- aline：规范段图直出 + 封面标志 mark.png
输出 → portfolio-site/assets/works/<id>/NN.png (PNG-256)
"""
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
from pathlib import Path
import numpy as np

ROOT = Path('/Users/jamchou/WorkBuddy/2026-09-07-10-36-15')
VAR = ROOT / 'work-pages/_tmp/variants'
OUT = ROOT / 'portfolio-site/assets/works'
TMP = ROOT / 'portfolio-site/_tmp/vpages'
TMP.mkdir(parents=True, exist_ok=True)

# ---------- aline 封面标志：从规范页裁标准标志 ----------
def make_aline_mark():
    import fitz
    doc = fitz.open('/Users/jamchou/Downloads/规范.pdf')
    pm = doc[0].get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(60, 640, 740, 745))
    im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples)
    a = np.asarray(im).astype(np.int16)
    ys, xs = np.where(a.mean(2) < 246)
    pad = 30
    im = im.crop((max(0, xs.min()-pad), max(0, ys.min()-pad),
                  min(im.width, xs.max()+pad), min(im.height, ys.max()+pad)))
    d = ROOT / 'work-pages/logo-aline/shots'
    d.mkdir(parents=True, exist_ok=True)
    im.save(d / 'mark.png')
    # 采样品牌蓝
    arr = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    mx, mn = arr.max(2), arr.min(2)
    sat = (mx - mn) / np.maximum(mx, 1e-6)
    mask = (sat > 0.4) & (mx > 0.3) & (arr[..., 2] > arr[..., 0])
    c = arr[mask].mean(0) if mask.sum() > 50 else np.array([0.25, 0.35, 0.8])
    hexc = '#%02X%02X%02X' % tuple((c * 255).astype(int))
    print('aline mark', im.size, 'accent', hexc)
    return hexc

# ---------- 变体卡 ----------
TPL = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1920px; height:1080px; overflow:hidden; }
  body { font-family:'Inter','PingFang SC','Hiragino Sans GB','Microsoft YaHei',-apple-system,sans-serif;
         background:#fafaf8; color:#111; -webkit-font-smoothing:antialiased; }
  .stage { position:relative; width:1920px; height:1080px; }
  .top { position:absolute; left:110px; right:110px; top:88px;
         display:flex; justify-content:space-between; align-items:baseline; }
  .brand { font-size:17px; letter-spacing:.30em; color:#6b6b6b; font-weight:500; }
  .num { font-size:15px; letter-spacing:.18em; color:#9a9a9a; font-variant-numeric:tabular-nums; }
  .num b { color:#111; font-weight:600; }
  .frame { position:absolute; left:110px; top:158px; width:1700px; height:740px; }
  .card { width:100%; height:100%; background:#fff; border:1px solid #e8e6e1; border-radius:14px;
          display:flex; align-items:center; justify-content:center; overflow:hidden; }
  .card img { max-width:82%; max-height:78%; object-fit:contain; }
  .bottom { position:absolute; left:110px; right:110px; top:948px;
            display:flex; justify-content:space-between; align-items:center; }
  .t-wrap { display:flex; align-items:center; gap:18px; }
  .bar { width:6px; height:34px; background:__ACCENT__; border-radius:3px; }
  .vname { font-size:27px; font-weight:600; letter-spacing:.02em; }
  .ven { font-size:14px; letter-spacing:.14em; color:#9a9a9a; margin-left:6px; }
</style></head><body><div class="stage">
  <div class="top"><div class="brand">__BRAND__</div><div class="num"><b>__I__</b> / __N__</div></div>
  <div class="frame"><div class="card"><img src="file://__IMG__"></div></div>
  <div class="bottom"><div class="t-wrap"><div class="bar"></div>
    <div class="vname">__VNAME__</div><div class="ven">__VEN__</div></div></div>
</div></body></html>"""

# (作品id, accent, 品牌行, [(变体文件, 中文名, 英文名)])
PLAN = [
 ('logo-liuxin', '#E8452F', '榴心社工 · 标志升级', [
    ('liuxin-std',      '标准组合', 'STANDARD LOCKUP'),
    ('liuxin-rev-dark', '反白 · 深灰底', 'REVERSE ON GREY'),
    ('liuxin-mark-grad','图形标志 · 渐变', 'GRADIENT EMBLEM'),
    ('liuxin-mark-red', '图形标志 · 红', 'RED EMBLEM'),
    ('liuxin-elem',     '设计元素', 'DESIGN ELEMENTS'),
 ]),
 ('logo-yan', '#3B7BF0', '我以我言做你眼', [
    ('yan-std',      '标准组合', 'STANDARD LOCKUP'),
    ('yan-mark',     '图形标志', 'EMBLEM'),
    ('yan-line-blue','横排 · 标准蓝', 'HORIZONTAL · BLUE'),
    ('yan-line-rev', '反白 · 深灰底', 'REVERSE ON GREY'),
 ]),
 ('logo-umbrella', '#6C7FD8', '安全健康保护伞', [
    ('umbrella-badge',      '主徽标', 'BADGE'),
    ('umbrella-line-color', '横排 · 彩色', 'HORIZONTAL · COLOUR'),
    ('umbrella-line-gray',  '横排 · 单色', 'HORIZONTAL · GREY'),
    ('umbrella-line-rev',   '反白 · 深灰底', 'REVERSE ON GREY'),
    ('umbrella-elem',       '设计元素', 'DESIGN ELEMENTS'),
 ]),
 ('logo-hexiang', '#6DB33F', '和美乡村', [
    ('hexiang-std',  '标准组合', 'STANDARD LOCKUP'),
    ('hexiang-mark', '图形标志', 'EMBLEM'),
 ]),
 ('logo-shiguang', '#E8A33D', '幸福食光', [
    ('shiguang-std',  '标准组合', 'STANDARD LOCKUP'),
    ('shiguang-mark', '图形标志', 'EMBLEM'),
 ]),
]

def quant_save(im, dest):
    im.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE).save(dest, optimize=True)

def main():
    accent = make_aline_mark()
    # 清掉 5 个 logo 旧 gallery 图（cover 保留）
    for wid, *_ in PLAN:
        for f in (OUT/wid).glob('0*.png'): f.unlink()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width':1920,'height':1080}, device_scale_factor=2)
        for wid, acc, brand, variants in PLAN:
            n = len(variants)
            for i, (vf, vn, ve) in enumerate(variants, 1):
                html = (TPL.replace('__ACCENT__', acc).replace('__BRAND__', brand)
                         .replace('__I__', f'{i:02d}').replace('__N__', f'{n:02d}')
                         .replace('__IMG__', str(VAR/f'{vf}.png'))
                         .replace('__VNAME__', vn).replace('__VEN__', ve))
                hp = TMP/f'{vf}.html'; hp.write_text(html, encoding='utf-8')
                pg.goto(hp.as_uri()); pg.wait_for_timeout(250)
                raw = TMP/f'{vf}.png'; pg.screenshot(path=str(raw))
                im = Image.open(raw).convert('RGB')
                quant_save(im, OUT/wid/f'{i:02d}.png')
                print(f'{wid} {i:02d} <- {vf}')
        b.close()
    # aline 段图直出
    segs = ['aline-std','aline-full','aline-config','aline-grid','aline-color','aline-bg','aline-apps']
    d = OUT/'logo-aline'; d.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(segs, 1):
        im = Image.open(VAR/f'{s}.png').convert('RGB')
        if im.width > 2600:
            im.thumbnail((2600, 99999), Image.LANCZOS)
        quant_save(im, d/f'{i:02d}.png')
        print(f'logo-aline {i:02d} <- {s} {im.size}')
    print('ALL DONE')

if __name__ == '__main__':
    main()
