#!/usr/bin/env python3
"""워밍업 2 · 회상(C8 방 탈출) 흑백 스케치 SVG.

- w2_door_q.svg (문제): 문 + 당기는 화살표 - '미는 문' 실마리 미노출.
- w2_door_a.svg (풀이): 살짝 열린 문 + 미는 화살표.
실행: python3 gen_door.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"


def caption(cx, y, lines, size=21):
    # 텍스트는 g translate 지역좌표로 - 큰 절대좌표 텍스트가 도형과 다른 배율로
    # 그려지는 크로미움 버그 회피(6주차 확립 규칙)
    t = [f'<g transform="translate({cx},{y})"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="0" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text></g>")
    return ["".join(t)]


def frame(x, y, w, h):
    """문틀(이중선) - 문은 별도로 그린다."""
    return [
        f'<rect x="{x-12}" y="{y-12}" width="{w+24}" height="{h+12}" fill="none" stroke="{INK}" stroke-width="3"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="1.6"/>',
    ]


def arrow_r(x1, x2, y, sw=3.0):
    return [
        f'<line x1="{x1}" y1="{y}" x2="{x2-12}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
        f'<polygon points="{x2},{y} {x2-14},{y-7} {x2-14},{y+7}" fill="{INK}"/>',
    ]


def arrow_l(x1, x2, y, sw=3.0):
    """x1(오른쪽)에서 x2(왼쪽)로 - 화살촉이 왼쪽을 향한다."""
    return [
        f'<line x1="{x1}" y1="{y}" x2="{x2+12}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
        f'<polygon points="{x2},{y} {x2+14},{y-7} {x2+14},{y+7}" fill="{INK}"/>',
    ]


# ---------- q: 닫힌 문 + 당기는 화살표 ----------
parts = []
dx, dy, dw, dh = 120, 60, 170, 260
parts += frame(dx, dy, dw, dh)
parts.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>')
parts.append(f'<circle cx="{dx+dw-26}" cy="{dy+dh*0.52}" r="9" fill="none" stroke="{INK}" stroke-width="2.6"/>')
# 손잡이에서 바깥(오른쪽)으로 당기는 화살표 세 개
for k, ay in enumerate((dy + dh * 0.36, dy + dh * 0.52, dy + dh * 0.68)):
    parts += arrow_r(dx + dw + 14, dx + dw + 92, ay, 2.6)
parts.append(f'<g transform="translate({dx+dw+130},{dy+dh*0.54})"><text x="0" y="0" font-family="{FONT}" font-size="22" fill="{INK}">아무리 당겨도</text></g>')
parts.append(f'<g transform="translate({dx+dw+130},{dy+dh*0.54+30})"><text x="0" y="0" font-family="{FONT}" font-size="22" fill="{INK}">꿈쩍도 안 한다</text></g>')
parts += caption(330, 380, ["열쇠도, 창문도 없다 - 어떻게 나갈까?"], 22)
W, H = 660, 408
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("w2_door_q.svg", "w", encoding="utf-8").write(svg)
print("wrote w2_door_q.svg")

# ---------- a: 살짝 열린 문 + 미는 화살표 ----------
parts = []
dx, dy, dw, dh = 150, 60, 170, 260
parts += frame(dx, dy, dw, dh)
# 안쪽으로 살짝 열린 문(사다리꼴로 원근 표현)
parts.append(f'<polygon points="{dx},{dy} {dx+dw*0.82},{dy+16} {dx+dw*0.82},{dy+dh-16} {dx},{dy+dh}" '
             f'fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>')
parts.append(f'<circle cx="{dx+dw*0.82-20}" cy="{dy+dh*0.52}" r="8" fill="none" stroke="{INK}" stroke-width="2.4"/>')
# 미는 화살표(바깥 → 문 쪽, 왼쪽 향함)
parts += arrow_l(dx + dw + 96, dx + dw + 18, dy + dh * 0.52, 3.4)
parts.append(f'<g transform="translate({dx+dw+128},{dy+dh*0.40})"><text x="0" y="0" font-family="{FONT}" font-size="23" font-weight="700" fill="{INK}">밀면 열린다</text></g>')
parts += caption(340, 380, ["\'잠겼다\'는 말은 문제 어디에도 없었다"], 22)
W, H = 680, 408
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("w2_door_a.svg", "w", encoding="utf-8").write(svg)
print("wrote w2_door_a.svg")
