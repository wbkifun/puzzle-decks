#!/usr/bin/env python3
"""칠판 수 지우기 게임(서브 p6·풀이 6-1) 흑백 스케치 SVG.

- p6_board_q.svg (문제): 칠판의 1~10 + 조작 예시 한 번(6·9 지우고 3 적기).
  규칙 시연만 — 합·홀짝 실마리 없음.
- s6_chain_a.svg (풀이 6-1): (a+b)−(a−b)=2b — 합은 짝수만큼만 줄어든다
  → 홀수(55)에서 출발한 홀짝이 끝까지 유지되는 사슬.
실행: python3 gen_erase.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
BOARD = "#3d3d3d"        # 칠판 면
CHALK = "#ffffff"


def chalkboard(x, y, w, h):
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{BOARD}" stroke="{INK}" stroke-width="4"/>']


def chalk_text(cx, cy, s, size=30, color=CHALK):
    return [f'<text x="{cx}" y="{cy}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="{size}" fill="{color}">{s}</text>']


def chalk_strike(cx, cy, r=16):
    return [f'<line x1="{cx-r}" y1="{cy-r+4}" x2="{cx+r}" y2="{cy+r-8}" stroke="{CHALK}" stroke-width="2.6"/>',
            f'<line x1="{cx-r}" y1="{cy+r-8}" x2="{cx+r}" y2="{cy-r+4}" stroke="{CHALK}" stroke-width="2.6"/>']


def arrow(x1, y, x2, label=None):
    p = [f'<line x1="{x1}" y1="{y}" x2="{x2-10}" y2="{y}" stroke="{INK}" stroke-width="3"/>',
         f'<polygon points="{x2},{y} {x2-13},{y-6.5} {x2-13},{y+6.5}" fill="{INK}"/>']
    if label:
        p.append(f'<text x="{(x1+x2)/2}" y="{y-12}" text-anchor="middle" font-family="{FONT}" font-size="17" fill="{INK}">{label}</text>')
    return p


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


CAP, H = 330, 396

# ---------- 문제용: 칠판 1~10 + 조작 예시 ----------
parts = []
bx, by, bw, bh = 28, 82, 300, 178
parts += chalkboard(bx, by, bw, bh)
for k in range(10):                                   # 1~10 두 줄
    cx = bx + 38 + (k % 5) * 57
    cy = by + 60 + (k // 5) * 56
    parts += chalk_text(cx, cy, str(k + 1))
parts += caption(bx + bw / 2, CAP, ["칠판에 1부터 10까지 — 열 개의 수"])

bx2 = 384
parts += chalkboard(bx2, by, bw, bh)
for k in range(10):
    cx = bx2 + 38 + (k % 5) * 57
    cy = by + 60 + (k // 5) * 56
    parts += chalk_text(cx, cy, str(k + 1))
    if k + 1 in (6, 9):                               # 6과 9를 지운다
        parts += chalk_strike(cx, cy - 10)
cx3, cy3 = bx2 + bw / 2, by + 162                     # 새로 적은 3 (셋째 줄 중앙)
parts += chalk_text(cx3, cy3, "3", 32)
parts.append(f'<circle cx="{cx3}" cy="{cy3 - 11}" r="23" fill="none" stroke="{CHALK}" stroke-width="2.4"/>')
parts += caption(bx2 + bw / 2, CAP, ["예: 6과 9를 지우고 차 3을 적는다", "— 이렇게 아홉 번이면 수 하나만 남는다"])

W = 712
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p6_board_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p6_board_q.svg")

# ---------- 풀이용: 홀짝 사슬 ----------
parts = []
parts += caption(330, 74, ["지우기 전 a + b,  적은 후 a − b  —  차이는 (a+b) − (a−b) = 2b", "→ 합은 언제나 ‘짝수만큼’ 줄어든다"], size=23)

def box(x, y, w, h, lines, sub=None):
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="none" stroke="{INK}" stroke-width="2.8"/>']
    cy = y + h / 2 + (0 if sub else 8)
    p.append(f'<text x="{x+w/2}" y="{cy - (10 if sub else 0)}" text-anchor="middle" font-family="{FONT}" font-size="23" fill="{INK}">{lines}</text>')
    if sub:
        p.append(f'<text x="{x+w/2}" y="{cy + 18}" text-anchor="middle" font-family="{FONT}" font-size="19" fill="{INK}">{sub}</text>')
    return p

yb, hb = 168, 74
parts += box(24, yb, 128, hb, "합 55", "홀수")
parts += arrow(160, yb + hb / 2, 224, "−짝수")
parts += box(232, yb, 96, hb, "홀수")
parts += arrow(336, yb + hb / 2, 400, "−짝수")
parts += box(408, yb, 96, hb, "홀수")
parts.append(f'<text x="536" y="{yb + hb/2 + 8}" text-anchor="middle" font-family="{FONT}" font-size="26" fill="{INK}">⋯</text>')
parts += arrow(566, yb + hb / 2, 606)
parts += box(614, yb - 8, 150, hb + 16, "마지막 수", "반드시 홀수")
parts += caption(394, CAP, ["아홉 번을 지나도 홀짝은 그대로 — 0(짝수)은 절대 될 수 없다", "(1은 짝지어 빼기로 실제로 만들 수 있다 — 다음 장)"])

W = 790
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s6_chain_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s6_chain_a.svg")
