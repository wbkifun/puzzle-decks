#!/usr/bin/env python3
"""도전 1 예시 풀이(고모리의 정리) — ‘뱀 복도’ 흑백 스케치 SVG.

패널 1: 모든 칸을 꼭 한 번씩 지나 제자리로 돌아오는 닫힌 복도(해밀턴 순환).
패널 2: 다른 색 두 칸을 뺀 62칸 — 복도가 두 토막(둘 다 짝수 길이)이 나고,
        복도를 따라 도미노 31개를 눕힌 완성 그림(코드가 인접성·짝수성 검증).
실행: python3 gen_sc1_snake.py  (풀이 전용 — 문제용 없음)
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"


def build_cycle():
    """8×8 닫힌 복도: 0행 →, 1~6행은 x=1..7 왕복, 7행 ←, 0열로 귀환."""
    cells = [(x, 0) for x in range(8)]
    for y in range(1, 7):
        xs = range(7, 0, -1) if y % 2 == 1 else range(1, 8)
        cells += [(x, y) for x in xs]
    cells += [(x, 7) for x in range(7, -1, -1)]
    cells += [(0, y) for y in range(6, 0, -1)]
    assert len(cells) == 64 and len(set(cells)) == 64
    for a, b in zip(cells, cells[1:] + cells[:1]):     # 순환 인접성
        assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1, (a, b)
    return cells


def dark(c):
    return (c[0] + c[1]) % 2 == 0


def cell_xy(x0, y0, cell, c):
    return x0 + c[0] * cell, y0 + (7 - c[1]) * cell


def center(x0, y0, cell, c):
    x, y = cell_xy(x0, y0, cell, c)
    return x + cell / 2, y + cell / 2


def checker(x0, y0, cell, skip=(), dark_fill="#cfcfcf"):
    p = []
    for i in range(8):
        for j in range(8):
            if (i, j) in skip:
                continue
            x, y = cell_xy(x0, y0, cell, (i, j))
            fill = dark_fill if dark((i, j)) else "none"
            p.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                     f'fill="{fill}" stroke="{INK}" stroke-width="1.2"/>')
    p.append(f'<rect x="{x0}" y="{y0}" width="{8*cell}" height="{8*cell}" '
             f'fill="none" stroke="{INK}" stroke-width="2.6"/>')
    return p


def halo_polyline(pts, close=False, w_halo=8, w_ink=4.4):
    tag = "polygon" if close else "polyline"
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    common = 'fill="none" stroke-linejoin="round" stroke-linecap="round"'
    return [f'<{tag} points="{s}" {common} stroke="{INK}" stroke-width="{w_ink}"/>']


def domino_outline(x0, y0, cell, a, b):
    """인접한 두 칸 a,b를 감싸는 도미노 테(흰 헤일로 + 검정)."""
    xa, ya = cell_xy(x0, y0, cell, a)
    xb, yb = cell_xy(x0, y0, cell, b)
    x, y = min(xa, xb), min(ya, yb)
    w = cell + abs(xa - xb)
    h = cell + abs(ya - yb)
    m = 0.08 * cell
    return [f'<rect x="{x+m}" y="{y+m}" width="{w-2*m}" height="{h-2*m}" rx="5" '
            f'fill="none" stroke="{INK}" stroke-width="3"/>']


def removed_mark(x0, y0, cell, c):
    """뺀 칸: 점선 + ✕ (검은 칸이었으면 회색 고스트)."""
    x, y = cell_xy(x0, y0, cell, c)
    m = 0.10 * cell
    fill = "#7d7d7d" if dark(c) else "none"
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


cycle = build_cycle()
REM_DARK, REM_WHITE = (4, 4), (6, 3)          # 다른 색 두 칸 (검, 흰)
assert dark(REM_DARK) and not dark(REM_WHITE)

BOT, CAP = 296, 330
c = 30
parts = []

# ---------- 패널 1: 닫힌 복도 ----------
x1, y1 = 24, BOT - 8 * c
parts += checker(x1, y1, c)
parts += halo_polyline([center(x1, y1, c, cc) for cc in cycle], close=True)
parts += caption(x1 + 4 * c, CAP, ["모든 칸을 꼭 한 번씩 지나", "제자리로 — 닫힌 복도"])

# ---------- 패널 2: 두 칸 빼고 복도 따라 도미노 ----------
x2, y2 = 330, BOT - 8 * c
i, j = sorted((cycle.index(REM_DARK), cycle.index(REM_WHITE)))
arc1 = cycle[i + 1:j]
arc2 = cycle[j + 1:] + cycle[:i]
assert len(arc1) % 2 == 0 and len(arc2) % 2 == 0, (len(arc1), len(arc2))
parts += checker(x2, y2, c, skip=(REM_DARK, REM_WHITE))
for arc in (arc1, arc2):
    for k in range(0, len(arc), 2):
        a, b = arc[k], arc[k + 1]
        assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
        parts += domino_outline(x2, y2, c, a, b)
parts += removed_mark(x2, y2, c, REM_DARK)
parts += removed_mark(x2, y2, c, REM_WHITE)
parts += caption(x2 + 4 * c, CAP, ["다른 색 두 칸을 빼면 토막은 둘 다 짝수", "— 복도를 따라 도미노 31개"])

W, H = 620, 396
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
       f'width="{W}" height="{H}">\n' + "\n".join(parts) + "\n</svg>\n")
open("sc1_snake.svg", "w", encoding="utf-8").write(svg)
print(f"wrote sc1_snake.svg (arcs: {len(arc1)}+{len(arc2)} = 62)")
