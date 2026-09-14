#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三语全站回归验证。

覆盖：8 个页面 × 3 种语言，逐屏滚动触发 reveal，逐步断言。
关键点：
- 浏览器 `loading="lazy"` 的图必须**先滚完**再断言 naturalWidth，
  否则未进入视口的图会被误判成坏图。
- 断言失败要显式列出，不能静默通过。
"""

import io, os, re, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8766"
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screens")
os.makedirs(OUT, exist_ok=True)

PAGES = [
    ("index.html", "01-home"),
    ("works.html", "02-works"),
    ("about.html", "03-about"),
    ("services.html", "04-services"),
    ("skills.html", "05-skills"),
    ("contact.html", "06-contact"),
    ("resume.html", "07-resume"),
    ("work-detail.html?id=asq-system", "08-detail-asq"),
    ("work-pingyuan-calendar.html", "09-pingyuan"),
    ("work-pingyuan2019-calendar.html", "09-pingyuan2019"),
    ("work-pingyuan2020-calendar.html", "09-pingyuan2020"),
    ("work-pingyuan2021-calendar.html", "09-pingyuan2021"),
    ("work-pingyuan2022-calendar.html", "09-pingyuan2022"),
    ("work-pingyuan2023-calendar.html", "09-pingyuan2023"),
    ("work-pingyuan2024-calendar.html", "09-pingyuan2024"),
    ("work-pingyuan2025-calendar.html", "09-pingyuan2025"),
]
LANGS = ["zh", "es", "en"]

fails = []


def scroll_all(pg, step=700):
    h = pg.evaluate("document.body.scrollHeight")
    y = 0
    while y < h:
        pg.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})")
        pg.wait_for_timeout(90)
        y += step
    pg.wait_for_timeout(900)


def check(cond, msg):
    if not cond:
        fails.append(msg)
    return cond


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-proxy-server"])

    for lang in LANGS:
        print(f"\n{'='*62}\n  语言：{lang.upper()}\n{'='*62}")
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append("PAGEERROR: " + str(e)))
        pg.on("console", lambda m: errs.append(f"[{m.type}] {m.text}") if m.type == "error" else None)

        # 先写语言偏好
        pg.goto(f"{BASE}/index.html", wait_until="domcontentloaded")
        pg.evaluate(f"localStorage.setItem('jun.lang','{lang}')")

        for path, label in PAGES:
            errs.clear()
            pg.goto(f"{BASE}/{path}", wait_until="networkidle", timeout=30000)
            scroll_all(pg)
            pg.evaluate("window.scrollTo({top:0,behavior:'instant'})")
            pg.wait_for_timeout(250)

            n_cards   = pg.locator(".work-card").count()
            # 注意：灯箱的 <img> 初始没有 src，必须排除，否则会被误判成坏图
            broken    = pg.evaluate(
                "()=>[...document.querySelectorAll('img')]"
                ".filter(i=>i.getAttribute('src') && (!i.complete||i.naturalWidth===0)).length")
            revealed  = pg.evaluate("document.querySelectorAll('.reveal.is-in').length")
            total_rev = pg.evaluate("document.querySelectorAll('.reveal').length")
            active    = pg.evaluate("()=>[...document.querySelectorAll('.lang-switch__opt.is-active')].map(e=>e.dataset.lang)")
            overflow  = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            h1        = (pg.locator("h1").first.inner_text() if pg.locator("h1").count() else "").replace("\n", " ")
            html_lang = pg.evaluate("document.documentElement.lang")
            # 词典缺词检查：HTML 里声明了 data-i18n 但当前语言没有对应词条时，
            # 页面会静默回退到 HTML 里的硬编码默认值（可能是过期的占位文案）。
            missing   = pg.evaluate(
                "lang=>{const D=window.I18N[lang]||{};"
                "return [...document.querySelectorAll('[data-i18n]')]"
                ".map(e=>e.getAttribute('data-i18n')).filter(k=>!(k in D));}", lang)

            ok = True
            ok &= check(not errs, f"[{lang}/{label}] JS 错误 {len(errs)}: {errs[:2]}")
            ok &= check(broken == 0, f"[{lang}/{label}] 未加载图片 {broken} 张")
            ok &= check(total_rev == 0 or revealed == total_rev, f"[{lang}/{label}] reveal {revealed}/{total_rev}")
            ok &= check(active == [lang], f"[{lang}/{label}] 切换器激活态 {active} ≠ [{lang}]")
            ok &= check(overflow <= 1, f"[{lang}/{label}] 横向溢出 {overflow}px")
            ok &= check(not missing, f"[{lang}/{label}] i18n 缺词 {len(missing)}: {missing[:5]}")

            pg.screenshot(path=os.path.join(OUT, f"{label}-{lang}.png"), full_page=True)
            flag = "✓" if ok else "✗"
            print(f"  {flag} {label:16s} cards={n_cards:2d} img_broken={broken} "
                  f"reveal={revealed}/{total_rev} lang={html_lang} | {h1[:34]}")

        # ---- 语言切换器点击实测 ----
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        for target in ("es", "en", "zh"):
            pg.click(f'.lang-switch__opt[data-lang="{target}"]')
            pg.wait_for_timeout(450)
            got = pg.evaluate("()=>[...document.querySelectorAll('.lang-switch__opt.is-active')].map(e=>e.dataset.lang)[0]")
            hl = pg.evaluate("document.documentElement.lang")
            saved = pg.evaluate("localStorage.getItem('jun.lang')")
            check(got == target, f"[{lang}] 点击 {target} 后激活态 {got}")
            check(hl == {"zh": "zh-CN", "es": "es-ES", "en": "en"}[target],
                  f"[{lang}] 点击 {target} 后 html lang = {hl}")
            check(saved == target, f"[{lang}] 点击 {target} 后 localStorage = {saved}")
        print(f"  ✓ 语言切换器点击实测（es→en→zh，激活态 + html lang + 存储均正确）")

        ctx.close()

    # ================= 功能专项 =================
    print(f"\n{'='*62}\n  功能专项\n{'='*62}")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    pg.goto(f"{BASE}/index.html", wait_until="domcontentloaded")
    pg.evaluate("localStorage.setItem('jun.lang','zh')")

    # 首页精选 = 每个板块一个，共 6 个
    pg.goto(f"{BASE}/index.html", wait_until="networkidle")
    pg.wait_for_timeout(400)
    feat = pg.locator(".work-card").count()
    cats = pg.evaluate("()=>[...new Set([...document.querySelectorAll('.work-card')].map(c=>c.dataset.category))]")
    check(feat == 3, f"首页精选应为 3 个，实际 {feat}")
    check(cats == ["digital", "graphic", "ip"], f"首页板块应为 ['digital','graphic','ip']，实际 {cats}")
    print(f"  ✓ 首页精选 {feat} 个 · 板块 {cats}")

    # 作品集：7 个案例 + 筛选
    pg.goto(f"{BASE}/works.html", wait_until="networkidle")
    pg.wait_for_timeout(500)
    total = pg.locator(".work-card").count()
    exp_total = pg.evaluate("()=>window.WORKS.length")   # 动态取，避免每加一个作品就改脚本
    check(total == exp_total, f"作品集应有 {exp_total} 个案例，实际 {total}")
    print(f"  ✓ 作品集共 {total} 个案例")
    for f in ("digital", "ip", "graphic", "all"):
        pg.click(f'.filter-btn[data-filter="{f}"]')
        pg.wait_for_timeout(220)
        vis = pg.evaluate(
            "()=>[...document.querySelectorAll('.work-card')].filter(c=>c.style.display!=='none').length")
        exp = exp_total if f == "all" else pg.evaluate(
            f"()=>window.WORKS.filter(w=>w.category==='{f}').length")
        check(vis == exp, f"筛选 {f}: 显示 {vis}，应为 {exp}")
        print(f"     筛选 {f:8s} → {vis} 个")
    pg.click('.filter-btn[data-filter="all"]')
    pg.wait_for_timeout(200)
    # i18n 注入会重置内联 style.display，「空提示」必须靠 class 保持隐藏
    empty_hidden = pg.evaluate(
        "()=>getComputedStyle(document.querySelector('[data-empty-msg]')).display === 'none'")
    check(empty_hidden, "「该板块暂无案例」空提示应默认隐藏")
    print("  ✓ 空提示默认隐藏（未被 i18n 注入显示出来）")

    # ASQ 数字产品案例：25 张 PNG 界面图
    pg.goto(f"{BASE}/work-detail.html?id=asq-system", wait_until="networkidle")
    scroll_all(pg)
    aimg = pg.locator(".work-gallery [data-lb]").count()
    abro = pg.evaluate("()=>[...document.querySelectorAll('.work-gallery img')].filter(i=>!i.complete||i.naturalWidth===0).length")
    check(aimg == 25, f"ASQ 案例图集应有 25 张，实际 {aimg}")
    check(abro == 0, f"ASQ 图集未加载 {abro} 张")
    print(f"  ✓ ASQ 案例图集 {aimg} 张，全部加载（PNG）")

    # 其余 6 个界面类案例：详情页可渲染 + 图集零裂图
    for wid, nimg in [("mind-web", 6), ("mind-platform", 6), ("ruizhi-cloud", 6),
                      ("parent-app", 4), ("tuoyou", 4), ("xiaoe-course", 2),
                      ("ui-showcase", 2), ("vis-guonin", 5), ("vis-xinzhi", 4),
                      ("logo-weixiaoxin", 4), ("logo-liuxin", 5), ("logo-yan", 4),
                      ("logo-umbrella", 5), ("logo-hexiang", 2), ("logo-shiguang", 2),
                      ("logo-pingyuan", 4), ("logo-aline", 8),
                      ("liuxin-book", 5), ("bjjz-book", 5),
                      ("logo-zhuhai-orchestra", 4),
                      ("liangbiao-book", 5), ("timp-32p", 5),
                      ("timp-84p", 5), ("yuangong-book", 5),
                      ("ruizhi-book", 5), ("ip-nino", 4),
                      ("ip-pingyuan-v1", 6), ("ip-pingyuan-v2", 5),
                      ("ip-pingyuan-v3", 7),
                      ("ip-mengjiacun-1", 6), ("ip-mengjiacun-2", 6),
                      ("ip-mengjiacun-3", 6), ("ip-mengjiacun-4", 6),
                      ("ip-mengjiacun-5", 6), ("ip-houcang", 2),
                      ("ip-shiliu", 8), ("app-shortcut-key", 18),
                      ("ip-emoji-shiliu", 3), ("ip-emoji-shishizi", 3),
                      ("ip-emoji-niuniuzi", 3), ("ip-emoji-tutuzi", 3),
                      ("ip-emoji-pilitu", 3), ("ip-emoji-huahua", 3)]:
        pg.goto(f"{BASE}/work-detail.html?id={wid}", wait_until="networkidle")
        scroll_all(pg)
        h1 = pg.locator("h1").first.inner_text().strip()
        gimg = pg.locator(".work-gallery [data-lb]").count()
        bro = pg.evaluate("()=>[...document.querySelectorAll('.work-gallery img')].filter(i=>!i.complete||i.naturalWidth===0).length")
        check(bool(h1) and gimg == nimg and bro == 0,
              f"{wid} 详情页异常：h1=「{h1}」 图 {gimg}/{nimg} 裂图 {bro}")
        print(f"  ✓ {wid:14s} 「{h1[:24]}」图集 {gimg} 张全载")

    # 平原商场台历：定制专题页（work-pingyuan-calendar.html）
    pg.goto(f"{BASE}/work-pingyuan-calendar.html", wait_until="networkidle")
    scroll_all(pg)
    p_sec = pg.locator(".pc-section").count()
    p_mon = pg.locator(".pc-month").count()
    p_plate = pg.locator("[data-pc-plate]").count()
    p_bro = pg.evaluate("()=>[...document.querySelectorAll('.pc img')].filter(i=>!i.complete||i.naturalWidth===0).length")
    check(p_sec == 6, f"台历专题页区块数应为 6，实际 {p_sec}")
    check(p_mon == 12, f"台历专题页逐月应为 12，实际 {p_mon}")
    check(p_bro == 0, f"台历专题页图集未加载 {p_bro} 张（共 {p_plate} 张底板图）")
    print(f"  ✓ 台历专题页：区块 {p_sec} · 逐月 {p_mon} · 底板图 {p_plate} 张全载")

    # 灯箱：按 src 去重后应为 28 项（30 张图集中 2 张样机图 mockup-hero/mockup-spread 为展示样机，不入灯箱）
    pg.locator("[data-pc-plate]").first.click()
    pg.wait_for_timeout(450)
    lb_on = pg.evaluate("document.getElementById('lb')?.classList.contains('is-on')")
    lb_cap = pg.evaluate("document.querySelector('#lb .lb__cap')?.textContent || ''")
    check(lb_on, "台历专题页灯箱未打开")
    check(bool(re.search(r"/\s*28\b", lb_cap or "")), f"台历灯箱去重后应为 28 项，caption={lb_cap!r}")
    print(f"  ✓ 台历灯箱打开：{lb_cap}")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    check(not pg.evaluate("document.getElementById('lb')?.classList.contains('is-on')"), "Esc 未关闭台历灯箱")
    print(f"  ✓ 台历灯箱 Esc 关闭")

    # 语言切换：专题页整体重绘
    for lg in ("es", "en"):
        pg.click(f'.lang-switch__opt[data-lang="{lg}"]')
        pg.wait_for_timeout(500)
        h1 = pg.locator("h1").first.inner_text()
        check(len(h1.strip()) > 2, f"台历专题页 {lg} 标题异常：{h1!r}")
        print(f"    · {lg}: 「{h1[:24]}」")
    pg.click('.lang-switch__opt[data-lang="zh"]')
    pg.wait_for_timeout(400)

    # 平原商场 2019-2025 台历：定制专题页
    for cal_path, cal_year in (
        ("work-pingyuan2019-calendar.html", "2019"),
        ("work-pingyuan2020-calendar.html", "2020"),
        ("work-pingyuan2021-calendar.html", "2021"),
        ("work-pingyuan2022-calendar.html", "2022"),
        ("work-pingyuan2023-calendar.html", "2023"),
        ("work-pingyuan2024-calendar.html", "2024"),
        ("work-pingyuan2025-calendar.html", "2025"),
    ):
        pg.goto(f"{BASE}/{cal_path}", wait_until="networkidle")
        scroll_all(pg)
        pxx_sec = pg.locator(".pc-section").count()
        pxx_mon = pg.locator(".pc-month").count()
        pxx_plate = pg.locator("[data-pc-plate]").count()
        pxx_bro = pg.evaluate("()=>[...document.querySelectorAll('.pc img')].filter(i=>!i.complete||i.naturalWidth===0).length")
        check(pxx_sec == 6, f"{cal_year} 台历专题页区块数应为 6，实际 {pxx_sec}")
        check(pxx_mon == 12, f"{cal_year} 台历专题页逐月应为 12，实际 {pxx_mon}")
        check(pxx_bro == 0, f"{cal_year} 台历专题页图集未加载 {pxx_bro} 张（共 {pxx_plate} 张底板图）")
        print(f"  ✓ {cal_year} 台历专题页：区块 {pxx_sec} · 逐月 {pxx_mon} · 底板图 {pxx_plate} 张全载")

        # 灯箱：按 src 去重后应为 28 项（30 张图集中 2 张样机图 mockup-hero/mockup-spread 为展示样机，不入灯箱）
        pg.locator("[data-pc-plate]").first.click()
        pg.wait_for_timeout(450)
        lbxx_on = pg.evaluate("document.getElementById('lb')?.classList.contains('is-on')")
        lbxx_cap = pg.evaluate("document.querySelector('#lb .lb__cap')?.textContent || ''")
        check(lbxx_on, f"{cal_year} 台历专题页灯箱未打开")
        check(bool(re.search(r"/\s*28\b", lbxx_cap or "")), f"{cal_year} 台历灯箱去重后应为 28 项，caption={lbxx_cap!r}")
        print(f"  ✓ {cal_year} 台历灯箱打开：{lbxx_cap}")
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(300)
        check(not pg.evaluate("document.getElementById('lb')?.classList.contains('is-on')"), f"Esc 未关闭 {cal_year} 台历灯箱")
        print(f"  ✓ {cal_year} 台历灯箱 Esc 关闭")

        # 语言切换：专题页整体重绘
        for lg in ("es", "en"):
            pg.click(f'.lang-switch__opt[data-lang="{lg}"]')
            pg.wait_for_timeout(500)
            h1 = pg.locator("h1").first.inner_text()
            check(len(h1.strip()) > 2, f"{cal_year} 台历专题页 {lg} 标题异常：{h1!r}")
            print(f"    · {lg}: 「{h1[:24]}」")
        pg.click('.lang-switch__opt[data-lang="zh"]')
        pg.wait_for_timeout(400)

    pg.goto(f"{BASE}/work-detail.html?id=asq-system", wait_until="networkidle")
    scroll_all(pg)
    pg.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    pg.wait_for_timeout(200)
    pg.locator(".work-gallery [data-lb]").first.click()
    pg.wait_for_timeout(450)
    lb_on = pg.evaluate("document.getElementById('lb')?.classList.contains('is-on')")
    lb_cap = pg.evaluate("document.querySelector('#lb .lb__cap')?.textContent")
    check(lb_on, "图集灯箱未打开")
    print(f"  ✓ 灯箱打开，页码显示「{lb_cap}」")
    pg.keyboard.press("ArrowRight")
    pg.wait_for_timeout(350)
    lb_cap2 = pg.evaluate("document.querySelector('#lb .lb__cap')?.textContent")
    check(lb_cap2 != lb_cap, "灯箱方向键翻页无效")
    print(f"  ✓ 方向键翻页 → 「{lb_cap2}」")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    check(not pg.evaluate("document.getElementById('lb')?.classList.contains('is-on')"), "Esc 未关闭灯箱")
    print(f"  ✓ Esc 关闭灯箱")

    # 三语切换时详情页整体重绘
    pg.click('.lang-switch__opt[data-lang="es"]')
    pg.wait_for_timeout(600)
    h1_es = pg.locator("h1").first.inner_text()
    check("ASQ" in h1_es or "cribado" in h1_es, f"详情页西语重绘异常: {h1_es}")
    print(f"  ✓ 详情页语言切换重绘 → 「{h1_es}」")

    # 简历页三个 PDF
    pg.goto(f"{BASE}/resume.html", wait_until="networkidle")
    pdfs = pg.evaluate("()=>[...document.querySelectorAll('a[href$=\".pdf\"]')].map(a=>a.getAttribute('href'))")
    check(len(pdfs) == 3, f"简历页应有 3 个 PDF，实际 {len(pdfs)}: {pdfs}")
    print(f"  ✓ 简历页 PDF 下载：{pdfs}")

    # 简历页：window.RESUME 数据驱动（内容可在后台编辑）
    # 注意：上面「详情页语言切换」把语言留在了 es，这里必须先切回 zh 再断言
    pg.click('.lang-switch__opt[data-lang="zh"]')
    pg.wait_for_timeout(450)
    rz = pg.evaluate(
        "()=>window.RESUME?{exp:((window.RESUME.exp||{}).items||[]).length,"
        "pdfs:(window.RESUME.pdfs||[]).length,"
        "skills:((window.RESUME.skills||{}).items||[]).length}:null")
    check(rz is not None, "resume-data.js 未加载（简历内容无从后台编辑）")
    if rz:
        check(rz["exp"] == 3 and rz["pdfs"] == 3 and rz["skills"] == 6,
              f"简历数据形状异常：{rz}")
    cards = pg.locator("#resumeBody .resume-card").count()
    check(cards == 5, f"简历卡片应为 5（简介1+经历3+技能1），实际 {cards}")
    hblocks = pg.locator("#resumeBody .h-block").count()
    check(hblocks == 2, f"简历区块标题应为 2（经历/技能），实际 {hblocks}")
    lis = pg.locator("#resumeBody .resume-card ul li").count()
    check(lis == 18, f"简历列表条目应为 18（经历12+技能6），实际 {lis}")
    leftover = pg.evaluate("()=>document.querySelectorAll('#resumeBody [data-i18n]').length")
    check(leftover == 0, f"JS 接管后不应残留 data-i18n 节点，实际 {leftover}")
    rp = pg.locator("#resumeBody .resume-body p").count()
    check(rp >= 1, f"简介正文应有段落，实际 {rp}")
    print(f"  ✓ 简历页数据驱动：卡片 {cards} · 区块 {hblocks} · 列表 {lis} · 简介 {rp} 段")

    # 简历页随语言切换整体重绘
    zh_first = pg.locator("#resumeBody .resume-card ul li").first.inner_text()
    pg.click('.lang-switch__opt[data-lang="es"]')
    pg.wait_for_timeout(500)
    es_title = pg.locator("#resumeBody h1").first.inner_text()
    es_first = pg.locator("#resumeBody .resume-card ul li").first.inner_text()
    es_cards = pg.locator("#resumeBody .resume-card").count()
    check("CV" in es_title or "curr" in es_title.lower(), f"西语简历主标题异常：「{es_title}」")
    check(es_first != zh_first and len(es_first) > 2, f"西语简历未重绘：「{es_first[:30]}」")
    check(es_cards == 5, f"切换语言后卡片数应仍为 5，实际 {es_cards}")
    pg.click('.lang-switch__opt[data-lang="zh"]')
    pg.wait_for_timeout(500)
    zh_title = pg.locator("#resumeBody h1").first.inner_text()
    check(zh_title == "网页版简历", f"切回中文标题异常：「{zh_title}」")
    print(f"  ✓ 简历页语言切换重绘 → ES「{es_title}」/ ZH「{zh_title}」")

    # ---- 后台配套：站点设置注入 / 数据源兜底 / 背景音乐 ----
    pg.goto(f"{BASE}/index.html", wait_until="networkidle")
    sd = pg.evaluate(
        "()=>window.SITE_DATA ? {copy:Object.keys(window.SITE_DATA.copy||{}).length,"
        " social:(window.SITE_DATA.social||[]).length,"
        " mode:((window.SITE_DATA.source||{}).mode||'')} : null")
    check(sd is not None, "site-data.js 未加载（后台主页文案 / 社交链接无从生效）")
    check(sd["social"] >= 3, f"社交入口应 ≥3 个，实际 {sd['social']}")
    check(sd["copy"] >= 20, f"可编辑文案键应 ≥20 条，实际 {sd['copy']}")
    src_mode = pg.evaluate("()=>document.documentElement.getAttribute('data-content-source')")
    check(src_mode == "local", f"未配置远端数据源时应回退 local，实际 {src_mode}")
    print(f"  ✓ 站点设置已加载：文案 {sd['copy']} 键 · 社交 {sd['social']} 个 · 数据源 {src_mode}（兜底生效）")

    mail = pg.evaluate("()=>document.querySelector('[data-social=\"email\"]')?.getAttribute('href')")
    check(bool(mail) and mail.startswith("mailto:"), f"社交邮箱链接未注入：{mail}")
    wx = pg.evaluate("()=>document.querySelector('[data-social=\"wechat\"]')?.getAttribute('href')")
    check(wx in ("#", "", None), f"二维码类型的微信入口不应指向内容页：{wx}")
    print(f"  ✓ 社交链接注入：email={mail} · wechat={wx or '（未配置）'}")

    # 二维码弹层：点击微信入口 → 展示图片 → Esc 关闭
    pg.goto(f"{BASE}/contact.html", wait_until="networkidle", timeout=30000)
    pg.click("[data-social=\"wechat\"]")
    pg.wait_for_timeout(600)
    on = pg.evaluate("()=>document.getElementById('qrOverlay')?.classList.contains('is-on')")
    check(on is True, f"点击微信入口应打开二维码弹层，实际 {on}")
    qsrc = pg.evaluate("()=>document.getElementById('qrImg')?.getAttribute('src')||''")
    check("wechat-qr" in qsrc, f"弹层图片应为微信二维码，实际 {qsrc}")
    qnat = pg.evaluate("()=>{const i=document.getElementById('qrImg');return i?i.naturalWidth:0}")
    check(qnat > 100, f"二维码图片应真实加载，实际宽度 {qnat}")
    qhint = pg.evaluate("()=>document.getElementById('qrHint')?.textContent||''")
    check(len(qhint) > 4, f"弹层应有长按识别提示，实际 {qhint!r}")
    pg.screenshot(path=os.path.join(OUT, "16-wechat-qr.png"), full_page=False)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(400)
    off = pg.evaluate("()=>document.getElementById('qrOverlay')?.classList.contains('is-on')")
    check(off is False, f"Esc 应关闭二维码弹层，实际 {off}")
    print(f"  ✓ 微信二维码弹层：打开 / 图片加载 {qnat}px / 提示「{qhint[:18]}」/ Esc 关闭")

    bgm = pg.evaluate("()=>document.querySelectorAll('.bgm-btn').length")
    check(bgm == 0, f"未配置背景音乐时不应出现播放按钮，实际 {bgm}")
    print("  ✓ 未配置背景音乐 → 无播放按钮")

    # ---- 三语完整性 / 页面标题随语言切换 / 三页文案 / 静态兜底一致性 ----
    pg.goto(f"{BASE}/about.html", wait_until="networkidle")
    pg.click('.lang-switch__opt[data-lang="zh"]')
    pg.wait_for_timeout(400)

    audit = pg.evaluate("""() => {
      const I = window.I18N, langs = ['zh','es','en'], all = new Set();
      // 允许显式留空的键：空值本身就是「该字段不显示」的语义，不是漏翻译。
      // resume.edu.date —— 就读起止年份未提供，页面渲染时该行自然为空。
      const ALLOW_EMPTY = ['resume.edu.date'];
      langs.forEach(l => Object.keys(I[l]||{}).forEach(k => all.add(k)));
      const missing = [], empty = [];
      all.forEach(k => langs.forEach(l => {
        const v = (I[l]||{})[k];
        if (v === undefined) missing.push(l + ':' + k);
        else if (String(v).trim() === '' && ALLOW_EMPTY.indexOf(k) === -1) empty.push(l + ':' + k);
      }));
      return { total: all.size, missing: missing.slice(0, 8), nMissing: missing.length,
               nEmpty: empty.length, empty: empty.slice(0, 8) };
    }""")
    check(audit["nMissing"] == 0, f"三语键不齐（缺 {audit['nMissing']}）：{audit['missing']}")
    check(audit["nEmpty"] == 0, f"三语存在空值（{audit['nEmpty']}）：{audit['empty']}")
    print(f"  ✓ 三语键完整性：{audit['total']} 键 × 3 语言，无缺键、无意外空值")

    # 页面标题 / meta description 随语言切换
    for lg in LANGS:
        pg.click(f'.lang-switch__opt[data-lang="{lg}"]')
        pg.wait_for_timeout(420)
        title = pg.title()
        desc = pg.evaluate("()=>document.querySelector('meta[name=description]')?.content||''")
        want_t = pg.evaluate(f"()=>window.I18N['{lg}']['meta.title.about']")
        want_d = pg.evaluate(f"()=>window.I18N['{lg}']['meta.desc.about']")
        check(title == want_t, f"[{lg}] 标签页标题应为「{want_t}」，实际「{title}」")
        check(desc == want_d, f"[{lg}] meta description 未随语言切换")
        print(f"    · {lg}: title「{title}」")
    pg.click('.lang-switch__opt[data-lang="zh"]')
    pg.wait_for_timeout(400)

    # 关于我：4 条优势（含 A4）/ 4 条原则 + 标题 / 3 段时间线 / 优势副标题
    # 注意：选择器含单引号，走 locator / eval_on_selector_all，不要塞进 JS 字符串里转义
    adv_keys = pg.eval_on_selector_all(
        "[data-i18n^='about.advantages.l']",
        "els=>els.map(e=>e.getAttribute('data-i18n'))")
    adv = len([k for k in adv_keys if re.fullmatch(r"about\.advantages\.l\d+", k or "")])
    check(adv == 4, f"关于我应有 4 条优势，实际 {adv}")
    lead = pg.locator("[data-i18n='about.advantages.lead']").count()
    check(lead == 1, "关于我「能力优势」副标题未接入 i18n（仍是硬编码）")
    prin = pg.locator("[data-i18n^='about.principle.']").count()
    check(prin == 5, f"设计原则应有 5 个 i18n 节点（1 标题 + 4 条），实际 {prin}")
    tl = pg.locator(".timeline__item").count()
    check(tl == 3, f"经历时间线应有 3 段，实际 {tl}")
    print(f"  ✓ 关于我：优势 {adv} 条 · 原则 {prin} 节点 · 时间线 {tl} 段")

    # 服务范围：6 个板块 + 序号
    pg.goto(f"{BASE}/services.html", wait_until="networkidle")
    cards = pg.locator(".service-card").count()
    check(cards == 6, f"服务范围应有 6 个板块，实际 {cards}")
    nums = pg.locator(".service-card__num").all_inner_texts()
    check(nums[:1] == ["01"] and nums[-1:] == ["06"], f"板块序号异常：{nums}")
    print(f"  ✓ 服务范围：{cards} 个板块，序号 {nums[0]}–{nums[-1]}")

    # 技能体系：9 条能力 + 10 个工具
    pg.goto(f"{BASE}/skills.html", wait_until="networkidle")
    pro = pg.locator(".skill-list li").count()
    tools = pg.locator(".tool-pill").count()
    check(pro == 9, f"专业能力应有 9 条，实际 {pro}")
    check(tools == 10, f"工具栈应有 10 个，实际 {tools}")
    print(f"  ✓ 技能体系：能力 {pro} 条 · 工具 {tools} 个")

    # 联系方式：7 个合作类型选项
    pg.goto(f"{BASE}/contact.html", wait_until="networkidle")
    opts = pg.locator("select#f-type option").count()
    check(opts == 7, f"合作类型应有 7 个选项，实际 {opts}")
    o7 = pg.locator("[data-i18n='contact.form.type.o7']").inner_text()
    check(o7.strip() == "其他", f"第 7 个选项应为「其他」，实际「{o7}」")
    print(f"  ✓ 联系方式：合作类型 {opts} 个选项（含「其他」）")

    # 静态兜底文案与 i18n 一致（防止三层文案再次漂移）
    zh = pg.evaluate("()=>window.I18N.zh")

    def _esc(t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    drift, n_checked = [], 0
    for fn in [x[0].split("?")[0] for x in PAGES]:
        src = io.open(os.path.join(ROOT, fn), encoding="utf-8").read()
        for m in re.finditer(r'<([a-zA-Z][a-zA-Z0-9]*)\b((?:[^>]*?))data-i18n="([^"]+)"((?:[^>]*?))>([^<]*)</\1>', src):
            key, inner = m.group(3), m.group(5)
            if key not in zh or not inner.strip():
                continue
            n_checked += 1
            want = "<br>".join(_esc(x) for x in str(zh[key]).split("\n"))
            if inner.strip() != want:
                drift.append(f"{fn}:{key}")
    check(not drift, f"静态兜底与 i18n 漂移 {len(drift)} 处：{drift[:6]}")
    print(f"  ✓ 静态兜底与 i18n 一致（校验 {n_checked} 个节点，零漂移）")

    # 移动端
    ctx.close()
    ctx = browser.new_context(viewport={"width": 390, "height": 844},
                              device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    me = []
    pg.on("pageerror", lambda e: me.append(str(e)))
    for path, label in [("index.html", "home"), ("works.html", "works")]:
        pg.goto(f"{BASE}/{path}", wait_until="networkidle", timeout=30000)
        scroll_all(pg)
        ov = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(ov <= 1, f"[mobile/{label}] 横向溢出 {ov}px")
        pg.screenshot(path=os.path.join(OUT, f"11-mobile-{label}.png"), full_page=True)
        print(f"  ✓ 移动端 {label} 无横向溢出（{ov}px）")
    check(not me, f"移动端 JS 错误: {me[:2]}")
    ctx.close()
    browser.close()

print(f"\n{'='*62}")
if fails:
    print(f"  ✗ 共 {len(fails)} 项未通过：")
    for f in fails:
        print("     ·", f)
    sys.exit(1)
print(f"  ✓ 全部通过 —— {len(PAGES)} 页 × 3 语言 + 功能专项 + 三语一致性 + 移动端，零失败")
