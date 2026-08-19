#!/usr/bin/env python3
"""워밍업 1 · 마른 사과(D8 회상) 흑백 스케치 SVG.

- w1_apple_q.svg  (문제): 수분 99% 사과 100kg -> 말린 뒤 수분 98%, 무게는? (답 실마리 미노출)
- ws1_apple_a.svg (풀이): 본체 막대 - 과육 1kg은 그대로, 전체(기준량)가 반 토막.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_apple.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 과육 1kg이 2%가 되는 전체 무게 = 50kg
assert 1 / 0.02 == 50
assert 100 * 0.99 == 99 and 50 * 0.98 == 49


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


def apple(cx, cy, r, dashed=False):
    dash = ' stroke-dasharray="9 8"' if dashed else ""
    p = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2.8"{dash}/>',
         # 꼭지 + 잎
         f'<path d="M {cx} {cy - r} q 4 -18 14 -26" fill="none" stroke="{INK}" stroke-width="2.6"/>',
         f'<path d="M {cx + 14} {cy - r - 26} q 26 -10 40 6 q -22 12 -40 -6 z" fill="{GRAY}" stroke="{INK}" stroke-width="1.6"/>']
    return p


def arrow_r(x1, x2, y, sw=2.6):
    return [f'<line x1="{x1}" y1="{y}" x2="{x2 - 12}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
            f'<polygon points="{x2},{y} {x2 - 16},{y - 8} {x2 - 16},{y + 8}" fill="{INK}"/>']


# ---------- q: 사과 두 개 ----------
parts = []
parts += apple(165, 215, 88)
parts += label(165, 208, "수분 99%", 24, 700)
parts += label(165, 244, "100kg", 22)
parts += arrow_r(290, 440, 205)
parts += label(365, 178, "햇볕에 말리면", 20)
parts += apple(575, 215, 88, dashed=True)
parts += label(575, 208, "수분 98%", 24, 700)
parts += label(575, 244, "? kg", 26, 700)
W, H = 760, 380
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("w1_apple_q.svg", "w", encoding="utf-8").write(svg)
print("wrote w1_apple_q.svg")

# ---------- a: 본체 막대(과육 고정, 전체 반 토막) ----------
parts = []
BX, BH = 60, 56
SOLID = 4.8          # 과육 1kg (막대 480px = 100kg 비례)
# 말리기 전: 100kg
Y1 = 96
parts += label(BX, Y1 - 16, "말리기 전 - 100kg", 21, 700, "start")
parts.append(f'<rect x="{BX}" y="{Y1}" width="{SOLID}" height="{BH}" fill="{INK}"/>')
parts.append(f'<rect x="{BX + SOLID}" y="{Y1}" width="{480 - SOLID}" height="{BH}" fill="{GRAY}" stroke="{INK}" stroke-width="2"/>')
parts += label(BX + 240, Y1 + 36, "물 99kg (99%)", 20)
# 말린 뒤: 50kg
Y2 = 246
parts += label(BX, Y2 - 16, "말린 뒤 - ? kg", 21, 700, "start")
parts.append(f'<rect x="{BX}" y="{Y2}" width="{SOLID}" height="{BH}" fill="{INK}"/>')
parts.append(f'<rect x="{BX + SOLID}" y="{Y2}" width="{240 - SOLID}" height="{BH}" fill="{GRAY}" stroke="{INK}" stroke-width="2"/>')
parts += label(BX + 125, Y2 + 36, "물 49kg (98%)", 20)
# 과육 연결(변하지 않는 것)
parts.append(f'<line x1="{BX + SOLID / 2}" y1="{Y1 + BH + 6}" x2="{BX + SOLID / 2}" y2="{Y2 - 24}" stroke="{INK}" stroke-width="1.6" stroke-dasharray="5 6"/>')
parts += label(BX + 14, Y1 + BH + 44, "과육 1kg - 변하지 않는 본체", 19, 700, "start")
# 오른쪽 계산
parts += label(590, 130, "과육 1kg이 이제 2%", 22, 700, "start")
parts += label(590, 168, "전체 = 1kg ÷ 2% = 50kg", 22, 400, "start")
parts += label(590, 206, "물은 99kg → 49kg", 21, 400, "start")
parts += label(590, 244, "- 50kg이 증발했다", 21, 400, "start")
parts += caption(460, 392, ["%를 버리고 본체(kg)로 내려가라 - 기준량(전체)이 반 토막 났다"], 22)
W, H = 920, 420
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("ws1_apple_a.svg", "w", encoding="utf-8").write(svg)
print("wrote ws1_apple_a.svg")
