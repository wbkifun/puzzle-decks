#!/usr/bin/env python3
"""릴레이 5 · 스위치 3개와 전구 3개(입장 한 번) 흑백 스케치 SVG.

- r5_switch_q.svg (문제): 스위치 3개 | 닫힌 문 | 전구 3개(연결 ?) - 열 실마리 미노출.
- r5_switch_a.svg (풀이): 3단계 절차 + 전구 세 가지 상태(켜짐·따뜻함·차가움).
반복 요소는 g transform 지역좌표로 저작(큰 절대좌표 텍스트 버그 회피).
실행: python3 gen_switch.py
"""

INK = "#111111"
GRAY = "#d7d7d7"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 빛만 = 상태 2가지 < 스위치 3개(비둘기집으로 불가), 열 추가 = 3가지 ≥ 3
assert 2 < 3 <= 3


def caption(cx, y, lines, size=21):
    # 텍스트는 g translate 지역좌표로 - 큰 절대좌표 텍스트가 도형과 다른 배율로
    # 그려지는 크로미움 버그 회피(6주차 확립 규칙)
    t = [f'<g transform="translate({cx},{y})"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="0" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text></g>")
    return ["".join(t)]


def switch(x, y, num, on=False):
    """벽 스위치: 판 + 토글(on=위, off=아래). g translate 지역좌표."""
    ty = 14 if on else 34
    return [
        f'<g transform="translate({x},{y})">'
        f'<rect x="0" y="0" width="44" height="64" rx="8" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>'
        f'<rect x="14" y="{ty}" width="16" height="16" rx="3" fill="{INK}"/>'
        f'<g transform="translate(22,92)"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="{INK}">{num}</text></g>'
        f"</g>"
    ]


def bulb(x, y, label=None, lit=False, warm=False, sub=None):
    """전구: 유리구 + 꼭지. lit=빛살, warm=아지랑이. g translate 지역좌표."""
    fill = GRAY if lit else "#ffffff"
    p = [f'<g transform="translate({x},{y})">']
    if lit:
        for dx1, dy1, dx2, dy2 in ((-38, -38, -26, -26), (0, -52, 0, -37), (38, -38, 26, -26),
                                   (-52, 0, -37, 0), (52, 0, 37, 0)):
            p.append(f'<line x1="{dx1}" y1="{dy1}" x2="{dx2}" y2="{dy2}" stroke="{INK}" stroke-width="2.4"/>')
    p.append(f'<circle cx="0" cy="0" r="26" fill="{fill}" stroke="{INK}" stroke-width="2.6"/>')
    p.append(f'<rect x="-10" y="24" width="20" height="14" rx="3" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>')
    if warm:
        for dx in (-14, 0, 14):
            p.append(f'<path d="M {dx-4} -48 q 6 -7 0 -14 q -6 -7 0 -14" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    if label:
        p.append(f'<g transform="translate(0,70)"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="{INK}">{label}</text></g>')
    if sub:
        p.append(f'<g transform="translate(0,98)"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="18" fill="{INK}">{sub}</text></g>')
    p.append("</g>")
    return p


# ---------- q: 스위치 3 | 문 | 전구 3 ----------
parts = []
for k in range(3):
    parts += switch(70 + k * 74, 120, k + 1)
parts.append(f'<g transform="translate(180,80)"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="{INK}">방 밖 - 스위치 3개</text></g>')
# 닫힌 문(문틀+문+손잡이)
parts.append(f'<rect x="352" y="66" width="116" height="220" fill="none" stroke="{INK}" stroke-width="3"/>')
parts.append(f'<rect x="362" y="76" width="96" height="210" fill="#ffffff" stroke="{INK}" stroke-width="2.4"/>')
parts.append(f'<circle cx="442" cy="186" r="7" fill="none" stroke="{INK}" stroke-width="2.4"/>')
parts.append(f'<g transform="translate(410,320)"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="19" fill="{INK}">안이 안 보인다</text></g>')
for k in range(3):
    parts += bulb(546 + k * 92, 150, label="?")
parts.append(f'<g transform="translate(638,80)"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="{INK}">방 안 - 전구 3개</text></g>')
parts += caption(410, 386, ["스위치는 밖에서 얼마든지 - 입장은 딱 한 번", "어느 스위치가 어느 전구와 연결됐을까?"], 22)
W, H = 820, 448
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r5_switch_q.svg", "w", encoding="utf-8").write(svg)
print("wrote r5_switch_q.svg")

# ---------- a: 절차 + 세 가지 상태 ----------
parts = []
steps = ["① 1번 켜고 10분", "② 1번 끄고 2번 켜기", "③ 입장 - 눈과 손으로"]
for k, s in enumerate(steps):
    x = 60 + k * 250
    parts.append(f'<g transform="translate({x},40)">'
                 f'<rect x="0" y="0" width="216" height="46" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2.4"/>'
                 f'<g transform="translate(108,30)"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="20" fill="{INK}">{s}</text></g>'
                 f"</g>")
    if k < 2:
        ax = 60 + k * 250 + 224
        parts.append(f'<line x1="{ax}" y1="63" x2="{ax+16}" y2="63" stroke="{INK}" stroke-width="2.6"/>')
        parts.append(f'<polygon points="{ax+26},63 {ax+13},56.5 {ax+13},69.5" fill="{INK}"/>')
parts += bulb(160, 210, label="켜져 있다", lit=True, sub="→ 2번")
parts += bulb(410, 210, label="꺼짐 + 따뜻함", warm=True, sub="→ 1번")
parts += bulb(660, 210, label="꺼짐 + 차가움", sub="→ 3번")
parts += caption(410, 372, ["빛만 보면 상태는 켜짐/꺼짐 2가지 - 셋 중 둘은 반드시 같은 상태(비둘기집)",
                            "열을 더하면 상태 3가지 ≥ 스위치 3개 - 셋 모두 다른 이름표"], 22)
W, H = 820, 430
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r5_switch_a.svg", "w", encoding="utf-8").write(svg)
print("wrote r5_switch_a.svg")
