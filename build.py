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

# 랜딩 페이지용 — Phase 메타, 32주 커리큘럼, 수업 날짜
PHASES = [
    {"n": 1, "name": "논리와 추론의 언어", "rng": "1–8주",
     "pa": "#4338ca", "soft": "#eceefc", "ink": "#2c248f"},
    {"n": 2, "name": "변수와 방정식", "rng": "9–16주",
     "pa": "#0f766e", "soft": "#d6f0ec", "ink": "#0a544e"},
    {"n": 3, "name": "함수와 그래프", "rng": "17–24주",
     "pa": "#b45309", "soft": "#fcecd2", "ink": "#8a3f07"},
    {"n": 4, "name": "고급 개념의 씨앗", "rng": "25–32주",
     "pa": "#6d28d9", "soft": "#ece4fb", "ink": "#561db0"},
]

# (주차, Phase, 제목, 목표 개념)
CURRICULUM = [
    (1, 1, "기사와 건달의 섬", "귀류법 · 진술의 부정 · 자기지시"),
    (2, 1, "세 명의 문지기", "드모르간 · 진리표 · 경우 나누기"),
    (3, 1, "이마에 묻은 진흙", "지식에 대한 추론 (공통 지식)"),
    (4, 1, "악수와 비둘기집", "비둘기집 원리 · 최악의 경우"),
    (5, 1, "덮을 수 있을까", "불변량(invariant)"),
    (6, 1, "스무고개의 과학", "정보량 · 이진/3진 탐색"),
    (7, 1, "숨은 가정 깨기", "숨은 전제 식별 · 발상 전환"),
    (8, 1, "Phase 1 정리", "자작 논리퍼즐 출제 대회"),
    (9, 2, "비율 직관의 함정", "비율과 기준량"),
    (10, 2, "변수 도입의 힘", "변수 · 식 세우기"),
    (11, 2, "일차방정식 모델링", "일차방정식"),
    (12, 2, "연립방정식의 필요성", "연립방정식 · 미지수 여러 개"),
    (13, 2, "정수해 방정식", "디오판토스 방정식 · 정수해"),
    (14, 2, "자릿수의 대수", "10진법 전개 · 복면산"),
    (15, 2, "약수와 소인수분해", "약수 · 소인수분해 · 제곱수"),
    (16, 2, "Phase 2 정리", "모델링 프로젝트"),
    (17, 3, "그래프 읽기", "그래프 해석"),
    (18, 3, "직선의 교점 = 사건", "일차함수 · 두 직선의 교점"),
    (19, 3, "계단함수와 경계 조건", "불연속 함수 · 경계 조건"),
    (20, 3, "변수 선택의 미학", "변수 선택 · 거꾸로 사고"),
    (21, 3, "지수 성장", "지수함수 · 성장 비교"),
    (22, 3, "이차함수 입구", "이차함수 · 최댓값"),
    (23, 3, "기하 확률", "기하 확률 (넓이 = 확률)"),
    (24, 3, "Phase 3 정리", "그래프 자작문제 발표회"),
    (25, 4, "가중치와 선형결합", "가중합 · 내적 · 선형결합"),
    (26, 4, "패리티와 mod 2", "mod 2 · 패리티 · 벡터공간"),
    (27, 4, "상태 공간 탐색", "상태 공간 · 그래프 탐색"),
    (28, 4, "좌표계와 거리", "좌표계 · 거리 함수"),
    (29, 4, "함수 합성과 암호", "함수 · 역함수 · 합성 · 공개키"),
    (30, 4, "무한과 극한", "무한급수 · 극한"),
    (31, 4, "넓이와 변화율", "적분 · 미분의 씨앗"),
    (32, 4, "최종 발표회", "퍼즐→일반화→수학 미니 강의"),
]

# 실제 수업 날짜 (확정된 것만 기록)
DATES = {1: "6.11 (목)", 2: "6.18 (목)"}


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
/* 화면용 기준 폰트 크기 — reveal 테마를 안 쓰므로 여기서 명시.
   교실 TV 가시성을 위해 디자인 의도(30px)보다 키움. 슬라이드별 내용이
   많아 넘칠 때만 해당 슬라이드에서 줄인다(.dense). 한 값으로 전체 조절. */
