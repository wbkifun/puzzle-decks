#!/usr/bin/env python3
"""워밍업 1 · 회상(C6 동전 2개) 흑백 스케치 SVG.

- w1_coins_q.svg (문제): ? 동전 두 개 + 합 600원 - 정답 실마리 미노출.
- w1_coins_a.svg (풀이): 500원 + 100원, '하나는 500원이 아니다'가 가리키는 쪽 표시.
실행: python3 gen_coins.py
"""

INK = "#111111"
GRAY = "#d7d7d7"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 500 + 100 = 600, 100은 500이 아니다(문장 참)
assert 500 + 100 == 600
assert 100 != 500


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


def coin(cx, cy, r, label, size=26, fill="#ffffff"):
    return [
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2.8"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r-7}" fill="none" stroke="{INK}" stroke-width="1.3"/>',
        f'<text x="{cx}" y="{cy+size*0.34}" text-anchor="middle" font-family="{FONT}" font-size="{size}" font-weight="700" fill="{INK}">{label}</text>',
    ]


# ---------- q: ? 동전 두 개 ----------
parts = []
parts += coin(150, 120, 42, "?", 34)
parts.append(f'<text x="240" y="132" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="700" fill="{INK}">+</text>')
parts += coin(330, 120, 42, "?", 34)
parts.append(f'<text x="420" y="132" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="700" fill="{INK}">=</text>')
parts.append(f'<text x="510" y="132" text-anchor="middle" font-family="{FONT}" font-size="32" font-weight="700" fill="{INK}">600원</text>')
parts += caption(330, 230, ["하나는 500원짜리가 아니다 - 무슨 동전 두 개일까?"], 22)
W, H = 660, 260
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("w1_coins_q.svg", "w", encoding="utf-8").write(svg)
print("wrote w1_coins_q.svg")

# ---------- a: 500 + 100, '하나'가 가리키는 쪽 ----------
parts = []
parts += coin(160, 110, 44, "500")
parts.append(f'<text x="255" y="122" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="700" fill="{INK}">+</text>')
parts += coin(350, 110, 36, "100", 24, GRAY)
parts.append(f'<text x="445" y="122" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="700" fill="{INK}">=</text>')
parts.append(f'<text x="535" y="122" text-anchor="middle" font-family="{FONT}" font-size="32" font-weight="700" fill="{INK}">600원</text>')
# '하나'를 가리키는 화살표
parts.append(f'<line x1="350" y1="196" x2="350" y2="160" stroke="{INK}" stroke-width="2.4"/>')
parts.append(f'<polygon points="350,152 343.5,166 356.5,166" fill="{INK}"/>')
parts.append(f'<text x="350" y="224" text-anchor="middle" font-family="{FONT}" font-size="21" fill="{INK}">\'하나\'는 이 동전 - 500원짜리가 아니다 (참!)</text>')
parts += caption(350, 276, ["문장은 \'500원짜리가 없다\'고 말한 적이 없다"], 22)
W, H = 700, 306
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("w1_coins_a.svg", "w", encoding="utf-8").write(svg)
print("wrote w1_coins_a.svg")
