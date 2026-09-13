#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「平原商场 · 2025 乙巳蛇年台历设计」作品专题页（三语）。

文案唯一真源在此（K 函数），由 pingyuan_common.build 同时产出：
  (a) assets/js/i18n.js 里 zh/es/en 三个语言块的 pc25.* 键（按标记幂等插入）
  b) work-pingyuan2025-calendar.html（静态兜底 = 中文值，零漂移）

用法：python3 _tools/gen_pingyuan2025_page.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pingyuan_common import make_registrar, build

K, TRI, KEYS = make_registrar()
prefix = "pc25"


def P(key, zh, es, en):
    K(key, zh, es, en)
    return zh


# ---- 页面元信息 ----
P("pc25.meta.title", "平原商场 · 2025 乙巳蛇年台历设计 — JUN",
  "Pingyuan Mall · Calendario anual 2025 — JUN",
  "Pingyuan Mall · 2025 Annual Calendar — JUN")
P("pc25.meta.desc",
  "平原商场 2025 乙巳蛇年台历设计：敦煌飞天蛇身女封面，金蛇送福与蛇行大运双扉页，古风国潮纸纹风格，平平化身平小宝、平小履、平小酷等角色逛遍商场。平面设计作品，周骏（JUN）设计。",
  "Calendario anual 2025 del centro comercial Pingyuan: portada de hada serpiente estilo Dunhuang, dobles aperturas «Serpiente dorada» y «Buena suerte serpenteante», estética guochao en papel de arroz con Pingping como Pingxiaobao y otros personajes. Diseño gráfico de JUN (Zhou Jun).",
  "The 2025 annual calendar for Pingyuan Mall: a Dunhuang-style flying snake-lady cover, \"Golden Snake\" and \"Slithering Luck\" dual opening pages, guochao rice-paper styling with Pingping as Pingxiaobao and other characters. Graphic design by JUN (Zhou Jun).")

# ---- 页内子导航 ----
P("pc25.nav.overview", "项目概览", "Resumen", "Overview")
P("pc25.nav.features", "设计亮点", "Destacados", "Highlights")
P("pc25.nav.mockups", "样机展示", "Maquetas", "Mockups")
P("pc25.nav.flat", "平铺图", "Láminas", "Flat layout")
P("pc25.nav.months", "逐月作品", "Mes a mes", "Month by month")
P("pc25.nav.back", "返回作品集", "Volver a proyectos", "Back to works")

# ---- Hero ----
P("pc25.hero.kicker", "DESIGN PORTFOLIO · 2025", "DESIGN PORTFOLIO · 2025", "DESIGN PORTFOLIO · 2025")
P("pc25.hero.title", "平原商场", "Pingyuan Mall", "Pingyuan Mall")
P("pc25.hero.sub", "2025 乙巳蛇年台历设计",
  "Calendario anual 2025 · Año de la Serpiente",
  "2025 Annual Calendar · Year of the Snake")
P("pc25.hero.desc",
  "以苹果吉祥物「平平」为主角的年度台历：蛇年封面敦煌飞天蛇身女、金蛇送福与蛇行大运双扉页、12 个月古风国潮楼层主题插画，平平化身平小宝、平小履、平小酷等角色逛遍商场。",
  "Un calendario anual protagonizado por la manzana «Pingping»: portada de hada serpiente estilo Dunhuang, dobles aperturas de la serpiente dorada y la suerte serpenteante, y 12 ilustraciones guochao de plantas con Pingping como Pingxiaobao, Pingxiaolü, Pingxiaoku y más personajes.",
  "An annual calendar led by the apple mascot Pingping: a Dunhuang flying snake-lady cover, \"Golden Snake\" and \"Slithering Luck\" dual opening pages, and 12 guochao floor-themed illustrations with Pingping as Pingxiaobao, Pingxiaolü, Pingxiaoku and more.")
P("pc25.hero.figcap", "封面样机 · 桌面展示",
  "Maqueta de cubierta · Escritorio", "Cover mockup · Desktop")
