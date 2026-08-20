#!/usr/bin/env python3
"""사다리 스텝 3·4 · 상자 그림(수를 모르는 채 따라가기) 흑백 스케치 SVG.

같은 파이프라인이 단계마다 자라난다(사용자 피드백 - 절차 전체가 그림으로 이어지게):
- r3_boxes_q.svg  (문제):  [□]→×2→[□□]→+10→[□□+●10]→÷2→[?]
- sr3_half_a.svg  (확인3): [□]→×2→[□□]→+10→[□□+●10]→÷2→[□+●5]→−처음 수→[?]
- sr4_gone_a.svg  (확인4): 전체 절차 완성 - 마지막에 상자가 지워지고 구슬 5 = 5.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_boxes.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
# 변수 x는 LaTeX 이탤릭 - 덱에 인라인된 KaTeX_Math 웹폰트 사용(단독 열람 시 serif italic 폴백)
MATH_FONT = "KaTeX_Math, 'Times New Roman', serif"

# 검증: (2x+10)/2 = x+5, (x+5)-x = 5
assert (2 * 7 + 10) / 2 == 7 + 5
assert (7 + 5) - 7 == 5


def caption(cx, y, lines, size=21):
    # 텍스트는 g translate 지역좌표로 - 큰 절대좌표 텍스트 배율 버그 회피(6주차 확립 규칙)
    t = [f'<g transform="translate({cx},{y})"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="0" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text></g>")
    return ["".join(t)]


def label(x, y, text, size=20, weight=400, anchor="middle"):
    return [f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{INK}">{text}</text></g>']


def math_term(cx, y, text, size=24):
    """그림 아래 문자식 항: 'x'만 KaTeX 이탤릭으로."""
    body = text.replace("x", f'<tspan font-family="{MATH_FONT}" font-style="italic" '
                             f'font-weight="400" font-size="{size + 3}">x</tspan>')
    return [f'<g transform="translate({cx},{y})"><text x="0" y="0" text-anchor="middle" '
            f'font-family="{FONT}" font-size="{size}" font-weight="700" fill="{INK}">{body}</text></g>']


def box(x, y, s=40, crossed=False):
    p = [f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{GRAY}" stroke="{INK}" stroke-width="2.6"/>',
         f'<g transform="translate({x + s / 2},{y + s / 2 + 8})"><text x="0" y="0" text-anchor="middle" '
         f'font-family="{FONT}" font-size="22" font-weight="700" fill="{INK}">?</text></g>']
    if crossed:
        p.append(f'<line x1="{x - 5}" y1="{y - 5}" x2="{x + s + 5}" y2="{y + s + 5}" stroke="{INK}" stroke-width="3"/>')
        p.append(f'<line x1="{x + s + 5}" y1="{y - 5}" x2="{x - 5}" y2="{y + s + 5}" stroke="{INK}" stroke-width="3"/>')
    return p


def beads(x, y, n, r=8, gap=22, per_row=5):
    p = []
    for k in range(n):
        cx = x + (k % per_row) * gap
        cy = y + (k // per_row) * gap
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>')
    return p


def arrow_r(x1, x2, y, sw=2.4):
    return [f'<line x1="{x1}" y1="{y}" x2="{x2 - 10}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
            f'<polygon points="{x2},{y} {x2 - 14},{y - 7} {x2 - 14},{y + 7}" fill="{INK}"/>']


def stage(x, cy, nboxes=0, nbeads=0, crossed=False):
    """상자 nboxes개 + 구슬 nbeads개 묶음. (x = 왼쪽 끝, cy = 세로 중심). 오른쪽 끝 x 반환."""
    p = []
    s = 40
    for k in range(nboxes):
        p += box(x, cy - s / 2, s, crossed=crossed)
        x += s + 8
    if nbeads:
        x += 6
        rows = (nbeads + 4) // 5
        y0 = cy - (rows - 1) * 11
        p += beads(x + 8, y0, nbeads)
        x += 8 + 4 * 22 + 8 + 2
    return p, x


def qbox(x, cy):
    """물음표 점선 카드."""
    s = 44
    p = [f'<rect x="{x}" y="{cy - s / 2}" width="{s}" height="{s}" rx="8" fill="#ffffff" '
         f'stroke="{INK}" stroke-width="2.4" stroke-dasharray="7 6"/>']
    p += label(x + s / 2, cy + 8, "?", 26, 700)
    return p, x + s


def op_arrow(parts, x, cy, name, wide=False):
    """연산 라벨이 붙은 화살표. 오른쪽 끝 x 반환."""
    w = 88 if wide else 46
    parts += arrow_r(x + 6, x + 6 + w, cy)
    parts += label(x + 6 + w / 2, cy - 16, name, 19, 700)
    return x + 12 + w


def pipeline(cy, upto, final=None, label_top=True):
    """upto: 몇 단계까지 그리나(2=+10 결과까지, 3=÷2 결과까지). final: 'q'(물음표) 또는 'gone'(상자 소거).
    반환: (parts, 오른쪽 끝 x, 단계별 중심 x 목록)."""
    parts, centers = [], []
    if label_top:
        parts += label(95, cy - 52, "고른 수 = 상자", 19, 700)
    sx = 75
    p, x = stage(sx, cy, nboxes=1)
    parts += p
    centers.append((sx + x) / 2)
    x = op_arrow(parts, x, cy, "×2")
    sx = x
    p, x = stage(x, cy, nboxes=2)
    parts += p
    centers.append((sx + x) / 2)
    x = op_arrow(parts, x, cy, "+10")
    sx = x
    p, x = stage(x, cy, nboxes=2, nbeads=10)
    parts += p
    centers.append((sx + x) / 2)
    x = op_arrow(parts, x, cy, "÷2")
    if upto == 2:
        p, x = qbox(x + 4, cy)
        parts += p
        return parts, x, centers
    sx = x
    p, x = stage(x, cy, nboxes=1, nbeads=5)
    parts += p
    centers.append((sx + x) / 2)
    x = op_arrow(parts, x, cy, "−처음 수", wide=True)
    if final == "q":
        p, x = qbox(x + 4, cy)
        parts += p
    else:
        sx = x
        p, x = stage(x, cy, nboxes=1, nbeads=5, crossed=True)
        parts += p
        centers.append((sx + x) / 2)
        parts += label(x + 14, cy + 9, "= 5", 28, 700, "start")
        x += 82
    return parts, x, centers


def write_svg(name, parts, w, h):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
           + "\n".join(parts) + "\n</svg>\n")
    open(name, "w", encoding="utf-8").write(svg)
    print(f"wrote {name}")


# ---------- q: ÷2까지, 결과는 물음표 ----------
parts, xe, _ = pipeline(130, upto=2)
parts += caption((75 + xe) / 2, 250, ["상자 두 개와 구슬 열 개 - 반으로 나누면 어떤 그림이 될까?"], 21)
write_svg("r3_boxes_q.svg", parts, xe + 60, 282)

# ---------- 확인 3: ÷2 결과 + 마지막 카드 예고 ----------
parts, xe, _ = pipeline(130, upto=3, final="q")
parts += caption((75 + xe) / 2, 250, ["반으로 나누면 상자 하나와 구슬 다섯 - 마지막 카드 −처음 수를 지나면?"], 21)
write_svg("sr3_half_a.svg", parts, xe + 60, 282)

# ---------- 확인 4: 전체 절차 완성 - 상자 소거 ----------
parts, xe, _ = pipeline(130, upto=3, final="gone")
parts += caption((75 + xe) / 2, 250, ["무엇이 들어 있었든 상자는 지워진다 - 남는 것은 언제나 구슬 다섯"], 21)
write_svg("sr4_gone_a.svg", parts, xe + 40, 282)

# ---------- 개념: 전체 절차 그림 + 문자식 일대일 대응 ----------
parts, xe, cs = pipeline(100, upto=3, final="gone", label_top=False)
assert len(cs) == 5
for c, t in zip(cs, ["x", "2x", "2x+10", "x+5", "5"]):
    parts += math_term(c, 196, t)
write_svg("concept_map_a.svg", parts, xe + 40, 220)
