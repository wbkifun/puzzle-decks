#!/usr/bin/env python3
"""릴레이 2 · 성냥 6개로 정삼각형 4개 흑백 스케치 SVG.

- r2_match_q.svg (문제): 성냥 3개=삼각형 1개 예시 + 성냥 6개 나열(입체 실마리 미노출).
- r2_match_a.svg (풀이): 정사면체 + 변 세기(4×3=12 = 성냥 6개 × 2몫).
실행: python3 gen_match.py
"""
import math

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증: 삼각형 4개의 변 자리 12 = 성냥 6개가 정확히 두 몫씩 (정사면체: 변 6, 면 4)
assert 4 * 3 == 12 and 12 // 6 == 2


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
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
open("r2_match_q.svg", "w", encoding="utf-8").write(svg)
print("wrote r2_match_q.svg")

# ---------- a: 정사면체 ----------
parts = []
# 꼭짓점: A·B 앞바닥, C 뒤바닥(위쪽으로 살짝), D 꼭대기
A = (120, 268)
B = (356, 268)
C = (296, 196)
D = (222, 74)
def line(p1, p2, dashed=False):
    dash = ' stroke-dasharray="9 7"' if dashed else ""
    return [f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="{INK}" stroke-width="4"{dash} stroke-linecap="round"/>']
# 뒤로 가는 변(점선) 먼저, 앞 변은 실선으로 위에
parts += line(A, C, dashed=True)
parts += line(B, C, dashed=True)
parts += line(C, D, dashed=True)
parts += line(A, B)
parts += line(A, D)
parts += line(B, D)
for p in (A, B, C, D):
    parts.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="6" fill="{INK}"/>')
parts.append(f'<text x="470" y="140" font-family="{FONT}" font-size="24" font-weight="700" fill="{INK}">정사면체</text>')
parts.append(f'<text x="470" y="176" font-family="{FONT}" font-size="21" fill="{INK}">변 6개 · 면 4개</text>')
parts.append(f'<text x="470" y="206" font-family="{FONT}" font-size="21" fill="{INK}">네 면이 모두 정삼각형</text>')
parts += caption(330, 330, ["세기로 확인: 변 자리 4 × 3 = 12 - 성냥 6개가 두 몫씩,", "모든 변이 정확히 두 면에 속한다"], 22)
W, H = 700, 388
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r2_match_a.svg", "w", encoding="utf-8").write(svg)
print("wrote r2_match_a.svg")
