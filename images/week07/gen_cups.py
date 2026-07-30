#!/usr/bin/env python3
"""릴레이 4 · 물컵 6개(컵 하나만 만져서 번갈아) 흑백 스케치 SVG.

- r4_cups_q.svg (문제): 지금 배열(참참참빈빈빈) + 목표 배열(붓기 실마리 미노출).
- r4_cups_a.svg (풀이): 2번 컵의 물을 5번 컵에 붓는 화살표 + 결과 배열.
컵은 g transform 지역좌표로 저작(큰 절대좌표 텍스트 버그 회피).
실행: python3 gen_cups.py
"""

INK = "#111111"
GRAY = "#d7d7d7"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 2번 컵의 물을 5번 컵에 부으면 번갈아 배열
arr = [1, 1, 1, 0, 0, 0]
arr[4], arr[1] = arr[1], arr[4]          # 물만 이동
assert arr == [1, 0, 1, 0, 1, 0], arr


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


CW, CH = 52, 62                    # 컵 크기(위가 넓은 사다리꼴)


def cup(x, y, filled, num=None):
    """(x,y)=컵 좌상단. g translate 지역좌표."""
    p = [f'<g transform="translate({x},{y})">']
    if filled:
        p.append(f'<polygon points="4,12 {CW-4},12 {CW-8},{CH} 8,{CH}" fill="{GRAY}"/>')
    p.append(f'<polygon points="0,0 {CW},0 {CW-9},{CH} 9,{CH}" fill="none" stroke="{INK}" stroke-width="2.8"/>')
    if filled:
        p.append(f'<line x1="4" y1="12" x2="{CW-4}" y2="12" stroke="{INK}" stroke-width="1.8"/>')
    if num is not None:
        p.append(f'<text x="{CW/2}" y="{CH+26}" text-anchor="middle" font-family="{FONT}" font-size="19" fill="{INK}">{num}</text>')
    p.append("</g>")
    return p


def row(x0, y0, states, label=None, nums=False):
    p = []
    if label:
        p.append(f'<text x="{x0-18}" y="{y0+CH*0.62}" text-anchor="end" font-family="{FONT}" font-size="22" font-weight="700" fill="{INK}">{label}</text>')
    for k, f in enumerate(states):
        p += cup(x0 + k * (CW + 22), y0, f, num=(k + 1) if nums else None)
    return p


# ---------- q: 지금 + 목표 ----------
parts = []
parts += row(120, 44, [1, 1, 1, 0, 0, 0], "지금", nums=True)
parts += row(120, 178, [1, 0, 1, 0, 1, 0], "목표")
parts += caption(330, 300, ["컵은 딱 한 개만 만질 수 있다 - 어떻게 할까?"], 22)
W, H = 620, 330
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r4_cups_q.svg", "w", encoding="utf-8").write(svg)
print("wrote r4_cups_q.svg")

# ---------- a: 붓기 화살표 + 결과 ----------
parts = []
parts += row(120, 96, [1, 1, 1, 0, 0, 0], "지금", nums=True)
# 2번 컵 → 5번 컵 곡선 화살표
x2 = 120 + 1 * (CW + 22) + CW / 2
x5 = 120 + 4 * (CW + 22) + CW / 2
parts.append(f'<path d="M {x2} 88 Q {(x2+x5)/2} 18 {x5-8} 82" fill="none" stroke="{INK}" stroke-width="3"/>')
parts.append(f'<polygon points="{x5},{92} {x5-15},{78} {x5-2},{72}" fill="{INK}"/>')
parts.append(f'<text x="{(x2+x5)/2}" y="34" text-anchor="middle" font-family="{FONT}" font-size="21" font-weight="700" fill="{INK}">물만 붓는다</text>')
parts += row(120, 250, [1, 0, 1, 0, 1, 0], "결과")
parts += caption(340, 372, ["만진 컵은 2번 하나 - 배열은 찬·빈·찬·빈·찬·빈"], 22)
W, H = 640, 402
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r4_cups_a.svg", "w", encoding="utf-8").write(svg)
print("wrote r4_cups_a.svg")
