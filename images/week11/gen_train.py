#!/usr/bin/env python3
"""기차와 다리 - 문제 그림(상황만): 다리 200m, 기차가 다리에 들어서는 순간 / 완전히 빠져나온 순간."""
INK = "#111111"; GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"


def txt(x, y, s, size=20, weight=700, anchor="middle"):
    return (f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" font-family="{FONT}"'
            f' font-size="{size}" font-weight="{weight}" fill="{INK}">{s}</text></g>')


def train(x, y, w=150):
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="8" fill="#cfe3f5" stroke="{INK}" stroke-width="2.4"/>']
    for k in range(3):
        p.append(f'<rect x="{x + 14 + k * 44}" y="{y + 9}" width="26" height="16" rx="3" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')
    for cx in (x + 25, x + w - 25):
        p.append(f'<circle cx="{cx}" cy="{y + 46}" r="8" fill="{INK}"/>')
    return p


def scene(y0, caption, tx):
    p = [f'<line x1="40" y1="{y0}" x2="800" y2="{y0}" stroke="{INK}" stroke-width="2"/>',
         f'<rect x="300" y="{y0 - 6}" width="300" height="12" fill="{GRAY}" stroke="{INK}" stroke-width="2"/>',
         f'<path d="M300,{y0 + 6} L300,{y0 + 40} M600,{y0 + 6} L600,{y0 + 40}" stroke="{INK}" stroke-width="2.4"/>',
         f'<path d="M300,{y0 + 40} Q450,{y0 - 30} 600,{y0 + 40}" fill="none" stroke="{INK}" stroke-width="2.4"/>',
         txt(450, y0 + 68, "다리 200m", 20)]
    p += train(tx, y0 - 60)
    p.append(txt(450, y0 - 88, caption, 20, 700))
    return p


parts = scene(120, "들어서는 순간", 150)
parts += scene(330, "완전히 빠져나온 순간", 600)
parts.append(txt(700, 140, "→ 시속 72km", 19, 400))
open("p_train_q.svg", "w", encoding="utf-8").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 420" width="840" height="420">\n' + "\n".join(parts) + "\n</svg>\n")
print("wrote p_train_q.svg")
