"""Generate bilingual résumé PDFs (placeholder until JUN supplies the real one).

Typography mirrors the site: minimal sans, generous whitespace, one warm accent.
Chinese text uses HarmonyOS Sans SC (TTF) — safe for reportlab embedding.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OUT_DIR = "/Users/jamchou/WorkBuddy/2026-09-07-10-36-15/portfolio-site/assets/docs"
os.makedirs(OUT_DIR, exist_ok=True)

FONT_DIR = os.path.expanduser("~/Library/Fonts")
pdfmetrics.registerFont(TTFont("HarmonySC",      os.path.join(FONT_DIR, "HarmonyOS_Sans_SC_Regular.ttf")))
pdfmetrics.registerFont(TTFont("HarmonySC-Md",   os.path.join(FONT_DIR, "HarmonyOS_Sans_SC_Medium.ttf")))
pdfmetrics.registerFont(TTFont("HarmonySC-Bold", os.path.join(FONT_DIR, "HarmonyOS_Sans_SC_Bold.ttf")))
pdfmetrics.registerFont(TTFont("HarmonySC-Lt",   os.path.join(FONT_DIR, "HarmonyOS_Sans_SC_Light.ttf")))

INK     = (0.067, 0.067, 0.067)
BODY    = (0.165, 0.165, 0.165)
MUTED   = (0.42, 0.42, 0.42)
FAINT   = (0.58, 0.58, 0.58)
RULE    = (0.91, 0.90, 0.88)
ACCENT  = (0.69, 0.52, 0.38)

W, H = A4
ML, MR = 62, 62
MT, MB = 58, 56
CW = W - ML - MR


def text(c, x, y, s, font="HarmonySC", size=9.5, color=BODY, align="left"):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    if align == "left":
        c.drawString(x, y, s)
    elif align == "right":
        c.drawRightString(x, y, s)
    else:
        c.drawCentredString(x, y, s)
    return y


def rule(c, x1, y, x2, color=RULE, width=0.6):
    c.setStrokeColorRGB(*color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def section(c, y, title, kicker=None):
    """Draw a section heading; returns the y below it."""
    y -= 30
    text(c, ML, y, title, "HarmonySC-Md", 12, INK)
    if kicker:
        text(c, W - MR, y, kicker, "HarmonySC", 8, FAINT, "right")
    y -= 10
    rule(c, ML, y, W - MR, RULE, 0.6)
    return y - 18


def wrap(c, x, y, s, size=9.5, font="HarmonySC", color=BODY, max_w=CW, lh=15):
    """Naive CJK-aware wrap (counts CJK as full width)."""
    c.setFont(font, size)
    lines, cur = [], ""
    for ch in s:
        trial = cur + ch
        if pdfmetrics.stringWidth(trial, font, size) > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = trial
    if cur:
        lines.append(cur)
    for ln in lines:
        text(c, x, y, ln, font, size, color)
        y -= lh
    return y


def build(lang):
    cn = lang == "cn"
    out = os.path.join(OUT_DIR, f"JUN-Resume-{'CN' if cn else 'EN'}.pdf")
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle("JUN · Résumé" + ("" if cn else " (EN)"))

    # ---- Header ----
    y = H - MT
    text(c, ML, y, "JUN", "HarmonySC-Md", 30, INK)
    text(c, ML, y - 22,
         "全域全媒介全栈创意设计师" if cn else "Full-spectrum · Multi-medium · End-to-end Designer",
         "HarmonySC", 11, MUTED)
    text(c, W - MR, y + 16, "周骏 / JUN" if cn else "JUN (Zhou Jun)",
         "HarmonySC", 9, FAINT, "right")
    text(c, W - MR, y + 2, "hello@jun-portfolio.com", "HarmonySC", 9, FAINT, "right")
    text(c, W - MR, y - 12, "Madrid, Spain", "HarmonySC", 9, FAINT, "right")
    y -= 40
    rule(c, ML, y, W - MR, INK, 0.9)

    # ---- Summary ----
    y = section(c, y, "个人简介" if cn else "Summary")
    y = wrap(c, ML, y,
             "全域全媒介全栈创意设计师。常驻马德里，10 年以上品牌 / IP / UI/UX / 动态 / 3D 跨媒介经验。"
             "擅长独立完成品牌 0-1 全链路设计与落地，从底层 CIS 搭建到 IP 原创、数字界面、品牌动态与 3D 视觉，"
             "所有媒介输出保持统一视觉语言。"
             if cn else
             "Full-spectrum, multi-medium, end-to-end creative designer based in Madrid, with 10+ years "
             "across brand, IP, UI/UX, motion and 3D. Specialises in independent 0→1 brand delivery — "
             "from foundational CIS to original IP, digital interfaces, brand motion and 3D — "
             "holding one unified visual language across every medium.",
             size=9.5, lh=15)

    # ---- Experience ----
    y = section(c, y - 8, "代表经历" if cn else "Experience")

    exp = [
        ("独立设计师 · 全媒介方向" if cn else "Independent Designer · Multi-medium",
         "自由职业 · 马德里" if cn else "Freelance · Madrid",
         "2022 — 现在" if cn else "2022 — Present",
         ["主导品牌 CIS-VIS、原创 IP 全案、UI/UX、动态与 3D 项目",
          "服务跨境客户，覆盖品牌升级、新品牌孵化、IP 周边开发"]
         if cn else
         ["Led brand CIS-VIS, original IP, UI/UX, motion and 3D projects",
          "Served cross-border clients across brand refresh, new brand launches and IP merchandise"]),
        ("主创视觉设计师" if cn else "Lead Visual Designer",
         "品牌设计工作室" if cn else "Brand Design Studio",
         "2018 — 2022",
         ["负责品牌系统搭建、产品 UI/UX、品牌动态与 IP 衍生品开发",
          "主导多个 0-1 新品牌孵化与上市视觉"]
         if cn else
         ["Brand systems, product UI/UX, brand motion, and IP merchandise",
          "Led multiple 0→1 new-brand launches and go-to-market visuals"]),
    ]

    for title, org, date, bullets in exp:
        text(c, ML, y, title, "HarmonySC-Md", 10.5, INK)
        text(c, W - MR, y, date, "HarmonySC", 8.5, FAINT, "right")
        y -= 14
        text(c, ML, y, org, "HarmonySC", 9, MUTED)
        y -= 15
        for b in bullets:
            text(c, ML + 4, y, "—", "HarmonySC", 9, ACCENT)
            y = wrap(c, ML + 16, y, b, size=9, color=BODY, max_w=CW - 16, lh=14)
            y -= 2
        y -= 12

    # ---- Education ----
    y = section(c, y - 4, "教育背景" if cn else "Education")
    text(c, ML, y, "视觉传达 / 数字媒体艺术" if cn else "Visual Communication / Digital Media Art",
         "HarmonySC-Md", 10.5, INK)
    text(c, W - MR, y, "2014 — 2018", "HarmonySC", 8.5, FAINT, "right")
    y -= 14
    text(c, ML, y, "艺术与设计院校" if cn else "Art & Design School", "HarmonySC", 9, MUTED)
    y -= 20

    # ---- Skills ----
    y = section(c, y - 4, "核心技能" if cn else "Core Skills")
    skills = (["品牌 CIS-VIS 系统 / 原创 IP 全案与衍生品",
               "平面视觉 / 海报 / 画册 / 印刷物料",
               "网页 & APP UI/UX 设计 / 组件库",
               "动态视频 / MG 动效 / 品牌短片",
               "3D 建模 / 场景渲染 / 产品视觉动画",
               "中英双语工作 / 海外项目远程协作"]
              if cn else
              ["Brand CIS-VIS systems / Original IP & merchandise",
               "Print, posters, lookbooks, packaging",
               "Web & app UI/UX design / Component libraries",
               "Motion graphics / Brand films",
               "3D modeling / Scene rendering / Product animation",
               "Bilingual 中文 / English · remote-ready"])
    col_w = CW / 2
    for i, s in enumerate(skills):
        col = i % 2
        row = i // 2
        x = ML + col * col_w
        yy = y - row * 17
        text(c, x, yy, "·", "HarmonySC-Bold", 9, ACCENT)
        text(c, x + 12, yy, s, "HarmonySC", 9, BODY)

    # ---- Tools ----
    y = section(c, y - ((len(skills) + 1) // 2) * 17 - 10, "软件工具" if cn else "Tools")
    tools = "Figma · Photoshop · Illustrator · Procreate · After Effects · Premiere · Blender / C4D · HTML / CSS"
    wrap(c, ML, y, tools, size=9, color=MUTED, max_w=CW, lh=14)

    # ---- Footer ----
    text(c, ML, MB, "JUN · 全域全媒介全栈创意设计师" if cn else "JUN · Full-spectrum multi-medium designer",
         "HarmonySC", 7.5, FAINT)
    text(c, W - MR, MB, "hello@jun-portfolio.com", "HarmonySC", 7.5, FAINT, "right")

    c.showPage()
    c.save()
    return out


for lg in ("cn", "en"):
    p = build(lg)
    print(f"✓ {os.path.basename(p)}  ({os.path.getsize(p)} bytes)")
