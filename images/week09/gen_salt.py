#!/usr/bin/env python3
"""본 문제 1 · 소금물 섞기 흑백 스케치 SVG.

- p1_salt_q.svg (문제): 10% 300g + 40% 100g -> 섞으면 몇 %? (답 실마리 미노출)
- s1_salt_a.svg (풀이): 본체(소금 g)로 - 30g + 40g = 70g / 400g = 17.5%.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_salt.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 소금 본체 30+40=70g, 소금물 400g -> 17.5%
assert 300 * 0.10 == 30 and 100 * 0.40 == 40
assert (30 + 40) / (300 + 100) == 0.175


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


def beaker(x, y, w, h, water_h, salt_h=0):
    """열린 비커: (x,y)=왼쪽 위. 물은 회색, 소금(풀이용)은 바닥 검정 띠."""
    p = []
    if water_h:
        p.append(f'<rect x="{x}" y="{y + h - water_h}" width="{w}" height="{water_h - salt_h}" fill="{GRAY}"/>')
    if salt_h:
        p.append(f'<rect x="{x}" y="{y + h - salt_h}" width="{w}" height="{salt_h}" fill="{INK}"/>')
    p.append(f'<path d="M {x} {y} L {x} {y + h} L {x + w} {y + h} L {x + w} {y}" '
             f'fill="none" stroke="{INK}" stroke-width="2.8"/>')
    return p


def arrow(x1, y1, x2, y2, sw=2.4):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    ux, uy = math.cos(ang), math.sin(ang)
    p = [f'<line x1="{x1}" y1="{y1}" x2="{x2 - 10 * ux:.1f}" y2="{y2 - 10 * uy:.1f}" stroke="{INK}" stroke-width="{sw}"/>',
         f'<polygon points="{x2},{y2} {x2 - 15 * ux - 7 * uy:.1f},{y2 - 15 * uy + 7 * ux:.1f} '
         f'{x2 - 15 * ux + 7 * uy:.1f},{y2 - 15 * uy - 7 * ux:.1f}" fill="{INK}"/>']
    return p


# ---------- q: 두 비커 -> 큰 그릇 ----------
parts = []
# A: 300g(물 높이 120), B: 100g(물 높이 40) - 폭 동일, 높이로 양 표현
parts += label(135, 84, "소금물 A - 농도 10%", 20, 700)
parts += beaker(80, 100, 110, 150, 120)
parts += label(135, 284, "300g", 21)
parts += label(245, 200, "+", 34, 700)
parts += label(355, 84, "소금물 B - 농도 40%", 20, 700)
parts += beaker(300, 100, 110, 150, 40)
parts += label(355, 284, "100g", 21)
# 큰 그릇
parts += arrow(450, 192, 530, 192)
parts += beaker(545, 120, 170, 160, 128)
parts += label(630, 226, "농도 ?%", 25, 700)
parts += caption(390, 372, ["두 소금물을 한 그릇에 모두 붓는다 - 농도는 몇 %가 될까?"], 22)
W, H = 780, 400
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p1_salt_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p1_salt_q.svg")

# ---------- a: 소금 본체로 ----------
parts = []
parts += label(135, 84, "300g의 10%", 20, 700)
parts += beaker(80, 100, 110, 150, 120, salt_h=12)
parts += label(135, 284, "소금 30g", 21, 700)
parts += label(245, 200, "+", 34, 700)
parts += label(355, 84, "100g의 40%", 20, 700)
parts += beaker(300, 100, 110, 150, 40, salt_h=16)
parts += label(355, 284, "소금 40g", 21, 700)
parts += arrow(450, 192, 530, 192)
parts += beaker(545, 120, 170, 160, 128, salt_h=22)
parts += label(630, 90, "소금물 400g", 20, 700)
parts += label(630, 314, "소금 70g", 21, 700)
parts += label(760, 180, "농도 = 70 ÷ 400", 22, 700, "start")
parts += label(760, 216, "= 17.5%", 24, 700, "start")
parts += label(760, 262, "(10+40)÷2 = 25%는", 19, 400, "start")
parts += label(760, 288, "양이 같을 때만 맞는다", 19, 400, "start")
parts += caption(500, 386, ["%는 더하거나 평균 낼 수 없다 - 본체(소금 g)는 더할 수 있다"], 22)
W, H = 1000, 414
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s1_salt_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s1_salt_a.svg")
