#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「平原商场 · 2023 癸卯兔年台历设计」作品专题页（三语）。

文案唯一真源在此（K 函数），由 pingyuan_common.build 同时产出：
  (a) assets/js/i18n.js 里 zh/es/en 三个语言块的 pc23.* 键（按标记幂等插入）
  b) work-pingyuan2023-calendar.html（静态兜底 = 中文值，零漂移）

用法：python3 _tools/gen_pingyuan2023_page.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pingyuan_common import make_registrar, build

K, TRI, KEYS = make_registrar()
prefix = "pc23"


def P(key, zh, es, en):
    K(key, zh, es, en)
    return zh


# ---- 页面元信息 ----
P("pc23.meta.title", "平原商场 · 2023 癸卯兔年台历设计 — JUN",
  "Pingyuan Mall · Calendario anual 2023 — JUN",
  "Pingyuan Mall · 2023 Annual Calendar — JUN")
P("pc23.meta.desc",
  "平原商场 2023 癸卯兔年台历设计：以苹果「平平」为品牌吉祥物，书签双扉页、12 个月楼层主题插画、12 页功能日历，跟着平平逛遍商场每一层。平面设计作品，周骏（JUN）设计。",
  "Calendario anual 2023 del centro comercial Pingyuan: la manzana «Pingping» como mascota de marca, doble página de marcapáginas, 12 ilustraciones temáticas por plantas y 12 páginas de calendario funcional. Diseño gráfico de JUN (Zhou Jun).",
  "The 2023 annual calendar for Pingyuan Mall: the apple mascot \"Pingping\", a double bookmark spread, 12 floor-themed illustrations and 12 functional calendar pages — follow Pingping through every floor. Graphic design by JUN (Zhou Jun).")

# ---- 页内子导航 ----
P("pc23.nav.overview", "项目概览", "Resumen", "Overview")
P("pc23.nav.features", "设计亮点", "Destacados", "Highlights")
P("pc23.nav.mockups", "样机展示", "Maquetas", "Mockups")
P("pc23.nav.flat", "平铺图", "Láminas", "Flat layout")
P("pc23.nav.months", "逐月作品", "Mes a mes", "Month by month")
P("pc23.nav.back", "返回作品集", "Volver a proyectos", "Back to works")

# ---- Hero ----
P("pc23.hero.kicker", "DESIGN PORTFOLIO · 2023", "DESIGN PORTFOLIO · 2023", "DESIGN PORTFOLIO · 2023")
P("pc23.hero.title", "平原商场", "Pingyuan Mall", "Pingyuan Mall")
P("pc23.hero.sub", "2023 癸卯兔年台历设计",
  "Calendario anual 2023 · Año del Conejo",
  "2023 Annual Calendar · Year of the Rabbit")
P("pc23.hero.desc",
  "以苹果吉祥物「平平」为主角的年度台历：兔年封面白兔骑鹿与飞天平平同框、平平书签双扉页可剪下收藏、12 个月楼层主题插画，跟着平平逛遍商场每一层。",
  "Un calendario anual protagonizado por la manzana «Pingping»: portada del Año del Conejo con un conejo blanco a lomos de un ciervo junto a Pingping apsara, doble página de marcapáginas recortables y 12 ilustraciones temáticas por plantas — acompaña a Pingping por cada piso del centro.",
  "An annual calendar led by the apple mascot Pingping: a Rabbit-year cover with a white rabbit riding a deer alongside a flying-apsara Pingping, a double spread of cut-out bookmarks, and 12 floor-themed illustrations — follow Pingping through every floor.")
P("pc23.hero.figcap", "封面样机 · 桌面展示",
  "Maqueta de cubierta · Escritorio", "Cover mockup · Desktop")
P("pc23.stat.pages", "个版面", "láminas", "plates")
P("pc23.stat.months", "个主题月", "meses temáticos", "themed months")
P("pc23.stat.sheets", "个书签扉页", "págs. de marcapáginas", "bookmark pages")
P("pc23.stat.mascot", "个吉祥物", "mascota", "mascot")

