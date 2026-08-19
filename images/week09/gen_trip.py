#!/usr/bin/env python3
"""본 문제 3 · 왕복 평균 속도 흑백 스케치 SVG.

- p3_trip_q.svg (문제): 집-바다 60km, 갈 때 시속 30 / 올 때 시속 60. 평균은? (답 실마리 미노출)
- s3_trip_a.svg (풀이): 시간 막대 - 3시간 중 2시간이 시속 30 구간, 120÷3 = 40.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_trip.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 60/30=2h, 60/60=1h, 평균 = 120/3 = 40
assert 60 / 30 == 2 and 60 / 60 == 1
assert (60 + 60) / (2 + 1) == 40


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


def house(cx, cy, s=44):
    return [f'<rect x="{cx - s / 2}" y="{cy - s / 2}" width="{s}" height="{s}" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>',
            f'<polygon points="{cx - s / 2 - 8},{cy - s / 2} {cx + s / 2 + 8},{cy - s / 2} {cx},{cy - s / 2 - 30}" '
            f'fill="{GRAY}" stroke="{INK}" stroke-width="2.6"/>',
            f'<rect x="{cx - 8}" y="{cy + s / 2 - 22}" width="16" height="22" fill="{INK}"/>']


def waves(cx, cy):
    p = []
    for k in range(3):
        y = cy + k * 14
        p.append(f'<path d="M {cx - 44} {y} q 11 -10 22 0 q 11 10 22 0 q 11 -10 22 0" '
                 f'fill="none" stroke="{INK}" stroke-width="2.4"/>')
    return p


def arrow_h(x1, x2, y, sw=2.6):
    d = 1 if x2 > x1 else -1
    return [f'<line x1="{x1}" y1="{y}" x2="{x2 - 12 * d}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
            f'<polygon points="{x2},{y} {x2 - 16 * d},{y - 8} {x2 - 16 * d},{y + 8}" fill="{INK}"/>']


# ---------- q ----------
parts = []
HX, SX, RY = 120, 620, 205
parts += house(HX, RY)
parts += label(HX, RY + 58, "집", 21, 700)
parts += waves(SX, RY - 14)
parts += label(SX, RY + 58, "바닷가", 21, 700)
# 길(두 줄) + 거리
parts.append(f'<line x1="{HX + 50}" y1="{RY - 6}" x2="{SX - 60}" y2="{RY - 6}" stroke="{INK}" stroke-width="1.4"/>')
parts.append(f'<line x1="{HX + 50}" y1="{RY + 8}" x2="{SX - 60}" y2="{RY + 8}" stroke="{INK}" stroke-width="1.4"/>')
parts += label((HX + SX) / 2, RY - 20, "60km", 20, 700)
# 갈 때 / 올 때
parts += arrow_h(HX + 60, SX - 70, RY - 88)
parts += label((HX + SX) / 2, RY - 104, "갈 때 - 시속 30km (길이 막혔다)", 20)
parts += arrow_h(SX - 70, HX + 60, RY + 96)
parts += label((HX + SX) / 2, RY + 132, "올 때 - 시속 60km (뻥 뚫렸다)", 20)
parts += caption(370, 400, ["왕복 전체의 평균 속도는 시속 몇 km일까?"], 22)
W, H = 740, 430
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p3_trip_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p3_trip_q.svg")

# ---------- a: 시간 막대 ----------
parts = []
BX, BY, BH, HOUR = 90, 120, 64, 180          # 1시간 = 180px
parts += label(BX, BY - 40, "걸린 시간으로 그려 보면 (1칸 = 1시간)", 21, 700, "start")
parts.append(f'<rect x="{BX}" y="{BY}" width="{2 * HOUR}" height="{BH}" fill="{GRAY}" stroke="{INK}" stroke-width="2.4"/>')
parts.append(f'<rect x="{BX + 2 * HOUR}" y="{BY}" width="{HOUR}" height="{BH}" fill="#ffffff" stroke="{INK}" stroke-width="2.4"/>')
parts += label(BX + HOUR, BY + 40, "갈 때 - 시속 30으로 2시간", 20, 700)
parts += label(BX + 2 * HOUR + HOUR / 2, BY + 40, "올 때 - 1시간", 19)
# 시간 눈금
for k in range(4):
    x = BX + k * HOUR
    parts.append(f'<line x1="{x}" y1="{BY + BH}" x2="{x}" y2="{BY + BH + 12}" stroke="{INK}" stroke-width="2"/>')
    parts += label(x, BY + BH + 36, f"{k}시간", 18)
parts += label(BX, BY + BH + 96, "왕복 거리 120km ÷ 총 3시간 = 시속 40km", 24, 700, "start")
parts += caption(370, BY + BH + 160, ["평균은 시간을 많이 먹은 쪽(느린 쪽)으로 끌려간다 - 45가 아니다"], 22)
W, H = 740, 400
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s3_trip_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s3_trip_a.svg")
