#!/usr/bin/env python3
"""동전 뒤집기(회상 p1·풀이 s1) 흑백 스케치 SVG.

- p1_coins_q.svg (문제): 모두 앞면인 동전 9개 + ‘정확히 2개씩 뒤집기’ 규칙 예시.
  풀이 실마리(홀짝) 없음.
- s1_coins_a.svg (풀이): 2개 뒤집기의 세 경우 — 앞면 개수 변화 +2/−2/0.
실행: python3 gen_coins.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"


def coin(cx, cy, r, face):
    """앞면 = 빈 원 + ‘앞’, 뒷면 = 검은 원 + 흰 ‘뒤’."""
    fs = round(r * 0.95)
    if face == "앞":
        return [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>',
                f'<text x="{cx}" y="{cy + fs*0.36}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" fill="{INK}">앞</text>']
    return [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{INK}" stroke="{INK}" stroke-width="2.6"/>',
            f'<text x="{cx}" y="{cy + fs*0.36}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" fill="#ffffff">뒤</text>']


def arrow(x1, y, x2, label=None):
    p = [f'<line x1="{x1}" y1="{y}" x2="{x2-10}" y2="{y}" stroke="{INK}" stroke-width="3"/>',
         f'<polygon points="{x2},{y} {x2-13},{y-6.5} {x2-13},{y+6.5}" fill="{INK}"/>']
    if label:
        p.append(f'<text x="{(x1+x2)/2}" y="{y-14}" text-anchor="middle" font-family="{FONT}" font-size="18" fill="{INK}">{label}</text>')
    return p


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


CAP = 330

# ---------- 문제용: 동전 9개 + 규칙 ----------
parts = []
r = 27
for k in range(9):                                   # 3×3 배열, 모두 앞면
    cx = 62 + (k % 3) * 74
    cy = 78 + (k // 3) * 74
    parts += coin(cx, cy, r, "앞")
parts += caption(62 + 74, CAP, ["모두 앞면인 동전 9개"])

x0 = 380                                             # 규칙: 2개 골라 동시에 뒤집기
parts += coin(x0, 152, r, "앞") + coin(x0 + 64, 152, r, "앞")
parts += arrow(x0 + 106, 152, x0 + 172, "한 번")
parts += coin(x0 + 214, 152, r, "뒤") + coin(x0 + 278, 152, r, "뒤")
parts += caption(x0 + 139, CAP, ["한 번에 ‘정확히 2개’를 골라", "동시에 뒤집는다 (횟수 제한 없음)"])

W, H = 700, 396
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p1_coins_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p1_coins_q.svg")

# ---------- 풀이용: 세 경우 — +2 / −2 / 0 ----------
parts = []
r = 24
rows = [("뒤", "뒤", "앞", "앞", "앞면 +2"),
        ("앞", "앞", "뒤", "뒤", "앞면 −2"),
        ("앞", "뒤", "뒤", "앞", "앞면 그대로 (0)")]
for n, (a, b, c, d, lab) in enumerate(rows):
    y = 74 + n * 92
    parts += coin(66, y, r, a) + coin(122, y, r, b)
    parts += arrow(162, y, 224)
    parts += coin(264, y, r, c) + coin(320, y, r, d)
    parts.append(f'<text x="376" y="{y+8}" font-family="{FONT}" font-size="23" fill="{INK}">{lab}</text>')
parts += caption(280, CAP, ["어떤 2개를 골라도 변화는 +2 · −2 · 0뿐", "→ ‘앞면 개수의 홀짝’은 절대 안 변한다"])

W = 560
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s1_coins_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s1_coins_a.svg")
