#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「平原商场 · 2024 甲辰龙年台历设计」作品专题页（三语）。

文案唯一真源在此（K 函数），由 pingyuan_common.build 同时产出：
  (a) assets/js/i18n.js 里 zh/es/en 三个语言块的 pc24.* 键（按标记幂等插入）
  b) work-pingyuan2024-calendar.html（静态兜底 = 中文值，零漂移）

用法：python3 _tools/gen_pingyuan2024_page.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pingyuan_common import make_registrar, build

K, TRI, KEYS = make_registrar()
prefix = "pc24"


def P(key, zh, es, en):
    K(key, zh, es, en)
    return zh


# ---- 页面元信息 ----
P("pc24.meta.title", "平原商场 · 2024 甲辰龙年台历设计 — JUN",
  "Pingyuan Mall · Calendario anual 2024 — JUN",
  "Pingyuan Mall · 2024 Annual Calendar — JUN")
P("pc24.meta.desc",
  "平原商场 2024 甲辰龙年台历设计：苹果吉祥物「平平」举「大吉大利」卷轴与绿龙同框，时间管理页与商场全家福双扉页，12 个月楼层主题插画，跟着平平逛遍商场每一层。平面设计作品，周骏（JUN）设计。",
  "Calendario anual 2024 del centro comercial Pingyuan: la manzana «Pingping» con un pergamino de buena suerte junto a un dragón verde, dobles aperturas de gestión del tiempo y retrato familiar, 12 ilustraciones temáticas por plantas. Diseño gráfico de JUN (Zhou Jun).",
  "The 2024 annual calendar for Pingyuan Mall: apple mascot Pingping with a \"good fortune\" scroll beside a green dragon, dual opening pages for time management and the mall family portrait, 12 floor-themed illustrations. Graphic design by JUN (Zhou Jun).")

# ---- 页内子导航 ----
P("pc24.nav.overview", "项目概览", "Resumen", "Overview")
P("pc24.nav.features", "设计亮点", "Destacados", "Highlights")
P("pc24.nav.mockups", "样机展示", "Maquetas", "Mockups")
P("pc24.nav.flat", "平铺图", "Láminas", "Flat layout")
P("pc24.nav.months", "逐月作品", "Mes a mes", "Month by month")
P("pc24.nav.back", "返回作品集", "Volver a proyectos", "Back to works")

# ---- Hero ----
P("pc24.hero.kicker", "DESIGN PORTFOLIO · 2024", "DESIGN PORTFOLIO · 2024", "DESIGN PORTFOLIO · 2024")
P("pc24.hero.title", "平原商场", "Pingyuan Mall", "Pingyuan Mall")
P("pc24.hero.sub", "2024 甲辰龙年台历设计",
  "Calendario anual 2024 · Año del Dragón",
  "2024 Annual Calendar · Year of the Dragon")
P("pc24.hero.desc",
  "以苹果吉祥物「平平」为主角的年度台历：龙年封面绿龙腾跃与举卷轴的平平同框、时间管理页与商场全家福双扉页、12 个月楼层主题插画，跟着平平逛遍商场每一层。",
  "Un calendario anual protagonizado por la manzana «Pingping»: en la cubierta un dragón verde comparte escena con Pingping de pergamino en mano, dobles aperturas de gestión del tiempo y retrato familiar, y 12 ilustraciones temáticas por plantas.",
  "An annual calendar led by the apple mascot Pingping: a green dragon soaring beside Pingping on the cover, dual opening pages for time management and the mall family portrait, and 12 floor-themed illustrations through every floor.")
P("pc24.hero.figcap", "封面样机 · 桌面展示",
  "Maqueta de cubierta · Escritorio", "Cover mockup · Desktop")
P("pc24.stat.pages", "个版面", "láminas", "plates")
P("pc24.stat.months", "个主题月", "meses temáticos", "themed months")
P("pc24.stat.sheets", "个特别扉页", "págs. de apertura", "opening pages")
P("pc24.stat.mascot", "个吉祥物", "mascota", "mascot")

