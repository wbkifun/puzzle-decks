#!/usr/bin/env python3
"""워밍업 2 · 가격 20% 인상 후 20% 인하(풀이) 흑백 스케치 SVG.

- ws2_price_a.svg (풀이): 10,000 -> 12,000 -> 9,600. 같은 20%라도 기준량이 다르다.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_price.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증
assert 10000 * 1.2 == 12000 and 12000 * 0.8 == 9600
assert 10000 * 1.2 * 0.8 == 9600


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


def tag(cx, cy, text, fill="#ffffff"):
    w, h = 180, 66
    p = [f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{INK}" stroke-width="2.6"/>']
    p += label(cx, cy + 8, text, 24, 700)
    return p


def arrow_r(x1, x2, y, sw=2.6):
    return [f'<line x1="{x1}" y1="{y}" x2="{x2 - 12}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
            f'<polygon points="{x2},{y} {x2 - 16},{y - 8} {x2 - 16},{y + 8}" fill="{INK}"/>']


parts = []
Y = 150
parts += tag(150, Y, "10,000원")
parts += tag(450, Y, "12,000원")
parts += tag(750, Y, "9,600원", fill=GRAY)
parts += arrow_r(250, 350, Y)
parts += arrow_r(550, 650, Y)
parts += label(300, Y - 44, "20% 인상", 21, 700)
parts += label(300, Y + 62, "기준: 10,000원", 19)
parts += label(300, Y + 88, "→ +2,000원", 19)
parts += label(600, Y - 44, "20% 인하", 21, 700)
parts += label(600, Y + 62, "기준: 12,000원", 19)
parts += label(600, Y + 88, "→ -2,400원", 19)
parts += caption(450, 300, ["같은 '20%'라도 기준량이 다르면 다른 돈이다 - ×1.2×0.8 = ×0.96"], 22)
W, H = 900, 330
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("ws2_price_a.svg", "w", encoding="utf-8").write(svg)
print("wrote ws2_price_a.svg")
