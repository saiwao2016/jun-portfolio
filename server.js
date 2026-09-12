/* =========================================================
   JUN Portfolio — 后台管理系统服务端
   零外部依赖（仅 node 内置模块）· 单端口 HTTP 服务
     静态托管整个站点  +  /admin 管理后台  +  /api/* REST 接口

   启动：
     node server.js                 # 默认 3000 端口
     PORT=8080 node server.js
     ADMIN_PASSWORD=xxxx node server.js

   数据源：content/works.json（作品）· content/site.json（站点设置）
   每次保存都会重写 assets/js/data.js 与 assets/js/site-data.js，
   并刷新两个文件在 HTML 中的内容哈希查询串（绕过 CDN 同名缓存）。
   ========================================================= */
'use strict';

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { syncAll } = require('./_tools/build_content.js');
const { spawnSync } = require('node:child_process');

const ROOT = __dirname;
const CONTENT_DIR = path.join(ROOT, 'content');
const WORKS_FILE = path.join(CONTENT_DIR, 'works.json');
const SITE_FILE = path.join(CONTENT_DIR, 'site.json');
const AUTH_FILE = path.join(CONTENT_DIR, 'auth.json');

const PORT = Number(process.env.PORT) || 3000;
const HOST = process.env.HOST || '0.0.0.0';
const MAX_JSON = 8 * 1024 * 1024;        // JSON 请求体上限
const MAX_UPLOAD = 1024 * 1024 * 1024;   // 上传上限 1GB（视频）
const SESSION_TTL = 12 * 60 * 60 * 1000; // 登录有效期 12h

/* ---------------- 工具 ---------------- */

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.gif': 'image/gif', '.webp': 'image/webp', '.avif': 'image/avif',
  '.ico': 'image/x-icon',
  '.mp4': 'video/mp4', '.webm': 'video/webm', '.mov': 'video/quicktime',
  '.mp3': 'audio/mpeg', '.m4a': 'audio/mp4', '.wav': 'audio/wav', '.ogg': 'audio/ogg',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf',
  '.pdf': 'application/pdf', '.txt': 'text/plain; charset=utf-8',
  '.md': 'text/plain; charset=utf-8',
};

const IMAGE_EXT = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif', '.svg'];
const VIDEO_EXT = ['.mp4', '.webm', '.mov', '.m4v'];
const AUDIO_EXT = ['.mp3', '.m4a', '.wav', '.ogg', '.aac'];

function json(res, code, data) {
  const body = JSON.stringify(data);
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-store',
  });
  res.end(body);
}

function readJsonFile(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    if (fallback !== undefined) return fallback;
    throw e;
  }
}

function writeJsonFile(file, data) {
  const tmp = file + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2) + '\n');
  fs.renameSync(tmp, file);
}

function readBody(req, limit) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', (c) => {
      size += c.length;
      if (size > limit) {
        reject(Object.assign(new Error('请求体过大'), { code: 413 }));
        req.destroy();
        return;
      }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

async function readJsonBody(req) {
  const buf = await readBody(req, MAX_JSON);
  if (!buf.length) return {};
  try {
    return JSON.parse(buf.toString('utf8'));
  } catch (e) {
    throw Object.assign(new Error('JSON 解析失败'), { code: 400 });
  }
}

/** 目录不存在才创建（沙箱内对已存在目录 mkdir 会抛 EEXIST） */
function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function slugify(s, fallback) {
  const out = String(s || '')
    .normalize('NFKD')
    .replace(/[^\w.\-\u4e00-\u9fa5]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 60);
  return out || fallback;
}

function kindOf(ext) {
  if (IMAGE_EXT.includes(ext)) return 'image';
  if (VIDEO_EXT.includes(ext)) return 'video';
  if (AUDIO_EXT.includes(ext)) return 'audio';
  return 'file';
}

/** 作品改名时，把指向旧素材目录的路径改写为新目录 */
function remapDir(p, fromId, toId) {
  if (!p || typeof p !== 'string') return p;
  const a = `assets/works/${fromId}/`;
  return p.startsWith(a) ? `assets/works/${toId}/${p.slice(a.length)}` : p;
}

/* ---------------- 鉴权 ---------------- */

