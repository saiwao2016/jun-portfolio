# 周骏 JUN · 个人作品集网站

视觉设计师个人官网。纯静态、零依赖、**中 / 西 / 英 三语一键切换**、100% 响应式。

极简黑白灰 + 低饱和暖棕点缀，无渐变堆砌、无弹窗、无水印。
内容全部基于**真实作品与真实履历**，无编造信息。

---

## 一、快速预览

```bash
cd portfolio-site
python3 -m http.server 8766
# 浏览器打开 http://127.0.0.1:8766
```

---

## 二、语言切换

右上角 `中 / ES / EN` 三段切换器，**一键切换，全站生效**。

- 选择写入 `localStorage['jun.lang']`，刷新和跨页保留
- 同步更新 `<html lang>`：`zh-CN` / `es-ES` / `en`
- 动态内容（作品卡片、案例详情整页）随语言重新渲染
- 语言标签本身不翻译（中 / ES / EN 三段式是通用写法）

三套字典都在 `assets/js/i18n.js`，键名完全一致，缺哪个语言补哪个语言的键值即可。

---

## 三、页面结构

| 文件 | 页面 | 说明 |
|---|---|---|
| `index.html` | 首页 | 首屏 + 精选案例（每板块 1 个）+ 能力结构 + 社交入口 |
| `works.html` | 作品集 | 全部案例 + 分类筛选（数字界面 / 原创 IP / 平面设计） |
| `work-detail.html?id=<案例id>` | 案例详情 | 动态渲染：背景 / 过程 / 规范 / 结果 + 图集（带灯箱） |
| `about.html` | 关于我 | 个人介绍 + 设计原则 + 三段真实经历时间线 + 能力优势 |
| `services.html` | 服务范围 | 六个可独立承接的板块 |
| `skills.html` | 技能体系 | 8 项专业能力 + 7 项工具 |
| `contact.html` | 联系方式 | 联系信息 + 留言表单 |
| `resume.html` | 简历 | 网页版简历 + 三语 PDF 下载 |

---

## 四、作品数据：**这一个文件就够**

所有案例内容都在 **`assets/js/data.js`**，改这个文件即可增删改案例，不用碰 HTML。

```js
{
  id: 'ruizhi-vi',              // 唯一标识，详情页 URL 用 ?id=ruizhi-vi
  category: 'brand',            // 六选一：brand | report | print | ip | digital | spatial
  year: '2020 — 2026',
  cover: 'assets/works/ruizhi-vi/01.jpg',   // 列表卡片封面
  gallery: [...],               // 详情页图集，数组里放图片路径
  title: { zh: '…', es: '…', en: '…' },     // 三语标题
  type:  { zh: '…', es: '…', en: '…' },     // 三语类型
  scope: { zh: '…', es: '…', en: '…' },     // 三语交付内容
  blurb: { zh: '…', es: '…', en: '…' },     // 三语简介
  body: [                       // 详情页正文段落，可只写部分，缺的自动用模板兜底
    { k: 'bg',      p: { zh: '…', es: '…', en: '…' } },
    { k: 'process', p: { … } },
    { k: 'system',  p: { … } },
    { k: 'summary', p: { … } },
  ],
}
```

**六个板块**（决定筛选标签与首页精选）：

| key | 中文 | Español | English |
|---|---|---|---|
| `brand` | 品牌系统 | Sistemas de marca | Brand systems |
| `report` | 报告与信息设计 | Informes e información | Reports & information |
| `print` | 画册与出版 | Editorial e impresión | Editorial & print |
| `ip` | 原创 IP 与插画 | IP original e ilustración | IP & illustration |
| `digital` | 数字界面 | Interfaces digitales | Digital interfaces |
| `spatial` | 包装与空间 | Packaging y espacio | Packaging & space |

> 首页"精选"逻辑：按数组顺序，每个板块取**第一个**案例。
> 想让某个案例上首页，把它挪到同板块第一个位置即可。
>
> ⚠️ **本文件现在是自动生成的**：数据改由内容后台维护（见第十二节），
> 真正的数据源是 `content/works.json`；手改 `assets/js/data.js` 会在下次保存时被覆盖。
> 早期撤出的 12 个案例仍在 `_archive/works-removed/`（可逆）。
> 新增案例时若用到新板块，记得同步 `works.html` 的筛选按钮与 `i18n.js` 的 `works.filter.*`。

---

## 五、替换作品图片

