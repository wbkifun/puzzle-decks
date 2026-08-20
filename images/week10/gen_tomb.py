#!/usr/bin/env python3
"""응용 2(정점) · 디오판토스의 묘비 흑백 스케치 SVG.

- p6_tomb_q.svg (문제): 묘비와 비문 - 답 실마리 미노출.
- s6_life_a.svg (풀이): 인생 84년을 조각 막대로 - 14+7+12+5+42+4 = 84.
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_tomb.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
# 변수 x는 LaTeX 이탤릭 - 덱에 인라인된 KaTeX_Math 웹폰트 사용(단독 열람 시 serif italic 폴백)
MATH_FONT = "KaTeX_Math, 'Times New Roman', serif"

# 검증: x/6 + x/12 + x/7 + 5 + x/2 + 4 = x -> x = 84
x = 84
seg = [x // 6, x // 12, x // 7, 5, x // 2, 4]
assert seg == [14, 7, 12, 5, 42, 4] and sum(seg) == x


def caption(cx, y, lines, size=21):
    # 텍스트는 g translate 지역좌표로 - 큰 절대좌표 텍스트 배율 버그 회피(6주차 확립 규칙)
    t = [f'<g transform="translate({cx},{y})"><text x="0" y="0" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="0" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text></g>")
    return ["".join(t)]


def label(x_, y, text, size=20, weight=400, anchor="middle"):
    return [f'<g transform="translate({x_},{y})"><text x="0" y="0" text-anchor="{anchor}" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{INK}">{text}</text></g>']


def math_label(x_, y, text, size=20, weight=400, anchor="middle"):
    """'x'만 KaTeX 이탤릭으로 감싼 수식 라벨."""
    body = text.replace("x", f'<tspan font-family="{MATH_FONT}" font-style="italic" '
                             f'font-weight="400" font-size="{size + 2}">x</tspan>')
    return [f'<g transform="translate({x_},{y})"><text x="0" y="0" text-anchor="{anchor}" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{INK}">{body}</text></g>']


# ---------- q: 묘비 ----------
parts = []
CX, TOP, W_, H_ = 330, 60, 460, 330
L, R = CX - W_ / 2, CX + W_ / 2
parts.append(f'<path d="M {L} {TOP + H_} L {L} {TOP + 70} Q {L} {TOP} {CX} {TOP} Q {R} {TOP} {R} {TOP + 70} '
             f'L {R} {TOP + H_} Z" fill="#ffffff" stroke="{INK}" stroke-width="3"/>')
parts.append(f'<rect x="{L - 34}" y="{TOP + H_}" width="{W_ + 68}" height="26" fill="{GRAY}" stroke="{INK}" stroke-width="2.4"/>')
lines = [
    ("여기 디오판토스 잠들다", 21, 700),
    ("인생의 1/6은 소년이었고", 18, 400),
    ("다시 1/12이 지나 수염이 났으며", 18, 400),
    ("다시 1/7이 지나 결혼하였다", 18, 400),
    ("5년 뒤 아들을 얻었으나", 18, 400),
    ("아들은 아버지 인생의 절반만 살았고", 18, 400),
    ("아들을 보내고 4년 뒤 그도 잠들었다", 18, 400),
]
y = TOP + 64
for (t, s, w) in lines:
    parts += label(CX, y, t, s, w)
    y += 38
parts += caption(CX, TOP + H_ + 78, ["디오판토스는 몇 살까지 살았을까?"], 22)
W, H = 660, 510
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p6_tomb_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p6_tomb_q.svg")

# ---------- a: 인생 조각 막대 ----------
parts = []
BX, BY, BH = 60, 120, 60
S = 8                                     # 1년 = 8px
names = ["소년", "수염", "결혼까지", "아들 출생", "아들과 함께", "마지막"]
fills = [GRAY, "#ffffff", GRAY, "#ffffff", GRAY, "#ffffff"]
xx = BX
for k, (n, yrs, f) in enumerate(zip(names, seg, fills)):
    w = yrs * S
    parts.append(f'<rect x="{xx}" y="{BY}" width="{w}" height="{BH}" fill="{f}" stroke="{INK}" stroke-width="2.2"/>')
    parts += label(xx + w / 2, BY + 38, str(yrs), 20, 700)
    # 이름표는 위아래 번갈아
    if k % 2 == 0:
        parts += label(xx + w / 2, BY - 14, n, 17)
    else:
        parts += label(xx + w / 2, BY + BH + 26, n, 17)
    xx += w
parts += math_label(BX, BY - 52, "x/6 + x/12 + x/7 + 5 + x/2 + 4 = x", 23, 700, "start")
parts += label(xx + 16, BY + 38, "= 84년", 23, 700, "start")
parts += caption((BX + xx) / 2, BY + BH + 84, ["나이는 6·12·7로 나누어져야 - 84의 배수. 사람의 수명에서 후보는 84 하나뿐"], 21)
W, H = 860, 300
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s6_life_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s6_life_a.svg")
