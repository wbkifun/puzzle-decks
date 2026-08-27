#!/usr/bin/env python3
"""11주차 문자식 박스 체인 SVG (10주차 gen_chain.py 형식 계승).
- 되감기 체인: 간 길 [x]→[2x]→[2x+8]=26 / 되감기 [26]→[18]→[9]
- 저울 체인: 방정식 박스 [5x−3=2x+9] → (양변 −2x) → ... → [x=4]  (변경 박스 회색·미지 점선 ?·특이점 빨강)
텍스트는 g transform 지역좌표. 변수(x·t·r)는 KaTeX_Math 이탤릭.
실행: python3 gen_chain.py (images/week11에서)
"""
import re

INK = "#111111"
GRAY = "#e4e4e4"
RED = "#c62828"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
MATH_FONT = "KaTeX_Math, 'Times New Roman', serif"

# ---- 검증 ----
assert 3 * 7 + 4 == 25 and (25 - 4) / 3 == 7                # 워밍업 되감기
assert 2 * 9 + 8 == 26 and (26 - 8) / 2 == 9                # 스텝 1
assert 5 * 9 - 7 == 38 and 20 / 4 + 3 == 8                  # 스텝 2
assert (7 + 5) * 3 - 6 == 30 and (30 + 6) / 3 - 5 == 7      # 스텝 3
assert 3 * 6 + 4 == 6 + 16                                  # 스텝 4 (양변 x)
assert 5 * 4 - 3 == 2 * 4 + 9                               # 변형 1
assert 4 * (-3) + 7 == (-3) - 2 and 2 * (4 + 3) == 4 + 10   # 변형 2
assert 40 + 5 == 3 * (10 + 5)                               # 도전 나이
t = 10 / 3
assert abs((30 - 4 * t) - (20 - t)) < 1e-9                  # 양초: 3시간 20분
assert abs((30 - 4 * 5 / 3) - (20 - 5 / 3) - 5) < 1e-9 and (20 - 5) - (30 - 20) == 5   # 차이 5cm 두 번


def label(x, y, text, size=20, weight=400, anchor="middle", color=INK):
    return [f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}">{text}</text></g>']


def arrow_r(x1, x2, y, sw=2.2):
    return [f'<line x1="{x1}" y1="{y}" x2="{x2 - 9}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
            f'<polygon points="{x2},{y} {x2 - 13},{y - 7} {x2 - 13},{y + 7}" fill="{INK}"/>']


