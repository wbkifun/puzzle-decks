#!/usr/bin/env python3
"""본 문제 2 · 소금을 넣어 두 배 진하게? 흑백 스케치 SVG.

- p2_salt2_q.svg (문제): 10% 400g에 소금 40g을 더 넣으면 20%? (답 실마리 미노출)
- s2_salt2_a.svg (풀이): 분자와 분모가 같이 변한다 - 80/440=18.2%, 답은 50g.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_salt2.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 40g을 넣으면 80/440 = 18.18..% (20% 아님), 50g을 넣으면 90/450 = 20%
assert abs((40 + 40) / (400 + 40) - 0.18181818) < 1e-6
assert (40 + 50) / (400 + 50) == 0.2


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
    p = []
    if water_h:
        p.append(f'<rect x="{x}" y="{y + h - water_h}" width="{w}" height="{water_h - salt_h}" fill="{GRAY}"/>')
    if salt_h:
        p.append(f'<rect x="{x}" y="{y + h - salt_h}" width="{w}" height="{salt_h}" fill="{INK}"/>')
    p.append(f'<path d="M {x} {y} L {x} {y + h} L {x + w} {y + h} L {x + w} {y}" '
             f'fill="none" stroke="{INK}" stroke-width="2.8"/>')
    return p


def pouch(cx, cy, text):
    """소금 봉지: 묶인 주머니 모양."""
    p = [f'<path d="M {cx - 34} {cy + 30} Q {cx - 40} {cy - 12} {cx - 10} {cy - 22} '
         f'L {cx + 10} {cy - 22} Q {cx + 40} {cy - 12} {cx + 34} {cy + 30} '
         f'Q {cx} {cy + 44} {cx - 34} {cy + 30} Z" fill="#ffffff" stroke="{INK}" stroke-width="2.4"/>',
         f'<line x1="{cx - 12}" y1="{cy - 22}" x2="{cx - 7}" y2="{cy - 34}" stroke="{INK}" stroke-width="2"/>',
         f'<line x1="{cx + 12}" y1="{cy - 22}" x2="{cx + 7}" y2="{cy - 34}" stroke="{INK}" stroke-width="2"/>']
    p += label(cx, cy - 48, text, 19, 700)
    return p


def arrow(x1, y1, x2, y2, sw=2.4):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    ux, uy = math.cos(ang), math.sin(ang)
    return [f'<line x1="{x1}" y1="{y1}" x2="{x2 - 10 * ux:.1f}" y2="{y2 - 10 * uy:.1f}" stroke="{INK}" stroke-width="{sw}"/>',
            f'<polygon points="{x2},{y2} {x2 - 15 * ux - 7 * uy:.1f},{y2 - 15 * uy + 7 * ux:.1f} '
            f'{x2 - 15 * ux + 7 * uy:.1f},{y2 - 15 * uy - 7 * ux:.1f}" fill="{INK}"/>']


# ---------- q ----------
parts = []
parts += label(190, 84, "농도 10% - 400g", 21, 700)
parts += beaker(120, 100, 140, 160, 130)
parts += pouch(420, 130, "소금 40g")
parts += arrow(420, 178, 300, 235)
parts += label(430, 230, "(든 소금과 같은 양을", 18, 400, "start")
parts += label(430, 256, "한 번 더 넣는다)", 18, 400, "start")
parts += caption(360, 340, ["소금이 두 배가 되면 - 농도도 두 배(20%)가 될까?"], 22)
W, H = 720, 370
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p2_salt2_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p2_salt2_q.svg")

# ---------- a: 분수의 위아래가 같이 변한다 ----------
parts = []


def frac(cx, top, bottom, res, y=150, tw=170):
    p = []
    p += label(cx, y - 26, top, 22, 700)
    p.append(f'<line x1="{cx - tw / 2}" y1="{y}" x2="{cx + tw / 2}" y2="{y}" stroke="{INK}" stroke-width="2.6"/>')
    p += label(cx, y + 38, bottom, 22, 400)
    p += label(cx, y + 96, res, 23, 700)
    return p


parts += label(210, 60, "소금 40g을 넣으면", 21, 700)
parts += frac(210, "소금 40 + 40 = 80", "전체 400 + 40 = 440", "= 18.2% - 모자란다!")
parts.append(f'<line x1="430" y1="150" x2="430" y2="230" stroke="{INK}" stroke-width="1.6" stroke-dasharray="6 7"/>')
parts += label(680, 60, "20%가 되려면 - 50g", 21, 700)
parts += frac(680, "소금 40 + 50 = 90", "전체 400 + 50 = 450", "= 20% - 검산 완료")
parts += caption(450, 320, ["넣은 소금은 분자에도, 분모(기준량)에도 들어간다 - 마른 사과의 거울상"], 22)
W, H = 900, 350
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s2_salt2_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s2_salt2_a.svg")
