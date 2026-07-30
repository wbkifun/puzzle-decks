#!/usr/bin/env python3
"""릴레이 5 · 수도사의 산길(같은 시각, 같은 지점) 흑백 스케치 SVG.

- r5_monk_q.svg (문제): 같은 산 두 panel - 첫째 날 오르막 / 둘째 날 내리막(겹치기 실마리 미노출).
- r5_monk_a.svg (풀이): 두 날을 한 무대에 겹친 산길(마주침) + 시간-높이 그래프 교차.
텍스트·반복 요소는 g transform 지역좌표로 저작(큰 절대좌표 텍스트 버그 회피).
실행: python3 gen_monk.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"


def caption(cx, y, lines, size=21):
    # 텍스트는 g translate 지역좌표로 - 큰 절대좌표 텍스트가 도형과 다른 배율로
    # 그려지는 크로미움 버그 회피(6주차 확립 규칙)
    t = [f'<g transform="translate({cx},{y})"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="0" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text></g>")
    return ["".join(t)]


def mountain(x, y, title, arrow):
    """산 스케치 한 panel. (x,y)=좌상단, 폭 300 × 높이 240. g translate 지역좌표.
    비탈(절→정상)이 산길 - arrow='up'이면 오르막, 'down'이면 내리막 화살표."""
    p = [f'<g transform="translate({x},{y})">']
    p.append(f'<text x="150" y="0" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="{INK}">{title}</text>')
    # 땅 + 산(왼쪽 비탈이 길)
    p.append(f'<line x1="0" y1="210" x2="300" y2="210" stroke="{INK}" stroke-width="2.6"/>')
    p.append(f'<path d="M 30 210 L 210 40 L 290 210" fill="#ffffff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    # 절(바닥 왼쪽): 몸체 + 지붕
    p.append(f'<rect x="6" y="182" width="34" height="28" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>')
    p.append(f'<path d="M 0 182 L 23 164 L 46 182 Z" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>')
    p.append(f'<text x="23" y="238" text-anchor="middle" font-family="{FONT}" font-size="18" fill="{INK}">절</text>')
    # 정상 깃발
    p.append(f'<line x1="210" y1="40" x2="210" y2="12" stroke="{INK}" stroke-width="2.4"/>')
    p.append(f'<polygon points="210,12 236,20 210,28" fill="{INK}"/>')
    p.append(f'<text x="252" y="46" font-family="{FONT}" font-size="18" fill="{INK}">정상</text>')
    # 비탈 중간 화살표(오르막/내리막) - 비탈 방향 (180,-170)/√.. 단위 ≈ (0.727,-0.687)
    if arrow == "up":
        x1, y1, x2, y2 = 96, 158, 152, 105
    else:
        x1, y1, x2, y2 = 152, 105, 96, 158
    dx, dy = x2 - x1, y2 - y1
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2-ux*12:.1f}" y2="{y2-uy*12:.1f}" stroke="{INK}" stroke-width="3.4"/>')
    p.append(f'<polygon points="{x2:.1f},{y2:.1f} {x2-ux*15-uy*7:.1f},{y2-uy*15+ux*7:.1f} {x2-ux*15+uy*7:.1f},{y2-uy*15-ux*7:.1f}" fill="{INK}"/>')
    lab = "새벽 6시 출발" if arrow == "up" else "새벽 6시 출발"
    p.append("</g>")
    return p


def person(x, y, flip=False):
    """비탈 위 사람: 머리 + 몸 + 팔다리. (x,y)=발 위치. g translate 지역좌표."""
    s = -1 if flip else 1
    return [
        f'<g transform="translate({x},{y})">'
        f'<circle cx="0" cy="-34" r="7" fill="#ffffff" stroke="{INK}" stroke-width="2.4"/>'
        f'<line x1="0" y1="-27" x2="0" y2="-12" stroke="{INK}" stroke-width="2.4"/>'
        f'<line x1="0" y1="-22" x2="{8*s}" y2="-16" stroke="{INK}" stroke-width="2.2"/>'
        f'<line x1="0" y1="-12" x2="{-6*s}" y2="0" stroke="{INK}" stroke-width="2.2"/>'
        f'<line x1="0" y1="-12" x2="{7*s}" y2="0" stroke="{INK}" stroke-width="2.2"/>'
        f"</g>"
    ]


# ---------- q: 두 panel (첫째 날 / 둘째 날) ----------
parts = []
parts += mountain(40, 40, "첫째 날 - 절에서 정상으로", "up")
parts += mountain(400, 40, "둘째 날 - 같은 길로 내려온다", "down")
parts += caption(370, 332, ["둘 다 새벽 6시 출발 - 속도는 제멋대로, 쉬는 것도 자유",
                            "'같은 시각, 같은 지점'인 순간이 반드시 있을까?"], 22)
W, H = 740, 372
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r5_monk_q.svg", "w", encoding="utf-8").write(svg)
print("wrote r5_monk_q.svg")

# ---------- a: 겹친 무대(마주침) + 시간-높이 그래프 ----------
parts = []
# 왼쪽 panel: 한 산에 두 사람 - 마주침
parts.append(f'<g transform="translate(40,40)">')
parts.append(f'<text x="150" y="0" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="{INK}">두 날을 한 무대에</text>')
parts.append(f'<line x1="0" y1="210" x2="300" y2="210" stroke="{INK}" stroke-width="2.6"/>')
parts.append(f'<path d="M 30 210 L 210 40 L 290 210" fill="#ffffff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
parts.append(f'<rect x="6" y="182" width="34" height="28" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>')
parts.append(f'<path d="M 0 182 L 23 164 L 46 182 Z" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>')
parts.append(f'<line x1="210" y1="40" x2="210" y2="12" stroke="{INK}" stroke-width="2.4"/>')
parts.append(f'<polygon points="210,12 236,20 210,28" fill="{INK}"/>')
parts.append("</g>")
# 두 사람: 비탈 위 마주 보게 (비탈: (30,210)-(210,40) → t=0.42, 0.58 지점)
def slope_pt(t):
    return (40 + 30 + 180 * t, 40 + 210 - 170 * t)
xa, ya = slope_pt(0.40)
xb, yb = slope_pt(0.60)
parts += person(xa, ya, flip=False)
parts += person(xb, yb, flip=True)
mx, my = slope_pt(0.50)
parts.append(f'<g transform="translate({mx:.0f},{my:.0f})">'
             f'<circle cx="0" cy="-8" r="13" fill="none" stroke="{INK}" stroke-width="2.6" stroke-dasharray="4 4"/>'
             f'<text x="4" y="34" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="{INK}">반드시 마주친다</text>'
             f"</g>")
# 오른쪽 panel: 시간-높이 그래프 (두 곡선은 중앙점을 지나 반드시 교차)
gx, gy, gw, gh = 430, 270, 260, 190       # 원점(좌하), 폭, 높이
parts.append(f'<g transform="translate({gx},{gy})">')
parts.append(f'<text x="{gw/2}" y="{-gh-20}" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="{INK}">시간-높이 그래프로 보면</text>')
parts.append(f'<line x1="0" y1="0" x2="{gw+14}" y2="0" stroke="{INK}" stroke-width="2.6"/>')
parts.append(f'<line x1="0" y1="0" x2="0" y2="{-gh-14}" stroke="{INK}" stroke-width="2.6"/>')
parts.append(f'<text x="{gw+8}" y="24" text-anchor="end" font-family="{FONT}" font-size="17" fill="{INK}">시간 (새벽→저녁)</text>')
parts.append(f'<text x="-12" y="{-gh-2}" text-anchor="end" font-family="{FONT}" font-size="17" fill="{INK}">정상</text>')
parts.append(f'<text x="-12" y="-2" text-anchor="end" font-family="{FONT}" font-size="17" fill="{INK}">절</text>')
# 오르는 날(멈춤 구간 포함) / 내리는 날 - 둘 다 중앙 (gw/2,-gh/2) 통과
parts.append(f'<path d="M 0 0 Q {gw*0.34} {-gh*0.06} {gw/2} {-gh/2} Q {gw*0.62} {-gh*0.86} {gw} {-gh}" '
             f'fill="none" stroke="{INK}" stroke-width="3"/>')
parts.append(f'<path d="M 0 {-gh} Q {gw*0.3} {-gh*0.94} {gw/2} {-gh/2} Q {gw*0.72} {-gh*0.12} {gw} 0" '
             f'fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="8 6"/>')
parts.append(f'<circle cx="{gw/2}" cy="{-gh/2}" r="8" fill="{INK}"/>')
parts.append("</g>")
parts += caption(370, 336, ["오르는 곡선(실선)과 내리는 곡선(점선)은 아무리 구불거려도 반드시 한 번은 만난다",
                            "마주친 시각·지점을 몰라도 - '반드시 있다'는 보장된다 (존재 증명)"], 21)
W, H = 740, 386
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r5_monk_a.svg", "w", encoding="utf-8").write(svg)
print("wrote r5_monk_a.svg")
