#!/usr/bin/env python3
"""체스판·도미노 슬라이드 세트(무대 설정·메인①②·풀이 2/3/4-1) 흑백 스케치 SVG.

- setup_board.svg   (무대 설정): 8×8 판 + ‘도미노 = 이웃 두 칸’ 규칙
- p2_board_q.svg    (메인① 문제): 온전한 64칸 + 도미노 ×32
- p3_board_q.svg    (메인② 문제): 모서리 한 칸 뗀 63칸 + 도미노 × ?
- s2_brick_a.svg    (풀이 2): 벽돌쌓기 — 한 줄에 4개씩 8줄 = 32개
- s3_parity_a.svg   (풀이 3): 도미노 k개 = 2k칸(짝수) vs 63(홀수)
- s4_fail_a.svg     (풀이 4-1): 62칸에 30개까지 놓으면 늘 두 칸이 멀리 남는다
실행: python3 gen_board_set.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
GRAY = "#cfcfcf"


def dark(c):
    return (c[0] + c[1]) % 2 == 0


def cell_xy(x0, y0, n, cell, c):
    return x0 + c[0] * cell, y0 + (n - 1 - c[1]) * cell


def checker(x0, y0, n, cell, dark_fill=INK, skip=()):
    p = []
    for i in range(n):
        for j in range(n):
            if (i, j) in skip:
                continue
            x, y = cell_xy(x0, y0, n, cell, (i, j))
            fill = dark_fill if dark((i, j)) else "none"
            p.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                     f'fill="{fill}" stroke="{INK}" stroke-width="1.2"/>')
    if not skip:
        p.append(f'<rect x="{x0}" y="{y0}" width="{n*cell}" height="{n*cell}" '
                 f'fill="none" stroke="{INK}" stroke-width="2.6"/>')
    else:                                   # 노치 포함 외곽(뗀 칸을 피해 그린다)
        pts_b = []
        rm = set(skip)
        if (0, 0) in rm:
            pts_b += [(1, 0), ]
        else:
            pts_b += [(0, 0), ]
        pts_b += [(n, 0)]
        if (n - 1, n - 1) in rm:
            pts_b += [(n, n - 1), (n - 1, n - 1), (n - 1, n)]
        else:
            pts_b += [(n, n)]
        pts_b += [(0, n)]
        if (0, 0) in rm:
            pts_b += [(0, 1), (1, 1)]
        pts = " ".join(f"{x0 + px*cell},{y0 + (n - py)*cell}" for px, py in pts_b)
        p.append(f'<polygon points="{pts}" fill="none" stroke="{INK}" stroke-width="2.6"/>')
    return p


def removed_mark(x0, y0, n, cell, c):
    """뗀 칸: 점선 + ✕ (색 미노출 — 중립 표시)."""
    x, y = cell_xy(x0, y0, n, cell, c)
    m = 0.10 * cell
    p = [f'<rect x="{x+m}" y="{y+m}" width="{cell-2*m}" height="{cell-2*m}" '
         f'fill="none" stroke="{INK}" stroke-width="1.8" stroke-dasharray="4.5 3.5"/>']
    a, b = x + 0.28 * cell, x + 0.72 * cell
    u, v = y + 0.28 * cell, y + 0.72 * cell
    p += [f'<line x1="{a}" y1="{u}" x2="{b}" y2="{v}" stroke="{INK}" stroke-width="1.8"/>',
          f'<line x1="{a}" y1="{v}" x2="{b}" y2="{u}" stroke="{INK}" stroke-width="1.8"/>']
    return p


def domino_outline(x0, y0, n, cell, a, b, halo=False, sw=3):
    xa, ya = cell_xy(x0, y0, n, cell, a)
    xb, yb = cell_xy(x0, y0, n, cell, b)
    x, y = min(xa, xb), min(ya, yb)
    w = cell + abs(xa - xb)
    h = cell + abs(ya - yb)
    m = 0.08 * cell
    core = (f'<rect x="{x+m}" y="{y+m}" width="{w-2*m}" height="{h-2*m}" rx="5" '
            f'fill="none" stroke="{INK}" stroke-width="{sw}"/>')
    if halo:
        return [f'<rect x="{x+m}" y="{y+m}" width="{w-2*m}" height="{h-2*m}" rx="5" '
                f'fill="none" stroke="#ffffff" stroke-width="{sw+3.5}"/>', core]
    return [core]


def blank_tile(x, y, w, h, label=None):
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" stroke="{INK}" stroke-width="3.5"/>',
         f'<line x1="{x+w/2}" y1="{y+4}" x2="{x+w/2}" y2="{y+h-4}" stroke="{INK}" stroke-width="2"/>']
    if label:
        p.append(f'<text x="{x + w + 18}" y="{y + h*0.68}" font-family="{FONT}" font-size="30" fill="{INK}">{label}</text>')
    return p


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


def build_cycle():
    cells = [(x, 0) for x in range(8)]
    for y in range(1, 7):
        xs = range(7, 0, -1) if y % 2 == 1 else range(1, 8)
        cells += [(x, y) for x in xs]
    cells += [(x, 7) for x in range(7, -1, -1)]
    cells += [(0, y) for y in range(6, 0, -1)]
    assert len(cells) == 64 and len(set(cells)) == 64
    return cells


BOT, CAP, H = 296, 330, 396
FIGS = {}

# ---------- 무대 설정: 판 + 도미노 규칙 ----------
parts = []
c = 33
parts += checker(24, BOT - 8 * c, 8, c)
parts += caption(24 + 4 * c, CAP, ["8×8 체스판 — 64칸"])
c3, x3 = 46, 388
y3 = BOT - 4 * c3
parts += checker(x3, y3, 4, c3)
parts += domino_outline(x3, y3, 4, c3, (0, 2), (1, 2), halo=True, sw=4)
parts += domino_outline(x3, y3, 4, c3, (2, 0), (2, 1), halo=True, sw=4)
parts += caption(x3 + 2 * c3, CAP, ["도미노 = 이웃 두 칸을 덮는 1×2 타일", "(가로·세로 모두) — 겹침·빈틈 없이"])
FIGS["setup_board.svg"] = (parts, 660)

# ---------- 메인 ① 문제: 온전한 판 + ×32 ----------
parts = []
parts += checker(40, BOT - 8 * c, 8, c)
parts += caption(40 + 4 * c, CAP, ["온전한 8×8 — 64칸"])
dc, dx = 46, 452
parts += blank_tile(dx, BOT - 4.6 * c, 2 * dc, dc, "× 32")
parts += caption(dx + 1.6 * dc, CAP, ["도미노 32개 — 빈틈없이", "덮을 수 있을까? 방법은 몇 가지?"])
FIGS["p2_board_q.svg"] = (parts, 700)

# ---------- 메인 ② 문제: 63칸 + × ? ----------
parts = []
RM1 = {(7, 7)}
parts += checker(40, BOT - 8 * c, 8, c, skip=RM1)
for cc in RM1:
    parts += removed_mark(40, BOT - 8 * c, 8, c, cc)
parts += caption(40 + 4 * c, CAP, ["모서리 한 칸을 뗀 63칸"])
parts += blank_tile(dx, BOT - 4.6 * c, 2 * dc, dc, "× ?")
parts += caption(dx + 1.6 * dc, CAP, ["도미노가 몇 개 필요할까", "— 개수부터 따져 보라"])
FIGS["p3_board_q.svg"] = (parts, 700)

# ---------- 풀이 2: 벽돌쌓기 32개 ----------
parts = []
cb, xb = 30, 160
yb = BOT - 8 * cb
parts += checker(xb, yb, 8, cb, dark_fill=GRAY)
for j in range(8):
    for i in (0, 2, 4, 6):
        parts += domino_outline(xb, yb, 8, cb, (i, j), (i + 1, j))
parts += caption(xb + 4 * cb, CAP, ["한 줄에 4개씩 × 8줄 = 32개 — ‘된다’ 증명 끝", "(다른 방법도 1,300만 가지쯤 있지만, 하나면 충분)"])
FIGS["s2_brick_a.svg"] = (parts, 560)

# ---------- 풀이 3: 2k칸(짝수) vs 63(홀수) ----------
parts = []
tc = 27
for k in (1, 2, 3):
    y = 66 + (k - 1) * 62
    for t in range(k):
        parts += blank_tile(46 + t * (2 * tc + 10), y, 2 * tc, tc)
    parts.append(f'<text x="{46 + k*(2*tc+10) + 8}" y="{y + tc*0.72}" '
                 f'font-family="{FONT}" font-size="24" fill="{INK}">= {2*k}칸</text>')
parts.append(f'<text x="46" y="268" font-family="{FONT}" font-size="24" fill="{INK}">⋯  k개 = 2k칸 — 언제나 짝수</text>')
parts += caption(160, CAP, ["도미노가 덮는 칸수는", "무조건 짝수"])
cs, xs = 26, 360
parts += checker(xs, BOT - 8 * cs, 8, cs, skip=RM1)
for cc in RM1:
    parts += removed_mark(xs, BOT - 8 * cs, 8, cs, cc)
parts += caption(xs + 4 * cs, CAP, ["그런데 판은 63칸 — 홀수.", "짝수는 결코 63이 되지 못한다"])
FIGS["s3_parity_a.svg"] = (parts, 620)

# ---------- 풀이 4-1: 30개 놓으면 두 칸이 멀리 남는다 ----------
parts = []
RM2 = {(0, 0), (7, 7)}                      # 마주 보는 두 모서리 (p4와 동일)
cycle = build_cycle()
i, j = sorted(cycle.index(cc) for cc in RM2)
arc1, arc2 = cycle[i + 1:j], cycle[j + 1:] + cycle[:i]
assert len(arc1) % 2 == 1 and len(arc2) % 2 == 1   # 같은 색 제거 → 홀수 토막
cf, xf = 30, 110
yf = BOT - 8 * cf
parts += checker(xf, yf, 8, cf, dark_fill=GRAY, skip=RM2)
for cc in RM2:
    parts += removed_mark(xf, yf, 8, cf, cc)
leftovers = []
for arc in (arc1, arc2):
    for k in range(0, len(arc) - 1, 2):
        a, b = arc[k], arc[k + 1]
        assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
        parts += domino_outline(xf, yf, 8, cf, a, b, sw=2.6)
    leftovers.append(arc[-1])
assert len(leftovers) == 2 and not any(dark(c_) for c_ in leftovers)
n_dom = (len(arc1) + len(arc2) - 2) // 2
assert n_dom == 30
for cc in leftovers:                        # 남은 두 칸: 굵은 점선 + ?
    x, y = cell_xy(xf, yf, 8, cf, cc)
    m = 0.10 * cf
    parts.append(f'<rect x="{x+m}" y="{y+m}" width="{cf-2*m}" height="{cf-2*m}" rx="4" '
                 f'fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="6 4"/>')
    parts.append(f'<text x="{x+cf/2}" y="{y+cf*0.72}" text-anchor="middle" '
                 f'font-family="{FONT}" font-size="20" fill="{INK}">?</text>')
parts += caption(xf + 4 * cf, CAP, ["30개까지는 놓인다 — 그런데 늘 두 칸이,", "그것도 멀리 떨어진 채 남는다. 백 번을 해도."])
FIGS["s4_fail_a.svg"] = (parts, 460)

for name, (parts, W) in FIGS.items():
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">\n' + "\n".join(parts) + "\n</svg>\n")
    open(name, "w", encoding="utf-8").write(svg)
    print("wrote", name)
