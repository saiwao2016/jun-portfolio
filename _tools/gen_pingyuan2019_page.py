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
OUT_HTML = os.path.join(ROOT, "work-pingyuan2019-calendar.html")
IMG = "assets/works/pingyuan-calendar-2019"

BEGIN = "/* >>> generated: pingyuan-calendar-2019 >>> */"
END = "/* <<< generated: pingyuan-calendar-2019 <<< */"

# 对应 content/works.json 里的作品 id（main.js 用它取上一件/下一件）
WORK_ID = "pingyuan-calendar-2019"

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
# ===== 2019 三语文案块（仅内容，逻辑从 gen_pingyuan_page.py 复用）=====

# ---- 页面元信息 ----
K("pc19.meta.title", "平原商场 · 2019 己亥年台历设计 — JUN",
  "Pingyuan Mall · Calendario anual 2019 — JUN",
  "Pingyuan Mall · 2019 Annual Calendar — JUN")
K("pc19.meta.desc",
  "平原商场 2019 己亥年台历设计：以粉色小鹿「平平」为品牌吉祥物，12 个月品牌主题插画、12 页功能日历，每月对应一个商场楼层与入驻品牌。平面设计作品，周骏（JUN）设计。",
  "Calendario anual 2019 del centro comercial Pingyuan: la cierva rosa «Pingping» como mascota de marca, 12 ilustraciones temáticas de marcas y 12 páginas de calendario funcional, un mes por cada planta y marca del centro. Diseño gráfico de JUN (Zhou Jun).",
  "The 2019 annual calendar for Pingyuan Mall: the pink deer mascot \"Pingping\", 12 brand-themed illustrations and 12 functional calendar pages, each month paired with a mall floor and its stores. Graphic design by JUN (Zhou Jun).")

# ---- 页内子导航 ----
K("pc19.nav.overview", "项目概览", "Resumen", "Overview")
K("pc19.nav.features", "设计亮点", "Destacados", "Highlights")
K("pc19.nav.mockups", "样机展示", "Maquetas", "Mockups")
K("pc19.nav.flat", "平铺图", "Láminas", "Flat layout")
K("pc19.nav.months", "逐月作品", "Mes a mes", "Month by month")
K("pc19.nav.back", "返回作品集", "Volver a proyectos", "Back to works")

# ---- Hero ----
K("pc19.hero.kicker", "DESIGN PORTFOLIO · 2019", "DESIGN PORTFOLIO · 2019", "DESIGN PORTFOLIO · 2019")
K("pc19.hero.title", "平原商场", "Pingyuan Mall", "Pingyuan Mall")
K("pc19.hero.sub", "2019 己亥年台历设计",
  "Calendario anual 2019 · Año del Cerdo",
  "2019 Annual Calendar · Year of the Pig")
K("pc19.hero.desc",
  "一套以粉色小鹿「平平」为品牌吉祥物的年度台历：12 个月份主题插画、12 页功能日历，将商场各楼层与入驻品牌融入吉祥物的生活场景，既是时间工具，也是商场全年的品牌画卷。",
  "Un calendario anual con la cierva rosa «Pingping» como mascota de marca: 12 ilustraciones temáticas y 12 páginas de calendario funcional, donde cada planta y marca del centro se funde en la vida cotidiana de la mascota. Sirve como calendario y como retrato de marca del año entero.",
  "An annual calendar built around the pink deer mascot \"Pingping\": 12 themed illustrations and 12 functional calendar pages, weaving the mall's floors and stores into the mascot's everyday life — both a date tool and a year-long brand portrait.")
K("pc19.hero.figcap", "封面样机 · 桌面展示",
  "Maqueta de cubierta · Escritorio", "Cover mockup · Desktop")
K("pc19.stat.pages", "个版面", "láminas", "plates")
K("pc19.stat.months", "个主题月", "meses temáticos", "themed months")
K("pc19.stat.sheets", "个扉页", "págs. de apertura", "opening pages")
K("pc19.stat.mascot", "个吉祥物", "mascota", "mascot")