def mathify(text, size):
    """변수(x·t·r)만 KaTeX 이탤릭 tspan으로(단일 패스)."""
    return re.sub(r"[xtr]", lambda m: (f'<tspan font-family="{MATH_FONT}" font-style="italic" '
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
    """간 길 / 되감기 두 줄."""
    parts = []
    p, xe1 = term_chain(70, fwd, fwd_ops, x0=x0, head="간 길")
    parts += p
    p, xe2 = term_chain(180, back, back_ops, x0=x0, head="되감기")
    parts += p
    write_svg(name, parts, max(xe1, xe2) + 60, 250)


# ---- 워밍업 2: 회상 - 거꾸로 마술 ×3, +4 → 25 ----
go_back("w2_rewind_q.svg", [("x", {}), ("3x", {}), ("25", G)], ["×3", "+4"],
        [("25", G), Q, Q], ["−4", "÷3"])
go_back("sw2_rewind_a.svg", [("x", {}), ("3x", {}), ("25", G)], ["×3", "+4"],
        [("25", G), ("21", {}), ("7", RG)], ["−4", "÷3"])

# ---- 스텝 1: 2x+8=26 ----
go_back("r1_chain_q.svg", [("x", {}), ("2x", {}), ("2x+8", {}), ("26", G)], ["×2", "+8", "="],
        [("26", G), Q, Q], ["−8", "÷2"])
go_back("sr1_chain_a.svg", [("x", {}), ("2x", {}), ("2x+8", {}), ("26", G)], ["×2", "+8", "="],
        [("26", G), ("18", {}), ("9", RG)], ["−8", "÷2"])

# ---- 스텝 2: 5x−7=38 / x÷4+3=8 (손잡이 둘: 빼기·나누기) ----
parts = []
p, xe1 = term_chain(60, [("x", {}), ("5x", G), ("5x−7", G), ("38", G)], ["×5", "−7", "="], x0=130, head="식 ①")
parts += p
p, xe2 = term_chain(170, [("38", G), Q, Q], ["+7", "÷5"], x0=130, head="되감기")
parts += p
p, xe3 = term_chain(280, [("x", {}), ("x÷4", G), ("x÷4+3", G), ("8", G)], ["÷4", "+3", "="], x0=130, head="식 ②")
parts += p
p, xe4 = term_chain(390, [("8", G), Q, Q], ["−3", "×4"], x0=130, head="되감기")
parts += p
write_svg("r2_chain_q.svg", parts, max(xe1, xe2, xe3, xe4) + 60, 460)

parts = []
p, xe1 = term_chain(60, [("x", {}), ("5x", G), ("5x−7", G), ("38", G)], ["×5", "−7", "="], x0=130, head="식 ①")
parts += p
p, xe2 = term_chain(170, [("38", G), ("45", {}), ("9", RG)], ["+7", "÷5"], x0=130, head="되감기")
parts += p
p, xe3 = term_chain(280, [("x", {}), ("x÷4", G), ("x÷4+3", G), ("8", G)], ["÷4", "+3", "="], x0=130, head="식 ②")
parts += p
p, xe4 = term_chain(390, [("8", G), ("5", {}), ("20", RG)], ["−3", "×4"], x0=130, head="되감기")
parts += p
write_svg("sr2_chain_a.svg", parts, max(xe1, xe2, xe3, xe4) + 60, 460)

# ---- 스텝 3: 3(x+5)−6=30 (규칙 셋) ----
go_back("r3_chain_q.svg", [("x", {}), ("x+5", {}), ("3(x+5)", {}), ("3(x+5)−6", {}), ("30", G)],
        ["+5", "×3", "−6", "="], [("30", G), Q, Q, Q], ["+6", "÷3", "−5"])
go_back("sr3_chain_a.svg", [("x", {}), ("x+5", {}), ("3(x+5)", {}), ("3(x+5)−6", {}), ("30", G)],
        ["+5", "×3", "−6", "="], [("30", G), ("36", {}), ("12", {}), ("7", RG)], ["+6", "÷3", "−5"])

# ---- 스텝 4(고비): 3x+4 = x+16 - 되감기 시작점이 없다 ----
parts = []
p, xe1 = term_chain(70, [("x", {}), ("3x", {}), ("3x+4", {}), ("x+16", RG)], ["×3", "+4", "="], x0=130, head="간 길")
parts += p
p, xe2 = term_chain(180, [("x+16", RG), Q, Q], ["−4", "÷3"], x0=130, head="되감기?")
parts += p
write_svg("r4_chain_q.svg", parts, max(xe1, xe2) + 60, 250)

# ---- 저울 체인(양변 연산) ----
def scale_chain(name, boxes, ops, x0=60):
    parts, xe = term_chain(85, boxes, ops, x0=x0)
    write_svg(name, parts, xe + 60, 170)


scale_chain("sr4_chain_a.svg", [("3x+4=x+16", {}), ("2x+4=16", G), ("2x=12", G), ("x=6", RG)],
            ["양변 −x", "양변 −4", "양변 ÷2"])
scale_chain("v1_chain_q.svg", [("5x−3=2x+9", {}), Q, Q, ("x=?", {"dashed": True})],
            ["양변 −2x", "양변 +3", "양변 ÷3"])
scale_chain("sv1_chain_a.svg", [("5x−3=2x+9", {}), ("3x−3=9", G), ("3x=12", G), ("x=4", RG)],
            ["양변 −2x", "양변 +3", "양변 ÷3"])

# 변형 2: 두 줄(음수 해 · 괄호)
parts = []
p, xe1 = term_chain(70, [("4x+7=x−2", {}), Q, Q, ("x=?", {"dashed": True})],
                    ["양변 −x", "양변 −7", "양변 ÷3"], x0=130, head="식 ①")
parts += p
p, xe2 = term_chain(180, [("2(x+3)=x+10", {}), ("2x+6=x+10", G), Q, ("x=?", {"dashed": True})],
                    ["괄호 풀기", "양변 −x", "양변 −6"], x0=130, head="식 ②")
parts += p
write_svg("v2_chain_q.svg", parts, max(xe1, xe2) + 60, 250)

parts = []
p, xe1 = term_chain(70, [("4x+7=x−2", {}), ("3x+7=−2", G), ("3x=−9", G), ("x=−3", RG)],
                    ["양변 −x", "양변 −7", "양변 ÷3"], x0=130, head="식 ①")
parts += p
p, xe2 = term_chain(180, [("2(x+3)=x+10", {}), ("2x+6=x+10", G), ("x+6=10", G), ("x=4", RG)],
                    ["괄호 풀기", "양변 −x", "양변 −6"], x0=130, head="식 ②")
parts += p
write_svg("sv2_chain_a.svg", parts, max(xe1, xe2) + 60, 250)

# 공방 예시: 답 7인 방정식 / 해가 없는 방정식
parts = []
p, xe1 = term_chain(70, [("4x−5=2x+9", {}), ("2x−5=9", G), ("2x=14", G), ("x=7", RG)],
                    ["양변 −2x", "양변 +5", "양변 ÷2"], x0=130, head="예시 1")
parts += p
p, xe2 = term_chain(180, [("3x+4=3x+9", {}), ("4=9", RG)],
                    ["양변 −3x"], x0=130, head="예시 2")
parts += p
parts += label(xe2 + 30, 187, "→ 거짓. 어떤 x를 넣어도 성립하지 않는다 - 해가 없다.", 20, 700, "start")
write_svg("sw_chain_a.svg", parts, xe2 + 560, 250)

# 양초: 식 풀기
scale_chain("s_candle_chain_a.svg", [("30−4t=20−t", {}), ("30=20+3t", G), ("10=3t", G), ("t=10/3", RG)],
            ["양변 +4t", "양변 −20", "양변 ÷3"])
# 양초 변형: 차이 5cm - 두 경우
parts = []
p, xe1 = term_chain(70, [("(30−4t)−(20−t)=5", {}), ("10−3t=5", G), ("3t=5", G), ("t=5/3", RG)],
                    ["정리", "양변 +3t, −5", "양변 ÷3"], x0=160, head="가는 쪽이 5cm 김")
parts += p
p, xe2 = term_chain(180, [("(20−t)−(30−4t)=5", {}), ("3t−10=5", G), ("3t=15", G), ("t=5", RG)],
                    ["정리", "양변 +10", "양변 ÷3"], x0=160, head="굵은 쪽이 5cm 김")
parts += p
write_svg("sv_candle_chain_a.svg", parts, max(xe1, xe2) + 60, 250)

# 도전: 나이 문제
scale_chain("sc1_chain_a.svg", [("40+x=3(10+x)", {}), ("40+x=30+3x", G), ("10+x=3x", G), ("10=2x", G), ("x=5", RG)],
            ["괄호 풀기", "양변 −30", "양변 −x", "양변 ÷2"])