.reveal { font-size: 34px; }
.reveal .slides > section.dense { font-size: 28px; }   /* 내용 많은 슬라이드용 */
.reveal .slides > section { padding: 0 !important; }
/* 모든 슬라이드의 실제 캔버스: 내가 100% 제어하는 고정 720 높이 박스
   (reveal의 섹션 높이 간섭을 받지 않음). 이 안에서
   band(top 고정) · smain(flex:1로 남는 공간 채움) · foot(흐름의 마지막=바닥)
   → 풋노트가 내용 많고 적음에 상관없이 항상 좌하단, 본문과 안 겹침. */
.canvas {
  position: relative; box-sizing: border-box;
  width: 100%; height: 720px;
  padding: 50px 64px 52px;          /* 하단 52px = 풋노트 자리 예약 */
  display: flex; flex-direction: column;
}
.smain { flex: 0 0 auto; display: flex; flex-direction: column; }
.center-v .canvas { justify-content: center; }   /* 타이틀/리빌/끝은 수직 중앙 */
.reveal .subtitle { color: var(--ink-soft); font-size: 1.1em; margin-top: .2em; }
/* 좌하단 풋노트 — 캔버스(고정720) 기준 하단 띠에 absolute 고정.
   본문은 fitSection이 이 띠 위로 들어맞게 축소 → 항상 같은 위치, 겹침 없음. */
.slide-foot {
  position: absolute; left: 64px; bottom: 18px;
  font-family: var(--font-mono); font-size: .42em; letter-spacing: .1em;
  color: var(--ink-soft); text-transform: uppercase;
}
.slide-foot b { color: var(--phase-accent-ink); font-weight: 700; }
.slide-foot .foot-num { color: var(--phase-accent-ink); font-weight: 700; }
/* 문제 ↔ 풀이 점프 링크 (우상단 끝 알약 버튼 — 32주 일관 위치)
   ※ reveal.css의 `.reveal a{position:relative}`(0,1,1)보다 우선하도록
     `.reveal .slide-link`(0,2,0)로 선택자 특이도를 높임. 안 그러면 absolute가
     무시되어 흐름에 남아 좌하단으로 떨어진다. */
.reveal .slide-link {
  position: absolute !important; right: 24px; top: 22px; z-index: 6;
  display: inline-flex; align-items: center; gap: .4em;
  font-family: var(--font-mono); font-size: .5em; font-weight: 700;
  letter-spacing: .04em; padding: .5em .9em; border-radius: 999px;
  text-decoration: none; color: #fff; background: var(--phase-accent);
  box-shadow: var(--shadow);
}
.reveal .slide-link:hover { filter: brightness(1.08); }
.reveal .slide-link .ar { font-size: 1.15em; line-height: 1; }
/* 섹션 구분 슬라이드 큰 제목 */
.divider-h { color: var(--phase-accent-ink); font-size: 2.6em; }
/* 드모르간 2×2 격자 그림 */
.dm-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; width: 440px; max-width: 100%; }
.dm-cell { border: 2px solid var(--line); border-radius: 10px; min-height: 76px;
  display: grid; place-items: center; text-align: center; white-space: nowrap;
  font-family: var(--font-mono); font-size: .78em; line-height: 1.3;
  background: var(--bg-panel); color: var(--ink-soft); }
.dm-cell.dm-on { background: var(--phase-accent-soft); border-color: var(--phase-accent);
  color: var(--phase-accent-ink); font-weight: 800; }
