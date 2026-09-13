#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「平原商场 · 2018 戊戌年台历设计」作品专题页。

为什么用生成器而不是直接手写：
  站点的文案是「三层结构」——HTML 静态兜底 → i18n.js → site.json 覆盖层。
  _tools/verify.py 有一条硬断言：每个 data-i18n 节点的静态兜底必须与
  i18n 的中文值逐字一致（防漂移）。本页有近 200 个节点，手写两边必然出错。
  所以这里把三语文案只定义一次（TRI），由脚本同时产出：
    (a) assets/js/i18n.js 里 zh / es / en 三个语言块的 pc.* 键（按标记幂等插入）
    (b) work-pingyuan-calendar.html（静态兜底 = 中文值，天然零漂移）

页头 / 导航 / 页脚从 work-detail.html 抽取复用，站点导航改动后重跑本脚本即可同步。

用法：python3 _tools/gen_pingyuan_page.py
"""

import html
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
I18N = os.path.join(ROOT, "assets/js/i18n.js")
DETAIL = os.path.join(ROOT, "work-detail.html")
OUT_HTML = os.path.join(ROOT, "work-pingyuan-calendar.html")
IMG = "assets/works/pingyuan-calendar"

BEGIN = "/* >>> generated: pingyuan-calendar >>> */"
END = "/* <<< generated: pingyuan-calendar <<< */"

# 对应 content/works.json 里的作品 id（main.js 用它取上一件/下一件）
WORK_ID = "pingyuan-calendar"

# ============================================================
# 一、三语内容表（唯一真源）
#     key -> (中文, Español, English)
# ============================================================
TRI = []
_KEYS = set()


def K(key, zh, es, en):
    """登记一条文案。重复 key 直接报错，避免静默覆盖。"""
    if key in _KEYS:
        raise SystemExit(f"重复的 key：{key}")
    _KEYS.add(key)
    TRI.append((key, zh, es, en))
    return zh


# ---- 页面元信息 ----
K("pc.meta.title", "平原商场 · 2018 戊戌年台历设计 — JUN",
  "Pingyuan Mall · Calendario anual 2018 — JUN",
  "Pingyuan Mall · 2018 Annual Calendar — JUN")
K("pc.meta.desc",
  "平原商场 2018 戊戌年台历设计：以苹果「平平」为品牌吉祥物，12 个月主题插画、12 页功能日历、年度计划与年终总结，日历页内嵌商场品牌优惠券。平面设计作品，周骏（JUN）设计。",
  "Calendario anual 2018 del centro comercial Pingyuan: la manzana «Pingping» como mascota de marca, 12 ilustraciones temáticas, 12 páginas de calendario funcional, plan anual y resumen de cierre, con cupones de las marcas del centro. Diseño gráfico de JUN (Zhou Jun).",
  "The 2018 annual calendar for Pingyuan Mall: the apple mascot \"Pingping\", 12 themed illustrations, 12 functional calendar pages, a yearly planner and a year-end summary, with the mall brands' coupons built into the calendar pages. Graphic design by JUN (Zhou Jun).")

# ---- 页内子导航 ----
K("pc.nav.overview", "项目概览", "Resumen", "Overview")
K("pc.nav.features", "设计亮点", "Destacados", "Highlights")
K("pc.nav.mockups", "样机展示", "Maquetas", "Mockups")
K("pc.nav.flat", "平铺图", "Láminas", "Flat layout")
K("pc.nav.months", "逐月作品", "Mes a mes", "Month by month")
K("pc.nav.back", "返回作品集", "Volver a proyectos", "Back to works")

# ---- Hero ----
K("pc.hero.kicker", "DESIGN PORTFOLIO · 2018", "DESIGN PORTFOLIO · 2018", "DESIGN PORTFOLIO · 2018")
K("pc.hero.title", "平原商场", "Pingyuan Mall", "Pingyuan Mall")
K("pc.hero.sub", "2018 戊戌年台历设计",
  "Calendario anual 2018 · Año del Perro",
  "2018 Annual Calendar · Year of the Dog")
K("pc.hero.desc",
  "一套以苹果「平平」为品牌吉祥物的年度台历：12 个月份主题插画、12 页功能日历、年度计划与年终总结，将中式新年喜庆与国际化元素融为一体。",
  "Un calendario anual con la manzana «Pingping» como mascota de marca: 12 ilustraciones temáticas, 12 páginas de calendario funcional, un plan anual y un resumen de cierre. La celebración del Año Nuevo chino se funde aquí con guiños internacionales.",
  "An annual calendar built around the red apple mascot \"Pingping\": 12 themed illustrations, 12 functional calendar pages, a yearly planner and a year-end summary — Chinese New Year festivity fused with international touches.")
K("pc.hero.figcap", "封面样机 · 桌面展示",
  "Maqueta de cubierta · Escritorio", "Cover mockup · Desktop")
K("pc.stat.pages", "个版面", "láminas", "plates")
K("pc.stat.months", "个主题月", "meses temáticos", "themed months")
K("pc.stat.sheets", "张纸页", "hojas", "sheets")
K("pc.stat.mascot", "个吉祥物", "mascota", "mascot")

# ---- 六个区块标题（英文标签为版面装饰，各语言一致） ----
K("pc.sec.overview", "项目概览", "Resumen del proyecto", "Project overview")
K("pc.sec.overview.tag", "PROJECT OVERVIEW", "PROJECT OVERVIEW", "PROJECT OVERVIEW")
K("pc.sec.features", "设计亮点", "Destacados del diseño", "Design highlights")
K("pc.sec.features.tag", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS")
K("pc.sec.mockups", "样机展示", "Maquetas", "Mockups")
K("pc.sec.mockups.tag", "MOCKUPS", "MOCKUPS", "MOCKUPS")
K("pc.sec.flat", "平铺图展示", "Láminas planas", "Flat layout")
K("pc.sec.flat.tag", "FLAT LAYOUT · 28 PLATES", "FLAT LAYOUT · 28 PLATES", "FLAT LAYOUT · 28 PLATES")
K("pc.sec.months", "逐月作品", "Mes a mes", "Month by month")
K("pc.sec.months.tag", "MONTH BY MONTH", "MONTH BY MONTH", "MONTH BY MONTH")
K("pc.sec.closing", "封底 · 尾声", "Contracubierta y cierre", "Back cover & closing")
K("pc.sec.closing.tag", "BACK COVER & CLOSING", "BACK COVER & CLOSING", "BACK COVER & CLOSING")

# ---- 01 项目概览 ----
K("pc.ov.client.k", "客户", "Cliente", "Client")
K("pc.ov.client.v", "平原商场 Pingyuan Mall", "Centro comercial Pingyuan", "Pingyuan Mall")
K("pc.ov.type.k", "项目类型", "Tipo", "Type")
K("pc.ov.type.v", "年度台历 · 平面设计", "Calendario anual · Diseño gráfico", "Annual calendar · Graphic design")
K("pc.ov.year.k", "设计年份", "Año", "Year")
K("pc.ov.year.v", "2018 · 戊戌狗年", "2018 · Año del Perro", "2018 · Year of the Dog")
K("pc.ov.pages.k", "页数", "Páginas", "Pages")
K("pc.ov.pages.v", "14 页 / 28 个版面", "14 hojas / 28 láminas", "14 sheets / 28 plates")
K("pc.ov.extra.k", "配套功能", "Extras", "Features")
K("pc.ov.extra.v", "节气标注 · 品牌优惠券", "Términos solares · Cupones de marca", "Solar terms · Brand coupons")
K("pc.ov.p1",
  "这是为**平原商场**打造的 2018 年度台历。作品以一只拟人化的红色**苹果「平平」**作为贯穿全年的品牌吉祥物——它出现在封面主视觉中，也化身数字「0」融入「2018」的字形，成为整套设计最鲜明的记忆点。",
  "Es el calendario anual 2018 creado para **Pingyuan Mall**. Su hilo conductor es una manzana roja antropomórfica, **«Pingping»**, mascota de marca que protagoniza la cubierta y se transforma en el «0» de «2018»: el recurso más reconocible de todo el proyecto.",
  "This is the 2018 annual calendar made for **Pingyuan Mall**. Its through-line is an anthropomorphic red apple, **\"Pingping\"**, the brand mascot who stars on the cover and turns into the \"0\" of \"2018\" — the single most memorable device in the set.")
K("pc.ov.p2",
  "每月一张**主题插画页**（舞狮新春、浪漫情人节、植树护绿、雨天市集、荷塘消夏、农场丰收……），一张**功能日历页**（公历、农历、节气、节日与商场品牌优惠券）。插画叙事与实用功能交替呈现，让台历既是日历，也是品牌全年的温情陪伴。",
  "Cada mes combina una **página ilustrada** (danza del león, San Valentín, plantación de árboles, mercado bajo la lluvia, estanque de lotos, cosecha…) con una **página de calendario funcional** (calendario gregoriano y lunar, términos solares, festividades y cupones de las marcas del centro). Narrativa y utilidad se alternan: sirve para consultar la fecha y también como compañía de marca durante todo el año.",
  "Every month pairs a **themed illustration page** (lion dance, Valentine's Day, tree planting, a rainy market, the lotus pond, the harvest…) with a **functional calendar page** (solar and lunar dates, solar terms, festivals and the mall brands' coupons). Story and utility alternate, so the calendar works both as a date reference and as a year-long brand companion.")
K("pc.ov.point1", "苹果「平平」贯穿 12 个月，统一识别",
  "«Pingping» recorre los 12 meses como sello unificador",
  "\"Pingping\" runs through all 12 months as a unifying mark")
K("pc.ov.point2", "中英双语月份标识与竖排品牌栏",
  "Meses bilingües y columna de marca vertical",
  "Bilingual month labels and a vertical brand column")
K("pc.ov.point3", "中式红金喜庆 + 世界地标国际化表达",
  "Festejo chino en rojo y oro + hitos internacionales",
  "Chinese red-and-gold festivity + international landmarks")
K("pc.ov.point4", "日历页内嵌商场品牌优惠券",
  "Cupones de marca integrados en las páginas de calendario",
  "Mall brand coupons embedded in the calendar pages")

# ---- 02 设计亮点 ----
FEATURES = [
    ("01 — 品牌吉祥物", "01 — Mascota de marca", "01 — Brand mascot",
     "苹果「平平」替代数字 0",
     "La manzana «Pingping» sustituye al 0",
     "The \"Pingping\" apple replaces the 0",
     "红色卡通苹果「平平」既是封面主角，又化身 2018 字形中的「0」。从年度计划页到年终总结页，同一形象反复出现，形成强烈的品牌记忆点。",
     "La manzana roja «Pingping» protagoniza la cubierta y a la vez se convierte en el «0» de 2018. De la página de plan anual al resumen de cierre, la misma figura reaparece hasta fijarse como recuerdo de marca.",
     "The red cartoon apple stars on the cover and doubles as the \"0\" in 2018. From the yearly planner to the year-end summary the same figure returns, until it sticks as a brand memory."),
    ("02 — 月度叙事插画", "02 — Ilustración narrativa", "02 — Monthly narrative",
     "12 个月 12 个场景", "12 meses, 12 escenas", "12 months, 12 scenes",
     "每月一幅原创卡通插画：一月舞狮、六月海滩、八月小卖部、十二月圣诞小屋……围绕节气与节日讲述一年的故事，温馨而富有生活气息。",
     "Una ilustración original por mes: la danza del león en enero, la playa en junio, la tienda de barrio en agosto, la casa de Papá Noel en diciembre… Un relato del año construido sobre términos solares y festividades, cálido y cotidiano.",
     "One original illustration per month — the lion dance in January, the beach in June, the corner shop in August, Santa's cabin in December. A story of the year told through solar terms and festivals: warm and everyday."),
    ("03 — 功能型日历页", "03 — Página funcional", "03 — Functional page",
     "日历 + 优惠券双功能", "Calendario y cupones en una página", "Calendar + coupons in one page",
     "日历页标注公历、农历、节气与传统节日，右侧嵌入商场各楼层品牌的优惠券板块，把日常使用场景转化为线下引流入口。",
     "La página de calendario anota fechas gregorianas y lunares, términos solares y fiestas tradicionales, e integra a la derecha los cupones de las marcas del centro: el uso diario se convierte en un canal de tráfico a la tienda.",
     "Each calendar page marks solar and lunar dates, solar terms and traditional festivals, and carries the mall brands' coupons on the right — turning daily use into foot traffic."),
    ("04 — 统一视觉系统", "04 — Sistema visual", "04 — Visual system",
     "红金喜庆 × 国际元素", "Rojo y oro × guiños internacionales", "Red and gold × international references",
     "中式灯笼、福字、锦鲤与自由女神像、埃菲尔铁塔同框，竖排「平原」品牌栏与中英月份名贯穿全册，喜庆而不失国际化。",
     "Farolillos, el carácter de la fortuna y carpas conviven con la Estatua de la Libertad y la Torre Eiffel; la columna vertical «Pingyuan» y los meses bilingües recorren todo el volumen. Festivo sin perder la mirada internacional.",
     "Chinese lanterns, fortune characters and koi share the page with the Statue of Liberty and the Eiffel Tower; a vertical \"Pingyuan\" column and bilingual month names run through the book. Festive, yet internationally minded."),
]
for i, (no_zh, no_es, no_en, t_zh, t_es, t_en, p_zh, p_es, p_en) in enumerate(FEATURES, 1):
    K(f"pc.ft{i}.no", no_zh, no_es, no_en)
    K(f"pc.ft{i}.t", t_zh, t_es, t_en)
    K(f"pc.ft{i}.p", p_zh, p_es, p_en)

# ---- 03 样机 ----
K("pc.mk1.cap", "双页展开 · 插画页与日历页",
  "Doble página abierta · Ilustración y calendario",
  "Spread · illustration and calendar page")
K("pc.mk2.cap", "立式桌面 · 封面主视觉",
  "En pie sobre la mesa · Portada", "Standing on a desk · Cover key visual")

# ---- 04 平铺图分组标题 ----
K("pc.fg1.t", "封面 · 封底 · 功能页", "Cubierta, contracubierta y funcionales", "Cover · back cover · planner pages")
K("pc.fg1.n", "4 PAGES", "4 LÁMINAS", "4 PLATES")
K("pc.fg2.t", "12 个月主题插画页", "12 ilustraciones temáticas", "12 themed illustration pages")
K("pc.fg2.n", "ILLUSTRATION PAGES", "ILUSTRACIONES", "ILLUSTRATIONS")
K("pc.fg3.t", "12 个月功能日历页", "12 páginas de calendario funcional", "12 functional calendar pages")
K("pc.fg3.n", "CALENDAR PAGES", "CALENDARIO", "CALENDAR PAGES")

# ---- 平铺图：封面组 ----
PLATES_HEAD = [
    ("cover", "封面", "Cubierta", "Cover",
     "2018 新年主视觉", "Visual de Año Nuevo 2018", "2018 New Year key visual"),
    ("back", "封底", "Contracubierta", "Back cover",
     "苹果「平平」2018 标识", "Logotipo 2018 con «Pingping»", "\"Pingping\" 2018 logo"),
    ("plan", "年度计划", "Plan anual", "Yearly planner",
     "2018 年度计划", "Plan anual 2018", "2018 yearly planner"),
    ("summary", "年终总结", "Cierre del año", "Year-end summary",
     "2018 年终总结", "Resumen de 2018", "2018 year-end summary"),
]
for slug, t_zh, t_es, t_en, s_zh, s_es, s_en in PLATES_HEAD:
    K(f"pc.pl.{slug}.t", t_zh, t_es, t_en)
    K(f"pc.pl.{slug}.s", s_zh, s_es, s_en)

# ---- 12 个月：中文序数名 / 西英月名 / 插画主题 / 节气 ----
MONTH_CN = ["壹月", "贰月", "叁月", "肆月", "伍月", "陆月", "柒月", "捌月", "玖月", "拾月", "拾壹月", "拾贰月"]
MONTH_CN_PLAIN = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
MONTH_EN = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]

THEME_ZH = ["舞狮新春", "浪漫情人节", "植树护绿", "雨天市集", "温馨厨房", "海滩度假",
            "荷塘消夏", "平原小卖部", "农场丰收", "国庆欢庆", "感恩节", "圣诞小屋"]
THEME_ES = ["Danza del león", "San Valentín", "Plantar árboles", "Mercado bajo la lluvia",
            "Cocina cálida", "Vacaciones en la playa", "Estanque de lotos", "La tienda Pingyuan",
            "Cosecha en la granja", "Fiesta Nacional", "Acción de Gracias", "La casa de Papá Noel"]
THEME_EN = ["Lion dance", "Valentine's Day", "Tree planting", "Rainy market",
            "Warm kitchen", "Beach holiday", "Lotus pond", "Pingyuan corner shop",
            "Farm harvest", "National Day", "Thanksgiving", "Santa's cabin"]

TERMS_ZH = ["元旦 · 小寒 · 大寒", "立春 · 除夕 · 春节 · 雨水", "惊蛰 · 春分", "清明 · 谷雨",
            "立夏 · 小满", "芒种 · 夏至", "小暑 · 大暑", "立秋 · 处暑",
            "白露 · 秋分", "寒露 · 霜降", "立冬 · 小雪", "大雪 · 冬至"]
TERMS_ES = ["Año Nuevo · Frío menor · Frío mayor",
            "Inicio de la primavera · Nochevieja china · Año Nuevo chino · Lluvia",
            "Despertar de los insectos · Equinoccio de primavera", "Claridad pura · Lluvia de grano",
            "Inicio del verano · Pequeña plenitud", "Grano en espiga · Solsticio de verano",
            "Calor menor · Calor mayor", "Inicio del otoño · Fin del calor",
            "Rocío blanco · Equinoccio de otoño", "Rocío frío · Caída de la escarcha",
            "Inicio del invierno · Nieve menor", "Nieve mayor · Solsticio de invierno"]
TERMS_EN = ["New Year's Day · Minor Cold · Major Cold",
            "Start of Spring · Chinese New Year's Eve · Spring Festival · Rain Water",
            "Awakening of Insects · Spring Equinox", "Pure Brightness · Grain Rain",
            "Start of Summer · Grain Full", "Grain in Ear · Summer Solstice",
            "Minor Heat · Major Heat", "Start of Autumn · End of Heat",
            "White Dew · Autumn Equinox", "Cold Dew · Frost's Descent",
            "Start of Winter · Minor Snow", "Major Snow · Winter Solstice"]

DESC_ZH = [
    "舞狮、雪人与小龙共贺新春，春联横批「财源滚滚随春至」，红火开场。",
    "小鹿长椅与摩天轮，气球与爱心交织，二月的浪漫遇上新春余温。",
    "春日植树护绿，小兔与吉祥物为小树浇水，「保护环境」的木牌立在花丛间。",
    "雨天市集的烟火气：红白遮阳篷的商场门店前，撑伞的福娃踩过积水。",
    "温馨厨房里，系着围裙的小龙备餐，另一只抱着花束，购物篮满载祝福。",
    "阳光沙滩与草编遮阳伞，戴泳圈的福袋泡在浅池里，夏日松弛感拉满。",
    "荷塘消夏：小龙趴在荷叶上酣睡，金鱼游弋、荷花半开，清凉一夏。",
    "「平原小卖部」的市井烟火：蓝白遮阳帘、平原冰糕，屋顶还趴着猫。",
    "平原农场秋收：金黄麦田、稻草人与收割机，丰收的喜悦溢满画面。",
    "国庆欢庆：小鹿举着相机记录城市庆典，气球彩旗下「国庆节」字样醒目。",
    "感恩节火鸡大餐，小鹿们围绕餐盘大快朵颐，中西节庆在此交汇。",
    "圣诞小屋亮起串灯，吉祥物踩着木梯装点圣诞树，一年的故事圆满收尾。",
]
DESC_ES = [
    "Leones, un muñeco de nieve y dragoncitos celebran el Año Nuevo; el cartel augura que la riqueza llegará con la primavera. Un arranque en rojo.",
    "Un banco con un cervatillo y una noria, globos y corazones entretejidos: el romanticismo de febrero se cruza con el rescoldo del Año Nuevo.",
    "Plantar y cuidar el verde en primavera: una liebre y la mascota riegan un arbolito, con el cartel de «protege el medio ambiente» entre las flores.",
    "El bullicio de un mercado lluvioso: ante los toldos rojos y blancos de las tiendas del centro, figuras de la fortuna cruzan los charcos con paraguas.",
    "En una cocina cálida, un dragoncito con delantal prepara la comida, otro abraza un ramo y la cesta rebosa de buenos deseos.",
    "Playa soleada y sombrillas de fibra: una bolsa de la fortuna con flotador se remoja en la orilla. Verano en estado puro.",
    "Verano en el estanque de lotos: un dragoncito duerme sobre una hoja, nadan las carpas doradas y el loto entreabre. Un verano fresco.",
    "El sabor de barrio de la «tienda Pingyuan»: toldos azules y blancos, helados Pingyuan y un gato tumbado en el tejado.",
    "Cosecha de otoño en la granja Pingyuan: campos dorados, espantapájaros y cosechadora. La alegría de la recolección llena el cuadro.",
    "Fiesta Nacional: un cervatillo fotografía la celebración urbana entre globos y banderines, con el rótulo «Fiesta Nacional» bien visible.",
    "Un banquete de pavo por Acción de Gracias: los cervatillos devoran el plato. Oriente y Occidente se encuentran en la misma fiesta.",
    "La casita navideña enciende sus luces y la mascota sube una escalera para adornar el árbol. La historia del año cierra en redondo.",
]
DESC_EN = [
    "Lions, a snowman and little dragons welcome the New Year, the couplet wishing wealth to arrive with spring. A red-hot opening.",
    "A deer on a bench and a Ferris wheel, balloons woven with hearts — February's romance meets the afterglow of the New Year.",
    "Spring planting: a rabbit and the mascot water a sapling, a \"protect the environment\" sign planted among the flowers.",
    "The bustle of a wet-weather market: in front of the mall's red-and-white awnings, fortune figures with umbrellas step through puddles.",
    "In a warm kitchen a dragon in an apron cooks, another hugs a bouquet, and the shopping basket overflows with good wishes.",
    "Sunny sand and straw parasols; a fortune bag in a swim ring soaks in the shallows. Peak summer ease.",
    "Summer at the lotus pond: a little dragon dozes on a leaf, goldfish drift by and the lotus half-opens. A cool summer.",
    "The neighbourhood flavour of the \"Pingyuan corner shop\": blue-and-white awnings, Pingyuan ice cream, and a cat on the roof.",
    "Autumn harvest at the Pingyuan farm: golden fields, a scarecrow and a harvester — the joy of the yield fills the frame.",
    "National Day: a deer photographs the city celebration amid balloons and bunting, the words \"National Day\" front and centre.",
    "A Thanksgiving turkey dinner: the deer gather round the plate. East and West meet in the same celebration.",
    "The Christmas cabin lights its string lights and the mascot climbs a ladder to dress the tree. The year's story closes full circle.",
]

for i in range(12):
    n = i + 1
    K(f"pc.pl.ill{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    K(f"pc.pl.ill{n}.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    K(f"pc.pl.cal{n}.t", MONTH_CN_PLAIN[i], MONTH_ES[i], MONTH_EN[i])
    K(f"pc.pl.cal{n}.s", "公历 · 农历 · 优惠券", "Gregoriano · lunar · cupones", "Solar · lunar · coupons")
    K(f"pc.m{n}.name", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    # 副行：中文版显示拉丁月名（设计稿原样）；西/英版把中文序数名留作装饰性呼应
    K(f"pc.m{n}.en", MONTH_EN[i].upper(), MONTH_CN[i], MONTH_CN[i])
    K(f"pc.m{n}.desc", DESC_ZH[i], DESC_ES[i], DESC_EN[i])
    K(f"pc.m{n}.ill.t", "插画页", "Ilustración", "Illustration")
    K(f"pc.m{n}.ill.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    K(f"pc.m{n}.cal.t", "日历页", "Calendario", "Calendar")
    K(f"pc.m{n}.cal.s", TERMS_ZH[i], TERMS_ES[i], TERMS_EN[i])

# ---- 06 封底 · 尾声 ----
K("pc.cl.back.t", "封底", "Contracubierta", "Back cover")
K("pc.cl.back.s", "苹果「平平」化身「0」· 品牌落款",
  "«Pingping» convertida en «0» · firma de marca",
  "\"Pingping\" as the \"0\" · brand sign-off")
K("pc.cl.sum.t", "年终总结", "Cierre del año", "Year-end summary")
K("pc.cl.sum.s", "留白书写 · 年度收官",
  "Espacio en blanco para escribir · cierre del año",
  "Blank space to write · closing the year")

# ---- 页脚 ----
K("pc.footer.note", "平原商场 · 2018 戊戌年台历设计 — 作品集展示",
  "Pingyuan Mall · Calendario anual 2018 — Presentación de proyecto",
  "Pingyuan Mall · 2018 Annual Calendar — Project showcase")
K("pc.backtop", "返回顶部", "Volver arriba", "Back to top")

VD = {k: (zh, es, en) for k, zh, es, en in TRI}
ORDER = [k for k, _, _, _ in TRI]


def zh(key):
    return VD[key][0]


# ============================================================
# 二、写入 assets/js/i18n.js（按标记幂等）
# ============================================================
def js_str(v):
    """输出为单引号 JS 字符串（与 i18n.js 现有风格一致）。"""
    return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"


def i18n_block(lang_index):
    lines = ["", "    /* ---- 作品专题页：平原商场 · 2018 台历 ---- */"]
    width = max(len(k) for k in ORDER) + 3
    for key in ORDER:
        val = VD[key][lang_index]
        lines.append(f"    {("'" + key + "'").ljust(width)}: {js_str(val)},")
    lines.append("    " + END)
    return "\n".join(lines)


def patch_i18n():
    src = io_read(I18N)
    lines = src.split("\n")
    close_idx = [i for i, l in enumerate(lines) if re.match(r"^  \}\s*,?\s*$", l)]
    if len(close_idx) != 3:
        raise SystemExit(f"i18n.js 结构异常：预期 3 个语言块闭合，实际 {len(close_idx)}")
    # 先移除旧块（幂等）：连同行首缩进与行尾换行一起删，
    # 与插入严格互逆——否则每跑一次会多留一行空白
    if BEGIN in src:
        src = re.sub(r"[ \t]*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n",
                     "", src, flags=re.S)
        io_write(I18N, src)
        lines = src.split("\n")
        close_idx = [i for i, l in enumerate(lines) if re.match(r"^  \}\s*,?\s*$", l)]
    if len(close_idx) != 3:
        raise SystemExit(f"清理后结构异常：{len(close_idx)}")
    out = list(lines)
    # 从后往前插，避免索引位移
    for lang_index, ci in reversed(list(enumerate(close_idx))):
        block = f"    {BEGIN}{i18n_block(lang_index)}"
        out.insert(ci, block)
    io_write(I18N, "\n".join(out))
    return len(ORDER)


# ============================================================
# 三、生成 HTML
# ============================================================
def e(v):
    """静态兜底文本：与 verify.py 的 _esc 规则一致（只转 &<>）。"""
    return html.escape(v, quote=False)


# 说明文案里的 **强调** 会被 main.js 的 i18n 注入转成 <strong>；
# 静态兜底（无 JS / 爬虫）也一并转成真标签，而不是把星号露出来。
# 注意：这类节点的 innerHTML 含 <，会被 verify.py 的漂移检查正则跳过（而非误报）。
_BOLD = re.compile(r"\*\*([^*]+)\*\*")


def rich(v):
    return _BOLD.sub(r"<strong>\1</strong>", e(v))


def txt(tag, key, cls=None, extra="", indent=""):
    c = f' class="{cls}"' if cls else ""
    return f'{indent}<{tag}{c}{extra} data-i18n="{key}">{rich(zh(key))}</{tag}>'


def plate_card(img, key_t, key_s, cap_cls="pc-plate__cap", card_cls="pc-plate", lazy=True):
    alt = e(zh(key_s))
    lz = ' loading="lazy"' if lazy else ""
    return f"""        <figure class="{card_cls}" data-pc-card>
          <div class="pc-plate__frame">
            <img src="{img}" alt="{alt}"{lz} data-pc-plate data-i18n-alt="{key_s}">
          </div>
          <figcaption class="{cap_cls}" data-pc-cap>
            <b data-i18n="{key_t}">{e(zh(key_t))}</b><span data-i18n="{key_s}">{e(zh(key_s))}</span>
          </figcaption>
        </figure>"""


def build_body():
    o = []
    A = o.append

    # ---- 子导航 ----
    A('    <nav class="pc-subnav" aria-label="页内导航">')
    A('      <div class="container pc-subnav__inner">')
    for sid, key in [("pc-overview", "pc.nav.overview"), ("pc-features", "pc.nav.features"),
                     ("pc-mockups", "pc.nav.mockups"), ("pc-flat", "pc.nav.flat"),
                     ("pc-months", "pc.nav.months")]:
        A(f'        <button class="pc-subnav__link" type="button" data-pc-scroll="{sid}"'
          f' data-i18n="{key}">{e(zh(key))}</button>')
    A(f'        <a class="pc-subnav__back" href="__WORKS__" data-i18n="pc.nav.back">{e(zh("pc.nav.back"))}</a>')
    A("      </div>")
    A("    </nav>")

    # ---- Hero ----
    A('    <header class="pc-hero">')
    A('      <div class="container pc-hero__grid">')
    A("        <div>")
    A(f'          <span class="eyebrow" data-i18n="pc.hero.kicker">{e(zh("pc.hero.kicker"))}</span>')
    A(f'          <h1 class="pc-hero__title" data-i18n="pc.hero.title">{e(zh("pc.hero.title"))}</h1>')
    A(f'          <p class="pc-hero__sub" data-i18n="pc.hero.sub">{e(zh("pc.hero.sub"))}</p>')
    A(f'          <p class="pc-hero__desc" data-i18n="pc.hero.desc">{e(zh("pc.hero.desc"))}</p>')
    A('          <div class="pc-stats">')
    for n, key in [("28", "pc.stat.pages"), ("12", "pc.stat.months"),
                   ("14", "pc.stat.sheets"), ("1", "pc.stat.mascot")]:
        A(f'            <div class="pc-stat"><b>{n}</b>'
          f'<span data-i18n="{key}">{e(zh(key))}</span></div>')
    A("          </div>")
    A("        </div>")
    A('        <figure class="pc-hero__figure">')
    A(f'          <img src="{IMG}/mockup-hero.jpg" alt="{e(zh("pc.hero.figcap"))}"'
      f' data-i18n-alt="pc.hero.figcap">')
    A(f'          <figcaption data-i18n="pc.hero.figcap">{e(zh("pc.hero.figcap"))}</figcaption>')
    A("        </figure>")
    A("      </div>")
    A("    </header>")

    def head2(num, key_t):
        """区块头：序号 + 中文标题（挂 i18n）+ 英文装饰标签。"""
        tag_key = key_t + ".tag"
        return f"""        <div class="pc-head">
          <h2 class="pc-head__title"><span class="pc-head__num">{num}</span><span data-i18n="{key_t}">{e(zh(key_t))}</span></h2>
          <span class="pc-head__tag" data-i18n="{tag_key}">{e(zh(tag_key))}</span>
        </div>"""

    # ---- 01 项目概览 ----
    A('    <section class="pc-section" id="pc-overview">')
    A('      <div class="container">')
    A(head2("01", "pc.sec.overview"))
    A('        <div class="pc-overview">')
    A('          <dl class="pc-info">')
    for key in ["client", "type", "year", "pages", "extra"]:
        A('            <div class="pc-info__row">')
        A(txt("dt", f"pc.ov.{key}.k", None, ""))
        A(txt("dd", f"pc.ov.{key}.v", None, ""))
        A("            </div>")
    A("          </dl>")
    A('          <div class="pc-overview__copy">')
    A(txt("p", "pc.ov.p1", None, "", indent="            "))
    A(txt("p", "pc.ov.p2", None, "", indent="            "))
    A('            <ul class="pc-points">')
    for i in range(1, 5):
        A(f'              <li data-i18n="pc.ov.point{i}">{e(zh(f"pc.ov.point{i}"))}</li>')
    A("            </ul>")
    A("          </div>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 02 设计亮点 ----
    A('    <section class="pc-section" id="pc-features">')
    A('      <div class="container">')
    A(head2("02", "pc.sec.features"))
    A('        <div class="pc-features">')
    for i in range(1, 5):
        A('          <article class="pc-feature">')
        A(f'            <span class="pc-feature__no" data-i18n="pc.ft{i}.no">{e(zh(f"pc.ft{i}.no"))}</span>')
        A(f'            <h3 data-i18n="pc.ft{i}.t">{e(zh(f"pc.ft{i}.t"))}</h3>')
        A(f'            <p data-i18n="pc.ft{i}.p">{e(zh(f"pc.ft{i}.p"))}</p>')
        A("          </article>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 03 样机 ----
    A('    <section class="pc-section" id="pc-mockups">')
    A('      <div class="container">')
    A(head2("03", "pc.sec.mockups"))
    A('        <div class="pc-mockups">')
    for img, key in [("mockup-spread.jpg", "pc.mk1.cap"), ("mockup-hero.jpg", "pc.mk2.cap")]:
        A('          <figure class="pc-mockup">')
        A(f'            <img src="{IMG}/{img}" alt="{e(zh(key))}" loading="lazy" data-i18n-alt="{key}">')
        A(f'            <figcaption data-i18n="{key}">{e(zh(key))}</figcaption>')
        A("          </figure>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 04 平铺图 ----
    A('    <section class="pc-section" id="pc-flat">')
    A('      <div class="container">')
    A(head2("04", "pc.sec.flat"))
    A('        <div class="pc-flat" data-pc-plates>')
    # 每组的 (分组键, [(图卡键后缀, 文件名)])——文件名与 assets 里的语义命名一一对应
    groups = [
        ("pc.fg1", [("cover", "cover"), ("back", "backcover"),
                    ("plan", "plan"), ("summary", "summary")]),
        ("pc.fg2", [(f"ill{i}", f"ill-{i:02d}") for i in range(1, 13)]),
        ("pc.fg3", [(f"cal{i}", f"cal-{i:02d}") for i in range(1, 13)]),
    ]
    for gkey, items in groups:
        A('          <div class="pc-flat__group">')
        A(f'            <div class="pc-flat__sub"><h3 data-i18n="{gkey}.t">{e(zh(gkey + ".t"))}</h3>'
          f'<span data-i18n="{gkey}.n">{e(zh(gkey + ".n"))}</span></div>')
        A('            <div class="pc-grid">')
        for key_slug, fname in items:
            A(plate_card(f"{IMG}/{fname}.jpg", f"pc.pl.{key_slug}.t", f"pc.pl.{key_slug}.s"))
        A("            </div>")
        A("          </div>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 05 逐月作品 ----
    A('    <section class="pc-section" id="pc-months">')
    A('      <div class="container">')
    A(head2("05", "pc.sec.months"))
    for i in range(1, 13):
        A('        <div class="pc-month">')
        A('          <div class="pc-month__head">')
        A(f'            <span class="pc-month__no">{i:02d}</span>')
        A(f'            <h3 class="pc-month__name" data-i18n="pc.m{i}.name">{e(zh(f"pc.m{i}.name"))}</h3>')
        A(f'            <div class="pc-month__en" data-i18n="pc.m{i}.en">{e(zh(f"pc.m{i}.en"))}</div>')
        A(f'            <p class="pc-month__desc" data-i18n="pc.m{i}.desc">{e(zh(f"pc.m{i}.desc"))}</p>')
        A("          </div>")
        A('          <div class="pc-month__pages">')
        A(plate_card(f"{IMG}/ill-{i:02d}.jpg", f"pc.m{i}.ill.t", f"pc.m{i}.ill.s"))
        A(plate_card(f"{IMG}/cal-{i:02d}.jpg", f"pc.m{i}.cal.t", f"pc.m{i}.cal.s"))
        A("          </div>")
        A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 06 封底 · 尾声 ----
    A('    <section class="pc-section" id="pc-closing">')
    A('      <div class="container">')
    A(head2("06", "pc.sec.closing"))
    A('        <div class="pc-closing">')
    A(plate_card(f"{IMG}/backcover.jpg", "pc.cl.back.t", "pc.cl.back.s"))
    A(plate_card(f"{IMG}/summary.jpg", "pc.cl.sum.t", "pc.cl.sum.s"))
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 上下篇导航 + 页脚说明 ----
    A('    <div class="container">')
    A('      <nav class="work-nav" data-pc-worknav>')
    A('        <a data-pc-prev href="__WORKS__">←</a>')
    A(f'        <a href="__WORKS__" data-i18n="pc.nav.back">{e(zh("pc.nav.back"))}</a>')
    A('        <a data-pc-next href="__WORKS__">→</a>')
    A("      </nav>")
    A('      <div class="pc-outer">')
    A(f'        <p data-i18n="pc.footer.note">{e(zh("pc.footer.note"))}</p>')
    A(f'        <button class="pc-backtop" type="button" data-pc-backtop data-i18n="pc.backtop">{e(zh("pc.backtop"))}</button>')
    A("      </div>")
    A("    </div>")
    return "\n".join(o)


def extract(pattern, src):
    m = re.search(pattern, src, re.S)
    if not m:
        raise SystemExit(f"未能从 {DETAIL} 抽取：{pattern}")
    return m.group(0)


def io_read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def io_write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def build_html():
    """导航与页脚从 work-detail.html 原样抽取复用（站点导航改动后重跑即可同步）；
    资源查询串也跟着取，保持全站版本号一致。"""
    detail = io_read(DETAIL)
    nav = extract(r"  <nav class=\"nav\">.*?\n  </nav>", detail)
    footer = extract(r"  <footer class=\"footer\">.*?\n  </footer>", detail)
    ver = re.search(r"main\.css\?v(\d+)", detail)
    if not ver:
        raise SystemExit("未能从 work-detail.html 取到资源版本号")
    v = "v" + ver.group(1)
    body = build_body().replace("__WORKS__", f"works.html?{v}")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Cache-Control" content="no-cache">
  <meta http-equiv="Pragma" content="no-cache">
  <script>document.documentElement.className += " js";</script>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#fafaf8">
  <meta name="description" content="{e(zh("pc.meta.desc"))}" data-i18n-content="pc.meta.desc">
  <title data-i18n="pc.meta.title">{e(zh("pc.meta.title"))}</title>
  <link rel="icon" type="image/svg+xml" href="assets/images/favicon.svg">
  <link rel="stylesheet" href="assets/css/main.css?{v}">
  <link rel="stylesheet" href="assets/css/work-pingyuan.css?{v}">
</head>
<body data-lang="zh">

{nav}

  <main class="pc" data-work-id="{WORK_ID}">

{body}

  </main>

{footer}

  <script src="assets/js/i18n.js?{v}"></script>
  <script src="assets/js/data.js?{DATA_HASH}"></script>
  <script src="assets/js/site-data.js?{SITE_HASH}"></script>
  <script src="assets/js/main.js?{v}"></script>
</body>
</html>
"""


if __name__ == "__main__":
    data_hash = re.search(r"assets/js/data\.js\?h=([0-9a-f]+)", io_read(DETAIL))
    site_hash = re.search(r"assets/js/site-data\.js\?h=([0-9a-f]+)", io_read(DETAIL))
    DATA_HASH = "h=" + (data_hash.group(1) if data_hash else "0")
    SITE_HASH = "h=" + (site_hash.group(1) if site_hash else "0")
    n = patch_i18n()
    io_write(OUT_HTML, build_html())
    print(f"i18n.js  ← {n} 个 pc.* 键 × 3 语言")
    print(f"页面      ← work-pingyuan-calendar.html")