P("pc25.stat.pages", "个版面", "láminas", "plates")
P("pc25.stat.months", "个主题月", "meses temáticos", "themed months")
P("pc25.stat.sheets", "个特别扉页", "págs. de apertura", "opening pages")
P("pc25.stat.roles", "个平平角色", "personajes Pingping", "Pingping characters")

# ---- 六个区块标题 ----
P("pc25.sec.overview", "项目概览", "Resumen del proyecto", "Project overview")
P("pc25.sec.overview.tag", "PROJECT OVERVIEW", "PROJECT OVERVIEW", "PROJECT OVERVIEW")
P("pc25.sec.features", "设计亮点", "Destacados del diseño", "Design highlights")
P("pc25.sec.features.tag", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS", "DESIGN HIGHLIGHTS")
P("pc25.sec.mockups", "样机展示", "Maquetas", "Mockups")
P("pc25.sec.mockups.tag", "MOCKUPS", "MOCKUPS", "MOCKUPS")
P("pc25.sec.flat", "平铺图展示", "Láminas planas", "Flat layout")
P("pc25.sec.flat.tag", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES", "FLAT LAYOUT · 28 PAGES")
P("pc25.sec.months", "逐月作品", "Mes a mes", "Month by month")
P("pc25.sec.months.tag", "MONTH BY MONTH", "MONTH BY MONTH", "MONTH BY MONTH")
P("pc25.sec.closing", "封底 · 尾声", "Contracubierta y cierre", "Back cover & closing")
P("pc25.sec.closing.tag", "BACK COVER & CLOSING", "BACK COVER & CLOSING", "BACK COVER & CLOSING")

# ---- 01 项目概览 ----
P("pc25.ov.client.k", "客户", "Cliente", "Client")
P("pc25.ov.client.v", "平原商场 Pingyuan Mall", "Centro comercial Pingyuan", "Pingyuan Mall")
P("pc25.ov.type.k", "项目类型", "Tipo", "Type")
P("pc25.ov.type.v", "年度台历 · 平面设计", "Calendario anual · Diseño gráfico", "Annual calendar · Graphic design")
P("pc25.ov.year.k", "设计年份", "Año", "Year")
P("pc25.ov.year.v", "2025 · 乙巳蛇年", "2025 · Año de la Serpiente", "2025 · Year of the Snake")
P("pc25.ov.pages.k", "页数", "Páginas", "Pages")
P("pc25.ov.pages.v", "28 个版面", "28 láminas", "28 plates")
P("pc25.ov.mascot.k", "吉祥物", "Mascota", "Mascot")
P("pc25.ov.mascot.v", "平平（苹果延伸形象）", "Pingping (de una manzana)", "Pingping (apple-derived)")
P("pc25.ov.p1",
  "这是为**平原商场**打造的 2025 年度台历。封面以乙巳蛇年敦煌飞天风格开场，金色背景上蛇身女子翩翩起舞，红绸绿带飞扬，火焰宝珠与祥云环绕，「2025」大字醒目，东方美学浓郁。",
  "Es el calendario anual 2025 creado para **Pingyuan Mall**. La cubierta abre al estilo feitian de Dunhuang del Año de la Serpiente: sobre fondo dorado, una mujer de cuerpo serpiente danza con cintas rojas y verdes al viento, rodeada de perlas de fuego y nubes auspiciosas, con el gran «2025» bien visible y una fuerte estética oriental.",
  "This is the 2025 annual calendar made for **Pingyuan Mall**. The cover opens in Dunhuang feitian style for the Year of the Snake — on a golden ground a snake-bodied lady dances with red and green ribbons streaming, ringed by flaming pearls and auspicious clouds beneath a bold \"2025\", steeped in Eastern aesthetics.")
P("pc25.ov.p2",
  "2025 年全面升级为**古风国潮纸纹风格**：米色宣纸纹理背景，顶部彩色圆角页眉书写月份大写中文与英文，苹果吉祥物「平平」化身多个古风角色——平小宝、平小履、平小酷、平小靓、平小乐、平小羽、平小美——每月对应一个商场楼层或业态。扉页设置**「金蛇送福」**与**「蛇行大运」**双页：金蛇送福页平平家族三人骑金蛇翱翔，蛇行大运页平平躺在摇椅上扇蒲扇享受生活。从一楼闪耀你的美到二楼鞋履，从魅力男装到四楼女装，从建店 68 周年到新大楼开业 25 周年，把商场的业态地图和品牌故事用古风画卷讲了一整年。",
  "En 2025 todo se renueva al **estilo guochao sobre papel de arroz**: fondo beige con textura de papel Xuan, cabeceras redondeadas de colores con el mes en chino clásico e inglés, y la manzana «Pingping» convertida en personajes de aire antiguo —Pingxiaobao, Pingxiaolü, Pingxiaoku, Pingxialiàng, Pingxiaole, Pingxiaoyu, Pingxiaomei— cada mes en una planta o negocio. Las aperturas son **«Serpiente dorada trae fortuna»** y **«Suerte serpenteante»**: en la primera tres miembros de la familia Pingping cabalgan la serpiente dorada; en la segunda Pingping descansa en una mecedora con abanico. Desde la planta baja que «hace brillar tu belleza» hasta los zapatos del segundo piso, de la moda masculina a la femenina del cuarto, del 68º aniversario al 25º del nuevo edificio: un pergamino antiguo que narra el mapa comercial del centro durante todo el año.",
  "2025 upgrades everything to a **guochao rice-paper style**: a beige Xuan-paper textured ground, colourful rounded headers with each month in classical Chinese and English, and the apple mascot Pingping becoming ancient-style characters — Pingxiaobao, Pingxiaolü, Pingxiaoku, Pingxialiang, Pingxiaole, Pingxiaoyu, Pingxiaomei — one per floor or business. The opening pages are **\"Golden Snake Brings Fortune\"** and **\"Slithering Luck\"**: three of Pingping's family ride the golden snake through the clouds, while Pingping lounges in a rocking chair fanning herself. From the ground floor that \"makes your beauty shine\" to 2F shoes, from charming menswear to 4F womenswear, from the 68th anniversary to the new building's 25th — an antique scroll telling the mall's story all year long.")
P("pc25.ov.point1", "古风国潮纸纹风格全新升级", "Renovación total: guochao sobre papel de arroz", "A full guochao rice-paper upgrade")
P("pc25.ov.point2", "平平化身 7+ 古风角色名", "Pingping con más de 7 nombres de personaje", "Pingping as 7+ named characters")
P("pc25.ov.point3", "金蛇送福 + 蛇行大运双扉页", "Dobles aperturas: serpiente dorada y suerte", "Golden Snake + Slithering Luck openings")
P("pc25.ov.point4", "七月建店68周年 · 十月新大楼25周年", "Julio: 68º aniversario · Octubre: 25º del nuevo edificio", "July: 68th founding · October: new building's 25th")

# ---- 02 设计亮点 ----
FEATURES = [
    ("01 — 蛇年封面", "01 — Cubierta Año de la Serpiente", "01 — Year-of-the-Snake cover",
     "敦煌飞天 × 蛇身神女", "Feitian de Dunhuang × Dama serpiente", "Dunhuang feitian × Snake lady",
     "2025 蛇年封面采用敦煌飞天风格，金色背景上蛇身女子翩翩起舞，红绸绿带飞扬，火焰宝珠与祥云环绕，「2025」大字醒目，东方美学与新年喜庆完美融合，视觉冲击力强。",
     "La cubierta de 2025 adopta el estilo feitian de Dunhuang: sobre fondo dorado, una mujer de cuerpo serpiente danza con cintas rojas y verdes al viento, rodeada de perlas de fuego y nubes auspiciosas, con el gran «2025» bien visible; estética oriental y fiesta de Año Nuevo fusionadas con gran impacto visual.",
     "The 2025 cover adopts the Dunhuang feitian style: on a golden ground a snake-bodied lady dances with red and green ribbons streaming, ringed by flaming pearls and auspicious clouds beneath a bold \"2025\" — Eastern aesthetics and New Year festivity fused with striking visual impact."),
    ("02 — 古风国潮升级", "02 — Renovación guochao", "02 — Guochao upgrade",
     "纸纹背景 × 角色命名", "Papel de arroz × Nombres de personaje", "Rice-paper texture × Named characters",
     "2025 年全面升级为古风国潮风格：米色宣纸纹理背景，顶部彩色圆角页眉书写壹月至拾贰月大写中文与英文。苹果吉祥物「平平」化身平小宝、平小履、平小酷、平小靓、平小乐、平小羽、平小美等古风角色，每月一个身份。",
     "En 2025 todo se renueva al estilo guochao: fondo beige con textura de papel Xuan y cabeceras redondeadas de colores con los meses del uno al doce en chino clásico e inglés. La manzana «Pingping» se convierte en personajes de aire antiguo —Pingxiaobao, Pingxiaolü, Pingxiaoku, Pingxialiàng, Pingxiaole, Pingxiaoyu, Pingxiaomei— con una identidad por mes.",
     "2025 upgrades everything to guochao style: a beige Xuan-paper textured ground and colourful rounded headers with months one to twelve in classical Chinese and English. The apple mascot Pingping becomes ancient-style characters — Pingxiaobao, Pingxiaolü, Pingxiaoku, Pingxialiang, Pingxiaole, Pingxiaoyu, Pingxiaomei — one identity per month."),
    ("03 — 双特别扉页", "03 — Dobles aperturas", "03 — Two special opening pages",
     "金蛇送福 × 蛇行大运", "Serpiente dorada × Suerte serpenteante", "Golden Snake × Slithering Luck",
     "台历开篇设置两个特别扉页：金蛇送福页平平家族三人（古装女子、戴P帽男孩、古装弓箭手）骑金蛇翱翔，祥云青山；蛇行大运页平平躺在摇椅上扇蒲扇，洗衣机、购物袋礼物环绕，阳台风景惬意。",
     "El calendario abre con dos páginas especiales: en «Serpiente dorada trae fortuna» tres miembros de la familia Pingping (dama de vestimenta antigua, niño con gorra P y arquero) cabalgan la serpiente dorada entre nubes y montañas; en «Suerte serpenteante» Pingping descansa en una mecedora con abanico de paja, rodeada de lavadora y bolsas de regalo, ante un balcón apacible.",
     "The calendar opens with two special pages: on \"Golden Snake Brings Fortune\" three of Pingping's family (a lady in antique dress, a boy in a P cap and an archer) ride the golden snake through clouds and mountains; on \"Slithering Luck\" Pingping lounges in a rocking chair with a straw fan, ringed by a washing machine and gift bags before a cozy balcony view."),
    ("04 — 功能型日历页", "04 — Página funcional", "04 — Functional calendar page",
     "左日历右插画 + 节气节日", "Calendario e ilustración + festividades", "Calendar & illustration + festivals",
     "2025 日历页采用左侧日历格、右侧吉祥物插画的版式，标注公历、农历、节气与传统节日（含除夕、春节、腊八节等），右侧插画延续当月古风主题，顶部小蛇图标与 P logo，底部「咱老百姓的商场」印章。",
     "La página de calendario de 2025 combina la rejilla del calendario a la izquierda con la ilustración de la mascota a la derecha, anotando fechas gregorianas y lunares, términos solares y festividades (Nochevieja, Año Nuevo chino, Laba…); la ilustración continúa el tema guochao del mes, con icono de serpiente y logo P en la cabecera y el sello «el centro del pueblo» al pie.",
     "The 2025 calendar page pairs the calendar grid on the left with the mascot illustration on the right, marking solar and lunar dates, solar terms and festivals (CNY Eve, Spring Festival, Laba and more); the illustration carries the month's guochao theme, with a snake icon and P logo in the header and the \"people's mall\" seal at the foot."),
]
for i, (no_zh, no_es, no_en, t_zh, t_es, t_en, p_zh, p_es, p_en) in enumerate(FEATURES, 1):
    P(f"pc25.ft{i}.no", no_zh, no_es, no_en)
    P(f"pc25.ft{i}.t", t_zh, t_es, t_en)
    P(f"pc25.ft{i}.p", p_zh, p_es, p_en)

# ---- 03 样机 ----
P("pc25.mk1.cap", "内页展示 · 一月日历正面",
  "Página interior · Calendario de enero", "Inner page · January calendar")
P("pc25.mk2.cap", "立式桌面 · 封面主视觉",
  "En pie sobre la mesa · Portada", "Standing on a desk · Cover key visual")

# ---- 04 平铺图分组标题 ----
P("pc25.fg1.t", "封面 · 特别扉页 · 封底", "Cubierta, aperturas y contracubierta", "Cover · openings · back cover")
P("pc25.fg1.n", "4 PAGES", "4 LÁMINAS", "4 PLATES")
P("pc25.fg2.t", "12 个月古风国潮插画页", "12 ilustraciones guochao", "12 guochao illustration pages")
P("pc25.fg2.n", "ILLUSTRATION PAGES", "ILUSTRACIONES", "ILLUSTRATIONS")
P("pc25.fg3.t", "12 个月功能日历页", "12 páginas de calendario funcional", "12 functional calendar pages")
P("pc25.fg3.n", "CALENDAR PAGES", "CALENDARIO", "CALENDAR PAGES")

# ---- 平铺图：封面组 ----
PLATES_HEAD = [
    ("cover", "封面", "Cubierta", "Cover",
     "2025 蛇年主视觉", "Visual Año de la Serpiente 2025", "2025 Snake-year key visual"),
    ("goldsending", "扉页 · 金蛇送福", "Apertura · Serpiente dorada", "Opening · Golden Snake",
     "平平骑金蛇", "Familia Pingping cabalgando", "Riding the golden snake"),
    ("snakeluck", "扉页 · 蛇行大运", "Apertura · Suerte serpenteante", "Opening · Slithering Luck",
     "平平摇椅蒲扇", "Pingping en mecedora", "Pingping in a rocking chair"),
    ("back", "封底", "Contracubierta", "Back cover",
     "咱老百姓的商场", "El centro del pueblo", "The people's mall"),
]
for slug, t_zh, t_es, t_en, s_zh, s_es, s_en in PLATES_HEAD:
    P(f"pc25.pl.{slug}.t", t_zh, t_es, t_en)
    P(f"pc25.pl.{slug}.s", s_zh, s_es, s_en)

# ---- 12 个月 ----
MONTH_CN = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
MONTH_EN = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]

THEME_ZH = ["财神平平 · 财源滚滚", "平小宝 · 一楼闪耀你的美", "平小履 · 二楼鞋履", "平小酷 · 魅力男装", "平小靓 · 四楼女装",
            "平小乐 · 运动童装", "建店68周年", "八方电器 · 天天低价", "时尚男装 · 潇洒男裤", "新大楼25周年",
            "平小羽 · 7楼羽绒服", "平小美 · 五楼女装"]
THEME_ES = ["Pingping财神 · riqueza sin fin", "Pingxiaobao · planta baja", "Pingxiaolü · zapatos 2F", "Pingxiaoku · moda masculina", "Pingxialiang · moda femenina 4F",
            "Pingxiaole · deporte infantil", "68º aniversario", "Electrodomésticos Bafang", "Moda masculina 3F", "25º nuevo edificio",
            "Pingxiaoyu · abrigos 7F", "Pingxiaomei · moda femenina 5F"]
THEME_EN = ["Fortune Pingping · endless wealth", "Pingxiaobao · ground floor", "Pingxiaolü · 2F shoes", "Pingxiaoku · charming menswear", "Pingxialiang · 4F womenswear",
            "Pingxiaole · kids' sportswear", "68th anniversary", "Bafang appliances", "3F menswear", "New building's 25th",
            "Pingxiaoyu · 7F down jackets", "Pingxiaomei · 5F womenswear"]

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
    "蛇年开场，财神平平手捧元宝，绿色小蛇盘绕身旁，「财源滚滚」横幅高悬，铜钱金元宝散落，红色页眉喜气洋洋，米色纸纹背景古意盎然。",
    "「平小宝」登场，古装女子怀抱中阮（阮上写「壹楼」），珍珠蝴蝶环绕，「肆意精致 自带光芒 一楼闪耀你的美」，粉色页眉浪漫温柔。",
    "「平小履」登场，古装书生平平撑伞持书，画卷展示各式鞋履，松树苍劲，「二楼鞋履 让您自信走好每一步」，薄荷绿页眉春日清新。",
    "「平小酷」登场，古装武士平平蹴鞠、射箭样样精通，「叁楼」旗帜飘扬，「魅力男装 男人的衣橱 懂生活 爱自由」，青绿色页眉英气勃发。",
    "「平小靓」登场，古装女子群像在桃花枝下争奇斗艳，「时尚不止一面 美丽由您展现 四楼女装欢迎您」，暖黄色页眉温婉动人。",
    "「平小乐」登场，古装父子放风筝、拨浪鼓、虎头帽，「陆楼」风筝高飞，「童年成长的每一步 都值得被精心呵护」，天蓝色页眉童趣盎然。",
    "平原商场建店 68 周年庆，古装平平们在商场牌楼前举杯庆祝，金元宝、灯笼、鞭炮、烟花齐飞，紫色页眉庆典隆重。",
    "「买电器 到八方 天天都低价 省钱到八方」，电视里斗笠平平耍双环威风凛凛，两侧古装女子捧花，冰箱洗衣机环绕，米色页眉夏日清凉。",
    "「时尚男装 潇洒男裤 温暖毛衫 让您畅享美好生活」，古装平平们踩剪刀、驾仙鹤、腾云驾雾，「叁楼」字样醒目，橄榄绿页眉仙风道骨。",
    "新大楼开业 25 周年，舞龙、敲鼓、灯笼、烟花齐上阵，平平们穿古装敲锣打鼓，大鼓上写「新大楼开业25周年」，宝蓝色页眉喜庆隆重。",
    "「平小羽」登场，古装女子抱着大大的羽绒服，屋顶上剑客平平挥剑挑梅花，雪人穿羽绒服戴桶帽，「天冷了 买羽绒服就到平原商场七楼」，红色页眉温暖治愈。",
    "「平小美」登场，古装女子在圆形试衣镜前试穿新衣，同伴帮忙挑选裤子和衣服，「伍楼」布料垂落，「五楼女装 简约生活 自信出彩」，暖橙色页眉年末温馨。",
]
DESC_ES = [
    "Arranca el Año de la Serpiente: Pingping de dioses de la fortuna sostiene lingotes entre monedas y oro esparcido, con una serpiente verde enroscada a su lado; la pancarta «riqueza sin fin» cuelga en alto sobre un fondo de papel de arroz, en rojo festivo.",
    "Llega «Pingxiaobao»: una dama de vestimenta antigua abraza un ruan (con «planta baja» escrito en él) entre perlas y mariposas; «desinhibida y refinada, luz propia: la planta baja hace brillar tu belleza», en cabecera rosa romántica.",
    "Llega «Pingxiaolü»: un erudito antiguo con sombrilla y libro despliega un pergamino de calzado entre pinos; «zapatos del segundo piso, que camines con confianza cada paso», en cabecera menta primaveral.",
    "Llega «Pingxiaoku»: un guerrero antiguo domina el cuju y el tiro con arzo bajo banderas del «tercer piso»; «moda masculina con encanto, el armario del hombre: entiende la vida, ama la libertad», en cabecera verde esmeralda.",
    "Llega «Pingxialiang»: un grupo de damas antiguas compite en belleza bajo ramas de melocotonero; «la moda no tiene un solo rostro, la belleza la muestras tú: bienvenidas a la moda femenina del 4F», en cabecera amarillo cálido.",
    "Llega «Pingxiaole»: padre e hijo de aire antiguo vuelan cometas con matracas y gorros de tigre, cometas altísimos en el «sexto piso»; «cada paso del crecimiento infantil merece cuidado esmerado», en cabecera azul celeste.",
    "68º aniversario de fundación: Pingpings de vestimenta antigua brindan ante el pórtico del centro entre lingotes, faroles, petardos y fuegos artificiales, en cabecera púrpura ceremonial.",
    "«Compra electrodomésticos en Bafang: precios bajos todos los días»: en la televisión, Pingping con sombrero de paja blandiendo aros dobles imponente, damas con flores a los lados y nevera y lavadora alrededor, en cabecera beige veraniega.",
    "«Moda masculina, pantalones elegantes, suéteres cálidos para disfrutar la buena vida»: Pingpings antiguos pisando tijeras voladoras, montando grullas y cabalgando nubes bajo el rótulo del «tercer piso», en cabecera verde oliva etérea.",
    "25º aniversario del nuevo edificio: danza del dragón, tambores, faroles y fuegos con Pingpings de vestimenta antigua tocando tambores que proclaman «25º aniversario del nuevo edificio», en cabecera azul zafiro festiva.",
    "Llega «Pingxiaoyu»: una dama antigua abraza un gran plumífero mientras un espadachín Pingping corta ciruelos en el tejado y un muñeco de nieve viste plumífero y sombrero de cubo; «hace frío: los abrigos se compran en el 7F de Pingyuan», en cabecera roja cálida.",
    "Llega «Pingxiaomei»: una dama antigua se prueba ropa ante un espejo circular mientras su acompañante elige pantalones y vestidos, telas colgando del «quinto piso»; «moda femenina del 5F: vida sencilla, brillo con confianza», en cabecera naranja acogedora.",
]
DESC_EN = [
    "The Snake year opens: fortune-god Pingping holds ingots amid scattered coins and gold, a green snake coiled at his side, the \"endless wealth\" banner overhead — a festive red header on an antique rice-paper ground.",
    "Meet \"Pingxiaobao\": a lady in antique dress hugs a ruan lute marked \"Ground Floor\", ringed by pearls and butterflies — \"free and refined, a light of your own: the ground floor makes your beauty shine\", on a romantic pink header.",
    "Meet \"Pingxiaolü\": an ancient scholar with umbrella and book unrolls a scroll of footwear among sturdy pines — \"2F shoes, walk every step with confidence\", on a fresh mint-green header.",
    "Meet \"Pingxiaoku\": an ancient warrior masters cuju football and archery beneath fluttering \"3F\" banners — \"charming menswear, a man's wardrobe: knows life, loves freedom\", on a spirited emerald header.",
    "Meet \"Pingxialiang\": antique ladies vie in beauty beneath peach blossoms — \"fashion has more than one face, beauty is yours to show: welcome to 4F womenswear\", on a warm yellow header.",
    "Meet \"Pingxiaole\": an ancient father and son fly kites with rattles and tiger hats, kites soaring high on \"Floor 6\" — \"every step of a child's growth deserves careful care\", on a playful sky-blue header.",
    "The mall's 68th founding anniversary: ancient-dressed Pingpings raise cups before the mall's gate tower amid ingots, lanterns, firecrackers and fireworks, on a ceremonious purple header.",
    "\"Buy appliances at Bafang — low prices every day\": on TV, straw-hat Pingping brandishes double hoops in style, flower-bearing ladies on both sides, fridge and washing machine around, on a cool beige summer header.",
    "\"Fashionable menswear, dashing trousers, warm knits for the good life\": ancient Pingpings ride flying scissors and cranes through the clouds beneath a bold \"3F\", on an ethereal olive-green header.",
    "The new building's 25th anniversary: dragon dance, drums, lanterns and fireworks as ancient-dressed Pingpings beat drums proclaiming \"25th anniversary of the new building\", on a festive sapphire header.",
    "Meet \"Pingxiaoyu\": an antique lady hugs a huge down jacket while a swordsman Pingping trims plum blossoms on the rooftop and a snowman wears a jacket and bucket hat — \"it's cold: buy down jackets on the 7th floor of Pingyuan Mall\", on a warm red header.",
    "Meet \"Pingxiaomei\": an antique lady tries on new clothes before a round mirror as a friend picks trousers and dresses, fabric draping from \"Floor 5\" — \"5F womenswear: simple living, confident shine\", on a cozy orange header.",
]

