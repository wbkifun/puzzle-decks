#!/usr/bin/env python3
"""열린 도전 1(c1) 문제용 흑백 스케치 SVG.

‘다른 색’ 두 칸(검 하나·흰 하나)을 서로 다른 자리에서 뗀 판 두 개 —
"아무 자리나 떼도 항상 될까?"라는 문제 상황만 제시(뱀 복도 등 풀이 실마리 없음).
실행: python3 gen_c1_board.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"


def dark(c):
    return (c[0] + c[1]) % 2 == 0


def cell_xy(x0, y0, cell, c):
    return x0 + c[0] * cell, y0 + (7 - c[1]) * cell


def checker(x0, y0, cell, skip=()):
    p = []
    for i in range(8):
        for j in range(8):
            if (i, j) in skip:
                continue
            x, y = cell_xy(x0, y0, cell, (i, j))
            fill = INK if dark((i, j)) else "none"
            p.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                     f'fill="{fill}" stroke="{INK}" stroke-width="1.2"/>')
    p.append(f'<rect x="{x0}" y="{y0}" width="{8*cell}" height="{8*cell}" '
             f'fill="none" stroke="{INK}" stroke-width="2.6"/>')
    return p


def removed_mark(x0, y0, cell, c):
    """뗀 칸: 점선 + ✕. 원래 검은 칸이었으면 회색 고스트(문제 조건이 ‘다른 색’이므로 색 표시는 상황 제시)."""
    x, y = cell_xy(x0, y0, cell, c)
    m = 0.10 * cell
    fill = "#8a8a8a" if dark(c) else "none"
    p = [f'<rect x="{x+m}" y="{y+m}" width="{cell-2*m}" height="{cell-2*m}" '
         f'fill="{fill}" stroke="{INK}" stroke-width="1.8" stroke-dasharray="4.5 3.5"/>']
    a, b = x + 0.28 * cell, x + 0.72 * cell
    u, v = y + 0.28 * cell, y + 0.72 * cell
    p += [f'<line x1="{a}" y1="{u}" x2="{b}" y2="{v}" stroke="{INK}" stroke-width="1.8"/>',
          f'<line x1="{a}" y1="{v}" x2="{b}" y2="{u}" stroke="{INK}" stroke-width="1.8"/>']
    return p


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


BOT, CAP, H = 296, 330, 396
c = 30
parts = []

A = {(2, 4), (5, 2)}                       # 검(2,4) · 흰(5,2)
assert sorted(dark(x) for x in A) == [False, True]
x1 = 24
parts += checker(x1, BOT - 8 * c, c, skip=A)
for cc in A:
    parts += removed_mark(x1, BOT - 8 * c, c, cc)
parts += caption(x1 + 4 * c, CAP, ["검 한 칸 · 흰 한 칸을 떼어냈다", "— 도미노 31개로 덮일까?"])

B = {(6, 2), (1, 4)}                       # 검(6,2) · 흰(1,4)
assert sorted(dark(x) for x in B) == [False, True]
x2 = 330
parts += checker(x2, BOT - 8 * c, c, skip=B)
for cc in B:
    parts += removed_mark(x2, BOT - 8 * c, c, cc)
parts += caption(x2 + 4 * c, CAP, ["자리를 바꿔 떼어내도?", "— ‘항상’이라고 말할 수 있을까"])

W = 620
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("c1_board_q.svg", "w", encoding="utf-8").write(svg)
print("wrote c1_board_q.svg")