function loadPassword() {
  if (process.env.ADMIN_PASSWORD) return { password: process.env.ADMIN_PASSWORD, generated: false };
  let doc = readJsonFile(AUTH_FILE, null);
  if (doc && doc.password) return { password: doc.password, generated: false };
  const password = crypto.randomBytes(4).toString('hex'); // 8 位
  ensureDir(CONTENT_DIR);
  writeJsonFile(AUTH_FILE, { password, createdAt: new Date().toISOString() });
  return { password, generated: true };
}

const AUTH = loadPassword();
const sessions = new Map(); // token → expiresAt
const loginFails = new Map(); // ip → {n, until}

function newSession() {
  const token = crypto.randomBytes(24).toString('hex');
  sessions.set(token, Date.now() + SESSION_TTL);
  return token;
}

function authed(req) {
  const h = req.headers.authorization || '';
  const token = h.startsWith('Bearer ') ? h.slice(7) : (req.headers['x-admin-token'] || '');
  if (!token) return false;
  const exp = sessions.get(token);
  if (!exp) return false;
  if (exp < Date.now()) { sessions.delete(token); return false; }
  return true;
}

/* ---------------- 内容读写 ---------------- */

function loadWorksDoc() {
  const doc = readJsonFile(WORKS_FILE);
  return Array.isArray(doc) ? { version: 1, works: doc } : doc;
}

function saveWorks(works) {
  writeJsonFile(WORKS_FILE, { version: 1, updatedAt: new Date().toISOString(), works });
  const stats = syncAll(ROOT);
  stats.hash = refreshAssetHashes();
  return stats;
}

function loadSite() { return readJsonFile(SITE_FILE); }
function saveSite(site) {
  site.updatedAt = new Date().toISOString();
  writeJsonFile(SITE_FILE, site);
  const stats = syncAll(ROOT);
  stats.hash = refreshAssetHashes();
  return stats;
}