/* KaTeX 가 슬라이드 폰트 위계와 충돌하지 않게 */
.reveal .katex { font-size: 1.05em; }
"""


# ---------- 슬라이드 조각 ----------
def notes(s):
    n = s.get("notes")
    return f'<aside class="notes">{esc(n)}</aside>' if n else ""


def foot(meta):
    # 좌하단 한 줄: 주차 · 단계 · 현재/전체 (슬라이드 번호를 풋노트에 통합)
    num = (f' · <span class="foot-num">{meta["idx"]} / {meta["n"]}</span>'
           if meta.get("n") else "")
    return (f'<div class="slide-foot"><b>W{meta["week"]:02d}</b> · '
            f'{esc(PHASE_NAME.get(meta["phase"], ""))}{num}</div>')


def kh(s):
    k = (f'<span class="kicker">{esc(s["kicker"])}</span>'
         if s.get("kicker") else "")
    h = f'<h2>{esc(s["h"])}</h2>' if s.get("h") else ""
    return k + h


def shell(meta, s, inner, center=False):
    # band(absolute) + smain(flex:1, 내용) + foot(흐름의 마지막 = 본문 아래) + notes
    # 풋노트가 absolute가 아니라 흐름 요소라, reveal가 섹션 높이를 어떻게 잡든
    # 본문 밑에 와서 절대 겹치지 않는다.
    cls = "slide center-v" if center else "slide"
    return (f'<section class="{cls}"><div class="canvas">'
            f'<div class="slide-band"></div>'
            f'<div class="smain">{inner}</div>'
            f'{foot(meta)}'
            f'</div>{notes(s)}</section>')


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


def jump_link(j):
    """문제↔풀이 점프 링크. dir 'prev'면 ← 왼쪽, 그 외 → 오른쪽."""
    label = esc(j.get("label", ""))
    if j.get("dir") == "prev":
        inner = f'<span class="ar">←</span>{label}'
    else:
        inner = f'{label}<span class="ar">→</span>'
    return f'<a class="slide-link" href="#/{j["to"]}">{inner}</a>'


# ---------- 아키타입 렌더러 (모두 shell 사용) ----------
def r_title(s, meta):
    kicker = f'Phase {meta["phase"]} · {meta["week"]}주차'
    inner = (f'<span class="kicker">{esc(kicker)}</span>'
             f'<h1>{esc(meta["title"])}</h1>'
             f'<p class="subtitle">{esc(meta.get("subtitle",""))}</p>')
    return shell(meta, s, inner, center=True)


def r_basic(s, meta):
    inner = kh(s) + (f'<div class="stack">{paras(s.get("body",[]))}'
                     f'{leadq(s)}{trapbox(s)}</div>')
    return shell(meta, s, inner)


def r_reason(s, meta):
    lis = "".join(
        f'<li class="{"key" if it.get("key") else ""}">{esc(it["t"])}</li>'
        for it in s["items"])
    inner = kh(s) + f'<ol class="reason">{lis}</ol>' + leadq(s)
    return shell(meta, s, inner)


def r_proof(s, meta):
    parts = []
    for i, st in enumerate(s["steps"]):
        if i:
            parts.append('<div class="arrow"></div>')
        sc = ("step " + st.get("kind", "")).strip()
        lead = (f'<span class="lead">{esc(st["lead"])}</span> '
                if st.get("lead") else "")
        parts.append(f'<div class="{sc}">{lead}{esc(st["t"])}</div>')
    lq = (f'<p class="lead-q" style="margin-bottom:.5em">{esc(s["q"])}</p>'
          if s.get("q") else "")
    inner = kh(s) + lq + f'<div class="proof-flow">{"".join(parts)}</div>'
    return shell(meta, s, inner)


def r_truth(s, meta):
    rows = [f'<tr>{"".join(f"<th>{esc(x)}</th>" for x in s["head"])}</tr>']
    for row in s["rows"]:
        marks = row.get("marks", [""] * len(row["cells"]))
        tds = "".join(f'<td class="{m}">{esc(c)}</td>'
                      for c, m in zip(row["cells"], marks))
        rows.append(f'<tr class="{"win" if row.get("win") else ""}">{tds}</tr>')
    cap = f'<p class="figcap">{esc(s["caption"])}</p>' if s.get("caption") else ""
    inner = kh(s) + f'<table class="truth">{"".join(rows)}</table>' + cap
    return shell(meta, s, inner)


def r_concept(s, meta):
    rk = (f'<span class="reveal-kicker">{esc(s["revealKicker"])}</span>'
          if s.get("revealKicker") else "")
    sub = f'<span class="sub">{esc(s["sub"])}</span>' if s.get("sub") else ""
    body = (f'<div class="stack" style="margin-top:1em">{paras(s["body"])}</div>'
            if s.get("body") else "")
    inner = (kh(s) + f'<div class="reveal-box">{rk}'
             f'<span class="concept">{esc(s["concept"])}</span>{sub}</div>' + body)
    return shell(meta, s, inner, center=True)


def r_divider(s, meta):
    # 섹션 구분(예: "풀이") — 큰 제목 + 안내 부제
    sub = f'<p class="subtitle">{esc(s["sub"])}</p>' if s.get("sub") else ""
    inner = f'<h1 class="divider-h">{esc(s.get("h","풀이"))}</h1>{sub}'
    return shell(meta, s, inner, center=True)


def r_raw(s, meta):
    # 커스텀 그림/레이아웃용: html 필드를 (이스케이프 없이) 그대로 삽입.
    # 콘텐츠는 내가 작성하는 신뢰 입력이므로 raw HTML 허용. 속성은 ' 사용 권장.
    inner = kh(s) + s.get("html", "")
    return shell(meta, s, inner, center=s.get("center", False))


def r_end(s, meta):
    return shell(meta, s, f'<h1>{esc(s.get("h","끝"))}</h1>', center=True)


RENDER = {
    "title": r_title, "warmup": r_basic, "problem": r_basic, "setup": r_basic,
    "solution": r_basic, "practice": r_basic, "reason": r_reason,
    "proof-flow": r_proof, "truth-table": r_truth, "concept-reveal": r_concept,
    "divider": r_divider, "raw": r_raw, "end": r_end,
}


def build(week_json: Path):
    data = json.loads(read(week_json))
    meta = {"week": data["week"], "phase": data["phase"],
            "title": data["title"], "subtitle": data.get("subtitle", "")}

    sections = []
    total = len(data["slides"])
    for i, s in enumerate(data["slides"]):
        meta["idx"], meta["n"] = i + 1, total
        fn = RENDER.get(s["type"])
        if not fn:
            sys.exit(f"unknown slide type: {s['type']}")
        sec = fn(s, meta)
        if s.get("id"):                      # 점프 대상이 되도록 #/<id> 부여
            sec = sec.replace("<section", f'<section id="{s["id"]}"', 1)
        if s.get("dense"):                   # 내용 많은 슬라이드는 폰트 축소
            sec = sec.replace("<section", '<section class="dense"', 1) \
                if 'class="' not in sec.split(">", 1)[0] else \
                sec.replace('class="', 'class="dense ', 1)
        if s.get("jump"):                    # 점프 링크를 캔버스 안(band 뒤)에 삽입 → 캔버스 기준 우상단
            sec = sec.replace('<div class="slide-band"></div>',
                              '<div class="slide-band"></div>' + jump_link(s["jump"]), 1)
        sections.append(sec)

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
// 슬라이드 내용이 캔버스(720px)를 넘치면 그 슬라이드만 폰트를 줄여 맞춤.
// 내용이 적은 슬라이드는 기준(34px) 유지 → "넘칠 때만 축소" 동적 조절.
function fitSection(sec){
  if(!sec) return;
  var c = sec.querySelector('.canvas'), m = sec.querySelector('.smain');
  if(!c || !m) return;
  sec.style.fontSize='';                       // 기준 크기로 리셋 후 측정
  var cs = getComputedStyle(c);
  // 풋노트 띠(하단 패딩) 위로 본문이 들어갈 실제 가용 높이(레이아웃 px, transform 무관)
  var avail = c.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
  var guard=0;
  while(m.scrollHeight > avail + 1 && guard++ < 16){
    var cur = parseFloat(getComputedStyle(sec).fontSize) || 34;
    sec.style.fontSize = (cur * Math.max(0.92, avail/m.scrollHeight)).toFixed(2)+'px';
  }
}
Reveal.initialize({hash:true, slideNumber:false, width:1280, height:720,
  center:false, margin:0.04, transition:'slide', viewDistance:5,
  plugins:[RevealNotes]})
.then(function(){
  renderMathInElement(document.body, {delimiters:[
    {left:'$$',right:'$$',display:true},
    {left:'$',right:'$',display:false},
    {left:'\\\\(',right:'\\\\)',display:false},
    {left:'\\\\[',right:'\\\\]',display:true}
  ], throwOnError:false});
  var fitCur = function(){ fitSection(Reveal.getCurrentSlide()); };
  Reveal.on('slidechanged', function(e){ fitSection(e.currentSlide); });
  Reveal.on('resize', fitCur);
  fitCur();
  if(document.fonts && document.fonts.ready){ document.fonts.ready.then(fitCur); }
  setTimeout(fitCur, 250);    // KaTeX/웹폰트 레이아웃 안정 후 최종 보정
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
    built = {int(p.stem[4:]) for p in (ROOT / "content").glob("week*.json")}

    phases_html = ""
    for ph in PHASES:
        cards = ""
        for w, p, title, concept in CURRICULUM:
            if p != ph["n"]:
                continue
            date = DATES.get(w, "")
            date_html = f'<span class="date">{esc(date)}</span>' if date else "<span></span>"
            top = f'<div class="top"><span>{w}주차</span>{date_html}</div>'
            mid = f'<div class="title">{esc(title)}</div><div class="concept">{esc(concept)}</div>'
            if w in built:
                cards += (f'<a class="card" href="week{w:02d}/">{top}{mid}'
                          f'<div class="go">▶ 슬라이드 열기</div></a>')
            else:
                cards += (f'<div class="card todo">{top}{mid}'
                          f'<div class="tagtodo">준비 중</div></div>')
        phases_html += (
            f'<section class="phase" style="--pa:{ph["pa"]};--soft:{ph["soft"]};--pink:{ph["ink"]}">'
            f'<div class="phead">PHASE {ph["n"]} · {esc(ph["name"])}'
            f'<span class="rng">{esc(ph["rng"])}</span></div>'
            f'<div class="weeks">{cards}</div></section>'
        )

    css = """
