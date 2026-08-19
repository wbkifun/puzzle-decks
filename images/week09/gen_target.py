#!/usr/bin/env python3
"""본 문제 4(정점) · 평균 시속 60 만들기 흑백 스케치 SVG.

- p4_target_q.svg  (문제): 갈 때 시속 30 확정, 올 때 ? - 목표 왕복 평균 60. (답 실마리 미노출)
- s4_ledger_a2.svg (풀이2): 시간 장부 - 허락된 2시간을 갈 때 다 썼다, 잔액 0.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_target.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 평균 60이려면 총 2시간 - 갈 때 60/30 = 2시간 소진, 잔액 0
assert 120 / 60 == 2 and 60 / 30 == 2
assert 120 / 60 - 60 / 30 == 0
# 오답 검산: 올 때 90이면 평균 45, 120이면 48
assert 120 / (2 + 60 / 90) == 45
assert 120 / (2 + 60 / 120) == 48


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
HX, SX, RY = 120, 620, 235
# 목표 배지
parts.append(f'<rect x="220" y="42" width="300" height="52" rx="26" fill="{GRAY}" stroke="{INK}" stroke-width="2.4"/>')
parts += label(370, 76, "목표 - 왕복 평균 시속 60km", 21, 700)
parts += house(HX, RY)
parts += label(HX, RY + 58, "집", 21, 700)
parts += waves(SX, RY - 14)
parts += label(SX, RY + 58, "바닷가", 21, 700)
parts.append(f'<line x1="{HX + 50}" y1="{RY - 6}" x2="{SX - 60}" y2="{RY - 6}" stroke="{INK}" stroke-width="1.4"/>')
parts.append(f'<line x1="{HX + 50}" y1="{RY + 8}" x2="{SX - 60}" y2="{RY + 8}" stroke="{INK}" stroke-width="1.4"/>')
parts += label((HX + SX) / 2, RY - 20, "60km", 20, 700)
parts += arrow_h(HX + 60, SX - 70, RY - 78)
parts += label((HX + SX) / 2, RY - 94, "갈 때 - 시속 30km (이미 확정)", 20)
parts += arrow_h(SX - 70, HX + 60, RY + 96)
parts += label((HX + SX) / 2, RY + 132, "올 때 - 시속 ? km", 22, 700)
parts += caption(370, 424, ["올 때 시속 몇 km로 달려야 왕복 평균이 시속 60km가 될까?"], 22)
W, H = 740, 452
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p4_target_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p4_target_q.svg")

# ---------- a2: 시간 장부 ----------
parts = []
BX, BH, HOUR = 90, 58, 210
Y1, Y2 = 96, 218
parts += label(BX, Y1 - 16, "허락된 시간 - 120km를 평균 시속 60으로: 2시간", 21, 700, "start")
parts.append(f'<rect x="{BX}" y="{Y1}" width="{2 * HOUR}" height="{BH}" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>')
parts += label(BX + HOUR, Y1 + 37, "2시간", 21, 700)
parts += label(BX, Y2 - 16, "갈 때 쓴 시간 - 60km를 시속 30으로: 2시간", 21, 700, "start")
parts.append(f'<rect x="{BX}" y="{Y2}" width="{2 * HOUR}" height="{BH}" fill="{GRAY}" stroke="{INK}" stroke-width="2.6"/>')
parts += label(BX + HOUR, Y2 + 37, "2시간 - 전부 소진", 21, 700)
# 잔액 0
parts.append(f'<line x1="{BX + 2 * HOUR}" y1="{Y1 - 34}" x2="{BX + 2 * HOUR}" y2="{Y2 + BH + 18}" '
             f'stroke="{INK}" stroke-width="1.8" stroke-dasharray="6 7"/>')
parts += label(BX + 2 * HOUR + 24, Y2 + 37, "올 때 몫 - 0시간", 22, 700, "start")
parts += caption(400, Y2 + BH + 74, ["올 때 무슨 속도로 달려도 시간은 0보다 크다 - 평균 60은 불가능"], 22)
W, H = 800, 386
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s4_ledger_a2.svg", "w", encoding="utf-8").write(svg)
print("wrote s4_ledger_a2.svg")
