#!/usr/bin/env python3
"""
content/weekNN.json + design-system/ → docs/weekNN/index.html
모든 자산(reveal.js·CSS)을 한 파일에 인라인 → GitHub Pages & 오프라인 더블클릭 모두 작동.
디자인은 design-system/(Claude Design+DesignSync)에서 오고, 콘텐츠는 content/에서 온다.
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVEAL = ROOT / "node_modules" / "reveal.js"
DS = ROOT / "design-system"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def notes(slide) -> str:
    n = slide.get("notes")
    return f'<aside class="notes">{esc(n)}</aside>' if n else ""


def lines(body) -> str:
    return "".join(f"<p>{esc(t)}</p>" for t in body)


# --- 아키타입별 렌더러 (계약: design-system 클래스 이름에 의존) ---
def r_title(s, meta):
    return f"""<section data-phase="{meta['phase']}">
<div class="slide-band"></div>
<span class="kicker">{esc(f"Phase {meta['phase']} · {meta['week']}주차")}</span>
<h1>{esc(meta['title'])}</h1>
<p class="subtitle">{esc(meta.get('subtitle',''))}</p>
{notes(s)}</section>"""


def r_basic(s, kind):
    return f"""<section>
<div class="slide-band"></div>
<span class="kicker">{esc(s.get('kicker',''))}</span>
<h2>{esc(s['h'])}</h2>
<div class="{kind}">{lines(s.get('body',[]))}</div>
{notes(s)}</section>"""


def r_proof(s, _):
    steps = ""
    for st in s["steps"]:
        cls = "step contra" if st["kind"] == "contra" else "step"
        steps += f'<div class="{cls}">{esc(st["t"])}</div>'
    return f"""<section>
<div class="slide-band"></div>
<span class="kicker">{esc(s.get('kicker',''))}</span>
<h2>{esc(s['h'])}</h2>
<div class="proof-flow">{steps}</div>
{notes(s)}</section>"""


def r_truth(s, _):
    head = "".join(f"<th>{esc(h)}</th>" for h in s["head"])
    rows = ""
    for row in s["rows"]:
        marks = row.get("marks", [""] * len(row["cells"]))
        tds = "".join(
            f'<td class="{m}">{esc(c)}</td>' for c, m in zip(row["cells"], marks)
        )
        rows += f'<tr class="{"win" if row.get("win") else ""}">{tds}</tr>'
    return f"""<section>
<div class="slide-band"></div>
<span class="kicker">{esc(s.get('kicker',''))}</span>
<h2>{esc(s['h'])}</h2>
<table class="truth"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>
{notes(s)}</section>"""


def r_reveal_concept(s, _):
    return f"""<section data-phase-reveal>
<div class="slide-band"></div>
<span class="kicker">{esc(s.get('kicker',''))}</span>
<h2>{esc(s['h'])}</h2>
<div class="reveal-box"><div class="concept">{esc(s['concept'])}</div></div>
<div class="body">{lines(s.get('body',[]))}</div>
{notes(s)}</section>"""


def r_end(s, _):
    return '<section data-phase><div class="slide-band"></div><h1>끝</h1></section>'


RENDER = {
    "title": r_title,
    "warmup": lambda s, m: r_basic(s, "warmup"),
    "problem": lambda s, m: r_basic(s, "problem"),
    "setup": lambda s, m: r_basic(s, "setup"),
    "solution": lambda s, m: r_basic(s, "solution"),
    "practice": lambda s, m: r_basic(s, "practice"),
    "proof-flow": r_proof,
    "truth-table": r_truth,
    "concept-reveal": r_reveal_concept,
    "end": r_end,
}


def build(week_json: Path):
    data = json.loads(read(week_json))
    meta = {k: data[k] for k in ("week", "phase", "title")}
    meta["subtitle"] = data.get("subtitle", "")

    sections = []
    for s in data["slides"]:
        fn = RENDER.get(s["type"])
        if not fn:
            sys.exit(f"unknown slide type: {s['type']}")
        sections.append(fn(s, meta) if s["type"] == "title" else fn(s, meta))

    css = "\n".join([
        read(REVEAL / "dist" / "reset.css"),
        read(REVEAL / "dist" / "reveal.css"),
        read(DS / "tokens.css"),
        read(DS / "components" / "components.css"),
        ".reveal .subtitle{color:var(--ink-soft);font-size:1.1em}"
        ".reveal section{padding:0 1.5em}",
    ])
    reveal_js = read(REVEAL / "dist" / "reveal.js")
    notes_js = read(REVEAL / "plugin" / "notes" / "notes.js")

    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(meta['title'])}</title>
<style>{css}</style></head>
<body data-phase="{meta['phase']}">
<div class="reveal"><div class="slides">
{chr(10).join(sections)}
</div></div>
<script>{reveal_js}</script>
<script>{notes_js}</script>
<script>
Reveal.initialize({{hash:true, slideNumber:'c/t', width:1280, height:720,
  margin:0.06, plugins:[RevealNotes]}});
</script>
</body></html>"""

    out_dir = ROOT / "docs" / f"week{meta['week']:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.html"
    out.write_text(doc, encoding="utf-8")
    return out, len(data["slides"])


def write_index():
    """docs/index.html — 전체 주차 목록 랜딩."""
    weeks = []
    for wj in sorted((ROOT / "content").glob("week*.json")):
        d = json.loads(read(wj))
        weeks.append((d["week"], d["phase"], d["title"]))
    items = "".join(
        f'<li><a href="week{w:02d}/" data-phase="{p}">'
        f'<b>{w}주차</b> {esc(t)}</a></li>'
        for w, p, t in weeks
    )
    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>논리퍼즐 수업</title><style>
body{{font-family:system-ui,"Noto Sans KR",sans-serif;max-width:720px;margin:3rem auto;padding:0 1rem;color:#0f172a}}
h1{{letter-spacing:-.02em}} ul{{list-style:none;padding:0}}
li a{{display:block;padding:.9rem 1.1rem;margin:.4rem 0;border:1px solid #e2e8f0;border-radius:10px;text-decoration:none;color:inherit;border-left:6px solid #4f46e5}}
li a[data-phase="2"]{{border-left-color:#0d9488}} li a[data-phase="3"]{{border-left-color:#d97706}} li a[data-phase="4"]{{border-left-color:#7c3aed}}
li a:hover{{background:#f8fafc}}
</style></head><body><h1>논리퍼즐 수업 — 슬라이드</h1>
<p>각 주차를 열고 <kbd>F</kbd> 전체화면, <kbd>S</kbd> 발표자 노트.</p>
<ul>{items}</ul></body></html>"""
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "index.html").write_text(doc, encoding="utf-8")
    print(f"built docs/index.html  ({len(weeks)} weeks)")


if __name__ == "__main__":
    targets = sys.argv[1:] or sorted((ROOT / "content").glob("week*.json"))
    for t in targets:
        out, n = build(Path(t))
        print(f"built {out.relative_to(ROOT)}  ({n} slides)")
    write_index()
