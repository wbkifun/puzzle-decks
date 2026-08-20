#!/usr/bin/env python3
"""사다리 스텝 3·4 · 상자 그림(수를 모르는 채 따라가기) 흑백 스케치 SVG.

- r3_boxes_q.svg  (문제): 상자 파이프라인 - ×2, +10까지 그림으로, ÷2는 물음표.
- sr3_half_a.svg  (확인): 상자 2 + 구슬 10을 반으로 - 상자 1 + 구슬 5.
- sr4_gone_a.svg  (확인): -처음 수에서 상자가 사라진다 - 구슬 5개만 남는다.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_boxes.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

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


# ---------- q: ×2, +10까지 - ÷2는 물음표 ----------
parts = []
Y = 130
parts += label(95, 84, "고른 수 = 상자", 19, 700)
parts += box(75, Y)
parts += arrow_r(140, 190, Y + 20)
parts += label(165, Y - 6, "×2", 19, 700)
parts += box(200, Y)
parts += box(248, Y)
parts += arrow_r(315, 365, Y + 20)
parts += label(340, Y - 6, "+10", 19, 700)
parts += box(375, Y)
parts += box(423, Y)
parts += beads(492, Y + 10, 10)
parts += arrow_r(608, 658, Y + 20)
parts += label(633, Y - 6, "÷2", 19, 700)
parts += label(700, Y + 28, "?", 40, 700)
parts += caption(400, 268, ["상자 두 개와 구슬 열 개 - 반으로 나누면 어떤 그림이 될까?"], 22)
W, H = 800, 300
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r3_boxes_q.svg", "w", encoding="utf-8").write(svg)
print("wrote r3_boxes_q.svg")

# ---------- a: 반으로 나누기 ----------
parts = []
Y = 120
parts += box(80, Y)
parts += box(128, Y)
parts += beads(197, Y + 10, 10)
parts += label(190, Y + 84, "상자 2 + 구슬 10", 19)
# 가운데 절단선 + 화살표
parts += arrow_r(320, 385, Y + 20)
parts += label(352, Y - 6, "÷2", 20, 700)
parts += box(405, Y)
parts += beads(474, Y + 10, 5)
parts += label(490, Y + 84, "상자 1 + 구슬 5", 19)
parts += caption(330, 262, ["반으로 나누면 - 상자 하나와 구슬 다섯: '고른 수 + 5'"], 22)
W, H = 660, 292
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("sr3_half_a.svg", "w", encoding="utf-8").write(svg)
print("wrote sr3_half_a.svg")

# ---------- a: 상자가 사라진다 ----------
parts = []
Y = 120
parts += box(80, Y)
parts += beads(149, Y + 10, 5)
parts += label(140, Y + 84, "상자 1 + 구슬 5", 19)
parts += arrow_r(270, 335, Y + 20)
parts += label(302, Y - 6, "−처음 수", 19, 700)
parts += box(355, Y, crossed=True)
parts += beads(444, Y + 10, 5)
parts += label(430, Y + 84, "상자가 지워진다", 19)
parts += label(600, Y + 34, "= 5", 34, 700)
parts += caption(360, 262, ["무엇이 들어 있었든 - 상자는 반드시 지워지도록 설계되어 있었다"], 22)
W, H = 720, 292
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("sr4_gone_a.svg", "w", encoding="utf-8").write(svg)
print("wrote sr4_gone_a.svg")