图片放在 `assets/works/<案例目录>/`，命名 `01.jpg`、`02.jpg`……
界面类案例用 `.png`（默认 1600px 宽、量化到 256 色，边缘比 JPEG 干净且体积相当）。

现有目录：

| 目录 | 内容 | 张数 | 格式 |
|---|---|---|---|
| `ruizhi-vi/` | 睿智云 VI 系统手册 | 44 | jpg |
| `ruizhi-report/` | 量表报告设计（抽样） | 12 | jpg |
| `ruizhi-manual/` | 睿智云产品手册 | 34 | jpg |
| `ruizhi-cert/` | 专业认证证书 | 2 | jpg |
| `rabbit-ip/` | 兔子 IP 形象 | 38 | jpg |
| `personal/` | 书法与插画创作 | 9 | jpg |
| `blood/` | 榴心社工品牌与 IP | 6 | jpg |
| `mzxc/` | MZXC 品牌视觉 | 3 | jpg |
| `asq-system/` | ASQ 儿童发育筛查系统界面 | 25 | png |
| `digital/` | 网站与移动端界面 | 3 | jpg |
| `editorial/` | 书籍画册封面 | 2 | jpg |
| `packaging/` | 包装与纪念品 | 2 | jpg |
| `spatial/` | 空间与环境 | 1 | jpg |

**换图建议**：宽 1400px、JPEG 质量 82 左右，单张控制在 200KB 内。
图集用瀑布流布局，**图片原始比例会被保留**（横竖混杂不会裁切），所以不用预先裁成统一比例。

### 从 `.sketch` 文件导出作品图（不用打开 Sketch）

Sketch 文件本质是 zip，本机装了 Sketch 就能用命令行导出画板，**不需要 Apple Events 权限**：

```bash
ST=/Applications/Sketch.app/Contents/MacOS/sketchtool

# 1) 看有哪些页面 / 画板（拿画板 ID）
"$ST" metadata "设计稿.sketch" > meta.json

# 2) 按 ID 导出画板，2 倍图 PNG
"$ST" export artboards "设计稿.sketch" \
  --output=./out --formats=png --scales=2 \
  --items="ID1,ID2,ID3" --use-id-for-name=YES
```

拿到 PNG 后按上面的规格压到 1600px 宽 + 256 色量化即可（`asq-system/` 就是这么来的）。
`--items` 不传会导出全部页面（含几百个组件画板），务必只传需要的 ID。

---

## 六、修改三语文案

除案例内容外，所有界面文案在 `assets/js/i18n.js`，结构是：

```js
window.I18N = {
  zh: { 'nav.home': '首页', … },
  es: { 'nav.home': 'Inicio', … },
  en: { 'nav.home': 'Home', … },
};
```

HTML 里写 `data-i18n="nav.home"` 就会自动注入对应语言的文本。

- **多行**：值里带 `\n` 会自动转成 `<br>`
- **空值**：值为 `''` 时该元素整块隐藏（例：未提供的毕业年份），不会留空行
- **表单占位符**：用 `data-i18n-placeholder="key"`

---

## 七、更新简历 PDF

三语简历由脚本生成，内容是独立维护的（不在 i18n 里）：

```bash
python3 _tools/gen_cv_pdf.py
# 输出 → assets/docs/JUN-CV-ZH.pdf / JUN-CV-ES.pdf / JUN-CV-EN.pdf
```

要改内容就编辑 `_tools/gen_cv_pdf.py` 里的 `build()` 函数。

> **字体坑**：脚本用的是 `~/Library/Fonts/HarmonyOS_Sans_SC_*.ttf`。
> 必须是 **TTF** —— 这台机器上渲染含中文的矢量 PDF 时，CFF/OTF 字体**会丢字形**。
> 换字体前先确认是 TTF，生成后务必渲染出来看一眼。

---

## 八、验证

```bash
# 先起服务
python3 -m http.server 8766

# 再跑验证（另开终端）
python3 _tools/verify.py
```

`_tools/verify.py` 会跑 **9 个页面 × 3 种语言**，逐屏滚动后断言：

- 零 JS 错误（含 console error 与 pageerror）
- 所有图片加载成功
- reveal 动画覆盖率 100%
- 语言切换器激活态 / `<html lang>` / localStorage 三者一致
- 无横向溢出
- 功能专项：首页精选 1 个、作品集 1 个、筛选各返回正确数量、图集 25 张、
  空提示默认隐藏（防 i18n 注入把 `display:none` 清掉）、
  灯箱打开/翻页/关闭、详情页语言切换重绘、简历页 3 个 PDF
