#!/usr/bin/env python3
"""릴레이 3 · 성냥 6개로 정삼각형 4개 흑백 스케치 SVG.

- r3_match_q.svg (문제): 성냥 3개=삼각형 1개 예시 + 성냥 6개 나열(입체 실마리 미노출).
- r3_match_a.svg (풀이): 정사면체 + 변 세기(4×3=12 = 성냥 6개 × 2몫).
실행: python3 gen_match.py
"""
import math

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 삼각형 4개의 변 자리 12 = 성냥 6개가 정확히 두 몫씩 (정사면체: 변 6, 면 4)
assert 4 * 3 == 12 and 12 // 6 == 2


def caption(cx, y, lines, size=21):
    # 텍스트는 g translate 지역좌표로 - 큰 절대좌표 텍스트가 도형과 다른 배율로
    # 그려지는 크로미움 버그 회피(6주차 확립 규칙)
    t = [f'<g transform="translate({cx},{y})"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="0" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text></g>")
    return ["".join(t)]


def match(x1, y1, x2, y2):
    """성냥개비: 몸통 선 + 머리(작은 원, 시작점 쪽)."""
    return [
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="4.2" stroke-linecap="round"/>',
        f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="5.5" fill="{INK}"/>',
    ]


# ---------- q: 삼각형 1개 예시 + 성냥 6개 ----------
parts = []
# 왼쪽: 성냥 3개로 정삼각형 (변 96)
ax, ay, s = 80, 210, 108
bx, by = ax + s, ay
cx3, cy3 = ax + s / 2, ay - s * math.sqrt(3) / 2
parts += match(ax, ay, bx, by)
parts += match(bx, by, cx3, cy3)
parts += match(cx3, cy3, ax, ay)
parts += caption(ax + s / 2, 258, ["세 개면 정삼각형 하나"], 21)
# 오른쪽: 성냥 6개 나열
for k in range(6):
    x = 320 + k * 42
    parts += match(x, 96, x, 208)
parts += caption(320 + 5 * 21, 258, ["이 여섯 개로 - 정삼각형 네 개?"], 21)
parts += caption(330, 318, ["부러뜨리기 · 겹치기 금지 - 한 변 = 성냥 한 개"], 22)
W, H = 660, 346
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r3_match_q.svg", "w", encoding="utf-8").write(svg)
print("wrote r3_match_q.svg")

# ---------- a: 정사면체 (위-오른쪽 시점: 앞면 + 오른쪽 면 두 개가 보여 입체감) ----------
parts = []
# 꼭짓점: A 앞왼쪽 바닥, B 앞오른쪽 바닥(가장 가깝고 낮음), C 뒤오른쪽 바닥(실루엣 위), D 꼭대기
A = (100, 258)
B = (300, 296)
C = (352, 170)
D = (178, 64)
def line(p1, p2, dashed=False):
    dash = ' stroke-dasharray="9 7"' if dashed else ""
    return [f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="{INK}" stroke-width="4"{dash} stroke-linecap="round"/>']
def face(pts, fill):
    s = " ".join(f"{x},{y}" for x, y in pts)
    return [f'<polygon points="{s}" fill="{fill}"/>']
# 보이는 면 두 개: 앞면 A-B-D(흰색) + 오른쪽 면 B-C-D(옅은 회색 음영)
parts += face((A, B, D), "#ffffff")
parts += face((B, C, D), "#e4e4e4")
# 숨은 변(점선)이 면 위로 비쳐 보이게 - 그다음 실선 변
parts += line(A, C, dashed=True)
for e in ((A, B), (A, D), (B, D), (B, C), (C, D)):
    parts += line(*e)
for p in (A, B, C, D):
    parts.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="6" fill="{INK}"/>')
parts.append(f'<g transform="translate(470,140)"><text x="0" y="0" font-family="{FONT}" font-size="24" font-weight="700" fill="{INK}">정사면체</text></g>')
parts.append(f'<g transform="translate(470,176)"><text x="0" y="0" font-family="{FONT}" font-size="21" fill="{INK}">변 6개 · 면 4개</text></g>')
parts.append(f'<g transform="translate(470,206)"><text x="0" y="0" font-family="{FONT}" font-size="21" fill="{INK}">네 면이 모두 정삼각형</text></g>')
parts += caption(330, 352, ["세기로 확인: 변 자리 4 × 3 = 12 - 성냥 6개가 두 몫씩,", "모든 변이 정확히 두 면에 속한다"], 22)
W, H = 700, 410
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r3_match_a.svg", "w", encoding="utf-8").write(svg)
print("wrote r3_match_a.svg")
