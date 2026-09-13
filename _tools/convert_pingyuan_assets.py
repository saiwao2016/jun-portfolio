#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 2020-2025 台历源图按语义命名 + 统一压到 1600 宽 q82 JPEG。

用法：
  python3 _tools/convert_pingyuan_assets.py 2020
  ...
  python3 _tools/convert_pingyuan_assets.py 2025
"""
import os
import sys
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BASE = "/Users/jamchou/DoubaoWork/chats/2026-09-13/new-chat"
MAXW = 1600
Q = 82

YEAR = sys.argv[1]
if YEAR == "2020":
    SRC = os.path.join(BASE, "pingyuan-calendar-2020-portfolio/assets")
    DST = os.path.join(ROOT, "assets/works/pingyuan-calendar-2020")
    PAGE0 = 0          # 0 基
    COVER_PAGE = 0
    BACK_PAGE = 1
    OPENING = {2: "honours", 3: "culture"}
elif YEAR == "2021":
    SRC = os.path.join(BASE, "pingyuan-calendar-2021-portfolio/assets")
    DST = os.path.join(ROOT, "assets/works/pingyuan-calendar-2021")
    PAGE0 = 1          # 1 基
    COVER_PAGE = 1
    BACK_PAGE = 28
    OPENING = {2: "newspaper", 3: "postcard"}
elif YEAR == "2022":
    SRC = os.path.join(BASE, "pingyuan-calendar-2022-portfolio/assets")
    DST = os.path.join(ROOT, "assets/works/pingyuan-calendar-2022")
    PAGE0 = 1          # 1 基
    COVER_PAGE = 1
    BACK_PAGE = 28
    OPENING = {2: "voucher1", 3: "voucher2"}
elif YEAR == "2023":
    SRC = os.path.join(BASE, "pingyuan-calendar-2023-portfolio/assets")
    DST = os.path.join(ROOT, "assets/works/pingyuan-calendar-2023")
    PAGE0 = 1          # 1 基
    COVER_PAGE = 1
    BACK_PAGE = 28
    OPENING = {2: "bookmark1", 3: "bookmark2"}
elif YEAR == "2024":
    SRC = os.path.join(BASE, "pingyuan-calendar-2024-portfolio/assets")
    DST = os.path.join(ROOT, "assets/works/pingyuan-calendar-2024")
    PAGE0 = 1          # 1 基
    COVER_PAGE = 1
    BACK_PAGE = 28
    OPENING = {2: "timemanage", 3: "family"}
elif YEAR == "2025":
    SRC = os.path.join(BASE, "pingyuan-calendar-2025-portfolio/assets")
    DST = os.path.join(ROOT, "assets/works/pingyuan-calendar-2025")
    PAGE0 = 1          # 1 基
    COVER_PAGE = 1
    BACK_PAGE = 28
    OPENING = {2: "goldsending", 3: "snakeluck"}
else:
    raise SystemExit("year must be 2020-2025")

os.makedirs(DST, exist_ok=True)


def proc(src_rel, dst_name):
    sp = os.path.join(SRC, src_rel)
    dp = os.path.join(DST, dst_name + ".jpg")
    im = Image.open(sp).convert("RGB")
    w, h = im.size
    if w > MAXW:
        nh = round(h * MAXW / w)
        im = im.resize((MAXW, nh), Image.LANCZOS)
    im.save(dp, "JPEG", quality=Q, optimize=True, progressive=True)
    print(f"  {src_rel:24s} -> {dst_name + '.jpg':18s} {w}x{h} -> {im.size[0]}x{im.size[1]}  {os.path.getsize(dp)//1024}KB")


# 封面 / 封底 / 特别扉页
proc(f"pages/{COVER_PAGE}.jpg", "cover")
proc(f"pages/{BACK_PAGE}.jpg", "backcover")
for pg, slug in OPENING.items():
    proc(f"pages/{pg}.jpg", slug)
# 12 插画 + 12 日历
for i in range(1, 13):
    proc(f"pages/{PAGE0 + 4 + 2*(i-1)}.jpg", f"ill-{i:02d}")
    proc(f"pages/{PAGE0 + 5 + 2*(i-1)}.jpg", f"cal-{i:02d}")
# 样机
proc("mockup-01-hero.jpg", "mockup-hero")
proc("mockup-02-spread.jpg", "mockup-spread")

# 完整性核对
expected = {"cover", "backcover"} | set(OPENING.values()) | \
    {f"ill-{i:02d}" for i in range(1, 13)} | {f"cal-{i:02d}" for i in range(1, 13)} | \
    {"mockup-hero", "mockup-spread"}
got = {os.path.splitext(f)[0] for f in os.listdir(DST) if f.endswith(".jpg")}
missing = expected - got
extra = got - expected
print(f"\n期望 {len(expected)} 张，实际 {len(got)} 张")
print("缺失:", sorted(missing) or "无")
print("多余:", sorted(extra) or "无")
assert not missing and not extra, "映射不完整"
print("OK")
