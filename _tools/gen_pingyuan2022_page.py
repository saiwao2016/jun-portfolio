#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「平原商场 · 2022 壬寅虎年台历设计」作品专题页（三语）。

文案唯一真源在此（K 函数），由 pingyuan_common.build 同时产出：
  (a) assets/js/i18n.js 里 zh/es/en 三个语言块的 pc22.* 键（按标记幂等插入）
  b) work-pingyuan2022-calendar.html（静态兜底 = 中文值，零漂移）

用法：python3 _tools/gen_pingyuan2022_page.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pingyuan_common import make_registrar, build

K, TRI, KEYS = make_registrar()
prefix = "pc22"


def P(key, zh, es, en):
    K(key, zh, es, en)
    return zh


# ---- 页面元信息 ----
P("pc22.meta.title", "平原商场 · 2022 壬寅虎年台历设计 — JUN",
  "Pingyuan Mall · Calendario anual 2022 — JUN",
  "Pingyuan Mall · 2022 Annual Calendar — JUN")
P("pc22.meta.desc",
  "平原商场 2022 壬寅虎年台历设计：以苹果「平平」为品牌吉祥物，抵用券双扉页、12 个月楼层主题插画、12 页功能日历，跟着平平逛遍商场每一层。平面设计作品，周骏（JUN）设计。",
  "Calendario anual 2022 del centro comercial Pingyuan: la manzana «Pingping» como mascota de marca, doble página de cupones, 12 ilustraciones temáticas por plantas y 12 páginas de calendario funcional. Diseño gráfico de JUN (Zhou Jun).",
  "The 2022 annual calendar for Pingyuan Mall: the apple mascot \"Pingping\", a double voucher spread, 12 floor-themed illustrations and 12 functional calendar pages — follow Pingping through every floor. Graphic design by JUN (Zhou Jun).")

# ---- 页内子导航 ----
P("pc22.nav.overview", "项目概览", "Resumen", "Overview")
P("pc22.nav.features", "设计亮点", "Destacados", "Highlights")
P("pc22.nav.mockups", "样机展示", "Maquetas", "Mockups")
P("pc22.nav.flat", "平铺图", "Láminas", "Flat layout")
P("pc22.nav.months", "逐月作品", "Mes a mes", "Month by month")
P("pc22.nav.back", "返回作品集", "Volver a proyectos", "Back to works")

# ---- Hero ----
P("pc22.hero.kicker", "DESIGN PORTFOLIO · 2022", "DESIGN PORTFOLIO · 2022", "DESIGN PORTFOLIO · 2022")
P("pc22.hero.title", "平原商场", "Pingyuan Mall", "Pingyuan Mall")
P("pc22.hero.sub", "2022 壬寅虎年台历设计",
  "Calendario anual 2022 · Año del Tigre",
  "2022 Annual Calendar · Year of the Tiger")
P("pc22.hero.desc",
  "以苹果吉祥物「平平」为主角的年度台历：虎年封面大黄虎与古装平平同框、抵用券双扉页覆盖 1F–9F 三十张优惠券、12 个月楼层主题插画，跟着平平逛遍商场每一层。",
  "Un calendario anual protagonizado por la manzana «Pingping»: portada del Año del Tigre con un gran tigre dorado junto a Pingping de época, doble página de cupones con treinta descuentos del 1F al 9F y 12 ilustraciones temáticas por plantas — acompaña a Pingping por cada piso del centro.",
  "An annual calendar led by the apple mascot Pingping: a Tiger-year cover with a golden tiger alongside Pingping in period costume, a double voucher spread with thirty coupons from 1F to 9F, and 12 floor-themed illustrations — follow Pingping through every floor.")
P("pc22.hero.figcap", "封面样机 · 桌面展示",
  "Maqueta de cubierta · Escritorio", "Cover mockup · Desktop")
P("pc22.stat.pages", "个版面", "láminas", "plates")
P("pc22.stat.months", "个主题月", "meses temáticos", "themed months")
P("pc22.stat.sheets", "个抵用券扉页", "págs. de cupones", "voucher pages")
P("pc22.stat.mascot", "个吉祥物", "mascota", "mascot")

