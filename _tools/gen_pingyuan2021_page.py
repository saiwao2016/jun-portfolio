#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「平原商场 · 2021 辛丑牛年台历设计」作品专题页（三语）。

文案唯一真源在此（K 函数），由 pingyuan_common.build 同时产出：
  (a) assets/js/i18n.js 里 zh/es/en 三个语言块的 pc21.* 键（按标记幂等插入）
  b) work-pingyuan2021-calendar.html（静态兜底 = 中文值，零漂移）

用法：python3 _tools/gen_pingyuan2021_page.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pingyuan_common import make_registrar, build

K, TRI, KEYS = make_registrar()
prefix = "pc21"


def P(key, zh, es, en):
    K(key, zh, es, en)
    return zh


# ---- 页面元信息 ----
P("pc21.meta.title", "平原商场 · 2021 辛丑牛年台历设计 — JUN",
  "Pingyuan Mall · Calendario anual 2021 — JUN",
  "Pingyuan Mall · 2021 Annual Calendar — JUN")
P("pc21.meta.desc",
  "平原商场 2021 辛丑牛年台历设计：以苹果「平平」为品牌吉祥物，报纸扉页与明信片双特别页、12 个月楼层主题插画、12 页功能日历，跟着平平逛遍商场每一层。平面设计作品，周骏（JUN）设计。",
  "Calendario anual 2021 del centro comercial Pingyuan: la manzana «Pingping» como mascota de marca, una página de periódico y una postal como páginas especiales, 12 ilustraciones temáticas por plantas y 12 páginas de calendario funcional. Diseño gráfico de JUN (Zhou Jun).",
  "The 2021 annual calendar for Pingyuan Mall: the apple mascot \"Pingping\", a newspaper opening page and a postcard as two special pages, 12 floor-themed illustrations and 12 functional calendar pages — follow Pingping through every floor. Graphic design by JUN (Zhou Jun).")

# ---- 页内子导航 ----
P("pc21.nav.overview", "项目概览", "Resumen", "Overview")
P("pc21.nav.features", "设计亮点", "Destacados", "Highlights")
P("pc21.nav.mockups", "样机展示", "Maquetas", "Mockups")
P("pc21.nav.flat", "平铺图", "Láminas", "Flat layout")
P("pc21.nav.months", "逐月作品", "Mes a mes", "Month by month")
P("pc21.nav.back", "返回作品集", "Volver a proyectos", "Back to works")

# ---- Hero ----
P("pc21.hero.kicker", "DESIGN PORTFOLIO · 2021", "DESIGN PORTFOLIO · 2021", "DESIGN PORTFOLIO · 2021")
P("pc21.hero.title", "平原商场", "Pingyuan Mall", "Pingyuan Mall")
P("pc21.hero.sub", "2021 辛丑牛年台历设计",
  "Calendario anual 2021 · Año del Buey",
  "2021 Annual Calendar · Year of the Ox")
P("pc21.hero.desc",
  "一套以苹果吉祥物「平平」为主角的年度台历：报纸扉页与明信片双特别页、12 个月楼层主题插画、12 页功能日历，跟着平平逛遍商场每一层，既是时间工具，也是商场全年的品牌画卷。",
  "Un calendario anual protagonizado por la manzana «Pingping»: una página de periódico y una postal como aperturas especiales, 12 ilustraciones temáticas por plantas y 12 páginas de calendario funcional; acompaña a Pingping por cada piso del centro — herramienta de tiempo y retrato de marca del año.",
  "An annual calendar led by the apple mascot Pingping: a newspaper opening and a postcard as two special pages, 12 floor-themed illustrations and 12 functional calendar pages — follow Pingping through every floor, both a date tool and a year-long brand canvas.")
P("pc21.hero.figcap", "封面样机 · 桌面展示",
  "Maqueta de cubierta · Escritorio", "Cover mockup · Desktop")
