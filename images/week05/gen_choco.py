#!/usr/bin/env python3
"""초콜릿 쪼개기(서브 p5·풀이 5-2) 흑백 스케치 SVG.

- p5_choco_q.svg (문제): 4×6 = 24조각 판초콜릿 + ‘쪼개기 = 한 덩어리 → 두 덩어리’ 규칙.
  풀이 실마리(덩어리 +1 셈) 없음.
- s5_choco_a.svg (풀이 5-2): 2×2로 보는 시퀀스 — 쪼갤 때마다 덩어리 꼭 +1.
실행: python3 gen_choco.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
CHOCO = "#e6e6e6"        # 초콜릿 덩어리 면


def chunk(x, y, cols, rows, cell):
    """cols×rows 초콜릿 덩어리: 굵은 외곽 + 홈(격자) + 조각 베벨."""
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


def arrow(x1, y, x2, label=None):
    p = [f'<line x1="{x1}" y1="{y}" x2="{x2-10}" y2="{y}" stroke="{INK}" stroke-width="3"/>',
         f'<polygon points="{x2},{y} {x2-13},{y-6.5} {x2-13},{y+6.5}" fill="{INK}"/>']
    if label:
        p.append(f'<text x="{(x1+x2)/2}" y="{y-14}" text-anchor="middle" font-family="{FONT}" font-size="18" fill="{INK}">{label}</text>')
    return p


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


CAP, H = 330, 396

# ---------- 문제용: 4×6 판 + 쪼개기 규칙 ----------
parts = []
c = 38
parts += chunk(40, 296 - 4 * c, 6, 4, c)             # 4×6 = 24조각 (가로 6 × 세로 4)
parts += caption(40 + 3 * c, CAP, ["4×6 — 24조각 판초콜릿"])

c2, x0, ym = 30, 388, 190                            # 규칙: 한 덩어리 → 두 덩어리
parts += chunk(x0, ym - c2, 3, 2, c2)
parts.append(f'<line x1="{x0+c2}" y1="{ym-c2-9}" x2="{x0+c2}" y2="{ym+c2+9}" '
             f'stroke="{INK}" stroke-width="2.4" stroke-dasharray="7 5"/>')
parts += arrow(x0 + 3 * c2 + 16, ym, x0 + 3 * c2 + 74)
xr = x0 + 3 * c2 + 88
parts += chunk(xr, ym - c2, 1, 2, c2)
parts += chunk(xr + c2 + 14, ym - c2, 2, 2, c2)
parts += caption((x0 + xr + 3 * c2 + 14) / 2, CAP, ["쪼개기 한 번 = 홈을 따라", "한 덩어리 → 두 덩어리"])

W = 700
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p5_choco_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p5_choco_q.svg")

# ---------- 풀이용: 2×2 시퀀스 — 덩어리 꼭 +1 ----------
parts = []
c = 30
ym = 168                                             # 덩어리 세로 중심
LBL = 296                                            # 덩어리 수 라벨

def state_label(cx, n):
    return caption(cx, LBL, [f"{n}덩어리"], size=20)

x = 36                                               # 상태 0: 2×2 한 덩어리
parts += chunk(x, ym - c, 2, 2, c)
parts += state_label(x + c, 1)
parts += arrow(x + 2 * c + 12, ym, x + 2 * c + 64, "1번")

x = x + 2 * c + 78                                   # 상태 1: 세로로 쪼갬 → 1×2 둘
parts += chunk(x, ym - c, 1, 2, c) + chunk(x + c + 12, ym - c, 1, 2, c)
parts += state_label(x + c + 6, 2)
parts += arrow(x + 2 * c + 24, ym, x + 2 * c + 76, "2번")

x = x + 2 * c + 90                                   # 상태 2: 왼쪽을 또 쪼갬 → 3덩어리
parts += chunk(x, ym - c, 1, 1, c) + chunk(x, ym + 12 - c + c, 1, 1, c) + chunk(x + c + 12, ym - c, 1, 2, c)
parts += state_label(x + c + 6, 3)
parts += arrow(x + 2 * c + 24, ym, x + 2 * c + 76, "3번")

x = x + 2 * c + 90                                   # 상태 3: 모두 분리 → 4덩어리
parts += (chunk(x, ym - c, 1, 1, c) + chunk(x, ym + 12, 1, 1, c)
          + chunk(x + c + 12, ym - c, 1, 1, c) + chunk(x + c + 12, ym + 12, 1, 1, c))
parts += state_label(x + c + 6, 4)

parts += caption(310, CAP + 6, ["쪼갤 때마다 덩어리는 꼭 하나 늘어난다",
                                "— 4조각은 언제나 3번, 24조각은 23번"])

W = 620
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s5_choco_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s5_choco_a.svg")
