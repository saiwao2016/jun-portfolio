#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""平原商场台历专题页生成器 —— 通用逻辑库。

各年份生成器（gen_pingyuan20xx_page.py）只负责：
  (1) 用 make_registrar() 注册三语文案（K 函数），得到 ORDER / VD；
  (2) 提供 config（页面配置 + 结构 spec）；
  (3) 调用本模块的 build() 同时产出 i18n.js 区块与定制 HTML。

i18n.js 注入规则（与 2018/2019 一致）：按 BEGIN/END 标记幂等插入/移除，
每个语言块闭合 `  },` 后插入；HTML 静态兜底 = 中文值，天然零漂移。

data.js / site-data.js 的 ?h= 直接取磁盘实际文件哈希，避免重建后陈旧。
"""

import hashlib
import html
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
I18N = os.path.join(ROOT, "assets/js/i18n.js")
DETAIL = os.path.join(ROOT, "work-detail.html")


def make_registrar():
    keys = set()
    tri = []

    def K(key, zh, es, en):
        if key in keys:
            raise SystemExit(f"重复的 key：{key}")
        keys.add(key)
        tri.append((key, zh, es, en))
        return zh

    return K, tri, keys


def js_str(v):
    """输出为单引号 JS 字符串（与 i18n.js 现有风格一致）。"""
    return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"


def i18n_block(order, vd, lang_index, begin, end):
    # begin 注释由 patch_i18n 统一加在块前，这里不能再包一层（嵌套 /* 会提前闭合注释）
    lines = [""]
    width = max(len(k) for k in order) + 3
    for key in order:
        val = vd[key][lang_index]
        lines.append(f"    {js_str(key).ljust(width)}: {js_str(val)},")
    lines.append("    " + end)
    return "\n".join(lines)


def patch_i18n(begin, end, order, vd, i18n_path=I18N):
    src = open(i18n_path, encoding="utf-8").read()
    lines = src.split("\n")
    close_idx = [i for i, l in enumerate(lines) if re.match(r"^  \}\s*,?\s*$", l)]
    if len(close_idx) != 3:
        raise SystemExit(f"i18n.js 结构异常：预期 3 个语言块闭合，实际 {len(close_idx)}")
    # 先移除旧块（幂等）
    if begin in src:
        src = re.sub(r"[ \t]*" + re.escape(begin) + r".*?" + re.escape(end) + r"\n",
                     "", src, flags=re.S)
        lines = src.split("\n")
        close_idx = [i for i, l in enumerate(lines) if re.match(r"^  \}\s*,?\s*$", l)]
    if len(close_idx) != 3:
        raise SystemExit(f"清理后结构异常：{len(close_idx)}")
    out = list(lines)
    for lang_index, ci in reversed(list(enumerate(close_idx))):
        block = f"    {begin}{i18n_block(order, vd, lang_index, begin, end)}"
        out.insert(ci, block)
    open(i18n_path, "w", encoding="utf-8").write("\n".join(out))
    return len(order)


def e(v):
    """静态兜底文本：与 verify.py 的 _esc 规则一致（只转 &<>）。"""
    return html.escape(v, quote=False)


_BOLD = re.compile(r"\*\*([^*]+)\*\*")


def rich(v):
    """**强调** → <strong>（静态兜底也转真标签，与 i18n 注入一致）。"""
    return _BOLD.sub(r"<strong>\1</strong>", e(v))


def txt(tag, key, vd, cls=None, extra="", indent=""):
    c = f' class="{cls}"' if cls else ""
    return f'{indent}<{tag}{c}{extra} data-i18n="{key}">{rich(vd[key][0])}</{tag}>'


def plate_card(img, key_t, key_s, vd, cap_cls="pc-plate__cap", card_cls="pc-plate", lazy=True):
    alt = e(vd[key_s][0])
    lz = ' loading="lazy"' if lazy else ""
    return f"""        <figure class="{card_cls}" data-pc-card>
          <div class="pc-plate__frame">
            <img src="{img}" alt="{alt}"{lz} data-pc-plate data-i18n-alt="{key_s}">
          </div>
          <figcaption class="{cap_cls}" data-pc-cap>
            <b data-i18n="{key_t}">{e(vd[key_t][0])}</b><span data-i18n="{key_s}">{e(vd[key_s][0])}</span>
          </figcaption>
        </figure>"""


def _head2(num, key_t, vd):
    tag_key = key_t + ".tag"
    return f"""        <div class="pc-head">
          <h2 class="pc-head__title"><span class="pc-head__num">{num}</span><span data-i18n="{key_t}">{e(vd[key_t][0])}</span></h2>
          <span class="pc-head__tag" data-i18n="{tag_key}">{e(vd[tag_key][0])}</span>
        </div>"""


def build_main(config, vd):
    """config 必须含：prefix, img, flat_g1(list[(slug,fname)]), flat_g2, flat_g3,
    overview_rows(list 5 项), features_count(int), months_count(int),
    stats(list[(数字, 键)] 4 项), closing(list[(fname,tkey,skey)]), nav_back_key。
    返回 <main> 内部 HTML 字符串。"""
    p = config["prefix"]
    IMG = config["img"]
    o = []
    A = o.append

    # ---- 子导航 ----
    A('    <nav class="pc-subnav" aria-label="页内导航">')
    A('      <div class="container pc-subnav__inner">')
    for sid, key in [("pc-overview", f"{p}.nav.overview"), ("pc-features", f"{p}.nav.features"),
                     ("pc-mockups", f"{p}.nav.mockups"), ("pc-flat", f"{p}.nav.flat"),
                     ("pc-months", f"{p}.nav.months")]:
        A(f'        <button class="pc-subnav__link" type="button" data-pc-scroll="{sid}"'
          f' data-i18n="{key}">{e(vd[key][0])}</button>')
    nb = config["nav_back_key"]
    A(f'        <a class="pc-subnav__back" href="__WORKS__" data-i18n="{nb}">{e(vd[nb][0])}</a>')
    A("      </div>")
    A("    </nav>")

    # ---- Hero ----
    A('    <header class="pc-hero">')
    A('      <div class="container pc-hero__grid">')
    A("        <div>")
    A(txt("span", f"{p}.hero.kicker", vd, "eyebrow"))
    A(txt("h1", f"{p}.hero.title", vd, "pc-hero__title"))
    A(txt("p", f"{p}.hero.sub", vd, "pc-hero__sub"))
    A(txt("p", f"{p}.hero.desc", vd, "pc-hero__desc"))
    A('          <div class="pc-stats">')
    for n, key in config["stats"]:
        A(f'            <div class="pc-stat"><b>{n}</b>'
          f'<span data-i18n="{key}">{e(vd[key][0])}</span></div>')
    A("          </div>")
    A("        </div>")
    A('        <figure class="pc-hero__figure">')
    A(f'          <img src="{IMG}/mockup-hero.jpg" alt="{e(vd[f"{p}.hero.figcap"][0])}"'
      f' data-i18n-alt="{p}.hero.figcap">')
    A(txt("figcaption", f"{p}.hero.figcap", vd))
    A("        </figure>")
    A("      </div>")
    A("    </header>")

    # ---- 01 项目概览 ----
    A('    <section class="pc-section" id="pc-overview">')
    A('      <div class="container">')
    A(_head2("01", f"{p}.sec.overview", vd))
    A('        <div class="pc-overview">')
    A('          <dl class="pc-info">')
    for key in config["overview_rows"]:
        A(txt("dt", f"{p}.ov.{key}.k", vd))
        A(txt("dd", f"{p}.ov.{key}.v", vd))
    A("          </dl>")
    A('          <div class="pc-overview__copy">')
    A(txt("p", f"{p}.ov.p1", vd, indent="            "))
    A(txt("p", f"{p}.ov.p2", vd, indent="            "))
    A('            <ul class="pc-points">')
    for i in range(1, 5):
        k = f"{p}.ov.point{i}"
        A(f'              <li data-i18n="{k}">{e(vd[k][0])}</li>')
    A("            </ul>")
    A("          </div>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 02 设计亮点 ----
    A('    <section class="pc-section" id="pc-features">')
    A('      <div class="container">')
    A(_head2("02", f"{p}.sec.features", vd))
    A('        <div class="pc-features">')
    for i in range(1, config["features_count"] + 1):
        A('          <article class="pc-feature">')
        A(f'            <span class="pc-feature__no" data-i18n="{p}.ft{i}.no">{e(vd[f"{p}.ft{i}.no"][0])}</span>')
        A(f'            <h3 data-i18n="{p}.ft{i}.t">{e(vd[f"{p}.ft{i}.t"][0])}</h3>')
        A(f'            <p data-i18n="{p}.ft{i}.p">{e(vd[f"{p}.ft{i}.p"][0])}</p>')
        A("          </article>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 03 样机 ----
    A('    <section class="pc-section" id="pc-mockups">')
    A('      <div class="container">')
    A(_head2("03", f"{p}.sec.mockups", vd))
    A('        <div class="pc-mockups">')
    for img, key in [("mockup-spread.jpg", f"{p}.mk1.cap"), ("mockup-hero.jpg", f"{p}.mk2.cap")]:
        A('          <figure class="pc-mockup">')
        A(f'            <img src="{IMG}/{img}" alt="{e(vd[key][0])}" loading="lazy" data-i18n-alt="{key}">')
        A(txt("figcaption", key, vd))
        A("          </figure>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 04 平铺图 ----
    A('    <section class="pc-section" id="pc-flat">')
    A('      <div class="container">')
    A(_head2("04", f"{p}.sec.flat", vd))
    A('        <div class="pc-flat" data-pc-plates>')
    groups = [
        (f"{p}.fg1", config["flat_g1"]),
        (f"{p}.fg2", config["flat_g2"]),
        (f"{p}.fg3", config["flat_g3"]),
    ]
    for gkey, items in groups:
        A('          <div class="pc-flat__group">')
        A(f'            <div class="pc-flat__sub"><h3 data-i18n="{gkey}.t">{e(vd[gkey + ".t"][0])}</h3>'
          f'<span data-i18n="{gkey}.n">{e(vd[gkey + ".n"][0])}</span></div>')
        A('            <div class="pc-grid">')
        for key_slug, fname in items:
            A(plate_card(f"{IMG}/{fname}.jpg", f"{p}.pl.{key_slug}.t", f"{p}.pl.{key_slug}.s", vd))
        A("            </div>")
        A("          </div>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 05 逐月作品 ----
    A('    <section class="pc-section" id="pc-months">')
    A('      <div class="container">')
    A(_head2("05", f"{p}.sec.months", vd))
    for i in range(1, config["months_count"] + 1):
        A('        <div class="pc-month">')
        A('          <div class="pc-month__head">')
        A(f'            <span class="pc-month__no">{i:02d}</span>')
        A(txt("h3", f"{p}.m{i}.name", vd, "pc-month__name"))
        A(txt("div", f"{p}.m{i}.en", vd, "pc-month__en"))
        A(txt("p", f"{p}.m{i}.desc", vd, "pc-month__desc"))
        A("          </div>")
        A('          <div class="pc-month__pages">')
        A(plate_card(f"{IMG}/ill-{i:02d}.jpg", f"{p}.m{i}.ill.t", f"{p}.m{i}.ill.s", vd))
        A(plate_card(f"{IMG}/cal-{i:02d}.jpg", f"{p}.m{i}.cal.t", f"{p}.m{i}.cal.s", vd))
        A("          </div>")
        A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 06 封底 · 尾声 ----
    A('    <section class="pc-section" id="pc-closing">')
    A('      <div class="container">')
    A(_head2("06", f"{p}.sec.closing", vd))
    A('        <div class="pc-closing">')
    for fname, tkey, skey in config["closing"]:
        A(plate_card(f"{IMG}/{fname}.jpg", tkey, skey, vd))
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 上下篇导航 + 页脚说明 ----
    A('    <div class="container">')
    A('      <nav class="work-nav" data-pc-worknav>')
    A('        <a data-pc-prev href="__WORKS__">←</a>')
    A(f'        <a href="__WORKS__" data-i18n="{config["nav_back_key"]}">{e(vd[config["nav_back_key"]][0])}</a>')
    A('        <a data-pc-next href="__WORKS__">→</a>')
    A("      </nav>")
    A('      <div class="pc-outer">')
    A(txt("p", f"{p}.footer.note", vd))
    A(txt("button", f"{p}.backtop", vd, "pc-backtop", ' type="button" data-pc-backtop'))
    A("      </div>")
    A("    </div>")
    return "\n".join(o)


def _hash_of(rel):
    p = os.path.join(ROOT, rel)
    return hashlib.md5(open(p, "rb").read()).hexdigest()[:8]


def build_html(config, vd):
    """导航与页脚从 work-detail.html 原样抽取复用；资源查询串跟随。"""
    detail = open(DETAIL, encoding="utf-8").read()
    nav = re.search(r"  <nav class=\"nav\">.*?\n  </nav>", detail, re.S).group(0)
    footer = re.search(r"  <footer class=\"footer\">.*?\n  </footer>", detail, re.S).group(0)
    ver = re.search(r"main\.css\?v(\d+)", detail)
    if not ver:
        raise SystemExit("未能从 work-detail.html 取到资源版本号")
    v = "v" + ver.group(1)
    body = build_main(config, vd).replace("__WORKS__", f"works.html?{v}")
    p = config["prefix"]
    dh = "h=" + _hash_of("assets/js/data.js")
    sh = "h=" + _hash_of("assets/js/site-data.js")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Cache-Control" content="no-cache">
  <meta http-equiv="Pragma" content="no-cache">
  <script>document.documentElement.className += " js";</script>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#fafaf8">
  <meta name="description" content="{e(vd[f'{p}.meta.desc'][0])}" data-i18n-content="{p}.meta.desc">
  <title data-i18n="{p}.meta.title">{e(vd[f'{p}.meta.title'][0])}</title>
  <link rel="icon" type="image/svg+xml" href="assets/images/favicon.svg">
  <link rel="stylesheet" href="assets/css/main.css?{v}">
  <link rel="stylesheet" href="assets/css/work-pingyuan.css?{v}">
</head>
<body data-lang="zh">

{nav}

  <main class="pc" data-work-id="{config['work_id']}">

{body}

  </main>

{footer}

  <script src="assets/js/i18n.js?{v}"></script>
  <script src="assets/js/data.js?{dh}"></script>
  <script src="assets/js/site-data.js?{sh}"></script>
  <script src="assets/js/main.js?{v}"></script>
</body>
</html>
"""


def build(config, order, vd):
    """一键：写 i18n.js 区块 + 生成 HTML。返回 (i18n 键数, html 路径)。"""
    n = patch_i18n(config["begin"], config["end"], order, vd)
    out = os.path.join(ROOT, config["out_html"])
    open(out, "w", encoding="utf-8").write(build_html(config, vd))
    return n, out
