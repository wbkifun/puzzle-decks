#!/usr/bin/env python3
"""워밍업 2(좋은 질문, 나쁜 질문) 흑백 스케치 SVG.

- w2_questions_q.svg (문제): 후보 1~16 타일 + 질문 카드 ㉮·㉯. 평가(최악의 경우) 실마리 없음.
- w2_questions_a.svg (풀이): 두 질문의 예/아니오 갈래별 남는 후보 수 - 최악 15 vs 최악 8.
실행: python3 gen_questions.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


def tile(x, y, s, label=None, fill="#ffffff"):
    p = [f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="6" fill="{fill}" stroke="{INK}" stroke-width="2.2"/>']
    if label is not None:
        tc = "#ffffff" if fill != "#ffffff" else INK
        p.append(f'<text x="{x+s/2}" y="{y+s*0.66}" text-anchor="middle" font-family="{FONT}" font-size="{round(s*0.42)}" fill="{tc}">{label}</text>')
    return p


def card(x, y, w, h, text, size=24):
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>',
            f'<text x="{x+w/2}" y="{y+h/2+size*0.34}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">{text}</text>']


def arrow(x1, y1, x2, y2, label=None, lx=0, ly=-10):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - 13 * math.cos(ang), y2 - 13 * math.sin(ang)
    p = [f'<line x1="{x1}" y1="{y1}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{INK}" stroke-width="2.6"/>']
    ux, uy = math.cos(ang), math.sin(ang)
    p.append(f'<polygon points="{x2},{y2} {x2-14*ux+6*uy:.1f},{y2-14*uy-6*ux:.1f} {x2-14*ux-6*uy:.1f},{y2-14*uy+6*ux:.1f}" fill="{INK}"/>')
    if label:
        p.append(f'<text x="{(x1+x2)/2+lx}" y="{(y1+y2)/2+ly}" text-anchor="middle" font-family="{FONT}" font-size="19" fill="{INK}">{label}</text>')
    return p


# ---------- 문제용: 후보 16 + 질문 카드 두 장 ----------
parts = []
S, G = 56, 9
for k in range(16):                                  # 4×4 후보 타일
    x = 46 + (k % 4) * (S + G)
    y = 52 + (k // 4) * (S + G)
    parts += tile(x, y, S, str(k + 1))
parts += caption(46 + 2 * (S + G) - G / 2, 344, ["후보는 1~16, 열여섯 개"])

x0 = 366
parts += card(x0, 92, 330, 72, "㉮  “정확히 3이니?”", 26)
parts += card(x0, 196, 330, 72, "㉯  “8 이하니?”", 26)
parts += caption(x0 + 165, 344, ["어느 쪽이 더 좋은 질문일까?"])

W, H = 740, 380
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("w2_questions_q.svg", "w", encoding="utf-8").write(svg)
print("wrote w2_questions_q.svg")

# ---------- 풀이용: 갈래별 남는 후보 수 ----------
parts = []


def branch_panel(x0, qtext, yes_n, no_n, worst):
    """질문 카드 → 예/아니오 두 갈래 → 남는 후보 미니 타일."""
    p = []
    p += card(x0, 30, 300, 58, qtext, 23)
    cx = x0 + 150
    p += arrow(cx - 40, 92, x0 + 62, 150, "예", lx=-16, ly=-2)
    p += arrow(cx + 40, 92, x0 + 238, 150, "아니오", lx=22, ly=-2)
    s, g = 24, 5                                     # 미니 타일 (‘예’ 쪽은 회색으로 구분)
    for side, n in (("yes", yes_n), ("no", no_n)):
        bx = x0 + (10 if side == "yes" else 158)
        fill = "#c9c9c9" if side == "yes" else "#ffffff"
        for k in range(n):
            xx = bx + (k % 5) * (s + g)
            yy = 162 + (k // 5) * (s + g)
            p += tile(xx, yy, s, fill=fill)
        lab = f"{n}개 남음"
        mark = "  ← 최악!" if n == worst else ""
        p.append(f'<text x="{bx + 2.5*(s+g) - g/2}" y="268" text-anchor="middle" font-family="{FONT}" font-size="20" '
                 f'fill="{INK}" font-weight="{700 if n == worst else 400}">{lab}{mark}</text>')
    return p


parts += branch_panel(30, "㉮ “정확히 3이니?”", 1, 15, 15)
parts += branch_panel(400, "㉯ “8 이하니?”", 8, 8, 8)
parts += caption(365, 330, ["질문의 실력 = 최악의 답이 남기는 후보 수 - ㉮는 15, ㉯는 8", "반반에 가깝게 가르는 질문일수록 강하다"])

W, H = 730, 380
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("w2_questions_a.svg", "w", encoding="utf-8").write(svg)
print("wrote w2_questions_a.svg")