# ---- 六个区块标题 ----
P("pc23.sec.overview", "项目概览", "Resumen del proyecto", "Project overview")
P("pc23.sec.overview.tag", "PROJECT OVERVIEW", "PROJECT OVERVIEW", "PROJECT OVERVIEW")
P("pc23.sec.features", "设计亮点", "Destacados del diseño", "Design highlights")
P("pc23.sec.features.tag", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS")
P("pc23.sec.mockups", "样机展示", "Maquetas", "Mockups")
P("pc23.sec.mockups.tag", "MOCKUPS", "MOCKUPS", "MOCKUPS")
P("pc23.sec.flat", "平铺图展示", "Láminas planas", "Flat layout")
P("pc23.sec.flat.tag", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES")
P("pc23.sec.months", "逐月作品", "Mes a mes", "Month by month")
P("pc23.sec.months.tag", "MONTH BY MONTH", "MONTH BY MONTH", "MONTH BY MONTH")
P("pc23.sec.closing", "封底 · 尾声", "Contracubierta y cierre", "Back cover & closing")
P("pc23.sec.closing.tag", "BACK COVER & CLOSING", "BACK COVER & CLOSING", "BACK COVER & CLOSING")

# ---- 01 项目概览 ----
P("pc23.ov.client.k", "客户", "Cliente", "Client")
P("pc23.ov.client.v", "平原商场 Pingyuan Mall", "Centro comercial Pingyuan", "Pingyuan Mall")
P("pc23.ov.type.k", "项目类型", "Tipo", "Type")
P("pc23.ov.type.v", "年度台历 · 平面设计", "Calendario anual · Diseño gráfico", "Annual calendar · Graphic design")
P("pc23.ov.year.k", "设计年份", "Año", "Year")
P("pc23.ov.year.v", "2023 · 癸卯兔年", "2023 · Año del Conejo", "2023 · Year of the Rabbit")
P("pc23.ov.pages.k", "页数", "Páginas", "Pages")
P("pc23.ov.pages.v", "28 个版面", "28 láminas", "28 plates")
P("pc23.ov.mascot.k", "吉祥物", "Mascota", "Mascot")
P("pc23.ov.mascot.v", "平平（苹果延伸形象）", "Pingping (de una manzana)", "Pingping (apple-derived)")
P("pc23.ov.p1",
  "这是为**平原商场**打造的 2023 年度台历。封面以癸卯兔年喜庆氛围开场，白兔戴花冠骑鹿，苹果吉祥物「平平」化作飞天造型——吹笛、弹琵琶、翩翩起舞——天灯、锦鲤、祥云环绕，粉色背景温柔浪漫。",
  "Es el calendario anual 2023 creado para **Pingyuan Mall**. La cubierta abre con el ambiente festivo del Año del Conejo: un conejo blanco con corona floral a lomos de un ciervo, y la manzana «Pingping» convertida en apsara — tocando la flauta, la pipa, danzando — rodeada de faroles flotantes, carpas y nubes auspiciosas sobre un fondo rosa tierno y romántico.",
  "This is the 2023 annual calendar made for **Pingyuan Mall**. The cover opens in festive Year-of-the-Rabbit mood — a white rabbit in a flower crown rides a deer while the apple mascot Pingping turns flying apsara, playing flute and pipa and dancing — surrounded by sky lanterns, koi and auspicious clouds on a tender pink backdrop.")
P("pc23.ov.p2",
  "扉页创新设置**「平平书签」**双页，共 8 枚可剪下的书签：平安、大吉、如意、事成与兔年大吉系列，传统屋檐灯笼配舞狮帽平平，「伴您阅读每一天」。每月一幅**楼层主题插画**，平平带着家人朋友逛遍商场各楼层——从黄金珠宝广场七大品牌到二楼鞋履舞龙，从三楼男装咖啡馆到四楼品质女装，从建店 66 周年施工庆典到新大楼开业 23 周年，把商场的业态地图和品牌故事画进了一整年。",
  "Las páginas de apertura innovan con la **doble página de «Marcapáginas Pingping»**: ocho marcapáginas recortables — Paz, Gran Fortuna, Deseos cumplidos y serie de Año Nuevo del Conejo — con faroles de alero tradicional y Pingping de danzante, «acompañándote cada día». Cada mes, una **ilustración temática de planta**: Pingping recorre el centro —de la plaza de joyería con siete marcas a la zapatería con danza del dragón del 2º, del bizcocho de moda masculina del 3º a la moda de calidad del 4º, del 66º aniversario de la fundación a los 23 años del nuevo edificio— dibujando el mapa comercial y la historia de marca del centro a lo largo de todo el año.",
  "The opening pages innovate with the double **\"Pingping Bookmarks\"** spread: eight cut-along-the-line bookmarks — Peace, Great Luck, Wishes Granted and the Rabbit New Year series — with traditional eave lanterns and lion-hat Pingping, \"reading with you every day\". Each month a **floor-themed illustration**: Pingping tours the mall — from the seven-brand gold & jewellery plaza to the 2F shoe store's dragon dance, from the 3F menswear café to 4F quality womenswear, from the 66th-anniversary construction celebration to the new building's 23rd — drawing the mall's tenant map and brand story across the whole year.")
P("pc23.ov.point1", "苹果吉祥物「平平」贯穿全年", "La manzana «Pingping» recorre el año", "The apple mascot runs through the year")
P("pc23.ov.point2", "平平书签双扉页 · 8 枚可剪下", "Doble página de marcapáginas · 8 recortables", "Double bookmark spread · 8 cut-outs")
P("pc23.ov.point3", "每月对应一个商场楼层/业态", "Cada mes, una planta o negocio", "Each month a mall floor or business")
P("pc23.ov.point4", "七月建店66周年 · 十月新大楼23周年", "Julio: 66º aniversario · Octubre: 23 años del nuevo edificio", "July: 66th anniversary · October: new building's 23rd")

# ---- 02 设计亮点 ----
FEATURES = [
    ("01 — 兔年封面", "01 — Cubierta Año del Conejo", "01 — Year-of-the-Rabbit cover",
     "白兔骑鹿 × 飞天平平", "Conejo a lomos de ciervo × Pingping apsara", "Rabbit riding a deer × flying-apsara Pingping",
     "「平平」是由苹果延伸而来的吉祥物，粉色圆润身体、黄色果柄触角、绿叶尾巴。2023 兔年封面中平平化作飞天造型吹笛弹琵琶，与戴花冠的白兔骑鹿同框，天灯锦鲤祥云环绕，粉色背景温柔浪漫。",
     "«Pingping» es un personaje nacido de una manzana: cuerpo rosado y redondo, antenas de pedúnculo amarillo y cola de hoja verde. En la cubierta de 2023 Pingping se convierte en apsara que toca flauta y pipa, junto al conejo blanco con corona floral a lomos de un ciervo, rodeado de faroles flotantes, carpas y nubes: fondo rosa tierno y romántico.",
     "Pingping is a mascot derived from an apple — pink rounded body, yellow stalk antennae and a green-leaf tail. On the 2023 Rabbit-year cover Pingping becomes a flying apsara playing flute and pipa, sharing the frame with a flower-crowned white rabbit riding a deer, amid sky lanterns, koi and clouds on a tender pink backdrop."),
    ("02 — 书签双扉页", "02 — Doble página de marcapáginas", "02 — Double bookmark spread",
     "8 枚平平书签可剪下", "8 marcapáginas recortables", "8 cut-out Pingping bookmarks",
     "台历开篇设置两个书签页，共 8 枚可沿虚线剪下的书签：平安、大吉、如意、事成与兔年大吉系列，传统屋檐灯笼配舞狮帽平平，「伴您阅读每一天，和我做个好朋友吧」，兼具实用与收藏趣味。",
     "El calendario abre con dos páginas de marcapáginas: ocho recortables por la línea punteada — Paz, Gran Fortuna, Deseos cumplidos y serie del Año del Conejo — con faroles de alero y Pingping de danzante: «acompañándote cada día, sé mi amigo», prácticos y coleccionables.",
     "The calendar opens with two bookmark pages — eight bookmarks to cut along the dotted lines: Peace, Great Luck, Wishes Granted and the Rabbit New Year series, with traditional eave lanterns and lion-hat Pingping, \"reading with you every day — be my friend\". Practical and collectible at once."),
    ("03 — 楼层主题插画", "03 — Ilustración de planta", "03 — Floor-themed illustration",
     "12 个月逛遍整座商场", "12 meses por todo el centro", "12 months across the whole mall",
     "每月插画对应一个楼层或业态：黄金珠宝广场七大品牌、二楼鞋履舞龙、三楼男装咖啡馆、四楼品质女装、六一旋转木马、7 楼羽绒服、八方电器、5 楼女装，外加建店 66 周年和新大楼 23 周年庆。",
     "Cada mes la ilustración corresponde a una planta o negocio: plaza de joyería con siete marcas, zapatería con danza del dragón en el 2º, café de moda masculina en el 3º, moda de calidad en el 4º, tiovivo del Día del Niño, abrigos en el 7º, electrodomésticos Bafang, moda del 5º, más el 66º aniversario y los 23 años del nuevo edificio.",
     "Each month's illustration matches a floor or business: the seven-brand gold & jewellery plaza, 2F shoes with a dragon dance, the 3F menswear café, 4F quality womenswear, the Children's Day carousel, 7F down jackets, Bafang appliances, 5F womenswear — plus the 66th anniversary and the new building's 23rd."),
    ("04 — 功能型日历页", "04 — Página funcional", "04 — Functional calendar page",
     "左日历右插画 + 节气节日", "Calendario a la izquierda, ilustración a la derecha", "Calendar left, illustration right",
     "2023 日历页采用左侧日历格、右侧吉祥物插画的版式，标注公历、农历、节气与传统节日，右侧插画延续当月主题，底部印有「平原商场恭祝全市人民新春快乐，兔年大吉」等品牌语，翻页之间持续传递品牌温度。",
     "La página de 2023 combina la rejilla del calendario a la izquierda con la ilustración de la mascota a la derecha, anota fechas gregorianas y lunares, términos solares y festividades, y al pie imprime lemas como «Pingyuan felicita a la ciudadanía: próspero Año del Conejo», transmitiendo el calor de la marca a cada paso.",
     "The 2023 calendar page pairs a left-hand date grid with a right-hand mascot illustration, marking solar and lunar dates, solar terms and traditional festivals; the illustration carries the month's theme and the foot prints brand lines like \"Pingyuan Mall wishes the whole city a happy Rabbit New Year\" — brand warmth with every turn."),
]
for i, (no_zh, no_es, no_en, t_zh, t_es, t_en, p_zh, p_es, p_en) in enumerate(FEATURES, 1):
    P(f"pc23.ft{i}.no", no_zh, no_es, no_en)
    P(f"pc23.ft{i}.t", t_zh, t_es, t_en)
    P(f"pc23.ft{i}.p", p_zh, p_es, p_en)

# ---- 03 样机 ----
P("pc23.mk1.cap", "双页展开 · 一月插画与日历",
  "Doble página abierta · Ilustración y calendario",
  "Spread · illustration and calendar page")
P("pc23.mk2.cap", "立式桌面 · 封面主视觉",
  "En pie sobre la mesa · Portada", "Standing on a desk · Cover key visual")

# ---- 04 平铺图分组标题 ----
P("pc23.fg1.t", "封面 · 书签扉页 · 封底", "Cubierta, marcapáginas y contracubierta", "Cover · bookmarks · back cover")
P("pc23.fg1.n", "4 PAGES", "4 LÁMINAS", "4 PLATES")
P("pc23.fg2.t", "12 个月楼层主题插画页", "12 ilustraciones temáticas de planta", "12 floor-themed illustration pages")
P("pc23.fg2.n", "ILLUSTRATION PAGES", "ILUSTRACIONES", "ILLUSTRATIONS")
P("pc23.fg3.t", "12 个月功能日历页", "12 páginas de calendario funcional", "12 functional calendar pages")
P("pc23.fg3.n", "CALENDAR PAGES", "CALENDARIO", "CALENDAR PAGES")

# ---- 平铺图：封面组（cover / bookmark1 / bookmark2 / back）----
PLATES_HEAD = [
    ("cover", "封面", "Cubierta", "Cover",
     "2023 兔年主视觉", "Visual Año del Conejo 2023", "2023 Rabbit-year key visual"),
    ("bookmark1", "扉页 · 平平书签", "Apertura · Marcapáginas", "Opening · Bookmarks",
     "平安大吉如意事成", "Paz · Fortuna · Deseos", "Peace · Luck · Wishes"),
    ("bookmark2", "扉页 · 平平书签", "Apertura · Marcapáginas", "Opening · Bookmarks",
     "兔年大吉系列", "Serie Año del Conejo", "Rabbit New Year series"),
    ("back", "封底", "Contracubierta", "Back cover",
     "咱老百姓的商场", "El centro del pueblo", "The people's mall"),
]
for slug, t_zh, t_es, t_en, s_zh, s_es, s_en in PLATES_HEAD:
    P(f"pc23.pl.{slug}.t", t_zh, t_es, t_en)
    P(f"pc23.pl.{slug}.s", s_zh, s_es, s_en)

# ---- 12 个月：中文序数名 / 西英月名 / 插画主题 / 节气 ----
MONTH_CN = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
MONTH_EN = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]

THEME_ZH = ["舞狮白兔", "黄金珠宝广场", "二楼鞋履", "三楼男装", "四楼品质女装",
            "非童凡响", "建店66周年", "八方电器", "教师节", "新大楼23周年",
            "7楼羽绒服", "五楼大众女装"]
THEME_ES = ["Danza del león y conejo blanco", "Plaza de joyería", "Zapatería 2F", "Moda masculina 3F", "Moda de calidad 4F",
            "Infancia extraordinaria", "66º aniversario", "Electrodomésticos Bafang", "Día del Maestro", "23 años del nuevo edificio",
            "Abrigos 7F", "Moda popular 5F"]
THEME_EN = ["Lion dance & white rabbit", "Gold & jewellery plaza", "2F shoe store", "3F menswear", "4F quality womenswear",
            "Extraordinary childhood", "66th anniversary", "Bafang appliances", "Teachers' Day", "New building's 23rd",
            "7F down jackets", "5F popular womenswear"]

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
    "兔年开场，舞狮、白兔与弹琵琶的平平齐聚，红灯笼、囍字建筑喜气洋洋，「平原商场恭祝全市人民新春快乐，兔年大吉」。",
    "情人节 × 平原商场黄金珠宝广场，周大福、周大生、老凤祥、周六福、英特纳、六福、老庙七大品牌齐聚，平平情侣在扶梯下浪漫求婚。",
    "二楼鞋履，舞龙与鞋形灯笼、花瓣路，「成功路上，二楼鞋履让您的每一步都足下生辉」，薄荷绿背景春日清新。",
    "三楼男装男裤「时尚经典 我型我酷」，雨天咖啡馆前平平穿背带裤喝咖啡，绿色背景，春日都市型男范。",
    "四楼品质女装「实惠服务新乡」，平平在服装架前试穿连衣裙，藤蔓拱门与花朵装饰，暖黄色调温馨动人。",
    "六一儿童节「非童凡响 童年不同Young」，旋转木马挂着童装、向日葵与拨浪鼓环绕，天蓝色调充满童趣幻想。",
    "平原商场建店 66 周年庆，施工队平平戴安全帽刷油漆、拿图纸，66 蜡烛蛋糕与彩旗气球，紫色庆典背景热闹非凡。",
    "「买电器到八方 天天都低价省钱到八方」，嫦娥平平在电视里与 88 数字同框，喜鹊、洗衣机环绕，米色背景夏日清凉。",
    "教师节，斗笠平平老师接受学生献花送茶，向日葵与黑板，橄榄绿色调温馨感恩。",
    "新大楼开业 23 周年，司机、消防员、军人、警察、修车工与老奶奶各职业平平齐聚，灯笼标 2/3，宝蓝色庆典背景。",
    "「天冷了！买羽绒服就到平原商场7楼」，雪屋服装店前雪人举着 7F 木牌，圣诞树与礼物环绕，红色背景温暖治愈。",
    "五楼「拍了拍」你，提醒你该买漂亮衣服了，秋冬街景平平喝奶茶，服装店橱窗里圣诞树与礼物，米色背景年末温馨。",
]
DESC_ES = [
    "Arranca el Año del Conejo: danza del león, conejo blanco y Pingping con pipa se reúnen entre faroles rojos y edificios con el carácter 囍 — «Pingyuan felicita a la ciudadanía: próspero Año del Conejo».",
    "San Valentín en la plaza de joyería: Chow Tai Fook, Chow Tai Seng, Lao Feng Xiang, Chow Tai Fook, Yitena, Luk Fook y Lao Miao — siete marcas reunidas — mientras la pareja Pingping se propone bajo la escalera mecánica.",
    "En la zapatería del 2º, danza del dragón, lámparas con forma de zapato y un camino de pétalos: «en el camino al éxito, la zapatería del 2º hace brillar cada paso», sobre un verde menta primaveral.",
    "Moda masculina del 3º «clásico de moda, estilo propio»: un Pingping de tirantes bebe café ante la cafetería lluviosa, sobre fondo verde de galán urbano primaveral.",
    "Moda de calidad del 4º «precios justos, servicio a Xinxiang»: Pingping se prueba un vestido ante los percheros, bajo arcos de enredaderas y flores en tonos amarillos cálidos.",
    "Día del Niño «infancia extraordinaria»: el tiovivo cargado de ropa infantil, girasoles y sonajeros rodean la escena sobre un azul celeste de fantasía.",
    "66º aniversario de la fundación: los Pingping de obra con casco pintan y sostienen planos, con tarta de 66 velas, banderines y globos sobre un animado fondo púrpura.",
    "«Compra electrodomésticos en Bafang, ahorro todos los días»: Pingping apsara dentro del televisor junto al número 88, rodeada de urracas y lavadoras sobre fondo beige veraniego.",
    "Día del Maestro: la maestra Pingping con sombrero de paja recibe flores y té de sus alumnos, con girasoles y pizarra sobre un verde oliva de gratitud.",
    "23 años del nuevo edificio: Pingping de oficios — conductor, bombero, militar, policía, mecánico y abuelita — se reúnen con faroles del 2/3 sobre un fondo azul zafiro.",
    "«¡Ha llegado el frío! Abrigos en la planta 7 de Pingyuan»: un muñeco de nieve sostiene el cartel 7F ante la tienda-iglú, con árbol de Navidad y regalos sobre fondo rojo cálido.",
    "El 5º piso «te ha dado un toque»: te recuerda que ya es hora de comprar ropa bonita; Pingping bebe bubble tea en la escena otoñal-invernal, con escaparate navideño sobre fondo beige.",
]
DESC_EN = [
    "The Rabbit year opens — lion dance, white rabbit and pipa-playing Pingping gather among red lanterns and 囍-character buildings: \"Pingyuan Mall wishes the whole city a happy, lucky Rabbit New Year.\"",
    "Valentine's Day × the gold & jewellery plaza: Chow Tai Fook, Chow Tai Seng, Lao Feng Xiang, Chow Tai Fook, Yitena, Luk Fook and Lao Miao — seven brands together — as the Pingping couple proposes under the escalator.",
    "At the 2F shoe store, a dragon dance, shoe-shaped lanterns and a petal path — \"on the road to success, 2F shoes make every step shine\" — on a fresh spring mint-green background.",
    "3F menswear \"classic fashion, my own style\": a suspender-wearing Pingping sips coffee outside the rainy-day café — green backdrop, springtime city-chic.",
    "4F quality womenswear \"honest prices, serving Xinxiang\": Pingping tries on a dress before the clothing racks, under vine arches and flowers in warm yellow tones.",
    "Children's Day \"An Extraordinary Childhood\" — the carousel hung with kids' clothes, sunflowers and rattle-drums surrounding the scene on a sky-blue background of wonder.",
    "The 66th-anniversary celebration: hard-hat Pingpings paint and hold blueprints, with a 66-candle cake, bunting and balloons on a lively purple backdrop.",
    "\"Buy appliances at Bafang — low prices every day\": apsara Pingping on TV beside the number 88, surrounded by magpies and washing machines on a cool beige summer scene.",
    "Teachers' Day: straw-hat teacher Pingping receives flowers and tea from her pupils, with sunflowers and a blackboard on an olive-green background of gratitude.",
    "The new building turns 23 — driver, firefighter, soldier, police officer, mechanic and grandma Pingpings gather with 2/3 lanterns on a sapphire-blue backdrop.",
    "\"It's getting cold! Buy down jackets on 7F of Pingyuan Mall\" — a snowman holds the 7F sign outside the igloo-shaped store, Christmas tree and gifts on a warm red background.",
    "Floor 5 \"nudges\" you — time to buy some pretty clothes: Pingping sips bubble tea in the autumn-winter street scene, Christmas tree in the shop window, a warm beige year-end.",
]