- 移动端 390px 无横向溢出

截图输出到 `_tools/screens/`。

---

## 九、目录结构

```
portfolio-site/
├── index.html / works.html / work-detail.html
├── about.html / services.html / skills.html / contact.html / resume.html
├── server.js                 # 内容后台服务（静态托管 + /api，零依赖）
├── admin/                    # 后台界面（原生 JS）
├── content/                  # ← 内容数据源（works.json / site.json / auth.json）
├── assets/
│   ├── css/main.css          # 设计系统（:root 变量）
│   ├── js/
│   │   ├── i18n.js           # 三语字典（界面文案）
│   │   ├── data.js           # 作品数据（自动生成）
│   │   ├── site-data.js      # 主页文案 / 社交 / 音乐（自动生成）
│   │   └── main.js           # 语言切换 / 渲染 / 筛选 / 灯箱 / 动效
│   ├── works/                # 作品图 ← 换图
│   ├── docs/                 # 三语简历 PDF
│   └── images/               # favicon / logo
├── _tools/
│   ├── gen_cv_pdf.py         # 生成三语简历 PDF
│   ├── build_content.js      # content/*.json → data.js / site-data.js
│   ├── migrate_content.mjs   # 一次性迁移（从旧 data.js / i18n.js 提取）
│   ├── verify.py             # 三语全站回归验证
│   ├── verify_admin.py       # 后台端到端验证
│   ├── screenshot.py         # 截图
│   └── screens/              # 验证截图输出
└── _archive/                 # 早期占位素材（已不用，留档）
```

---

## 十、部署

纯静态，把整个 `portfolio-site/` 目录上传到任意静态托管即可（Vercel / Netlify / GitHub Pages / 对象存储 / 虚拟主机）。

无需构建步骤，无需 Node 环境。记得一起传：
- `assets/works/`（约 19MB）
- `assets/docs/`（三份 PDF）

---

## 十一、待办 / 需确认

- [x] **ASQ 案例年份**：已确认 —— `2016 — 至今`（2026-09-11 JUN 更正）。服务企业写为
      **深圳市心智心理测量技术研究所有限公司 · 珠海市海扬教育有限公司**
- [ ] **任职时间重叠（待确认）**：心智心测 / 海扬现已改为 `2016.06 — 至今`，
      与睿智云 `2019 — 至今` 并行 —— 简历上会出现两条「至今」。
      如果睿智云已离职，给我结束年份；如果是同时在做的两家，保持现状也行
- [ ] **ASQ 组件页（`asq-system/25.png`）**：该页示例文案是英文占位
      （`Add Project` / `Evan Yates` / `Backlog`…），像是基于现成 UI kit 改的。
      若确为第三方 kit，告诉我 —— 要么删掉这一张，要么在文案里注明来源
- [ ] **ASQ 未覆盖的模块**：侧栏还有「我的账户 / 评估课程 / 其他课程 / 家长端二维码」
      四项没导出对应界面。有稿就补，我可以直接加进图集
- [ ] **教育背景毕业年份**：本地资料未提供，目前留空（页面自动隐藏该项）
- [ ] **语言能力表述**：现为「中文母语 / English 工作 / Español 学习中」，请按实际情况调整
- [ ] **社交链接**：Behance 与小红书目前是空链接（`href="#"`），需要真实地址
- [x] ~~**旧作品集衍生图**~~：已按 JUN 要求把除 ASQ 外的 12 个作品全部撤出线上，
      图片移到 `_archive/works-removed/` 保留（含 `blood/` `mzxc/` `digital/`
      `editorial/` `packaging/` `spatial/` 六组旧 PDF 裁图）。要恢复就移回并补 `data.js`。
- [ ] **联系方式**：仅有邮箱 `saiwao@qq.com`；如需要可补电话 / 微信 / LinkedIn

---

## 十二、内容后台（`/admin`）

站点自带一个**零依赖内容后台**：`server.js` 只用 Node 内置模块，同时提供静态站点与 REST 接口；
管理界面在 `admin/`（原生 HTML/CSS/JS，无框架、无构建）。

### 启动

```bash
cd portfolio-site
node server.js                 # 默认 3000 端口
PORT=8080 node server.js       # 换端口
ADMIN_PASSWORD=自定义密码 node server.js
```

- 站点 → http://localhost:3000/
- 后台 → http://localhost:3000/admin

