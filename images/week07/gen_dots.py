#!/usr/bin/env python3
"""릴레이 3 · 아홉 점을 직선 4개로 흑백 스케치 SVG.

- r3_dots_q.svg (문제): 3×3 점만(경계 실마리 미노출).
- r3_dots_a.svg (풀이): 상자 밖 두 점을 도는 4직선 경로(①~④) - 코드로 전 점 통과 검증.
실행: python3 gen_dots.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 점 좌표(수학 좌표, y 위쪽) - (0..2)×(0..2)
DOTS = [(i, j) for i in range(3) for j in range(3)]
# 4직선 경로: 꼭짓점들(수학 좌표). 상자 밖 점: (0,3)·(3,0)
PATH = [(0, 0), (0, 3), (3, 0), (0, 0), (2, 2)]


def on_seg(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    cross = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
    if cross != 0:
        return False
    return min(ax, bx) <= px <= max(ax, bx) and min(ay, by) <= py <= max(ay, by)


covered = {d for d in DOTS for a, b in zip(PATH, PATH[1:]) if on_seg(d, a, b)}
assert covered == set(DOTS), f"경로가 못 지나는 점: {set(DOTS)-covered}"
assert len(PATH) - 1 == 4


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


S, OX, OY = 74, 266, 300         # 간격, 원점(수학 (0,0))의 SVG 좌표 - 캡션 폭 기준 중앙


def sx(p):
    return OX + p[0] * S


def sy(p):
    return OY - p[1] * S


# ---------- q: 점 아홉 개만 ----------
parts = []
for d in DOTS:
    parts.append(f'<circle cx="{sx(d)}" cy="{sy(d)}" r="8" fill="{INK}"/>')
parts += caption(OX + S, 370, ["펜을 떼지 않고 - 이어진 직선 4개로 아홉 점을 모두 지나라"], 22)
W, H = 680, 398
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r3_dots_q.svg", "w", encoding="utf-8").write(svg)
print("wrote r3_dots_q.svg")

# ---------- a: 경로 + 번호 ----------
parts = []
# 점들이 만드는 '상자'를 옅은 점선으로
parts.append(f'<rect x="{sx((0,0))}" y="{sy((0,2))}" width="{2*S}" height="{2*S}" '
             f'fill="none" stroke="{INK}" stroke-width="1.2" stroke-dasharray="5 6" opacity="0.45"/>')
# 경로
pts = " ".join(f"{sx(p)},{sy(p)}" for p in PATH)
parts.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/>')
# 마지막 구간 화살촉 ((0,0)→(2,2) 방향)
ex, ey = sx((2, 2)), sy((2, 2))
parts.append(f'<polygon points="{ex+8},{ey-8} {ex-14},{ey-2} {ex-2},{ey+14}" fill="{INK}"/>')
for d in DOTS:
    parts.append(f'<circle cx="{sx(d)}" cy="{sy(d)}" r="8" fill="#ffffff" stroke="{INK}" stroke-width="3"/>')
# 구간 번호 ①~④
labels = ["①", "②", "③", "④"]
offs = [(-24, 0), (26, -6), (0, 26), (26, 2)]
for k, (a, b) in enumerate(zip(PATH, PATH[1:])):
    mx, my = (sx(a) + sx(b)) / 2 + offs[k][0], (sy(a) + sy(b)) / 2 + offs[k][1]
    parts.append(f'<text x="{mx}" y="{my+8}" text-anchor="middle" font-family="{FONT}" font-size="24" font-weight="700" fill="{INK}">{labels[k]}</text>')
parts += caption(OX + S, 384, ["상자 밖 두 점을 빌린다 - 경계는 우리 눈이 만든 것"], 22)
W, H = 680, 412
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r3_dots_a.svg", "w", encoding="utf-8").write(svg)
print("wrote r3_dots_a.svg")
