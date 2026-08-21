#!/usr/bin/env python3
"""응용 1 · 소금 50g(9주차의 빚) 풀이 - 물 불변 흑백 스케치 SVG.

- s5_water_a.svg (풀이): 물 360g은 그대로 - 20%가 되려면 전체 450g, 소금 90g.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_salt3.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 물 360g이 80%가 되는 전체 = 450g, 소금 = 90g (더 넣은 소금 50g)
assert 400 - 40 == 360
assert 360 / 0.8 == 450 and 450 - 360 == 90 and 90 - 40 == 50


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


parts = []
BX, BH = 70, 54
S = 1.1                                   # 1g = 1.1px
Y1, Y2 = 92, 232
# 넣기 전: 물 360 + 소금 40
parts += label(BX, Y1 - 16, "넣기 전 - 400g (소금 10%)", 20, 700, "start")
parts.append(f'<rect x="{BX}" y="{Y1}" width="{360 * S:.0f}" height="{BH}" fill="{GRAY}" stroke="{INK}" stroke-width="2.2"/>')
parts.append(f'<rect x="{BX + 360 * S:.0f}" y="{Y1}" width="{40 * S:.0f}" height="{BH}" fill="{INK}"/>')
parts += label(BX + 180 * S, Y1 + 35, "물 360g", 20)
parts += label(BX + 424 * S, Y1 + 35, "소금 40g", 17, 400, "start")
# 넣은 뒤: 물 360 + 소금 90
parts += label(BX, Y2 - 16, "넣은 뒤 - ?g (소금 20% = 물 80%)", 20, 700, "start")
parts.append(f'<rect x="{BX}" y="{Y2}" width="{360 * S:.0f}" height="{BH}" fill="{GRAY}" stroke="{INK}" stroke-width="2.2"/>')
parts.append(f'<rect x="{BX + 360 * S:.0f}" y="{Y2}" width="{90 * S:.0f}" height="{BH}" fill="{INK}"/>')
parts += label(BX + 180 * S, Y2 + 35, "물 360g - 그대로!", 20)
parts += label(BX + 460 * S, Y2 + 35, "소금 ?g", 17, 400, "start", )
# 물 불변 연결
parts.append(f'<line x1="{BX + 360 * S:.0f}" y1="{Y1 + BH + 8}" x2="{BX + 360 * S:.0f}" y2="{Y2 - 24}" '
             f'stroke="{INK}" stroke-width="1.6" stroke-dasharray="5 6"/>')
# 오른쪽 계산
parts += label(640, 160, "물 360g이 전체의 80%", 21, 700, "start")
parts += label(640, 200, "→ 전체 = 360 ÷ 0.8 = 450g", 21, 400, "start")
parts += label(640, 240, "→ 더 넣은 소금 = 450 − 400 = 50g", 22, 700, "start")
parts += caption(480, 366, ["소금을 넣어도 물은 변하지 않는다 - 마른 사과의 과육처럼"], 22)
W, H = 1030, 396
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s5_water_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s5_water_a.svg")