首次启动自动生成访问密码，**打印在控制台**并写入 `content/auth.json`。
忘了密码就看这个文件，或删掉它重启重新生成。站点本身是公开的，只有 `/admin` 与 `/api/*` 需要密码。

### 后台覆盖的能力

| # | 能力 | 在后台哪里 |
|---|---|---|
| 1 | 新增 / 删除作品 | 左侧「+ 新建作品」· 编辑器右上「删除」（可勾选一并删除素材目录） |
| 2 | 改标题、年份、分类、三语文案 | 基本信息（标题 / 类型 / 范围 / 说明，均可空行分段） |
| 3 | 图片 / 视频类型切换 | 封面与媒体 → 首屏媒体形态 |
| 4 | 更换封面、视频、视频 Poster | 封面与媒体（上传 / 素材库选取 / 直接填 URL / 清除） |
| 5 | 修改详情页媒体 | 详情页图集：上传、替换、删除、拖动整行排序，图片与视频可混排 |
| 6 | sortOrder 调整顺序 | 左侧条目 ▲▼ 按钮，或基本信息里的 sortOrder 数字 |
| 7 | 草稿与发布状态 | 编辑器右上「已发布」开关 —— **草稿不会出现在站点上** |
| 8 | 可选背景音乐 | 每个作品一个「背景音乐」，另有站点级音乐（站点设置） |
| 9 | 远端数据源 + 本地兜底 | 站点设置 → 数据源与兜底 |
| 10 | 主页文案与社交链接 | 站点设置 → 主页 / 页脚文案、社交入口 |

### 数据流

```
content/works.json ──┐
                     ├─ 保存时自动重写 ─→ assets/js/data.js       （站点作品数据）
content/site.json  ──┘                    assets/js/site-data.js （主页文案/社交/音乐/数据源）
```

- 保存即生效，无需构建。页面里 `data.js?h=…`、`site-data.js?h=…` 的查询串按**内容哈希**刷新，
  用来绕过 CDN 的同名文件缓存；与 `bump_version.py` 的 `ASSET_V` 互不干扰。
- 上传的素材落在 `assets/works/<作品id>/`，站点级素材落在 `assets/uploads/`、`assets/site/`。
- 作品改名会自动迁移素材目录，并改写所有指向旧目录的媒体路径。

### 数据源与兜底（第 9 条）

站点加载顺序是 **远端数据源（Sanity / 自建 API）→ 失败或未配置 → 本地 `data.js`**。
远端请求 6 秒超时即静默回退，`<html data-content-source>` 会标出本次实际生效的来源，
所以离线、断网、Sanity 挂掉时站点照常显示，不会白屏。

### 验证

```bash
python3 _tools/verify.py         # 站点：10 页 × 3 语言 + 功能专项 + 移动端
python3 _tools/verify_admin.py   # 后台：鉴权 / CRUD / 上传 / 视频 / 排序 / 改名 / 站点设置 / 兜底 / 界面
```

`verify_admin.py` 会自己拉起 `server.js`（默认 3199 端口），测试数据全部用 `zze2e-` 前缀，跑完自动清理。

### 部署

后台是 Node 服务，发布时的启动命令用：

```
node server.js        # 监听 $PORT，绑定 0.0.0.0
```

纯静态托管（GitHub Pages / 对象存储等）跑不了 `/api` 与 `/admin`，只能承载站点部分。

---

## 发布与缓存（重要）

站点发布在 `https://jun-portfolio.app.workbuddy.host/`，CDN 会按 URL（含查询串与压缩格式）分别缓存，
同名文件覆盖发布后，旧的缓存副本不会立刻失效。

**每次发布若有同名文件被覆盖，必须递增资源版本号 `vYYYYMMDD`：**

1. `assets/js/main.js` 顶部的 `const ASSET_V = 'v…'`；
2. 全部 `*.html` 里的资源引用与站内链接（`assets/css/main.css?v…`、`assets/js/*.js?v…`、`href="xxx.html?v…"`）；
3. `assets/js/main.js` 里动态生成的链接后缀（`work-detail.html?id=…&v…`、`works.html?v…`）。

可用 `_tools/bump_version.py`（若不存在则按上述三处手动全局替换）统一递增。
发布后用 `python3 -m http.server 8766` + `_tools/verify.py` 校验，再部署；部署后在**无痕窗口**打开
`https://jun-portfolio.app.workbuddy.host/index.html?v…` 确认案例数量与图片是否为最新。
