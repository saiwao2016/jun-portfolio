#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""手册样机渲染 v2（参考实拍风格）：
  closed.png — 闭合方册斜置透视（rotateX+rotateZ、脊背、纸页缘、长投影）
  open.png   — 展开跨页平铺（中缝、页缘弧度、柔和投影）
输出 work-pages/<proj>/shots/{closed,open}.png (1600x1100@2x)
"""
from PIL import Image
from playwright.sync_api import sync_playwright
from pathlib import Path

ROOT = Path('/Users/jamchou/WorkBuddy/2026-09-07-10-36-15/work-pages')
TMP = ROOT / '_tmp/mockups'; TMP.mkdir(parents=True, exist_ok=True)

CLOSED_TPL = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1600px; height:1100px; overflow:hidden; }
  body { background:radial-gradient(120% 90% at 42% 30%, #f7f6f4 0%, #efeceb 55%, #e3e1dc 100%);
         font-family:-apple-system,sans-serif; }
  .scene { position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
           perspective:2600px; perspective-origin:50% 40%; }
  .stage { position:relative; transform:rotateX(56deg) rotateZ(-38deg); transform-style:preserve-3d; }
  .book { position:relative; width:560px; height:560px; transform-style:preserve-3d; }
  /* 封面 */
  .front { position:absolute; inset:0; transform:translateZ(15px);
           box-shadow: 2px 4px 10px rgba(25,22,30,.18); }
  .front img { width:100%; height:100%; object-fit:cover; display:block; }
  /* 左侧脊背 */
  .spine { position:absolute; top:0; bottom:0; left:0; width:22px;
           transform:rotateY(90deg) translateZ(-11px); transform-origin:left center;
           background:linear-gradient(90deg,__SPINE_D__,__SPINE_M__ 55%,__SPINE_L__); }
  /* 前口纸页（右） */
  .fore { position:absolute; top:6px; bottom:6px; right:0; width:26px;
          transform:rotateY(90deg); transform-origin:right center;
          background:repeating-linear-gradient(90deg,#fcfbf8 0 2px,#e7e4dd 2px 4px);
          box-shadow: inset -2px 0 6px rgba(0,0,0,.15); }
  /* 底缘纸页 */
  .bottom { position:absolute; left:0; right:0; bottom:0; height:26px;
            transform:rotateX(-90deg); transform-origin:center bottom;
            background:repeating-linear-gradient(0deg,#fcfbf8 0 2px,#e7e4dd 2px 4px); }
  /* 封底 */
  .back { position:absolute; inset:0; transform:translateZ(-14px); background:#1b1f28; }
  /* 台面长投影 */
  .shadow { position:absolute; left:70px; top:90px; width:760px; height:760px;
            background:radial-gradient(ellipse at 42% 46%, rgba(30,26,38,.34), rgba(30,26,38,0) 62%);
            filter:blur(14px); transform:translateZ(-60px); }
</style></head><body>
  <div class="scene"><div class="stage">
    <div class="shadow"></div>
    <div class="book">
      <div class="back"></div>
      <div class="bottom"></div>
      <div class="fore"></div>
      <div class="spine"></div>
      <div class="front"><img src="file://__COVER__"></div>
    </div>
  </div></div>
</body></html>"""

