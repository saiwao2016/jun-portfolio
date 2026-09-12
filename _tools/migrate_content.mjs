/* =========================================================
   一次性迁移：assets/js/data.js + i18n.js + index.html
        →  content/works.json  +  content/site.json
   幂等：若 content/works.json 已存在则拒绝覆盖（除非 --force）。
   ========================================================= */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const FORCE = process.argv.includes('--force');

const CONTENT = path.join(ROOT, 'content');
if (!fs.existsSync(CONTENT)) fs.mkdirSync(CONTENT, { recursive: true });

function loadGlobals(file, key) {
  const src = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const win = {};
  const ctx = vm.createContext({ window: win, console, Math, Date, JSON, Array, Object, String, Number, Boolean });
  vm.runInContext(src, ctx, { filename: file });
  if (!win[key]) throw new Error(`${file} 未暴露 window.${key}`);
  return win[key];
}

const worksFile = path.join(CONTENT, 'works.json');
const siteFile = path.join(CONTENT, 'site.json');
if (!FORCE && (fs.existsSync(worksFile) || fs.existsSync(siteFile))) {
  console.error('content/ 下已存在 works.json 或 site.json，加 --force 才会覆盖。');
  process.exit(1);
}

/* ---------- 1. 作品 ---------- */
const WORKS = loadGlobals('assets/js/data.js', 'WORKS');

const works = WORKS.map((w, i) => ({
  id: w.id,
  category: w.category,
  status: 'published',
  sortOrder: i + 1,
  year: w.year || '',
  // 媒体形态：image（图集）/ video（首屏视频）
  mediaType: 'image',
  cover: w.cover || '',
  video: '',
  videoPoster: '',
  bgm: '',
  single: !!w.single,
  gallery: (w.gallery || []).map((src) => ({ type: 'image', src, poster: '' })),
  title: w.title,
  type: w.type,
  scope: w.scope,
  blurb: w.blurb,
}));

fs.writeFileSync(worksFile, JSON.stringify({ version: 1, updatedAt: new Date().toISOString(), works }, null, 2) + '\n');
console.log(`works.json  ←  ${works.length} 个案例`);

/* ---------- 2. 站点设置 ---------- */
const I18N = loadGlobals('assets/js/i18n.js', 'I18N');
const LANGS = ['zh', 'es', 'en'];

// 可后台编辑的文案键：主页 + 页脚（其余 UI 文案仍锁定在 i18n.js）
const EDITABLE_PREFIX = ['home.', 'footer.'];
const copy = {};
Object.keys(I18N.zh)
  .filter((k) => EDITABLE_PREFIX.some((p) => k.startsWith(p)))
  .forEach((k) => {
    copy[k] = {};
    LANGS.forEach((l) => { copy[k][l] = (I18N[l] && I18N[l][k]) || ''; });
  });

// 社交链接：从 index.html 抓现有入口（Behance / 小红书 / 邮箱）
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const socialBlock = html.match(/<!-- ===== Social ===== -->([\s\S]*?)<\/section>/);
const social = [];
if (socialBlock) {
  const re = /<a\b([^>]*)>([^<]*)<\/a>/g;
  let m;
  while ((m = re.exec(socialBlock[1]))) {
    const attrs = m[1];
    const text = m[2].trim();
    const href = (attrs.match(/href="([^"]*)"/) || [, ''])[1];
    const key = (attrs.match(/data-i18n="([^"]*)"/) || [, ''])[1];
    const label = key ? copy[key] || {} : null;
    // id 优先取文案键后缀；Behance 这类无键入口回退到链接文字
    const id = key ? key.replace('footer.link.', '')
      : (text.toLowerCase() === 'behance' ? 'behance' : text.trim().toLowerCase());
    social.push({
      id,
      url: href === '#' ? '' : href,
      label: label && label.zh ? label : { zh: text, es: text, en: text },
      i18nKey: key || '',
    });
  }
}

const site = {
  version: 1,
  updatedAt: new Date().toISOString(),
  // 数据源：local（读站点内 data.js）/ api（读 apiBase）/ sanity（读 Sanity 项目）
  // 远端失败一律回退本地 data.js，站点不会空白
  source: {
    mode: 'local',
    apiBase: '',
    sanity: { projectId: '', dataset: 'production', apiVersion: '2024-01-01' },
  },
  // 站点级背景音乐（作品级另有 bgm 字段）
  bgm: { enabled: false, src: '', title: { zh: '', es: '', en: '' }, autoplay: false, loop: true },
  social,
  copy,
};

fs.writeFileSync(siteFile, JSON.stringify(site, null, 2) + '\n');
console.log(`site.json   ←  ${Object.keys(copy).length} 条文案键 · ${social.length} 个社交入口`);
console.log('社交入口：', social.map((s) => `${s.id}(${s.url || '空'})`).join(' · '));
