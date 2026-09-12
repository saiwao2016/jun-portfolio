#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成三语简历 PDF（中文 / Español / English）。

要点：
- 用 HarmonyOS Sans SC 的 **TTF** 版本。这台机器上渲染含中文的 PDF 时，
  CFF/OTF 会丢字形（见用户级 MEMORY.md），TTF 不受影响。
- 字体本身带拉丁字形，三语共用一套字体家族即可，版式不会因语言漂移。
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, HRFlowable, KeepTogether)

FONT_DIR = os.path.expanduser("~/Library/Fonts")
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "docs")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------- 字体 ----------
for name, fn in [("JUN", "HarmonyOS_Sans_SC_Regular.ttf"),
                 ("JUN-B", "HarmonyOS_Sans_SC_Bold.ttf"),
                 ("JUN-M", "HarmonyOS_Sans_SC_Medium.ttf"),
                 ("JUN-L", "HarmonyOS_Sans_SC_Light.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fn)))

INK = colors.HexColor("#141414")
INK2 = colors.HexColor("#4a4a4a")
MUTED = colors.HexColor("#8a8a8a")
ACCENT = colors.HexColor("#c8452f")
RULE = colors.HexColor("#dcdcd8")

# ---------- 样式 ----------
S = {
    "name":    ParagraphStyle("name", fontName="JUN-B", fontSize=23, leading=28,
                              textColor=INK, spaceAfter=2),
    "role":    ParagraphStyle("role", fontName="JUN-L", fontSize=11, leading=15,
                              textColor=ACCENT, spaceAfter=7),
    "contact": ParagraphStyle("contact", fontName="JUN", fontSize=9, leading=14,
                              textColor=MUTED),
    "h2":      ParagraphStyle("h2", fontName="JUN-B", fontSize=11, leading=15,
                              textColor=INK, spaceBefore=2, spaceAfter=1),
    "body":    ParagraphStyle("body", fontName="JUN", fontSize=9.3, leading=14,
                              textColor=INK2),
    "job":     ParagraphStyle("job", fontName="JUN-M", fontSize=10.2, leading=14,
                              textColor=INK),
    "meta":    ParagraphStyle("meta", fontName="JUN-L", fontSize=8.5, leading=12,
                              textColor=MUTED),
    "bullet":  ParagraphStyle("bullet", fontName="JUN", fontSize=9, leading=13.4,
                              textColor=INK2, leftIndent=10, bulletIndent=1,
                              spaceAfter=1.2),
}


def section(title):
    """章节标题：标题 + 细分隔线"""
    return KeepTogether([
        Spacer(1, 7),
        Paragraph(title, S["h2"]),
        HRFlowable(width="100%", thickness=0.6, color=RULE,
                   spaceBefore=3, spaceAfter=7),
    ])


def job(title, org, date, bullets):
    return KeepTogether(
        [Paragraph(title, S["job"]),
         Paragraph(f"{org} &nbsp;·&nbsp; {date}", S["meta"]),
         Spacer(1, 3.5)]
        + [Paragraph(b, S["bullet"], bulletText="·") for b in bullets]
        + [Spacer(1, 5.5)]
    )


# ---------- 内容 ----------
def build(lang):
    """返回 (文件名, 姓名, 职位, 联系方式, flowables)"""

    if lang == "zh":
        name, role = "周骏 · JUN", "视觉设计师 — 品牌系统 · 信息设计 · 原创 IP"
        contact = "saiwao@qq.com &nbsp;|&nbsp; 西班牙马德里 &nbsp;|&nbsp; 中文（母语）· English · Español"
        L = dict(
            summary_t="个人简介",
            summary=("视觉设计师，十余年品牌与信息设计经验。擅长把复杂内容整理成可复用的视觉系统："
                     "206 份心理量表报告共用一套模板体系，44 页品牌识别手册从标志制图规范到办公物料完整落地。"
                     "具备品牌、出版、界面、IP、包装、空间六类交付能力，熟悉印刷工艺与制作流程。现居西班牙马德里。"),
            exp_t="工作经历",
            jobs=[
                ("视觉设计师", "睿智云（广东省睿智云智慧科技）· 心理与儿童健康测评", "2019 — 至今", [
                    "建立量表报告版式体系，206 份报告共用一套模板，覆盖基本信息、结果图表、解读与建议全流程",
                    "主导品牌识别系统（VIS 手册 44 页）：标志标准制图、色彩与字体规范、办公物料与场景应用",
                    "完成 34 页产品手册、企业画册、解决方案演示文档的编排与印刷交付",
                    "设计证书体系（ASQ / CDI / CHTIC / M-CHAT / Timp）与周边物料",
                ]),
                ("视觉设计师", "深圳市心智心理测量技术研究所有限公司 · 珠海市海扬教育有限公司", "2016.06 — 至今", [
                    "完成新公司整体 VIS 设计",
                    "负责 WEB 页面视觉设计、UI 设计与交互流程梳理",
                    "负责 ASQ 儿童发育筛查系统与 M-CHAT 测评系统的结构梳理与原型绘制",
                    "设计 M-CHAT 系统测量动画，绘制分镜头并制作上线",
                ]),
                ("平面设计师", "新乡市志愿者联合会 · 红领巾志愿服务中心", "2013.09 — 2016.06", [
                    "负责公益活动全套宣传物料：海报、展板、易拉宝、宣传页、募捐箱",
                    "运营维护团队微博及微信平台，制作配套视觉物料",
                    "设计志愿者项目吉祥物与微信表情包，建立卡通 IP「石榴妹」",
                    "核心项目获 2015 年中国青年志愿服务项目大赛奖项",
                ]),
            ],
            edu_t="教育背景",
            edu=("天津滨海职业技术学院", "环境艺术设计"),
            skill_t="核心技能",
            skills=[
                "品牌 CIS / VIS 系统搭建与规范手册",
                "量表报告 / 表单 / 信息可视化版式系统",
                "画册 / 手册 / 书籍装帧与印刷工艺",
                "原创 IP 形象 / 表情包 / 周边衍生",
                "网页与移动端界面设计",
                "包装结构 / 展陈物料 / 空间图形",
            ],
            cert_t="资质认证",
            cert=["ACAA 中国认证设计师"],
        )
        fn = "JUN-CV-ZH.pdf"

    elif lang == "es":
        name, role = "Jun Zhou (JUN)", "Diseñador visual — Marca · Diseño de información · IP original"
        contact = "saiwao@qq.com &nbsp;|&nbsp; Madrid, España &nbsp;|&nbsp; Chino nativo · English · Español"
        L = dict(
            summary_t="Perfil",
            summary=("Diseñador visual con más de diez años en marca y diseño de información. Convierto contenido "
                     "complejo en sistemas visuales reutilizables: 206 informes de escalas psicológicas comparten "
                     "una plantilla y un manual de identidad de 44 páginas cubre del logotipo a la papelería. Seis "
                     "áreas —marca, editorial, interfaz, IP, packaging y espacio— con dominio de artes gráficas."),
            exp_t="Experiencia",
            jobs=[
                ("Diseñador visual", "Ruizhi Cloud · Evaluación psicológica e infantil", "2019 — Actualidad", [
                    "Sistema de maquetación de informes: 206 informes con una plantilla única, de los datos básicos a las recomendaciones",
                    "Dirección del sistema de identidad de marca (manual VIS de 44 páginas): logotipo, color, tipografía, papelería y aplicaciones",
                    "Maquetación y producción impresa de un manual de 34 páginas, catálogo corporativo y documentos de solución",
                    "Diseño del sistema de certificados (ASQ / CDI / CHTIC / M-CHAT / Timp) y material promocional",
                ]),
                ("Diseñador visual", "Instituto de Medición Psicológica de Shenzhen · Haiyang Education (Zhuhai)", "06.2016 — Actualidad", [
                    "VIS corporativo completo para la nueva empresa",
                    "Diseño visual web, diseño de interfaz y definición de flujos de interacción",
                    "Estructuración y prototipado de los sistemas de evaluación ASQ y M-CHAT",
                    "Diseño de animaciones del sistema M-CHAT, storyboards y puesta en producción",
                ]),
                ("Diseñador gráfico", "Federación de Voluntarios de Xinxiang · Centro Honglingjin", "09.2013 — 06.2016", [
                    "Materiales completos de campañas: carteles, paneles, roll-ups, folletos y huchas",
                    "Gestión de las cuentas de Weibo y WeChat y de su material gráfico",
                    "Mascota del programa de voluntariado y stickers de WeChat; creación de la IP «Shiliu Mei»",
                    "El proyecto principal obtuvo el premio del Concurso Nacional de Proyectos de Voluntariado Juvenil 2015",
                ]),
            ],
            edu_t="Formación",
            edu=("Tianjin Binhai Vocational Technical College", "Diseño de Arte Ambiental"),
            skill_t="Competencias clave",
            skills=[
                "Sistemas CIS / VIS y manuales de marca",
                "Informes de escalas, formularios y sistemas de maquetación",
                "Catálogos, manuales, encuadernación y artes gráficas",
                "Personajes IP, stickers y merchandising",
                "Interfaces web y móviles",
                "Packaging, material expositivo y gráfica espacial",
            ],
            cert_t="Certificaciones",
            cert=["ACAA Certified Designer (China)"],
        )
        fn = "JUN-CV-ES.pdf"

    else:
        name, role = "Jun Zhou (JUN)", "Visual designer — Brand · Information design · Original IP"
        contact = "saiwao@qq.com &nbsp;|&nbsp; Madrid, Spain &nbsp;|&nbsp; Native Chinese · English · Spanish"
        L = dict(
            summary_t="Summary",
            summary=("Visual designer with over ten years in brand and information design. I turn complex content "
                     "into reusable visual systems: 206 psychological assessment reports share a single template, "
                     "and a 44-page identity manual runs from logo construction to stationery. Six delivery areas "
                     "—brand, editorial, interface, IP, packaging and space— with strong print-production fluency. "
                     "Based in Madrid."),
            exp_t="Experience",
            jobs=[
                ("Visual designer", "Ruizhi Cloud · Psychological & child health assessment", "2019 — Present", [
                    "Built the report layout system: 206 reports on a single template, covering basic data, result charts, interpretation and recommendations",
                    "Led the brand identity system (44-page VIS manual): logo construction, colour, typography, stationery and applications",
                    "Layout and print delivery of a 34-page product manual, corporate brochure and solution decks",
                    "Designed the certificate system (ASQ / CDI / CHTIC / M-CHAT / Timp) and merchandise",
                ]),
                ("Visual designer", "Shenzhen Institute of Psychological Measurement Technology · Zhuhai Haiyang Education", "06.2016 — Present", [
                    "Complete corporate VIS for the new company",
                    "Web visual design, UI design and interaction flow definition",
                    "Structuring and prototyping of the ASQ and M-CHAT assessment systems",
                    "Designed M-CHAT measurement animations, storyboards and production rollout",
                ]),
                ("Graphic designer", "Xinxiang Volunteer Federation · Honglingjin Service Centre", "09.2013 — 06.2016", [
                    "Full campaign collateral: posters, panels, roll-ups, leaflets, donation boxes",
                    "Ran Weibo and WeChat channels and their visual material",
                    "Designed the volunteer programme mascot and WeChat stickers; created the IP “Shiliu Mei”",
                    "Core project won the 2015 China Youth Volunteer Service Project Competition",
                ]),
            ],
            edu_t="Education",
            edu=("Tianjin Binhai Vocational Technical College", "Environmental Art Design"),
            skill_t="Core skills",
            skills=[
                "CIS / VIS systems and brand manuals",
                "Assessment reports, forms and layout systems",
                "Brochures, manuals, bookbinding and print production",
                "Original IP characters, stickers and merchandise",
                "Web and mobile interface design",
                "Packaging, exhibition material and spatial graphics",
            ],
            cert_t="Certification",
            cert=["ACAA Certified Designer (China)"],
        )
        fn = "JUN-CV-EN.pdf"

    flow = [
        Paragraph(name, S["name"]),
        Paragraph(role, S["role"]),
        Paragraph(contact, S["contact"]),
        HRFlowable(width="100%", thickness=1.1, color=INK, spaceBefore=11, spaceAfter=2),

        section(L["summary_t"]),
        Paragraph(L["summary"], S["body"]),

        section(L["exp_t"]),
    ]
    for j in L["jobs"]:
        flow.append(job(*j))

    flow += [section(L["edu_t"]),
             Paragraph(L["edu"][0], S["job"]),
             Paragraph(L["edu"][1], S["meta"])]

    flow += [section(L["skill_t"])]
    flow += [Paragraph(s, S["bullet"], bulletText="·") for s in L["skills"]]

    flow += [section(L["cert_t"])]
    flow += [Paragraph(c, S["bullet"], bulletText="·") for c in L["cert"]]

    return fn, flow


# ---------- 渲染 ----------
def render(lang):
    fn, flow = build(lang)
    path = os.path.join(OUT_DIR, fn)

    doc = BaseDocTemplate(path, pagesize=A4,
                          leftMargin=19 * mm, rightMargin=19 * mm,
                          topMargin=14 * mm, bottomMargin=13 * mm,
                          title=f"Jun Zhou — CV ({lang})", author="Jun Zhou",
                          subject="Curriculum Vitae")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")

    def footer(canv, d):
        canv.saveState()
        canv.setFont("JUN-L", 7.5)
        canv.setFillColor(MUTED)
        canv.drawString(doc.leftMargin, 11 * mm, "Jun Zhou (JUN) · Visual designer · Madrid")
        canv.drawRightString(A4[0] - doc.rightMargin, 11 * mm, str(canv.getPageNumber()))
        canv.restoreState()

    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])
    doc.build(flow)
    return path


if __name__ == "__main__":
    for lg in ("zh", "es", "en"):
        print("✓", render(lg))
