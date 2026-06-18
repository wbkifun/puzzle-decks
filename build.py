#!/usr/bin/env python3
"""
content/weekNN.json + design-system/ → docs/weekNN/index.html

· 디자인: design-system/(Claude Design + DesignSync) 의 tokens.css·components.css
· 콘텐츠: content/weekNN.json (디자인과 분리)
· 수식: KaTeX (CSS·JS·woff2 폰트까지 인라인 → 단일 파일에서도 안 깨짐)
· 브랜드 폰트(Pretendard·JetBrains): docs/_assets/fonts/ 공유 자산으로 상대 참조
  (Pages·오프라인 폴더에서 작동, 단일 파일 단독 복사 시엔 시스템 한글로 폴백)
콘텐츠의 수식은 $...$ (인라인) 또는 $$...$$ (디스플레이) 로 쓴다.
"""
import base64
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVEAL = ROOT / "node_modules" / "reveal.js"
KATEX = ROOT / "node_modules" / "katex" / "dist"
DS = ROOT / "design-system"
PHASE_NAME = {1: "논리와 추론", 2: "변수와 방정식", 3: "함수와 그래프", 4: "고급 개념의 씨앗"}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def esc(s: str) -> str:
    # &<> 만 엔티티화 → 브라우저가 textContent로 되돌리므로 KaTeX의 $...$ 는 보존됨
    return html.escape(s, quote=False)


def katex_css_inlined() -> str:
    """katex.min.css 의 woff2 폰트를 base64 data URI로 치환(단일 파일 보장)."""
    css = read(KATEX / "katex.min.css")

    def repl(m):
        name = m.group(1)
        data = base64.b64encode((KATEX / "fonts" / name).read_bytes()).decode()
        return f"url(data:font/woff2;base64,{data})"

    # woff2 만 data URI로; woff/ttf 대체 src는 그대로 둬도 woff2가 우선이라 fetch 안 됨
    return re.sub(r"url\(fonts/(KaTeX_[A-Za-z0-9_-]+\.woff2)\)", repl, css)


DECK_CSS = """
/* 실제 덱 레이아웃 (_frame.css 는 미리보기 전용이라 제외, 여기서 재현) */
.reveal .slides { height: 100%; }
.reveal .slides > section {
  box-sizing: border-box; width: 100%; height: 720px;
  padding: 60px 72px 56px;
  display: flex; flex-direction: column;
}
.reveal .slides > section.center-v { justify-content: center; }
.reveal .subtitle { color: var(--ink-soft); font-size: 1.1em; margin-top: .2em; }
.spacer { flex: 1 1 auto; }
/* 좌하단 풋노트 — 32주 내내 같은 자리 */
.slide-foot {
  position: absolute; left: 72px; bottom: 22px;
  font-family: var(--font-mono); font-size: .42em; letter-spacing: .1em;
  color: var(--ink-soft); text-transform: uppercase;
}
.slide-foot b { color: var(--phase-accent-ink); font-weight: 700; }
/* KaTeX 가 슬라이드 폰트 위계와 충돌하지 않게 */
.reveal .katex { font-size: 1.05em; }
"""


# ---------- 슬라이드 조각 ----------
def notes(s):
    n = s.get("notes")
    return f'<aside class="notes">{esc(n)}</aside>' if n else ""


def foot(meta):
    return (f'<div class="slide-foot"><b>W{meta["week"]:02d}</b> · '
            f'{esc(PHASE_NAME.get(meta["phase"], ""))}</div>')


def head_bits(s, meta, center=False):
    cls = ' class="center-v"' if center else ""
    kicker = (f'<span class="kicker">{esc(s["kicker"])}</span>'
              if s.get("kicker") else "")
    h = ""
    if s.get("h"):
        h = f'<h2>{esc(s["h"])}</h2>'
    return cls, kicker, h


def paras(body):
    return "".join(f"<p>{esc(t)}</p>" for t in body)


def leadq(s):
    return f'<p class="lead-q">{esc(s["q"])}</p>' if s.get("q") else ""


