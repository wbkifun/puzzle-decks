#!/usr/bin/env python3
"""저울·동전 문제(회상 p1, 서브 p5, 도전 c2)와 풀이(s1, s5) 흑백 스케치 SVG.

- p1_coins_q.svg (문제): 똑같은 동전 9개 + 양팔 저울 ‘2번’. 3·3·3 실마리 없음.
- s1_scale_a.svg (풀이): 저울 한 번 = 대답 3가지 → 9 → 3 → 1 두 계단.
- p5_coins27_q.svg (문제): 동전 27개 + 저울 ‘3번’.
- s5_tree_a.svg  (풀이): 27 → 9 → 3 → 1 세 계단 + 3의 사다리, 2번 한계(3²=9<27).
- c2_coins12_q.svg (문제): 동전 12개, 무거운지 가벼운지 모름 + 저울 3번.
실행: python3 gen_scale.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


def coin(cx, cy, r):
    return [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2.4"/>']


def scale(cx, cy, s=1.0):
    """양팔 저울(수평) 아이콘. s = 배율."""
    p = []
    bw, ph = 150 * s, 44 * s                          # 빔 폭, 접시 내림 길이
    p.append(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy+56*s}" stroke="{INK}" stroke-width="{4*s}"/>')       # 기둥
    p.append(f'<line x1="{cx-34*s}" y1="{cy+56*s}" x2="{cx+34*s}" y2="{cy+56*s}" stroke="{INK}" stroke-width="{4*s}"/>')  # 받침
    p.append(f'<line x1="{cx-bw/2}" y1="{cy}" x2="{cx+bw/2}" y2="{cy}" stroke="{INK}" stroke-width="{4*s}"/>')  # 빔
    for sgn in (-1, 1):
        px = cx + sgn * bw / 2
        p.append(f'<line x1="{px}" y1="{cy}" x2="{px}" y2="{cy+ph}" stroke="{INK}" stroke-width="{2.6*s}"/>')
        p.append(f'<path d="M {px-26*s} {cy+ph} A {26*s} {20*s} 0 0 0 {px+26*s} {cy+ph}" fill="none" stroke="{INK}" stroke-width="{3*s}"/>')
    return p


def coin_grid(x0, y0, n, cols, r=15, gap=8):
    p = []
    for k in range(n):
        cx = x0 + (k % cols) * (2 * r + gap) + r
        cy = y0 + (k // cols) * (2 * r + gap) + r
        p += coin(cx, cy, r)
    return p


def box(x, y, w, h, text, size=23, bold=False):
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>',
            f'<text x="{x+w/2}" y="{y+h/2+size*0.34}" text-anchor="middle" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{700 if bold else 400}" fill="{INK}">{text}</text>']


def fan(x1, y, x2, label):
    """세 갈래 화살표 묶음(위·중앙·아래) + 라벨 = 대답 3가지."""
    import math
    p = []
    for dy in (-26, 0, 26):
        ang = math.atan2(dy * 0.55, x2 - x1)
        ex, ey = x2, y + dy * 0.55
        bx, by = ex - 13 * math.cos(ang), ey - 13 * math.sin(ang)
        p.append(f'<line x1="{x1}" y1="{y+dy*0.2:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{INK}" stroke-width="2.4"/>')
        ux, uy = math.cos(ang), math.sin(ang)
        p.append(f'<polygon points="{ex},{ey:.1f} {ex-14*ux+6*uy:.1f},{ey-14*uy-6*ux:.1f} {ex-14*ux-6*uy:.1f},{ey-14*uy+6*ux:.1f}" fill="{INK}"/>')
    p.append(f'<text x="{(x1+x2)/2}" y="{y-38}" text-anchor="middle" font-family="{FONT}" font-size="18" fill="{INK}">{label}</text>')
    return p


# ---------- p1 문제: 동전 9개 + 저울 2번 ----------
parts = []
parts += coin_grid(60, 60, 9, 3, r=25, gap=14)
parts += caption(60 + 96, 320, ["똑같이 생긴 9개 —", "1개만 살짝 가볍다"])
parts += scale(470, 120, 1.15)
parts.append(f'<text x="470" y="268" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="{INK}">× 2번</text>')
parts += caption(470, 320, ["저울은 딱 2번 —", "어떻게 달아야 찾을 수 있을까?"])
W, H = 660, 372
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p1_coins_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p1_coins_q.svg")

# ---------- s1 풀이: 9 → 3 → 1 (대답 3가지) ----------
parts = []
y = 150
parts += box(30, y - 32, 150, 64, "후보 9개", 25, bold=True)
parts += fan(192, y, 302, "3개 ⚖ 3개")
parts += box(314, y - 32, 210, 64, "어느 대답이든 3개", 22)
parts += fan(536, y, 646, "1개 ⚖ 1개")
parts += box(658, y - 32, 150, 64, "후보 1개!", 25, bold=True)
parts += caption(300, 78, ["대답은 셋 중 하나 — 왼쪽 가벼움 · 균형 · 오른쪽 가벼움"], 22)
parts += caption(420, 268, ["한 번의 저울질이 후보를 셋으로 가른다 → 9 → 3 → 1, 두 계단이면 끝",
                            "1번이 안 되는 이유: 대답 3가지 < 후보 9개"])
W, H = 840, 330
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s1_scale_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s1_scale_a.svg")

# ---------- p5 문제: 동전 27개 + 저울 3번 ----------
parts = []
for g in range(3):                                   # 9개씩 세 덩이
    parts += coin_grid(40 + g * 128, 56, 9, 3, r=16, gap=8)
parts += caption(40 + 128 + 56, 310, ["똑같이 생긴 27개 — 1개만 살짝 가볍다"])
parts += scale(560, 110, 1.05)
parts.append(f'<text x="560" y="248" text-anchor="middle" font-family="{FONT}" font-size="28" font-weight="700" fill="{INK}">× 3번</text>')
parts += caption(560, 310, ["3번이면 찾을 수 있을까?", "그리고 2번으로는 왜 안 될까?"])
W, H = 730, 362
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p5_coins27_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p5_coins27_q.svg")

# ---------- s5 풀이: 27 → 9 → 3 → 1 + 3의 사다리 ----------
parts = []
y = 120
parts += box(24, y - 30, 128, 60, "27개", 25, bold=True)
parts += fan(160, y, 246, "9 ⚖ 9")
parts += box(256, y - 30, 100, 60, "9개", 25)
parts += fan(364, y, 450, "3 ⚖ 3")
parts += box(460, y - 30, 100, 60, "3개", 25)
parts += fan(568, y, 654, "1 ⚖ 1")
parts += box(664, y - 30, 110, 60, "1개!", 25, bold=True)
parts += caption(400, 230, ["세 계단이면 끝 — 저울 n번은 후보 3ⁿ개까지 (3의 사다리: 3 · 9 · 27)"], 22)
parts += caption(400, 292, ["2번의 기록은 3² = 9가지뿐 < 후보 27개 → 2번으론 절대 안 된다"], 22)
W, H = 800, 330
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s5_tree_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s5_tree_a.svg")

# ---------- c2 문제: 동전 12개, 무거운지 가벼운지 모름 ----------
parts = []
parts += coin_grid(46, 66, 12, 4, r=20, gap=11)
parts += caption(46 + 102, 316, ["12개 중 가짜 1개 —", "무거운지 가벼운지도 모른다"])
parts += scale(520, 112, 1.05)
parts.append(f'<text x="520" y="250" text-anchor="middle" font-family="{FONT}" font-size="28" font-weight="700" fill="{INK}">× 3번?</text>')
parts += caption(520, 316, ["전략을 짜기 전에 —", "먼저 ‘경우의 수’를 세어 보라"])
W, H = 700, 372
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("c2_coins12_q.svg", "w", encoding="utf-8").write(svg)
print("wrote c2_coins12_q.svg")