for i in range(12):
    n = i + 1
    P(f"pc23.pl.ill{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc23.pl.ill{n}.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc23.pl.cal{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc23.pl.cal{n}.s", "公历 · 农历 · 节气", "Gregoriano · lunar · términos", "Solar · lunar · terms")
    P(f"pc23.m{n}.name", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc23.m{n}.en", MONTH_EN[i].upper(), MONTH_CN[i], MONTH_CN[i])
    P(f"pc23.m{n}.desc", DESC_ZH[i], DESC_ES[i], DESC_EN[i])
    P(f"pc23.m{n}.ill.t", "插画页", "Ilustración", "Illustration")
    P(f"pc23.m{n}.ill.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc23.m{n}.cal.t", "日历页", "Calendario", "Calendar")
    P(f"pc23.m{n}.cal.s", TERMS_ZH[i], TERMS_ES[i], TERMS_EN[i])

# ---- 06 封底 · 尾声 ----
P("pc23.cl.back.t", "封底", "Contracubierta", "Back cover")
P("pc23.cl.back.s", "咱老百姓的商场", "El centro del pueblo", "The people's mall")
P("pc23.cl.sum.t", "书签扉页", "Página de marcapáginas", "Bookmark page")
P("pc23.cl.sum.s", "8 枚可剪下收藏", "8 recortables", "8 cut-out collectibles")

# ---- 页脚 ----
P("pc23.footer.note", "平原商场 · 2023 癸卯兔年台历设计 — 作品集展示",
  "Pingyuan Mall · Calendario anual 2023 — Presentación de proyecto",
  "Pingyuan Mall · 2023 Annual Calendar — Project showcase")
P("pc23.backtop", "返回顶部", "Volver arriba", "Back to top")

VD = {k: (zh, es, en) for k, zh, es, en in TRI}
ORDER = [k for k, _, _, _ in TRI]

config = dict(
    prefix=prefix,
    work_id="pingyuan-calendar-2023",
    out_html="work-pingyuan2023-calendar.html",
    img="assets/works/pingyuan-calendar-2023",
    begin="/* >>> generated: pingyuan-calendar-2023 >>> */",
    end="/* <<< generated: pingyuan-calendar-2023 <<< */",
    nav_back_key="pc23.nav.back",
    overview_rows=["client", "type", "year", "pages", "mascot"],
    features_count=4,
    months_count=12,
    stats=[("28", "pc23.stat.pages"), ("12", "pc23.stat.months"),
           ("2", "pc23.stat.sheets"), ("1", "pc23.stat.mascot")],
    flat_g1=[("cover", "cover"), ("bookmark1", "bookmark1"), ("bookmark2", "bookmark2"), ("back", "backcover")],
    flat_g2=[(f"ill{i}", f"ill-{i:02d}") for i in range(1, 13)],
    flat_g3=[(f"cal{i}", f"cal-{i:02d}") for i in range(1, 13)],
    closing=[("backcover", "pc23.cl.back.t", "pc23.cl.back.s"),
             ("bookmark1", "pc23.cl.sum.t", "pc23.cl.sum.s")],
)

if __name__ == "__main__":
    n, out = build(config, ORDER, VD)
    print(f"i18n.js  ← {n} 个 pc23.* 键 × 3 语言")
    print(f"页面      ← {out}  ({len(ORDER)} 键)")