# ---- 六个区块标题（英文标签为版面装饰，各语言一致） ----
K("pc19.sec.overview", "项目概览", "Resumen del proyecto", "Project overview")
K("pc19.sec.overview.tag", "PROJECT OVERVIEW", "PROJECT OVERVIEW", "PROJECT OVERVIEW")
K("pc19.sec.features", "设计亮点", "Destacados del diseño", "Design highlights")
K("pc19.sec.features.tag", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS")
K("pc19.sec.mockups", "样机展示", "Maquetas", "Mockups")
K("pc19.sec.mockups.tag", "MOCKUPS", "MOCKUPS", "MOCKUPS")
K("pc19.sec.flat", "平铺图展示", "Láminas planas", "Flat layout")
K("pc19.sec.flat.tag", "FLAT LAYOUT · 28 PLATES", "FLAT LAYOUT · 28 PLATES", "FLAT LAYOUT · 28 PLATES")
K("pc19.sec.months", "逐月作品", "Mes a mes", "Month by month")
K("pc19.sec.months.tag", "MONTH BY MONTH", "MONTH BY MONTH", "MONTH BY MONTH")
K("pc19.sec.closing", "封底 · 尾声", "Contracubierta y cierre", "Back cover & closing")
K("pc19.sec.closing.tag", "BACK COVER & CLOSING", "BACK COVER & CLOSING", "BACK COVER & CLOSING")

# ---- 01 项目概览 ----
K("pc19.ov.client.k", "客户", "Cliente", "Client")
K("pc19.ov.client.v", "平原商场 Pingyuan Mall", "Centro comercial Pingyuan", "Pingyuan Mall")
K("pc19.ov.type.k", "项目类型", "Tipo", "Type")
K("pc19.ov.type.v", "年度台历 · 平面设计", "Calendario anual · Diseño gráfico", "Annual calendar · Graphic design")
K("pc19.ov.year.k", "设计年份", "Año", "Year")
K("pc19.ov.year.v", "2019 · 己亥猪年", "2019 · Año del Cerdo", "2019 · Year of the Pig")
K("pc19.ov.pages.k", "页数", "Páginas", "Pages")
K("pc19.ov.pages.v", "28 个版面", "28 láminas", "28 plates")
K("pc19.ov.extra.k", "主题", "Tema", "Theme")
K("pc19.ov.extra.v", "时光旅历 · 只做咱老百姓的商场", "Viaje en el tiempo · El centro del pueblo", "Time journey · The people's mall")
K("pc19.ov.p1",
  "这是为**平原商场**打造的 2019 年度台历，主题为**「时光旅历」**。扉页以「出彩的足迹」时间轴回顾商场 1957—2018 年的发展历程，再以「贰零壹玖用心体会，只做咱老百姓的商场」开启新一年。",
  "Es el calendario anual 2019 creado para **Pingyuan Mall**. Su tema es **«Viaje en el tiempo»**: una página de apertura con la línea de tiempo «Huellas brillantes» repasa la historia del centro de 1957 a 2018, y el lema «2019 con atención, el centro del pueblo» abre el nuevo año.",
  "This is the 2019 annual calendar made for **Pingyuan Mall**, themed **\"Time Journey\"**. An opening page with the \"Brilliant Footprints\" timeline reviews the mall's history from 1957 to 2018, then the line \"2019 with care — the people's mall\" opens the new year.")
K("pc19.ov.p2",
  "每月一幅**品牌主题插画**，将商场各楼层与入驻品牌（羽绒服、美妆、男装、女鞋、儿童娱乐城、内衣、名表、黄金珠宝等）融入粉色小鹿吉祥物的生活场景；配套日历页标注公历、农历、节气与节日，底部绘制品牌街景，让台历既是时间工具，也是商场全年的品牌画卷。",
  "Cada mes una **ilustración temática de marca** integra las plantas y marcas del centro (abrigos, maquillaje, ropa de hombre, zapatos, zona infantil, ropa interior, relojes, oro y joyas…) en la vida cotidiana de la cierva rosa. La página de calendario anota fechas gregorianas y lunares, términos solares y festividades, y dibuja la calle de marcas al pie: un cuadro de marca de todo el año.",
  "Each month a **brand-themed illustration** folds the mall's floors and stores (down jackets, makeup, menswear, shoes, kids' zone, lingerie, watches, gold and jewellery…) into the pink deer's everyday scene; the paired calendar page marks solar and lunar dates, solar terms and festivals, and draws a brand street at the bottom — making the calendar both a date tool and a year-long brand canvas.")
K("pc19.ov.point1", "粉色小鹿吉祥物贯穿 12 个月",
  "La cierva rosa recorre los 12 meses", "The pink deer runs through all 12 months")
K("pc19.ov.point2", "扉页含商场 60 年历史时间轴",
  "La apertura incluye 60 años de historia", "Opening holds a 60-year history timeline")
K("pc19.ov.point3", "每月对应一个商场品牌/楼层主题",
  "Cada mes, una marca o planta del centro", "Each month a mall brand or floor theme")
K("pc19.ov.point4", "日历页底部绘制品牌街景",
  "Calle de marcas al pie del calendario", "Brand street drawn at the calendar foot")

# ---- 02 设计亮点 ----
FEATURES = [
    ("01 — 时光旅历主题", "01 — Tema: Viaje en el tiempo", "01 — Theme: Time journey",
     "扉页讲述商场 60 年", "La apertura cuenta 60 años", "Opening tells 60 years",
     "封面以猪年喜庆氛围开场，「出彩的足迹」时间轴串联 1957 年开业至 2018 年蝶变升级的十个关键节点，再由「时光旅历」标题页承上启下，把品牌历史写进新年。",
     "La cubierta abre con el ambiente festivo del Año del Cerdo; la línea de tiempo «Huellas brillantes» enlaza diez hitos del centro desde su apertura en 1957 hasta su transformación en 2018, y la página título «Viaje en el tiempo» sirve de puente para escribir la historia de marca en el nuevo año.",
     "The cover opens in festive Year-of-the-Pig mood; the \"Brilliant Footprints\" timeline links ten milestones from the 1957 opening to the 2018 upgrade, and the \"Time Journey\" title page bridges them, writing the brand's history into the new year."),
    ("02 — 粉色小鹿吉祥物", "02 — Mascota: cierva rosa", "02 — Mascot: pink deer",
     "一只鹿逛遍整座商场", "Una cierva recorre el centro", "One deer roams the whole mall",
     "拟人化的粉色小鹿是全年主角，它试羽绒服、买美妆、逛男装、挑女鞋、带娃去娱乐城、选黄金珠宝……以顾客视角把商场各楼层串成一条温暖的生活动线。",
     "La cierva rosa antropomórfica es la protagonista del año: prueba abrigos, compra maquillaje, recorre la ropa de hombre, elige zapatos, lleva a los niños a la zona infantil y escoge oro y joyas… Desde la mirada del cliente, enlaza las plantas del centro en una cálida línea de vida.",
     "The anthropomorphic pink deer is the year's lead — trying on down jackets, buying makeup, browsing menswear, picking shoes, taking the kids to the play zone, choosing gold and jewellery… seen through the customer's eyes, it strings the mall's floors into one warm daily thread."),
    ("03 — 月度品牌插画", "03 — Ilustración de marca", "03 — Monthly brand illustration",
     "12 个月 12 个品牌场景", "12 meses, 12 escenas de marca", "12 months, 12 brand scenes",
     "每月一幅原创插画对应一个入驻品牌或楼层：强人鞋、花花公子、曼卡璐、猫人内衣、九鹿王、老庙黄金、老凤祥……插画底部配品牌 slogan，商业信息自然融入叙事。",
     "Cada mes una ilustración original corresponde a una marca o planta: Qiangren, Playboy, Manka Road, Miao Ren, Jiuluwang, Laomiao Gold, Lao Feng Xiang… El slogan de marca al pie de cada ilustración funde la información comercial en la narrativa.",
     "Each month an original illustration matches a store or floor: Qiangren, Playboy, Manka Road, Cat Man, Jiuluwang, Laomiao Gold, Lao Feng Xiang… a brand slogan at the foot of each illustration blends the commercial message into the story."),
    ("04 — 功能型日历页", "04 — Página funcional", "04 — Functional calendar page",
     "节气节日 + 品牌街景", "Términos solares + calle de marcas", "Solar terms + brand street",
     "日历页标注公历、农历、节气与传统节日，底部绘制当月主题品牌的店铺街景，与插画页呼应，把日常翻页变成一次商场橱窗漫步。",
     "La página de calendario anota fechas gregorianas y lunares, términos solares y festividades tradicionales, y dibuja la calle de la marca del mes al pie, haciendo eco de la ilustración: pasar las páginas se vuelve un paseo por los escaparates del centro.",
     "The calendar page marks solar and lunar dates, solar terms and traditional festivals, and draws the month's brand street at the foot, echoing the illustration — turning daily page-turning into a stroll past the mall's windows."),
]
for i, (no_zh, no_es, no_en, t_zh, t_es, t_en, p_zh, p_es, p_en) in enumerate(FEATURES, 1):
    K(f"pc19.ft{i}.no", no_zh, no_es, no_en)
    K(f"pc19.ft{i}.t", t_zh, t_es, t_en)
    K(f"pc19.ft{i}.p", p_zh, p_es, p_en)

# ---- 03 样机 ----
K("pc19.mk1.cap", "双页展开 · 一月插画与日历",
  "Doble página abierta · Ilustración y calendario",
  "Spread · illustration and calendar page")
K("pc19.mk2.cap", "立式桌面 · 封面主视觉",
  "En pie sobre la mesa · Portada", "Standing on a desk · Cover key visual")

# ---- 04 平铺图分组标题 ----
K("pc19.fg1.t", "封面 · 扉页 · 封底", "Cubierta, apertura y contracubierta", "Cover · opening · back cover")
K("pc19.fg1.n", "4 PAGES", "4 LÁMINAS", "4 PLATES")
K("pc19.fg2.t", "12 个月品牌主题插画页", "12 ilustraciones temáticas de marca", "12 brand-themed illustration pages")
K("pc19.fg2.n", "ILLUSTRATION PAGES", "ILUSTRACIONES", "ILLUSTRATIONS")
K("pc19.fg3.t", "12 个月功能日历页", "12 páginas de calendario funcional", "12 functional calendar pages")
K("pc19.fg3.n", "CALENDAR PAGES", "CALENDARIO", "CALENDAR PAGES")

# ---- 平铺图：封面组 ----
PLATES_HEAD = [
    ("cover", "封面", "Cubierta", "Cover",
     "2019 猪年主视觉", "Visual Año Nuevo 2019", "2019 New Year key visual"),
    ("plan", "扉页·出彩的足迹", "Apertura · Huellas", "Opening · Footprints",
     "1957—2018 商场历程", "1957—2018 trayectoria", "1957—2018 journey"),
    ("summary", "扉页·时光旅历", "Apertura · Viaje en el tiempo", "Opening · Time journey",
     "贰零壹玖用心体会", "2019 con atención", "2019 with care"),
    ("back", "封底", "Contracubierta", "Back cover",
     "咱老百姓的商场", "El centro del pueblo", "The people's mall"),
]
for slug, t_zh, t_es, t_en, s_zh, s_es, s_en in PLATES_HEAD:
    K(f"pc19.pl.{slug}.t", t_zh, t_es, t_en)
    K(f"pc19.pl.{slug}.s", s_zh, s_es, s_en)

# ---- 12 个月：中文序数名 / 西英月名 / 插画主题 / 节气 ----
MONTH_CN = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_CN_PLAIN = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
MONTH_EN = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]

