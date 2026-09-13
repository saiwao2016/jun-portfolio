#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信表情包作品图生成器
素材：work-pages/<id>/shots/stickers/*.png（原始 120×120）+ qr.png
产出：portfolio-site/assets/works/<id>/01.png 全套表情总览
      02.png 细节放大（2×2）
      03.png 微信表情商店二维码卡
      以及 work-pages/<id>/shots/cover_src.png（4×2 网格，供 gen_covers.py 出封面）

版式沿用站点既有约定：暖白纸感底 · 细描边卡片 · 无花哨渐变。
"""
import sys, shutil
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path('/Users/jamchou/WorkBuddy/2026-09-07-10-36-15')
WP = ROOT / 'work-pages'
SITE = ROOT / 'portfolio-site'
OUT = SITE / 'assets' / 'works'
TMP = SITE / '_tmp' / 'emoji'

# id / 中文名 / 作者 / 贴纸数 / 强调色
PACKS = [
    dict(id='ip-emoji-shiliu',   name='石榴妹萌萌',   artist='怪物饲养员', accent='#CC1204'),
    dict(id='ip-emoji-shishizi', name='狮狮子',       artist='怪物饲养员', accent='#C8843A'),
    dict(id='ip-emoji-niuniuzi', name='牛牛子',       artist='怪物饲养员', accent='#A9713F'),
    dict(id='ip-emoji-tutuzi',   name='兔兔子',       artist='怪物饲养员', accent='#E9B93E'),
    dict(id='ip-emoji-pilitu',   name='一只霹雳兔',   artist='怪物饲养员', accent='#D93A2B'),
    dict(id='ip-emoji-huahua',   name='虎阿虎阿',     artist='怪物饲养员', accent='#E8892F'),
]

TILE = '#f6f4f1'
INK  = '#111111'
SUB  = '#8f8f8f'

HTML = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:__W__px; height:__H__px; overflow:hidden; }
  body { font-family:'Inter','PingFang SC','Hiragino Sans GB','Microsoft YaHei',-apple-system,sans-serif;
         background:#ffffff; color:__INK__; -webkit-font-smoothing:antialiased;
         display:flex; flex-direction:column; }
  .head { height:112px; flex:none; padding:0 56px; display:flex; align-items:center; justify-content:space-between; }
  .eyebrow { font-size:16px; letter-spacing:.3em; color:__SUB__; font-weight:500; }
  .count { font-size:16px; letter-spacing:.18em; color:__SUB__; font-variant-numeric:tabular-nums; }
  .count b { color:__INK__; font-weight:600; }
  .grid { flex:1; padding:0 56px 56px; display:grid; }
  .cell { background:__TILE__; border-radius:22px; display:flex; align-items:center; justify-content:center; overflow:hidden; }
  .cell img { display:block; }
  /* 二维码卡 */
  .qrwrap { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:34px; padding-bottom:56px; }
  .qrtile { background:__TILE__; border-radius:28px; padding:38px; display:flex; }
  .qrwrap .name { font-size:44px; font-weight:600; letter-spacing:.04em; }
  .qrwrap .hint { font-size:22px; letter-spacing:.16em; color:__SUB__; margin-top:-14px; }
  .qrwrap .meta { font-size:18px; letter-spacing:.14em; color:__SUB__; }
