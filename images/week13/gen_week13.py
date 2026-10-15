#!/usr/bin/env python3
"""13주차 정수해 방정식 그림. 문제용(_q)은 상황만, 풀이용(_a)에 칠하기·✕.
텍스트는 전부 g transform 지역좌표(큰 절대좌표 text 금지 규칙). 수치는 assert로 검증.
"""
INK = "#111111"
GRAY = "#d9d9d9"
RED = "#c62828"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
MATH_FONT = "KaTeX_Math, 'Times New Roman', serif"


def makeable(gens, n_max=120):
    s = {0}
    for n in range(1, n_max + 1):
        if any(n >= g and n - g in s for g in gens):
            s.add(n)
    return s


S35 = makeable((3, 5))
S46 = makeable((4, 6))
SNUG = makeable((6, 9, 20))
assert [n for n in range(1, 16) if n not in S35] == [1, 2, 4, 7]
assert all(n in S35 for n in range(8, 120))
assert max(n for n in range(1, 120) if n not in SNUG) == 43
assert all(n in SNUG for n in range(44, 50))
assert all(n % 2 == 0 for n in S46)


def txt(x, y, s, size=20, weight=700, anchor="middle", color=INK, math=False):
    fam = f'{MATH_FONT}" font-style="italic' if math else FONT
    return (f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" font-family="{fam}"'
            f' font-size="{size}" font-weight="{weight}" fill="{color}">{s}</text></g>')


def cell(x, y, n, w=50, h=50, fill="#ffffff", mark=None, color=INK, sw=2.2, size=21):
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>',
         txt(x + w / 2, y + h / 2 + 7, str(n), size, 700, color=color)]
    if mark == "x":
        p.append(f'<line x1="{x + 8}" y1="{y + 8}" x2="{x + w - 8}" y2="{y + h - 8}" stroke="{RED}" stroke-width="3"/>')
        p.append(f'<line x1="{x + w - 8}" y1="{y + 8}" x2="{x + 8}" y2="{y + h - 8}" stroke="{RED}" stroke-width="3"/>')
    return p


def stamp(x, y, v, w=46, h=56):
    """톱니 테두리 우표: 점선 바깥 + 실선 안쪽 + 금액."""
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#ffffff" stroke="{INK}" '
            f'stroke-width="2.4" stroke-dasharray="4 3"/>',
            f'<rect x="{x + 5}" y="{y + 5}" width="{w - 10}" height="{h - 10}" fill="#ffffff" stroke="{INK}" stroke-width="1.4"/>',
            txt(x + w / 2, y + h / 2 + 7, f"{v}원", 15 if w < 60 else 22, 800)]


def write_svg(name, parts, w, h):
    open(name, "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
        + "\n".join(parts) + "\n</svg>\n")
    print("wrote", name)


def strip(y, nums, shade, x0=40, w=50, gap=6):
    p = []
    for k, n in enumerate(nums):
        x = x0 + k * (w + gap)
        if shade is None:
            p += cell(x, y, n, w)
        elif n in shade:
            p += cell(x, y, n, w, fill=GRAY)
        else:
            p += cell(x, y, n, w, mark="x")
    return p


# ---- 1. 우표 문제(상황만) ----
p = stamp(300, 30, 3, 90, 110) + stamp(560, 30, 5, 90, 110)
p += [txt(345, 175, "3원 우표 - 얼마든지", 19), txt(605, 175, "5원 우표 - 얼마든지", 19)]
p += strip(215, range(1, 16), None, x0=55)
p.append(txt(475, 315, "1원부터 15원까지 - 우표값을 정확히 맞춰 붙일 수 있는 금액은?", 20, 400))
write_svg("p_stamps_q.svg", p, 950, 340)

# ---- 2. 우표 확인: 칠하기 ----
p = strip(30, range(1, 16), S35, x0=55)
p.append(txt(475, 125, "칠한 칸: 3원·5원 우표로 정확히 맞출 수 있는 금액", 19, 400))
p.append(txt(475, 160, "✕: 1, 2, 4, 7원", 22, 800, color=RED))
write_svg("sr1_strip_a.svg", p, 950, 185)