@font-face{font-family:"Pretendard";font-weight:400;font-display:swap;src:url("_assets/fonts/Pretendard-Regular.woff2") format("woff2")}
@font-face{font-family:"Pretendard";font-weight:700;font-display:swap;src:url("_assets/fonts/Pretendard-Bold.woff2") format("woff2")}
@font-face{font-family:"Pretendard";font-weight:800;font-display:swap;src:url("_assets/fonts/Pretendard-ExtraBold.woff2") format("woff2")}
*{box-sizing:border-box}
body{font-family:"Pretendard","Apple SD Gothic Neo","Noto Sans KR",system-ui,sans-serif;color:#15171e;background:#fcfcfd;margin:0;padding:44px 20px;line-height:1.5}
.wrap{max-width:940px;margin:0 auto}
h1{font-size:2rem;letter-spacing:-.02em;margin:0 0 .15em}
.sub{color:#565d6b;margin:0 0 1.8rem}
.phase{margin:1.4rem 0}
.phead{display:flex;align-items:baseline;gap:.55em;padding:.5em .85em;border-radius:10px;background:var(--pa);color:#fff;font-weight:800;font-size:1.05rem}
.phead .rng{font-size:.78em;font-weight:600;opacity:.85}
.weeks{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
.card{display:block;text-decoration:none;color:inherit;background:#fff;border:1px solid #e2e5ea;border-left:5px solid var(--pa);border-radius:10px;padding:.7em .9em;transition:.12s}
a.card:hover{background:var(--soft);transform:translateY(-1px);box-shadow:0 4px 14px rgba(21,23,30,.07)}
.card .top{display:flex;justify-content:space-between;align-items:baseline;font-size:.76rem;font-weight:800;color:var(--pink)}
.card .date{color:#565d6b;font-weight:700;font-feature-settings:"tnum"}
.card .title{font-weight:800;font-size:1.02rem;margin:.18em 0 .12em}
.card .concept{font-size:.82rem;color:#565d6b}
.card .go{font-size:.72rem;color:var(--pink);font-weight:800;margin-top:.45em}
.card.todo{opacity:.55;background:#f8fafc}
.card .tagtodo{font-size:.72rem;color:#565d6b;font-weight:700;margin-top:.45em}
.legend{font-size:.82rem;color:#565d6b;margin:.2rem 0 0}
@media(max-width:640px){.weeks{grid-template-columns:1fr}}
"""
    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>논리퍼즐 수업 — 32주</title><style>{css}</style></head>
<body><div class="wrap">
<h1>논리퍼즐 수업</h1>
<p class="sub">중학생 토론 수업 · 주 1회 90분 · 32주 (퍼즐 → 일반화 → 수학 개념)</p>
<p class="legend">완성된 주차의 카드를 누르면 슬라이드가 열립니다. 발표: <kbd>F</kbd> 전체화면 · <kbd>S</kbd> 발표자 노트 · 방향키로 넘김.</p>
{phases_html}
</div></body></html>"""
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "index.html").write_text(doc, encoding="utf-8")
    print(f"built docs/index.html  (32주 구조, 완성 {len(built)}주)")


if __name__ == "__main__":
    targets = sys.argv[1:] or sorted((ROOT / "content").glob("week*.json"))
    for t in targets:
        out, n = build(Path(t))
        print(f"built {out.relative_to(ROOT)}  ({n} slides)")
    write_index()
