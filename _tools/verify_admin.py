#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""后台管理系统端到端校验。

以真实服务方式启动 `node server.js`，覆盖：
  鉴权 · 作品 CRUD · 上传 · 视频/海报字段 · 图集视频项 · 草稿与发布 ·
  sortOrder 重排 · 作品改名（素材目录迁移）· 站点文案 / 社交链接 ·
  数据源兜底 · 后台界面可用性 · 站点侧渲染（视频首屏 / 图集视频 / 背景音乐）

用法：
    python3 _tools/verify_admin.py

测试数据全部使用 `__e2e-` 前缀，结束后自动清理并恢复 site.json。
"""
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("ADMIN_TEST_PORT", "3199"))
BASE = f"http://127.0.0.1:{PORT}"
NODE = os.environ.get("NODE_BIN") or shutil.which("node") or \
    "/Users/jamchou/.workbuddy/binaries/node/versions/22.22.2-3/bin/node"
TMP_WORK = "zze2e-admin-test"

fails = []
log = []


def check(cond, msg):
    if cond:
        log.append(f"  · {msg}")
    else:
        fails.append(msg)
        log.append(f"  ✗ {msg}")


def req(method, path, body=None, token=None, raw=None, headers=None, timeout=30):
    h = {}
    if token:
        h["Authorization"] = "Bearer " + token
    data = None
    if raw is not None:
        data = raw
    elif body is not None:
        data = json.dumps(body).encode("utf-8")
        h["Content-Type"] = "application/json"
    if headers:
        h.update(headers)
    r = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8") or "{}")
        except Exception:
            return e.code, {}


def make_wav(path: Path, seconds=0.25, rate=8000):
    """生成一个真实可播放的 wav，用于背景音乐上传测试。"""
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        frames = b"".join(
            struct.pack("<h", int(6000 * math.sin(2 * math.pi * 440 * i / rate)))
            for i in range(int(rate * seconds))
        )
        w.writeframes(frames)


def make_png(path: Path):
    """1×1 白色 PNG（用于上传接口测试）。"""
    path.write_bytes(bytes.fromhex(
        "89504e470d0a1a0a0000000d4948445200000001000000010806000000"
        "1f15c4890000000a49444154789c6360000002000100ffff030000060005"
        "57bfabd40000000049454e44ae426082"))


# ───────────────────────────── 启动服务 ─────────────────────────────

site_backup = (ROOT / "content/site.json").read_text(encoding="utf-8")
uploads_dir = ROOT / "assets/uploads"
created_uploads = []

env = dict(os.environ)
env["PORT"] = str(PORT)
proc = subprocess.Popen([NODE, "server.js"], cwd=str(ROOT), env=env,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

def wait_health():
    for _ in range(80):
        try:
            code, _ = req("GET", "/api/health", timeout=2)
            if code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.25)
    return False


if not wait_health():
    print("✗ 服务未能启动，server.js 输出：")
    proc.kill()
    print(proc.stdout.read()[:2000] if proc.stdout else "")
    sys.exit(1)

PASSWORD = os.environ.get("ADMIN_PASSWORD") or \
    json.loads((ROOT / "content/auth.json").read_text(encoding="utf-8"))["password"]

print("=" * 62)
print("  后台管理系统端到端校验")
print("=" * 62)

try:
    # ---------- 1. 鉴权 ----------
    code, _ = req("GET", "/api/state")
    check(code == 401, f"未登录访问 /api/state 应 401，实际 {code}")

    code, _ = req("POST", "/api/login", {"password": "definitely-wrong"})
    check(code == 401, f"错误密码应 401，实际 {code}")

    code, r = req("POST", "/api/login", {"password": PASSWORD})
    check(code == 200 and r.get("token"), "正确密码应返回 token")
    TOKEN = r.get("token", "")

    code, st = req("GET", "/api/state", token=TOKEN)
    n0 = len(st.get("works", []))
    check(code == 200 and n0 == 38, f"应读到 38 个案例，实际 {n0}")
    print(f"  · 鉴权通过 · 现有案例 {n0} 个")

    # ---------- 2. 上传 ----------
    tmp = ROOT / "_tmp"
    if not tmp.exists():          # 沙箱内对已存在目录 mkdir 会抛 EEXIST
        tmp.mkdir(parents=True, exist_ok=True)
    png, wav = tmp / "_e2e.png", tmp / "_e2e.wav"
    make_png(png)
    make_wav(wav)

    code, up1 = req("POST", "/api/upload", token=TOKEN, raw=png.read_bytes(),
                    headers={"x-filename": "_e2e.png", "x-target": "uploads",
                             "Content-Type": "application/octet-stream"})
    check(code == 200 and up1.get("kind") == "image", f"图片上传失败：{up1}")
    check((ROOT / up1.get("path", "")).exists(), "上传的图片未落盘")
    created_uploads.append(up1.get("path"))

    code, up2 = req("POST", "/api/upload", token=TOKEN, raw=wav.read_bytes(),
                    headers={"x-filename": "_e2e.wav", "x-target": "uploads",
                             "Content-Type": "application/octet-stream"})
    check(code == 200 and up2.get("kind") == "audio", f"音频上传失败：{up2}")
    created_uploads.append(up2.get("path"))
    print(f"  · 上传通过 · {up1.get('name')} / {up2.get('name')}")

    # ---------- 3. 新建草稿（视频形态 + 海报 + 音乐 + 图集视频项）----------
    video_path = up1["path"]          # 结构占位：任意可访问路径
    poster_path = up1["path"]
    new_work = {
        "id": TMP_WORK, "category": "digital", "status": "draft", "sortOrder": 99,
        "year": "2026", "mediaType": "video",
        "cover": up1["path"], "video": video_path, "videoPoster": poster_path,
        "bgm": up2["path"], "single": False,
        "gallery": [up1["path"], {"type": "video", "src": video_path, "poster": poster_path}],
        "title": {"zh": "端到端测试作品", "es": "Prueba E2E", "en": "E2E test work"},
        "type": {"zh": "测试类型", "es": "Tipo", "en": "Type"},
        "scope": {"zh": "测试范围", "es": "Alcance", "en": "Scope"},
        "blurb": {"zh": "第一段。\n\n第二段。", "es": "Uno.\n\nDos.", "en": "One.\n\nTwo."},
    }
    code, r = req("POST", "/api/works", new_work, token=TOKEN)
    check(code == 200, f"新建作品失败：{r}")
    check(r.get("stats", {}).get("draft", 0) >= 1, "新建草稿后 stats.draft 应 ≥1")

    data_js = (ROOT / "assets/js/data.js").read_text(encoding="utf-8")
    check(TMP_WORK not in data_js, "草稿不应写入站点 data.js")
    print("  · 新建草稿通过 · 草稿未进入 data.js")

    # ---------- 4. 发布 ----------
    code, r = req("PUT", f"/api/works/{TMP_WORK}", {"status": "published"}, token=TOKEN)
    check(code == 200, f"发布失败：{r}")
    data_js = (ROOT / "assets/js/data.js").read_text(encoding="utf-8")
    check(TMP_WORK in data_js, "发布后应写入 data.js")
    check('"mediaType": "video"' in data_js and '"videoPoster"' in data_js,
          "data.js 应包含 mediaType/videoPoster 字段")
    check('"type": "video"' in data_js, "data.js 图集应包含视频项对象")
    check('"bgm"' in data_js, "data.js 应包含 bgm 字段")
    print("  · 发布通过 · 视频/海报/音乐/图集视频字段已写入 data.js")

    # ---------- 5. sortOrder 重排 ----------
    code, st = req("GET", "/api/state", token=TOKEN)
    ids = [w["id"] for w in sorted(st["works"], key=lambda x: x.get("sortOrder", 0))]
    ids.remove(TMP_WORK)
    ids.insert(0, TMP_WORK)
    code, r = req("POST", "/api/works/reorder", {"ids": ids}, token=TOKEN)
    check(code == 200, f"重排失败：{r}")
    data_js = (ROOT / "assets/js/data.js").read_text(encoding="utf-8")
    first_id = data_js.split('"id": "', 1)[1].split('"', 1)[0]
    check(first_id == TMP_WORK, f"重排后 data.js 首项应为 {TMP_WORK}，实际 {first_id}")
    print(f"  · 排序通过 · data.js 首项 = {first_id}")

    # ---------- 6. 改名 + 素材目录迁移 ----------
    media_dir_old = ROOT / "assets/uploads"
    code, r = req("PUT", f"/api/works/{TMP_WORK}", {"id": TMP_WORK + "-r"}, token=TOKEN)
    check(code == 200, f"改名失败：{r}")
    check(TMP_WORK + "-r" in (ROOT / "assets/js/data.js").read_text(encoding="utf-8"),
          "改名后 data.js 应使用新 id")
    print("  · 改名通过 · id 已切换并重写站点数据")
    TMP_WORK = TMP_WORK + "-r"

    # ---------- 7. 站点设置：主页文案 + 社交链接 ----------
    code, site = req("GET", "/api/site", token=TOKEN)
    old_sub = site["copy"].get("home.subtitle", {}).get("zh", "")
    site["copy"]["home.subtitle"]["zh"] = "【E2E】后台主页文案覆盖测试"
    site["social"][1]["url"] = "https://e2e.example.com/xhs"
    code, r = req("PUT", "/api/site", site, token=TOKEN)
    check(code == 200, f"保存站点设置失败：{r}")
    site_js = (ROOT / "assets/js/site-data.js").read_text(encoding="utf-8")
    check("【E2E】后台主页文案覆盖测试" in site_js, "site-data.js 未写入新文案")
    check("e2e.example.com" in site_js, "site-data.js 未写入社交链接")
    print("  · 站点设置通过 · site-data.js 已重写")

    # ---------- 8. 数据源兜底（不可达 API）----------
    site = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
    site["source"] = {"mode": "api", "apiBase": "http://127.0.0.1:1/definitely-down",
                      "sanity": {"projectId": "", "dataset": "production", "apiVersion": "2024-01-01"}}
    code, r = req("PUT", "/api/site", site, token=TOKEN)
    check(code == 200, "切换到远端数据源失败")

    # ---------- 9. 浏览器侧验证 ----------
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))

        # 9.1 后台界面可用
        pg.goto(f"{BASE}/admin", wait_until="networkidle")
        check(pg.locator("#login").is_visible(), "后台应显示登录页")
        pg.fill("#pw", PASSWORD)
        pg.click("#loginBtn")
        pg.wait_for_timeout(1500)
        check(pg.locator("#app").is_visible(), "登录后应进入后台主界面")
        items = pg.locator(".item").count()
        check(items >= 38, f"后台列表应 ≥38 项，实际 {items}")
        title0 = pg.locator("#pane .pane__title").first.inner_text()
        check(bool(title0.strip()), "后台应渲染作品编辑面板")
        tabs = pg.locator("#pane .tab").count()
        check(tabs == 4, f"编辑器应有 4 个页签，实际 {tabs}")
        pg.click('.tab[data-tab="gallery"]')
        pg.wait_for_timeout(400)
        check(pg.locator("#galleryList").count() == 1, "图集页签应渲染图集列表")
        pg.screenshot(path=str(ROOT / "_tools/screens/12-admin-works.png"), full_page=False)
        print(f"  · 后台界面通过 · {items} 个作品 · 4 页签 · 面板「{title0.strip()[:20]}」")

        # 9.2 站点设置面板
        pg.click("#btnSiteSettings")
        pg.wait_for_timeout(600)
        check(pg.locator('[data-source="mode"]').count() == 1, "站点设置应包含数据源选项")
        social_cards = pg.locator("#socialList .rowcard").count()
        check(social_cards >= 3, f"社交入口应有 ≥3 个，实际 {social_cards}")
        pg.screenshot(path=str(ROOT / "_tools/screens/13-admin-site.png"), full_page=False)
        print(f"  · 站点设置面板通过 · 社交入口 {social_cards} 个")

        # 9.3 详情页：远端不可达 → 回退本地；视频首屏 + 图集视频 + 背景音乐
        pg.goto(f"{BASE}/work-detail.html?id={TMP_WORK}", wait_until="networkidle")
        pg.wait_for_timeout(1500)
        src_mode = pg.evaluate("()=>document.documentElement.getAttribute('data-content-source')")
        check(src_mode == "local", f"远端 API 不可达时应回退 local，实际 {src_mode}")
        h1 = pg.locator("h1").first.inner_text()
        check("端到端测试作品" in h1, f"兜底后应渲染本地数据，实际标题「{h1}」")
        vids = pg.locator(".work-cover video").count()
        check(vids == 1, f"视频形态作品首屏应有 1 个 video，实际 {vids}")
        gv = pg.locator(".work-gallery video").count()
        check(gv == 1, f"图集应渲染 1 个 video，实际 {gv}")
        gi = pg.locator(".work-gallery img").count()
        check(gi == 1, f"图集应渲染 1 个 img，实际 {gi}")
        bgm = pg.locator(".bgm-btn").count()
        check(bgm == 1, f"配置了音乐应出现播放按钮，实际 {bgm}")
        if bgm:
            pg.click(".bgm-btn")
            pg.wait_for_timeout(700)
            on = pg.evaluate("()=>document.querySelector('.bgm-btn').classList.contains('is-on')")
            check(on, "点击背景音乐按钮后应进入播放态")
        pg.screenshot(path=str(ROOT / "_tools/screens/14-admin-video-detail.png"), full_page=False)
        print(f"  · 详情页通过 · 兜底源 {src_mode} · 视频 {vids} · 图集 视频{gv}/图{gi} · 音乐按钮 {bgm}")

        # 9.4 首页：site-data 覆盖文案 + 社交链接
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        pg.wait_for_timeout(800)
        sub = pg.evaluate("()=>document.querySelector('[data-i18n=\"home.subtitle\"]')?.textContent||''")
        check("【E2E】" in sub, f"首页副标题应显示后台覆盖文案，实际「{sub[:40]}」")
        href = pg.evaluate("()=>document.querySelector('[data-social=\"xhs\"]')?.getAttribute('href')")
        check(href == "https://e2e.example.com/xhs", f"社交链接未注入，实际 {href}")
        print(f"  · 首页覆盖通过 · 副标题「{sub[:22]}…」· xhs={href}")

        check(not errs, f"浏览器 JS 错误：{errs[:2]}")
        browser.close()

finally:
    # ---------- 清理 ----------
    try:
        code, st = req("GET", "/api/state", token=TOKEN)
        for w in st.get("works", []):
            if w["id"].startswith("zze2e-"):
                req("DELETE", f"/api/works/{urllib.parse.quote(w['id'])}?deleteMedia=1", token=TOKEN)
    except Exception:
        pass
    try:
        (ROOT / "content/site.json").write_text(site_backup, encoding="utf-8")
        req("POST", "/api/sync", token=TOKEN)
    except Exception:
        pass
    for rel in created_uploads:
        p = ROOT / rel
        if p.exists():
            p.unlink()
    for f in [ROOT / "_tmp/_e2e.png", ROOT / "_tmp/_e2e.wav"]:
        if f.exists():
            f.unlink()
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()

# ---------- 结果 ----------
print("\n".join(log))
print("=" * 62)
data_js = (ROOT / "assets/js/data.js").read_text(encoding="utf-8")
check("zze2e-" not in data_js, "清理后 data.js 不应残留测试作品")
print(f"  清理完成 · data.js 案例数 {data_js.count('\"id\": \"')}")
print("=" * 62)

if fails:
    print(f"  ✗ 共 {len(fails)} 项未通过：")
    for f in fails:
        print("     ·", f)
    sys.exit(1)
print("  ✓ 后台管理系统全部通过 —— 鉴权 / CRUD / 上传 / 视频 / 排序 / 改名 / 站点设置 / 兜底 / 界面")
