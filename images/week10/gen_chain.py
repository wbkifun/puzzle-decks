#!/usr/bin/env python3
"""미니 카드 체인(연산 순서를 카드로) 흑백 스케치 SVG - 1단 박스, 연산자·숫자만.

- r1_chain_q.svg  (스텝 1): [3]→[×2]→[+10]→[÷2]→[−처음 수]→[?] 두 줄(3, 10).
- v1_chain_q.svg  (변형 1): [×2]→[+6]→[÷2]→[−처음 수]→[?] - 바뀐 카드(+6)만 회색.
- v2_chain_q.svg  (변형 2): [×3]→[+12]→[÷3]→[−처음 수]→[?] - 바뀐 카드 회색.
- v3_chain_q.svg  (변형 3·고장): [×3]→[+10]→[÷2]→[−처음 수]→[?] - 어긋난 짝(×3·÷2) 회색.
- sc2_chain_a.svg (도전 2 풀이): 간 길 [x]→[×2]→[+8]→[r], 되감기 [r]→[−8]→[÷2]→[x].
사용자 피드백: 문장 속 '-' 체인은 빼기와 혼동 + 카드가 가시성이 좋다 → 전 페이지 카드화.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_chain.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증
assert ((3 * 2 + 10) / 2) - 3 == 5 and ((10 * 2 + 10) / 2) - 10 == 5
assert ((7 * 2 + 6) / 2) - 7 == 3                      # 변형 1
assert ((5 * 3 + 12) / 3) - 5 == 4                     # 변형 2
assert ((3 * 3 + 10) / 2) - 3 != ((10 * 3 + 10) / 2) - 10   # 변형 3: 고장(답이 흔들림)
assert (9 * 2 + 8) == 26 and (26 - 8) / 2 == 9         # 거꾸로 마술


def label(x, y, text, size=20, weight=400, anchor="middle"):
    return [f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{INK}">{text}</text></g>']


def mini_card(x, cy, w, text, size=23, dashed=False, fill="#ffffff"):
    """1단 미니 카드: 연산자·숫자만. (x = 왼쪽 끝, cy = 세로 중심). 오른쪽 끝 x를 반환."""
    h = 56
    dash = ' stroke-dasharray="7 6"' if dashed else ""
    p = [f'<rect x="{x}" y="{cy - h / 2}" width="{w}" height="{h}" rx="10" '
         f'fill="{fill}" stroke="{INK}" stroke-width="2.4"{dash}/>']
    p += label(x + w / 2, cy + 8, text, size, 700)
    return p, x + w


def arrow_r(x1, x2, y, sw=2.2):
    return [f'<line x1="{x1}" y1="{y}" x2="{x2 - 9}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>',
            f'<polygon points="{x2},{y} {x2 - 13},{y - 7} {x2 - 13},{y + 7}" fill="{INK}"/>']


def chain_row(cy, specs, x0=60, head=None):
    """specs = [(w, text, fill, dashed)] 를 화살표로 이은 한 줄. head는 줄 왼쪽 라벨."""
    parts = []
    x = x0
    if head:
        parts += label(x0 - 14, cy + 7, head, 19, 700, "end")
    for k, (w, t, f, d) in enumerate(specs):
        if k:
            parts += arrow_r(x + 6, x + 34, cy)
            x += 40
        p, x = mini_card(x, cy, w, t, size=22 if len(t) > 3 else 23, fill=f, dashed=d)
        parts += p
    return parts, x


def write_svg(name, parts, w, h):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
           + "\n".join(parts) + "\n</svg>\n")
    open(name, "w", encoding="utf-8").write(svg)
    print(f"wrote {name}")


W_ = "#ffffff"
Q = (58, "?", W_, True)

# ---------- r1: 두 줄 (3, 10) ----------
parts = []
row = [(58, "3", GRAY, False), (64, "×2", W_, False), (78, "+10", W_, False),
       (64, "÷2", W_, False), (118, "−처음 수", W_, False), Q]
p, xe = chain_row(70, row)
parts += p
row[0] = (58, "10", GRAY, False)
p, _ = chain_row(180, row)
parts += p
write_svg("r1_chain_q.svg", parts, xe + 60, 250)

# ---------- v1: +6만 회색 ----------
parts = []
p, xe = chain_row(85, [(64, "×2", W_, False), (64, "+6", GRAY, False),
                       (64, "÷2", W_, False), (118, "−처음 수", W_, False), Q])
parts += p
write_svg("v1_chain_q.svg", parts, xe + 60, 170)

# ---------- v2: ×3·+12·÷3 회색 ----------
parts = []
p, xe = chain_row(85, [(64, "×3", GRAY, False), (78, "+12", GRAY, False),
                       (64, "÷3", GRAY, False), (118, "−처음 수", W_, False), Q])
parts += p
write_svg("v2_chain_q.svg", parts, xe + 60, 170)

# ---------- v3: 어긋난 짝 ×3·÷2 회색 ----------
parts = []
p, xe = chain_row(85, [(64, "×3", GRAY, False), (78, "+10", W_, False),
                       (64, "÷2", GRAY, False), (118, "−처음 수", W_, False), Q])
parts += p
write_svg("v3_chain_q.svg", parts, xe + 60, 170)

# ---------- sc2: 간 길 / 되감기 ----------
parts = []
p, xe = chain_row(70, [(58, "x", GRAY, False), (64, "×2", W_, False),
                       (64, "+8", W_, False), (58, "r", GRAY, False)], x0=130, head="간 길")
parts += p
p, _ = chain_row(180, [(58, "r", GRAY, False), (64, "−8", W_, False),
                       (64, "÷2", W_, False), (58, "x", GRAY, False)], x0=130, head="되감기")
parts += p
write_svg("sc2_chain_a.svg", parts, xe + 60, 250)
