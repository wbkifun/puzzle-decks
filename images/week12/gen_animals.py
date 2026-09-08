#!/usr/bin/env python3
"""학·거북·문어 - 문제 그림(상황만): 세 동물과 다리 수, 물음표 우리. 실마리 없음."""
INK = "#111111"; GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"


def txt(x, y, s, size=20, weight=700, anchor="middle"):
    return (f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" font-family="{FONT}"'
            f' font-size="{size}" font-weight="{weight}" fill="{INK}">{s}</text></g>')


def crane(x, y):  # 학: 몸 + 긴 목 + 다리 2
    return [f'<ellipse cx="{x}" cy="{y}" rx="34" ry="22" fill="#fff" stroke="{INK}" stroke-width="2.4"/>',
            f'<path d="M{x+28},{y-10} Q{x+52},{y-38} {x+44},{y-56}" fill="none" stroke="{INK}" stroke-width="2.4"/>',
            f'<circle cx="{x+44}" cy="{y-60}" r="7" fill="#fff" stroke="{INK}" stroke-width="2.2"/>',
            f'<path d="M{x+51},{y-60} l14,3 l-14,3 Z" fill="{INK}"/>',
            f'<line x1="{x-10}" y1="{y+20}" x2="{x-12}" y2="{y+56}" stroke="{INK}" stroke-width="2.4"/>',
            f'<line x1="{x+10}" y1="{y+20}" x2="{x+12}" y2="{y+56}" stroke="{INK}" stroke-width="2.4"/>']


def turtle(x, y):  # 거북: 등딱지 + 다리 4
    p = [f'<path d="M{x-38},{y+14} A38,30 0 0 1 {x+38},{y+14} Z" fill="#d9ead3" stroke="{INK}" stroke-width="2.4"/>',
         f'<circle cx="{x+46}" cy="{y+6}" r="8" fill="#fff" stroke="{INK}" stroke-width="2.2"/>']
    for dx in (-28, -10, 10, 28):
        p.append(f'<line x1="{x+dx}" y1="{y+14}" x2="{x+dx}" y2="{y+34}" stroke="{INK}" stroke-width="2.4"/>')
    return p


def octopus(x, y):  # 문어: 머리 + 다리 8
    p = [f'<circle cx="{x}" cy="{y}" r="24" fill="#f4cccc" stroke="{INK}" stroke-width="2.4"/>',
         f'<circle cx="{x-8}" cy="{y-4}" r="2.6" fill="{INK}"/>', f'<circle cx="{x+8}" cy="{y-4}" r="2.6" fill="{INK}"/>']
    for k in range(8):
        dx = -28 + k * 8
        bend = 10 if k % 2 else -6
        p.append(f'<path d="M{x+dx},{y+18} q{bend},22 {bend//2},34" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    return p


parts = [f'<rect x="30" y="30" width="900" height="330" rx="18" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="12 9"/>']
parts += crane(160, 150)
parts += turtle(430, 150)
parts += octopus(720, 140)
parts += [txt(160, 240, "학 - 다리 2", 20), txt(430, 240, "거북 - 다리 4", 20), txt(720, 240, "문어 - 다리 8", 20)]
parts.append(txt(480, 320, "몇 마리씩인지는 보이지 않는다 - 어두운 수조", 20, 400))
parts.append(txt(480, 420, "머리를 세니 10개, 다리를 세니 40개", 26, 800))
open("p_animals_q.svg", "w", encoding="utf-8").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 460" width="960" height="460">\n' + "\n".join(parts) + "\n</svg>\n")
print("wrote p_animals_q.svg")
