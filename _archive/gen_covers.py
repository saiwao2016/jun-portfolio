"""Generate placeholder SVG covers for works, by category."""
import os
import random

OUT_DIR = "/Users/jamchou/WorkBuddy/2026-09-07-10-36-15/portfolio-site/assets/images"
os.makedirs(OUT_DIR, exist_ok=True)

# 设计色板（与主 CSS 一致）
INK = "#111111"
MUTED = "#6b6b6b"
BG = "#f4f3f0"
BG2 = "#e8e6e1"
ACCENT = "#b08560"
ACCENT_DEEP = "#8a6644"
SURFACE = "#ffffff"

random.seed(42)

def wrap(content: str, bg=BG, w=1200, h=900) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">
  <rect width="{w}" height="{h}" fill="{bg}"/>
  {content}
</svg>'''


def brand(idx: int) -> str:
    """品牌封面：极简 logo mock + 几何符号 + 细线网格"""
    symbols = [
        # 1: 字母 X 极简 logo
        f'''
        <g transform="translate(600 450)" stroke="{INK}" fill="none" stroke-width="3">
          <line x1="-100" y1="-100" x2="100" y2="100"/>
          <line x1="100" y1="-100" x2="-100" y2="100"/>
        </g>
        <g transform="translate(600 700)" fill="{INK}" font-family="Inter, sans-serif" font-size="36" font-weight="500" text-anchor="middle" letter-spacing="6">XUNCHÁ</g>
        <g stroke="{BG2}" stroke-width="1" fill="none">
          <line x1="0" y1="200" x2="1200" y2="200"/>
          <line x1="0" y1="800" x2="1200" y2="800"/>
        </g>
        ''',
        # 2: 极简相机轮廓
        f'''
        <g transform="translate(600 450)" stroke="{INK}" stroke-width="3" fill="none">
          <rect x="-180" y="-110" width="360" height="220" rx="6"/>
          <circle cx="0" cy="0" r="80"/>
          <circle cx="0" cy="0" r="40"/>
          <rect x="120" y="-150" width="60" height="40" rx="3"/>
        </g>
        <g transform="translate(600 700)" fill="{INK}" font-family="Inter, sans-serif" font-size="32" font-weight="500" text-anchor="middle" letter-spacing="8">OBSCURA</g>
        ''',
        # 3: 瓶身轮廓 + 标签
        f'''
        <g transform="translate(600 450)">
          <path d="M -60 -160 L 60 -160 L 60 -120 L 90 -80 L 90 160 L -90 160 L -90 -80 L -60 -120 Z"
                fill="none" stroke="{INK}" stroke-width="3"/>
          <line x1="-70" y1="20" x2="70" y2="20" stroke="{INK}" stroke-width="1"/>
          <text x="0" y="60" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="32" fill="{INK}">CIRCA</text>
          <text x="0" y="90" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" letter-spacing="3" fill="{MUTED}">PARFUM</text>
        </g>
        ''',
    ]
    return wrap(symbols[idx % 3])


def ip(idx: int) -> str:
    """IP 封面：简化角色剪影 + 装饰元素"""
    parts = [
        # 1: 森林蘑菇角色（圆+茎）
        f'''
        <g transform="translate(600 460)">
          <ellipse cx="0" cy="0" rx="180" ry="60" fill="{ACCENT}"/>
          <rect x="-30" y="0" width="60" height="120" rx="30" fill="{INK}"/>
          <circle cx="-60" cy="-20" r="14" fill="{SURFACE}"/>
          <circle cx="60" cy="-20" r="14" fill="{SURFACE}"/>
          <circle cx="-60" cy="-20" r="6" fill="{INK}"/>
          <circle cx="60" cy="-20" r="6" fill="{INK}"/>
        </g>
        <text x="600" y="720" text-anchor="middle" font-family="Inter, sans-serif" font-size="40" letter-spacing="6" fill="{INK}">MOSSY</text>
        ''',
        # 2: 太空猫（圆头+三角耳）
        f'''
        <g transform="translate(600 460)">
          <circle cx="0" cy="20" r="140" fill="{INK}"/>
          <polygon points="-90,-90 -50,-30 -130,-30" fill="{INK}"/>
          <polygon points="90,-90 50,-30 130,-30" fill="{INK}"/>
          <circle cx="-45" cy="20" r="20" fill="{SURFACE}"/>
          <circle cx="45" cy="20" r="20" fill="{SURFACE}"/>
          <circle cx="-45" cy="20" r="8" fill="{ACCENT}"/>
          <circle cx="45" cy="20" r="8" fill="{ACCENT}"/>
        </g>
        <text x="600" y="720" text-anchor="middle" font-family="Inter, sans-serif" font-size="36" letter-spacing="10" fill="{INK}">ORBIT</text>
        ''',
        # 3: 城市夜行角色（人形剪影）
        f'''
        <g transform="translate(600 460)">
          <circle cx="0" cy="-100" r="50" fill="{INK}"/>
          <path d="M -80 -40 Q -90 80 -50 160 L 50 160 Q 90 80 80 -40 Z" fill="{INK}"/>
          <rect x="-12" y="-100" width="24" height="40" fill="{INK}"/>
        </g>
        <g stroke="{ACCENT}" stroke-width="2" fill="none">
          <circle cx="200" cy="200" r="40" opacity="0.6"/>
          <circle cx="1000" cy="180" r="60" opacity="0.4"/>
        </g>
        <text x="600" y="720" text-anchor="middle" font-family="Inter, sans-serif" font-size="34" letter-spacing="8" fill="{INK}">KIRA</text>
        ''',
    ]
    return wrap(parts[idx % 3])


def graphic(idx: int) -> str:
    """平面封面：排版与负空间"""
    parts = [
        # 1: 海报排版
        f'''
        <g transform="translate(120 180)" fill="{INK}" font-family="Inter, sans-serif" font-weight="600">
          <text x="0" y="0" font-size="180" letter-spacing="-8">边界</text>
          <text x="0" y="200" font-size="180" letter-spacing="-8">BORDER</text>
        </g>
        <line x1="120" y1="780" x2="1080" y2="780" stroke="{INK}" stroke-width="2"/>
        <text x="120" y="820" font-family="Inter, sans-serif" font-size="20" letter-spacing="4" fill="{MUTED}">A POSTER SERIES · 2023</text>
        <text x="1080" y="820" text-anchor="end" font-family="Inter, sans-serif" font-size="20" letter-spacing="4" fill="{MUTED}">N° 01</text>
        ''',
        # 2: 画册封面
        f'''
        <g transform="translate(600 450)">
          <rect x="-300" y="-280" width="600" height="560" fill="{SURFACE}" stroke="{INK}" stroke-width="1"/>
          <rect x="-260" y="160" width="520" height="80" fill="{INK}"/>
          <text x="0" y="-100" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="56" fill="{INK}">Issue 12</text>
          <text x="0" y="0" text-anchor="middle" font-family="Inter, sans-serif" font-size="18" letter-spacing="6" fill="{MUTED}">QUIET ROOMS</text>
          <text x="0" y="210" text-anchor="middle" font-family="Inter, sans-serif" font-size="14" letter-spacing="4" fill="{SURFACE}">BOOKSTORE MONTHLY</text>
        </g>
        ''',
    ]
    return wrap(parts[idx % 2])


def ui(idx: int) -> str:
    """UI 封面：手机/屏幕 mockup + UI 元素"""
    parts = [
        # 1: 手机 + 数据
        f'''
        <g transform="translate(600 460)">
          <rect x="-120" y="-220" width="240" height="440" rx="28" fill="{SURFACE}" stroke="{INK}" stroke-width="2"/>
          <rect x="-100" y="-190" width="200" height="380" rx="14" fill="{BG2}"/>
          <circle cx="-100" cy="190" r="3" fill="{INK}"/>
          <rect x="-90" y="-170" width="80" height="6" rx="3" fill="{INK}"/>
          <rect x="-90" y="-150" width="40" height="3" rx="1" fill="{MUTED}"/>
          <circle cx="0" cy="-50" r="50" fill="none" stroke="{ACCENT}" stroke-width="6"/>
          <circle cx="0" cy="-50" r="32" fill="{ACCENT}"/>
          <text x="0" y="-42" text-anchor="middle" font-family="Inter, sans-serif" font-size="20" font-weight="600" fill="{SURFACE}">82</text>
          <rect x="-90" y="20" width="180" height="8" rx="4" fill="{INK}" opacity="0.15"/>
          <rect x="-90" y="20" width="140" height="8" rx="4" fill="{INK}"/>
          <rect x="-90" y="50" width="180" height="8" rx="4" fill="{INK}" opacity="0.15"/>
          <rect x="-90" y="50" width="100" height="8" rx="4" fill="{INK}"/>
          <rect x="-90" y="100" width="180" height="60" rx="8" fill="{INK}"/>
          <text x="0" y="138" text-anchor="middle" font-family="Inter, sans-serif" font-size="14" font-weight="500" fill="{SURFACE}" letter-spacing="2">START</text>
        </g>
        <text x="600" y="760" text-anchor="middle" font-family="Inter, sans-serif" font-size="28" letter-spacing="6" fill="{INK}">PULSE</text>
        ''',
        # 2: 桌面后台
        f'''
        <g transform="translate(80 160)">
          <rect width="1040" height="540" rx="8" fill="{SURFACE}" stroke="{INK}" stroke-width="1"/>
          <rect width="220" height="540" fill="{BG2}"/>
          <rect x="20" y="20" width="180" height="6" rx="3" fill="{INK}"/>
          <rect x="20" y="60" width="120" height="6" rx="3" fill="{MUTED}"/>
          <rect x="20" y="80" width="140" height="6" rx="3" fill="{MUTED}"/>
          <rect x="20" y="100" width="100" height="6" rx="3" fill="{MUTED}"/>
          <rect x="260" y="20" width="760" height="60" rx="4" fill="{BG2}"/>
          <rect x="280" y="40" width="200" height="20" rx="3" fill="{INK}"/>
          <rect x="260" y="100" width="240" height="200" rx="4" fill="{BG2}"/>
          <rect x="520" y="100" width="240" height="200" rx="4" fill="{BG2}"/>
          <rect x="780" y="100" width="240" height="200" rx="4" fill="{BG2}"/>
          <polyline points="280,260 320,240 360,250 400,210 440,230 480,180" stroke="{ACCENT}" stroke-width="3" fill="none"/>
          <polyline points="540,260 580,230 620,240 660,200 700,210 740,170" stroke="{INK}" stroke-width="3" fill="none"/>
        </g>
        <text x="600" y="760" text-anchor="middle" font-family="Inter, sans-serif" font-size="28" letter-spacing="6" fill="{INK}">MERIDIAN</text>
        ''',
        # 3: 网页排版
        f'''
        <g transform="translate(80 200)">
          <rect width="1040" height="500" rx="8" fill="{SURFACE}" stroke="{INK}" stroke-width="1"/>
          <rect x="0" y="0" width="1040" height="40" fill="{INK}"/>
          <text x="40" y="26" font-family="Georgia, serif" font-style="italic" font-size="20" fill="{SURFACE}">A.</text>
          <text x="980" y="26" text-anchor="end" font-family="Inter, sans-serif" font-size="12" letter-spacing="3" fill="{SURFACE}" opacity="0.7">MENU</text>
          <text x="60" y="180" font-family="Georgia, serif" font-style="italic" font-size="120" fill="{INK}">Atelier</text>
          <text x="60" y="280" font-family="Inter, sans-serif" font-size="48" font-weight="300" fill="{INK}" letter-spacing="-1">Creative studio.</text>
          <line x1="60" y1="320" x2="980" y2="320" stroke="{INK}" stroke-width="1"/>
          <text x="60" y="360" font-family="Inter, sans-serif" font-size="14" letter-spacing="2" fill="{MUTED}">INDEPENDENT · MULTI-MEDIUM · 2018—</text>
          <rect x="60" y="400" width="180" height="50" fill="{INK}"/>
          <text x="150" y="432" text-anchor="middle" font-family="Inter, sans-serif" font-size="14" letter-spacing="3" fill="{SURFACE}">VIEW WORKS →</text>
        </g>
        ''',
    ]
    return wrap(parts[idx % 3])


def motion(idx: int) -> str:
    """动态封面：胶片帧条 + 渐变"""
    parts = [
        # 1: 视频帧
        f'''
        <g transform="translate(100 200)">
          <rect width="1000" height="500" fill="{INK}"/>
          <g fill="{SURFACE}">
            <rect x="0" y="0" width="60" height="500"/>
            <rect x="940" y="0" width="60" height="500"/>
          </g>
          <g fill="{SURFACE}" opacity="0.3">
            <rect x="80" y="20" width="20" height="20"/>
            <rect x="80" y="60" width="20" height="20"/>
            <rect x="80" y="100" width="20" height="20"/>
            <rect x="80" y="140" width="20" height="20"/>
            <rect x="80" y="180" width="20" height="20"/>
            <rect x="80" y="220" width="20" height="20"/>
            <rect x="80" y="260" width="20" height="20"/>
            <rect x="80" y="300" width="20" height="20"/>
            <rect x="900" y="20" width="20" height="20"/>
            <rect x="900" y="60" width="20" height="20"/>
            <rect x="900" y="100" width="20" height="20"/>
            <rect x="900" y="140" width="20" height="20"/>
            <rect x="900" y="180" width="20" height="20"/>
            <rect x="900" y="220" width="20" height="20"/>
            <rect x="900" y="260" width="20" height="20"/>
            <rect x="900" y="300" width="20" height="20"/>
          </g>
          <text x="500" y="240" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="80" fill="{SURFACE}">CIRCA</text>
          <text x="500" y="320" text-anchor="middle" font-family="Inter, sans-serif" font-size="18" letter-spacing="6" fill="{SURFACE}" opacity="0.7">BRAND FILM · 60s</text>
        </g>
        ''',
        # 2: MG 动效
        f'''
        <g transform="translate(600 460)">
          <circle r="180" fill="{ACCENT}"/>
          <circle r="140" fill="{ACCENT_DEEP}"/>
          <circle r="100" fill="{INK}"/>
          <circle r="60" fill="{ACCENT}"/>
          <circle r="20" fill="{INK}"/>
        </g>
        <text x="600" y="780" text-anchor="middle" font-family="Inter, sans-serif" font-size="32" letter-spacing="8" fill="{INK}">MAGMA</text>
        ''',
    ]
    return wrap(parts[idx % 2])


def d3(idx: int) -> str:
    """3D 封面：几何体 + 阴影"""
    parts = [
        # 1: 产品盒
        f'''
        <g transform="translate(600 480)">
          <rect x="-200" y="-150" width="400" height="300" rx="20" fill="{SURFACE}"/>
          <rect x="-200" y="-150" width="400" height="60" rx="20" fill="{INK}"/>
          <circle cx="0" cy="60" r="80" fill="none" stroke="{INK}" stroke-width="2"/>
          <circle cx="0" cy="60" r="40" fill="{ACCENT}"/>
          <rect x="-150" y="180" width="300" height="6" rx="3" fill="{MUTED}"/>
          <ellipse cx="0" cy="180" rx="220" ry="20" fill="{BG2}"/>
        </g>
        <text x="600" y="780" text-anchor="middle" font-family="Inter, sans-serif" font-size="28" letter-spacing="6" fill="{INK}">MERIDIAN 3D</text>
        ''',
        # 2: 3D 角色剪影 + 网格
        f'''
        <g stroke="{BG2}" stroke-width="1" fill="none">
          <line x1="0" y1="600" x2="1200" y2="600"/>
          <line x1="600" y1="200" x2="600" y2="600"/>
          <line x1="300" y1="200" x2="300" y2="600"/>
          <line x1="900" y1="200" x2="900" y2="600"/>
          <line x1="0" y1="400" x2="1200" y2="400"/>
        </g>
        <g transform="translate(600 480)">
          <circle cy="-60" r="60" fill="{INK}"/>
          <path d="M -80 0 Q -100 80 -60 160 L 60 160 Q 100 80 80 0 Z" fill="{INK}"/>
          <ellipse cx="0" cy="180" rx="120" ry="14" fill="{INK}" opacity="0.2"/>
        </g>
        ''',
        # 3: 抽象球 + 平面
        f'''
        <g transform="translate(600 460)">
          <circle r="200" fill="{INK}"/>
          <ellipse cx="0" cy="220" rx="220" ry="20" fill="{BG2}"/>
          <rect x="-200" y="220" width="400" height="20" fill="{BG2}"/>
        </g>
        <g stroke="{BG2}" stroke-width="1" fill="none" opacity="0.4">
          <line x1="0" y1="460" x2="1200" y2="460"/>
          <line x1="0" y1="660" x2="1200" y2="660"/>
        </g>
        <text x="600" y="800" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="36" fill="{INK}">TERRA</text>
        ''',
    ]
    return wrap(parts[idx % 3])


def main():
    plan = [
        ("work-brand-1.svg", brand, 0),
        ("work-brand-2.svg", brand, 1),
        ("work-brand-3.svg", brand, 2),
        ("work-ip-1.svg", ip, 0),
        ("work-ip-2.svg", ip, 1),
        ("work-ip-3.svg", ip, 2),
        ("work-graphic-1.svg", graphic, 0),
        ("work-graphic-2.svg", graphic, 1),
        ("work-ui-1.svg", ui, 0),
        ("work-ui-2.svg", ui, 1),
        ("work-ui-3.svg", ui, 2),
        ("work-motion-1.svg", motion, 0),
        ("work-motion-2.svg", motion, 1),
        ("work-3d-1.svg", d3, 0),
        ("work-3d-2.svg", d3, 1),
        ("work-3d-3.svg", d3, 2),
    ]
    for fname, fn, idx in plan:
        path = os.path.join(OUT_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(fn(idx))
        print(f"✓ {fname}")

    # Logo & favicon
    logo_svg = wrap(f'''
        <g transform="translate(600 450)">
          <text text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="320" font-weight="400" fill="{INK}">J</text>
          <line x1="-260" y1="240" x2="260" y2="240" stroke="{ACCENT}" stroke-width="2"/>
        </g>
    ''', bg="#ffffff")
    with open(os.path.join(OUT_DIR, "logo.svg"), "w", encoding="utf-8") as f:
        f.write(logo_svg)
    print("✓ logo.svg")

    # favicon
    favicon = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" fill="{INK}"/>
  <text x="16" y="24" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="24" fill="{SURFACE}">J</text>
</svg>'''
    with open(os.path.join(OUT_DIR, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(favicon)
    print("✓ favicon.svg")


if __name__ == "__main__":
    main()