# ---- 3. 교환 규칙: 3원 5장 = 5원 3장, 30원의 해 셋 ----
sols30 = [(x, (30 - 3 * x) // 5) for x in range(0, 11) if (30 - 3 * x) % 5 == 0]
assert sols30 == [(0, 6), (5, 3), (10, 0)]
p = []
rows = [(10, 0), (5, 3), (0, 6)]
for r, (a, b) in enumerate(rows):
    y = 30 + r * 92
    p.append(txt(120, y + 38, f"({a}, {b})", 24, 700))
    x = 200
    for _ in range(a):
        p += stamp(x, y, 3, 40, 52)
        x += 46
    if a and b:
        x += 18
    for _ in range(b):
        p += stamp(x, y, 5, 40, 52)
        x += 46
# 교환 화살표(빨강): 1행 오른쪽 5장 → 2행 5원 3장
p.append(f'<rect x="{200 + 5 * 46 - 6}" y="24" width="{5 * 46 + 6}" height="64" rx="8" fill="none" '
         f'stroke="{RED}" stroke-width="2.6" stroke-dasharray="8 5"/>')
p.append(f'<rect x="{200 + 5 * 46 + 12}" y="116" width="{3 * 46 + 6}" height="64" rx="8" fill="none" '
         f'stroke="{RED}" stroke-width="2.6" stroke-dasharray="8 5"/>')
p.append(txt(850, 112, "3원 5장 = 5원 3장", 21, 800, color=RED))
p.append(txt(850, 140, "(둘 다 15원)", 18, 400, color=RED))
p.append(txt(500, 325, "바꿔치기 한 번마다 다음 해로 건너간다", 19, 400))
write_svg("sr2_swap_a.svg", p, 1000, 345)

# ---- 4. 연속 셋이면 영원히 ----
p = []
for r in range(4):
    for c in range(3):
        n = 8 + 3 * r + c
        p += cell(330 + c * 70, 25 + r * 70, n, 58, 52, fill=GRAY if r == 0 else "#ffffff")
    if r:
        y = 25 + r * 70
        p.append(f'<path d="M318,{y - 44} q-34,22 0,44" fill="none" stroke="{RED}" stroke-width="2.4"/>')
        p.append(f'<polygon points="318,{y} 330,{y - 3} 320,{y - 11}" fill="{RED}"/>')
        p.append(txt(262, y - 14, "+3원", 18, 800, color=RED))
p.append(txt(435, 318, "⋮", 30, 700))
p.append(txt(725, 60, "← 맨 윗줄: 직접 만든 세 금액", 18, 400, anchor="start"))
p.append(txt(510, 365, "윗줄에 3원 우표 한 장씩 - 아랫줄이 끝없이 채워진다", 19, 400))
write_svg("sr3_run_a.svg", p, 1020, 385)

# ---- 5. 4원·6원: 홀수의 벽 ----
p = strip(30, range(1, 17), S46, x0=30, w=46)
p.append(txt(437, 120, "4원·6원 우표 - 칠한 칸만 가능", 19, 400))
p.append(txt(437, 155, "홀수는 몇 원이든 ✕ - 짝수끼리 더하면 짝수뿐", 21, 800, color=RED))
write_svg("sv2_even_a.svg", p, 880, 180)


# ---- 6. 너겟 상자(상황만) ----
def box(x, y, w, h, n):
    q = [f'<path d="M{x},{y} L{x + w},{y} L{x + w - 10},{y + h} L{x + 10},{y + h} Z" fill="#ffffff" '
         f'stroke="{INK}" stroke-width="2.6"/>',
         f'<path d="M{x},{y} L{x + w * 0.2},{y - 26} L{x + w * 0.8},{y - 26} L{x + w},{y}" fill="none" '
         f'stroke="{INK}" stroke-width="2.2"/>']
    cols = {6: 3, 9: 3, 20: 5}[n]
    rws = (n + cols - 1) // cols
    for k in range(n):
        cx = x + w / 2 + (k % cols - (cols - 1) / 2) * 20
        cy = y + 22 + (k // cols) * 18
        q.append(f'<ellipse cx="{cx}" cy="{cy}" rx="8" ry="6" fill="{GRAY}" stroke="{INK}" stroke-width="1.4"/>')
    q.append(txt(x + w / 2, y + h + 34, f"{n}개 상자", 22, 800))
    return q


p = box(110, 60, 110, 90, 6) + box(360, 60, 110, 90, 9) + box(620, 60, 170, 110, 20)
p.append(txt(475, 275, "가게는 이 세 가지 상자만 판다 - 낱개 판매 없음", 20, 400))
write_svg("p_nugget_q.svg", p, 950, 300)


# ---- 7. 나머지 세 줄 표: 문제용(빈 표) / 풀이용 ----
def rows_fig(name, solved):
    p = []
    names = ["3의 배수", "3으로 나누면 1 남음", "3으로 나누면 2 남음"]
    for r in range(3):
        y = 30 + r * 66
        p.append(txt(205, y + 32, names[r], 18, 700, anchor="end"))
        for c in range(17):
            n = r + 3 * c
            x = 220 + c * 48
            if solved and n == 43:
                p += cell(x, y, n, 42, 48, mark=None, color=RED, sw=3.6, size=18)
                p.append(f'<rect x="{x - 4}" y="{y - 4}" width="50" height="56" rx="9" fill="none" '
                         f'stroke="{RED}" stroke-width="3"/>')
            elif solved and n in SNUG:
                p += cell(x, y, n, 42, 48, fill=GRAY, size=18)
            else:
                p += cell(x, y, n, 42, 48, size=18)
    if solved:
        p.append(txt(630, 250, "각 줄은 한 번 칠해지면 +6·+9로 끝까지 칠해진다 - 마지막 빈칸은 43", 19, 400))
    else:
        p.append(txt(630, 250, "0부터 50까지 - 살 수 있는 개수의 칸을 칠하라", 19, 400))
    write_svg(name, p, 1060, 270)


rows_fig("pn_rows_q.svg", False)
rows_fig("sn_rows_a.svg", True)

# ---- 8. 도전 3: 0~7 짝짓기 ----
p = []
for n in range(8):
    x = 120 + n * 90
    p += cell(x, 120, n, 56, 56, fill=GRAY if n in S35 else "#ffffff")
for k in range(4):
    a, b = k, 7 - k
    assert (a in S35) != (b in S35)
    xa, xb = 148 + a * 90, 148 + b * 90
    h = 22 + k * 0 + (3 - k) * 24
    p.append(f'<path d="M{xa},112 C{xa},{112 - h - 20} {xb},{112 - h - 20} {xb},112" fill="none" '
             f'stroke="{RED}" stroke-width="2.4"/>')
p.append(txt(475, 225, "짝(합이 7)마다 정확히 하나만 칠해진다", 21, 800, color=RED))
write_svg("sc3_pairs_a.svg", p, 950, 250)