for i in range(12):
    n = i + 1
    P(f"pc25.pl.ill{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc25.pl.ill{n}.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc25.pl.cal{n}.t", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc25.pl.cal{n}.s", "公历 · 农历 · 节气", "Gregoriano · lunar · términos", "Solar · lunar · terms")
    P(f"pc25.m{n}.name", MONTH_CN[i], MONTH_ES[i], MONTH_EN[i])
    P(f"pc25.m{n}.en", MONTH_EN[i].upper(), MONTH_CN[i], MONTH_CN[i])
    P(f"pc25.m{n}.desc", DESC_ZH[i], DESC_ES[i], DESC_EN[i])
    P(f"pc25.m{n}.ill.t", "插画页", "Ilustración", "Illustration")
    P(f"pc25.m{n}.ill.s", THEME_ZH[i], THEME_ES[i], THEME_EN[i])
    P(f"pc25.m{n}.cal.t", "日历页", "Calendario", "Calendar")
    P(f"pc25.m{n}.cal.s", TERMS_ZH[i], TERMS_ES[i], TERMS_EN[i])

# ---- 06 封底 · 尾声 ----
P("pc25.cl.back.t", "封底", "Contracubierta", "Back cover")
P("pc25.cl.back.s", "咱老百姓的商场", "El centro del pueblo", "The people's mall")
P("pc25.cl.sum.t", "扉页 · 蛇行大运", "Apertura · Suerte serpenteante", "Opening · Slithering Luck")
P("pc25.cl.sum.s", "平平摇椅蒲扇", "Pingping en mecedora", "Pingping in a rocking chair")

# ---- 页脚 ----
P("pc25.footer.note", "平原商场 · 2025 乙巳蛇年台历设计 — 作品集展示",
  "Pingyuan Mall · Calendario anual 2025 — Presentación de proyecto",
  "Pingyuan Mall · 2025 Annual Calendar — Project showcase")
P("pc25.backtop", "返回顶部", "Volver arriba", "Back to top")

VD = {k: (zh, es, en) for k, zh, es, en in TRI}
ORDER = [k for k, _, _, _ in TRI]

config = dict(
    prefix=prefix,
    work_id="pingyuan-calendar-2025",
    out_html="work-pingyuan2025-calendar.html",
    img="assets/works/pingyuan-calendar-2025",
    begin="/* >>> generated: pingyuan-calendar-2025 >>> */",
    end="/* <<< generated: pingyuan-calendar-2025 <<< */",
    nav_back_key="pc25.nav.back",
    overview_rows=["client", "type", "year", "pages", "mascot"],
    features_count=4,
    months_count=12,
    stats=[("28", "pc25.stat.pages"), ("12", "pc25.stat.months"),
           ("2", "pc25.stat.sheets"), ("7+", "pc25.stat.roles")],
    flat_g1=[("cover", "cover"), ("goldsending", "goldsending"), ("snakeluck", "snakeluck"), ("back", "backcover")],
    flat_g2=[(f"ill{i}", f"ill-{i:02d}") for i in range(1, 13)],
    flat_g3=[(f"cal{i}", f"cal-{i:02d}") for i in range(1, 13)],
    closing=[("backcover", "pc25.cl.back.t", "pc25.cl.back.s"),
             ("snakeluck", "pc25.cl.sum.t", "pc25.cl.sum.s")],
)

if __name__ == "__main__":
    n, out = build(config, ORDER, VD)
    print(f"i18n.js  ← {n} 个 pc25.* 键 × 3 语言")
    print(f"页面      ← {out}  ({len(ORDER)} 键)")
