#!/usr/bin/env python3
"""워밍업 1 · 숫자 마술 규칙 카드 흑백 스케치 SVG.

- w1_cards_q.svg (문제): 규칙 카드 4장 (×2, +10, ÷2, -처음 수) - 답 미노출.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_cards.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 3과 10과 0.6 모두 5
for x in (3, 10, 0.6):
    assert ((x * 2 + 10) / 2) - x == 5


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


def card(cx, cy, big, small, w=132, h=150, big_size=34):
    p = [f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="14" '
         f'fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>',
         f'<rect x="{cx - w / 2 + 9}" y="{cy - h / 2 + 9}" width="{w - 18}" height="{h - 18}" rx="9" '
         f'fill="none" stroke="{INK}" stroke-width="1.2"/>']
    p += label(cx, cy + 2, big, big_size, 700)
    p += label(cx, cy + 46, small, 16)
    return p


def arrow_r(x1, x2, y, sw=2.6):
    return [f'<line x1="{x1}" y1="{y}" x2="{x2 - 12}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
            f'<polygon points="{x2},{y} {x2 - 16},{y - 8} {x2 - 16},{y + 8}" fill="{INK}"/>']


parts = []
CY = 170
xs = [120, 320, 520, 720]
cards = [("×2", "두 배로", 34), ("+10", "10을 더해", 34), ("÷2", "반으로", 34), ("−처음 수", "고른 수를 빼", 25)]
for (bx, (big, small, bs)) in zip(xs, cards):
    parts += card(bx, CY, big, small, big_size=bs)
for a, b in zip(xs[:-1], xs[1:]):
    parts += arrow_r(a + 70, b - 70, CY)
parts += label(120, 60, "마음속으로 아무 수나 골라 -", 21, 700, "start")
parts += caption(420, 320, ["네 장의 카드를 차례로 통과시키면 - 어떤 수가 남을까?"], 22)
W, H = 840, 350
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("w1_cards_q.svg", "w", encoding="utf-8").write(svg)
print("wrote w1_cards_q.svg")
