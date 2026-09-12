/* =========================================================
   内容构建器：content/works.json + content/site.json
              →  assets/js/data.js  +  assets/js/site-data.js
   由后台 server.js 保存时调用，也可单独 CLI 执行：
     node _tools/build_content.js
   ========================================================= */
'use strict';
const fs = require('node:fs');
const path = require('node:path');

const HEADER =
  '/* =========================================================\n' +
  '   JUN Portfolio — Works data（自动生成）\n' +
  '   数据源：content/works.json · 由后台 /admin 保存时重写，请勿手改本文件。\n' +
  '   仅包含 status = published 的案例，按 sortOrder 升序排列。\n' +
  '   图片位于 assets/works/<dir>/；gallery 项为字符串（图片）或\n' +
  '   { type:"video", src, poster }（视频）。\n' +
  '   ========================================================= */\n\n';

const SITE_HEADER =
  '/* =========================================================\n' +
  '   JUN Portfolio — Site settings（自动生成）\n' +
  '   数据源：content/site.json · 由后台 /admin 保存时重写，请勿手改本文件。\n' +
  '   window.SITE_DATA.copy   → 覆盖 i18n 中的主页 / 页脚文案\n' +
  '   window.SITE_DATA.social → 社交入口（文案 + 链接）\n' +
  '   window.SITE_DATA.bgm    → 站点背景音乐\n' +
  '   window.SITE_DATA.source → 远端数据源配置（失败回退本地 data.js）\n' +
  '   ========================================================= */\n\n';

function readJson(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    if (fallback !== undefined) return fallback;
    throw e;
  }
}

/** 归一化单个作品：字段补全 + 只保留站点需要的键 */
function normalizeWork(w, index) {
  const gallery = (w.gallery || [])
    .map((g) => (typeof g === 'string' ? { type: 'image', src: g, poster: '' } : g))
    .filter((g) => g && g.src)
    .map((g) => (g.type === 'video'
      ? { type: 'video', src: g.src, poster: g.poster || '' }
      : g.src));

  const out = {
    id: String(w.id),
    category: w.category || 'digital',
    year: w.year || '',
    cover: w.cover || '',
    gallery,
    title: w.title || { zh: '', es: '', en: '' },
    type: w.type || { zh: '', es: '', en: '' },
    scope: w.scope || { zh: '', es: '', en: '' },
    blurb: w.blurb || { zh: '', es: '', en: '' },
  };
  // 可选字段只在有值时输出，保持 data.js 干净
  if (w.single) out.single = true;
  if (w.mediaType === 'video' && w.video) {
    out.mediaType = 'video';
    out.video = w.video;
    if (w.videoPoster) out.videoPoster = w.videoPoster;
  }
  if (w.bgm) out.bgm = w.bgm;
  return out;
}

function sortWorks(works) {
  return works
    .filter((w) => (w.status || 'published') === 'published')
    .slice()
    .sort((a, b) => (Number(a.sortOrder) || 0) - (Number(b.sortOrder) || 0));
}

/** 生成 assets/js/data.js 文本 */
function buildDataJs(works) {
  const published = sortWorks(works).map(normalizeWork);
  const body = JSON.stringify(published, null, 2)
    .split('\n')
    .map((line) => (line ? '  ' + line : line))
    .join('\n');
  return (
    HEADER +
    '(function () {\n' +
    "  'use strict';\n\n" +
    '  window.WORKS = ' + body.trimStart() + ';\n' +
    '})();\n'
  );
}

/** 生成 assets/js/site-data.js 文本 */
function buildSiteJs(site) {
  const payload = {
    copy: site.copy || {},
    social: site.social || [],
    bgm: site.bgm || {},
    source: site.source || { mode: 'local' },
  };
  const body = JSON.stringify(payload, null, 2)
    .split('\n')
    .map((line) => (line ? '  ' + line : line))
    .join('\n');
  return SITE_HEADER + 'window.SITE_DATA = ' + body.trimStart() + ';\n';
}

/** 读取 content/*.json 并写回站点脚本，返回统计信息 */
function syncAll(root) {
  const contentDir = path.join(root, 'content');
  const worksDoc = readJson(path.join(contentDir, 'works.json'));
  const siteDoc = readJson(path.join(contentDir, 'site.json'));
  const works = Array.isArray(worksDoc) ? worksDoc : worksDoc.works || [];

  const dataPath = path.join(root, 'assets/js/data.js');
  const sitePath = path.join(root, 'assets/js/site-data.js');
  fs.writeFileSync(dataPath, buildDataJs(works));
  fs.writeFileSync(sitePath, buildSiteJs(siteDoc));

  const published = sortWorks(works).length;
  return {
    total: works.length,
    published,
    draft: works.length - published,
    dataPath,
    sitePath,
    bytes: fs.statSync(dataPath).size,
  };
}

module.exports = { buildDataJs, buildSiteJs, syncAll, sortWorks, normalizeWork };

if (require.main === module) {
  const root = path.resolve(__dirname, '..');
  const r = syncAll(root);
  console.log(`data.js  ←  ${r.published} 个已发布案例（草稿 ${r.draft} 个，共 ${r.total}）  ${(r.bytes / 1024).toFixed(1)} KB`);
  console.log('site-data.js  ←  content/site.json');
}