</style></head><body>
<div class="head"><div class="eyebrow">__EYEBROW__</div><div class="count">__RIGHT__</div></div>
__BODY__
</body></html>"""


def ensure(p: Path):
    """沙箱下对已存在目录 mkdir 会抛 EEXIST，先判存在"""
    if not p.exists():
        p.mkdir(parents=True)


def upscale(src: Path, size: int, dest: Path):
    """LANCZOS 预放大一次，供浏览器等比缩用（避免浏览器放大发虚）"""
    im = Image.open(src).convert('RGBA')
    im.resize((size, size), Image.LANCZOS).save(dest)


def prepare(pack, work):
    """把原始素材放大到工作目录，返回 (贴纸列表, 二维码文件)"""
    src = WP / pack['id'] / 'shots' / 'stickers'
    files = sorted(p for p in src.glob('*.png') if p.stem.isdigit())
    big = TMP / pack['id']
    if big.exists():
        shutil.rmtree(big)
    ensure(big)
    out = []
    for f in files:
        d = big / f.name
        upscale(f, 960, d)
        out.append(d)
    qr_src = src / 'qr.png'
    qr = big / 'qr.png'
    if qr_src.exists():
        q = Image.open(qr_src).convert('L')
        q = q.resize((q.width * 3, q.height * 3), Image.NEAREST)  # 整数倍，QR 保持锐利
        q.save(qr)
    return out, (qr if qr_src.exists() else None)


def sheet_grid(pack, work, stickers, cols, cell, gap, width, eyebrow, right, out):
    rows = (len(stickers) + cols - 1) // cols
    height = 112 + rows * cell + (rows - 1) * gap + 56
    inner = cell * 0.78
    cells = ''.join(
        f'<div class="cell"><img src="file://{p}" style="width:{inner:.0f}px;height:{inner:.0f}px"></div>'
        for p in stickers)
    body = (f'<div class="grid" style="grid-template-columns:{("1fr " * cols).strip()};'
            f'grid-auto-rows:{cell}px;gap:{gap}px">{cells}</div>')
    html = (HTML.replace('__W__', str(width)).replace('__H__', str(height))
            .replace('__INK__', INK).replace('__SUB__', SUB).replace('__TILE__', TILE)
            .replace('__EYEBROW__', eyebrow).replace('__RIGHT__', right)
            .replace('__BODY__', body))
    hp = TMP / f'{work}-{out.stem}.html'
    hp.write_text(html, encoding='utf-8')
    return hp, width, height


def sheet_qr(pack, work, qr, width, height, out):
    body = (f'<div class="qrwrap">'
            f'<div class="qrtile"><img src="file://{qr}" style="width:645px;height:645px"></div>'
            f'<div class="name">{pack["name"]}</div>'
            f'<div class="hint">微信扫一扫 · 查看表情</div>'
            f'<div class="meta">微信表情商店 · WECHAT STICKER STORE</div>'
            f'</div>')
    html = (HTML.replace('__W__', str(width)).replace('__H__', str(height))
            .replace('__INK__', INK).replace('__SUB__', SUB).replace('__TILE__', TILE)
            .replace('__EYEBROW__', '微信表情商店 · WECHAT STICKER STORE')
            .replace('__RIGHT__', '')
            .replace('__BODY__', body))
    hp = TMP / f'{work}-{out.stem}.html'
    hp.write_text(html, encoding='utf-8')
    return hp, width, height


def main(only=None):
    ensure(TMP)
    jobs = []
    for pack in PACKS:
        if only and pack['id'] not in only:
            continue
        work = pack['id']
        stickers, qr = prepare(pack, work)
        n = len(stickers)
        dest = OUT / work
        ensure(dest)
        width = 1420
        # 01 全套总览（4 列）
        jobs.append((pack, sheet_grid(
            pack, work, stickers, 4, 300, 36, width,
            '微信表情商店上架作品 · WECHAT STICKER PACK',
            f'<b>{n}</b> 个表情', dest / '01.png')))
        # 02 细节放大（2×2，取前 4 张）
        detail_cell = int((width - 112 - 44) / 2)
        jobs.append((pack, sheet_grid(
            pack, work, stickers[:4], 2, detail_cell, 44, width,
            '表情细节 · DETAIL',
            f'01 — 0{min(4, n)} / {n}', dest / '02.png')))
        # 03 微信表情商店二维码卡
        if qr:
            jobs.append((pack, sheet_qr(pack, work, qr, width, 1180, dest / '03.png')))
        # cover_src：4×2 网格
        cover = WP / work / 'shots' / 'cover_src.png'
        jobs.append((pack, sheet_grid(
            pack, work, stickers[:8], 4, 300, 36, width,
            '', '', cover)))
        print(f'  {work}: {n} 张贴纸' + ('，含二维码卡' if qr else '，无二维码'))

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(device_scale_factor=2)
        last = None
        for pack, (hp, w, h) in jobs:
            if (w, h) != last:
                page.set_viewport_size({'width': w, 'height': h})
                last = (w, h)
            page.goto(hp.as_uri())
            page.wait_for_timeout(420)
            raw = TMP / (hp.stem + '.raw.png')
            page.screenshot(path=str(raw))
            im = Image.open(raw).convert('RGB')
            if im.size != (w * 2, h * 2):
                im = im.resize((w * 2, h * 2), Image.LANCZOS)
            im = im.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
            target = hp.stem.replace(f'{pack["id"]}-', '')
            target = {'01': OUT / pack['id'] / '01.png',
                      '02': OUT / pack['id'] / '02.png',
                      '03': OUT / pack['id'] / '03.png',
                      'cover_src': WP / pack['id'] / 'shots' / 'cover_src.png'}[target]
            im.save(target, optimize=True)
            print(f'    ok {target.relative_to(ROOT)} {im.size[0]}×{im.size[1]} '
                  f'{target.stat().st_size // 1024}KB')
        browser.close()


if __name__ == '__main__':
    main(set(sys.argv[1:]) or None)
