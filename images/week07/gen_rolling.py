#!/usr/bin/env python3
"""본 문제 6 · 동전 주위를 도는 동전(회전수) 흑백 스케치 SVG.

- p6_rolling_q.svg  (문제): 고정 동전 + 굴린 동전(방향 표시) + 궤도 화살표 - 2r 원 실마리 미노출.
- s6_rolling_a1.svg (풀이1): 반 바퀴 체크포인트(그림이 벌써 정방향) + 중심이 그리는 반지름 2r 원.
- s6_rolling_a2.svg (풀이2): 미끄러뜨리기(공전만 1바퀴) + R=3r 일반화(3+1=4바퀴).
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_rolling.py
"""
import math

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 같은 크기 → 중심 원 반지름 2r → 4πr/2πr = 2바퀴, R=3r → 3+1=4바퀴
assert (2 * math.pi * 2) / (2 * math.pi * 1) == 2
assert 3 + 1 == 4


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


def coin(cx, cy, r, mark_deg=None, fill="#ffffff", sw=2.8):
    """동전: 원 + 안쪽 테 + 방향 표시(중심→테두리 화살표, mark_deg=0이 위쪽)."""
    p = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r-7}" fill="none" stroke="{INK}" stroke-width="1.2"/>']
    if mark_deg is not None:
        a = math.radians(mark_deg - 90)          # 0도 = 위쪽
        ex, ey = cx + (r - 13) * math.cos(a), cy + (r - 13) * math.sin(a)
        p.append(f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{INK}" stroke-width="3.4"/>')
        hx, hy = cx + (r - 5) * math.cos(a), cy + (r - 5) * math.sin(a)
        ux, uy = math.cos(a), math.sin(a)
        p.append(f'<polygon points="{hx:.1f},{hy:.1f} {hx-12*ux-6*uy:.1f},{hy-12*uy+6*ux:.1f} '
                 f'{hx-12*ux+6*uy:.1f},{hy-12*uy-6*ux:.1f}" fill="{INK}"/>')
    return p


def orbit_arrow(cx, cy, rad, a1, a2, sw=2.4, dashed=True):
    """(cx,cy) 중심 반지름 rad의 원호 화살표. 각도는 도 단위(0=위, 시계방향)."""
    r1, r2 = math.radians(a1 - 90), math.radians(a2 - 90)
    x1, y1 = cx + rad * math.cos(r1), cy + rad * math.sin(r1)
    x2, y2 = cx + rad * math.cos(r2), cy + rad * math.sin(r2)
    large = 1 if (a2 - a1) % 360 > 180 else 0
    dash = ' stroke-dasharray="7 7"' if dashed else ""
    p = [f'<path d="M {x1:.1f} {y1:.1f} A {rad} {rad} 0 {large} 1 {x2:.1f} {y2:.1f}" '
         f'fill="none" stroke="{INK}" stroke-width="{sw}"{dash}/>']
    ta = math.radians(a2 - 90)
    ux, uy = -math.sin(ta), math.cos(ta)          # 시계방향 접선
    p.append(f'<polygon points="{x2:.1f},{y2:.1f} {x2-14*ux-7*uy:.1f},{y2-14*uy+7*ux:.1f} '
             f'{x2-14*ux+7*uy:.1f},{y2-14*uy-7*ux:.1f}" fill="{INK}"/>')
    return p


# ---------- q: 고정 + 굴린 동전 + 궤도 ----------
parts = []
FCX, FCY, R = 300, 205, 72
parts += coin(FCX, FCY, R, fill=GRAY)
parts += label(FCX, FCY + 8, "고정", 24, 700)
parts += coin(FCX + 2 * R, FCY, R, mark_deg=0)
parts += label(FCX + 2 * R, FCY - R - 22, "굴린 동전", 20)
parts += orbit_arrow(FCX, FCY, 2 * R + 26, 100, 300)
parts += label(FCX - 2 * R - 46, FCY - 132, "미끄러짐 없이", 20, anchor="middle")
parts += label(FCX - 2 * R - 46, FCY - 105, "한 바퀴", 20, anchor="middle")
parts += caption(FCX + 40, 442, ["출발점으로 돌아올 때까지 - 화살표 그림은 몇 바퀴 돌까?"], 22)
W, H = 740, 470
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p6_rolling_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p6_rolling_q.svg")

# ---------- a1: 반 바퀴 체크포인트 + 중심의 원(2r) ----------
parts = []
FCX, FCY, R = 235, 195, 62
parts += coin(FCX, FCY, R, fill=GRAY)
parts += label(FCX, FCY + 7, "고정", 21, 700)
# 중심이 그리는 원(반지름 2r)
parts.append(f'<circle cx="{FCX}" cy="{FCY}" r="{2*R}" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="8 8"/>')
parts += orbit_arrow(FCX, FCY, 2 * R, 100, 160, sw=2.6, dashed=False)
# 출발(오른쪽, 화살표 위) / 반 바퀴(왼쪽, 화살표 다시 위!)
parts += coin(FCX + 2 * R, FCY, R, mark_deg=0)
parts += label(FCX + 2 * R + 4, FCY + R + 34, "출발", 19)
parts += coin(FCX - 2 * R, FCY, R, mark_deg=0)
parts += label(FCX - 2 * R - 4, FCY + R + 34, "반 바퀴 - 벌써 정방향!", 19)
# 오른쪽 설명
parts += label(500, 130, "중심이 그리는 원의 반지름 = 2r", 22, 700, "start")
parts += label(500, 168, "중심 이동 거리 = 2π×(2r) = 4πr", 21, 400, "start")
parts += label(500, 206, "회전수 = 4πr ÷ 2πr = 2바퀴", 22, 700, "start")
parts += caption(410, 372, ["회전수는 접촉면이 스친 거리가 아니라 - 중심이 움직인 거리가 정한다"], 22)
W, H = 860, 400
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s6_rolling_a1.svg", "w", encoding="utf-8").write(svg)
print("wrote s6_rolling_a1.svg")

# ---------- a2: 미끄러뜨리기(공전만) + R=3r 일반화 ----------
parts = []
# 왼쪽 panel: 같은 면이 안쪽을 보게 4위치 - 공전만으로 1바퀴
FCX, FCY, R = 190, 190, 44
ORB = 2 * R
parts += coin(FCX, FCY, R, fill=GRAY)
for deg in (90, 180, 270, 0):                  # 오른쪽·아래·왼쪽·위
    a = math.radians(deg - 90)
    cx, cy = FCX + ORB * math.cos(a), FCY + ORB * math.sin(a)
    parts += coin(cx, cy, R, mark_deg=deg + 180)   # 화살표가 항상 중심을 향함
parts.append(f'<circle cx="{FCX}" cy="{FCY}" r="{ORB}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-dasharray="6 8"/>')
parts += caption(FCX, 386, ["굴리지 않고 미끄러뜨려도(같은 면이 안쪽)", "공전만으로 그림은 1바퀴 돈다"], 20)
# 오른쪽 panel: R = 3r
BCX, BCY, BR, br = 600, 195, 105, 35
parts += coin(BCX, BCY, BR, fill=GRAY)
parts += label(BCX, BCY + 7, "반지름 3배", 21, 700)
parts += coin(BCX + BR + br, BCY, br, mark_deg=0)
parts += orbit_arrow(BCX, BCY, BR + br + 22, 100, 240)
parts += caption(BCX, 386, ["거리÷둘레가 말하는 3바퀴가 아니라", "3 + 1 = 4바퀴"], 20)
parts += caption(400, 452, ["자전(구름) + 공전(궤도 한 바퀴) - 회전수 = R/r + 1"], 22)
W, H = 800, 480
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s6_rolling_a2.svg", "w", encoding="utf-8").write(svg)
print("wrote s6_rolling_a2.svg")
