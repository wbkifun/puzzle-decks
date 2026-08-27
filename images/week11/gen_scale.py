#!/usr/bin/env python3
"""저울 그림 - 등식은 저울. 3x+4 = x+16 → 양쪽에서 x 하나씩 내리면 2x+4 = 16.
sr4_scale_a.svg (확인 4) / concept_scale_a.svg (개념: 저울 하나, 양변 같은 짓)."""
INK = "#111111"; GRAY = "#e4e4e4"; RED = "#c62828"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
MATH = "KaTeX_Math, 'Times New Roman', serif"


def txt(x, y, s, size=20, weight=700, anchor="middle", color=INK, math=False):
    ff = MATH if math else FONT
    it = ' font-style="italic"' if math else ""
    return (f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" font-family="{ff}"'
            f'{it} font-size="{size}" font-weight="{weight}" fill="{color}">{s}</text></g>')


def xbox(x, y, faded=False):
    op = ' opacity="0.25"' if faded else ""
    return (f'<g{op}><rect x="{x}" y="{y}" width="34" height="34" rx="6" fill="#fff" stroke="{INK}" stroke-width="2.2"/>'
            + txt(x + 17, y + 25, "x", 24, 400, math=True) + "</g>")


def weight(x, y, s, w=44):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="4" fill="{GRAY}" stroke="{INK}" stroke-width="2.2"/>'
            + txt(x + w / 2, y + 25, s, 21))


def scale(cx, base_y, left, right, caption):
    """left/right = (n_x, faded_n, weight_label). 팬 위에 x상자 n개(뒤에서 faded개는 흐리게) + 추."""
    p = []
    # 받침·기둥·가로대
    p.append(f'<polygon points="{cx - 40},{base_y} {cx + 40},{base_y} {cx},{base_y - 30}" fill="{INK}"/>')
    p.append(f'<line x1="{cx}" y1="{base_y - 30}" x2="{cx}" y2="{base_y - 120}" stroke="{INK}" stroke-width="5"/>')
    p.append(f'<line x1="{cx - 150}" y1="{base_y - 120}" x2="{cx + 150}" y2="{base_y - 120}" stroke="{INK}" stroke-width="4"/>')
    for side, (n, faded, wl) in ((-1, left), (1, right)):
        px = cx + side * 150
        p.append(f'<line x1="{px}" y1="{base_y - 120}" x2="{px}" y2="{base_y - 70}" stroke="{INK}" stroke-width="2.5"/>')
        p.append(f'<path d="M{px - 90},{base_y - 70} L{px + 90},{base_y - 70} L{px + 70},{base_y - 48} L{px - 70},{base_y - 48} Z" '
                 f'fill="#fff" stroke="{INK}" stroke-width="2.5"/>')
        items_w = n * 40 + 50
        x = px - items_w / 2
        for i in range(n):
            p.append(xbox(x, base_y - 108, faded=(i >= n - faded)))
            x += 40
        p.append(weight(x + 2, base_y - 108, wl))
    p.append(txt(cx, base_y + 34, caption, 21, 700))
    return p


def write(name, parts, w, h):
    open(name, "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
        + "\n".join(parts) + "\n</svg>\n")
    print("wrote", name)


parts = scale(230, 170, (3, 1, "4"), (1, 1, "16"), "양쪽에서 x를 하나씩 내린다")
parts.append(f'<line x1="470" y1="110" x2="530" y2="110" stroke="{INK}" stroke-width="3"/>')
parts.append(f'<polygon points="545,110 530,102 530,118" fill="{INK}"/>')
parts += scale(780, 170, (2, 0, "4"), (0, 0, "16"), "균형은 그대로 - 2x + 4 = 16")
write("sr4_scale_a.svg", parts, 1030, 215)

parts = scale(260, 170, (3, 0, "4"), (1, 0, "16"), "3x + 4 = x + 16 - 저울은 균형이다")
write("r4_scale_q.svg", parts, 520, 215)