# ---- 六个区块标题 ----
P("pc22.sec.overview", "项目概览", "Resumen del proyecto", "Project overview")
P("pc22.sec.overview.tag", "PROJECT OVERVIEW", "PROJECT OVERVIEW", "PROJECT OVERVIEW")
P("pc22.sec.features", "设计亮点", "Destacados del diseño", "Design highlights")
P("pc22.sec.features.tag", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS")
P("pc22.sec.mockups", "样机展示", "Maquetas", "Mockups")
P("pc22.sec.mockups.tag", "MOCKUPS", "MOCKUPS", "MOCKUPS")
P("pc22.sec.flat", "平铺图展示", "Láminas planas", "Flat layout")
P("pc22.sec.flat.tag", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES")
P("pc22.sec.months", "逐月作品", "Mes a mes", "Month by month")
P("pc22.sec.months.tag", "MONTH BY MONTH", "MONTH BY MONTH", "MONTH BY MONTH")
P("pc22.sec.closing", "封底 · 尾声", "Contracubierta y cierre", "Back cover & closing")
P("pc22.sec.closing.tag", "BACK COVER & CLOSING", "BACK COVER & CLOSING", "BACK COVER & CLOSING")

# ---- 01 项目概览 ----
P("pc22.ov.client.k", "客户", "Cliente", "Client")
P("pc22.ov.client.v", "平原商场 Pingyuan Mall", "Centro comercial Pingyuan", "Pingyuan Mall")
P("pc22.ov.type.k", "项目类型", "Tipo", "Type")
P("pc22.ov.type.v", "年度台历 · 平面设计", "Calendario anual · Diseño gráfico", "Annual calendar · Graphic design")
P("pc22.ov.year.k", "设计年份", "Año", "Year")
P("pc22.ov.year.v", "2022 · 壬寅虎年", "2022 · Año del Tigre", "2022 · Year of the Tiger")
P("pc22.ov.pages.k", "页数", "Páginas", "Pages")
P("pc22.ov.pages.v", "28 个版面", "28 láminas", "28 plates")
P("pc22.ov.mascot.k", "吉祥物", "Mascota", "Mascot")
P("pc22.ov.mascot.v", "平平（苹果延伸形象）", "Pingping (de una manzana)", "Pingping (apple-derived)")
P("pc22.ov.p1",
  "这是为**平原商场**打造的 2022 年度台历。封面以壬寅虎年喜庆氛围开场，金色大老虎（额头王字）与苹果吉祥物「平平」家族穿古装同框——嫦娥弹琵琶、虎帽舞狮者——橙红色放射背景、祥云山峦烘托新年气势。",
  "Es el calendario anual 2022 creado para **Pingyuan Mall**. La cubierta abre con el ambiente festivo del Año del Tigre: un gran tigre dorado con el carácter 王 en la frente comparte escena con la familia de la manzana «Pingping» vestida de época — una Chang'e con pipa y un danzante de león con gorro de tigre — sobre un fondo radial naranja rojizo con nubes auspiciosas y montañas.",
  "This is the 2022 annual calendar made for **Pingyuan Mall**. The cover opens in festive Year-of-the-Tiger mood — a golden tiger (with the 王 mark on its forehead) shares the frame with the Pingping apple family in period costume: a pipa-playing Chang'e and a lion dancer in a tiger hat — against an orange-red radial backdrop of auspicious clouds and mountains.")
P("pc22.ov.p2",
  "扉页创新设置**「平原商场抵用券」**双页，共 30 张优惠券覆盖 1F 至 9F 各楼层品牌，兼具实用与收藏价值。每月一幅**楼层主题插画**，平平带着家人朋友逛遍商场各楼层——从珠宝城求婚到 SHOES 鞋包店，从三楼运动馆到四楼女装扮靓新乡，从建店 65 周年庆典到新大楼开业 22 周年，把商场的业态地图和品牌故事画进了一整年。",
  "Las páginas de apertura innovan con la **doble página de «Cupones Pingyuan»**: treinta cupones cubren las marcas del 1F al 9F, prácticas y coleccionables. Cada mes, una **ilustración temática de planta**: Pingping recorre el centro con familia y amigos —de la propuesta en la joyería a la zapatería SHOES, del pabellón deportivo del 3º a la moda femenina del 4º, del 65º aniversario de la fundación a los 22 años del nuevo edificio— dibujando el mapa comercial y la historia de marca del centro a lo largo de todo el año.",
  "The opening pages innovate with the double **\"Pingyuan Vouchers\"** spread: thirty coupons cover brands from 1F to 9F, practical and collectible. Each month a **floor-themed illustration**: Pingping tours the mall with family and friends — from the jewellery-city proposal to the SHOES store, from the 3F sports hall to 4F womenswear, from the 65th-anniversary celebration to the new building's 22nd — drawing the mall's tenant map and brand story across the whole year.")
P("pc22.ov.point1", "苹果吉祥物「平平」贯穿全年", "La manzana «Pingping» recorre el año", "The apple mascot runs through the year")
P("pc22.ov.point2", "抵用券双扉页 · 30 张优惠券", "Doble página de cupones · 30 descuentos", "Double voucher spread · 30 coupons")
P("pc22.ov.point3", "每月对应一个商场楼层/业态", "Cada mes, una planta o negocio", "Each month a mall floor or business")
P("pc22.ov.point4", "七月建店65周年 · 十月新大楼22周年", "Julio: 65º aniversario · Octubre: 22 años del nuevo edificio", "July: 65th anniversary · October: new building's 22nd")

# ---- 02 设计亮点 ----
FEATURES = [
    ("01 — 虎年封面", "01 — Cubierta Año del Tigre", "01 — Year-of-the-Tiger cover",
     "大黄虎 × 古装平平家族", "Gran tigre dorado × Pingping de época", "Golden tiger × Pingping family in period costume",
     "「平平」是由苹果延伸而来的吉祥物，粉色圆润身体、黄色果柄触角、绿叶尾巴。2022 虎年封面中平平家族换上古装——嫦娥弹琵琶、虎帽舞狮——与金色大老虎同框，橙红放射背景气势十足。",
     "«Pingping» es un personaje nacido de una manzana: cuerpo rosado y redondo, antenas de pedúnculo amarillo y cola de hoja verde. En la cubierta de 2022 la familia Pingping viste de época — Chang'e con pipa, danza del león con gorro de tigre — junto al gran tigre dorado, sobre un fondo radial naranja rojizo de gran fuerza.",
     "Pingping is a mascot derived from an apple — pink rounded body, yellow stalk antennae and a green-leaf tail. On the 2022 Tiger-year cover the Pingping family dresses in period costume — a pipa-playing Chang'e, a tiger-hat lion dancer — sharing the frame with the golden tiger against a powerful orange-red radial backdrop."),
    ("02 — 抵用券双扉页", "02 — Doble página de cupones", "02 — Double voucher spread",
     "30 张优惠券覆盖 1F–9F", "30 cupones del 1F al 9F", "30 coupons from 1F to 9F",
     "台历开篇设置两个抵用券页，共 30 张品牌优惠券，从 1F 黄金珠宝到 3F 运动男装、再到 9F 餐饮娱乐，每层楼都有专属福利，翻台历的同时也是一份商场消费指南。",
     "El calendario abre con dos páginas de cupones: treinta cupones de marca, desde la joyería del 1F y la ropa deportiva del 3F hasta la restauración y ocio del 9F; cada planta tiene su beneficio, y hojear el calendario es también una guía de compras del centro.",
     "The calendar opens with two voucher pages — thirty brand coupons from 1F gold & jewellery and 3F sportswear to 9F dining and entertainment. Every floor has its own perk: flipping the calendar doubles as a shopping guide to the mall."),
    ("03 — 楼层主题插画", "03 — Ilustración de planta", "03 — Floor-themed illustration",
     "12 个月逛遍整座商场", "12 meses por todo el centro", "12 months across the whole mall",
     "每月插画对应一个楼层或业态：珠宝城求婚、SHOES 鞋包店、三楼运动馆、四楼女装、六一儿童、7 楼羽绒服反季、八方电器、5 楼大众女装，外加建店 65 周年和新大楼 22 周年庆。",
     "Cada mes la ilustración corresponde a una planta o negocio: propuesta en la joyería, zapatería SHOES, pabellón deportivo del 3º, moda femenina del 4º, Día del Niño, abrigos de rebajas en el 7º, electrodomésticos Bafang, moda popular del 5º, más el 65º aniversario y los 22 años del nuevo edificio.",
     "Each month's illustration matches a floor or business: the jewellery-city proposal, the SHOES store, the 3F sports hall, 4F womenswear, Children's Day, 7F off-season down jackets, Bafang appliances, 5F popular womenswear — plus the 65th anniversary and the new building's 22nd."),
    ("04 — 功能型日历页", "04 — Página funcional", "04 — Functional calendar page",
     "左日历右插画 + 节气节日", "Calendario a la izquierda, ilustración a la derecha", "Calendar left, illustration right",
     "2022 日历页采用左侧日历格、右侧吉祥物插画的版式，标注公历、农历、节气与传统节日，右侧插画延续当月主题，底部印有「平原商场恭祝全市人民新年快乐」等品牌语，翻页之间持续传递品牌温度。",
     "La página de 2022 combina la rejilla del calendario a la izquierda con la ilustración de la mascota a la derecha, anota fechas gregorianas y lunares, términos solares y festividades, y al pie imprime lemas de marca como «Pingyuan felicita a la ciudadanía por el Año Nuevo», transmitiendo el calor de la marca a cada paso.",
     "The 2022 calendar page pairs a left-hand date grid with a right-hand mascot illustration, marking solar and lunar dates, solar terms and traditional festivals; the illustration carries the month's theme and the foot prints brand lines like \"Pingyuan Mall wishes the whole city a Happy New Year\" — brand warmth with every turn."),
]
for i, (no_zh, no_es, no_en, t_zh, t_es, t_en, p_zh, p_es, p_en) in enumerate(FEATURES, 1):
    P(f"pc22.ft{i}.no", no_zh, no_es, no_en)
    P(f"pc22.ft{i}.t", t_zh, t_es, t_en)
    P(f"pc22.ft{i}.p", p_zh, p_es, p_en)

# ---- 03 样机 ----
P("pc22.mk1.cap", "双页展开 · 一月插画与日历",
  "Doble página abierta · Ilustración y calendario",
  "Spread · illustration and calendar page")
P("pc22.mk2.cap", "立式桌面 · 封面主视觉",
  "En pie sobre la mesa · Portada", "Standing on a desk · Cover key visual")

# ---- 04 平铺图分组标题 ----
P("pc22.fg1.t", "封面 · 抵用券扉页 · 封底", "Cubierta, cupones y contracubierta", "Cover · vouchers · back cover")
P("pc22.fg1.n", "4 PAGES", "4 LÁMINAS", "4 PLATES")
P("pc22.fg2.t", "12 个月楼层主题插画页", "12 ilustraciones temáticas de planta", "12 floor-themed illustration pages")
P("pc22.fg2.n", "ILLUSTRATION PAGES", "ILUSTRACIONES", "ILLUSTRATIONS")
P("pc22.fg3.t", "12 个月功能日历页", "12 páginas de calendario funcional", "12 functional calendar pages")
P("pc22.fg3.n", "CALENDAR PAGES", "CALENDARIO", "CALENDAR PAGES")

# ---- 平铺图：封面组（cover / voucher1 / voucher2 / back）----
PLATES_HEAD = [
    ("cover", "封面", "Cubierta", "Cover",
     "2022 虎年主视觉", "Visual Año del Tigre 2022", "2022 Tiger-year key visual"),
    ("voucher1", "扉页 · 抵用券", "Apertura · Cupones", "Opening · Vouchers",
     "1F–3F 品牌", "Marcas 1F–3F", "Brands 1F–3F"),
    ("voucher2", "扉页 · 抵用券", "Apertura · Cupones", "Opening · Vouchers",
     "3F–9F 品牌", "Marcas 3F–9F", "Brands 3F–9F"),
    ("back", "封底", "Contracubierta", "Back cover",
     "咱老百姓的商场", "El centro del pueblo", "The people's mall"),
]
for slug, t_zh, t_es, t_en, s_zh, s_es, s_en in PLATES_HEAD:
    P(f"pc22.pl.{slug}.t", t_zh, t_es, t_en)
    P(f"pc22.pl.{slug}.s", s_zh, s_es, s_en)

# ---- 12 个月：中文序数名 / 西英月名 / 插画主题 / 节气 ----
MONTH_CN = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
MONTH_EN = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]

THEME_ZH = ["舞狮元旦", "珠宝城求婚", "SHOES 鞋包店", "三楼运动馆", "四楼女装",
            "童心童趣", "建店65周年", "7楼羽绒服反季", "八方电器", "新大楼22周年",
            "7楼羽绒服", "五楼大众女装"]
THEME_ES = ["Danza del león de Año Nuevo", "Propuesta en la joyería", "Zapatería SHOES", "Pabellón deportivo 3F", "Moda femenina 4F",
            "Alegría infantil", "65º aniversario", "Abrigos de rebajas 7F", "Electrodomésticos Bafang", "22 años del nuevo edificio",
            "Abrigos 7F", "Moda popular 5F"]
THEME_EN = ["Lion-dance New Year", "Jewellery-city proposal", "SHOES store", "3F sports hall", "4F womenswear",
            "Childlike joy", "65th anniversary", "7F off-season jackets", "Bafang appliances", "New building's 22nd",
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
    "新年开场，舞狮平平举着「元旦」卷轴，平平一家在雪地钟楼前迎接零点，红灯笼、烟花、铜钱铺满画面，热热闹闹迎新春。",
    "情人节遇上平原商场珠宝城，平平在珠宝城前上演浪漫求婚，戒指与花束烘托甜蜜氛围，红色背景喜气洋洋。",
    "SHOES 鞋包店，民国风平平提着行李箱，「陪着你，遇见最美的风景」，薄荷绿背景清新明快，春日出行正当时。",
    "三楼运动馆，安踏、匹克、乔丹齐聚，平平们打篮球、举哑铃，青绿色背景充满春日活力，运动正当时。",
    "母亲节 × 四楼女装「扮靓新乡」，连衣裙人台与星星星球环绕，暖黄色调温馨动人，给妈妈一份美丽礼物。",
    "六一儿童节「童心童趣 快乐童年」，鲤鱼旗、玩具车、城堡风车环绕婴儿平平，天蓝色调充满童趣幻想。",
    "平原商场建店 65 周年，65 气球、生日蛋糕、麦克风主持齐聚，紫色庆典背景，平平们举杯共庆商场生日。",
    "「羽绒服反季销售开始啦」，7 楼羽绒服区，草帽平平吃冰棍遛小狗，米色背景夏日清凉，反季聚划算。",
    "「买电器到八方 品牌齐全」，家电卖场里企鹅与嫦娥抱兔同框，橄榄绿色调，洗衣机、冰箱、电视一应俱全。",
    "新大楼开业 22 周年，工人、警察、农民、医生各职业平平齐聚商场前，小狗作伴，紫色庆典背景，New 22 气球升空。",
    "「天冷了！买羽绒服就到平原商场七楼」，驯鹿驮着羽绒服在雪地树林里送货，雪人躲在树后偷看，橙色背景温暖治愈。",
    "「五楼大众女装 圆您美丽梦想」，试衣间前平平试穿新裙，圣诞树、猫咪、礼物环绕，米色背景温馨，年末的美丽收尾。",
]
DESC_ES = [
    "Arranca el año: Pingping danzante de león sostiene un pergamino de «Año Nuevo»; la familia Pingping recibe la medianoche ante la torre del reloj nevada, con faroles rojos, fuegos artificiales y monedas llenando la escena.",
    "San Valentín en la joyería de Pingyuan: Pingping hace una romántica propuesta ante la tienda, con anillos y ramos endulzando el ambiente sobre un fondo rojo festivo.",
    "En la zapatería SHOES, un Pingping de época republicana lleva una maleta: «contigo, descubro el paisaje más bello», sobre un fondo verde menta fresco, perfecto para salir en primavera.",
    "En el pabellón deportivo del 3º se reúnen Anta, Peak y Jordan; los Pingping juegan al baloncesto y levantan pesas, llenando el fondo verdemar de vitalidad primaveral.",
    "Día de la Madre × moda femenina del 4º «embellece Xinxiang»: maniquíes de vestido, estrellas y planetas rodean la escena en tonos amarillos cálidos — un bello regalo para mamá.",
    "Día del Niño «alegría infantil»: banderas de carpa, coches de juguete y molinos de castillo rodean al bebé Pingping sobre un fondo azul celeste de fantasía.",
    "65º aniversario de Pingyuan: globos del 65, tarta de cumpleaños y maestro de ceremonias se reúnen sobre un fondo púrpura; los Pingping brindan por el cumpleaños del centro.",
    "«¡Empiezan las rebajas de abrigos!»: en la planta 7 de abrigos, un Pingping con sombrero de paja toma un polo y pasea al perrito, con fondo beige veraniego — chollo de temporada.",
    "«Compra electrodomésticos en Bafang, todas las marcas»: en la tienda, un pingüino y una Chang'e con conejo comparten escena sobre fondo verde oliva, con lavadoras, neveras y televisores de todo.",
    "22 años del nuevo edificio: Pingping de oficios — obrero, policía, agricultor, médico — se reúnen ante el centro con un perrito de compañía, sobre fondo púrpura y globos «New 22» al cielo.",
    "«¡Ha llegado el frío! Abrigos en la planta 7 de Pingyuan»: un reno entrega abrigos por el bosque nevado mientras un muñeco de nieve espía tras los árboles, sobre fondo naranja cálido.",
    "«La moda popular del 5º hace realidad tus sueños de belleza»: Pingping se prueba un vestido ante el probador, rodeado de árbol de Navidad, gatitos y regalos — un cálido cierre de año en beige.",
]
DESC_EN = [
    "The year opens with a lion-dance Pingping holding a \"New Year\" scroll; the Pingping family greets midnight before the snowy clock tower, red lanterns, fireworks and coins filling the scene.",
    "Valentine's Day meets the Pingyuan jewellery city — Pingping stages a romantic proposal in front of the store, rings and bouquets sweetening the festive red backdrop.",
    "At the SHOES store, a Republican-era Pingping carries a suitcase — \"with you, meeting the most beautiful scenery\" — on a fresh mint-green background, perfect for spring outings.",
    "In the 3F sports hall, Anta, Peak and Jordan gather; Pingpings play basketball and lift dumbbells, filling the teal backdrop with spring energy.",
    "Mother's Day × 4F womenswear \"Dress Up Xinxiang\" — dress forms, stars and planets surround the scene in warm yellow tones: a beautiful gift for mum.",
    "Children's Day \"Childlike Joy\" — carp banners, toy cars and castle pinwheels surround baby Pingping on a sky-blue background full of wonder.",
    "Pingyuan's 65th anniversary — 65 balloons, a birthday cake and an MC with microphone gather on a purple backdrop; the Pingpings raise a toast to the mall's birthday.",
    "\"Off-season down-jacket sales begin!\" In the 7F zone, a straw-hat Pingping licks a popsicle while walking the dog — a cool beige summer scene full of bargains.",
    "\"Buy appliances at Bafang — every brand here\": a penguin and a rabbit-holding Chang'e share the olive-green store scene, with washers, fridges and TVs galore.",
    "The new building turns 22 — worker, police officer, farmer and doctor Pingpings gather in front of the mall with a little dog, purple backdrop and \"New 22\" balloons rising.",
    "\"It's getting cold! Buy down jackets on 7F of Pingyuan Mall\" — a reindeer delivers jackets through the snowy woods while a snowman peeks from behind the trees, on a warm orange background.",
    "\"5F popular womenswear makes your beautiful dreams come true\" — Pingping tries on a new dress at the fitting room, surrounded by a Christmas tree, kittens and gifts: a warm beige year-end finale.",
]

for i in range(12):
    n = i + 1
    P(f"pc22.pl.ill{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc22.pl.ill{n}.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc22.pl.cal{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc22.pl.cal{n}.s", "公历 · 农历 · 节气", "Gregoriano · lunar · términos", "Solar · lunar · terms")
    P(f"pc22.m{n}.name", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc22.m{n}.en", MONTH_EN[i].upper(), MONTH_CN[i], MONTH_CN[i])
    P(f"pc22.m{n}.desc", DESC_ZH[i], DESC_ES[i], DESC_EN[i])
    P(f"pc22.m{n}.ill.t", "插画页", "Ilustración", "Illustration")
    P(f"pc22.m{n}.ill.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc22.m{n}.cal.t", "日历页", "Calendario", "Calendar")
    P(f"pc22.m{n}.cal.s", TERMS_ZH[i], TERMS_ES[i], TERMS_EN[i])

# ---- 06 封底 · 尾声 ----
P("pc22.cl.back.t", "封底", "Contracubierta", "Back cover")
P("pc22.cl.back.s", "咱老百姓的商场", "El centro del pueblo", "The people's mall")
P("pc22.cl.sum.t", "抵用券扉页", "Página de cupones", "Voucher page")
P("pc22.cl.sum.s", "30 张品牌优惠券", "30 cupones de marca", "30 brand coupons")

# ---- 页脚 ----
P("pc22.footer.note", "平原商场 · 2022 壬寅虎年台历设计 — 作品集展示",
  "Pingyuan Mall · Calendario anual 2022 — Presentación de proyecto",
  "Pingyuan Mall · 2022 Annual Calendar — Project showcase")
P("pc22.backtop", "返回顶部", "Volver arriba", "Back to top")

VD = {k: (zh, es, en) for k, zh, es, en in TRI}
ORDER = [k for k, _, _, _ in TRI]

config = dict(
    prefix=prefix,
    work_id="pingyuan-calendar-2022",
    out_html="work-pingyuan2022-calendar.html",
    img="assets/works/pingyuan-calendar-2022",
    begin="/* >>> generated: pingyuan-calendar-2022 >>> */",
    end="/* <<< generated: pingyuan-calendar-2022 <<< */",
    nav_back_key="pc22.nav.back",
    overview_rows=["client", "type", "year", "pages", "mascot"],
    features_count=4,
    months_count=12,
    stats=[("28", "pc22.stat.pages"), ("12", "pc22.stat.months"),
           ("2", "pc22.stat.sheets"), ("1", "pc22.stat.mascot")],
    flat_g1=[("cover", "cover"), ("voucher1", "voucher1"), ("voucher2", "voucher2"), ("back", "backcover")],
    flat_g2=[(f"ill{i}", f"ill-{i:02d}") for i in range(1, 13)],
    flat_g3=[(f"cal{i}", f"cal-{i:02d}") for i in range(1, 13)],
    closing=[("backcover", "pc22.cl.back.t", "pc22.cl.back.s"),
             ("voucher1", "pc22.cl.sum.t", "pc22.cl.sum.s")],
)

if __name__ == "__main__":
    n, out = build(config, ORDER, VD)
    print(f"i18n.js  ← {n} 个 pc22.* 键 × 3 语言")
    print(f"页面      ← {out}  ({len(ORDER)} 键)")
