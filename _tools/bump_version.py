#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一递增站点资源版本号，绕过 CDN 对同名文件的缓存。

用法：
    python3 _tools/bump_version.py v20260913      # 指定新版本号
    python3 _tools/bump_version.py --today        # 用 vYYYYMMDD（默认）

会替换三处：
  1. assets/js/main.js 里的 `const ASSET_V = '...'`
  2. 所有 *.html 里的 `assets/...?v…` 与 `href="xxx.html?v…"`
  3. assets/js/main.js 里动态链接后缀 `&v…`
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else '--today'
    new = date.today().strftime('v%Y%m%d') if arg == '--today' else arg
    assert re.fullmatch(r'v\d{8}', new), '版本号格式应为 vYYYYMMDD，例如 v20260913'

    main_js = ROOT / 'assets/js/main.js'
    s = main_js.read_text(encoding='utf-8')
    m = re.search(r"const ASSET_V = '(v\d{8})'", s)
    assert m, 'main.js 中找不到 ASSET_V'
    old = m.group(1)
    if old == new:
        print(f'版本号已是 {new}，未做改动')
        return

    total = 0
    for p in [main_js, *sorted(ROOT.glob('*.html'))]:
        t = p.read_text(encoding='utf-8')
        t2 = t.replace(old, new)
        if t2 != t:
            p.write_text(t2, encoding='utf-8')
            n = t.count(old)
            total += n
            print(f'{p.relative_to(ROOT)}  替换 {n} 处')

    print(f'完成：{old} → {new}，共 {total} 处。接着跑 _tools/verify.py，再部署。')


if __name__ == '__main__':
    main()
