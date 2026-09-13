#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性脚本：把 i18n.js 里的 resume.* 文案结构化为 content/resume.json。

运行：python3 _tools/seed_resume.py
（已执行完毕，保留以便日后重建种子）
"""
import io, json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODE = "/Users/jamchou/.workbuddy/binaries/node/versions/22.22.2-3/bin/node"
LANGS = ["zh", "es", "en"]

# 1) 用 node 读 i18n.js，导出三语 resume.* 词条
dump = subprocess.run(
    [NODE, "-e", """
global.window={};
require('./assets/js/i18n.js');
const I=window.I18N, langs=['zh','es','en'];
const out={};
Object.keys(I.zh).filter(k=>k.startsWith('resume.')).forEach(k=>{
  out[k]={}; langs.forEach(l=>out[k][l]=(I[l]||{})[k]||'');
});
console.log(JSON.stringify(out));
"""],
    cwd=ROOT, capture_output=True, text=True, check=True)
T = json.loads(dump.stdout)


def L(key):
    return {l: T.get(key, {}).get(l, "") for l in LANGS}


def bullets(prefix, n=4):
    out = []
    for i in range(1, n + 1):
        v = L(f"{prefix}.l{i}")
        if any(v.values()):
            out.append(v)
    return out


resume = {
    "version": 1,
    "updatedAt": "2026-09-13T00:00:00.000Z",
    "head": {
        "eyebrow": L("resume.eyebrow"),
        "title": L("resume.title"),
        "lead": L("resume.lead"),
    },
    "pdfs": [
        {"id": "zh", "file": "assets/docs/JUN-CV-ZH.pdf", "enabled": True, "label": L("resume.download.zh")},
        {"id": "es", "file": "assets/docs/JUN-CV-ES.pdf", "enabled": True, "label": L("resume.download.es")},
        {"id": "en", "file": "assets/docs/JUN-CV-EN.pdf", "enabled": True, "label": L("resume.download.en")},
    ],
    "summary": {"title": L("resume.summary.title"), "body": L("resume.summary.body")},
    "exp": {
        "title": L("resume.exp.title"),
        "items": [
            {"title": L("resume.exp.1.t"), "org": L("resume.exp.1.org"),
             "date": L("resume.exp.1.date"), "bullets": bullets("resume.exp.1")},
            {"title": L("resume.exp.2.t"), "org": L("resume.exp.2.org"),
             "date": L("resume.exp.2.date"), "bullets": bullets("resume.exp.2")},
            {"title": L("resume.exp.3.t"), "org": L("resume.exp.3.org"),
             "date": L("resume.exp.3.date"), "bullets": bullets("resume.exp.3")},
        ],
    },
    "edu": {
        "title": L("resume.edu.title"),
        "items": [{"title": L("resume.edu.t"), "org": L("resume.edu.org"), "date": L("resume.edu.date")}],
    },
    "skills": {"title": L("resume.skills.title"), "items": bullets("resume.skills", 6)},
    "certs": {"title": L("resume.cert.title"), "items": bullets("resume.cert", 1)},
}

out = os.path.join(ROOT, "content", "resume.json")
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(resume, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("已写入", out)
print("经历", len(resume["exp"]["items"]), "段 · 技能", len(resume["skills"]["items"]),
      "条 · 认证", len(resume["certs"]["items"]), "条 · PDF", len(resume["pdfs"]), "个")