P("pc21.stat.pages", "个版面", "láminas", "plates")
P("pc21.stat.months", "个主题月", "meses temáticos", "themed months")
P("pc21.stat.sheets", "个特别扉页", "págs. especiales", "special pages")
P("pc21.stat.mascot", "个吉祥物", "mascota", "mascot")

# ---- 六个区块标题 ----
P("pc21.sec.overview", "项目概览", "Resumen del proyecto", "Project overview")
P("pc21.sec.overview.tag", "PROJECT OVERVIEW", "PROJECT OVERVIEW", "PROJECT OVERVIEW")
P("pc21.sec.features", "设计亮点", "Destacados del diseño", "Design highlights")
P("pc21.sec.features.tag", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS")
P("pc21.sec.mockups", "样机展示", "Maquetas", "Mockups")
P("pc21.sec.mockups.tag", "MOCKUPS", "MOCKUPS", "MOCKUPS")
P("pc21.sec.flat", "平铺图展示", "Láminas planas", "Flat layout")
P("pc21.sec.flat.tag", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES")
P("pc21.sec.months", "逐月作品", "Mes a mes", "Month by month")
P("pc21.sec.months.tag", "MONTH BY MONTH", "MONTH BY MONTH", "MONTH BY MONTH")
P("pc21.sec.closing", "封底 · 尾声", "Contracubierta y cierre", "Back cover & closing")
P("pc21.sec.closing.tag", "BACK COVER & CLOSING", "BACK COVER & CLOSING", "BACK COVER & CLOSING")

# ---- 01 项目概览 ----
P("pc21.ov.client.k", "客户", "Cliente", "Client")
P("pc21.ov.client.v", "平原商场 Pingyuan Mall", "Centro comercial Pingyuan", "Pingyuan Mall")
P("pc21.ov.type.k", "项目类型", "Tipo", "Type")
P("pc21.ov.type.v", "年度台历 · 平面设计", "Calendario anual · Diseño gráfico", "Annual calendar · Graphic design")
P("pc21.ov.year.k", "设计年份", "Año", "Year")
P("pc21.ov.year.v", "2021 · 辛丑牛年", "2021 · Año del Buey", "2021 · Year of the Ox")
P("pc21.ov.pages.k", "页数", "Páginas", "Pages")
P("pc21.ov.pages.v", "28 个版面", "28 láminas", "28 plates")
P("pc21.ov.mascot.k", "吉祥物", "Mascota", "Mascot")
P("pc21.ov.mascot.v", "平平（苹果延伸形象）", "Pingping (de una manzana)", "Pingping (apple-derived)")
P("pc21.ov.p1",
  "这是为**平原商场**打造的 2021 年度台历。封面以辛丑牛年喜庆氛围开场，金色大牛与苹果吉祥物「平平」家族同框，红色囍字建筑、烟花灯笼、铜钱烘托新年气氛。",
  "Es el calendario anual 2021 creado para **Pingyuan Mall**. La cubierta abre con el ambiente festivo del Año del Buey: un gran buey dorado comparte escena con la familia de la manzana «Pingping», y un edificio con el carácter 囍, fuegos artificiales, faroles y monedas de bronce realzan el aire de Año Nuevo.",
  "This is the 2021 annual calendar made for **Pingyuan Mall**. The cover opens in festive Year-of-the-Ox mood — a golden ox shares the frame with the Pingping apple family, while a 囍-character building, fireworks, lanterns and bronze coins set the New Year tone.")
P("pc21.ov.p2",
  "扉页创新设置**「平原商场报」**报纸风格页与**「平原邮政」**明信片页，前者以头条新闻形式传递品牌理念，后者以邮票和邮戳增添收藏趣味。每月一幅**楼层主题插画**，平平带着家人朋友逛遍商场各楼层——从周大福珠宝到 2F 女鞋箱包，从 3F 运动休闲到 6 楼儿童卖场，从建店 64 周年庆典到新大楼开业 21 周年，把商场的业态地图和品牌故事画进了一整年。",
  "Las páginas de apertura innovan con **«Pingyuan Mall News»**, una página estilo periódico, y **«Pingyuan Post»**, una postal: la primera transmite la filosofía de marca en forma de titular, la segunda añade sellos y matasellos para coleccionar. Cada mes, una **ilustración temática de planta**: Pingping recorre el centro con familia y amigos —de las joyas Chow Tai Fook a zapatos y bolsos en 2F, del deporte en 3F a la zona infantil en 6F, del 64º aniversario de la tienda a los 21 años del nuevo edificio— dibujando el mapa comercial y la historia de marca del centro a lo largo de todo el año.",
  "The opening pages innovate with **\"Pingyuan Mall News\"** — a newspaper-style page — and **\"Pingyuan Post\"** — a postcard: the first delivers the brand philosophy as a headline, the second adds stamps and postmarks for collecting. Each month a **floor-themed illustration**: Pingping tours the mall with family and friends — from Chow Tai Fook jewellery to 2F shoes and bags, from 3F sports to the 6F kids' zone, from the 64th store anniversary to the new building's 21st — drawing the mall's tenant map and brand story across the whole year.")
P("pc21.ov.point1", "苹果吉祥物「平平」贯穿全年", "La manzana «Pingping» recorre el año", "The apple mascot runs through the year")
P("pc21.ov.point2", "报纸扉页 + 明信片双特别页", "Periódico + postal especiales", "Newspaper + postcard special pages")
P("pc21.ov.point3", "每月对应一个商场楼层/业态", "Cada mes, una planta o negocio", "Each month a mall floor or business")
P("pc21.ov.point4", "七月建店64周年 · 十月新大楼21周年", "Julio: 64º aniversario · Oct: 21º del edificio", "July: 64th store anniversary · Oct: 21st of new building")

# ---- 02 设计亮点 ----
FEATURES = [
    ("01 — 牛年封面", "01 — Cubierta Año del Buey", "01 — Year-of-the-Ox cover",
     "苹果吉祥物「平平」", "Mascota: manzana «Pingping»", "Mascot: apple",
     "「平平」是由苹果延伸而来的吉祥物形象，粉色圆润身体、黄色果柄触角、绿叶尾巴，辨识度极高。2021 牛年封面中平平家族与金色大牛同框，热闹喜庆。",
     "«Pingping» es un personaje nacido de una manzana: cuerpo rosado y redondo, antenas de pedúnculo amarillo y cola de hoja verde, con altísima reconocibilidad. En la cubierta de 2021 la familia Pingping comparte escena con un gran buey dorado, llena de alegría y fiesta.",
     "Pingping is a mascot derived from an apple — pink rounded body, yellow stalk antennae and a green-leaf tail, instantly recognizable. On the 2021 Ox-year cover the Pingping family shares the frame with a golden ox, festive and lively."),
    ("02 — 双特别扉页", "02 — Dos aperturas especiales", "02 — Two special opening pages",
     "平原商场报 + 明信片", "Periódico + Postal", "Mall News + Postcard",
     "台历开篇设置两个创意扉页：「平原商场报」以报纸头条形式传递\"做咱老百姓的商场\"品牌理念；「平原邮政」明信片页含邮票和邮戳，增添收藏与互动趣味。",
     "El calendario abre con dos páginas creativas: «Pingyuan Mall News» transmite la filosofía de marca «El centro del pueblo» en forma de titular de periódico; la postal «Pingyuan Post» incluye sellos y matasellos, sumando coleccionismo e interactividad.",
     "The calendar opens with two creative pages: \"Pingyuan Mall News\" delivers the brand philosophy \"The mall of the people\" as a newspaper headline; the \"Pingyuan Post\" postcard page carries stamps and postmarks, adding collecting and interaction fun."),
    ("03 — 楼层主题插画", "03 — Ilustración de planta", "03 — Floor-themed illustration",
     "12 个月逛遍整座商场", "12 meses por todo el centro", "12 months across the whole mall",
     "每月插画对应一个楼层或业态：周大福珠宝、2F 女鞋箱包、3F 运动休闲、4F 精品女装、6 楼儿童卖场、7 楼羽绒服、5 楼内衣，外加建店 64 周年、关爱员工和新大楼 21 周年庆。",
     "Cada mes la ilustración corresponde a una planta o negocio: joyas Chow Tai Fook, zapatos y bolsos en 2F, deporte en 3F, ropa femenina de lujo en 4F, zona infantil en 6F, abrigos en 7F, ropa interior en 5F, más el 64º aniversario de la tienda, el cuidado al empleado y los 21 años del nuevo edificio.",
     "Each month's illustration matches a floor or business: Chow Tai Fook jewellery, shoes and bags on 2F, sports on 3F, premium women's wear on 4F, kids' zone on 6F, down jackets on 7F, lingerie on 5F, plus the 64th store anniversary, caring for staff and the new building's 21st anniversary."),
    ("04 — 功能型日历页", "04 — Página funcional", "04 — Functional calendar page",
     "左插画右日历 + 节气节日", "Ilustración + calendario + términos", "Illustration + calendar + terms",
     "2021 日历页采用左侧吉祥物插画、右侧日历格的新版式，标注公历、农历、节气与传统节日，底部印有「平原商场 咱老百姓的商场」品牌语，翻页之间持续传递品牌温度。",
     "En 2021 la página de calendario adopta un nuevo diseño: ilustración del personaje a la izquierda y cuadrícula del calendario a la derecha, anota fechas gregorianas y lunares, términos solares y festividades, e imprime al pie el lema «Pingyuan, el centro del pueblo», transmitiendo el calor de la marca a cada paso.",
     "In 2021 the calendar page takes a new layout — mascot illustration on the left, calendar grid on the right — marking solar and lunar dates, solar terms and traditional festivals, and printing the brand line \"Pingyuan — the mall of the people\" at the foot, carrying the brand's warmth with every turn."),
]
for i, (no_zh, no_es, no_en, t_zh, t_es, t_en, p_zh, p_es, p_en) in enumerate(FEATURES, 1):
    P(f"pc21.ft{i}.no", no_zh, no_es, no_en)
    P(f"pc21.ft{i}.t", t_zh, t_es, t_en)
    P(f"pc21.ft{i}.p", p_zh, p_es, p_en)

# ---- 03 样机 ----
P("pc21.mk1.cap", "双页展开 · 一月插画与日历",
  "Doble página abierta · Ilustración y calendario",
  "Spread · illustration and calendar page")
P("pc21.mk2.cap", "立式桌面 · 封面主视觉",
  "En pie sobre la mesa · Portada", "Standing on a desk · Cover key visual")

# ---- 04 平铺图分组标题 ----
P("pc21.fg1.t", "封面 · 特别扉页 · 封底", "Cubierta, aperturas y contracubierta", "Cover · special pages · back cover")
P("pc21.fg1.n", "4 PAGES", "4 LÁMINAS", "4 PLATES")
P("pc21.fg2.t", "12 个月楼层主题插画页", "12 ilustraciones temáticas de planta", "12 floor-themed illustration pages")
P("pc21.fg2.n", "ILLUSTRATION PAGES", "ILUSTRACIONES", "ILLUSTRATIONS")
P("pc21.fg3.t", "12 个月功能日历页", "12 páginas de calendario funcional", "12 functional calendar pages")
P("pc21.fg3.n", "CALENDAR PAGES", "CALENDARIO", "CALENDAR PAGES")

# ---- 平铺图：封面组（cover / newspaper / postcard / back）----
PLATES_HEAD = [
    ("cover", "封面", "Cubierta", "Cover",
     "2021 牛年主视觉", "Visual Año Nuevo 2021", "2021 New Year key visual"),
    ("newspaper", "扉页 · 平原商场报", "Apertura · Pingyuan News", "Opening · Mall News",
     "报纸风格页", "Estilo periódico", "Newspaper-style page"),
    ("postcard", "扉页 · 平原邮政明信片", "Apertura · Pingyuan Post", "Opening · Postcard",
     "邮票与邮戳", "Sello y matasello", "Stamps & postmarks"),
    ("back", "封底", "Contracubierta", "Back cover",
     "咱老百姓的商场", "El centro del pueblo", "The people's mall"),
]
for slug, t_zh, t_es, t_en, s_zh, s_es, s_en in PLATES_HEAD:
    P(f"pc21.pl.{slug}.t", t_zh, t_es, t_en)
    P(f"pc21.pl.{slug}.s", s_zh, s_es, s_en)

# ---- 12 个月：中文序数名 / 西英月名 / 插画主题 / 节气 ----
MONTH_CN = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
MONTH_EN = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]

THEME_ZH = ["新年放鞭炮", "周大福珠宝", "2F 女鞋箱包", "3F 运动休闲", "4F 精品女装",
            "6楼儿童卖场", "建店64周年", "7楼羽绒服反季", "关爱员工", "新大楼21周年庆",
            "7楼羽绒服", "5楼内衣"]
THEME_ES = ["Año Nuevo · petardos", "Joyas Chow Tai Fook", "Zapatos y bolsos 2F", "Deporte 3F", "Ropa femenina de lujo 4F",
            "Zona infantil 6F", "64º aniversario", "Abrigos 7º piso (temporada baja)", "Cuidado al empleado", "21º aniversario nuevo edificio",
            "Abrigos 7º piso", "Ropa interior 5F"]
THEME_EN = ["New Year fireworks", "Chow Tai Fook jewellery", "2F shoes & bags", "3F sports & leisure", "4F premium women's wear",
            "6F kids' zone", "64th store anniversary", "7F off-season down jackets", "Caring for staff", "New building 21st anniversary",
            "7F down jackets", "5F lingerie"]

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
    "新年开场，平平们在商场前的雪地里放鞭炮，红灯笼、烟花、铜钱铺满画面，热热闹闹迎新春。",
    "情人节遇上周大福珠宝，平平在珠宝店前上演浪漫求婚，粉色背景烘托甜蜜氛围，「真诚 永恒」。",
    "2F 女鞋箱包卖场，薄荷绿背景清新明快，平平坐在鞋凳上试鞋，「时尚之行，始于足下」。",
    "3F 运动休闲区，佐丹奴、贵人鸟、乐菲图、匹克齐聚，平平们换上运动装在山间步道徒步，春日活力满满。",
    "母亲节 × 4F 精品女装，暖黄花园里小平平给妈妈送上新衣服，「季节在变，选择不变」，温馨动人。",
    "六一儿童节 × 6 楼儿童卖场，狮子、兔子和平平们一起试穿新衣服，「我们擅长的，就是孩子需要的」。",
    "平原商场建店 64 周年（1957.7.1—2021.7.1），紫色庆典背景，平平们戴上皇冠举杯庆祝，囍字、气球、彩纸齐飞。",
    "7 楼羽绒服反季促销开始，平平举着「羽绒服」木牌招揽顾客，冰棍、自动贩卖机点缀夏日，反季聚划算。",
    "「关爱员工，用心打造幸福平原」，平原商场医务室前，平平们提着慰问袋和鲜花，秋日落叶飘洒，温暖人心。",
    "新大楼开业 21 周年庆，飘雪的服装店里平平们忙碌营业，灯笼、皇冠 21 号牌、热咖啡，周年庆氛围浓厚。",
    "「天冷了！买羽绒服就到平原商场七楼」，平平们裹着羽绒服躺在蓬松的棉花上，雪花飘落，温暖又治愈。",
    "5 楼内衣欢迎您，俯拍卧室场景里平平穿着睡衣安睡在被窝中，猫咪、抱枕、暖灯环绕，年末的温柔收尾。",
]
DESC_ES = [
    "Apertura de Año Nuevo: los Pingping sueltan petardos en la nieve frente al centro; faroles rojos, fuegos artificiales y monedas de bronce llenan la escena para recibir la primavera con alegría.",
    "Por San Valentín, junto a las joyas Chow Tai Fook, Pingping representa una propuesta de matrimonio ante la joyería; un fondo rosado realza la dulzura: «Sincero · Eterno».",
    "En la zona de zapatos y bolsos del 2F, sobre fondo verde menta fresco, Pingping prueba zapatos sentado en el banco: «La moda comienza por los pies».",
    "En la zona de deporte del 3F se reúnen Giordano, Guirenniao, Lefetu y Peak; los Pingping se visten de deporte y caminan por senderos de montaña, llenos de energía primaveral.",
    "Día de la Madre × ropa femenina de lujo del 4F: en un cálido jardín amarillo, un pequeño Pingping regala ropa nueva a su madre; «La estación cambia, la elección no», conmovedor.",
    "Día del Niño × zona infantil del 6F: leones, conejos y Pingping prueban ropa nueva juntos; «Lo que sabemos hacer es lo que los niños necesitan».",
    "64º aniversario de Pingyuan Mall (1957.7.1—2021.7.1): sobre fondo de fiesta púrpura, los Pingping se coronan y brindan; caracteres 囍, globos y confeti vuelan.",
    "Empieza la promoción de abrigos de temporada baja en el 7F; Pingping lleva un cartel de «abrigos» para atraer clientes, con helados y máquinas expendedoras en el verano: la mejor oferta de temporada baja.",
    "«Cuidar al empleado, crear un Pingyuan feliz»: ante la enfermería del centro, los Pingping llevan bolsas de consuelo y flores; hojas de otoño caen, cálido y reconfortante.",
    "21º aniversario de la apertura del nuevo edificio: en la tienda de ropa con nieve, los Pingping trabajan afanosos; faroles, corona con el número 21 y café caliente llenan el ambiente de aniversario.",
    "«¡Hace frío! Los abrigos se compran en el 7º piso de Pingyuan»: los Pingping envueltos en abrigos descansan sobre algodón esponjoso, con la nieve cayendo: cálido y sanador.",
    "Ropa interior del 5F les da la bienvenida: en una escena de dormitorio vista desde arriba, Pingping duerme en pijama entre gatos, cojines y luces cálidas: un tierno final de año.",
]
DESC_EN = [
    "New Year opening: the Pingpings set off firecrackers in the snow in front of the mall; red lanterns, fireworks and bronze coins fill the scene to welcome spring with joy.",
    "On Valentine's Day, by Chow Tai Fook jewellery, Pingping stages a romantic proposal in front of the store; a pink backdrop heightens the sweetness: \"Sincere · Eternal\".",
    "At the 2F shoe-and-bag zone, on a fresh mint-green background, Pingping tries on shoes seated on the bench — \"A stylish journey begins at your feet\".",
    "In the 3F sports zone, Giordano, Guirenniao, Lefetu and Peak gather; the Pingpings change into sportswear and hike the mountain trails, full of spring energy.",
    "Mother's Day × 4F premium women's wear: in a warm yellow garden, little Pingping gives Mom new clothes — \"Seasons change, choices don't\" — touching.",
    "Children's Day × 6F kids' zone: lions, rabbits and Pingpings try on new clothes together — \"What we're good at is what children need\".",
    "Pingyuan Mall's 64th anniversary (1957.7.1—2021.7.1): on a festive purple backdrop, the Pingpings don crowns and raise a toast; 囍 characters, balloons and confetti fly.",
    "The 7F off-season down-jacket sale begins; Pingping holds an \"abrigos\" (down jackets) sign to attract customers, with ice lollies and vending machines dotting the summer — the best off-season deal.",
    "\"Care for staff, build a happy Pingyuan\" — in front of the mall's clinic, the Pingpings carry comfort bags and flowers; autumn leaves drift down, warm and heartening.",
    "New building's 21st anniversary: in the snowy clothing store, the Pingpings work busily; lanterns, a crown with the number 21 and hot coffee fill the anniversary mood.",
    "\"It's cold! Buy down jackets on the 7th floor of Pingyuan Mall\" — the Pingpings, wrapped in down, rest on fluffy cotton as snow falls: warm and healing.",
    "5F lingerie welcomes you: in an overhead bedroom scene, Pingping sleeps in pyjamas among cats, cushions and warm lamps — a gentle year-end close.",
]

