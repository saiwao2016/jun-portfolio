#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一封面生成器 — 为 portfolio-site 全部 17 个作品生成同版式封面
版式：暖白纸底 + 分类标签/编号 + 视觉窗（desktop / mobile / brand 三型）+ 标题·年份·品牌色条
输出：portfolio-site/assets/works/<id>/cover.png (1600x1200, PNG-256)
"""
import json, os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path('/Users/jamchou/WorkBuddy/2026-09-07-10-36-15')
WP = ROOT / 'work-pages'
SITE = ROOT / 'portfolio-site'
OUT = SITE / 'assets' / 'works'
TMP = SITE / '_tmp' / 'covers'

# ---- 每个作品一份封面配置（顺序 = data.js 顺序 = 编号） ----
# kind: desktop | mobile | brand
# img: 相对 work-pages 的素材路径列表（desktop/brand 取 1 张，mobile 取 3 张）
CAT_DIG = '数字界面 · DIGITAL INTERFACE'
CAT_IP  = '原创 IP · IP DESIGN'
CAT_GRA = '平面设计 · GRAPHIC DESIGN'
WORKS = [
 dict(id='asq-system',      cat=CAT_DIG, kind='desktop', accent='#3B82D8',
      img=['asq-system/shots/d-home.png'],
      title='ASQ 儿童发育筛查系统', year='2016 — 至今'),
 dict(id='mind-web',        cat=CAT_DIG, kind='desktop', accent='#38B4BE',
      img=['mind-web/shots/d-home.png'],
      title='心智官网 · 心智网校', year='2016 — 至今'),
 dict(id='mind-platform',   cat=CAT_DIG, kind='desktop', accent='#2FA8B2',
      img=['mind-platform/shots/pd-home.png'],
      title='心智测评机构中台', year='2016 — 至今'),
 dict(id='ruizhi-cloud',    cat=CAT_DIG, kind='desktop', accent='#5B8DEF',
      img=['ruizhi-cloud/shots/doc-report.png'],
      title='睿智云 · 发育评估平台', year='2019 — 至今'),
 dict(id='parent-app',      cat=CAT_DIG, kind='mobile', accent='#3AB5BF',
      img=['parent-app/shots/p-home.png','parent-app/shots/p-learn.png','parent-app/shots/p-report.png'],
      title='家长端测评小程序', year='2016 — 至今'),
 dict(id='tuoyou',          cat=CAT_DIG, kind='desktop', accent='#0062FF',
      img=['tuoyou/shots/t-list.png'],
      title='托幼健康测评后台', year='2025 — 至今'),
 dict(id='xiaoe-course',    cat=CAT_DIG, kind='mobile', accent='#019E9D',
      img=['xiaoe-course/shots/m-s1-top.png','xiaoe-course/shots/m-s2-expert.png','xiaoe-course/shots/m-s3-latest.png'],
      title='小鹅通线上店铺', year='2025 — 至今'),
 dict(id='ui-showcase',     cat=CAT_DIG, kind='mobile', accent='#B08560',
      img=['ui-showcase/shots/g-movie-list.png','ui-showcase/shots/a-maybelline.png','ui-showcase/shots/e-mall.png'],
      title='移动端界面合集', year='2019'),
 dict(id='vis-guonin',      cat=CAT_GRA, kind='mockup', accent='#8CC63E',
      img=['vis-guonin/shots/closed.png'],
      title='果您品牌视觉识别', year=''),
 dict(id='vis-xinzhi',      cat=CAT_GRA, kind='brand', accent='#38B4BE',
      img=['vis-xinzhi/shots/xin-p03.png'],
      title='心智视觉形象识别', year='2017'),
 dict(id='logo-weixiaoxin', cat=CAT_GRA, kind='mark', accent='#E60012',
      img=['logo-weixiaoxin/shots/mark.png'],
      title='卫小新品牌标志', year=''),
 dict(id='logo-liuxin',     cat=CAT_GRA, kind='mark', accent='#E8452F',
      img=['logo-liuxin/shots/mark.png'],
      title='榴心社工标志', year=''),
 dict(id='logo-yan',        cat=CAT_GRA, kind='mark', accent='#3B7BF0',
      img=['logo-yan/shots/mark.png'],
      title='我以我言做你眼', year=''),
 dict(id='logo-umbrella',   cat=CAT_GRA, kind='mark', accent='#6C7FD8',
      img=['logo-umbrella/shots/mark.png'],
      title='安全健康保护伞', year=''),
 dict(id='logo-hexiang',    cat=CAT_GRA, kind='mark', accent='#6DB33F',
      img=['logo-hexiang/shots/mark.png'],
      title='和美乡村', year=''),
 dict(id='logo-shiguang',   cat=CAT_GRA, kind='mark', accent='#E8A33D',
      img=['logo-shiguang/shots/mark.png'],
      title='幸福食光', year=''),
 dict(id='logo-pingyuan',   cat=CAT_GRA, kind='mark', accent='#C8102E',
      img=['logo-pingyuan/shots/mark.png'],
      title='平原来喜', year=''),
 dict(id='logo-aline',      cat=CAT_GRA, kind='mark', accent='#415A9B',
      img=['logo-aline/shots/mark.png'],
      title='一根线条 · 标志规范', year=''),
 dict(id='liuxin-book',     cat=CAT_GRA, kind='mockup', accent='#D9472B',
      img=['liuxin-book/shots/closed.png'],
      title='榴心 · 护苗成长计划画册', year=''),
 dict(id='bjjz-book',       cat=CAT_GRA, kind='mockup', accent='#24386B',
      img=['bjjz-book/shots/closed.png'],
      title='北京建筑北方集团 · 企业画册', year=''),
 dict(id='logo-zhuhai-orchestra', cat=CAT_GRA, kind='mark', accent='#F26522',
      img=['logo-zhuhai-orchestra/shots/mark.png'],
      title='珠海少年管弦乐团 · 标志设计', year='2020 — 2021'),
 dict(id='liangbiao-book',     cat=CAT_GRA, kind='mockup', accent='#00A3B4',
      img=['liangbiao-book/shots/closed.png'],
      title='心智 · 量表介绍手册', year=''),
 dict(id='timp-32p',           cat=CAT_GRA, kind='mockup', accent='#66B8C3',
      img=['timp-32p/shots/closed.png'],
      title='TIMP · 32页使用手册', year=''),
 dict(id='timp-84p',           cat=CAT_GRA, kind='mockup', accent='#307E9C',
      img=['timp-84p/shots/closed.png'],
      title='TIMP · 84页核对手册', year=''),
 dict(id='yuangong-book',      cat=CAT_GRA, kind='mockup', accent='#21ABB5',
      img=['yuangong-book/shots/closed.png'],
      title='心智 · 企业员工手册', year=''),
 dict(id='ruizhi-book',        cat=CAT_GRA, kind='mockup', accent='#2B3676',
      img=['ruizhi-book/shots/closed.png'],
      title='睿智云 · 产品手册', year=''),
 dict(id='ip-nino',            cat=CAT_IP,  kind='brand', accent='#FF5949',
      img=['ip-nino/shots/01.png'],
      title='泡泡玛特潮玩设计大赛 · NIÑO', year=''),
 dict(id='ip-pingyuan-v1',     cat=CAT_IP,  kind='brand', accent='#C8102E',
      img=['ip-pingyuan-v1/shots/cover_src.png'],
      title='平原来喜 · 平平 IP 形象 1.0', year=''),
 dict(id='ip-pingyuan-v2',     cat=CAT_IP,  kind='brand', accent='#FF6B5E',
      img=['ip-pingyuan-v2/shots/cover_src.png'],
      title='平原来喜 · 平平 IP 形象 2.0', year=''),
 dict(id='ip-pingyuan-v3',     cat=CAT_IP,  kind='brand', accent='#F05548',
      img=['ip-pingyuan-v3/shots/cover_src.png'],
      title='平原来喜 · 平平 IP 形象 3.0', year=''),
 dict(id='ip-mengjiacun-1',    cat=CAT_IP,  kind='brand', accent='#1A1AAD',
      img=['ip-mengjiacun-1/shots/cover_src.png'],
      title='河北省孟家村 · 乌斯豚 IP 形象', year=''),
 dict(id='ip-mengjiacun-2',    cat=CAT_IP,  kind='brand', accent='#FFD430',
      img=['ip-mengjiacun-2/shots/cover_src.png'],
      title='河北省孟家村 · 金翼使 IP 形象', year=''),
 dict(id='ip-mengjiacun-3',    cat=CAT_IP,  kind='brand', accent='#FF5949',
      img=['ip-mengjiacun-3/shots/cover_src.png'],
      title='河北省孟家村 · 梦芳 IP 形象', year=''),
 dict(id='ip-mengjiacun-4',    cat=CAT_IP,  kind='brand', accent='#5CA7AA',
      img=['ip-mengjiacun-4/shots/cover_src.png'],
      title='河北省孟家村 · 勇安 IP 形象', year=''),
 dict(id='ip-mengjiacun-5',    cat=CAT_IP,  kind='brand', accent='#5784C5',
      img=['ip-mengjiacun-5/shots/cover_src.png'],
      title='河北省孟家村 · 龙吉 IP 形象', year=''),
 dict(id='ip-houcang',         cat=CAT_IP,  kind='brand', accent='#392C61',
      img=['ip-houcang/shots/cover_src.png'],
      title='厚仓美育 · 品牌 IP 与 LOGO 设计', year=''),
 dict(id='ip-shiliu',          cat=CAT_IP,  kind='brand', accent='#CC1204',
      img=['ip-shiliu/shots/cover_src.png'],
      title='石榴妹萌萌 · 公益 IP 形象设计', year=''),
 dict(id='app-shortcut-key',   cat=CAT_DIG, kind='desktop', accent='#EF7979',
      img=['app-shortcut-key/shots/cover_src.jpg'],
      title='Shortcut Key · 快捷键 App 概念设计', year='2018'),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1600px; height:1200px; overflow:hidden; }
  body {
    font-family:'Inter','PingFang SC','Hiragino Sans GB','Microsoft YaHei',-apple-system,sans-serif;
    background:#fafaf8; color:#111111;
    -webkit-font-smoothing:antialiased;
  }
  .stage { position:relative; width:1600px; height:1200px; }
  /* 顶部信息行 */
  .top { position:absolute; left:96px; right:96px; top:152px;
         display:flex; justify-content:space-between; align-items:baseline; }
  .cat  { font-size:15px; letter-spacing:.32em; color:#6b6b6b; font-weight:500; }
  .num  { font-size:15px; letter-spacing:.18em; color:#9a9a9a; font-variant-numeric:tabular-nums; }
  .num b { color:#111; font-weight:600; }
  /* 视觉窗 */
  .frame { position:absolute; left:96px; top:226px; width:1408px; height:692px; }
  .card  { width:100%; height:100%; background:#ffffff; border:1px solid #e8e6e1;
           border-radius:14px; overflow:hidden;
           display:flex; align-items:center; justify-content:center; }
  .card img { max-width:100%; max-height:100%; object-fit:contain; display:block; }
  .card img.mark { max-width:86%; max-height:80%; }
  .phones { width:100%; height:100%; display:flex; align-items:center; justify-content:center; gap:48px; }
  .ph { height:100%; aspect-ratio:300/660; background:#ffffff; border:1px solid #e8e6e1;
        border-radius:22px; overflow:hidden; box-shadow:0 14px 36px rgba(17,17,17,.07); }
  .ph img { width:100%; height:100%; object-fit:cover; object-position:top center; display:block; }
  /* 底部信息行 */
  .bottom { position:absolute; left:96px; right:96px; top:962px;
            display:flex; justify-content:space-between; align-items:center; }
  .t-wrap { display:flex; align-items:center; gap:20px; min-width:0; }
  .bar { width:6px; height:38px; background:__ACCENT__; border-radius:3px; flex:none; }
  .title { font-size:37px; font-weight:600; letter-spacing:.02em; color:#111; white-space:nowrap; }
  .year { font-size:15px; letter-spacing:.14em; color:#9a9a9a; font-variant-numeric:tabular-nums; flex:none; }
</style></head>
<body><div class="stage">
  <div class="top"><div class="cat">__CAT__</div><div class="num"><b>__NO__</b> / 38</div></div>
  <div class="frame">__FRAME__</div>
  <div class="bottom">
    <div class="t-wrap"><div class="bar"></div><div class="title">__TITLE__</div></div>
    <div class="year">__YEAR__</div>
  </div>
</div></body></html>"""

