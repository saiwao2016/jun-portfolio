/* =========================================================
   JUN Portfolio — 内容后台前端
   原生 JS，无框架、无构建。与 server.js 的 /api 对接。
   ========================================================= */
(() => {
  'use strict';

  /* ---------------- 常量 ---------------- */

  const LANGS = [['zh', '中文'], ['es', 'Español'], ['en', 'English']];

  // 站点分类：前三项在 works.html 有对应筛选按钮
  const CATS = [
    ['digital', '数字界面', true],
    ['ip', '原创 IP', true],
    ['graphic', '平面设计', true],
    ['brand', '品牌 CIS', false],
    ['print', '画册印刷', false],
    ['report', '心理测量报告', false],
    ['spatial', '空间视觉', false],
  ];

  const COPY_GROUPS = [
    { title: '首屏 Hero', keys: ['home.eyebrow', 'home.title.line1', 'home.title.line2', 'home.title.line3', 'home.subtitle'] },
    { title: '首屏按钮', prefix: 'home.cta.' },
    { title: '首屏信息条', prefix: 'home.meta.' },
    { title: '精选作品区', prefix: 'home.featured.' },
    { title: '为什么是我', prefix: 'home.advantages.' },
    { title: '社交区标题', prefix: 'home.social.' },
    { title: '页脚', prefix: 'footer.' },
  ];

  const COPY_LABELS = {
    'home.eyebrow': '眉标',
    'home.title.line1': '主标题 · 第 1 行',
    'home.title.line2': '主标题 · 第 2 行',
    'home.title.line3': '主标题 · 第 3 行（暖棕强调）',
    'home.subtitle': '副标题',
    'home.cta.works': '按钮 · 浏览作品',
    'home.cta.resume': '按钮 · 下载简历',
    'home.cta.contact': '按钮 · 联系合作',
    'home.meta.location': '信息条 · 所在地（标签）',
    'home.meta.location_v': '信息条 · 所在地（内容）',
    'home.meta.lang': '信息条 · 语言（标签）',
    'home.meta.lang_v': '信息条 · 语言（内容）',
    'home.meta.status': '信息条 · 合作状态（标签）',
    'home.meta.status_v': '信息条 · 合作状态（内容）',
    'home.featured.eyebrow': '眉标',
    'home.featured.title': '标题',
    'home.featured.note': '备注',
    'home.advantages.eyebrow': '眉标',
    'home.advantages.title': '标题',
    'home.advantages.lead': '导语',
    'home.advantages.1.title': '第 1 块 · 标题',
    'home.advantages.1.desc': '第 1 块 · 描述',
    'home.advantages.2.title': '第 2 块 · 标题',
    'home.advantages.2.desc': '第 2 块 · 描述',
    'home.advantages.3.title': '第 3 块 · 标题',
    'home.advantages.3.desc': '第 3 块 · 描述',
    'home.social.eyebrow': '眉标',
    'home.social.title': '标题',
    'footer.copy': '版权行',
    'footer.note': '版权行 · 补充',
    'footer.link.behance': '链接 · Behance',
    'footer.link.xhs': '链接 · 小红书',
    'footer.link.email': '链接 · 邮箱',
  };

  /* ---------------- 小工具 ---------------- */

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const esc = (s) => String(s == null ? '' : s)
    .replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  const isImage = (p) => /\.(png|jpe?g|gif|webp|avif|svg)$/i.test(p || '');
  const isVideo = (p) => /\.(mp4|webm|mov|m4v)$/i.test(p || '');
  const isAudio = (p) => /\.(mp3|m4a|wav|ogg|aac)$/i.test(p || '');
  const sizeText = (n) => (n > 1048576 ? (n / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(n / 1024)) + ' KB');

  let toastTimer = null;
  function toast(msg, isErr) {
    const t = $('#toast');
    t.textContent = msg;
    t.className = 'toast is-on' + (isErr ? ' toast--err' : '');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { t.className = 'toast'; }, isErr ? 4200 : 2200);
  }

  /* ---------------- 状态 ---------------- */

  const S = {
    token: localStorage.getItem('jun.admin.token') || '',
    works: [],
    site: null,
    sel: null,
    origId: null,      // 当前作品在服务端的 id（改 id 时用它发请求）
    view: 'work',      // work | site
    tab: 'basic',      // basic | media | gallery | music
    query: '',
    filter: 'all',
    dirty: false,
    pwGenerated: false,
  };

  const work = () => S.works.find((w) => w.id === S.sel) || null;
  const sorted = () => S.works.slice().sort((a, b) => (Number(a.sortOrder) || 0) - (Number(b.sortOrder) || 0));

  /* ---------------- API ---------------- */

  async function api(method, path, body) {
    const headers = {};
    if (S.token) headers['Authorization'] = 'Bearer ' + S.token;
    let payload;
    if (body !== undefined) {
      headers['Content-Type'] = 'application/json';
      payload = JSON.stringify(body);
    }
    const res = await fetch(path, { method, headers, body: payload });
    if (res.status === 401) { logout(true); throw new Error('登录已过期，请重新登录'); }
    const text = await res.text();
    let data = {};
    try { data = text ? JSON.parse(text) : {}; } catch { data = { error: text }; }
    if (!res.ok) throw new Error(data.error || ('请求失败 ' + res.status));
    return data;
  }

  /** 原始二进制上传（避免 multipart） */
  async function upload(file, target) {
    const res = await fetch('/api/upload', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + S.token,
        'x-filename': encodeURIComponent(file.name),
        'x-target': target || 'uploads',
        'Content-Type': 'application/octet-stream',
      },
      body: file,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || '上传失败');
    return data; // { path, kind, size, name }
  }

  function pickFiles(accept, multiple) {
    return new Promise((resolve) => {
      const inp = document.createElement('input');
      inp.type = 'file';
      if (accept) inp.accept = accept;
      if (multiple) inp.multiple = true;
      inp.style.display = 'none';
      document.body.appendChild(inp);
      inp.addEventListener('change', () => {
        const files = Array.from(inp.files || []);
        inp.remove();
        resolve(files);
      });
      inp.click();
    });
  }

  /** 素材库选择器：列出该作品目录 / assets/site 下的已有文件 */
  async function pickMedia(target) {
    let files = [];
    let dir = '';
    try {
      const r = await api('GET', '/api/media?target=' + encodeURIComponent(target || 'uploads'));
      files = r.files || [];
      dir = r.dir;
    } catch (e) { toast(e.message, true); return null; }

    return new Promise((resolve) => {
      const host = $('#modalHost');
      host.innerHTML = `
        <div class="modal"><div class="modal__box" style="max-width:680px">
          <h3>选择素材</h3>
          <p style="margin:0 0 14px;color:var(--muted);font-size:12px">目录 ${esc(dir)} · 共 ${files.length} 个文件</p>
          <div style="max-height:56vh;overflow:auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:8px">
            ${files.length ? files.map((f) => `
              <button class="btn" style="height:auto;padding:6px;display:grid;gap:6px;justify-items:stretch" data-pick="${esc(f.path)}" title="${esc(f.name)} · ${sizeText(f.size)}">
                ${f.kind === 'image'
                  ? `<img src="/${esc(f.path)}" style="width:100%;height:62px;object-fit:cover;border-radius:3px" loading="lazy">`
                  : `<span class="badge" style="justify-self:center">${esc(f.kind)}</span>`}
                <span style="font-size:10px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(f.name)}</span>
              </button>`).join('') : '<div class="empty">该目录暂无文件，可直接上传</div>'}
          </div>
          <div class="modal__ops" style="margin-top:16px">
            <button class="btn" data-m="cancel">取消</button>
          </div>
        </div></div>`;

      const close = (v) => { host.innerHTML = ''; resolve(v); };
      host.querySelector('[data-m="cancel"]').onclick = () => close(null);
      host.querySelectorAll('[data-pick]').forEach((b) => { b.onclick = () => close(b.dataset.pick); });
    });
  }

  /* ---------------- 登录 ---------------- */

  function logout(silent) {
    if (!silent && S.token) api('POST', '/api/logout').catch(() => {});
    S.token = '';
    localStorage.removeItem('jun.admin.token');
    $('#app').classList.add('is-hidden');
    $('#login').classList.remove('is-hidden');
    $('#pwHint').textContent = '密码保存在服务端 content/auth.json（首次启动时生成并打印在控制台）';
  }

  async function doLogin(pw) {
    const r = await api('POST', '/api/login', { password: pw });
    S.token = r.token;
    localStorage.setItem('jun.admin.token', r.token);
    S.pwGenerated = !!r.passwordIsGenerated;
    await boot();
  }

  /* ---------------- 启动 ---------------- */

  async function boot() {
    try {
      const st = await api('GET', '/api/state');
      S.works = st.works || [];
      S.site = st.site || {};
      S.pwGenerated = S.pwGenerated || st.passwordIsGenerated;
      $('#login').classList.add('is-hidden');
      $('#app').classList.remove('is-hidden');
      if (!S.sel && S.works.length) { S.sel = sorted()[0].id; S.origId = S.sel; }
      renderAll();
      if (S.pwGenerated) {
        toast('当前使用首次启动自动生成的密码，建议修改 content/auth.json 后重启服务', true);
      }
    } catch (e) {
      logout(true);
      $('#loginMsg').textContent = e.message === '登录已过期，请重新登录' ? '' : e.message;
    }
  }

  /* ---------------- 渲染：统计 & 列表 ---------------- */

  function renderStats() {
    const pub = S.works.filter((w) => w.status !== 'draft').length;
    const draft = S.works.length - pub;
    const byCat = {};
    S.works.forEach((w) => { byCat[w.category] = (byCat[w.category] || 0) + 1; });
    $('#stats').innerHTML =
      `<span class="badge badge--ok">已发布 ${pub}</span>` +
      (draft ? `<span class="badge badge--draft">草稿 ${draft}</span>` : '') +
      `<span class="badge">共 ${S.works.length}</span>`;
    $('#stats').title = Object.entries(byCat)
      .map(([k, v]) => `${CATS.find((c) => c[0] === k)?.[1] || k} ${v}`).join(' · ');
  }

  function renderFilters() {
    const items = [['all', '全部'], ['published', '已发布'], ['draft', '草稿'],
      ...CATS.filter((c) => S.works.some((w) => w.category === c[0])).map((c) => [c[0], c[1]])];
    $('#filters').innerHTML = items.map(([id, label]) =>
      `<button class="btn btn--sm${S.filter === id ? ' btn--primary' : ''}" data-filter="${id}">${esc(label)}</button>`
    ).join('');
  }

  function visibleWorks() {
    const q = S.query.trim().toLowerCase();
    return sorted().filter((w) => {
      if (S.filter === 'published' && w.status === 'draft') return false;
      if (S.filter === 'draft' && w.status !== 'draft') return false;
      if (!['all', 'published', 'draft'].includes(S.filter) && w.category !== S.filter) return false;
      if (!q) return true;
      return [w.id, w.year, w.title?.zh, w.title?.en, w.title?.es]
        .some((v) => String(v || '').toLowerCase().includes(q));
    });
  }

  function renderList() {
    const list = visibleWorks();
    const host = $('#list');
    if (!list.length) { host.innerHTML = '<div class="empty">没有匹配的作品</div>'; return; }
    const idxAll = sorted();
    host.innerHTML = list.map((w) => {
      const i = idxAll.indexOf(w);
      const draft = w.status === 'draft';
      const thumb = isVideo(w.cover) ? (w.videoPoster || '') : w.cover;
      return `
      <div class="item${w.id === S.sel && S.view === 'work' ? ' is-active' : ''}" data-id="${esc(w.id)}">
        <span class="item__no">${String(w.sortOrder || i + 1).padStart(2, '0')}</span>
        ${thumb
          ? `<img class="item__thumb" src="/${esc(thumb)}" alt="" loading="lazy">`
          : '<span class="item__thumb"></span>'}
        <div class="item__body">
          <div class="item__title">${esc(w.title?.zh || w.id)}</div>
          <div class="item__meta">
            <span>${esc(w.year || '—')}</span>
            ${draft ? '<span class="badge badge--draft">草稿</span>' : ''}
            ${w.mediaType === 'video' ? '<span class="badge badge--video">视频</span>' : ''}
            ${w.single ? '<span class="badge">单列</span>' : ''}
          </div>
        </div>
        <div class="item__ops">
          <button data-op="up" title="上移">▲</button>
          <button data-op="down" title="下移">▼</button>
          <button data-op="del" title="删除" style="color:var(--danger)">✕</button>
        </div>
      </div>`;
    }).join('');
  }

  function renderAll() { renderStats(); renderFilters(); renderList(); renderPane(); }

  /* ---------------- 渲染：右侧面板 ---------------- */

  function renderPane() {
    const pane = $('#pane');
    if (S.view === 'site') { pane.innerHTML = sitePaneHtml(); return; }
    const w = work();
    if (!w) {
      pane.innerHTML = `<div class="empty">左侧选择或新建一个作品<br><br>
        <button class="btn btn--primary" data-act="new">+ 新建作品</button></div>`;
      return;
    }
    pane.innerHTML = workPaneHtml(w);
  }

  function tabsHtml(w) {
    const t = (id, label) => `<button class="tab${S.tab === id ? ' is-active' : ''}" data-tab="${id}">${label}</button>`;
    const draft = w.status === 'draft';
    return `<div class="tabs">
        ${t('basic', '基本信息')}
        ${t('media', '封面与媒体')}
        ${t('gallery', `详情页图集 <span class="badge">${(w.gallery || []).length}</span>`)}
        ${t('music', '背景音乐')}
      </div>
      <div class="note">
        ${draft
          ? '当前是 <b>草稿</b>：不会出现在站点上。改为「已发布」并保存后即可上线。'
          : '当前 <b>已发布</b>：保存后站点数据立即重写（assets/js/data.js）。'}
        作品详情页：<a href="/work-detail.html?id=${esc(w.id)}" target="_blank" rel="noopener">/work-detail.html?id=${esc(w.id)} ↗</a>
      </div>`;
  }

  function langField(label, objKey, val, hint, rows) {
    return `
      <div class="section">
        <h4 class="section__title">${esc(label)}${hint ? ` <span class="field__hint">${esc(hint)}</span>` : ''}</h4>
        <div class="field">
          ${LANGS.map(([l, ln]) => `
            <div class="copyrow__lang">
              <span class="copyrow__langlabel">${ln}</span>
              ${rows
                ? `<textarea class="textarea" data-lang="${l}" data-key="${objKey}" style="min-height:${rows}px">${esc(val?.[l] || '')}</textarea>`
                : `<input class="input" data-lang="${l}" data-key="${objKey}" value="${esc(val?.[l] || '')}">`}
            </div>`).join('')}
        </div>
      </div>`;
  }

  function workPaneHtml(w) {
    let body = '';
    if (S.tab === 'basic') body = basicTab(w);
    else if (S.tab === 'media') body = mediaTab(w);
    else if (S.tab === 'gallery') body = galleryTab(w);
    else body = musicTab(w);

    return `
      <header class="pane__head">
        <div>
          <h2 class="pane__title">${esc(w.title?.zh || w.id)}</h2>
          <div class="pane__sub">id: ${esc(w.id)} · sortOrder: ${w.sortOrder} · ${esc(w.category)}</div>
        </div>
        <div class="pane__actions">
          <label class="field__label" style="text-transform:none;letter-spacing:0">
            <input type="checkbox" data-field="status" ${w.status === 'draft' ? '' : 'checked'}> 已发布
          </label>
          <button class="btn btn--primary" data-act="save">保存</button>
          <button class="btn btn--danger" data-act="del">删除</button>
        </div>
      </header>
      ${tabsHtml(w)}
      <div id="tabBody">${body}</div>
    `;
  }

  /* ----- 基本信息 ----- */
  function basicTab(w) {
    return `
      <div class="section">
        <h4 class="section__title">标识</h4>
        <div class="grid3">
          <div class="field">
            <label class="field__label">作品 id <span class="field__hint">用于 URL 与素材目录</span></label>
            <input class="input input--mono" data-field="id" value="${esc(w.id)}">
          </div>
          <div class="field">
            <label class="field__label">分类</label>
            <select class="select" data-field="category">
              ${CATS.map(([id, label, hasFilter]) => `<option value="${id}"${w.category === id ? ' selected' : ''}>${esc(label)}${hasFilter ? '' : '（站点暂无筛选按钮）'}</option>`).join('')}
            </select>
          </div>
          <div class="field">
            <label class="field__label">年份</label>
            <input class="input" data-field="year" value="${esc(w.year)}" placeholder="如 2018 / 2016 — 至今">
          </div>
        </div>
        <div class="grid2" style="margin-top:12px">
          <div class="field">
            <label class="field__label">排序 sortOrder <span class="field__hint">数字越小越靠前</span></label>
            <input class="input" type="number" data-field="sortOrder" value="${esc(w.sortOrder)}">
          </div>
          <div class="field">
            <label class="field__label">图集布局</label>
            <label class="field__hint" style="display:flex;gap:6px;align-items:center;height:32px">
              <input type="checkbox" data-field="single" ${w.single ? 'checked' : ''}> 单列无缝排列（切图复原，不启用瀑布流）
            </label>
          </div>
        </div>
      </div>

      ${langField('标题 title', 'title', w.title, '卡片与详情页大标题')}
      ${langField('类型 type', 'type', w.type, '卡片上「类型 · 年份」的短标签')}
      ${langField('范围 scope', 'scope', w.scope, '详情页「设计范围」一行')}
      ${langField('说明 blurb', 'blurb', w.blurb, '详情页导语，空行可分段', 110)}
    `;
  }

  /* ----- 封面与媒体 ----- */
  function mediaTab(w) {
    const isVid = w.mediaType === 'video';
    return `
      <div class="section">
        <h4 class="section__title">首屏媒体形态</h4>
        <div class="field">
          <label class="field__label">类型</label>
          <select class="select" data-field="mediaType" style="max-width:280px">
            <option value="image"${!isVid ? ' selected' : ''}>图片（使用封面图）</option>
            <option value="video"${isVid ? ' selected' : ''}>视频（首屏播放视频）</option>
          </select>
          <span class="field__hint">选「视频」后，详情页首屏显示视频，用 Poster 作为视频封面。</span>
        </div>
      </div>

      <div class="grid--side">
        <div class="section">
          <h4 class="section__title">封面 cover</h4>
          <div class="media-preview">
            ${w.cover
              ? (isVideo(w.cover)
                ? `<video src="/${esc(w.cover)}" muted playsinline preload="metadata"></video>`
                : `<img src="/${esc(w.cover)}" alt="">`)
              : '<span class="media-preview__empty">未设置封面</span>'}
          </div>
          <div class="media-actions">
            <button class="btn btn--sm" data-act="up-cover">上传图片</button>
            <button class="btn btn--sm" data-act="pick-cover">从素材库选</button>
            <button class="btn btn--sm btn--danger" data-act="clear-cover">清除</button>
          </div>
          <div class="field" style="margin-top:10px">
            <label class="field__label">路径 / URL</label>
            <input class="input input--mono" data-field="cover" value="${esc(w.cover)}">
          </div>
        </div>

        ${isVid ? `
        <div class="section">
          <h4 class="section__title">视频 video</h4>
          <div class="media-preview">
            ${w.video ? `<video src="/${esc(w.video)}" muted playsinline preload="metadata" controls></video>`
              : '<span class="media-preview__empty">未设置视频</span>'}
          </div>
          <div class="media-actions">
            <button class="btn btn--sm" data-act="up-video">上传视频</button>
            <button class="btn btn--sm btn--danger" data-act="clear-video">清除</button>
          </div>
          <div class="field" style="margin-top:10px">
            <label class="field__label">视频路径 / URL <span class="field__hint">mp4 / webm</span></label>
            <input class="input input--mono" data-field="video" value="${esc(w.video || '')}">
          </div>
          <div class="field" style="margin-top:10px">
            <label class="field__label">视频 Poster <span class="field__hint">播放前显示的封面图</span></label>
            <input class="input input--mono" data-field="videoPoster" value="${esc(w.videoPoster || '')}">
          </div>
          <div class="media-actions">
            <button class="btn btn--sm" data-act="up-poster">上传 Poster</button>
            <button class="btn btn--sm" data-act="poster-from-cover">用封面图作为 Poster</button>
          </div>
          ${w.videoPoster ? `<div class="media-preview" style="margin-top:10px"><img src="/${esc(w.videoPoster)}" alt=""></div>` : ''}
        </div>` : ''}
      </div>

      <div class="section">
        <h4 class="section__title">素材库（本作品目录）</h4>
        <div class="media-actions">
          <button class="btn btn--sm" data-act="batch-media">批量上传到该作品目录</button>
          <span class="field__hint">上传后可在图集里引用；文件存放于 assets/works/${esc(w.id)}/</span>
        </div>
      </div>
    `;
  }

  /* ----- 图集 ----- */
  function galleryTab(w) {
    const g = w.gallery || [];
    const items = g.map((item, i) => {
      const isVid = typeof item === 'object' && item.type === 'video';
      const src = typeof item === 'string' ? item : item.src;
      const poster = typeof item === 'object' ? (item.poster || '') : '';
      return `
      <div class="gitem" draggable="true" data-gi="${i}">
        <span class="gitem__handle" title="拖动排序">⠿</span>
        <span class="item__no">${String(i + 1).padStart(2, '0')}</span>
        ${isVid
          ? (poster ? `<img class="gitem__thumb" src="/${esc(poster)}" alt="">` : '<span class="gitem__thumb" style="display:grid;place-items:center;font-size:10px;color:#9a9a9a">VIDEO</span>')
          : (isImage(src) ? `<img class="gitem__thumb" src="/${esc(src)}" alt="">` : '<span class="gitem__thumb"></span>')}
        <div class="gitem__body">
          <div class="gitem__row">
            <select class="select" data-gtype="${i}" style="max-width:110px">
              <option value="image"${isVid ? '' : ' selected'}>图片</option>
              <option value="video"${isVid ? ' selected' : ''}>视频</option>
            </select>
            <input class="input input--mono" data-gsrc="${i}" value="${esc(src)}" placeholder="assets/... 或完整 URL">
          </div>
          ${isVid ? `<div class="gitem__row">
            <input class="input input--mono" data-gposter="${i}" value="${esc(poster)}" placeholder="视频 Poster（可选）">
          </div>` : ''}
        </div>
        <div class="gitem__ops">
          <button class="btn btn--sm" data-gop="up" data-gi="${i}" title="上移">▲</button>
          <button class="btn btn--sm" data-gop="down" data-gi="${i}" title="下移">▼</button>
          <button class="btn btn--sm" data-gop="replace" data-gi="${i}" title="上传替换">⇪</button>
          <button class="btn btn--sm btn--danger" data-gop="del" data-gi="${i}" title="删除">✕</button>
        </div>
      </div>`;
    }).join('');

    return `
      <div class="section">
        <div class="media-actions" style="margin-top:0">
          <button class="btn btn--primary btn--sm" data-act="g-add-files">+ 上传图片 / 视频</button>
          <button class="btn btn--sm" data-act="g-add-empty">+ 添加空项（填 URL）</button>
          <span class="field__hint">共 ${g.length} 项 · 可拖动整行排序</span>
        </div>
      </div>
      <div class="gallery-list" id="galleryList">
        ${items || '<div class="empty">图集为空</div>'}
      </div>
    `;
  }

  /* ----- 背景音乐 ----- */
  function musicTab(w) {
    return `
      <div class="section">
        <h4 class="section__title">作品背景音乐</h4>
        <div class="note">留空即不播放。填入音频路径或完整 URL 后，详情页会出现播放按钮（默认不自动播放，避免浏览器拦截）。</div>
        <div class="field">
          <label class="field__label">音频路径 / URL</label>
          <input class="input input--mono" data-field="bgm" value="${esc(w.bgm || '')}" placeholder="assets/uploads/xxx.mp3 或 https://...">
        </div>
        <div class="media-actions">
          <button class="btn btn--sm" data-act="up-bgm">上传音频</button>
          <button class="btn btn--sm btn--danger" data-act="clear-bgm">清除</button>
        </div>
        ${w.bgm ? `<audio src="/${esc(w.bgm)}" controls style="margin-top:12px;width:100%"></audio>` : ''}
      </div>
    `;
  }

  /* ----- 站点设置 ----- */
  function sitePaneHtml() {
    const s = S.site || {};
    const src = s.source || { mode: 'local', apiBase: '', sanity: {} };
    const bgm = s.bgm || {};

    const groups = COPY_GROUPS.map((grp) => {
      const keys = grp.keys || Object.keys(s.copy || {}).filter((k) => k.startsWith(grp.prefix));
      const rows = keys.map((k) => `
        <div class="copyrow">
          <div class="copyrow__key">${esc(COPY_LABELS[k] || k)} <span style="color:var(--muted-2)">${esc(k)}</span></div>
          ${LANGS.map(([l, ln]) => `
            <div class="copyrow__lang">
              <span class="copyrow__langlabel">${ln}</span>
              <input class="input" data-copy="${esc(k)}" data-lang="${l}" value="${esc((s.copy?.[k] || {})[l] || '')}">
            </div>`).join('')}
        </div>`).join('');
      return `<details class="card" style="margin-bottom:12px" open>
        <summary style="cursor:pointer;font-size:13px;font-weight:500">${esc(grp.title)} <span class="field__hint">${keys.length} 条</span></summary>
        <div style="margin-top:12px">${rows || '<div class="empty">无</div>'}</div>
      </details>`;
    }).join('');

    return `
      <header class="pane__head">
        <div>
          <h2 class="pane__title">站点设置</h2>
          <div class="pane__sub">主页文案 · 社交链接 · 音乐 · 数据源</div>
        </div>
        <div class="pane__actions">
          <button class="btn btn--primary" data-act="save-site">保存站点设置</button>
        </div>
      </header>

      <div class="section">
        <h4 class="section__title">社交入口（主页 + 页脚）</h4>
        <div id="socialList">
          ${(s.social || []).map((item, i) => `
            <div class="rowcard" data-si="${i}">
              <div class="rowcard__head">
                <span class="badge">${esc(item.id)}</span>
                <span class="field__hint">${esc(item.i18nKey || '自定义')}</span>
                <span class="rowcard__spacer"></span>
                <button class="btn btn--sm btn--danger" data-act="del-social" data-si="${i}">删除</button>
              </div>
              <div class="field" style="margin-bottom:8px">
                <label class="field__label">链接 URL</label>
                <input class="input input--mono" data-social-url="${i}" value="${esc(item.url)}" placeholder="https://... 或 mailto:...">
              </div>
              <div class="grid3">
                ${LANGS.map(([l, ln]) => `
                  <div class="field">
                    <label class="field__label">${ln} 文字</label>
                    <input class="input" data-social-label="${i}" data-lang="${l}" value="${esc((item.label || {})[l] || '')}">
                  </div>`).join('')}
              </div>
            </div>`).join('')}
        </div>
        <button class="btn btn--sm" data-act="add-social">+ 新增社交入口</button>
      </div>

      <div class="section">
        <h4 class="section__title">主页 / 页脚文案</h4>
        <div class="note">修改后保存 → 重写 <b>assets/js/site-data.js</b>，并在页面加载时覆盖 i18n 中的同名字段。三语各自独立，留空的语种仍回落到 i18n 原值。</div>
        ${groups}
      </div>

      <div class="section">
        <h4 class="section__title">站点背景音乐</h4>
        <div class="grid--side">
          <div class="rowcard">
            <div class="rowcard__head"><span class="rowcard__title">全局音乐</span><span class="rowcard__spacer"></span>
              <label class="field__hint" style="display:flex;gap:6px;align-items:center">
                <input type="checkbox" data-bgm="enabled" ${bgm.enabled ? 'checked' : ''}> 启用
              </label>
            </div>
            <div class="field" style="margin-bottom:8px">
              <label class="field__label">音频路径 / URL</label>
              <input class="input input--mono" data-bgm="src" value="${esc(bgm.src || '')}">
            </div>
            <div class="grid2">
              <label class="field__hint" style="display:flex;gap:6px;align-items:center">
                <input type="checkbox" data-bgm="autoplay" ${bgm.autoplay ? 'checked' : ''}> 自动播放（多数浏览器会拦截）
              </label>
              <label class="field__hint" style="display:flex;gap:6px;align-items:center">
                <input type="checkbox" data-bgm="loop" ${bgm.loop ? 'checked' : ''}> 循环
              </label>
            </div>
          </div>
          <div class="rowcard">
            <div class="rowcard__head"><span class="rowcard__title">音乐标题</span></div>
            ${LANGS.map(([l, ln]) => `
              <div class="copyrow__lang">
                <span class="copyrow__langlabel">${ln}</span>
                <input class="input" data-bgm-title="${l}" value="${esc((bgm.title || {})[l] || '')}">
              </div>`).join('')}
          </div>
        </div>
      </div>

      <div class="section">
        <h4 class="section__title">数据源与兜底</h4>
        <div class="note">
          站点默认读取内置 <b>assets/js/data.js</b>。若选择远端数据源，页面会先尝试拉取，
          <b>失败或未配置时自动回退本地 data.js</b>，站点不会空白。
        </div>
        <div class="grid3">
          <div class="field">
            <label class="field__label">模式</label>
            <select class="select" data-source="mode">
              <option value="local"${src.mode === 'local' ? ' selected' : ''}>local · 仅用本地 data.js</option>
              <option value="api"${src.mode === 'api' ? ' selected' : ''}>api · 自建接口</option>
              <option value="sanity"${src.mode === 'sanity' ? ' selected' : ''}>sanity · Sanity 项目</option>
            </select>
          </div>
          <div class="field">
            <label class="field__label">API 地址 <span class="field__hint">返回 {works:[…]}</span></label>
            <input class="input input--mono" data-source="apiBase" value="${esc(src.apiBase || '')}" placeholder="https://.../api/content">
          </div>
          <div class="field">
            <label class="field__label">Sanity Project ID</label>
            <input class="input input--mono" data-source="sanity.projectId" value="${esc((src.sanity || {}).projectId || '')}">
          </div>
          <div class="field">
            <label class="field__label">Sanity Dataset</label>
            <input class="input input--mono" data-source="sanity.dataset" value="${esc((src.sanity || {}).dataset || '')}">
          </div>
          <div class="field">
            <label class="field__label">Sanity API 版本</label>
            <input class="input input--mono" data-source="sanity.apiVersion" value="${esc((src.sanity || {}).apiVersion || '')}">
          </div>
        </div>
      </div>
    `;
  }

  /* ---------------- 交互：侧栏 ---------------- */

  $('#list').addEventListener('click', async (e) => {
    const item = e.target.closest('.item');
    if (!item) return;
    const id = item.dataset.id;
    const opBtn = e.target.closest('button[data-op]');
    if (opBtn) {
      const op = opBtn.dataset.op;
      if (op === 'del') return confirmDelete(id);
      return moveWork(id, op === 'up' ? -1 : 1);
    }
    if (S.dirty && !confirm('当前修改尚未保存，确定切换？')) return;
    S.dirty = false;
    S.sel = id; S.origId = id; S.view = 'work'; S.tab = 'basic';
    renderAll();
  });

  $('#search').addEventListener('input', (e) => { S.query = e.target.value; renderList(); });
  $('#filters').addEventListener('click', (e) => {
    const b = e.target.closest('button[data-filter]');
    if (!b) return;
    S.filter = b.dataset.filter;
    renderFilters(); renderList();
  });

  async function moveWork(id, dir) {
    const list = sorted().map((w) => w.id);
    const i = list.indexOf(id);
    const j = i + dir;
    if (i < 0 || j < 0 || j >= list.length) return;
    [list[i], list[j]] = [list[j], list[i]];
    try {
      await api('POST', '/api/works/reorder', { ids: list });
      list.forEach((wid, k) => { const w = S.works.find((x) => x.id === wid); if (w) w.sortOrder = k + 1; });
      renderAll();
      toast('顺序已更新');
    } catch (err) { toast(err.message, true); }
  }

  /* ---------------- 交互：右侧面板 ---------------- */

  $('#pane').addEventListener('click', async (e) => {
    const tab = e.target.closest('.tab');
    if (tab) {
      saveDraftToState();
      S.tab = tab.dataset.tab;
      renderPane();
      return;
    }
    const btn = e.target.closest('button[data-act]');
    if (btn) return handleAction(btn.dataset.act, btn, e);
    const gop = e.target.closest('button[data-gop]');
    if (gop) return galleryOp(gop.dataset.gop, Number(gop.dataset.gi));
  });

  // 表单输入 → 同步到内存（不重渲染，避免打断输入）
  $('#pane').addEventListener('input', (e) => {
    const t = e.target;
    const w = work();
    if (!w) return;
    if (t.dataset.lang && t.dataset.key) {
      w[t.dataset.key] = w[t.dataset.key] || {};
      w[t.dataset.key][t.dataset.lang] = t.value;
      S.dirty = true;
      if (t.dataset.key === 'title') { renderList(); renderStats(); }
      return;
    }
    if (t.dataset.field !== undefined) {
      const f = t.dataset.field;
      if (f === 'status') w.status = t.checked ? 'published' : 'draft';
      else if (f === 'single') w.single = t.checked;
      else if (f === 'sortOrder') w.sortOrder = Number(t.value) || 0;
      else w[f] = t.value;
      S.dirty = true;
      if (f === 'status' || f === 'sortOrder') { renderList(); renderStats(); }
      return;
    }
    if (t.dataset.gsrc !== undefined) { setG(Number(t.dataset.gsrc), t.value, null); S.dirty = true; }
    else if (t.dataset.gposter !== undefined) { setG(Number(t.dataset.gposter), null, t.value); S.dirty = true; }
  });

  $('#pane').addEventListener('change', (e) => {
    const t = e.target;
    const w = work();
    if (!w) return;
    if (t.dataset.gtype !== undefined) {
      const i = Number(t.dataset.gtype);
      const g = w.gallery[i];
      const src = typeof g === 'string' ? g : g.src;
      w.gallery[i] = t.value === 'video' ? { type: 'video', src, poster: '' } : src;
      S.dirty = true;
      renderPane();
      return;
    }
    if (t.dataset.field === 'mediaType') {
      w.mediaType = t.value; S.dirty = true; renderPane(); return;
    }
    if (t.dataset.field === 'category') { w.category = t.value; S.dirty = true; renderList(); return; }
    if (t.dataset.field === 'status' || t.dataset.field === 'single') {
      if (t.dataset.field === 'status') w.status = t.checked ? 'published' : 'draft';
      else w.single = t.checked;
      S.dirty = true; renderList(); renderStats(); return;
    }
    // 站点设置
    if (t.dataset.copy) { setCopy(t.dataset.copy, t.dataset.lang, t.value); return; }
    if (t.dataset.socialUrl !== undefined) { S.site.social[Number(t.dataset.socialUrl)].url = t.value; return; }
    if (t.dataset.socialLabel !== undefined) { S.site.social[Number(t.dataset.socialLabel)].label[t.dataset.lang] = t.value; return; }
    if (t.dataset.source) { setSource(t.dataset.source, t.value); return; }
    if (t.dataset.bgm) {
      const k = t.dataset.bgm;
      S.site.bgm[k] = t.type === 'checkbox' ? t.checked : t.value;
      return;
    }
  });

  // 站点面板是 input 型控件，另接一个 input 监听
  document.addEventListener('input', (e) => {
    const t = e.target;
    if (t.dataset && t.dataset.copy && t.tagName === 'INPUT') setCopy(t.dataset.copy, t.dataset.lang, t.value);
    if (t.dataset && t.dataset.socialUrl !== undefined && t.tagName === 'INPUT') S.site.social[Number(t.dataset.socialUrl)].url = t.value;
    if (t.dataset && t.dataset.socialLabel !== undefined && t.tagName === 'INPUT') S.site.social[Number(t.dataset.socialLabel)].label[t.dataset.lang] = t.value;
    if (t.dataset && t.dataset.source && t.tagName === 'INPUT') setSource(t.dataset.source, t.value);
    if (t.dataset && t.dataset.bgmTitle && t.tagName === 'INPUT') S.site.bgm.title[t.dataset.bgmTitle] = t.value;
    if (t.dataset && t.dataset.bgm && t.tagName === 'INPUT') S.site.bgm[t.dataset.bgm] = t.value;
  });

  function setCopy(key, lang, val) {
    S.site.copy[key] = S.site.copy[key] || {};
    S.site.copy[key][lang] = val;
  }
  function setSource(path, val) {
    const src = S.site.source;
    if (path.includes('.')) {
      const [, sub] = path.split('.');
      src.sanity = src.sanity || {};
      src.sanity[sub] = val;
    } else src[path] = val;
  }
  function setG(i, src, poster) {
    const w = work();
    const g = w.gallery[i];
    const obj = typeof g === 'string' ? { type: 'image', src: g, poster: '' } : g;
    if (src !== null) obj.src = src;
    if (poster !== null) obj.poster = poster;
    w.gallery[i] = obj.type === 'video' ? obj : obj.src;
  }

  function saveDraftToState() { /* 输入已实时写入 S，无需额外处理 */ }

  /* ---------------- 动作 ---------------- */

  async function handleAction(act, btn, ev) {
    const w = work();
    try {
      switch (act) {
        case 'new': return createWorkDialog();

        case 'save': {
          if (!w) return;
          const body = { ...w };
          const from = S.origId || w.id;
          const r = await api('PUT', '/api/works/' + encodeURIComponent(from), body);
          Object.assign(w, r.work);
          S.sel = w.id;
          S.origId = w.id;
          S.dirty = false;
          renderAll();
          toast('已保存' + (r.renameNote || '') + (r.stats ? ` · 站点数据已重写（${r.stats.published} 个已发布）` : ''));
          return;
        }

        case 'del': return confirmDelete(w.id);

        /* 封面 */
        case 'up-cover': {
          const [f] = await pickFiles('image/*');
          if (!f) return;
          btn.disabled = true; btn.textContent = '上传中…';
          const r = await upload(f, S.origId || w.id);
          w.cover = r.path; S.dirty = true; renderPane();
          toast('封面已上传，记得保存');
          return;
        }
        case 'pick-cover': {
          const p = await pickMedia(S.origId || w.id);
          if (p) { w.cover = p; S.dirty = true; renderPane(); toast('已选择封面，记得保存'); }
          return;
        }
        case 'clear-cover': w.cover = ''; S.dirty = true; renderPane(); return;

        /* 视频 */
        case 'up-video': {
          const [f] = await pickFiles('video/*');
          if (!f) return;
          btn.disabled = true; btn.textContent = '上传中…';
          const r = await upload(f, S.origId || w.id);
          w.video = r.path; w.mediaType = 'video'; S.dirty = true; renderPane();
          toast('视频已上传，记得保存');
          return;
        }
        case 'clear-video': w.video = ''; S.dirty = true; renderPane(); return;

        /* Poster */
        case 'up-poster': {
          const [f] = await pickFiles('image/*');
          if (!f) return;
          btn.disabled = true; btn.textContent = '上传中…';
          const r = await upload(f, S.origId || w.id);
          w.videoPoster = r.path; S.dirty = true; renderPane();
          toast('Poster 已上传，记得保存');
          return;
        }
        case 'poster-from-cover': w.videoPoster = w.cover; S.dirty = true; renderPane(); return;

        /* 素材库批量上传 */
        case 'batch-media': {
          const files = await pickFiles('image/*,video/*', true);
          if (!files.length) return;
          btn.disabled = true;
          for (let i = 0; i < files.length; i++) {
            btn.textContent = `上传中 ${i + 1}/${files.length}…`;
            await upload(files[i], S.origId || w.id);
          }
          toast(`已上传 ${files.length} 个文件到 assets/works/${w.id}/`);
          renderPane();
          return;
        }

        /* 图集 */
        case 'g-add-files': {
          const files = await pickFiles('image/*,video/*', true);
          if (!files.length) return;
          btn.disabled = true;
          for (let i = 0; i < files.length; i++) {
            btn.textContent = `上传中 ${i + 1}/${files.length}…`;
            const r = await upload(files[i], S.origId || w.id);
            w.gallery = w.gallery || [];
            w.gallery.push(r.kind === 'video' ? { type: 'video', src: r.path, poster: '' } : r.path);
          }
          S.dirty = true; renderPane();
          toast(`已追加 ${files.length} 项，记得保存`);
          return;
        }
        case 'g-add-empty': w.gallery = w.gallery || []; w.gallery.push(''); S.dirty = true; renderPane(); return;

        case 'up-bgm': {
          const [f] = await pickFiles('audio/*');
          if (!f) return;
          btn.disabled = true; btn.textContent = '上传中…';
          const r = await upload(f, 'site');
          w.bgm = r.path; S.dirty = true; renderPane();
          toast('音频已上传，记得保存');
          return;
        }
        case 'clear-bgm': w.bgm = ''; S.dirty = true; renderPane(); return;

        /* 站点设置 */
        case 'save-site': {
          const r = await api('PUT', '/api/site', S.site);
          S.site = r.site;
          renderPane();
          toast('站点设置已保存 · site-data.js 已重写');
          return;
        }
        case 'add-social': {
          S.site.social = S.site.social || [];
          S.site.social.push({ id: 'custom' + (S.site.social.length + 1), url: '', label: { zh: '', es: '', en: '' }, i18nKey: '' });
          renderPane();
          return;
        }
        case 'del-social': {
          const i = Number(ev.target.dataset.si);
          S.site.social.splice(i, 1);
          renderPane();
          return;
        }
        default:
          return;
      }
    } catch (e) {
      toast(e.message, true);
      if (btn) { btn.disabled = false; }
      renderPane();
    }
  }

  /* ----- 图集操作 ----- */
  async function galleryOp(op, i) {
    const w = work();
    const g = w.gallery;
    if (!w || !g) return;
    if (op === 'up' && i > 0) { [g[i - 1], g[i]] = [g[i], g[i - 1]]; }
    else if (op === 'down' && i < g.length - 1) { [g[i + 1], g[i]] = [g[i], g[i + 1]]; }
    else if (op === 'del') { g.splice(i, 1); }
    else if (op === 'replace') {
      const [f] = await pickFiles('image/*,video/*');
      if (!f) return;
      try {
        const r = await upload(f, S.origId || w.id);
        g[i] = r.kind === 'video' ? { type: 'video', src: r.path, poster: '' } : r.path;
      } catch (e) { return toast(e.message, true); }
    } else return;
    S.dirty = true;
    renderPane(); renderStats();
  }

  // 拖拽排序
  let dragFrom = null;
  $('#pane').addEventListener('dragstart', (e) => {
    const row = e.target.closest('.gitem');
    if (!row) return;
    dragFrom = Number(row.dataset.gi);
    row.classList.add('is-dragging');
  });
  $('#pane').addEventListener('dragend', (e) => {
    const row = e.target.closest('.gitem');
    if (row) row.classList.remove('is-dragging');
  });
  $('#pane').addEventListener('dragover', (e) => {
    if (dragFrom === null) return;
    e.preventDefault();
  });
  $('#pane').addEventListener('drop', (e) => {
    const row = e.target.closest('.gitem');
    if (!row || dragFrom === null) return;
    e.preventDefault();
    const w = work();
    const to = Number(row.dataset.gi);
    if (to === dragFrom || isNaN(to)) return;
    const [moved] = w.gallery.splice(dragFrom, 1);
    w.gallery.splice(to, 0, moved);
    dragFrom = null;
    S.dirty = true;
    renderPane();
  });

  /* ---------------- 新建 / 删除 ---------------- */

  function dialog(title, bodyHtml, onOk, okLabel) {
    const host = $('#modalHost');
    host.innerHTML = `
      <div class="modal">
        <div class="modal__box">
          <h3>${esc(title)}</h3>
          ${bodyHtml}
          <div class="modal__ops">
            <button class="btn" data-m="cancel">取消</button>
            <button class="btn btn--primary" data-m="ok">${esc(okLabel || '确定')}</button>
          </div>
        </div>
      </div>`;
    const close = () => { host.innerHTML = ''; };
    host.querySelector('[data-m="cancel"]').onclick = close;
    host.querySelector('[data-m="ok"]').onclick = async () => { await onOk(host); };
  }

  function createWorkDialog() {
    dialog('新建作品', `
      <div class="field" style="margin-bottom:10px">
        <label class="field__label">作品 id <span class="field__hint">小写英文，用于 URL 与素材目录</span></label>
        <input class="input input--mono" id="nwId" placeholder="my-new-work">
      </div>
      <div class="field" style="margin-bottom:10px">
        <label class="field__label">中文标题</label>
        <input class="input" id="nwTitle" placeholder="作品名称">
      </div>
      <div class="grid2">
        <div class="field">
          <label class="field__label">分类</label>
          <select class="select" id="nwCat">${CATS.map(([id, l]) => `<option value="${id}">${esc(l)}</option>`).join('')}</select>
        </div>
        <div class="field">
          <label class="field__label">年份</label>
          <input class="input" id="nwYear" placeholder="2026">
        </div>
      </div>`, async (host) => {
      const id = host.querySelector('#nwId').value.trim();
      const title = host.querySelector('#nwTitle').value.trim();
      const category = host.querySelector('#nwCat').value;
      const year = host.querySelector('#nwYear').value.trim();
      if (!/^[a-z0-9][a-z0-9._-]*$/i.test(id)) return toast('id 只能包含字母、数字、. _ -', true);
      if (!title) return toast('请填写中文标题', true);
      const blank = { zh: '', es: '', en: '' };
      const body = {
        id, category, year, status: 'draft', sortOrder: S.works.length + 1,
        mediaType: 'image', cover: '', video: '', videoPoster: '', bgm: '', single: false,
        gallery: [],
        title: { ...blank, zh: title },
        type: { ...blank }, scope: { ...blank }, blurb: { ...blank },
      };
      try {
        const r = await api('POST', '/api/works', body);
        S.works.push(r.work);
        S.sel = r.work.id; S.view = 'work'; S.tab = 'basic';
        host.closest('.modal').remove();
        renderAll();
        toast('已创建（草稿），请继续完善并保存');
      } catch (e) { toast(e.message, true); }
    }, '创建');
  }

  function confirmDelete(id) {
    const w = S.works.find((x) => x.id === id);
    if (!w) return;
    const hasMedia = /^[\w.-]+$/.test(id);
    dialog(`删除作品「${w.title?.zh || id}」`, `
      <p>将从 content/works.json 中移除该作品，并立即重写站点数据。此操作不可撤销。</p>
      <label class="field__hint" style="display:flex;gap:8px;align-items:center">
        <input type="checkbox" id="delMedia" ${hasMedia ? '' : 'disabled'}>
        同时删除素材目录 assets/works/${esc(id)}/
      </label>`, async (host) => {
      const delMedia = host.querySelector('#delMedia').checked;
      try {
        const r = await api('DELETE', `/api/works/${encodeURIComponent(id)}?deleteMedia=${delMedia ? 1 : 0}`);
        S.works = S.works.filter((x) => x.id !== id);
        if (S.sel === id) S.sel = S.works.length ? sorted()[0].id : null;
        host.closest('.modal').remove();
        renderAll();
        toast('已删除' + (r.mediaNote ? r.mediaNote : ''));
      } catch (e) { toast(e.message, true); }
    }, '确认删除');
  }

  /* ---------------- 顶栏 ---------------- */

  $('#btnSync').addEventListener('click', async () => {
    try {
      const r = await api('POST', '/api/sync');
      toast(`已重写站点数据：${r.stats.published} 个已发布 / ${r.stats.draft} 个草稿`);
    } catch (e) { toast(e.message, true); }
  });

  $('#btnNew').addEventListener('click', createWorkDialog);
  $('#btnSiteSettings').addEventListener('click', () => {
    if (S.dirty && !confirm('当前修改尚未保存，确定离开？')) return;
    S.dirty = false;
    S.view = 'site';
    renderAll();
  });
  $('#btnLogout').addEventListener('click', () => logout(false));

  /* ---------------- 登录表单 ---------------- */

  $('#loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const pw = $('#pw').value;
    if (!pw) return;
    $('#loginBtn').disabled = true;
    $('#loginMsg').textContent = '';
    try {
      await doLogin(pw);
      $('#pw').value = '';
    } catch (err) {
      $('#loginMsg').textContent = err.message;
    } finally {
      $('#loginBtn').disabled = false;
    }
  });

  // 离开前提示未保存
  window.addEventListener('beforeunload', (e) => {
    if (S.dirty) { e.preventDefault(); e.returnValue = ''; }
  });

  /* ---------------- 启动 ---------------- */

  if (S.token) boot(); else logout(true);
})();
