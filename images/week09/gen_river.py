#!/usr/bin/env python3
"""열린 도전 1 · 강물 왕복 흑백 스케치 SVG.

- c1_river_q.svg (문제): 잔잔한 호수 왕복 2시간 vs 물살 있는 강 왕복 - 같을까? (답 실마리 미노출)
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_river.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증(예시 수치): 배 10, 물살 5, 편도 10km -> 10/15 + 10/5 = 8/3시간 > 2시간
assert 10 / 15 + 10 / 5 > 2


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


def boat(cx, cy):
    return [f'<path d="M {cx - 36} {cy} L {cx + 36} {cy} L {cx + 22} {cy + 18} L {cx - 22} {cy + 18} Z" '
            f'fill="#ffffff" stroke="{INK}" stroke-width="2.4"/>',
            f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 40}" stroke="{INK}" stroke-width="2.4"/>',
            f'<polygon points="{cx},{cy - 40} {cx + 30},{cy - 12} {cx},{cy - 12}" fill="{GRAY}" stroke="{INK}" stroke-width="1.8"/>']


def water(x1, x2, y):
    p = []
    for k in range(2):
        yy = y + k * 13
        seg = []
        x = x1
        while x + 22 <= x2:
            seg.append(f"q 11 -9 22 0")
            x += 22
        p.append(f'<path d="M {x1} {yy} ' + " ".join(seg) + f'" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    return p


def arrow_h(x1, x2, y, sw=2.2, dashed=False):
    d = 1 if x2 > x1 else -1
    dash = ' stroke-dasharray="6 6"' if dashed else ""
    return [f'<line x1="{x1}" y1="{y}" x2="{x2 - 10 * d}" y2="{y}" stroke="{INK}" stroke-width="{sw}"{dash}/>',
            f'<polygon points="{x2},{y} {x2 - 14 * d},{y - 7} {x2 - 14 * d},{y + 7}" fill="{INK}"/>']


parts = []
# 왼쪽: 잔잔한 호수
parts += label(190, 56, "잔잔한 호수", 22, 700)
parts += boat(190, 150)
parts += water(70, 320, 178)
parts += arrow_h(110, 270, 236)
parts += arrow_h(270, 110, 262, dashed=True)
parts += label(190, 300, "왕복 - 2시간", 20, 700)
# 오른쪽: 흐르는 강
parts += label(590, 56, "흐르는 강 - 같은 거리", 22, 700)
parts += boat(590, 150)
parts += water(470, 720, 178)
for k in range(3):
    parts += arrow_h(480 + k * 90, 540 + k * 90, 205, sw=1.8)
parts += label(748, 211, "물살", 18, 400, "start")
parts += arrow_h(510, 670, 238)
parts += label(590, 260, "밀어준다", 17)
parts += arrow_h(670, 510, 284, dashed=True)
parts += label(590, 306, "거슬러 온다", 17)
parts += label(590, 338, "왕복 - ?", 20, 700)
parts += caption(410, 372, ["도움과 방해는 정확히 같은 크기 - 왕복 시간은 2시간보다 길까, 짧을까, 같을까?"], 21)
W, H = 820, 400
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("c1_river_q.svg", "w", encoding="utf-8").write(svg)
print("wrote c1_river_q.svg")