THEME_ZH = ["羽绒服季", "春节回家 强人鞋", "平原美妆", "花花公子男装", "曼卡璐女鞋", "六楼儿童娱乐城",
            "猫人内衣", "平原名表", "九鹿王男装", "仕乐内衣", "老庙黄金", "老凤祥珠宝"]
THEME_ES = ["Temporada de abrigos", "Año Nuevo y Qiangren", "Maquillaje Pingyuan", "Trajes Playboy", "Zapatos Manka Road", "Zona infantil 6º piso",
            "Ropa interior Miao Ren", "Relojes Pingyuan", "Trajes Jiuluwang", "Ropa interior Shile", "Oro Laomiao", "Joyería Lao Feng Xiang"]
THEME_EN = ["Down jacket season", "Spring Festival · Qiangren", "Pingyuan makeup", "Playboy menswear", "Manka Road shoes", "6th-floor kids zone",
            "Cat Man lingerie", "Pingyuan watches", "Jiuluwang menswear", "Shile lingerie", "Laomiao Gold", "Lao Feng Xiang jewellery"]

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
    "深冬羽绒服季，小鹿在试衣间里换上新装，「天冷了，买羽绒服就到平原商场 7 楼」。",
    "春节回家团圆，小鹿提着强人鞋的购物袋与家人围坐，「新强人，新产品，新服务」。",
    "梳妆台前口红、眼影、化妆刷一字排开，「平原美妆，靓丽新乡」，春日焕新颜。",
    "花花公子男装新品发布会，戴墨镜的小鹿在闪光灯下登场，「最愉快，最有价值的生活」。",
    "曼卡璐女鞋化作花丛中的高跟鞋，长着翅膀的小鹿探出头，「不迈平庸步，只走非凡路」。",
    "六楼儿童用品娱乐城，泰迪熊、街机、篮球架一应俱全，小鹿牵着孩子的手走进彩虹门。",
    "猫人内衣的聚光灯橱窗里，小鹿认真挑选，「最合适的，才是真正最好的」。",
    "平原名表柜台前，小鹿隔着玻璃欣赏腕表，领结一戴，时光也变得讲究起来。",
    "九鹿王男装户外广告拍摄现场，小鹿与真鹿同框，「逐生活之悦」，秋日型格上线。",
    "仕乐内衣的星空下，两只小鹿躺在云朵上安睡，「更懂你的舒适，不薄不厚刚刚好」。",
    "老庙黄金门店前，「11 月会员感恩月」的立牌醒目，小鹿推门而入，暖意融融。",
    "老凤祥百年老店前，小鹿撑伞赴约，西装领结与旗袍项链，一年的故事在珠宝光泽里收官。",
]
DESC_ES = [
    "En pleno invierno de abrigos, la cierva se prueba ropa nueva en el probador: «Hace frío, los abrigos se compran en el 7º piso de Pingyuan».",
    "Reunión familiar por el Año Nuevo; la cierva lleva la bolsa de Qiangren y se sienta con la familia: «Nuevo Qiangren, nuevo producto, nuevo servicio».",
    "Ante el tocador, pintalabios, sombras y brochas alineados: «Maquillaje Pingyuan, hermosa Xinxiang», un rostro renovado en primavera.",
    "Desfile de nueva colección de Playboy; la cierva con gafas de sol deslumbra bajo las luces: «La vida más alegre y valiosa».",
    "Los tacones Manka Road florecen entre las flores; la cierva alada asoma: «Ni un paso mediocre, solo un camino extraordinario».",
    "En la zona infantil del 6º piso hay osos de peluche, máquinas arcade y canastas; la cierva entra por la puerta del arcoíris de la mano del niño.",
    "En el escaparate iluminado de Miao Ren, la cierva elige con cuidado: «Lo más adecuado es lo verdaderamente mejor».",
    "Ante el mostrador de relojes Pingyuan, la cierva admira los relojes tras el cristal; con la pajarita, el tiempo se vuelve elegante.",
    "En el rodaje exterior de Jiuluwang, la cierva comparte plano con un ciervo real: «Siguiendo la alegría de vivir», el estilo otoñal llega.",
    "Bajo el cielo estrellado de Shile, dos ciervas duermen en las nubes: «Más cómodo para ti, ni fino ni grueso, justo lo justo».",
    "Frente a la tienda de Oro Laomiao, el cartel «Noviembre, mes de gratitud a socios» destaca; la cierva entra, llena de calidez.",
    "Ante la centenaria Lao Feng Xiang, la cierva acude con paraguas y pajarita; junto al cheongsam y el collar, la historia del año cierra con el brillo de las joyas.",
]
DESC_EN = [
    "Deep winter, down-jacket season: the deer tries on new clothes in the fitting room — \"When it's cold, buy down jackets on the 7th floor of Pingyuan Mall.\"",
    "Spring Festival reunion: the deer carries a Qiangren shoe bag and sits with family — \"New Qiangren, new product, new service.\"",
    "At the dressing table, lipstick, eyeshadow and brushes lined up — \"Pingyuan makeup, beautiful Xinxiang,\" a fresh face for spring.",
    "A Playboy menswear launch; the deer in sunglasses steps into the flash — \"The happiest, most worthwhile life.\"",
    "Manka Road heels bloom among the flowers; a winged deer peeks out — \"No mediocre step, only an extraordinary path.\"",
    "On the 6th-floor kids' zone, teddy bears, arcade machines and hoops are all there; the deer walks through the rainbow gate hand in hand with the child.",
    "In Cat Man's spotlight window, the deer picks carefully — \"The most suitable is truly the best.\"",
    "At the Pingyuan watch counter, the deer admires the watches through the glass; with the bow tie, time turns refined.",
    "On the Jiuluwang menswear outdoor shoot, the deer shares the frame with a real deer — \"Chasing the joy of living,\" autumn style arrives.",
    "Under Shile's starry sky, two deer doze on the clouds — \"Comfort that knows you: not thin, not thick, just right.\"",
    "In front of Laomiao Gold, the \"November Member Gratitude Month\" stand stands out; the deer steps in, warm inside.",
    "Before century-old Lao Feng Xiang, the deer keeps the date with umbrella and bow tie; with the cheongsam and necklace, the year's story closes in the glow of jewellery.",
]