# ---- 六个区块标题 ----
P("pc24.sec.overview", "项目概览", "Resumen del proyecto", "Project overview")
P("pc24.sec.overview.tag", "PROJECT OVERVIEW", "PROJECT OVERVIEW", "PROJECT OVERVIEW")
P("pc24.sec.features", "设计亮点", "Destacados del diseño", "Design highlights")
P("pc24.sec.features.tag", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS")
P("pc24.sec.mockups", "样机展示", "Maquetas", "Mockups")
P("pc24.sec.mockups.tag", "MOCKUPS", "MOCKUPS", "MOCKUPS")
P("pc24.sec.flat", "平铺图展示", "Láminas planas", "Flat layout")
P("pc24.sec.flat.tag", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES")
P("pc24.sec.months", "逐月作品", "Mes a mes", "Month by month")
P("pc24.sec.months.tag", "MONTH BY MONTH", "MONTH BY MONTH", "MONTH BY MONTH")
P("pc24.sec.closing", "封底 · 尾声", "Contracubierta y cierre", "Back cover & closing")
P("pc24.sec.closing.tag", "BACK COVER & CLOSING", "BACK COVER & CLOSING", "BACK COVER & CLOSING")

# ---- 01 项目概览 ----
P("pc24.ov.client.k", "客户", "Cliente", "Client")
P("pc24.ov.client.v", "平原商场 Pingyuan Mall", "Centro comercial Pingyuan", "Pingyuan Mall")
P("pc24.ov.type.k", "项目类型", "Tipo", "Type")
P("pc24.ov.type.v", "年度台历 · 平面设计", "Calendario anual · Diseño gráfico", "Annual calendar · Graphic design")
P("pc24.ov.year.k", "设计年份", "Año", "Year")
P("pc24.ov.year.v", "2024 · 甲辰龙年", "2024 · Año del Dragón", "2024 · Year of the Dragon")
P("pc24.ov.pages.k", "页数", "Páginas", "Pages")
P("pc24.ov.pages.v", "28 个版面", "28 láminas", "28 plates")
P("pc24.ov.mascot.k", "吉祥物", "Mascota", "Mascot")
P("pc24.ov.mascot.v", "平平（苹果延伸形象）", "Pingping (de una manzana)", "Pingping (apple-derived)")
P("pc24.ov.p1",
  "这是为**平原商场**打造的 2024 年度台历。封面以甲辰龙年喜庆氛围开场，红金放射背景上绿色巨龙腾跃，苹果吉祥物「平平」化作小女孩举着「大吉大利」卷轴，柿子、铜钱、祥云与囍字建筑环绕，喜气洋洋。",
  "Es el calendario anual 2024 creado para **Pingyuan Mall**. La cubierta abre con el ambiente festivo del Año del Dragón: sobre un fondo radiante rojo y oro, un gran dragón verde se eleva mientras la manzana «Pingping», convertida en niña, sostiene un pergamino de «gran fortuna», rodeada de caquis, monedas, nubes auspiciosas y edificios con el carácter 囍.",
  "This is the 2024 annual calendar made for **Pingyuan Mall**. The cover opens in festive Year-of-the-Dragon mood — on a red-and-gold radiating backdrop a green dragon soars while the apple mascot Pingping, as a little girl, holds up a \"great fortune\" scroll, surrounded by persimmons, coins, auspicious clouds and 囍-character buildings.")
P("pc24.ov.p2",
  "扉页创新设置**「时间管理页」**与**「商场全家福」**双页：时间管理页以 12 个月格子搭配星星、烟花、纸飞机、气球、树叶、雪花等装饰图标；全家福页则是平平一家——妈妈推婴儿车、爸爸、奶奶推购物车、小孩——在商场大楼前，「咱老百姓的商场」。每月一幅**楼层主题插画**，平平带着家人朋友逛遍商场各楼层——从 1F 黄金珠宝广场到负 1F 八方电器，从建店 67 周年庆到新大楼开业 24 周年，把商场的业态地图和品牌故事画进了一整年。",
  "Las aperturas innovan con **«Gestión del tiempo»** y **«Retrato familiar del centro»**: la primera organiza 12 casillas mensuales con iconos decorativos (estrellas, fuegos artificiales, aviones de papel, globos, hojas, copos de nieve); la segunda muestra a la familia de Pingping —mamá con cochecito, papá, la abuela con carrito y los niños— ante el edificio del centro, «el centro del pueblo». Cada mes, una **ilustración temática de planta**: Pingping recorre el centro con familia y amigos —de la plaza de oro y joyas del 1F a los electrodomésticos Bafang del −1F, del 67º aniversario de fundación al 24º del nuevo edificio— dibujando el mapa comercial del centro durante todo el año.",
  "The opening pages innovate with **\"Time Management\"** and the **\"Mall Family Portrait\"**: the first lays out 12 monthly grids decorated with stars, fireworks, paper planes, balloons, leaves and snowflakes; the second shows Pingping's family — mum with a stroller, dad, grandma with a shopping cart, kids — in front of the mall building, \"the people's mall\". Each month a **floor-themed illustration**: Pingping tours the mall with family and friends — from the 1F gold-and-jewellery plaza to the B1F Bafang appliances, from the 67th founding anniversary to the new building's 24th — drawing the mall's tenant map across the whole year.")
P("pc24.ov.point1", "苹果吉祥物「平平」贯穿全年", "La manzana «Pingping» recorre el año", "The apple mascot runs through the year")
P("pc24.ov.point2", "时间管理页 + 商场全家福双扉页", "Dos aperturas: gestión del tiempo y retrato familiar", "Two opening pages: time management & family portrait")
P("pc24.ov.point3", "每月对应一个商场楼层/业态", "Cada mes, una planta o negocio", "Each month a mall floor or business")
P("pc24.ov.point4", "七月建店67周年 · 十月新大楼24周年", "Julio: 67º aniversario · Octubre: 24º del nuevo edificio", "July: 67th founding · October: new building's 24th")

# ---- 02 设计亮点 ----
FEATURES = [
    ("01 — 龙年封面", "01 — Cubierta Año del Dragón", "01 — Year-of-the-Dragon cover",
     "绿龙腾跃 × 大吉大利", "Dragón verde × Gran fortuna", "Green dragon × Great fortune",
     "「平平」是由苹果延伸而来的吉祥物，粉色圆润身体、黄色果柄触角、绿叶尾巴。2024 龙年封面中平平化作小女孩举着「大吉大利」卷轴，与红角绿龙同框，柿子、铜钱、祥云、囍字建筑环绕，红金放射背景喜庆热烈。",
     "«Pingping» es un personaje nacido de una manzana: cuerpo rosado y redondo, antenas de pedúnculo amarillo y cola de hoja verde. En la cubierta de 2024 Pingping, convertida en niña, sostiene un pergamino de «gran fortuna» junto a un dragón verde de cuernos rojos, rodeada de caquis, monedas, nubes y edificios con el carácter 囍 sobre un fondo radiante rojo y oro.",
     "Pingping is a mascot derived from an apple — pink rounded body, yellow stalk antennae and a green-leaf tail. On the 2024 Dragon-year cover Pingping, as a little girl, holds a \"great fortune\" scroll beside a red-horned green dragon, framed by persimmons, coins, clouds and 囍-character buildings on a festive red-gold radiating backdrop."),
    ("02 — 双特别扉页", "02 — Dobles aperturas", "02 — Two special opening pages",
     "时间管理 × 商场全家福", "Gestión del tiempo × Retrato familiar", "Time management × Family portrait",
     "台历开篇设置两个特别扉页：时间管理页以 12 个月格子搭配季节装饰图标（星星、烟花、纸飞机、气球、树叶、雪花），红色背景灯笼烟花；商场全家福页是平平一家在商场大楼前，想法气泡里装着购物心愿，「咱老百姓的商场」。",
     "El calendario abre con dos páginas especiales: la de gestión del tiempo organiza 12 casillas mensuales con iconos de temporada (estrellas, fuegos artificiales, aviones de papel, globos, hojas, copos) sobre fondo rojo con faroles y fuegos; la del retrato familiar muestra a la familia de Pingping ante el edificio, con burbujas de pensamiento llenas de deseos de compra: «el centro del pueblo».",
     "The calendar opens with two special pages: the Time Management page lays out 12 monthly grids with seasonal icons (stars, fireworks, paper planes, balloons, leaves, snowflakes) on a red backdrop of lanterns and fireworks; the Family Portrait page shows Pingping's family before the mall building, thought bubbles filled with shopping wishes — \"the people's mall\"."),
    ("03 — 楼层主题插画", "03 — Ilustración de planta", "03 — Floor-themed illustration",
     "12 个月逛遍整座商场", "12 meses por todo el centro", "12 months across the whole mall",
     "每月插画对应一个楼层或业态：1F 黄金珠宝广场、2F 二楼鞋履、3F 运动、4F 品质女装、6F 运动童装、负1F 八方电器、3F 运动户外、7F 羽绒服、5F 大众女装，外加建店 67 周年和新大楼 24 周年庆。",
     "Cada mes la ilustración corresponde a una planta o negocio: plaza de oro y joyas en 1F, zapatos en 2F, deporte en 3F, moda femenina de calidad en 4F, deporte infantil en 6F, electrodomésticos Bafang en −1F, deporte y aire libre en 3F, abrigos en 7F y moda femenina popular en 5F, más el 67º aniversario y el 24º del nuevo edificio.",
     "Each month's illustration matches a floor or business: the 1F gold-and-jewellery plaza, 2F shoes, 3F sports, 4F quality womenswear, 6F kids' sportswear, B1F Bafang appliances, 3F outdoor sports, 7F down jackets, 5F popular womenswear — plus the 67th founding anniversary and the new building's 24th."),
    ("04 — 功能型日历页", "04 — Página funcional", "04 — Functional calendar page",
     "左插画右日历 + 节气节日", "Ilustración y calendario + festividades", "Illustration & calendar + festivals",
     "2024 日历页采用左侧吉祥物插画、右侧日历格的版式，标注公历、农历、节气与传统节日，左侧插画延续当月主题，顶部印有「抬头见囍 2024 遇见更好的自己」等品牌语，底部「咱老百姓的商场」印章，翻页之间持续传递品牌温度。",
     "La página de calendario de 2024 combina la ilustración de la mascota a la izquierda con la rejilla del calendario a la derecha, anotando fechas gregorianas y lunares, términos solares y festividades; la ilustración continúa el tema del mes, la cabecera imprime lemas de marca como «Buena suerte al levantar la vista · 2024, sé mejor tú mismo», y al pie el sello «el centro del pueblo», transmitiendo el calor de la marca a cada paso.",
     "The 2024 calendar page pairs the mascot illustration on the left with the calendar grid on the right, marking solar and lunar dates, solar terms and traditional festivals; the illustration carries the month's theme, the header prints brand lines like \"Look up for luck — 2024, a better you\", and the foot bears the \"people's mall\" seal, carrying brand warmth with every turn."),
]
for i, (no_zh, no_es, no_en, t_zh, t_es, t_en, p_zh, p_es, p_en) in enumerate(FEATURES, 1):
    P(f"pc24.ft{i}.no", no_zh, no_es, no_en)
    P(f"pc24.ft{i}.t", t_zh, t_es, t_en)
    P(f"pc24.ft{i}.p", p_zh, p_es, p_en)

# ---- 03 样机 ----
P("pc24.mk1.cap", "内页展示 · 一月日历正面",
  "Página interior · Calendario de enero", "Inner page · January calendar")
P("pc24.mk2.cap", "立式桌面 · 封面主视觉",
  "En pie sobre la mesa · Portada", "Standing on a desk · Cover key visual")

# ---- 04 平铺图分组标题 ----
P("pc24.fg1.t", "封面 · 特别扉页 · 封底", "Cubierta, aperturas y contracubierta", "Cover · openings · back cover")
P("pc24.fg1.n", "4 PAGES", "4 LÁMINAS", "4 PLATES")
P("pc24.fg2.t", "12 个月楼层主题插画页", "12 ilustraciones temáticas de planta", "12 floor-themed illustration pages")
P("pc24.fg2.n", "ILLUSTRATION PAGES", "ILUSTRACIONES", "ILLUSTRATIONS")
P("pc24.fg3.t", "12 个月功能日历页", "12 páginas de calendario funcional", "12 functional calendar pages")
P("pc24.fg3.n", "CALENDAR PAGES", "CALENDARIO", "CALENDAR PAGES")

# ---- 平铺图：封面组 ----
PLATES_HEAD = [
    ("cover", "封面", "Cubierta", "Cover",
     "2024 龙年主视觉", "Visual Año del Dragón 2024", "2024 Dragon-year key visual"),
    ("timemanage", "扉页 · 时间管理", "Apertura · Gestión del tiempo", "Opening · Time management",
     "12月格子装饰", "12 casillas mensuales", "12 monthly grids"),
    ("family", "扉页 · 全家福", "Apertura · Retrato familiar", "Opening · Family portrait",
     "咱老百姓的商场", "El centro del pueblo", "The people's mall"),
    ("back", "封底", "Contracubierta", "Back cover",
     "咱老百姓的商场", "El centro del pueblo", "The people's mall"),
]
for slug, t_zh, t_es, t_en, s_zh, s_es, s_en in PLATES_HEAD:
    P(f"pc24.pl.{slug}.t", t_zh, t_es, t_en)
    P(f"pc24.pl.{slug}.s", s_zh, s_es, s_en)

# ---- 12 个月 ----
MONTH_CN = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
MONTH_EN = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]

THEME_ZH = ["金龙送福", "1F黄金珠宝", "2F二楼鞋履", "3F运动", "4F品质女装",
            "6F运动童装", "建店67周年", "负1F八方电器", "3F运动户外", "新大楼24周年",
            "7F羽绒服", "5F大众女装"]
THEME_ES = ["Dragón dorado trae fortuna", "Oro y joyas 1F", "Zapatos 2F", "Deporte 3F", "Moda femenina 4F",
            "Deporte infantil 6F", "67º aniversario", "Electrodomésticos Bafang −1F", "Deporte al aire libre 3F", "24º nuevo edificio",
            "Abrigos 7F", "Moda femenina popular 5F"]
THEME_EN = ["Golden dragon brings fortune", "1F gold & jewellery", "2F shoes", "3F sports", "4F quality womenswear",
            "6F kids' sportswear", "67th anniversary", "B1F Bafang appliances", "3F outdoor sports", "New building's 24th",
            "7F down jackets", "5F popular womenswear"]

TERMS_ZH = ["元旦 · 小寒 · 腊八", "立春 · 除夕 · 春节 · 元宵", "惊蛰 · 春分 · 妇女节", "清明 · 谷雨",
            "立夏 · 小满 · 母亲节", "芒种 · 夏至 · 端午 · 儿童节", "小暑 · 大暑", "立秋 · 处暑 · 七夕",
            "白露 · 秋分 · 中秋 · 教师节", "寒露 · 霜降 · 国庆", "立冬 · 小雪 · 感恩节", "大雪 · 冬至 · 平安夜 · 圣诞"]
TERMS_ES = ["Año Nuevo · Frío menor · Fest. Laba",
            "Inicio prima. · Nochevieja · Año Nuevo · Farolillos",
            "Despertar insectos · Equinoccio prima. · Día mujer",
            "Claridad pura · Lluvia grano",
            "Inicio verano · Plenitud menor · Día madre",
            "Espiga en espiga · Solsticio verano · Bote dragón · Día niño",
            "Calor menor · Calor mayor", "Inicio otoño · Fin calor · Noche de Vía Láctea",
            "Rocío blanco · Equinoccio otoño · Medio Otoño · Día maestro",
            "Rocío frío · Caída escarcha · Fiesta Nacional",
            "Inicio invierno · Nieve menor · Día Acción Gracias",
            "Nieve mayor · Solsticio invierno · Nochebuena · Navidad"]
TERMS_EN = ["New Year's Day · Minor Cold · Laba",
            "Start of Spring · CNY Eve · Spring Festival · Lantern Festival",
            "Awakening Insects · Spring Equinox · Women's Day",
            "Pure Brightness · Grain Rain",
            "Start of Summer · Grain Full · Mother's Day",
            "Grain in Ear · Summer Solstice · Dragon Boat · Children's Day",
            "Minor Heat · Major Heat", "Start of Autumn · End of Heat · Qixi",
            "White Dew · Autumn Equinox · Mid-Autumn · Teachers' Day",
            "Cold Dew · Frost's Descent · National Day",
            "Start of Winter · Minor Snow · Thanksgiving",
            "Major Snow · Winter Solstice · Christmas Eve · Christmas"]

DESC_ZH = [
    "龙年开场，金龙腾跃，小女孩平平举福字、另一个平平举绣球，灯笼鞭炮烟花齐鸣，红色背景喜气洋洋，「平原商场恭祝全市人民」。",
    "情人节 × 1F 黄金珠宝广场，平平情侣在心形钻石前浪漫相拥，玫瑰与项链环绕，「引领饰尚 饰爱一生」，粉色背景温柔浪漫。",
    "2F 二楼鞋履，鞋架上展示各式鞋履，平平导购热情接待顾客，「足下之乐 品质生活」「让您自信走好每一步」，薄荷绿背景春日清新。",
    "3F 运动楼层，NIKE、特步、QIAODAN、ANTA、361° 五大运动品牌齐聚，平平们跑步冲线，「给走向未来的路，一个加速度」，青绿色背景充满活力。",
    "4F 四楼品质女装，平平撑伞漫步石桥，燕子与荷叶环绕，「扮靓美丽新乡 四楼品质女装」，暖黄色调温婉动人。",
    "6F 运动童装，乔克叔叔、361°、七波辉、皇室童缘四大童装品牌，平平玩篮球，向日葵环绕，「运动童装 快乐童年有我」，天蓝色调充满童趣。",
    "平原商场建店 67 周年庆，67 大字与商场大楼蛋糕，平平们举杯庆祝，气球烟花齐飞，紫色庆典背景热闹非凡。",
    "负1F 八方电器，平平情侣窝在沙发看电视，空调、洗衣机、冰箱环绕，玫瑰花装饰，「买电器到八方 天天都低价 省钱到八方」，米色背景夏日清凉。",
    "3F 运动户外，PEAK、ERKE、超斯特、贵人鸟、PLAYBOY 五大品牌，平平跳伞翱翔，「轻若无物，运动无负担」，橄榄绿色调自由奔放。",
    "新大楼开业 24 周年，平平逛街购物满载而归，商场大楼前烟花绽放，「24 years」，宝蓝色庆典背景喜庆隆重。",
    "「天冷了！买羽绒服就到平原商场7楼」，雪屋服装店前平平裹着厚厚的羽绒服，雪花飘落，红色背景温暖治愈。",
    "5F 五楼大众女装，平平喝着热奶茶，服装店橱窗里圣诞树与礼物，「为您精选每一季」，米色背景年末温馨。",
]
DESC_ES = [
    "Arranca el Año del Dragón: un dragón dorado se eleva, la niña Pingping alza el carácter fu y otra Pingping sostiene una bola bordada, entre faroles, petardos y fuegos artificiales sobre un fondo rojo festivo: «Pingyuan felicita a toda la ciudad».",
    "San Valentín en la plaza de oro y joyas del 1F: la pareja de Pingping se abraza ante un diamante en forma de corazón, rodeada de rosas y collares; «liderar la moda, amar para siempre», sobre un fondo rosa tierno.",
    "Zapatos del 2F: estanterías con todo tipo de calzado y una Pingping dependienta que atiende con entusiasmo; «el placer de los pies, vida de calidad» y «que camines con confianza cada paso», sobre un fondo menta primaveral.",
    "Deportes en el 3F: NIKE, Xtep, QIAODAN, ANTA y 361° se reúnen mientras las Pingping corren hacia la meta; «un impulso para el camino hacia el futuro», sobre un fondo verde azulado lleno de energía.",
    "Moda femenina de calidad del 4F: Pingping pasea con sombrilla por un puente de piedra entre golondrinas y hojas de loto; «embellecer la bella Xinxiang, moda femenina de calidad del 4F», en tonos amarillo cálido.",
    "Deporte infantil del 6F: las marcas 乔克叔叔, 361°, 七波辉 y 皇室童缘 rodean a una Pingping jugando al baloncesto entre girasoles; «deporte infantil, la infancia feliz cuenta conmigo», en azul celeste lleno de ternura.",
    "67º aniversario de fundación: el gran «67» y una tarta con forma del edificio, Pingpings brindando entre globos y fuegos artificiales sobre un fondo púrpura de fiesta.",
    "Electrodomésticos Bafang del −1F: la pareja de Pingping ve la tele en el sofá rodeada de aire acondicionado, lavadora y nevera con rosas; «compra electrodomésticos en Bafang, precios bajos todos los días», sobre un fondo beige veraniego.",
    "Deporte al aire libre del 3F: PEAK, ERKE, 超斯特, 贵人鸟 y PLAYBOY, con Pingping volando en paracaídas; «ligero como nada, deporte sin carga», en tonos verde oliva libres.",
    "24º aniversario del nuevo edificio: Pingping vuelve de las compras cargada de bolsas mientras estallan fuegos ante el edificio; «24 years», sobre un fondo azul zafiro ceremonial.",
    "«¡Hace frío! Los abrigos se compran en el 7F de Pingyuan»: Pingping, arropada con un grueso plumífero ante la tienda cabaña de nieve, entre copos que caen, sobre un fondo rojo cálido.",
    "Moda femenina popular del 5F: Pingping bebe té caliente mientras el escaparate luce árbol de Navidad y regalos; «seleccionado para ti cada temporada», sobre un fondo beige de fin de año.",
]
DESC_EN = [
    "The Dragon year opens: a golden dragon soars, girl Pingping holds up the fu character while another carries an embroidered ball, amid lanterns, firecrackers and fireworks on a festive red backdrop — \"Pingyuan greets the whole city\".",
    "Valentine's Day at the 1F gold-and-jewellery plaza: Pingping's couple embraces before a heart-shaped diamond, framed by roses and necklaces — \"leading fashion, loving for life\", on a tender pink background.",
    "2F shoes: racks of every kind of footwear and a shop-assistant Pingping greeting customers warmly — \"the joy underfoot, quality life\" and \"walk every step with confidence\", on a fresh mint-green spring background.",
    "3F sports floor: NIKE, Xtep, QIAODAN, ANTA and 361° gather as the Pingpings sprint to the finish line — \"give the road to the future an acceleration\", on an energetic teal background.",
    "4F quality womenswear: Pingping strolls with an umbrella across a stone bridge among swallows and lotus leaves — \"beautify beautiful Xinxiang, 4F quality womenswear\", in warm yellow tones.",
    "6F kids' sportswear: brands Uncle Joe, 361°, Qibohui and Royal Kids surround a basketball-playing Pingping among sunflowers — \"kids' sportswear, happy childhood counts on me\", in playful sky blue.",
    "The mall's 67th founding anniversary: a giant \"67\" and a building-shaped cake, Pingpings raising glasses amid balloons and fireworks on a lively purple festive backdrop.",
    "B1F Bafang appliances: Pingping's couple cuddles on the sofa watching TV, surrounded by air conditioning, washing machine and fridge with roses — \"buy appliances at Bafang, low prices every day\", on a cool beige summer background.",
    "3F outdoor sports: PEAK, ERKE, Chaosite, Guirenniao and PLAYBOY, with Pingping skydiving — \"light as nothing, sport without burden\", in free-spirited olive green.",
    "The new building's 24th anniversary: Pingping returns from shopping loaded with bags as fireworks burst before the mall — \"24 years\", on a ceremonious sapphire-blue backdrop.",
    "\"It's cold! Buy down jackets on the 7th floor of Pingyuan Mall\": Pingping bundled in a thick down jacket before the snow-hut store, snowflakes drifting, on a warm red background.",
    "5F popular womenswear: Pingping sips hot milk tea while the shop window glows with a Christmas tree and gifts — \"selected for you every season\", on a cozy beige year-end background.",
]

for i in range(12):
    n = i + 1
    P(f"pc24.pl.ill{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc24.pl.ill{n}.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc24.pl.cal{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc24.pl.cal{n}.s", "公历 · 农历 · 节气", "Gregoriano · lunar · términos", "Solar · lunar · terms")
    P(f"pc24.m{n}.name", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc24.m{n}.en", MONTH_EN[i].upper(), MONTH_CN[i], MONTH_CN[i])
    P(f"pc24.m{n}.desc", DESC_ZH[i], DESC_ES[i], DESC_EN[i])
    P(f"pc24.m{n}.ill.t", "插画页", "Ilustración", "Illustration")
    P(f"pc24.m{n}.ill.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc24.m{n}.cal.t", "日历页", "Calendario", "Calendar")
    P(f"pc24.m{n}.cal.s", TERMS_ZH[i], TERMS_ES[i], TERMS_EN[i])

# ---- 06 封底 · 尾声 ----
P("pc24.cl.back.t", "封底", "Contracubierta", "Back cover")
P("pc24.cl.back.s", "咱老百姓的商场", "El centro del pueblo", "The people's mall")
P("pc24.cl.sum.t", "扉页 · 商场全家福", "Apertura · Retrato familiar", "Opening · Family portrait")
P("pc24.cl.sum.s", "咱老百姓的商场", "El centro del pueblo", "The people's mall")

# ---- 页脚 ----
P("pc24.footer.note", "平原商场 · 2024 甲辰龙年台历设计 — 作品集展示",
  "Pingyuan Mall · Calendario anual 2024 — Presentación de proyecto",
  "Pingyuan Mall · 2024 Annual Calendar — Project showcase")
P("pc24.backtop", "返回顶部", "Volver arriba", "Back to top")

VD = {k: (zh, es, en) for k, zh, es, en in TRI}
ORDER = [k for k, _, _, _ in TRI]

config = dict(
    prefix=prefix,
    work_id="pingyuan-calendar-2024",
    out_html="work-pingyuan2024-calendar.html",
    img="assets/works/pingyuan-calendar-2024",
    begin="/* >>> generated: pingyuan-calendar-2024 >>> */",
    end="/* <<< generated: pingyuan-calendar-2024 <<< */",
    nav_back_key="pc24.nav.back",
    overview_rows=["client", "type", "year", "pages", "mascot"],
    features_count=4,
    months_count=12,
    stats=[("28", "pc24.stat.pages"), ("12", "pc24.stat.months"),
           ("2", "pc24.stat.sheets"), ("1", "pc24.stat.mascot")],
    flat_g1=[("cover", "cover"), ("timemanage", "timemanage"), ("family", "family"), ("back", "backcover")],
    flat_g2=[(f"ill{i}", f"ill-{i:02d}") for i in range(1, 13)],
    flat_g3=[(f"cal{i}", f"cal-{i:02d}") for i in range(1, 13)],
    closing=[("backcover", "pc24.cl.back.t", "pc24.cl.back.s"),
             ("family", "pc24.cl.sum.t", "pc24.cl.sum.s")],
)

if __name__ == "__main__":
    n, out = build(config, ORDER, VD)
    print(f"i18n.js  ← {n} 个 pc24.* 键 × 3 语言")
    print(f"页面      ← {out}  ({len(ORDER)} 键)")