/** 为 data.js / site-data.js 刷新 HTML 里的内容哈希查询串 */
function refreshAssetHashes() {
  const targets = [
    ['assets/js/data.js', 'assets/js/data.js'],
    ['assets/js/site-data.js', 'assets/js/site-data.js'],
  ];
  const hashes = {};
  targets.forEach(([rel]) => {
    const p = path.join(ROOT, rel);
    if (!fs.existsSync(p)) return;
    const h = crypto.createHash('sha1').update(fs.readFileSync(p)).digest('hex').slice(0, 8);
    hashes[rel] = h;
  });
  const htmlFiles = fs.readdirSync(ROOT).filter((f) => f.endsWith('.html'));
  let changed = 0;
  htmlFiles.forEach((f) => {
    const p = path.join(ROOT, f);
    let t = fs.readFileSync(p, 'utf8');
    const before = t;
    Object.entries(hashes).forEach(([rel, h]) => {
      const re = new RegExp(rel.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\?[^"\']*', 'g');
      t = t.replace(re, `${rel}?h=${h}`);
    });
    if (t !== before) { fs.writeFileSync(p, t); changed++; }
  });
  return { hashes, changed };
}

/* ---------------- 发布：提交并推送到远端（触发 Pages 重建） ---------------- */

const PUBLISH_FILE = path.join(CONTENT_DIR, 'publish.json');
const DEFAULT_PUBLISH = {
  remote: 'origin',
  branch: 'main',
  siteUrl: '',
  authorName: 'JUN',
  authorEmail: 'saiwao@qq.com',
};

function loadPublishCfg() {
  const doc = readJsonFile(PUBLISH_FILE, {}) || {};
  return {
    ...DEFAULT_PUBLISH,
    ...doc,
    remote: process.env.GIT_REMOTE || doc.remote || DEFAULT_PUBLISH.remote,
    branch: process.env.GIT_BRANCH || doc.branch || DEFAULT_PUBLISH.branch,
  };
}

/** 同步执行 git；返回 { ok, code, out } */
function git(args) {
  const r = spawnSync('git', args, {
    cwd: ROOT,
    encoding: 'utf8',
    env: { ...process.env, GIT_TERMINAL_PROMPT: '0' },
    maxBuffer: 32 * 1024 * 1024,
  });
  if (r.error) return { ok: false, code: -1, out: String(r.error.message || r.error) };
  return { ok: r.status === 0, code: r.status, out: ((r.stdout || '') + (r.stderr || '')).trim() };
}

/** 提交身份：优先用仓库/全局配置，没有则临时指定 */
function gitIdentity(cfg) {
  return ['-c', `user.name=${cfg.authorName}`, '-c', `user.email=${cfg.authorEmail}`];
}

function publishStatus(cfg) {
  if (git(['rev-parse', '--is-inside-work-tree']).out !== 'true') {
    return { repo: false, error: '当前目录不是 Git 仓库' };
  }
  const branch = git(['rev-parse', '--abbrev-ref', 'HEAD']).out || cfg.branch;
  const ru = git(['remote', 'get-url', cfg.remote]);
  const porcelain = git(['status', '--porcelain']).out;
  const dirty = porcelain ? porcelain.split('\n').filter(Boolean) : [];
  const [hash = '', subject = '', date = ''] = git(['log', '-1', '--format=%h|%s|%ci']).out.split('|');
  const ahead = Number(git(['rev-list', '--count', `${cfg.remote}/${branch}..HEAD`]).out) || 0;
  return {
    repo: true,
    branch,
    remote: cfg.remote,
    remoteUrl: ru.ok ? ru.out.replace(/\/\/[^@/]+@/, '//') : '',
    dirty: dirty.slice(0, 300),
    dirtyCount: dirty.length,
    ahead,
    lastCommit: hash ? { hash, subject, date } : null,
    siteUrl: cfg.siteUrl,
  };
}

function doPublish(cfg, message) {
  if (git(['rev-parse', '--is-inside-work-tree']).out !== 'true') {
    throw new Error('当前目录不是 Git 仓库，无法发布');
  }
  // 先按最新 content/*.json 重写 data.js / site-data.js，保证线上与后台一致
  try { syncAll(ROOT); refreshAssetHashes(); } catch (e) { throw new Error('生成站点数据失败：' + e.message); }

  const add = git(['add', '-A']);
  if (!add.ok) throw new Error('git add 失败：' + add.out);

  const changed = (git(['status', '--porcelain']).out || '').split('\n').filter(Boolean);
  if (!changed.length) {
    return { ok: true, committed: false, pushed: false, changed: 0,
      message: '没有需要发布的改动', status: publishStatus(cfg) };
  }

  const msg = message || `内容更新 · ${new Date().toLocaleString('zh-CN', { hour12: false })}`;
  const cm = git([...gitIdentity(cfg), 'commit', '-m', msg]);
  if (!cm.ok) throw new Error('git commit 失败：' + cm.out);

  const push = git(['push', cfg.remote, `HEAD:${cfg.branch}`]);
  if (!push.ok) {
    const bad = /Authentication failed|could not read Username|Invalid username|403|401|Permission denied/i.test(push.out);
    throw new Error((bad
      ? '推送失败：远端凭据无效或已过期（GitHub Token 通常 30–90 天到期），请更新后重试。\n'
      : 'git push 失败：') + push.out);
  }
  return {
    ok: true, committed: true, pushed: true, changed: changed.length,
    commit: git(['log', '-1', '--format=%h %s']).out,
    message: `已推送 ${changed.length} 项改动到 ${cfg.remote}/${cfg.branch}，线上约 1 分钟后更新`,
    status: publishStatus(cfg),
  };
}

/* ---------------- 静态文件 ---------------- */

function serveStatic(req, res, urlPath, { noCache = false } = {}) {
  let rel = decodeURIComponent(urlPath);
  if (rel === '/' || rel === '') rel = '/index.html';
  if (rel.endsWith('/')) rel += 'index.html';

  const abs = path.join(ROOT, path.normalize(rel).replace(/^(\.\.[/\\])+/, ''));
  if (!abs.startsWith(ROOT)) return json(res, 403, { error: 'forbidden' });

  let stat;
  try { stat = fs.statSync(abs); } catch { return notFound(res); }
  if (stat.isDirectory()) return serveStatic(req, res, rel.replace(/\/?$/, '/index.html'), { noCache });

  const ext = path.extname(abs).toLowerCase();
  const type = MIME[ext] || 'application/octet-stream';
  const etag = `W/"${stat.size}-${stat.mtimeMs}"`;
  const headers = {
    'Content-Type': type,
    'Cache-Control': noCache ? 'no-store' : 'public, max-age=300',
    'ETag': etag,
    'Last-Modified': new Date(stat.mtimeMs).toUTCString(),
    'Accept-Ranges': 'bytes',
  };

  if (req.headers['if-none-match'] === etag) {
    res.writeHead(304, headers);
    return res.end();
  }

  // Range（视频拖动进度必需）
  const range = req.headers.range;
  if (range && /^bytes=\d*-\d*$/.test(range)) {
    const [s, e] = range.replace('bytes=', '').split('-');
    const start = s === '' ? Math.max(0, stat.size - Number(e)) : Number(s);
    const end = s === '' || e === '' ? stat.size - 1 : Math.min(Number(e), stat.size - 1);
    if (start <= end && start < stat.size) {
      headers['Content-Range'] = `bytes ${start}-${end}/${stat.size}`;
      headers['Content-Length'] = end - start + 1;
      res.writeHead(206, headers);
      return fs.createReadStream(abs, { start, end }).pipe(res);
    }
  }

  headers['Content-Length'] = stat.size;
  res.writeHead(200, headers);
  if (req.method === 'HEAD') return res.end();
  fs.createReadStream(abs).pipe(res);
}

function notFound(res) {
  const p = path.join(ROOT, '404.html');
  if (fs.existsSync(p)) {
    const body = fs.readFileSync(p);
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8', 'Content-Length': body.length });
    return res.end(body);
  }
  json(res, 404, { error: 'not_found' });
}

/* ---------------- API 路由 ---------------- */

async function handleApi(req, res, seg, query) {
  const route = seg.slice(1).join('/'); // /api/xxx → 'xxx'
  const method = req.method;

  /* --- 公开 --- */
  if (route === 'health') return json(res, 200, { ok: true, ts: Date.now() });

  if (route === 'login' && method === 'POST') {
    const ip = req.socket.remoteAddress || '-';
    const rec = loginFails.get(ip);
    if (rec && rec.until > Date.now()) {
      return json(res, 429, { error: `尝试过多，请 ${Math.ceil((rec.until - Date.now()) / 1000)} 秒后重试` });
    }
    const body = await readJsonBody(req);
    if (!body.password || body.password !== AUTH.password) {
      const n = (rec && rec.n) || 0;
      loginFails.set(ip, n + 1 >= 5 ? { n: 0, until: Date.now() + 60_000 } : { n: n + 1, until: 0 });
      return json(res, 401, { error: '密码错误' });
    }
    loginFails.delete(ip);
    return json(res, 200, { token: newSession(), passwordIsGenerated: AUTH.generated });
  }

  /* --- 以下需登录 --- */
  if (!authed(req)) return json(res, 401, { error: '未登录或登录已过期' });

  if (route === 'logout' && method === 'POST') {
    const h = req.headers.authorization || '';
    sessions.delete(h.replace('Bearer ', ''));
    return json(res, 200, { ok: true });
  }

  if (route === 'state' && method === 'GET') {
    return json(res, 200, {
      works: loadWorksDoc().works,
      site: loadSite(),
      passwordIsGenerated: AUTH.generated,
    });
  }

  /* --- 作品 CRUD --- */
  if (route === 'works' && method === 'POST') {
    const w = await readJsonBody(req);
    if (!w.id) return json(res, 400, { error: '缺少 id' });
    const doc = loadWorksDoc();
    if (doc.works.some((x) => x.id === w.id)) return json(res, 409, { error: `id「${w.id}」已存在` });
    w.sortOrder = Number(w.sortOrder) || (doc.works.length + 1);
    doc.works.push(w);
    const stats = saveWorks(doc.works);
    return json(res, 200, { work: w, stats });
  }

  if (route === 'works/reorder' && method === 'POST') {
    const { ids } = await readJsonBody(req);
    const doc = loadWorksDoc();
    ids.forEach((id, i) => {
      const w = doc.works.find((x) => x.id === id);
      if (w) w.sortOrder = i + 1;
    });
    return json(res, 200, { ok: true, stats: saveWorks(doc.works) });
  }

  if (seg[1] === 'works' && seg[2]) {
    const id = decodeURIComponent(seg[2]);
    const doc = loadWorksDoc();
    const idx = doc.works.findIndex((x) => x.id === id);

    if (method === 'PUT') {
      const patch = await readJsonBody(req);
      if (idx < 0) return json(res, 404, { error: '作品不存在' });
      let renameNote = '';
      // 支持改名：id 变化时校验唯一性并迁移素材目录
      const nextId = patch.id ? String(patch.id).trim() : id;
      if (nextId && nextId !== id) {
        if (!/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(nextId)) {
          return json(res, 400, { error: 'id 只能包含字母、数字、. _ -，且以字母或数字开头' });
        }
        if (doc.works.some((x, k) => k !== idx && x.id === nextId)) {
          return json(res, 409, { error: `id「${nextId}」已被占用` });
        }
        const from = path.join(ROOT, 'assets/works', id);
        const to = path.join(ROOT, 'assets/works', nextId);
        if (fs.existsSync(from) && !fs.existsSync(to)) {
          fs.renameSync(from, to);
          renameNote = `，素材目录已迁移至 assets/works/${nextId}/`;
        }
        // 同步改写指向旧目录的媒体路径（仅处理本次确实提交了的字段，
        // 否则会把未提交的 cover/video 覆盖成 undefined 而丢失）
        if ('cover' in patch) patch.cover = remapDir(patch.cover, id, nextId);
        if ('video' in patch) patch.video = remapDir(patch.video, id, nextId);
        if ('videoPoster' in patch) patch.videoPoster = remapDir(patch.videoPoster, id, nextId);
        if (Array.isArray(patch.gallery)) {
          patch.gallery = patch.gallery.map((g) => {
            if (typeof g === 'string') return remapDir(g, id, nextId);
            if (g && g.src) return { ...g, src: remapDir(g.src, id, nextId), poster: remapDir(g.poster, id, nextId) };
            return g;
          });
        }
      }
      doc.works[idx] = { ...doc.works[idx], ...patch, id: nextId || id };
      const stats = saveWorks(doc.works);
      return json(res, 200, { work: doc.works[idx], renameNote, stats });
    }

    if (method === 'DELETE') {
      if (idx < 0) return json(res, 404, { error: '作品不存在' });
      const [removed] = doc.works.splice(idx, 1);
      let mediaNote = '';
      if (query.get('deleteMedia') === '1' && /^[\w.\-\u4e00-\u9fa5]+$/.test(removed.id)) {
        const dir = path.join(ROOT, 'assets/works', removed.id);
        if (dir.startsWith(ROOT) && fs.existsSync(dir)) {
          fs.rmSync(dir, { recursive: true, force: true });
          mediaNote = `，已删除素材目录 assets/works/${removed.id}/`;
        }
      }
      const stats = saveWorks(doc.works);
      return json(res, 200, { ok: true, removed: removed.id, mediaNote, stats });
    }
  }

  /* --- 上传（原始二进制 + 头部元信息，避免 multipart 解析） --- */
  if (route === 'upload' && method === 'POST') {
    const rawName = decodeURIComponent(req.headers['x-filename'] || '');
    if (!rawName) return json(res, 400, { error: '缺少 x-filename' });
    const target = slugify(req.headers['x-target'] || 'uploads', 'uploads');
    const ext = path.extname(rawName).toLowerCase();
    const base = slugify(path.basename(rawName, path.extname(rawName)), 'file');
    const buf = await readBody(req, MAX_UPLOAD);
    if (!buf.length) return json(res, 400, { error: '空文件' });

    const relDir = target === 'site'
      ? 'assets/site'
      : (target === 'uploads' ? 'assets/uploads' : `assets/works/${target}`);
    const absDir = path.join(ROOT, relDir);
    ensureDir(absDir);

    const stamp = Date.now().toString(36).slice(-5);
    const file = `${base}-${stamp}${ext}`;
    fs.writeFileSync(path.join(absDir, file), buf);

    const rel = `${relDir}/${file}`;
    return json(res, 200, {
      path: rel,
      url: rel,
      kind: kindOf(ext),
      size: buf.length,
      name: file,
    });
  }

  /* --- 媒体删除 --- */
  if (route === 'media/delete' && method === 'POST') {
    const { path: rel } = await readJsonBody(req);
    if (!rel || !/^assets\/(works|uploads|site)\//.test(rel)) {
      return json(res, 400, { error: '只能删除 assets/works|uploads|site 下的文件' });
    }
    const abs = path.join(ROOT, rel);
    if (!abs.startsWith(ROOT) || !fs.existsSync(abs)) return json(res, 404, { error: '文件不存在' });
    fs.unlinkSync(abs);
    return json(res, 200, { ok: true, path: rel });
  }

  /* --- 站点设置 --- */
  if (route === 'site') {
    if (method === 'GET') return json(res, 200, loadSite());
    if (method === 'PUT') {
      const body = await readJsonBody(req);
      const site = { ...loadSite(), ...body };
      return json(res, 200, { site, stats: saveSite(site) });
    }
  }

  /* --- 媒体文件列表（供后台选择已有素材） --- */
  if (route === 'media' && method === 'GET') {
    const target = query.get('target') || '';
    const relDir = target === 'site'
      ? 'assets/site'
      : (target === 'uploads' || !target ? 'assets/uploads' : `assets/works/${slugify(target, 'uploads')}`);
    const absDir = path.join(ROOT, relDir);
    let files = [];
    try {
      files = fs.readdirSync(absDir)
        .filter((f) => !f.startsWith('.'))
        .map((f) => {
          const st = fs.statSync(path.join(absDir, f));
          const ext = path.extname(f).toLowerCase();
          return { path: `${relDir}/${f}`, name: f, size: st.size, kind: kindOf(ext), mtime: st.mtimeMs };
        })
        .sort((a, b) => b.mtime - a.mtime);
    } catch { /* 目录不存在 → 空列表 */ }
    return json(res, 200, { dir: relDir, files });
  }

  /* --- 手动同步（重写 data.js / site-data.js + 刷新哈希） --- */
  if (route === 'sync' && method === 'POST') {
    const stats = syncAll(ROOT);
    const hash = refreshAssetHashes();
    return json(res, 200, { stats, hash });
  }

  /* --- 发布到线上（git commit + push，触发 Pages 重建） --- */
  if (route === 'publish') {
    const cfg = loadPublishCfg();
    if (method === 'GET') return json(res, 200, publishStatus(cfg));
    if (method === 'POST') {
      let message = '';
      try {
        const body = await readJsonBody(req);
        message = String((body && body.message) || '').trim();
      } catch { /* 允许空 body */ }
      try {
        return json(res, 200, doPublish(cfg, message));
      } catch (e) {
        return json(res, 500, { error: e.message || '发布失败', status: publishStatus(cfg) });
      }
    }
  }

  return json(res, 404, { error: `未知接口 ${method} /api/${route}` });
}

/* ---------------- 服务器 ---------------- */

const server = http.createServer(async (req, res) => {
  let url;
  try {
    url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  } catch {
    return json(res, 400, { error: 'bad url' });
  }
  const seg = url.pathname.split('/').filter((s) => s !== '');

  res.setHeader('X-Content-Type-Options', 'nosniff');

  try {
    if (seg[0] === 'api') return await handleApi(req, res, seg, url.searchParams);

    // 后台界面
    if (seg[0] === 'admin') {
      // 补尾斜杠，保证页面内相对路径按 /admin/ 解析
      if (url.pathname === '/admin') {
        res.writeHead(301, { Location: '/admin/' });
        return res.end();
      }
      const rest = seg.slice(1).join('/');
      if (rest === '' || rest === 'index.html') {
        return serveStatic(req, res, '/admin/index.html', { noCache: true });
      }
      return serveStatic(req, res, '/admin/' + rest, { noCache: true });
    }

    if (req.method !== 'GET' && req.method !== 'HEAD') {
      return json(res, 405, { error: 'method not allowed' });
    }
    return serveStatic(req, res, url.pathname);
  } catch (err) {
    const code = err && err.code ? err.code : 500;
    console.error('[error]', req.method, url.pathname, err && err.message);
    if (res.headersSent) return res.end();
    json(res, typeof code === 'number' ? code : 500, { error: err.message || 'server error' });
  }
});

server.listen(PORT, HOST, () => {
  const line = '─'.repeat(58);
  console.log(line);
  console.log('  JUN Portfolio · 站点 + 内容后台已启动');
  console.log(line);
  console.log(`  站点首页   http://localhost:${PORT}/`);
  console.log(`  管理后台   http://localhost:${PORT}/admin`);
  console.log(`  监听       ${HOST}:${PORT}`);
  if (AUTH.generated) {
    console.log(line);
    console.log('  已生成后台密码（首次启动，保存在 content/auth.json）：');
    console.log(`      ${AUTH.password}`);
  }
  console.log(line);
});

process.on('SIGINT', () => { console.log('\n已停止。'); process.exit(0); });