def trapbox(s):
    t = s.get("trap")
    if not t:
        return ""
    label = f'<span class="trap-label">{esc(t.get("label","흔한 함정"))}</span>'
    return f'<div class="trapbox">{label}{esc(t["text"])}</div>'


# ---------- 아키타입 렌더러 ----------
def r_title(s, meta):
    return f"""<section class="center-v">
<div class="slide-band"></div>
<span class="kicker">{esc(f'Phase {meta["phase"]} · {meta["week"]}주차')}</span>
<h1>{esc(meta['title'])}</h1>
<p class="subtitle">{esc(meta.get('subtitle',''))}</p>
{foot(meta)}{notes(s)}</section>"""


def r_basic(s, meta):
    cls, kicker, h = head_bits(s, meta)
    return f"""<section{cls}>
<div class="slide-band"></div>{kicker}{h}
<div class="stack">{paras(s.get('body',[]))}{leadq(s)}{trapbox(s)}</div>
{foot(meta)}{notes(s)}</section>"""


def r_reason(s, meta):
    cls, kicker, h = head_bits(s, meta)
    lis = "".join(
        f'<li class="{"key" if it.get("key") else ""}">{esc(it["t"])}</li>'
        for it in s["items"]
    )
    return f"""<section{cls}>
<div class="slide-band"></div>{kicker}{h}
<ol class="reason">{lis}</ol>{leadq(s)}
{foot(meta)}{notes(s)}</section>"""


def r_proof(s, meta):
    cls, kicker, h = head_bits(s, meta)
    parts = []
    for i, st in enumerate(s["steps"]):
        if i:
            parts.append('<div class="arrow"></div>')
        k = st.get("kind", "")
        sc = f"step {k}".strip()
        lead = f'<span class="lead">{esc(st["lead"])}</span> ' if st.get("lead") else ""
        parts.append(f'<div class="{sc}">{lead}{esc(st["t"])}</div>')
    lq = (f'<p class="lead-q" style="margin-bottom:.6em">{esc(s["q"])}</p>'
          if s.get("q") else "")
    return f"""<section{cls}>
<div class="slide-band"></div>{kicker}{h}{lq}
<div class="proof-flow">{''.join(parts)}</div>
{foot(meta)}{notes(s)}</section>"""


def r_truth(s, meta):
    cls, kicker, h = head_bits(s, meta)
    rows = [f'<tr>{"".join(f"<th>{esc(x)}</th>" for x in s["head"])}</tr>']
    for row in s["rows"]:
        marks = row.get("marks", [""] * len(row["cells"]))
        tds = "".join(f'<td class="{m}">{esc(c)}</td>'
                      for c, m in zip(row["cells"], marks))
        rows.append(f'<tr class="{"win" if row.get("win") else ""}">{tds}</tr>')
    cap = f'<p class="figcap">{esc(s["caption"])}</p>' if s.get("caption") else ""
    return f"""<section{cls}>
<div class="slide-band"></div>{kicker}{h}
<table class="truth">{''.join(rows)}</table>{cap}
{foot(meta)}{notes(s)}</section>"""


def r_concept(s, meta):
    cls, kicker, h = head_bits(s, meta, center=True)
    rk = (f'<span class="reveal-kicker">{esc(s["revealKicker"])}</span>'
          if s.get("revealKicker") else "")
    sub = f'<span class="sub">{esc(s["sub"])}</span>' if s.get("sub") else ""
    body = f'<div class="stack" style="margin-top:1em">{paras(s["body"])}</div>' \
        if s.get("body") else ""
    return f"""<section{cls}>
<div class="slide-band"></div>{kicker}{h}
<div class="reveal-box">{rk}<span class="concept">{esc(s['concept'])}</span>{sub}</div>
{body}{foot(meta)}{notes(s)}</section>"""


def r_end(s, meta):
    return (f'<section class="center-v"><div class="slide-band"></div>'
            f'<h1>{esc(s.get("h","끝"))}</h1>{foot(meta)}{notes(s)}</section>')