OPEN_TPL = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1600px; height:1100px; overflow:hidden; }
  body { background:radial-gradient(120% 95% at 45% 32%, #f7f6f4 0%, #eeecea 55%, #e2e0db 100%);
         font-family:-apple-system,sans-serif; }
  .scene { position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
           perspective:2800px; perspective-origin:50% 42%; }
  .book { position:relative; width:1080px; height:540px;
          transform:rotateX(14deg) rotateZ(-6deg); transform-style:preserve-3d;
          filter:drop-shadow(14px 26px 22px rgba(30,26,36,.22)); }
  .pg { position:absolute; top:0; bottom:0; width:540px; overflow:hidden; background:#fff; }
  .pg img { width:100%; height:100%; object-fit:cover; display:block; }
  .pg.l { left:0; border-radius:3px 0 0 3px; }
  .pg.r { right:0; border-radius:0 3px 3px 0; }
  .pg.full { left:0; right:0; width:auto; border-radius:3px; }
  /* 中缝阴影与页弧 */
  .fold { position:absolute; top:0; bottom:0; left:50%; width:120px; transform:translateX(-50%);
          background:linear-gradient(90deg,
            rgba(20,18,24,0) 0%, rgba(20,18,24,.16) 34%, rgba(20,18,24,.30) 50%,
            rgba(20,18,24,.16) 66%, rgba(20,18,24,0) 100%); }
  .pg.l::after { content:''; position:absolute; inset:0;
          background:linear-gradient(90deg, rgba(0,0,0,0) 72%, rgba(24,20,28,.10) 94%, rgba(24,20,28,.22) 100%); }
  .pg.r::after { content:''; position:absolute; inset:0;
          background:linear-gradient(270deg, rgba(0,0,0,0) 72%, rgba(24,20,28,.10) 94%, rgba(24,20,28,.22) 100%); }
  /* 外缘微翘的高光 */
  .edge-l { position:absolute; top:0; bottom:0; left:0; width:8px;
            background:linear-gradient(90deg, rgba(255,255,255,.55), rgba(255,255,255,0)); }
  .edge-r { position:absolute; top:0; bottom:0; right:0; width:8px;
            background:linear-gradient(270deg, rgba(255,255,255,.55), rgba(255,255,255,0)); }
</style></head><body>
  <div class="scene"><div class="book">
    __PAGES__
    <div class="fold"></div>
    <div class="edge-l"></div><div class="edge-r"></div>
  </div></div>
</body></html>"""

# (proj, 封面(方), spine(暗/中/亮), 展开页: ('full', img) 单跨页 或 ('pair', 左, 右))
JOBS = [
  ('liuxin-book', ROOT/'liuxin-book/shots/p01.png', ('#5d1410','#8a231c','#a83a30'),
                  ('full', ROOT/'liuxin-book/shots/p11.png')),
  ('bjjz-book',   ROOT/'bjjz-book/shots/p01.png',   ('#0d1017','#1d2330','#39415a'),
                  ('pair', ROOT/'bjjz-book/shots/p03.png', ROOT/'bjjz-book/shots/p04.png')),
]

def square_crop(src: Path, dst: Path):
    """封面居中裁方（榴心跨页封面取右半作正面）"""
    im = Image.open(src).convert('RGB')
    w, h = im.size
    if 'liuxin' in src.parent.parent.name:
        im = im.crop((w//2, 0, w, h))          # 跨页右半 = 正封面
        w, h = im.size
    side = min(w, h)
    x0 = (w - side)//2; y0 = max(0, (h - side)//3)   # 略偏上取方
    im.crop((x0, y0, x0+side, y0+side)).save(dst)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width':1600,'height':1100}, device_scale_factor=2)
    for proj, cover, spine, spread in JOBS:
        sq = TMP/f'{proj}-sq.png'
        square_crop(cover, sq)
        html = (CLOSED_TPL.replace('__COVER__', str(sq))
                .replace('__SPINE_D__', spine[0]).replace('__SPINE_M__', spine[1])
                .replace('__SPINE_L__', spine[2]))
        hp = TMP/f'{proj}-closed.html'; hp.write_text(html, encoding='utf-8')
        pg.goto(hp.as_uri()); pg.wait_for_timeout(400)
        out = ROOT/proj/'shots/closed.png'
        pg.screenshot(path=str(out)); print(proj, 'closed ok')

        if spread[0] == 'full':
            pages = f'<div class="pg full"><img src="file://{spread[1]}"></div>'
        else:
            pages = (f'<div class="pg l"><img src="file://{spread[1]}"></div>'
                     f'<div class="pg r"><img src="file://{spread[2]}"></div>')
        html = OPEN_TPL.replace('__PAGES__', pages)
        hp = TMP/f'{proj}-open.html'; hp.write_text(html, encoding='utf-8')
        pg.goto(hp.as_uri()); pg.wait_for_timeout(400)
        out = ROOT/proj/'shots/open.png'
        pg.screenshot(path=str(out)); print(proj, 'open ok')
    b.close()
