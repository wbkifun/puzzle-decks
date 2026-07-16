#!/usr/bin/env python3
"""메인 ③(p4 · 62칸)과 풀이 4-2용 흑백 스케치 SVG 생성.

- p4_board_q.svg (문제): 마주 보는 두 모서리를 뗀 62칸 판(순수한 부재로 표현)
  + 1×2 도미노 타일 ×31 — 풀이 실마리(색 강조) 없음.
- p4_board_a.svg (풀이 4-2): 도미노는 어디 놓아도 검1+흰1(4×4 강조 패널)
  + 떼어낸 두 모서리가 같은 색(검)임을 고스트 칸으로 표시.
실행: python3 gen_p4_board.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
REMOVED = {(0, 0), (7, 7)}      # 왼쪽 아래·오른쪽 위 (bottom 기준, 둘 다 검은 칸)


def cell_xy(x0, y0, n, cell, i, j):
    """(i,j) bottom 기준 → SVG 좌상단 좌표."""
    return x0 + i * cell, y0 + (n - 1 - j) * cell


def notched_board(x0, y0, n, cell, removed, ghost=None):
    """모서리를 뗀 체스판. ghost: None=순수 부재, "neutral"=점선+✕(색 미노출, 문제용),
    "dark"=회색 점선 고스트(원래 검은 칸이었음을 표시, 풀이용)."""
    p = []
    for i in range(n):
        for j in range(n):
            if (i, j) in removed:
                continue
            x, y = cell_xy(x0, y0, n, cell, i, j)
            fill = INK if (i + j) % 2 == 0 else "none"
            p.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                     f'fill="{fill}" stroke="{INK}" stroke-width="1.4"/>')
    # 바깥 윤곽(노치 포함)을 굵게 — bottom 기준 꼭짓점 나열 후 y 뒤집기
    pts_b = [(1, 0), (n, 0), (n, n - 1), (n - 1, n - 1), (n - 1, n), (0, n), (0, 1), (1, 1)]
    pts = " ".join(f"{x0 + px*cell},{y0 + (n - py)*cell}" for px, py in pts_b)
    p.append(f'<polygon points="{pts}" fill="none" stroke="{INK}" stroke-width="3"/>')
    if ghost:
        fill = "#9a9a9a" if ghost == "dark" else "none"
        for (i, j) in removed:
            x, y = cell_xy(x0, y0, n, cell, i, j)
            m = 0.09 * cell
            p.append(f'<rect x="{x+m}" y="{y+m}" width="{cell-2*m}" height="{cell-2*m}" '
                     f'fill="{fill}" stroke="{INK}" stroke-width="2" stroke-dasharray="5 4"/>')
            if ghost == "neutral":                      # ✕ — ‘떼어냈음’만 표시
                a, b = x + 0.26 * cell, x + 0.74 * cell
                u, v = y + 0.26 * cell, y + 0.74 * cell
                p.append(f'<line x1="{a}" y1="{u}" x2="{b}" y2="{v}" stroke="{INK}" stroke-width="2"/>')
                p.append(f'<line x1="{a}" y1="{v}" x2="{b}" y2="{u}" stroke="{INK}" stroke-width="2"/>')
    return p


def board(x0, y0, n, cell, sw_grid=1.5, sw_frame=3):
    """좌하단이 검은 칸인 n×n 체스판."""
    p = []
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                x, y = cell_xy(x0, y0, n, cell, i, j)
                p.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{INK}"/>')
    for k in range(n + 1):
        p.append(f'<line x1="{x0 + k*cell}" y1="{y0}" x2="{x0 + k*cell}" y2="{y0 + n*cell}" stroke="{INK}" stroke-width="{sw_grid}"/>')
        p.append(f'<line x1="{x0}" y1="{y0 + k*cell}" x2="{x0 + n*cell}" y2="{y0 + k*cell}" stroke="{INK}" stroke-width="{sw_grid}"/>')
    p.append(f'<rect x="{x0}" y="{y0}" width="{n*cell}" height="{n*cell}" fill="none" stroke="{INK}" stroke-width="{sw_frame}"/>')
    return p


def pair_outline(x, y, w, h):
    return [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="#ffffff" stroke-width="7.5"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{INK}" stroke-width="4"/>',
    ]


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


BOT, CAP = 296, 330


def fig_q():
    """문제용: 62칸 판(부재로 표현) + 1×2 도미노 ×31."""
    parts = []
    c = 33
    parts += notched_board(40, BOT - 8 * c, 8, c, REMOVED, ghost="neutral")
    parts += caption(40 + 4 * c, CAP, ["마주 보는 두 모서리를 뗀 62칸"])

    # 도미노 타일(빈 1×2, 반쪽 구분선) + ×31
    dc, dx = 46, 452
    dy = BOT - 4.6 * c
    parts += [
        f'<rect x="{dx}" y="{dy}" width="{2*dc}" height="{dc}" rx="8" fill="none" stroke="{INK}" stroke-width="3.5"/>',
        f'<line x1="{dx+dc}" y1="{dy+4}" x2="{dx+dc}" y2="{dy+dc-4}" stroke="{INK}" stroke-width="2"/>',
        f'<text x="{dx + 2*dc + 18}" y="{dy + dc*0.68}" font-family="{FONT}" font-size="30" fill="{INK}">× 31</text>',
    ]
    parts += caption(dx + 1.6 * dc, CAP, ["도미노 = 이웃 두 칸을 덮는 타일", "62칸 ÷ 2 = 31개, 개수는 딱 맞다"])
    return parts, 700


def fig_a():
    """풀이 4-2용: 도미노=검1+흰1 강조 + 떼어낸 두 모서리는 같은 색."""
    parts = []
    c3, x3 = 46, 24
    y3 = BOT - 4 * c3
    parts += board(x3, y3, 4, c3)
    parts += pair_outline(x3 + 0.03 * c3, y3 + 1.03 * c3, 1.94 * c3, 0.94 * c3)
    parts += pair_outline(x3 + 2.03 * c3, y3 + 2.03 * c3, 0.94 * c3, 1.94 * c3)
    parts += caption(x3 + 2 * c3, CAP, ["도미노는 어디에 놓아도", "검 1 + 흰 1"])

    c, x2 = 33, 330
    parts += notched_board(x2, BOT - 8 * c, 8, c, REMOVED, ghost="dark")
    parts += caption(x2 + 4 * c, CAP, ["떼어낸 두 모서리는 같은 색", "— 둘 다 검은 칸"])
    return parts, 640


for name, (parts, W) in {"p4_board_q.svg": fig_q(), "p4_board_a.svg": fig_a()}.items():
    H = 396
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">\n' + "\n".join(parts) + "\n</svg>\n")
    open(name, "w", encoding="utf-8").write(svg)
    print("wrote", name)
