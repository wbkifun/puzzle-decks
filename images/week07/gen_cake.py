#!/usr/bin/env python3
"""릴레이 1 · 케이크(칼질 3번, 똑같은 8조각) 흑백 스케치 SVG.

- r1_cake_q.svg (문제): 위에서 본 케이크 - 두 번=네 조각 예시 + 빈 케이크(세 번째 칼 실마리 미노출).
- r1_cake_a.svg (풀이): 십자 두 번(위) + 옆에서 수평 한 칼(옆면) = 8조각.
실행: python3 gen_cake.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 십자 2번 = 4조각, 수평 1번이 조각마다 2배 → 3번으로 8조각
assert 4 * 2 == 8


def caption(cx, y, lines, size=21):
    # 텍스트는 g translate 지역좌표로 - 큰 절대좌표 텍스트가 도형과 다른 배율로
    # 그려지는 크로미움 버그 회피(6주차 확립 규칙)
    t = [f'<g transform="translate({cx},{y})"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="0" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text></g>")
    return ["".join(t)]


def top_cake(cx, cy, r, cross=False):
    p = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>']
    if cross:
        p.append(f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="{INK}" stroke-width="2.2"/>')
        p.append(f'<line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy+r}" stroke="{INK}" stroke-width="2.2"/>')
    return p


def side_cake(cx, cy, rw, rh, h, hcut=False):
    """옆에서 본 케이크(원기둥): 윗면 타원 + 몸통. hcut=수평 절단선."""
    p = [
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rw}" ry="{rh}" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>',
        f'<path d="M {cx-rw} {cy} L {cx-rw} {cy+h} A {rw} {rh} 0 0 0 {cx+rw} {cy+h} L {cx+rw} {cy}" '
        f'fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>',
        # 윗면 타원을 몸통 위에 다시 (겹침 정리)
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rw}" ry="{rh}" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>',
    ]
    if hcut:
        yc = cy + h / 2
        p.append(f'<path d="M {cx-rw} {yc} A {rw} {rh} 0 0 0 {cx+rw} {yc}" '
                 f'fill="none" stroke="{INK}" stroke-width="2.4" stroke-dasharray="9 7"/>')
    return p


# ---------- q: 두 번=네 조각 + 세 번째는? ----------
parts = []
parts += top_cake(150, 150, 92, cross=True)
parts += caption(150, 290, ["칼질 두 번 = 네 조각"], 21)
parts.append(f'<g transform="translate(330,160)"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="{INK}">→</text></g>')
parts += top_cake(510, 150, 92, cross=False)
parts += caption(510, 290, ["세 번째 칼은 어디에?"], 21)
parts += caption(330, 348, ["크기가 똑같은 여덟 조각 - 칼질은 딱 세 번"], 22)
W, H = 660, 376
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r1_cake_q.svg", "w", encoding="utf-8").write(svg)
print("wrote r1_cake_q.svg")

# ---------- a: 십자(위) + 수평 한 칼(옆) ----------
parts = []
parts += top_cake(140, 140, 88, cross=True)
parts += caption(140, 272, ["위에서 십자 - 칼질 두 번"], 21)
parts.append(f'<g transform="translate(300,150)"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="{INK}">＋</text></g>')
parts += side_cake(480, 88, 92, 20, 116, hcut=True)
# 수평 절단을 가리키는 화살표
parts.append(f'<line x1="612" y1="146" x2="586" y2="146" stroke="{INK}" stroke-width="2.8"/>')
parts.append(f'<polygon points="578,146 592,139 592,153" fill="{INK}"/>')
parts.append(f'<g transform="translate(622,153)"><text x="0" y="0" font-family="{FONT}" font-size="21" font-weight="700" fill="{INK}">옆에서 수평으로 한 칼</text></g>')
parts += caption(480, 272, ["높이 절반을 가른다 - 칼질 한 번"], 21)
parts += caption(410, 330, ["4조각이 각각 위아래로 - 4 × 2 = 8조각 · 칼의 방향은 문제가 정하지 않았다"], 22)
W, H = 860, 358
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r1_cake_a.svg", "w", encoding="utf-8").write(svg)
print("wrote r1_cake_a.svg")
