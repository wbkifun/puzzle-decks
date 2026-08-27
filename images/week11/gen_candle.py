#!/usr/bin/env python3
"""양초 두 자루 - 문제 그림(상황만): 가는 양초 30cm(시간당 4cm), 굵은 양초 20cm(시간당 1cm)."""
INK = "#111111"; GRAY = "#e4e4e4"; RED = "#c62828"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
assert abs((30 - 4 * 10 / 3) - (20 - 10 / 3)) < 1e-9


def txt(x, y, s, size=20, weight=700, anchor="middle", color=INK):
    return (f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" font-family="{FONT}"'
            f' font-size="{size}" font-weight="{weight}" fill="{color}">{s}</text></g>')


def candle(x, base, w, h_cm, scale, name, rate, wax="#fff4d6"):
    h = h_cm * scale
    p = [f'<rect x="{x - w / 2}" y="{base - h}" width="{w}" height="{h}" rx="4" fill="{wax}" stroke="{INK}" stroke-width="2.4"/>',
         f'<line x1="{x}" y1="{base - h}" x2="{x}" y2="{base - h - 14}" stroke="{INK}" stroke-width="2"/>',
         f'<path d="M{x},{base - h - 44} C{x + 14},{base - h - 30} {x + 12},{base - h - 16} {x},{base - h - 12} '
         f'C{x - 12},{base - h - 16} {x - 14},{base - h - 30} {x},{base - h - 44} Z" fill="#f6b73c" stroke="#d98b12" stroke-width="2"/>',
         # 높이 치수선
         f'<line x1="{x + w / 2 + 22}" y1="{base}" x2="{x + w / 2 + 22}" y2="{base - h}" stroke="{INK}" stroke-width="1.5"/>',
         f'<line x1="{x + w / 2 + 14}" y1="{base}" x2="{x + w / 2 + 30}" y2="{base}" stroke="{INK}" stroke-width="1.5"/>',
         f'<line x1="{x + w / 2 + 14}" y1="{base - h}" x2="{x + w / 2 + 30}" y2="{base - h}" stroke="{INK}" stroke-width="1.5"/>',
         txt(x + w / 2 + 38, base - h / 2 + 7, f"{h_cm}cm", 20, 700, "start"),
         txt(x, base + 30, name, 21, 700),
         txt(x, base + 56, f"1시간에 {rate}cm씩 탄다", 19, 400)]
    return p


parts = [f'<line x1="40" y1="330" x2="640" y2="330" stroke="{INK}" stroke-width="3"/>']
parts += candle(170, 330, 36, 30, 8.5, "가는 양초", 4)
parts += candle(450, 330, 90, 20, 8.5, "굵은 양초", 1, wax="#f3e3c8")
parts.append(txt(340, 60, "동시에 불을 붙인다", 22, 700))
open("p_candle_q.svg", "w", encoding="utf-8").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 400" width="680" height="400">\n' + "\n".join(parts) + "\n</svg>\n")
print("wrote p_candle_q.svg")
