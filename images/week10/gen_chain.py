#!/usr/bin/env python3
"""사다리 스텝 1 · 미니 카드 체인(연산 순서를 카드로) 흑백 스케치 SVG.

- r1_chain_q.svg (문제): [3]→[×2]→[+10]→[÷2]→[−처음 수]→[?] 두 줄(3, 10).
1단 박스 - 연산자와 숫자만, 한글 설명 없음(사용자 피드백: 문장 속 '-' 체인은 빼기와 혼동).
텍스트는 g transform 지역좌표(크로미움 배율 버그 회피).
실행: python3 gen_chain.py
"""

INK = "#111111"
GRAY = "#e4e4e4"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 검증
assert ((3 * 2 + 10) / 2) - 3 == 5 and ((10 * 2 + 10) / 2) - 10 == 5


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


def chain(cy, start_text):
    """[시작]→[×2]→[+10]→[÷2]→[−처음 수]→[?] 한 줄."""
    parts = []
    x = 60
    specs = [(58, start_text, GRAY), (64, "×2", "#ffffff"), (78, "+10", "#ffffff"),
             (64, "÷2", "#ffffff"), (118, "−처음 수", "#ffffff")]
    for k, (w, t, f) in enumerate(specs):
        p, x = mini_card(x, cy, w, t, size=22 if len(t) > 3 else 23, fill=f)
        parts += p
        parts += arrow_r(x + 6, x + 34, cy)
        x += 40
    p, x = mini_card(x, cy, 58, "?", dashed=True)
    parts += p
    return parts, x


parts = []
c1, xe = chain(70, "3")
parts += c1
c2, _ = chain(180, "10")
parts += c2
W, H = xe + 60, 250
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("r1_chain_q.svg", "w", encoding="utf-8").write(svg)
print("wrote r1_chain_q.svg")