def frame_html(w):
    if w['kind'] == 'mobile':
        imgs = '\n'.join(f'<div class="ph"><img src="file://{WP / p}"></div>' for p in w['img'])
        return f'<div class="phones">{imgs}</div>'
    if w['kind'] == 'mark':
        return f'<div class="card"><img class="mark" src="file://{WP / w["img"][0]}"></div>'
    if w['kind'] == 'mockup':
        return f'<div class="card"><img style="max-width:94%;max-height:94%;border-radius:8px;" src="file://{WP / w["img"][0]}"></div>'
    return f'<div class="card"><img src="file://{WP / w["img"][0]}"></div>'

def main(only=None):
    TMP.mkdir(parents=True, exist_ok=True)
    items = [w for w in WORKS if not only or w['id'] in only]
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width':1600,'height':1200}, device_scale_factor=2)
        for i, w in enumerate(items, 1):
            html = (TEMPLATE
                    .replace('__ACCENT__', w['accent'])
                    .replace('__CAT__', w['cat'])
                    .replace('__NO__', f'{WORKS.index(w)+1:02d}')
                    .replace('__FRAME__', frame_html(w))
                    .replace('__TITLE__', w['title'])
                    .replace('__YEAR__', w['year']))
            hp = TMP / f"{w['id']}.html"; hp.write_text(html, encoding='utf-8')
            page.goto(hp.as_uri())
            page.wait_for_timeout(350)
            raw = TMP / f"{w['id']}.png"
            page.screenshot(path=str(raw))
            im = Image.open(raw).convert('RGB').resize((1600,1200), Image.LANCZOS)
            im = im.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
            dest = OUT / w['id'] / 'cover.png'
            dest.parent.mkdir(parents=True, exist_ok=True)
            im.save(dest, optimize=True)
            print(f"ok {w['id']:16s} -> {dest.name} {dest.stat().st_size//1024}KB")
        browser.close()

if __name__ == '__main__':
    main(set(sys.argv[1:]) or None)
