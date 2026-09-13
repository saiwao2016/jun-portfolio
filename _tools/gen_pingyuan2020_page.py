#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「平原商场 · 2020 庚子鼠年台历设计」作品专题页（三语）。

文案唯一真源在此（K 函数），由 pingyuan_common.build 同时产出：
  (a) assets/js/i18n.js 里 zh/es/en 三个语言块的 pc20.* 键（按标记幂等插入）
  b) work-pingyuan2020-calendar.html（静态兜底 = 中文值，零漂移）

用法：python3 _tools/gen_pingyuan2020_page.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pingyuan_common import make_registrar, build

K, TRI, KEYS = make_registrar()
prefix = "pc20"


def P(key, zh, es, en):
    K(key, zh, es, en)
    return zh


# ---- 页面元信息 ----
P("pc20.meta.title", "平原商场 · 2020 庚子鼠年台历设计 — JUN",
  "Pingyuan Mall · Calendario anual 2020 — JUN",
  "Pingyuan Mall · 2020 Annual Calendar — JUN")
P("pc20.meta.desc",
  "平原商场 2020 庚子鼠年台历设计：以苹果「平平」为品牌吉祥物，2 个品牌扉页、12 个月楼层主题插画、12 页功能日历，跟着平平逛遍商场每一层。平面设计作品，周骏（JUN）设计。",
  "Calendario anual 2020 del centro comercial Pingyuan: la manzana «Pingping» como mascota de marca, dos páginas de apertura de marca, 12 ilustraciones temáticas por plantas y 12 páginas de calendario funcional. Diseño gráfico de JUN (Zhou Jun).",
  "The 2020 annual calendar for Pingyuan Mall: the apple mascot \"Pingping\", two brand opening pages, 12 floor-themed illustrations and 12 functional calendar pages — follow Pingping through every floor. Graphic design by JUN (Zhou Jun).")

# ---- 页内子导航 ----
P("pc20.nav.overview", "项目概览", "Resumen", "Overview")
P("pc20.nav.features", "设计亮点", "Destacados", "Highlights")
P("pc20.nav.mockups", "样机展示", "Maquetas", "Mockups")
P("pc20.nav.flat", "平铺图", "Láminas", "Flat layout")
P("pc20.nav.months", "逐月作品", "Mes a mes", "Month by month")
P("pc20.nav.back", "返回作品集", "Volver a proyectos", "Back to works")

# ---- Hero ----
P("pc20.hero.kicker", "DESIGN PORTFOLIO · 2020", "DESIGN PORTFOLIO · 2020", "DESIGN PORTFOLIO · 2020")
P("pc20.hero.title", "平原商场", "Pingyuan Mall", "Pingyuan Mall")
P("pc20.hero.sub", "2020 庚子鼠年台历设计",
  "Calendario anual 2020 · Año de la Rata",
  "2020 Annual Calendar · Year of the Rat")
P("pc20.hero.desc",
  "一套以苹果吉祥物「平平」为主角的年度台历：2 个品牌扉页、12 个月楼层主题插画、12 页功能日历，跟着平平逛遍商场每一层，既是时间工具，也是商场全年的品牌画卷。",
  "Un calendario anual protagonizado por la manzana «Pingping»: dos páginas de apertura de marca, 12 ilustraciones temáticas por plantas y 12 páginas de calendario funcional; acompaña a Pingping por cada piso del centro — a la vez herramienta de tiempo y retrato de marca del año.",
  "An annual calendar led by the apple mascot Pingping: two brand opening pages, 12 floor-themed illustrations and 12 functional calendar pages — follow Pingping through every floor, both a date tool and a year-long brand canvas.")
P("pc20.hero.figcap", "封面样机 · 桌面展示",
  "Maqueta de cubierta · Escritorio", "Cover mockup · Desktop")
P("pc20.stat.pages", "个版面", "láminas", "plates")
P("pc20.stat.months", "个主题月", "meses temáticos", "themed months")
P("pc20.stat.sheets", "个品牌扉页", "págs. de apertura", "opening pages")
P("pc20.stat.mascot", "个吉祥物", "mascota", "mascot")

