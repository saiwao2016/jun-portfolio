/* =========================================================
   JUN Portfolio — Main script
   i18n · nav · works grid · filter · form · reveal · active link
   ========================================================= */

(function () {
  'use strict';

  const root = document.documentElement;
  const STORAGE_KEY = 'jun.lang';
  const FALLBACK_LANG = 'zh';

  /* 资源版本号：每次发布若有同名文件被覆盖，需递增，避免 CDN/浏览器缓存旧资源 */
  const ASSET_V = 'v20260920';
  function vUrl(u) {
    if (!u) return u;
    return u + (u.indexOf('?') >= 0 ? '&' : '?') + ASSET_V;
  }

  /** 作品链接：作品可自带 href（定制专题页，如 work-pingyuan-calendar.html），
      否则走通用详情页 work-detail.html?id=… */
  function workHref(w) {
    if (w && w.href) return w.href + '?' + ASSET_V;
    return 'work-detail.html?id=' + encodeURIComponent(w.id) + '&' + ASSET_V;
  }

  /* ---------- 站点设置（assets/js/site-data.js，由后台 /admin 生成） ---------- */
  const SITE = (window.SITE_DATA && typeof window.SITE_DATA === 'object') ? window.SITE_DATA : {};

  /** 后台保存的主页 / 页脚文案覆盖 i18n；某语种留空则保留 i18n 原值 */
  function applySiteCopy() {
    const copy = SITE.copy || {};
    Object.keys(copy).forEach((key) => {
      ['zh', 'es', 'en'].forEach((lang) => {
        const v = copy[key] && copy[key][lang];
        if (v === undefined || v === null || v === '') return;
        if (!window.I18N[lang]) return;
        window.I18N[lang][key] = v;
      });
    });
  }

  /* ---------- 二维码弹层：社交入口可选「链接」或「二维码图片」 ---------- */

  let qrEl = null;

  function ensureQr() {
    if (qrEl) return qrEl;
    const el = document.createElement('div');
    el.className = 'qr-overlay';
    el.id = 'qrOverlay';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'true');
    el.innerHTML =
      '<div class="qr-overlay__box">' +
        '<button class="qr-overlay__close" type="button" aria-label="关闭">&times;</button>' +
        '<img class="qr-overlay__img" id="qrImg" alt="QR code" decoding="async">' +
        '<p class="qr-overlay__label" id="qrLabel"></p>' +
        '<p class="qr-overlay__hint" id="qrHint"></p>' +
        '<a class="qr-overlay__open" id="qrOpen" href="#" target="_blank" rel="noopener"></a>' +
      '</div>';
    document.body.appendChild(el);
    el.addEventListener('click', (e) => {
      if (e.target === el || e.target.closest('.qr-overlay__close')) closeQr();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && el.classList.contains('is-on')) closeQr();
    });
    qrEl = el;
    return el;
  }

  function t18n(key, fallback) {
    const dict = window.I18N && window.I18N[getLang()];
    return (dict && dict[key]) || fallback || '';
  }

  function openQr(item) {
    const el = ensureQr();
    const lang = getLang();
    el.querySelector('#qrImg').src = vUrl(item.qr);
    el.querySelector('#qrLabel').textContent = (item.label && item.label[lang]) || '';
    el.querySelector('#qrHint').textContent = t18n('qr.hint', '长按二维码识别，扫码添加好友');
    const openA = el.querySelector('#qrOpen');
    if (item.url && /^https?:/i.test(item.url)) {
      openA.href = item.url;
      openA.textContent = t18n('qr.open', '在浏览器中打开图片');
      openA.style.display = '';
    } else {
      openA.removeAttribute('href');
      openA.style.display = 'none';
    }
    el.classList.add('is-on');
    document.body.classList.add('is-qr-open');
    const btn = el.querySelector('.qr-overlay__close');
    if (btn) btn.focus();
  }

  function closeQr() {
    if (!qrEl) return;
    qrEl.classList.remove('is-on');
    document.body.classList.remove('is-qr-open');
  }

  /** 社交入口：把后台配置的链接 / 二维码与文案写到带 data-social 的锚点上 */
  function applySocial() {
    const social = Array.isArray(SITE.social) ? SITE.social : [];
    if (!social.length) return;
    const byId = {};
    social.forEach((it) => { byId[it.id] = it; });

    const sync = () => {
      const lang = getLang();
      document.querySelectorAll('[data-social]').forEach((a) => {
        const it = byId[a.getAttribute('data-social')];
        if (!it) return;
        const asQr = it.kind === 'qr' && !!it.qr;
        if (asQr) {
          a.setAttribute('href', '#');
          a.setAttribute('role', 'button');
          a.setAttribute('aria-haspopup', 'dialog');
          a.setAttribute('data-qr', it.qr);
          a.classList.add('has-qr');
          const label = (it.label && it.label[lang]) || '';
          if (label) a.setAttribute('aria-label', label + ' · QR');
          if (!a.dataset.qrBound) {
            a.dataset.qrBound = '1';
            a.addEventListener('click', (ev) => { ev.preventDefault(); openQr(it); });
          }
        } else if (it.url) {
          a.setAttribute('href', it.url);
        }
        // 带 data-i18n 的锚点文字由 i18n（已被 copy 覆盖）负责，其余在此写入
        if (!a.hasAttribute('data-i18n')) {
          const label = it.label && it.label[lang];
          if (label) a.textContent = label;
        }
      });
    };
    sync();
    onLangChange(sync);
  }

  /* ---------- 内容源：远端优先，失败或未配置一律回退本地 data.js ---------- */
  const isVideoPath = (p) => /\.(mp4|webm|mov|m4v)$/i.test(p || '');

  function fetchWithTimeout(url, ms) {
    if (typeof AbortController === 'undefined') return fetch(url);
    const ac = new AbortController();
    const t = setTimeout(() => ac.abort(), ms);
    return fetch(url, { signal: ac.signal }).finally(() => clearTimeout(t));
  }

  function normalizeGallery(list) {
    return (list || [])
      .map((it) => (typeof it === 'string'
        ? { type: isVideoPath(it) ? 'video' : 'image', src: it, poster: '' }
        : { type: (it && it.type) || 'image', src: it && it.src, poster: (it && it.poster) || '' }))
      .filter((it) => !!it.src);
  }

  /** 草稿过滤 + sortOrder 排序 + 字段补全 */
  function normalizeWorks(list) {
    const arr = (list || []).filter((w) => w && w.id && w.status !== 'draft');
    if (arr.some((w) => w.sortOrder !== undefined && w.sortOrder !== null)) {
      arr.sort((a, b) => (Number(a.sortOrder) || 0) - (Number(b.sortOrder) || 0));
    }
    return arr.map((w) => ({
      ...w,
      title: w.title || {},
      type: w.type || {},
      scope: w.scope || {},
      blurb: w.blurb || {},
      gallery: normalizeGallery(w.gallery),
    }));
  }

  /** Sanity 文档 → 站点作品结构 */
  function fromSanity(d) {
    return {
      id: d.id || String(d._id || '').replace(/^drafts\./, ''),
      category: d.category, year: d.year, cover: d.cover,
      gallery: d.gallery || [], mediaType: d.mediaType, video: d.video,
      videoPoster: d.videoPoster, bgm: d.bgm, single: d.single,
      sortOrder: d.sortOrder, status: d.status,
      title: d.title, type: d.type, scope: d.scope, blurb: d.blurb,
    };
  }

  async function loadContent() {
    const src = SITE.source || { mode: 'local' };
    let remote = null;
    try {
      if (src.mode === 'sanity' && src.sanity && src.sanity.projectId) {
        const ds = src.sanity.dataset || 'production';
        const av = src.sanity.apiVersion || '2024-01-01';
        const q = encodeURIComponent('*[_type=="work"]|order(sortOrder asc)');
        const r = await fetchWithTimeout(
          `https://${src.sanity.projectId}.api.sanity.io/v${av}/data/query/${ds}?query=${q}`, 6000);
        const j = await r.json();
        remote = (j.result || []).map(fromSanity);
      } else if (src.mode === 'api' && src.apiBase) {
        const r = await fetchWithTimeout(src.apiBase, 6000);
        const j = await r.json();
        remote = Array.isArray(j) ? j : (j.works || []);
      }
    } catch (err) {
      // 兜底：远端失败静默回退本地 data.js，站点照常渲染
      console.warn('[content] 远端数据源不可用，已回退本地 data.js：', err && err.message);
      remote = null;
    }
    const list = (remote && remote.length) ? remote : (window.WORKS || []);
    window.WORKS = normalizeWorks(list);
    document.documentElement.setAttribute('data-content-source', remote ? src.mode : 'local');
  }

  /* ---------- 背景音乐 ---------- */
  function mountBgm(src, opts) {
    if (!src) return;
    const o = opts || {};
    const audio = document.createElement('audio');
    audio.src = decodeURI(src);
    audio.loop = o.loop !== false;
    audio.preload = 'none';

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'bgm-btn';
    btn.setAttribute('aria-label', o.label || '背景音乐');
    btn.innerHTML = '<span class="bgm-btn__ico">♪</span><span class="bgm-btn__txt"></span>';
    const txt = btn.querySelector('.bgm-btn__txt');

    document.body.appendChild(audio);
    document.body.appendChild(btn);

    let on = false;
    const sync = () => {
      btn.classList.toggle('is-on', on);
      txt.textContent = on ? (o.onText || '播放中') : (o.offText || '背景音乐');
    };
    sync();

    btn.addEventListener('click', () => {
      if (on) { audio.pause(); on = false; sync(); return; }
      audio.play().then(() => { on = true; sync(); }).catch(() => { on = false; sync(); });
    });
    if (o.autoplay) audio.play().then(() => { on = true; sync(); }).catch(() => {});
  }

  /** 详情页优先用作品音乐，其余页面用站点音乐 */
  function bindBgm() {
    const site = SITE.bgm || {};
    const host = document.querySelector('[data-work-detail]');
    let workBgm = '';
    if (host && window.WORKS && window.WORKS.length) {
      const id = new URLSearchParams(location.search).get('id');
      // 与详情页渲染保持一致：找不到 id 时回退第一个案例
      const w = window.WORKS.find((x) => x.id === id) || window.WORKS[0];
      workBgm = (w && w.bgm) || '';
    }
    if (workBgm) return mountBgm(workBgm, { label: '作品背景音乐' });
    if (site.enabled && site.src) {
      return mountBgm(site.src, { autoplay: !!site.autoplay, loop: site.loop !== false });
    }
  }

  /* ---------- Language ---------- */
  const langSubs = [];

  function getLang() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && window.I18N[saved]) return saved;
    return FALLBACK_LANG;
  }

  function onLangChange(fn) { langSubs.push(fn); }

  const HTML_LANG = { zh: 'zh-CN', es: 'es-ES', en: 'en' };

  function setLang(lang) {
    if (!window.I18N[lang]) return;
    localStorage.setItem(STORAGE_KEY, lang);
    root.setAttribute('lang', HTML_LANG[lang] || 'en');
    document.body.setAttribute('data-lang', lang);
    applyI18N(lang);
    syncLangSwitch(lang);
    if (typeof window.onLangChange === 'function') window.onLangChange(lang);
    langSubs.forEach((fn) => fn(lang));
  }

  function applyI18N(lang) {
    const dict = window.I18N[lang];
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      const val = dict[key];
      if (val === undefined) return;
      // 空值代表该项不适用（如未提供的年份）—— 整块隐藏，不留空行
      el.style.display = val === '' ? 'none' : '';
      if (val === '') return;
      // 支持极简强调 **粗体**；多行内容保留 \n。
      // 先整串转义，再把 **x** 放行成 <strong>，避免注入。
      const esc = escapeHtml(val);
      const rich = esc.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      if (val.indexOf('\n') !== -1) {
        el.innerHTML = rich.split('\n').join('<br>');
      } else if (rich !== esc) {
        el.innerHTML = rich;
      } else {
        el.textContent = val;
      }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
      const key = el.getAttribute('data-i18n-placeholder');
      const val = dict[key];
      if (val !== undefined) el.setAttribute('placeholder', val);
    });

    // <img data-i18n-alt="…">：图片替代文本随语言切换
    document.querySelectorAll('[data-i18n-alt]').forEach((el) => {
      const key = el.getAttribute('data-i18n-alt');
      const val = dict[key];
      if (val !== undefined) el.setAttribute('alt', val);
    });

    // <meta name="description" data-i18n-content="…"> 之类的属性型注入
    document.querySelectorAll('[data-i18n-content]').forEach((el) => {
      const key = el.getAttribute('data-i18n-content');
      const val = dict[key];
      if (val !== undefined) el.setAttribute('content', val);
    });
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  function syncLangSwitch(lang) {
    document.querySelectorAll('.lang-switch').forEach((el) => {
      el.querySelectorAll('.lang-switch__opt').forEach((o) => {
        o.classList.toggle('is-active', o.dataset.lang === lang);
      });
    });
  }

  function bindLangSwitch() {
    document.querySelectorAll('.lang-switch').forEach((el) => {
      el.addEventListener('click', (e) => {
        const opt = e.target.closest('.lang-switch__opt');
        if (!opt) return;
        setLang(opt.dataset.lang);
      });
    });
  }

  /* ---------- Nav scroll state & mobile toggle ---------- */
  function bindNav() {
    const nav = document.querySelector('.nav');
    if (!nav) return;

    const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 8);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    const toggle = nav.querySelector('.nav__toggle');
    if (toggle) {
      toggle.addEventListener('click', () => nav.classList.toggle('is-open'));
    }

    nav.querySelectorAll('.nav__link').forEach((link) => {
      link.addEventListener('click', () => nav.classList.remove('is-open'));
    });
  }

  /* ---------- Active nav link ---------- */
  function bindActiveLink() {
    const path = location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav__link').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href) return;
      if (href === path || (path === '' && href === 'index.html')) {
        link.classList.add('is-active');
      }
    });
  }

  /* ---------- Works grid render & filter ---------- */
  function renderWorks() {
    const grid = document.querySelector('[data-works-grid]');
    if (!grid || !window.WORKS) return;

    const lang = getLang();
    // 首页使用 data-works-featured：每个能力分类只取一个代表，共 6 个
    const featured = grid.hasAttribute('data-works-featured');
    let list = window.WORKS;
    if (featured) {
      const seen = new Set();
      list = window.WORKS.filter((w) => {
        if (seen.has(w.category)) return false;
        seen.add(w.category);
        return true;
      });
    }

    const frag = document.createDocumentFragment();

    list.forEach((w) => {
      const tagKey = 'works.tag.' + w.category;
      const tagText = window.I18N[lang][tagKey] || w.category;

      const card = document.createElement('a');
      card.className = 'work-card reveal';
      card.href = workHref(w);
      card.dataset.category = w.category;

      card.innerHTML = `
        <div class="work-card__media">
          <span class="work-card__tag">${escapeHtml(tagText)}</span>
          <img src="${escapeHtml(vUrl(w.cover))}" alt="${escapeHtml(w.title[lang])}" loading="lazy">
        </div>
        <div class="work-card__title" data-i18n-dyn="${w.id}__title">${escapeHtml(w.title[lang])}</div>
        <div class="work-card__meta">
          <span data-i18n-dyn="${w.id}__type">${escapeHtml(w.type[lang])}</span>
          <span> · ${w.year}</span>
        </div>
      `;
      frag.appendChild(card);
    });

    grid.appendChild(frag);
    onLangChange((lang) => {
      grid.querySelectorAll('.work-card').forEach((card) => {
        const w = window.WORKS.find((x) => card.href.includes(encodeURIComponent(x.id)));
        if (!w) return;
        const tEl = card.querySelector(`[data-i18n-dyn$="__title"]`);
        const tyEl = card.querySelector(`[data-i18n-dyn$="__type"]`);
        if (tEl) tEl.textContent = w.title[lang];
        if (tyEl) tyEl.textContent = w.type[lang];
      });
    });
  }

  function bindFilter() {
    const bar = document.querySelector('.filter-bar');
    const grid = document.querySelector('[data-works-grid]');
    if (!bar || !grid) return;

    bar.addEventListener('click', (e) => {
      const btn = e.target.closest('.filter-btn');
      if (!btn) return;
      bar.querySelectorAll('.filter-btn').forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');

      const cat = btn.dataset.filter;
      grid.querySelectorAll('.work-card').forEach((card) => {
        const show = cat === 'all' || card.dataset.category === cat;
        card.style.display = show ? '' : 'none';
      });
    });
  }

  /* ---------- Contact form ---------- */
  function bindForm() {
    const form = document.querySelector('[data-form]');
    if (!form) return;
    const msg = form.querySelector('.form-msg');
    const lang = getLang();

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());
      if (!data.name || !data.email || !data.message) return;

      // 占位：真实环境请 POST 到后端或邮件服务
      console.log('[JUN Portfolio] contact submit', data);
      if (msg) {
        msg.textContent = window.I18N[lang]['contact.form.success'];
        msg.classList.add('is-show');
      }
      form.reset();
      setTimeout(() => msg && msg.classList.remove('is-show'), 4500);
    });

    onLangChange((l) => {
      if (msg && msg.classList.contains('is-show')) {
        msg.textContent = window.I18N[l]['contact.form.success'];
      }
    });
  }

  /* ---------- Reveal on scroll （可重入：支持动态新增节点） ---------- */
  let revealObserver = null;

  function getRevealObserver() {
    if (revealObserver) return revealObserver;
    if (!('IntersectionObserver' in window)) return null;
    revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    return revealObserver;
  }

  function bindReveal(scope) {
    const ctx = scope || document;
    const els = ctx.querySelectorAll('.reveal:not(.is-in)');
    const io = getRevealObserver();
    if (!io) {
      els.forEach((el) => el.classList.add('is-in'));
      return;
    }
    els.forEach((el) => io.observe(el));
  }

  /* ---------- Work detail page ---------- */
  const SECTIONS = ['bg', 'process', 'system', 'summary'];

  function renderWorkDetail() {
    const host = document.querySelector('[data-work-detail]');
    if (!host || !window.WORKS) return;

    const params = new URLSearchParams(location.search);
    const id = params.get('id');
    const w = window.WORKS.find((x) => x.id === id) || window.WORKS[0];

    const idx = window.WORKS.indexOf(w);
    const nextW = window.WORKS[(idx + 1) % window.WORKS.length];
    const prevW = window.WORKS[(idx - 1 + window.WORKS.length) % window.WORKS.length];

    // 该作品有定制专题页时（如台历），旧链接直接送过去，避免同一作品两套详情并存
    if (w.href) { location.replace(workHref(w)); return; }

    // data.js 里写了的段落用真实内容，没写的用 i18n 模板兜底
    const real = {};
    (w.body || []).forEach((s) => { real[s.k] = s.p; });

    function para(lang, k) {
      const D = window.I18N[lang];
      if (real[k]) return real[k][lang];
      const key = k === 'bg' ? 'work.ph.bg2' : 'work.ph.' + k;
      return (D[key] || '').replace(/\{title\}/g, w.title[lang]);
    }

    function draw(lang) {
      const D = window.I18N[lang];
      const tag = D['works.tag.' + w.category] || w.category;
      document.title = 'JUN · ' + w.title[lang];

      const blocks = SECTIONS.map((k) => `
        <div class="work-body split">
          <aside><span class="eyebrow">${escapeHtml(D['work.section.' + k])}</span></aside>
          <div><p>${escapeHtml(para(lang, k))}</p></div>
        </div>`).join('');

      const media = w.gallery || [];
      const gallery = media.map((it, i) => (it.type === 'video'
        ? `<video src="${escapeHtml(vUrl(it.src))}"${it.poster ? ` poster="${escapeHtml(vUrl(it.poster))}"` : ''}
             controls playsinline preload="metadata" data-lb="${i}"></video>`
        : `<img src="${escapeHtml(vUrl(it.src))}" alt="${escapeHtml(w.title[lang])} ${i + 1}"
             loading="lazy" data-lb="${i}">`)).join('');

      // 说明文案允许用空行分段（\n\n → 多个段落），单段时保持原样
      const paras = String(w.blurb[lang] || '').split(/\n{2,}/)
        .map((s) => s.trim()).filter(Boolean);
      const blurbHtml = paras.map((p) => `<span class="blk">${escapeHtml(p)}</span>`).join('');
      const blurbCls = paras.length > 1 ? 'lead lead--multi' : 'lead';

      host.innerHTML = `
      <header class="work-hero container">
        <span class="eyebrow">${escapeHtml(tag)}</span>
        <h1 class="h-section" style="margin-top:8px;max-width:26ch">${escapeHtml(w.title[lang])}</h1>
        <p class="${blurbCls}" style="margin-top:24px">${blurbHtml}</p>
        <dl class="work-hero__meta">
          <div><dt>${escapeHtml(D['work.meta.type'])}</dt><dd>${escapeHtml(w.type[lang])}</dd></div>
          <div><dt>${escapeHtml(D['work.meta.year'])}</dt><dd>${escapeHtml(w.year)}</dd></div>
          <div><dt>${escapeHtml(D['work.meta.role'])}</dt><dd>${escapeHtml(D['work.meta.role.v'])}</dd></div>
        </dl>
      </header>

      <div class="container">
        <div class="work-cover${w.mediaType === 'video' && w.video ? ' is-video' : ''}">
          ${w.mediaType === 'video' && w.video
            ? `<video src="${escapeHtml(vUrl(w.video))}"${(w.videoPoster || w.cover) ? ` poster="${escapeHtml(vUrl(w.videoPoster || w.cover))}"` : ''}
                 controls playsinline preload="metadata"></video>`
            : (w.cover ? `<img src="${escapeHtml(vUrl(w.cover))}" alt="${escapeHtml(w.title[lang])}">` : '')}
        </div>

        <div class="work-scope">
          <span class="eyebrow">${escapeHtml(D['work.meta.scope'])}</span>
          <p>${escapeHtml(w.scope[lang])}</p>
        </div>

        ${blocks}

        <div class="work-body split">
          <aside>
            <span class="eyebrow">${escapeHtml(D['work.section.gallery'])}</span>
            <p class="muted" style="font-size:12px;margin-top:6px">
              ${escapeHtml((D['work.gallery.note'] || '').replace('{n}', String((w.gallery || []).length)))}
            </p>
          </aside>
          <div>
            <div class="work-gallery${w.single ? ' is-single' : ''}">${gallery}</div>
          </div>
        </div>

        <nav class="work-nav">
          <a href="${workHref(prevW)}">← ${escapeHtml(prevW.title[lang])}</a>
          <a href="works.html?${ASSET_V}">${escapeHtml(D['work.nav.back'])}</a>
          <a href="${workHref(nextW)}">${escapeHtml(nextW.title[lang])} →</a>
        </nav>
      </div>
    `;

      bindLightbox(w.gallery || []);
    }

    draw(getLang());
    onLangChange(draw);   // 语言切换时整页重绘
  }

  /* ---------- Gallery lightbox（图片 + 视频） ---------- */
  function bindLightbox(list, scope) {
    // 通用详情页的图集在 .work-gallery 内；定制专题页直接传整个文档
    const nodes = Array.from((scope || document).querySelectorAll('[data-lb]'));
    const items = (list || []).map((it) => (typeof it === 'string'
      ? { type: isVideoPath(it) ? 'video' : 'image', src: it, poster: '' }
      : it));
    if (!nodes.length || !items.length) return;

    let lb = document.getElementById('lb');
    if (!lb) {
      lb = document.createElement('div');
      lb.id = 'lb';
      lb.className = 'lb';
      document.body.appendChild(lb);
    }
    lb.innerHTML = '<img alt=""><video controls playsinline></video><span class="lb__cap"></span>';
    const lbImg = lb.querySelector('img');
    const lbVid = lb.querySelector('video');
    const lbCap = lb.querySelector('.lb__cap');
    const close = () => {
      lb.classList.remove('is-on');
      lbVid.pause();
      lbVid.removeAttribute('src');
    };
    // 只有点击背景或图片才关闭，避免误关视频控件
    lb.onclick = (e) => { if (e.target === lb || e.target === lbImg) close(); };

    let cur = 0;
    function show(i) {
      cur = (i + items.length) % items.length;
      const it = items[cur];
      const vid = it.type === 'video';
      lbImg.classList.toggle('is-hidden', vid);
      lbVid.classList.toggle('is-hidden', !vid);
      if (vid) {
        lbVid.src = vUrl(it.src);
        if (it.poster) lbVid.setAttribute('poster', vUrl(it.poster));
        else lbVid.removeAttribute('poster');
        lbVid.play().catch(() => {});
      } else {
        lbVid.pause();
        lbVid.removeAttribute('src');
        lbImg.src = vUrl(it.src);
      }
      // 说明文字取点击时的可见标题文本 —— 语言切换后自动是当前语言
      const capEl = it.capEl;
      const capTxt = capEl
        ? String(capEl.innerText || capEl.textContent || '').replace(/\s+/g, ' ').trim()
        : String(it.cap || '');
      lbCap.textContent = (cur + 1) + ' / ' + items.length + (capTxt ? ' · ' + capTxt : '');
    }

    nodes.forEach((im) => {
      im.addEventListener('click', () => {
        show(parseInt(im.dataset.lb, 10) || 0);
        lb.classList.add('is-on');
      });
    });

    document.onkeydown = (e) => {
      if (!lb.classList.contains('is-on')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
    };
  }

  /* ---------- 作品专题页（定制排版）----------
     部分作品有自己的专题页（如台历：可交互的分区块长页）。
     页面由 _tools/gen_pingyuan_page.py 生成，这里只接三件事：
     页内锚点 / 返回顶部 / 图集灯箱（同一张图在「平铺图」与「逐月」
     两个区块重复出现，必须按 src 去重，否则灯箱里会看到重复项）。 */
  function bindCustomWorkPage(host) {
    // 页内锚点
    host.querySelectorAll('[data-pc-scroll]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const t = document.getElementById(btn.getAttribute('data-pc-scroll'));
        if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });

    const top = host.querySelector('[data-pc-backtop]');
    if (top) top.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

    // 图集灯箱
    const imgs = Array.from(host.querySelectorAll('[data-pc-plate]'));
    if (imgs.length) {
      const items = [];
      const seen = Object.create(null);
      const capOf = (im) => {
        const card = im.closest('[data-pc-card]');
        return card && card.querySelector('[data-pc-cap]');
      };
      imgs.forEach((im) => {
        const src = im.getAttribute('src');
        if (!(src in seen)) {
          seen[src] = items.length;
          items.push({ type: 'image', src, capEl: capOf(im) });
        }
        im.setAttribute('data-lb', String(seen[src]));
      });
      bindLightbox(items);

      // 图片 alt 跟随当前语言（取图上标题文本，随切换器一起更新）
      const syncAlt = () => {
        imgs.forEach((im) => {
          const cap = capOf(im);
          if (cap) im.setAttribute('alt', String(cap.innerText || '').replace(/\s+/g, ' ').trim());
        });
      };
      syncAlt();
      onLangChange(syncAlt);
    }

    // 上一件 / 下一件
    const navWrap = document.querySelector('[data-pc-worknav]');
    const id = host.getAttribute('data-work-id');
    if (navWrap && id && window.WORKS && window.WORKS.length) {
      const i = window.WORKS.findIndex((w) => w.id === id);
      if (i >= 0) {
        const prev = window.WORKS[(i - 1 + window.WORKS.length) % window.WORKS.length];
        const next = window.WORKS[(i + 1) % window.WORKS.length];
        const pa = navWrap.querySelector('[data-pc-prev]');
        const na = navWrap.querySelector('[data-pc-next]');
        const drawNav = (lang) => {
          if (pa) { pa.textContent = '← ' + prev.title[lang]; pa.href = workHref(prev); }
          if (na) { na.textContent = next.title[lang] + ' →'; na.href = workHref(next); }
        };
        drawNav(getLang());
        onLangChange(drawNav);
      }
    }
  }

  /* ---------- Résumé page（数据驱动，内容来自 content/resume.json） ---------- */

  function resumeParas(text) {
    return String(text || '').split(/\n{2,}/).map((s) => s.trim()).filter(Boolean);
  }

  function renderResume() {
    const host = document.getElementById('resumeBody');
    const R = window.RESUME;
    if (!host || !R || typeof R !== 'object') return;  // 无数据 → 保留 HTML 静态兜底
    const lang = getLang();
    const L = (o) => String((o && (o[lang] || o.zh || o.en)) || '');
    const head = R.head || {};
    const h = [];

    // 页面标题
    if (L(head.eyebrow)) h.push(`<span class="eyebrow reveal">${escapeHtml(L(head.eyebrow))}</span>`);
    if (L(head.title)) h.push(`<h1 class="h-section reveal">${escapeHtml(L(head.title))}</h1>`);
    if (L(head.lead)) h.push(`<p class="lead reveal mt-5">${escapeHtml(L(head.lead))}</p>`);

    // PDF 下载
    const pdfs = (R.pdfs || []).filter((p) => p && p.file && p.enabled !== false);
    if (pdfs.length) {
      h.push('<div class="btn-row reveal">' + pdfs.map((p, i) => `
          <a href="${escapeHtml(p.file)}" download class="btn${i === 0 ? '' : ' btn--ghost'}">
            <span>${escapeHtml(L(p.label) || p.id || 'PDF')}</span>
            <span class="btn__arrow">↓</span>
          </a>`).join('') + '</div>');
    }

    // 个人简介（空行分段）
    const sum = R.summary || {};
    if (L(sum.body)) {
      const body = resumeParas(L(sum.body)).map((p) => `<p>${escapeHtml(p)}</p>`).join('');
      h.push(`<article class="resume-card mt-9 reveal">
        <h2 class="resume-card__title">${escapeHtml(L(sum.title))}</h2>
        <div class="resume-body muted">${body}</div>
      </article>`);
    }

    // 工作经历
    const exp = R.exp || {};
    const expItems = (exp.items || []).filter((it) => it && L(it.title));
    if (expItems.length) {
      h.push(`<h2 class="h-block reveal" style="margin-top:64px">${escapeHtml(L(exp.title))}</h2>`);
      expItems.forEach((it) => {
        const bl = (it.bullets || []).filter((b) => L(b));
        h.push(`<article class="resume-card reveal">
        <div class="resume-card__head">
          <div>
            <div class="resume-card__title">${escapeHtml(L(it.title))}</div>
            <div class="resume-card__org">${escapeHtml(L(it.org))}</div>
          </div>
          <div class="resume-card__date">${escapeHtml(L(it.date))}</div>
        </div>
        ${bl.length ? '<ul>' + bl.map((b) => `<li>${escapeHtml(L(b))}</li>`).join('') + '</ul>' : ''}
      </article>`);
      });
    }

    // 教育背景（条目对象：职位/学校 + 时间）
    const eduItems = ((R.edu || {}).items || []).filter((it) => it && L(it.title));
    if (eduItems.length) {
      h.push(`<h2 class="h-block reveal" style="margin-top:64px">${escapeHtml(L((R.edu || {}).title))}</h2>`);
      eduItems.forEach((it) => {
        h.push(`<article class="resume-card reveal">
        <div class="resume-card__head">
          <div>
            <div class="resume-card__title">${escapeHtml(L(it.title))}</div>
            <div class="resume-card__org">${escapeHtml(L(it.org))}</div>
          </div>
          <div class="resume-card__date">${escapeHtml(L(it.date))}</div>
        </div>
      </article>`);
      });
    }

    // 核心技能 / 资质认证（纯词条列表）
    [R.skills, R.certs].forEach((sec) => {
      if (!sec) return;
      const items = (sec.items || []).filter((b) => b && L(b));
      if (!items.length) return;
      h.push(`<h2 class="h-block reveal" style="margin-top:64px">${escapeHtml(L(sec.title))}</h2>`);
      h.push(`<article class="resume-card reveal"><ul>${items
        .map((b) => `<li>${escapeHtml(L(b))}</li>`).join('')}</ul></article>`);
    });

    host.innerHTML = h.join('\n');
    bindReveal(host);
  }

  /* ---------- Boot ---------- */
  document.addEventListener('DOMContentLoaded', async () => {
    applySiteCopy();      // 后台主页 / 页脚文案覆盖 i18n

    bindLangSwitch();
    bindNav();
    bindActiveLink();
    bindFilter();
    bindForm();

    await loadContent();  // 远端数据源优先，失败回退本地 data.js
    applySocial();

    // 先渲染动态内容，再统一挂 reveal 观察器，
    // 否则 JS 生成的卡片不会被 IntersectionObserver 观察到而永远 opacity:0
    renderWorks();
    renderWorkDetail();
    const customPage = document.querySelector('.pc[data-work-id]');
    if (customPage) bindCustomWorkPage(customPage);
    bindBgm();
    bindReveal();

    onLangChange(renderResume);   // 简历页：数据驱动，随语言切换重绘
    setLang(getLang());           // 最后一步，触发注入（同时首次渲染简历）
  });
})();