RENDER = {
    "title": r_title, "warmup": r_basic, "problem": r_basic, "setup": r_basic,
    "solution": r_basic, "practice": r_basic, "reason": r_reason,
    "proof-flow": r_proof, "truth-table": r_truth, "concept-reveal": r_concept,
    "end": r_end,
}


def build(week_json: Path):
    data = json.loads(read(week_json))
    meta = {"week": data["week"], "phase": data["phase"],
            "title": data["title"], "subtitle": data.get("subtitle", "")}

    sections = []
    for s in data["slides"]:
        fn = RENDER.get(s["type"])
        if not fn:
            sys.exit(f"unknown slide type: {s['type']}")
        sections.append(fn(s, meta))

    tokens = read(DS / "tokens.css").replace('url("fonts/', 'url("../_assets/fonts/')
    css = "\n".join([
        read(REVEAL / "dist" / "reset.css"),
        read(REVEAL / "dist" / "reveal.css"),
        katex_css_inlined(),
        tokens,
        read(DS / "components" / "components.css"),
        DECK_CSS,
    ])
    # 각 라이브러리는 개별 <script>로 (이어붙이면 경계에서 ASI 오류 위험)
    libs = [
        read(REVEAL / "dist" / "reveal.js"),
        read(REVEAL / "plugin" / "notes" / "notes.js"),
        read(KATEX / "katex.min.js"),
        read(KATEX / "contrib" / "auto-render.min.js"),
    ]
    scripts = "\n".join(f"<script>{lib}</script>" for lib in libs)

    init = """
Reveal.initialize({hash:true, slideNumber:'c/t', width:1280, height:720,
  center:false, margin:0.04, transition:'slide', plugins:[RevealNotes]})
.then(function(){
  renderMathInElement(document.body, {delimiters:[
    {left:'$$',right:'$$',display:true},
    {left:'$',right:'$',display:false},
    {left:'\\\\(',right:'\\\\)',display:false},
    {left:'\\\\[',right:'\\\\]',display:true}
  ], throwOnError:false});
  Reveal.layout();
});
"""

    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(meta['title'])}</title>
<style>{css}</style></head>
<body data-phase="{meta['phase']}">
<div class="reveal"><div class="slides">
{chr(10).join(sections)}
</div></div>
{scripts}
<script>{init}</script>
</body></html>"""

    out_dir = ROOT / "docs" / f"week{meta['week']:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(doc, encoding="utf-8")
    return out_dir / "index.html", len(data["slides"])


def write_index():
    weeks = []
    for wj in sorted((ROOT / "content").glob("week*.json")):
        d = json.loads(read(wj))
        weeks.append((d["week"], d["phase"], d["title"]))
    items = "".join(
        f'<li><a href="week{w:02d}/" data-phase="{p}"><b>{w}주차</b> {esc(t)}</a></li>'
        for w, p, t in weeks
    )
    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>논리퍼즐 수업</title><style>
body{{font-family:"Pretendard",system-ui,"Noto Sans KR",sans-serif;max-width:720px;margin:3rem auto;padding:0 1rem;color:#15171e}}
h1{{letter-spacing:-.02em}} ul{{list-style:none;padding:0}}
li a{{display:block;padding:.9rem 1.1rem;margin:.4rem 0;border:1px solid #e2e5ea;border-radius:12px;text-decoration:none;color:inherit;border-left:6px solid #4338ca}}
li a[data-phase="2"]{{border-left-color:#0f766e}} li a[data-phase="3"]{{border-left-color:#b45309}} li a[data-phase="4"]{{border-left-color:#6d28d9}}
li a:hover{{background:#f3f4f7}}
</style></head><body><h1>논리퍼즐 수업 — 슬라이드</h1>
<p>각 주차를 열고 <kbd>F</kbd> 전체화면, <kbd>S</kbd> 발표자 노트, 방향키로 넘김.</p>
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
