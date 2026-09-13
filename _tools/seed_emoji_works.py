#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 6 个微信表情包作为独立作品写入 content/works.json（IP 分类）。
素材来源：微信表情商店 6 个作品详情页（艺术家均为「怪物饲养员」）。
运行后需再执行 build_content.js / POST /api/sync 重写 data.js。
"""
import json, io
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
P = ROOT / 'content' / 'works.json'

TYPE = {
    'zh': '原创 IP / 微信表情包上架',
    'es': 'IP original / Stickers para WeChat',
    'en': 'Original IP / WeChat sticker pack',
}
SCOPE = {
    'zh': '角色设定 · 表情设计 · 微信表情商店上架',
    'es': 'Diseño de personaje · Emoticonos · Publicado en la tienda de WeChat',
    'en': 'Character design · Sticker design · Published on the WeChat Sticker Store',
}

PACKS = [
    dict(id='ip-emoji-shiliu', sort=40, n=16,
         title={'zh': '石榴妹萌萌 · 微信表情包',
                'es': 'Shiliu Mei Mengmeng · Stickers para WeChat',
                'en': 'Shiliu Mei Mengmeng · WeChat Sticker Pack'},
         blurb={
             'zh': '微信表情商店上架作品，收录 16 个表情。\n\n'
                   '角色沿用「榴心社工」公益 IP 石榴妹萌萌：头顶石榴帽、身披碎花蓝、胸戴红领巾，'
                   '把石榴、留守儿童与志愿者三重线索收进同一个形象。\n\n'
                   '表情包按聊天里的高频场景展开——早安、晚安、比心、抱抱、害羞、生气、大哭，'
                   '还有一句「厉害了我的萌」。扁平矢量配上红色帽子与蓝色碎花衣的强对比，'
                   '缩到聊天框里也一眼能认出来。',
             'es': 'Colección publicada en la tienda de stickers de WeChat, con 16 emoticonos.\n\n'
                   'El personaje retoma la IP solidaria «Shiliu Mei Mengmeng» del proyecto Liuxin: '
                   'gorro de granada, chaqueta azul de flores y pañuelo rojo, reuniendo en una sola '
                   'figura la granada, los niños del proyecto y los voluntarios.\n\n'
                   'Los emoticonos siguen las situaciones más frecuentes del chat — buenos días, '
                   'buenas noches, corazón, abrazo, vergüenza, enfado o llanto, más un «qué crack eres». '
                   'El vector plano y el fuerte contraste entre el rojo y el azul mantienen la lectura '
                   'incluso en el tamaño mínimo del chat.',
             'en': 'A sticker pack published on the WeChat Sticker Store, with 16 emoticons.\n\n'
                   'The character carries over the charity IP “Shiliu Mei Mengmeng” from the Liuxin '
                   'social-work project — pomegranate hat, floral blue jacket, red neckerchief — '
                   'folding the pomegranate, the left-behind children and the volunteers into one figure.\n\n'
                   'The set follows everyday chat rhythms: good morning, good night, heart, hug, '
                   'shyness, anger and crying, plus a “you’re amazing” stamp. Flat vector shapes and '
                   'the hard red-and-blue contrast keep it legible even at chat-box size.',
         }),
    dict(id='ip-emoji-shishizi', sort=41, n=16,
         title={'zh': '狮狮子 · 微信表情包',
                'es': 'Shi Shi Zi · Stickers para WeChat',
                'en': 'Shi Shi Zi · WeChat Sticker Pack'},
         blurb={
             'zh': '「Youknow design」系列第一号，微信表情商店上架，收录 16 个表情。\n\n'
                   '主角是一头鬃毛蓬松的狮子：棕色鬃毛压住橘色身体，圆耳、短尾、腮红，'
                   '整体走厚实憨态的路子。\n\n'
                   '表情从大笑、指点、哼、喵，到「辛苦啦」和 bye，覆盖日常语气；'
                   '粗描边配低饱和橘棕，让它在表情栏的小尺寸下依然清晰。',
             'es': 'Primer número de la serie «Youknow design», publicado en la tienda de stickers '
                   'de WeChat con 16 emoticonos.\n\n'
                   'El protagonista es un león de melena frondosa: melena marrón sobre cuerpo naranja, '
                   'orejas redondas, cola corta y mejillas sonrosadas, con un aire macizo y bonachón.\n\n'
                   'Las expresiones van de la risa al gesto de señalar, del resoplido al «maullido» y '
                   'del «buen trabajo» al bye, cubriendo el tono diario; el contorno grueso y el naranja '
                   'terroso se leen bien a tamaño pequeño.',
             'en': 'First entry in the “Youknow design” series, published on the WeChat Sticker Store '
                   'with 16 emoticons.\n\n'
                   'The lead is a lion with a heavy mane: brown mane over an orange body, round ears, '
                   'a stub tail and pink cheeks — sturdy and good-natured.\n\n'
                   'Expressions run from a belly laugh and a pointing finger to a huff, a “meow”, a '
                   '“nice work” and a bye; thick outlines and muted orange-brown stay readable at small size.',
         }),
    dict(id='ip-emoji-niuniuzi', sort=42, n=24,
         title={'zh': '牛牛子 · 微信表情包',
                'es': 'Niu Niu Zi · Stickers para WeChat',
                'en': 'Niu Niu Zi · WeChat Sticker Pack'},
         blurb={
             'zh': '「Youknow design」系列第二号，微信表情商店上架，收录 24 个表情。\n\n'
                   '主角是一对牛：棕黄牛与戴粉色蝴蝶结的黑白花牛，两种配色轮换出场，'
                   '把「对 / 好吧 / 收到 / 在吗 / 晚安 / 加油」这类沟通高频词做成了动作。\n\n'
                   '24 个表情的体量让语义覆盖更完整——从比心、献花、闪亮，到无语、喷水、哈哈哈，'
                   '情绪跨度拉得比较开。',
             'es': 'Segundo número de la serie «Youknow design», publicado en la tienda de stickers '
                   'de WeChat con 24 emoticonos.\n\n'
                   'Dos vacas: una parda y otra blanquinegra con lazo rosa, que se alternan para dar '
                   'forma a las palabras más usadas del chat — «vale», «recibido», «¿estás?», '
                   '«buenas noches», «ánimo».\n\n'
                   'Con 24 piezas la cobertura semántica es más amplia: del corazón, las flores y el '
                   'brillo al sin palabras, el chorro de agua o el jajaja.',
             'en': 'Second entry in the “Youknow design” series, published on the WeChat Sticker Store '
                   'with 24 emoticons.\n\n'
                   'Two cows — one tawny, one black-and-white with a pink bow — alternate to carry the '
                   'workhorses of chat: “sure”, “received”, “you there?”, “good night”, “you can do it”.\n\n'
                   'At 24 pieces the semantic range is wider: from hearts, flowers and sparkles to '
                   'speechlessness, a water spout and a laugh-out-loud.',
         }),
    dict(id='ip-emoji-tutuzi', sort=43, n=16,
         title={'zh': '一只兔兔子 · 微信表情包',
                'es': 'Yi Zhi Tu Tu Zi · Stickers para WeChat',
                'en': 'Tu Tu Zi · WeChat Sticker Pack'},
         blurb={
             'zh': '「Youknow design」系列第三号（署名 Xzzz），微信表情商店上架，收录 16 个表情。\n\n'
                   '一只极简线条兔：细黑描边、白色身体，只留黄、蓝、橙三种小衣服，'
                   '画面里大量留白，还有一根贯穿好几格的桌线。\n\n'
                   '内容多是生活切片——冲浪、唱歌、喝咖啡、遛狗、吐彩虹、打坐发光、'
                   '趴在桌上发呆——弱化语言，靠动作和留白说话。',
             'es': 'Tercer número de la serie «Youknow design» (firmado Xzzz), publicado en la tienda '
                   'de stickers de WeChat con 16 emoticonos.\n\n'
                   'Un conejo de línea mínima: contorno negro fino, cuerpo blanco y solo tres colores '
                   'de ropa —amarillo, azul y naranja—, con mucho aire y una línea de mesa que '
                   'atraviesa varias escenas.\n\n'
                   'El contenido son pequeños fragmentos de vida: surf, cantar, café, pasear al perro, '
                   'vomitar un arcoíris, meditar o quedarse mirando la nada sobre la mesa.',
             'en': 'Third entry in the “Youknow design” series (credited Xzzz), published on the WeChat '
                   'Sticker Store with 16 emoticons.\n\n'
                   'A minimum-line rabbit: thin black outline, white body and only three garment '
                   'colours — yellow, blue and orange — with generous empty space and a table line '
                   'running through several scenes.\n\n'
                   'The subjects are small slices of life: surfing, singing, coffee, walking the dog, '
                   'throwing up a rainbow, meditating, or blankly staring across a desk.',
         }),
    dict(id='ip-emoji-pilitu', sort=44, n=16,
         title={'zh': '一只霹雳兔 · 微信表情包',
                'es': 'Yi Zhi Pi Li Tu · Stickers para WeChat',
                'en': 'Pi Li Tu · WeChat Sticker Pack'},
         blurb={
             'zh': '微信表情商店上架作品，收录 16 个表情。\n\n'
                   '一只系红领巾、戴红色贝雷帽的兔子，表情夸张到变形：翻白眼、张望、'
                   '哭到喷水、满脸嫌弃，还有挥手指着屏幕的「退!!!」。\n\n'
                   '用最少的结构画最大的情绪是这个包的核心——线条简单、五官放大，'
                   '追求一眼就能读出来的表情张力。',
             'es': 'Publicado en la tienda de stickers de WeChat con 16 emoticonos.\n\n'
                   'Un conejo con pañuelo rojo y boina a juego, con expresiones llevadas hasta la '
                   'deformación: ojos en blanco, cara de asco, llanto con chorro de agua y un '
                   '«¡¡¡atrás!!!» señalando con el dedo.\n\n'
                   'Sacar la máxima emoción con la mínima estructura es el eje del paquete: línea '
                   'sencilla, rasgos agrandados, lectura inmediata.',
             'en': 'Published on the WeChat Sticker Store with 16 emoticons.\n\n'
                   'A rabbit in a red neckerchief and matching beret, with expressions pushed to the '
                   'point of distortion: rolled eyes, a look of disgust, a crying fit with a water '
                   'spout, and a finger-pointing “back off!!!”.\n\n'
                   'Getting maximum emotion out of minimum structure is the point of the pack: simple '
                   'lines, enlarged features, instantly readable.',
         }),
    dict(id='ip-emoji-huahua', sort=45, n=24,
         title={'zh': '虎阿虎阿 · 微信表情包',
                'es': 'Hu A Hu A · Stickers para WeChat',
                'en': 'Hu A Hu A · WeChat Sticker Pack'},
         blurb={
             'zh': '微信表情商店上架作品，收录 24 个表情。\n\n'
                   '一只圆滚滚的小老虎：橘色皮毛配黑色条纹，脑袋大、身子短，走软萌憨态路线。\n\n'
                   '24 个动作全都围绕「可爱」展开——捧脸、抱尾、趴着睡、啃爪子、害羞、'
                   '打哈欠，还有被吓到掉眼泪；整套保持统一的暖调柔光，摆在一起像一组小剧场。',
             'es': 'Publicado en la tienda de stickers de WeChat con 24 emoticonos.\n\n'
                   'Un tigre rechoncho: pelaje naranja con rayas negras, cabeza grande y cuerpo corto, '
                   'en clave tierna y bonachona.\n\n'
                   'Las 24 acciones giran en torno a la ternura: cara entre las manos, abrazar la cola, '
                   'dormir boca abajo, mordisquearse la garra, timidez, bostezos y sustos hasta el '
                   'llanto, todas bajo la misma luz cálida.',
             'en': 'Published on the WeChat Sticker Store with 24 emoticons.\n\n'
                   'A chubby little tiger: orange coat with black stripes, oversized head, short body '
                   '— soft and good-humoured.\n\n'
                   'The 24 actions all orbit cuteness: face in hands, hugging its tail, sleeping on its '
                   'belly, chewing a paw, shyness, yawns and being startled to tears, held together by '
                   'the same warm light.',
         }),
]


def main():
    doc = json.loads(P.read_text(encoding='utf-8'))
    works = doc['works']
    ids = {w['id'] for w in works}
    added = 0
    for p in PACKS:
        if p['id'] in ids:
            print(f"  · {p['id']} 已存在，跳过")
            continue
        works.append({
            'id': p['id'],
            'category': 'ip',
            'status': 'published',
            'sortOrder': p['sort'],
            'year': '—',
            'mediaType': 'image',
            'cover': f"assets/works/{p['id']}/cover.png",
            'video': '', 'videoPoster': '', 'bgm': '',
            'single': False,
            'gallery': [
                {'type': 'image', 'src': f"assets/works/{p['id']}/{n}.png", 'poster': ''}
                for n in ('01', '02', '03')
            ],
            'title': p['title'],
            'type': TYPE,
            'scope': SCOPE,
            'blurb': p['blurb'],
        })
        added += 1
        print(f"  + {p['id']} sortOrder={p['sort']} ({p['n']} 表情)")
    doc['updatedAt'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.') + \
        f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"
    P.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'新增 {added} 个作品，现在共 {len(works)} 个')


if __name__ == '__main__':
    main()
