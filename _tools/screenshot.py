"""Headless screenshot verification for all site pages (desktop + mobile + EN)."""
import os
from playwright.sync_api import sync_playwright

# 绕过沙箱 HTTP 代理，直连本地服务器
for k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "ALL_PROXY"):
    os.environ.pop(k, None)

BASE = "http://127.0.0.1:8765"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screens")
os.makedirs(OUT, exist_ok=True)

PAGES = [
    ("index.html", "01-home-zh", "zh"),
    ("works.html", "02-works-zh", "zh"),
    ("about.html", "03-about-zh", "zh"),
    ("services.html", "04-services-zh", "zh"),
    ("skills.html", "05-skills-zh", "zh"),
    ("contact.html", "06-contact-zh", "zh"),
    ("resume.html", "07-resume-zh", "zh"),
    ("work-detail.html?id=brand-1", "08-work-detail-zh", "zh"),
    ("work-detail.html?id=ip-1", "09-work-detail-ip-zh", "zh"),
    ("index.html", "11-home-en", "en"),
    ("works.html", "12-works-en", "en"),
    ("contact.html", "13-contact-en", "en"),
]

STEP_SCROLL = """
async () => {
  const step = Math.round(window.innerHeight * 0.75);
  const total = document.body.scrollHeight;
  for (let y = 0; y <= total; y += step) {
    window.scrollTo({top: y, behavior: 'instant'});
    await new Promise(r => setTimeout(r, 140));
  }
  window.scrollTo({top: 0, behavior: 'instant'});
  await new Promise(r => setTimeout(r, 250));
}
"""


def load_and_settle(page, url, lang):
    if lang == "en":
        page.goto(f"{BASE}/index.html", wait_until="domcontentloaded")
        page.evaluate("localStorage.setItem('jun.lang','en')")
    page.goto(url, wait_until="networkidle", timeout=20000)
    page.wait_for_timeout(300)
    page.evaluate(STEP_SCROLL)   # 逐屏滚动，确保每个 reveal 元素都进入过视口
    page.wait_for_timeout(200)


errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-proxy-server"])

    for page_path, label, lang in PAGES:
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        msgs = []
        page.on("console", lambda m: msgs.append(f"[{m.type}] {m.text}"))
        page.on("pageerror", lambda e: msgs.append(f"[pageerror] {e}"))

        load_and_settle(page, f"{BASE}/{page_path}", lang)

        revealed = page.evaluate("document.querySelectorAll('.reveal.is-in').length")
        total = page.evaluate("document.querySelectorAll('.reveal').length")
        cards = page.locator(".work-card").count()

        page.screenshot(path=os.path.join(OUT, f"{label}.png"), full_page=True)
        print(f"✓ {label:26s} reveal {revealed}/{total}  cards {cards}")
        for m in msgs:
            if "[error]" in m or "[pageerror]" in m:
                errors.append((label, m))
                print(f"    !! {m}")
        ctx.close()

    # 移动端
    for page_path, label in [("index.html", "00-home-mobile"),
                             ("works.html", "00-works-mobile")]:
        ctx = browser.new_context(viewport={"width": 390, "height": 844},
                                  device_scale_factor=2, is_mobile=True, has_touch=True)
        page = ctx.new_page()
        load_and_settle(page, f"{BASE}/{page_path}", "zh")
        page.screenshot(path=os.path.join(OUT, f"{label}.png"), full_page=True)
        print(f"✓ {label:26s} (mobile)")
        ctx.close()

    browser.close()

print()
if errors:
    print("!!! JS ERRORS !!!")
    for label, m in errors:
        print(f"  {label}: {m}")
    raise SystemExit(1)
print("✅ 全部页面渲染干净，无 JS 错误。")