for i in range(12):
    n = i + 1
    P(f"pc21.pl.ill{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc21.pl.ill{n}.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc21.pl.cal{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc21.pl.cal{n}.s", "公历 · 农历 · 节气", "Gregoriano · lunar · términos", "Solar · lunar · terms")
    P(f"pc21.m{n}.name", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc21.m{n}.en", MONTH_EN[i].upper(), MONTH_CN[i], MONTH_CN[i])
    P(f"pc21.m{n}.desc", DESC_ZH[i], DESC_ES[i], DESC_EN[i])
    P(f"pc21.m{n}.ill.t", "插画页", "Ilustración", "Illustration")
    P(f"pc21.m{n}.ill.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc21.m{n}.cal.t", "日历页", "Calendario", "Calendar")
    P(f"pc21.m{n}.cal.s", TERMS_ZH[i], TERMS_ES[i], TERMS_EN[i])

# ---- 06 封底 · 尾声 ----
P("pc21.cl.back.t", "封底", "Contracubierta", "Back cover")
P("pc21.cl.back.s", "咱老百姓的商场", "El centro del pueblo", "The people's mall")
P("pc21.cl.sum.t", "平原商场报", "Pingyuan Mall News", "Mall News")
P("pc21.cl.sum.s", "做咱老百姓的商场", "El centro del pueblo", "The mall of the people")

# ---- 页脚 ----
P("pc21.footer.note", "平原商场 · 2021 辛丑牛年台历设计 — 作品集展示",
  "Pingyuan Mall · Calendario anual 2021 — Presentación de proyecto",
  "Pingyuan Mall · 2021 Annual Calendar — Project showcase")
P("pc21.backtop", "返回顶部", "Volver arriba", "Back to top")

VD = {k: (zh, es, en) for k, zh, es, en in TRI}
ORDER = [k for k, _, _, _ in TRI]

config = dict(
    prefix=prefix,
    work_id="pingyuan-calendar-2021",
    out_html="work-pingyuan2021-calendar.html",
    img="assets/works/pingyuan-calendar-2021",
    begin="/* >>> generated: pingyuan-calendar-2021 >>> */",
    end="/* <<< generated: pingyuan-calendar-2021 <<< */",
    nav_back_key="pc21.nav.back",
    overview_rows=["client", "type", "year", "pages", "mascot"],
    features_count=4,
    months_count=12,
    stats=[("28", "pc21.stat.pages"), ("12", "pc21.stat.months"),
           ("2", "pc21.stat.sheets"), ("1", "pc21.stat.mascot")],
    flat_g1=[("cover", "cover"), ("newspaper", "newspaper"), ("postcard", "postcard"), ("back", "backcover")],
    flat_g2=[(f"ill{i}", f"ill-{i:02d}") for i in range(1, 13)],
    flat_g3=[(f"cal{i}", f"cal-{i:02d}") for i in range(1, 13)],
    closing=[("backcover", "pc21.cl.back.t", "pc21.cl.back.s"),
             ("newspaper", "pc21.cl.sum.t", "pc21.cl.sum.s")],
)

if __name__ == "__main__":
    n, out = build(config, ORDER, VD)
    print(f"i18n.js  ← {n} 个 pc21.* 键 × 3 语言")
    print(f"页面      ← {out}  ({len(ORDER)} 键)")
