#!/usr/bin/env python3
"""12주차 문자식 박스 체인 SVG (10·11주차 형식 계승). 변수는 x·y·z·a·b.
텍스트는 g transform 지역좌표. 변수(x·t·r)는 KaTeX_Math 이탤릭.
"""
import re

INK = "#111111"
GRAY = "#e4e4e4"
RED = "#c62828"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
MATH_FONT = "KaTeX_Math, 'Times New Roman', serif"

# ---- 검증 ----
t = 10 / 3


def label(x, y, text, size=20, weight=400, anchor="middle", color=INK):
    return [f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}">{text}</text></g>']


def arrow_r(x1, x2, y, sw=2.2):
    return [f'<line x1="{x1}" y1="{y}" x2="{x2 - 9}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
            f'<polygon points="{x2},{y} {x2 - 13},{y - 7} {x2 - 13},{y + 7}" fill="{INK}"/>']


def mathify(text, size):
    """변수(x·t·r)만 KaTeX 이탤릭 tspan으로(단일 패스)."""
    return re.sub(r"[xyzab]", lambda m: (f'<tspan font-family="{MATH_FONT}" font-style="italic" '
                                       f'font-weight="400" font-size="{size + 3}">{m.group(0)}</tspan>'),
                  text)


def term_box(x, cy, text, gray=False, dashed=False, color=INK, size=23):
    h = 56
    w = max(56, 30 + int(sum(23 if ord(c) > 0x3000 else 13.5 for c in text)))
    fill = GRAY if gray else "#ffffff"
    dash = ' stroke-dasharray="7 6"' if dashed else ""
    p = [f'<rect x="{x}" y="{cy - h / 2}" width="{w}" height="{h}" rx="10" '
         f'fill="{fill}" stroke="{INK}" stroke-width="2.4"{dash}/>']
    p.append(f'<g transform="translate({x + w / 2},{cy + 8})"><text x="0" y="0" text-anchor="middle" '
             f'font-family="{FONT}" font-size="{size}" font-weight="700" fill="{color}">{mathify(text, size)}</text></g>')
    return p, x + w


def term_chain(cy, boxes, ops, x0=60, head=None):
    parts = []
    x = x0
    if head:
        parts += label(x0 - 14, cy + 7, head, 19, 700, "end")
    for k, b in enumerate(boxes):
        text, opts = b[0], (b[1] if len(b) > 1 else {})
        if k:
            op = ops[k - 1]
            w = 50 + (40 if any(ord(c) > 0x3000 for c in op) else 0) + max(0, (len(op) - 4) * 9)
            parts += arrow_r(x + 6, x + 6 + w, cy)
            parts.append(f'<g transform="translate({x + 6 + w / 2},{cy - 16})"><text x="0" y="0" '
                         f'text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="700" '
                         f'fill="{INK}">{mathify(op, 19)}</text></g>')
            x += 12 + w
        p, x = term_box(x, cy, text, **opts)
        parts += p
    return parts, x


def write_svg(name, parts, w, h):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
           + "\n".join(parts) + "\n</svg>\n")
    open(name, "w", encoding="utf-8").write(svg)
    print(f"wrote {name}")


G = {"gray": True}
Q = ("?", {"dashed": True})
RG = {"gray": True, "color": RED}


def go_back(name, fwd, fwd_ops, back, back_ops, x0=130):
    parts = []
    parts += p
    p, xe2 = term_chain(180, back, back_ops, x0=x0, head="되감기")
    parts += p
    write_svg(name, parts, max(xe1, xe2) + 60, 250)


