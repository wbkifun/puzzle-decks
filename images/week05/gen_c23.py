#!/usr/bin/env python3
"""열린 도전 2(c2)·3(c3) 문제용 흑백 스케치 SVG.

- c2_board_q.svg: m×n 초콜릿(일반화) + 동전 ‘3개씩’ 규칙 변경 — 상황만, 홀짝 붕괴 미노출.
- c3_board_q.svg: 자작 퍼즐 설계 — 재료(동전·판·수) → 나만의 퍼즐(불변량 몰래 심기).
실행: python3 gen_c23.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
CHOCO = "#e6e6e6"
BOARD = "#3d3d3d"
CHALK = "#ffffff"


def chunk(x, y, cols, rows, cell):
    w, h = cols * cell, rows * cell
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{CHOCO}" stroke="{INK}" stroke-width="2.8"/>']
    for k in range(1, cols):
        p.append(f'<line x1="{x+k*cell}" y1="{y}" x2="{x+k*cell}" y2="{y+h}" stroke="{INK}" stroke-width="1.3"/>')
    for k in range(1, rows):
        p.append(f'<line x1="{x}" y1="{y+k*cell}" x2="{x+w}" y2="{y+k*cell}" stroke="{INK}" stroke-width="1.3"/>')
    m = 0.18 * cell
    for i in range(cols):
        for j in range(rows):
            p.append(f'<rect x="{x+i*cell+m}" y="{y+j*cell+m}" width="{cell-2*m}" height="{cell-2*m}" '
                     f'rx="3" fill="none" stroke="{INK}" stroke-width="0.9" opacity="0.55"/>')
    return p


def coin(cx, cy, r, face):
    fs = round(r * 0.95)
    if face == "앞":
        return [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2.4"/>',
                f'<text x="{cx}" y="{cy + fs*0.36}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" fill="{INK}">앞</text>']
    return [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{INK}" stroke="{INK}" stroke-width="2.4"/>',
            f'<text x="{cx}" y="{cy + fs*0.36}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" fill="#ffffff">뒤</text>']


def dim_arrow(x1, y1, x2, y2, label, lx, ly):
    """양방향 치수 화살표 + 라벨."""
    p = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="2"/>']
    # 화살촉(단순 삼각형 2개)
    if x1 == x2:      # 세로
        p.append(f'<polygon points="{x1},{y1} {x1-5},{y1+9} {x1+5},{y1+9}" fill="{INK}"/>')
        p.append(f'<polygon points="{x2},{y2} {x2-5},{y2-9} {x2+5},{y2-9}" fill="{INK}"/>')
    else:             # 가로
        p.append(f'<polygon points="{x1},{y1} {x1+9},{y1-5} {x1+9},{y1+5}" fill="{INK}"/>')
        p.append(f'<polygon points="{x2},{y2} {x2-9},{y2-5} {x2-9},{y2+5}" fill="{INK}"/>')
    p.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="{FONT}" font-size="20" fill="{INK}">{label}</text>')
    return p


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


CAP, H = 330, 396

# ---------- 도전 2: m×n 초콜릿 + 3개씩 뒤집기 ----------
parts = []
cx0, cy0, cc = 110, 120, 34                            # 5×3 초콜릿
parts += chunk(cx0, cy0, 5, 3, cc)
parts += dim_arrow(cx0, cy0 + 3 * cc + 22, cx0 + 5 * cc, cy0 + 3 * cc + 22, "가로 n조각", cx0 + 2.5 * cc, cy0 + 3 * cc + 50)
parts += dim_arrow(cx0 - 22, cy0, cx0 - 22, cy0 + 3 * cc, "세로 m조각", cx0 - 22, cy0 - 14)
parts += caption(cx0 + 2.5 * cc, CAP, ["m×n 판초콜릿이라면 몇 번?", "‘방법’은 답에 나타날까?"])

x0 = 520                                              # 동전 9개 + ‘3개씩’ 규칙
r = 24
for k in range(9):
    ccx = x0 + (k % 3) * 64
    ccy = 84 + (k // 3) * 64
    parts += coin(ccx, ccy, r, "앞")
parts.append(f'<rect x="{x0 - 34}" y="{84 - 34}" width="{2*64 + 68}" height="66" rx="33" '
             f'fill="none" stroke="{INK}" stroke-width="2.4" stroke-dasharray="7 5"/>')
parts.append(f'<text x="{x0 + 64}" y="36" text-anchor="middle" font-family="{FONT}" font-size="21" fill="{INK}">한 번에 꼭 3개씩!</text>')
parts += caption(x0 + 64, CAP, ["앞면 9개, ‘정확히 3개’씩 뒤집기", "— 모두 뒷면 가능?"])

W = 780
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("c2_board_q.svg", "w", encoding="utf-8").write(svg)
print("wrote c2_board_q.svg")

# ---------- 도전 3: 재료 → 나만의 퍼즐 설계 ----------
parts = []
# 재료 1: 동전 둘
parts += coin(64, 150, 22, "앞") + coin(116, 150, 22, "뒤")
# 재료 2: 미니 체스판
bs, bx, by = 17, 160, 196
for i in range(4):
    for j in range(4):
        if (i + j) % 2 == 0:
            parts.append(f'<rect x="{bx+i*bs}" y="{by+j*bs}" width="{bs}" height="{bs}" fill="{INK}"/>')
parts.append(f'<rect x="{bx}" y="{by}" width="{4*bs}" height="{4*bs}" fill="none" stroke="{INK}" stroke-width="2"/>')
# 재료 3: 미니 칠판
parts.append(f'<rect x="40" y="196" width="104" height="68" rx="6" fill="{BOARD}" stroke="{INK}" stroke-width="2.6"/>')
parts.append(f'<text x="92" y="238" text-anchor="middle" font-family="{FONT}" font-size="22" fill="{CHALK}">1 2 3</text>')
parts += caption(140, CAP, ["재료: 동전 · 판 · 수 — 무엇이든"])

# 큰 화살표
parts.append(f'<line x1="268" y1="190" x2="330" y2="190" stroke="{INK}" stroke-width="3.5"/>')
parts.append(f'<polygon points="344,190 328,182 328,198" fill="{INK}"/>')

# 나만의 퍼즐 상자
px, py, pw, ph = 360, 92, 300, 196
parts.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="none" stroke="{INK}" stroke-width="3.2"/>')
parts.append(f'<text x="{px+pw/2}" y="{py+52}" text-anchor="middle" font-family="{FONT}" font-size="27" fill="{INK}">나만의 ‘안 되는’ 퍼즐</text>')
parts.append(f'<text x="{px+pw/2}" y="{py+96}" text-anchor="middle" font-family="{FONT}" font-size="22" fill="{INK}">조작 규칙: ______</text>')
parts.append(f'<rect x="{px+38}" y="{py+124}" width="{pw-76}" height="46" rx="8" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="6 5"/>')
parts.append(f'<text x="{px+pw/2}" y="{py+154}" text-anchor="middle" font-family="{FONT}" font-size="20" fill="{INK}">몰래 심은 불변량 (비밀!)</text>')
parts += caption(px + pw / 2, CAP, ["규칙은 단순하게, 불변량은 깊숙이", "— 친구가 충분히 고생해야 좋은 문제"])

W = 700
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("c3_board_q.svg", "w", encoding="utf-8").write(svg)
print("wrote c3_board_q.svg")