for i in range(12):
    n = i + 1
    K(f"pc19.pl.ill{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    K(f"pc19.pl.ill{n}.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    K(f"pc19.pl.cal{n}.t", MONTH_CN_PLAIN[i], MONTH_ES[i], MONTH_EN[i])
    K(f"pc19.pl.cal{n}.s", "公历 · 农历 · 节气", "Gregoriano · lunar · términos", "Solar · lunar · terms")
    K(f"pc19.m{n}.name", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    K(f"pc19.m{n}.en", MONTH_EN[i].upper(), MONTH_CN[i], MONTH_CN[i])
    K(f"pc19.m{n}.desc", DESC_ZH[i], DESC_ES[i], DESC_EN[i])
    K(f"pc19.m{n}.ill.t", "插画页", "Ilustración", "Illustration")
    K(f"pc19.m{n}.ill.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    K(f"pc19.m{n}.cal.t", "日历页", "Calendario", "Calendar")
    K(f"pc19.m{n}.cal.s", TERMS_ZH[i], TERMS_ES[i], TERMS_EN[i])

# ---- 06 封底 · 尾声 ----
K("pc19.cl.back.t", "封底", "Contracubierta", "Back cover")
K("pc19.cl.back.s", "咱老百姓的商场", "El centro del pueblo", "The people's mall")
K("pc19.cl.sum.t", "时光旅历", "Viaje en el tiempo", "Time journey")
K("pc19.cl.sum.s", "贰零壹玖用心体会", "2019 con atención", "2019 with care")

# ---- 页脚 ----
K("pc19.footer.note", "平原商场 · 2019 己亥年台历设计 — 作品集展示",
  "Pingyuan Mall · Calendario anual 2019 — Presentación de proyecto",
  "Pingyuan Mall · 2019 Annual Calendar — Project showcase")
K("pc19.backtop", "返回顶部", "Volver arriba", "Back to top")

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
    lines = ["", "    /* ---- 作品专题页：平原商场 · 2019 台历 ---- */"]
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
    for sid, key in [("pc-overview", "pc19.nav.overview"), ("pc-features", "pc19.nav.features"),
                     ("pc-mockups", "pc19.nav.mockups"), ("pc-flat", "pc19.nav.flat"),
                     ("pc-months", "pc19.nav.months")]:
        A(f'        <button class="pc-subnav__link" type="button" data-pc-scroll="{sid}"'
          f' data-i18n="{key}">{e(zh(key))}</button>')
    A(f'        <a class="pc-subnav__back" href="__WORKS__" data-i18n="pc19.nav.back">{e(zh("pc19.nav.back"))}</a>')
    A("      </div>")
    A("    </nav>")

    # ---- Hero ----
    A('    <header class="pc-hero">')
    A('      <div class="container pc-hero__grid">')
    A("        <div>")
    A(f'          <span class="eyebrow" data-i18n="pc19.hero.kicker">{e(zh("pc19.hero.kicker"))}</span>')
    A(f'          <h1 class="pc-hero__title" data-i18n="pc19.hero.title">{e(zh("pc19.hero.title"))}</h1>')
    A(f'          <p class="pc-hero__sub" data-i18n="pc19.hero.sub">{e(zh("pc19.hero.sub"))}</p>')
    A(f'          <p class="pc-hero__desc" data-i18n="pc19.hero.desc">{e(zh("pc19.hero.desc"))}</p>')
    A('          <div class="pc-stats">')
    for n, key in [("28", "pc19.stat.pages"), ("12", "pc19.stat.months"),
                   ("3", "pc19.stat.sheets"), ("1", "pc19.stat.mascot")]:
        A(f'            <div class="pc-stat"><b>{n}</b>'
          f'<span data-i18n="{key}">{e(zh(key))}</span></div>')
    A("          </div>")
    A("        </div>")
    A('        <figure class="pc-hero__figure">')
    A(f'          <img src="{IMG}/mockup-hero.jpg" alt="{e(zh("pc19.hero.figcap"))}"'
      f' data-i18n-alt="pc19.hero.figcap">')
    A(f'          <figcaption data-i18n="pc19.hero.figcap">{e(zh("pc19.hero.figcap"))}</figcaption>')
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
    A(head2("01", "pc19.sec.overview"))
    A('        <div class="pc-overview">')
    A('          <dl class="pc-info">')
    for key in ["client", "type", "year", "pages", "extra"]:
        A('            <div class="pc-info__row">')
        A(txt("dt", f"pc19.ov.{key}.k", None, ""))
        A(txt("dd", f"pc19.ov.{key}.v", None, ""))
        A("            </div>")
    A("          </dl>")
    A('          <div class="pc-overview__copy">')
    A(txt("p", "pc19.ov.p1", None, "", indent="            "))
    A(txt("p", "pc19.ov.p2", None, "", indent="            "))
    A('            <ul class="pc-points">')
    for i in range(1, 5):
        A(f'              <li data-i18n="pc19.ov.point{i}">{e(zh(f"pc19.ov.point{i}"))}</li>')
    A("            </ul>")
    A("          </div>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 02 设计亮点 ----
    A('    <section class="pc-section" id="pc-features">')
    A('      <div class="container">')
    A(head2("02", "pc19.sec.features"))
    A('        <div class="pc-features">')
    for i in range(1, 5):
        A('          <article class="pc-feature">')
        A(f'            <span class="pc-feature__no" data-i18n="pc19.ft{i}.no">{e(zh(f"pc19.ft{i}.no"))}</span>')
        A(f'            <h3 data-i18n="pc19.ft{i}.t">{e(zh(f"pc19.ft{i}.t"))}</h3>')
        A(f'            <p data-i18n="pc19.ft{i}.p">{e(zh(f"pc19.ft{i}.p"))}</p>')
        A("          </article>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 03 样机 ----
    A('    <section class="pc-section" id="pc-mockups">')
    A('      <div class="container">')
    A(head2("03", "pc19.sec.mockups"))
    A('        <div class="pc-mockups">')
    for img, key in [("mockup-spread.jpg", "pc19.mk1.cap"), ("mockup-hero.jpg", "pc19.mk2.cap")]:
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
    A(head2("04", "pc19.sec.flat"))
    A('        <div class="pc-flat" data-pc-plates>')
    # 每组的 (分组键, [(图卡键后缀, 文件名)])——文件名与 assets 里的语义命名一一对应
    groups = [
        ("pc19.fg1", [("cover", "cover"), ("back", "backcover"),
                    ("plan", "plan"), ("summary", "summary")]),
        ("pc19.fg2", [(f"ill{i}", f"ill-{i:02d}") for i in range(1, 13)]),
        ("pc19.fg3", [(f"cal{i}", f"cal-{i:02d}") for i in range(1, 13)]),
    ]
    for gkey, items in groups:
        A('          <div class="pc-flat__group">')
        A(f'            <div class="pc-flat__sub"><h3 data-i18n="{gkey}.t">{e(zh(gkey + ".t"))}</h3>'
          f'<span data-i18n="{gkey}.n">{e(zh(gkey + ".n"))}</span></div>')
        A('            <div class="pc-grid">')
        for key_slug, fname in items:
            A(plate_card(f"{IMG}/{fname}.jpg", f"pc19.pl.{key_slug}.t", f"pc19.pl.{key_slug}.s"))
        A("            </div>")
        A("          </div>")
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 05 逐月作品 ----
    A('    <section class="pc-section" id="pc-months">')
    A('      <div class="container">')
    A(head2("05", "pc19.sec.months"))
    for i in range(1, 13):
        A('        <div class="pc-month">')
        A('          <div class="pc-month__head">')
        A(f'            <span class="pc-month__no">{i:02d}</span>')
        A(f'            <h3 class="pc-month__name" data-i18n="pc19.m{i}.name">{e(zh(f"pc19.m{i}.name"))}</h3>')
        A(f'            <div class="pc-month__en" data-i18n="pc19.m{i}.en">{e(zh(f"pc19.m{i}.en"))}</div>')
        A(f'            <p class="pc-month__desc" data-i18n="pc19.m{i}.desc">{e(zh(f"pc19.m{i}.desc"))}</p>')
        A("          </div>")
        A('          <div class="pc-month__pages">')
        A(plate_card(f"{IMG}/ill-{i:02d}.jpg", f"pc19.m{i}.ill.t", f"pc19.m{i}.ill.s"))
        A(plate_card(f"{IMG}/cal-{i:02d}.jpg", f"pc19.m{i}.cal.t", f"pc19.m{i}.cal.s"))
        A("          </div>")
        A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 06 封底 · 尾声 ----
    A('    <section class="pc-section" id="pc-closing">')
    A('      <div class="container">')
    A(head2("06", "pc19.sec.closing"))
    A('        <div class="pc-closing">')
    A(plate_card(f"{IMG}/backcover.jpg", "pc19.cl.back.t", "pc19.cl.back.s"))
    A(plate_card(f"{IMG}/summary.jpg", "pc19.cl.sum.t", "pc19.cl.sum.s"))
    A("        </div>")
    A("      </div>")
    A("    </section>")

    # ---- 上下篇导航 + 页脚说明 ----
    A('    <div class="container">')
    A('      <nav class="work-nav" data-pc-worknav>')
    A('        <a data-pc-prev href="__WORKS__">←</a>')
    A(f'        <a href="__WORKS__" data-i18n="pc19.nav.back">{e(zh("pc19.nav.back"))}</a>')
    A('        <a data-pc-next href="__WORKS__">→</a>')
    A("      </nav>")
    A('      <div class="pc-outer">')
    A(f'        <p data-i18n="pc19.footer.note">{e(zh("pc19.footer.note"))}</p>')
    A(f'        <button class="pc-backtop" type="button" data-pc-backtop data-i18n="pc19.backtop">{e(zh("pc19.backtop"))}</button>')
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
  <meta name="description" content="{e(zh("pc19.meta.desc"))}" data-i18n-content="pc19.meta.desc">
  <title data-i18n="pc19.meta.title">{e(zh("pc19.meta.title"))}</title>
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