# ---- 六个区块标题 ----
P("pc20.sec.overview", "项目概览", "Resumen del proyecto", "Project overview")
P("pc20.sec.overview.tag", "PROJECT OVERVIEW", "PROJECT OVERVIEW", "PROJECT OVERVIEW")
P("pc20.sec.features", "设计亮点", "Destacados del diseño", "Design highlights")
P("pc20.sec.features.tag", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS")
P("pc20.sec.mockups", "样机展示", "Maquetas", "Mockups")
P("pc20.sec.mockups.tag", "MOCKUPS", "MOCKUPS", "MOCKUPS")
P("pc20.sec.flat", "平铺图展示", "Láminas planas", "Flat layout")
P("pc20.sec.flat.tag", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES")
P("pc20.sec.months", "逐月作品", "Mes a mes", "Month by month")
P("pc20.sec.months.tag", "MONTH BY MONTH", "MONTH BY MONTH", "MONTH BY MONTH")
P("pc20.sec.closing", "封底 · 尾声", "Contracubierta y cierre", "Back cover & closing")
P("pc20.sec.closing.tag", "BACK COVER & CLOSING", "BACK COVER & CLOSING", "BACK COVER & CLOSING")

# ---- 01 项目概览 ----
P("pc20.ov.client.k", "客户", "Cliente", "Client")
P("pc20.ov.client.v", "平原商场 Pingyuan Mall", "Centro comercial Pingyuan", "Pingyuan Mall")
P("pc20.ov.type.k", "项目类型", "Tipo", "Type")
P("pc20.ov.type.v", "年度台历 · 平面设计", "Calendario anual · Diseño gráfico", "Annual calendar · Graphic design")
P("pc20.ov.year.k", "设计年份", "Año", "Year")
P("pc20.ov.year.v", "2020 · 庚子鼠年", "2020 · Año de la Rata", "2020 · Year of the Rat")
P("pc20.ov.pages.k", "页数", "Páginas", "Pages")
P("pc20.ov.pages.v", "28 个版面", "28 láminas", "28 plates")
P("pc20.ov.mascot.k", "吉祥物", "Mascota", "Mascot")
P("pc20.ov.mascot.v", "平平（苹果延伸形象）", "Pingping (de una manzana)", "Pingping (apple-derived)")
P("pc20.ov.p1",
  "这是为**平原商场**打造的 2020 年度台历。封面以庚子鼠年喜庆氛围开场，苹果吉祥物「平平」与老鼠形象同框，红色囍字建筑、烟花灯笼烘托新年气氛。",
  "Es el calendario anual 2020 creado para **Pingyuan Mall**. La cubierta abre con el ambiente festivo del Año de la Rata: la manzana «Pingping» comparte escena con ratones, y un edificio con el carácter 囍, fuegos artificiales y faroles realzan el aire de Año Nuevo.",
  "This is the 2020 annual calendar made for **Pingyuan Mall**. The cover opens in festive Year-of-the-Rat mood — the apple mascot Pingping shares the frame with mice, while a 囍-character building, fireworks and lanterns set the New Year tone.")
P("pc20.ov.p2",
  "扉页设置**「荣誉历程」**与**「企业文化」**两个品牌页面，展示商场历年荣誉与经营理念。每月一幅**楼层主题插画**，平平带着家人朋友逛遍商场各楼层——从 1 楼名表化妆品到 7 楼羽绒服卖场，从童装特卖到家电清洗，把商场的业态地图画进了一整年。",
  "Las páginas de apertura presentan **«Honours 荣誉历程»** y **«Culture 企业文化»**, dos páginas de marca que muestran los galardones del centro y su filosofía. Cada mes, una **ilustración temática de planta**: Pingping recorre el centro con familia y amigos —del 1º piso de relojes y cosmética al 7º de abrigos, de las rebajas infantiles a la limpieza de electrodomésticos— dibujando el mapa comercial del centro a lo largo de todo el año.",
  "The opening pages present **\"Honours\"** and **\"Culture\"** — two brand pages showing the mall's awards and philosophy. Each month a **floor-themed illustration**: Pingping tours the mall with family and friends — from the 1st-floor watches and cosmetics to the 7th-floor down jackets, from kids' sales to appliance cleaning — drawing the mall's tenant map across the whole year.")
P("pc20.ov.point1", "苹果吉祥物「平平」贯穿全年", "La manzana «Pingping» recorre el año", "The apple mascot runs through the year")
P("pc20.ov.point2", "荣誉历程 + 企业文化双扉页", "Dos aperturas: honores y cultura", "Two opening pages: honours & culture")
P("pc20.ov.point3", "每月对应一个商场楼层/业态", "Cada mes, una planta o negocio", "Each month a mall floor or business")
P("pc20.ov.point4", "十月特别企划：商场 20 周年庆典", "Octubre: 20º aniversario del centro", "October: mall's 20th-anniversary event")

# ---- 02 设计亮点 ----
FEATURES = [
    ("01 — 鼠年封面", "01 — Cubierta Año de la Rata", "01 — Year-of-the-Rat cover",
     "苹果吉祥物「平平」", "Mascota: manzana «Pingping»", "Mascot: apple",
     "「平平」是由苹果延伸而来的吉祥物形象，粉色圆润身体、黄色果柄触角、绿叶尾巴，辨识度极高。2020 鼠年封面中平平与老鼠形象同框，热闹喜庆。",
     "«Pingping» es un personaje nacido de una manzana: cuerpo rosado y redondo, antenas de pedúnculo amarillo y cola de hoja verde, con altísima reconocibilidad. En la cubierta de 2020 comparte escena con ratones, llena de alegría y fiesta.",
     "Pingping is a mascot derived from an apple — pink rounded body, yellow stalk antennae and a green-leaf tail, instantly recognizable. On the 2020 Rat-year cover it shares the frame with mice, festive and lively."),
    ("02 — 双品牌扉页", "02 — Dos aperturas de marca", "02 — Two brand opening pages",
     "荣誉历程 + 企业文化", "Honours + Culture", "Honours + Culture",
     "台历开篇设置两个品牌扉页：「Honours 荣誉历程」以时间轴展示商场历年荣誉，「Culture 企业文化」传递经营理念，让台历兼具品牌手册功能。",
     "El calendario abre con dos páginas de marca: «Honours» muestra en una línea de tiempo los galardones del centro a lo largo de los años, y «Culture» transmite su filosofía de gestión, dando al calendario también función de manual de marca.",
     "The calendar opens with two brand pages: \"Honours\" displays the mall's past awards on a timeline, and \"Culture\" conveys its management philosophy — giving the calendar the added role of a brand handbook."),
    ("03 — 楼层主题插画", "03 — Ilustración de planta", "03 — Floor-themed illustration",
     "12 个月逛遍整座商场", "12 meses por todo el centro", "12 months across the whole mall",
     "每月插画对应一个楼层或业态：1F 名表化妆品、2F 女鞋箱包、3F 男装、4F 童装女装、5F 女装内衣、6F 童装特卖、7F 羽绒服，外加运动休闲、家电、珠宝和 20 周年庆典。",
     "Cada mes la ilustración corresponde a una planta o negocio: relojes y cosmética en 1F, zapatos y bolsos en 2F, ropa de hombre en 3F, ropa infantil y femenina en 4F, ropa interior femenina en 5F, rebajas infantiles en 6F, abrigos en 7F, más deportes, electrodomésticos, joyería y la fiesta del 20º aniversario.",
     "Each month's illustration matches a floor or business: watches and cosmetics on 1F, shoes and bags on 2F, menswear on 3F, kids' and women's wear on 4F, lingerie on 5F, kids' sales on 6F, down jackets on 7F, plus sports, appliances, jewellery and the 20th-anniversary celebration."),
    ("04 — 功能型日历页", "04 — Página funcional", "04 — Functional calendar page",
     "节气节日 + 品牌信息", "Términos solares + marca", "Solar terms + brand info",
     "日历页标注公历、农历、节气与传统节日，底部印有「平原商场 咱老百姓的商场」品牌语，翻页之间持续传递品牌温度。",
     "La página de calendario anota fechas gregorianas y lunares, términos solares y festividades tradicionales, e imprime al pie el lema de marca «Pingyuan, el centro del pueblo», transmitiendo el calor de la marca a cada paso.",
     "The calendar page marks solar and lunar dates, solar terms and traditional festivals, and prints the brand line \"Pingyuan — the mall of the people\" at the foot, carrying the brand's warmth with every turn."),
]
for i, (no_zh, no_es, no_en, t_zh, t_es, t_en, p_zh, p_es, p_en) in enumerate(FEATURES, 1):
    P(f"pc20.ft{i}.no", no_zh, no_es, no_en)
    P(f"pc20.ft{i}.t", t_zh, t_es, t_en)
    P(f"pc20.ft{i}.p", p_zh, p_es, p_en)

# ---- 03 样机 ----
P("pc20.mk1.cap", "双页展开 · 一月插画与日历",
  "Doble página abierta · Ilustración y calendario",
  "Spread · illustration and calendar page")
P("pc20.mk2.cap", "立式桌面 · 封面主视觉",
  "En pie sobre la mesa · Portada", "Standing on a desk · Cover key visual")

# ---- 04 平铺图分组标题 ----
P("pc20.fg1.t", "封面 · 扉页 · 封底", "Cubierta, apertura y contracubierta", "Cover · opening · back cover")
P("pc20.fg1.n", "4 PAGES", "4 LÁMINAS", "4 PLATES")
P("pc20.fg2.t", "12 个月楼层主题插画页", "12 ilustraciones temáticas de planta", "12 floor-themed illustration pages")
P("pc20.fg2.n", "ILLUSTRATION PAGES", "ILUSTRACIONES", "ILLUSTRATIONS")
P("pc20.fg3.t", "12 个月功能日历页", "12 páginas de calendario funcional", "12 functional calendar pages")
P("pc20.fg3.n", "CALENDAR PAGES", "CALENDARIO", "CALENDAR PAGES")

# ---- 平铺图：封面组（cover / honours / culture / back）----
PLATES_HEAD = [
    ("cover", "封面", "Cubierta", "Cover",
     "2020 鼠年主视觉", "Visual Año Nuevo 2020", "2020 New Year key visual"),
    ("honours", "扉页 · 荣誉历程", "Apertura · Honours", "Opening · Honours",
     "历年荣誉时间轴", "Línea de honores", "Awards timeline"),
    ("culture", "扉页 · 企业文化", "Apertura · Culture", "Opening · Culture",
     "经营理念", "Filosofía de gestión", "Management philosophy"),
    ("back", "封底", "Contracubierta", "Back cover",
     "咱老百姓的商场", "El centro del pueblo", "The people's mall"),
]
for slug, t_zh, t_es, t_en, s_zh, s_es, s_en in PLATES_HEAD:
    P(f"pc20.pl.{slug}.t", t_zh, t_es, t_en)
    P(f"pc20.pl.{slug}.s", s_zh, s_es, s_en)

# ---- 12 个月：中文序数名 / 西英月名 / 插画主题 / 节气 ----
MONTH_CN = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
MONTH_EN = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]

THEME_ZH = ["平原来喜 · 新年", "平原珠宝城", "2F 女鞋箱包", "3F 男装", "4F 童装女装",
            "6F 童装特卖", "1F 名表化妆品", "运动休闲", "八方名品家电", "20 周年庆典",
            "7楼羽绒服卖场", "5F 女装内衣"]
THEME_ES = ["Pingyuan da la alegría", "Joyas Pingyuan", "Zapatos y bolsos 2F", "Ropa hombre 3F", "Ropa infantil y femenina 4F",
            "Rebajas infantiles 6F", "Relojes y cosmética 1F", "Deporte y ocio", "Electrodomésticos Bafang", "20º aniversario",
            "Abrigos 7º piso", "Ropa interior 5F"]
THEME_EN = ["Pingyuan Welcomes Joy", "Pingyuan Jewellery City", "2F shoes & bags", "3F menswear", "4F kids & women's wear",
            "6F kids' clearance", "1F watches & cosmetics", "Sports & leisure", "Bafang appliances", "20th anniversary",
            "7F down-jacket store", "5F lingerie"]

TERMS_ZH = ["元旦 · 小寒 · 大寒 · 腊八", "立春 · 除夕 · 春节 · 元宵", "惊蛰 · 春分 · 妇女节", "清明 · 谷雨",
            "立夏 · 小满 · 母亲节", "芒种 · 夏至 · 端午 · 儿童节", "小暑 · 大暑", "立秋 · 处暑",
            "白露 · 秋分 · 中秋 · 教师节", "寒露 · 霜降 · 国庆", "立冬 · 小雪 · 感恩节", "大雪 · 冬至 · 平安夜 · 圣诞"]
TERMS_ES = ["Año Nuevo · Frío menor · Frío mayor · Fest. Laba",
            "Inicio prima. · Nochevieja · Año Nuevo · Farolillos",
            "Despertar insectos · Equinoccio prima. · Día mujer",
            "Claridad pura · Lluvia grano",
            "Inicio verano · Plenitud menor · Día madre",
            "Espiga en espiga · Solsticio verano · Bote dragón · Día niño",
            "Calor menor · Calor mayor", "Inicio otoño · Fin calor",
            "Rocío blanco · Equinoccio otoño · Medio Otoño · Día maestro",
            "Rocío frío · Caída escarcha · Fiesta Nacional",
            "Inicio invierno · Nieve menor · Día Acción Gracias",
            "Nieve mayor · Solsticio invierno · Nochebuena · Navidad"]
TERMS_EN = ["New Year's Day · Minor Cold · Major Cold · Laba",
            "Start of Spring · CNY Eve · Spring Festival · Lantern Festival",
            "Awakening Insects · Spring Equinox · Women's Day",
            "Pure Brightness · Grain Rain",
            "Start of Summer · Grain Full · Mother's Day",
            "Grain in Ear · Summer Solstice · Dragon Boat · Children's Day",
            "Minor Heat · Major Heat", "Start of Autumn · End of Heat",
            "White Dew · Autumn Equinox · Mid-Autumn · Teachers' Day",
            "Cold Dew · Frost's Descent · National Day",
            "Start of Winter · Minor Snow · Thanksgiving",
            "Major Snow · Winter Solstice · Christmas Eve · Christmas"]

DESC_ZH = [
    "「平原来喜」，平平一家围坐年夜饭，红灯笼、福字、烟花，新年团圆的温暖开场。",
    "平原珠宝城前，平平戴着珍珠项链与伴侣交换戒指，猫咪在旁求婚，浪漫情人节。",
    "2F 女鞋箱包区，New!! 高跟鞋海报醒目，3 月 8 日妇女节，平平捧着花束登场。",
    "3F 男装区，羊毛衫新品上市，平平在试衣间前试穿西装，另一只平平帮忙选裤子。",
    "4F 童装女装区化身花园，长翅膀的平平在花丛中挑选新衣，树枝上挂满衣架。",
    "6F 童装特卖 SALE，宝箱里装满婴儿衣服，泰迪熊和大猫陪着宝宝平平，儿童节狂欢。",
    "1F 名表化妆品区，MAC 口红、腕表、粉饼一字排开，三只平平围着化妆台臭美。",
    "运动休闲专区，佐丹奴、贵人鸟、匹克、龙狮戴尔齐聚，篮球网球羽毛球，平平活力满满。",
    "八方名品家电区，冰箱、洗衣机、厨房电器一应俱全，平平体验家电清洗服务，焕然一新。",
    "平原商场盛大开业 20 周年！囍字建筑、蛋糕、礼物、灯笼，平平家族全员到场庆祝。",
    "「天冷了买羽绒服就到平原商场 7 楼」，雪人陪着平平逛羽绒服专业卖场，全市最低价。",
    "5F 女装内衣区，圣诞树、礼物、彩灯环绕，「美丽与舒适从五楼开始」，温暖收官。",
]
DESC_ES = [
    "«Pingyuan da la bienvenida a la alegría»: la familia de Pingping se reúne para la cena de Nochevieja; faroles rojos, caracteres fu y fuegos artificiales abren el cálido reencuentro.",
    "Ante la Joyería Pingyuan, Pingping lleva un collar de perlas e intercambia anillos con su pareja mientras un gato propone matrimonio: un romántico Día de San Valentín.",
    "En la zona de zapatos y bolsos del 2F, un cartel de «¡Nuevo!!» tacones destaca; por el Día de la Mujer (8 mar) Pingping aparece con un ramo.",
    "En la ropa de hombre del 3F llegan nuevos suéteres de lana; Pingping prueba un traje ante el probador mientras otro Pingping ayuda a elegir pantalones.",
    "La zona de ropa infantil y femenina del 4F se vuelve un jardín; una Pingping alada elige ropa nueva entre las flores, con perchas colgando de las ramas.",
    "Rebajas infantiles SALE en el 6F: un cofre lleno de ropa de bebé, osos de peluche y un gran gato acompañan al bebé Pingping en el carnaval del Día del Niño.",
    "En relojes y cosmética del 1F, pintalabios MAC, relojes y polvos se alinean; tres Pingping se arreglan junto al tocador.",
    "En la zona de deporte y ocio se reúnen Giordano, Guirenniao, Peak y Longshi-Dale; baloncesto, tenis y bádminton: Pingping lleno de energía.",
    "En electrodomésticos de Bafang hay neveras, lavadoras y aparatos de cocina; Pingping prueba la limpieza de electrodomésticos y sale como nuevo.",
    "¡20º aniversario de Pingyuan Mall! Un edificio con el carácter 囍, pastel, regalos y faroles: toda la familia Pingping acude a celebrar.",
    "«Cuando hace frío, los abrigos se compran en el 7º piso de Pingyuan»: un muñeco de nieve acompaña a Pingping por la tienda especializada de abrigos, los precios más bajos de la ciudad.",
    "En la ropa interior del 5F, árboles de Navidad, regalos y luces rodean a Pingping; «La belleza y la comodidad empiezan en el 5º piso»: un cálido final.",
]
DESC_EN = [
    "\"Pingyuan Welcomes Joy\" — Pingping's family gathers for the New Year's Eve dinner; red lanterns, fu characters and fireworks open the warm reunion.",
    "In front of Pingyuan Jewellery City, Pingping wears a pearl necklace and exchanges rings with a partner while a cat proposes — a romantic Valentine's Day.",
    "At the 2F shoe-and-bag zone, a \"New!!\" high-heel poster stands out; on Women's Day (Mar 8) Pingping appears holding a bouquet.",
    "In the 3F menswear zone, new wool-sweater arrivals; Pingping tries on a suit by the fitting room while another Pingping helps pick trousers.",
    "The 4F kids'-and-women's-wear zone turns into a garden; a winged Pingping picks new clothes among blossoms, clothes hangers hanging from the branches.",
    "6F kids' clearance SALE — a treasure chest full of baby clothes, teddy bears and a big cat keep baby Pingping company for a Children's Day carnival.",
    "At the 1F watch-and-cosmetics zone, MAC lipstick, wristwatches and powder compacts line up; three Pingpings preen around the dressing table.",
    "In the sports-and-leisure zone, Giordano, Guirenniao, Peak and Longshi-Dale gather; basketball, tennis and badminton — Pingping is full of energy.",
    "At the Bafang famous-appliances zone, fridges, washing machines and kitchen appliances are all there; Pingping tries the appliance-cleaning service and comes out refreshed.",
    "Pingyuan Mall's grand 20th anniversary! A 囍-character building, cake, gifts and lanterns — the whole Pingping family shows up to celebrate.",
    "\"When it's cold, buy down jackets on the 7th floor of Pingyuan Mall\" — a snowman accompanies Pingping through the down-jacket specialty store, lowest prices in town.",
    "In the 5F lingerie zone, Christmas trees, gifts and fairy lights surround Pingping; \"Beauty and comfort start on the 5th floor\" — a warm finale.",
]

for i in range(12):
    n = i + 1
    P(f"pc20.pl.ill{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc20.pl.ill{n}.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc20.pl.cal{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc20.pl.cal{n}.s", "公历 · 农历 · 节气", "Gregoriano · lunar · términos", "Solar · lunar · terms")
    P(f"pc20.m{n}.name", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc20.m{n}.en", MONTH_EN[i].upper(), MONTH_CN[i], MONTH_CN[i])
    P(f"pc20.m{n}.desc", DESC_ZH[i], DESC_ES[i], DESC_EN[i])
    P(f"pc20.m{n}.ill.t", "插画页", "Ilustración", "Illustration")
    P(f"pc20.m{n}.ill.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc20.m{n}.cal.t", "日历页", "Calendario", "Calendar")
    P(f"pc20.m{n}.cal.s", TERMS_ZH[i], TERMS_ES[i], TERMS_EN[i])

# ---- 06 封底 · 尾声 ----
P("pc20.cl.back.t", "封底", "Contracubierta", "Back cover")
P("pc20.cl.back.s", "咱老百姓的商场", "El centro del pueblo", "The people's mall")
P("pc20.cl.sum.t", "荣誉历程", "Honours · 历年荣誉", "Honours · Awards")
P("pc20.cl.sum.s", "Honours · 历年荣誉", "Trayectoria de honores", "Awards through the years")

# ---- 页脚 ----
P("pc20.footer.note", "平原商场 · 2020 庚子鼠年台历设计 — 作品集展示",
  "Pingyuan Mall · Calendario anual 2020 — Presentación de proyecto",
  "Pingyuan Mall · 2020 Annual Calendar — Project showcase")
P("pc20.backtop", "返回顶部", "Volver arriba", "Back to top")

VD = {k: (zh, es, en) for k, zh, es, en in TRI}
ORDER = [k for k, _, _, _ in TRI]

config = dict(
    prefix=prefix,
    work_id="pingyuan-calendar-2020",
    out_html="work-pingyuan2020-calendar.html",
    img="assets/works/pingyuan-calendar-2020",
    begin="/* >>> generated: pingyuan-calendar-2020 >>> */",
    end="/* <<< generated: pingyuan-calendar-2020 <<< */",
    nav_back_key="pc20.nav.back",
    overview_rows=["client", "type", "year", "pages", "mascot"],
    features_count=4,
    months_count=12,
    stats=[("28", "pc20.stat.pages"), ("12", "pc20.stat.months"),
           ("2", "pc20.stat.sheets"), ("1", "pc20.stat.mascot")],
    flat_g1=[("cover", "cover"), ("honours", "honours"), ("culture", "culture"), ("back", "backcover")],
    flat_g2=[(f"ill{i}", f"ill-{i:02d}") for i in range(1, 13)],
    flat_g3=[(f"cal{i}", f"cal-{i:02d}") for i in range(1, 13)],
    closing=[("backcover", "pc20.cl.back.t", "pc20.cl.back.s"),
             ("honours", "pc20.cl.sum.t", "pc20.cl.sum.s")],
)

if __name__ == "__main__":
    n, out = build(config, ORDER, VD)
    print(f"i18n.js  ← {n} 个 pc20.* 键 × 3 语言")
    print(f"页面      ← {out}  ({len(ORDER)} 键)")
