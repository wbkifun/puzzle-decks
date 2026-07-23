#!/usr/bin/env python3
"""풀이 4-2(대답 기록 = 이름표, 비둘기집) 흑백 스케치 SVG.

- s4_records_a.svg: 서로 다른 두 수가 같은 ○× 기록(이름표)을 받는 그림 +
  이름표 64장 < 수 100개 비교.
실행: python3 gen_records.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

TAG = "○×○××○"                                      # 예시 기록 (6글자)
assert len(TAG) == 6 and set(TAG) <= {"○", "×"}


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


def num(cx, cy, label, r=34):
    return [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>',
            f'<text x="{cx}" y="{cy+10}" text-anchor="middle" font-family="{FONT}" font-size="28" font-weight="700" fill="{INK}">{label}</text>']


def tag(x, y, w, h, text, dashed=False):
    d = ' stroke-dasharray="7 5"' if dashed else ""
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2.6"{d}/>',
            f'<circle cx="{x+16}" cy="{y+h/2}" r="4.5" fill="none" stroke="{INK}" stroke-width="2"/>',
            f'<text x="{x+w/2+8}" y="{y+h/2+9}" text-anchor="middle" font-family="{FONT}" font-size="26" fill="{INK}">{text}</text>']


def arrow(x1, y1, x2, y2):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - 13 * math.cos(ang), y2 - 13 * math.sin(ang)
    ux, uy = math.cos(ang), math.sin(ang)
    return [f'<line x1="{x1}" y1="{y1}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{INK}" stroke-width="2.6"/>',
            f'<polygon points="{x2},{y2} {x2-14*ux+6*uy:.1f},{y2-14*uy-6*ux:.1f} {x2-14*ux-6*uy:.1f},{y2-14*uy+6*ux:.1f}" fill="{INK}"/>']


parts = []
# 왼쪽: 두 수 → 같은 이름표
parts += num(80, 90, "37")
parts += num(80, 210, "58")
parts += tag(220, 116, 240, 66, TAG)
parts += arrow(122, 100, 214, 138)
parts += arrow(122, 200, 214, 162)
parts.append(f'<text x="340" y="92" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="{INK}">같은 대답 기록!</text>')
parts += caption(270, 296, ["기록이 같은 두 수는", "무엇으로도 구분할 수 없다"], 22)

# 오른쪽: 이름표 64장 < 수 100개
x0 = 560
parts.append(f'<text x="{x0+130}" y="66" text-anchor="middle" font-family="{FONT}" font-size="23" font-weight="700" fill="{INK}">○× 여섯 글자 이름표</text>')
parts += tag(x0, 84, 260, 56, "2⁶ = 64가지")
parts.append(f'<text x="{x0+130}" y="188" text-anchor="middle" font-family="{FONT}" font-size="23" font-weight="700" fill="{INK}">이름이 필요한 수</text>')
parts += num(x0 + 130, 238, "100", 40)
parts.append(f'<text x="{x0+130}" y="308" text-anchor="middle" font-family="{FONT}" font-size="24" font-weight="700" fill="{INK}">100 &gt; 64 → 비둘기집!</text>')

W, H = 860, 340
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s4_records_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s4_records_a.svg")
