#!/usr/bin/env python3
"""문자식 박스 체인 SVG - 둥근 모서리 박스 속 항(x, 2x, 2x+10, ...) + 화살표 위 연산 라벨.

12페이지(개념)의 'x → 2x → 2x+10 → x+5 → 5' 형태를 이후 전 페이지가 공유한다(사용자 피드백).
- r1_chain_q.svg   (스텝 1, 개념 이전): 연산 카드 체인 [3]→[×2]→[+10]→[÷2]→[−처음 수]→[?] 유지.
- v1_chain_q.svg   (변형 1 문제): [x]→[2x]→[2x+6(회색)]→[?]→[?], 연산 ×2·+6·÷2·−처음 수.
- sv1_chain_a.svg  (변형 1 확인): +6·+100·+2026 세 줄 - 변경부만 회색, 마지막 박스에 값.
- v2_chain_q.svg   (변형 2 문제): [x]→[3x]→[3x+12]→[?]→[?] (변경부 회색).
- sv2_chain_a.svg  (변형 2 확인): [x]→[3x]→[3x+12]→[x+4]→[4].
- v3_chain_q.svg   (변형 3 문제·고장): [x]→[3x(회색)]→[3x+10]→[?]→[?], ÷2 그대로.
- sv3_chain_a.svg  (변형 3 확인): [x]→[3x]→[3x+10]→[1.5x+5]→[0.5x+5] - x가 살아남음(빨강).
- sv4_chain_a.svg  (공방 예시): ×4·+20·÷4 → 5 / 다섯 규칙 → 0, 두 줄.
- sc2_chain_a.svg  (거꾸로 마술): 간 길 [x]→[2x]→[r], 되감기 [r]→[r−8]→[x].
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피). 변수는 KaTeX_Math 이탤릭.
실행: python3 gen_chain.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
RED = "#c62828"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
# 변수는 LaTeX 이탤릭 - 덱에 인라인된 KaTeX_Math 웹폰트 사용(단독 열람 시 serif italic 폴백)
MATH_FONT = "KaTeX_Math, 'Times New Roman', serif"

# 검증
assert ((3 * 2 + 10) / 2) - 3 == 5 and ((10 * 2 + 10) / 2) - 10 == 5
assert ((7 * 2 + 6) / 2) - 7 == 3 and ((7 * 2 + 100) / 2) - 7 == 50 and ((7 * 2 + 2026) / 2) - 7 == 1013
assert ((5 * 3 + 12) / 3) - 5 == 4                     # 변형 2
assert all((3 * x + 10) / 2 - x == 0.5 * x + 5 for x in (3, 10))   # 변형 3: 0.5x+5
assert ((7 * 4 + 20) / 4) - 7 == 5                     # 공방 예시 1
assert ((7 * 2 + 8) / 2 - 4) - 7 == 0                  # 공방 예시 2
assert (9 * 2 + 8) == 26 and (26 - 8) / 2 == 9         # 거꾸로 마술


def label(x, y, text, size=20, weight=400, anchor="middle"):
    return [f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{INK}">{text}</text></g>']


def arrow_r(x1, x2, y, sw=2.2):
    return [f'<line x1="{x1}" y1="{y}" x2="{x2 - 9}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
            f'<polygon points="{x2},{y} {x2 - 13},{y - 7} {x2 - 13},{y + 7}" fill="{INK}"/>']


def mathify(text, size):
    """변수(x·r·a·b)만 KaTeX 이탤릭 tspan으로(단일 패스 - 삽입된 마크업을 재치환하지 않도록)."""
    import re
    return re.sub(r"[xrab]", lambda m: (f'<tspan font-family="{MATH_FONT}" font-style="italic" '
                                        f'font-weight="400" font-size="{size + 3}">{m.group(0)}</tspan>'),
                  text)


def term_box(x, cy, text, gray=False, dashed=False, color=INK, size=23):
    """둥근 모서리 박스 속 항(문자식). (x = 왼쪽 끝, cy = 세로 중심). 오른쪽 끝 x 반환."""
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
    """boxes = [(text, opts)] 를 화살표로 이은 한 줄. ops = 화살표 위 연산 라벨(len = len(boxes)-1)."""
    parts = []
    x = x0
    if head:
        parts += label(x0 - 14, cy + 7, head, 19, 700, "end")
    for k, b in enumerate(boxes):
        text, opts = b[0], (b[1] if len(b) > 1 else {})
        if k:
            op = ops[k - 1]
            w = 50 + (40 if any(ord(c) > 0x3000 for c in op) else 0)
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
OPS = ["×2", "+10", "÷2", "−x"]

# ---------- r1(개념 이전): 연산 카드 체인 유지 ----------
def op_card_chain(cy, start):
    boxes = [(start, {"gray": True}), ("×2", {}), ("+10", {}), ("÷2", {}), ("−처음 수", {}), Q]
    return term_chain(cy, boxes, ["", "", "", "", ""])


parts = []
p, xe = op_card_chain(70, "3")
parts += p
p, _ = op_card_chain(180, "10")
parts += p
write_svg("r1_chain_q.svg", parts, xe + 60, 250)

# ---------- 변형 1 문제: +10 → +6, 변경부 회색, 나머지는 물음표 ----------
parts, xe = term_chain(85, [("x", {}), ("2x", {}), ("2x+6", G), Q, Q], ["×2", "+6", "÷2", "−x"])
write_svg("v1_chain_q.svg", parts, xe + 60, 170)

# ---------- 변형 1 확인: +6 · +100 · +2026 세 줄, 마지막 박스에 값 ----------
parts = []
rows = [("+6", "2x+6", "x+3", "3"), ("+100", "2x+100", "x+50", "50"), ("+2026", "2x+2026", "x+1013", "1013")]
for k, (op, t2, t3, t4) in enumerate(rows):
    p, xe = term_chain(60 + k * 108, [("x", {}), ("2x", {}), (t2, G), (t3, G), (t4, G)],
                       ["×2", op, "÷2", "−x"])
    parts += p
write_svg("sv1_chain_a.svg", parts, xe + 60, 336)

# ---------- 변형 2 문제 ----------
parts, xe = term_chain(85, [("x", {}), ("3x", G), ("3x+12", G), Q, Q], ["×3", "+12", "÷3", "−x"])
write_svg("v2_chain_q.svg", parts, xe + 60, 170)

# ---------- 변형 2 확인 ----------
parts, xe = term_chain(85, [("x", {}), ("3x", G), ("3x+12", G), ("x+4", G), ("4", G)],
                       ["×3", "+12", "÷3", "−x"])
write_svg("sv2_chain_a.svg", parts, xe + 60, 170)

# ---------- 변형 3 문제(고장): ×3만 바뀌고 ÷2는 그대로 ----------
parts, xe = term_chain(85, [("x", {}), ("3x", G), ("3x+10", {}), Q, Q], ["×3", "+10", "÷2", "−x"])
write_svg("v3_chain_q.svg", parts, xe + 60, 170)

# ---------- 변형 3 확인: x가 살아남는다(빨강) ----------
parts, xe = term_chain(85, [("x", {}), ("3x", G), ("3x+10", {}), ("1.5x+5", G),
                            ("0.5x+5", {"gray": True, "color": RED})],
                       ["×3", "+10", "÷2", "−x"])
write_svg("sv3_chain_a.svg", parts, xe + 60, 170)

# ---------- 공방 예시: 두 줄 ----------
parts = []
p, xe1 = term_chain(70, [("x", {}), ("4x", {}), ("4x+20", {}), ("x+5", {}), ("5", {})],
                    ["×4", "+20", "÷4", "−x"])
parts += p
p, xe2 = term_chain(180, [("x", {}), ("2x", {}), ("2x+8", {}), ("x+4", {}), ("x", {}), ("0", {})],
                    ["×2", "+8", "÷2", "−4", "−x"])
parts += p
write_svg("sv4_chain_a.svg", parts, max(xe1, xe2) + 60, 250)

# ---------- 변형 2 확인 + 전환 문구 + 변형 3(고장) 문제 ----------
parts = []
p, xe1 = term_chain(60, [("x", {}), ("3x", G), ("3x+12", G), ("x+4", G), ("4", G)],
                    ["×3", "+12", "÷3", "−x"], x0=150, head="변형 2")
parts += p
parts += label(110, 158, "바로 고장 난 마술 하나를 진단하자 - 어느 마술사가 ×3으로 바꿔 놓고, 나누기는 ÷2 그대로 두었다.", 20, 700, "start")
parts += label(110, 188, "시작 3으로 한 번, 10으로 한 번 - 각자 시험해 보라.", 20, 400, "start")
p, xe2 = term_chain(258, [("x", {}), ("3x", G), ("3x+10", {}), Q, Q],
                    ["×3", "+10", "÷2", "−x"], x0=150, head="고장?")
parts += p
write_svg("sv2v3_chain_a.svg", parts, max(xe1, xe2) + 60, 322)

# ---------- 주사위 두 개 마술: 문제 / 풀이 ----------
parts, xe = term_chain(85, [("첫째 눈", G), Q, Q, Q, ("결과", G)], ["×5", "+7", "×2", "+둘째 눈"])
write_svg("c1_dice_q.svg", parts, xe + 60, 170)

parts, xe = term_chain(85, [("a", {}), ("5a", {}), ("5a+7", {}), ("10a+14", {}),
                            ("10a+14+b", {}), ("10a+b", G)],
                       ["×5", "+7", "×2", "+b", "−14"])
write_svg("sc1_dice_a.svg", parts, xe + 60, 170)

# ---------- 레시피 일반화: ×a, +b, ÷a ----------
parts, xe = term_chain(85, [("x", {}), ("ax", {}), ("ax+b", {}), ("x+b÷a", {}),
                            ("b÷a", {"gray": True, "color": RED})],
                       ["×a", "+b", "÷a", "−x"])
write_svg("recipe_chain_a.svg", parts, xe + 60, 170)

# ---------- 거꾸로 마술: 간 길 / 되감기 ----------
parts = []
p, xe1 = term_chain(70, [("x", {}), ("2x", {}), ("r", {})], ["×2", "+8"], x0=130, head="간 길")
parts += p
p, xe2 = term_chain(180, [("r", {}), ("r−8", {}), ("x", {})], ["−8", "÷2"], x0=130, head="되감기")
parts += p
write_svg("sc2_chain_a.svg", parts, max(xe1, xe2) + 60, 250)
