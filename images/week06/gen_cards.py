#!/usr/bin/env python3
"""생일 마술 카드(서브 p6·풀이 s6 3장)와 도전 3(자작 설계) 흑백 스케치 SVG.

- p6_bday_q.svg  (문제): 1~31 생일 카드 5장(A~E, 실제 수 전부 표기) - 슬라이드엔 제목과 이 카드만.
  첫 수 강조·비밀 힌트는 없음(학생이 스스로 발견).
- s6a_reveal_a.svg (풀이 1): 비밀 공개 - 21이면 A·C·E를 고르게 되고 첫 수 합 1+4+16=21.
- s6b_unique_a.svg (풀이 2): 유일한 분해 - 21은 16·4·1이 각각 '필수'가 되는 사슬.
- s6c_binary_a.svg (풀이 3): 이름표(○×) = 분해표 = 이진법 10101, 2⁵=32 ≥ 31.
- c3_design_q.svg (도전): 후보·도구 재료 → 나만의 맞히기 퍼즐 (정답 횟수는 비밀).
실행: python3 gen_cards.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

LETTERS = ["A", "B", "C", "D", "E"]
REPS = [1, 2, 4, 8, 16]
CARDS = [[n for n in range(1, 32) if n & r] for r in REPS]
for r, nums in zip(REPS, CARDS):
    assert len(nums) == 16 and nums[0] == r          # 각 카드 16개, 첫 수 = 대표수

N = 21                                               # 풀이 예시: 21 = 16+4+1
picked = [r for r in REPS if N & r]
assert sum(picked) == N and picked == [1, 4, 16]


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


# ---------- p6 문제: 생일 카드 5장 (수 전부 표기, 슬라이드를 채우는 큰 판형) ----------
# 카드마다 <g transform>으로 지역좌표를 쓴다 - 큰 절대좌표의 텍스트가 덱 안에서
# 도형과 다른 배율로 그려지는 크로미움 렌더 버그(5주차 figH 사례와 동류) 우회.
parts = []
cw, ch, gap = 200, 356, 18
for k, (letter, nums) in enumerate(zip(LETTERS, CARDS)):
    g = [f'<text x="{cw/2}" y="46" text-anchor="middle" font-family="{FONT}" font-size="42" font-weight="800" fill="{INK}">{letter}</text>',
         f'<rect x="0" y="64" width="{cw}" height="{ch}" rx="14" fill="#ffffff" stroke="{INK}" stroke-width="3.2"/>']
    for r_ in range(4):                              # 4×4 숫자 배열 - 행도 g translate로(큰 y좌표 텍스트 회피)
        row = [f'<text x="{36 + c_*44}" y="0" text-anchor="middle" font-family="{FONT}" font-size="30" fill="{INK}">{nums[r_*4+c_]}</text>'
               for c_ in range(4)]
        g.append(f'<g transform="translate(0,{138 + r_*82})">' + "".join(row) + "</g>")
    parts.append(f'<g transform="translate({28 + k * (cw + gap)},0)">' + "".join(g) + "</g>")
W, H = 28 * 2 + 5 * cw + 4 * gap, 434
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p6_bday_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p6_bday_q.svg")

# ---------- s6a 풀이 1: 비밀 공개 (21 = A·C·E) ----------
parts = []
cw, ch = 108, 118
for k, (letter, rep) in enumerate(zip(LETTERS, REPS)):
    x = 34 + k * (cw + 16)
    on = rep in picked
    parts.append(f'<text x="{x+cw/2}" y="34" text-anchor="middle" font-family="{FONT}" font-size="27" font-weight="800" fill="{INK}">{letter}</text>')
    parts.append(f'<rect x="{x}" y="50" width="{cw}" height="{ch}" rx="10" fill="{"#e2e2e2" if on else "#ffffff"}" stroke="{INK}" stroke-width="{3.4 if on else 2.2}"/>')
    parts.append(f'<text x="{x+cw/2}" y="{50+56}" text-anchor="middle" font-family="{FONT}" font-size="36" font-weight="700" fill="{INK}">{rep}</text>')
    parts.append(f'<text x="{x+cw/2}" y="{50+88}" text-anchor="middle" font-family="{FONT}" font-size="16" fill="{INK}" opacity="0.7">카드의 첫 수</text>')
    mark = "○ 골랐다" if on else "× 안 골랐다"
    parts.append(f'<text x="{x+cw/2}" y="{50+ch+34}" text-anchor="middle" font-family="{FONT}" font-size="20" '
                 f'font-weight="{700 if on else 400}" fill="{INK}">{mark}</text>')
cx = 34 + (5 * cw + 4 * 16) / 2
parts += caption(cx, 258, ["생일이 21일이라면 - 21이 적힌 카드는 A·C·E뿐이라 그 셋을 고르게 된다"], 22)
parts += caption(cx, 306, ["마술사의 계산: 고른 카드의 첫 수 합 = 1 + 4 + 16 = 21 - 즉석에서 맞힌다!"], 22)
W, H = int(cx * 2), 336
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s6a_reveal_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s6a_reveal_a.svg")

# ---------- s6b 풀이 2: 유일한 분해 사슬 ----------
parts = []


def bx(x, w, text, y=120, bold=False):
    return [f'<rect x="{x}" y="{y}" width="{w}" height="62" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>',
            f'<text x="{x+w/2}" y="{y+40}" text-anchor="middle" font-family="{FONT}" font-size="25" '
            f'font-weight="{700 if bold else 400}" fill="{INK}">{text}</text>']


def ar(x1, x2, y, label):
    return [f'<line x1="{x1}" y1="{y}" x2="{x2-11}" y2="{y}" stroke="{INK}" stroke-width="3"/>',
            f'<polygon points="{x2},{y} {x2-14},{y-7} {x2-14},{y+7}" fill="{INK}"/>',
            f'<text x="{(x1+x2)/2}" y="{y-16}" text-anchor="middle" font-family="{FONT}" font-size="18" fill="{INK}">{label}</text>']


parts += bx(28, 110, "21", bold=True)
parts += ar(148, 344, 151, "16은 필수 - 없으면 최대 15")
parts += bx(354, 130, "남은 5")
parts += ar(494, 682, 151, "4는 필수 - 없으면 최대 3")
parts += bx(692, 130, "남은 1")
parts += ar(832, 928, 151, "1로 마무리")
parts += bx(938, 96, "0 · 끝", bold=True)
parts += caption(530, 64, ["큰 수부터 따져 보면 매 걸음 선택의 여지가 없다 (1+2+4+8 = 15 < 16)"], 22)
parts += caption(530, 244, ["그래서 21 = 16 + 4 + 1 - 다른 방법은 없다. 1~31의 모든 수가 이렇게 딱 한 가지로 분해된다"], 22)
W, H = 1062, 280
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s6b_unique_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s6b_unique_a.svg")

# ---------- s6c 풀이 3: 이름표 = 이진법 ----------
parts = []
cols = list(zip(LETTERS, REPS))[::-1]                # E(16) D(8) C(4) B(2) A(1)
x0, step = 250, 96
rows_y = {"letter": 66, "rep": 96, "mark": 156, "bit": 216}
parts.append(f'<text x="{x0-120}" y="{rows_y["letter"]+14}" font-family="{FONT}" font-size="21" font-weight="700" fill="{INK}">카드</text>')
parts.append(f'<text x="{x0-120}" y="{rows_y["mark"]}" font-family="{FONT}" font-size="21" font-weight="700" fill="{INK}">고른다?</text>')
parts.append(f'<text x="{x0-120}" y="{rows_y["bit"]}" font-family="{FONT}" font-size="21" font-weight="700" fill="{INK}">이진법</text>')
bits = []
for i, (letter, rep) in enumerate(cols):
    x = x0 + i * step
    on = bool(N & rep)
    bits.append("1" if on else "0")
    parts.append(f'<text x="{x}" y="{rows_y["letter"]}" text-anchor="middle" font-family="{FONT}" font-size="28" font-weight="800" fill="{INK}">{letter}</text>')
    parts.append(f'<text x="{x}" y="{rows_y["rep"]}" text-anchor="middle" font-family="{FONT}" font-size="17" fill="{INK}" opacity="0.7">({rep})</text>')
    parts.append(f'<text x="{x}" y="{rows_y["mark"]}" text-anchor="middle" font-family="{FONT}" font-size="30" '
                 f'font-weight="{700 if on else 400}" fill="{INK}">{"○" if on else "×"}</text>')
    parts.append(f'<text x="{x}" y="{rows_y["bit"]}" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="{INK}">{"1" if on else "0"}</text>')
assert int("".join(bits), 2) == N                    # 10101₂ = 21
parts.append(f'<text x="{x0 + 4*step + 70}" y="{rows_y["mark"]}" font-family="{FONT}" font-size="23" fill="{INK}">= 16+4+1 = 21</text>')
parts.append(f'<text x="{x0 + 4*step + 70}" y="{rows_y["bit"]}" font-family="{FONT}" font-size="23" fill="{INK}">= 10101₂</text>')
cx = 470
parts += caption(cx, 282, ["이름표(고른다/안 고른다) = 분해표 = 이진법 표기 - 다섯 글자의 가짓수는 2⁵ = 32 ≥ 31",
                           "1~100 판은 카드 7장(1·2·4·8·16·32·64): 2⁷ = 128 ≥ 100 - 스무고개가 7번인 것과 같은 이유"], 21)
W, H = 940, 340
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s6c_binary_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s6c_binary_a.svg")

# ---------- c3 도전: 1~15 마법사 카드 만들기 (빈 카드 A~D) ----------
LETTERS4 = ["A", "B", "C", "D"]
REPS4 = [1, 2, 4, 8]
CARDS4 = [[n for n in range(1, 16) if n & r] for r in REPS4]
for r, nums in zip(REPS4, CARDS4):
    assert len(nums) == 8 and nums[0] == r

parts = []
cw, ch, gap = 182, 210, 22
for k, letter in enumerate(LETTERS4):
    g = [f'<text x="{cw/2}" y="40" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="800" fill="{INK}">{letter}</text>',
         f'<rect x="0" y="56" width="{cw}" height="{ch}" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>']
    for r_ in range(2):                              # 빈 기입란(점선) 4×2
        for c_ in range(4):
            g.append(f'<rect x="{16 + c_*38}" y="{92 + r_*62}" width="30" height="34" rx="6" '
                     f'fill="none" stroke="{INK}" stroke-width="1.6" stroke-dasharray="5 4" opacity="0.55"/>')
    g.append(f'<text x="{cw/2}" y="238" text-anchor="middle" font-family="{FONT}" font-size="19" fill="{INK}" opacity="0.75">어떤 수들을 적을까?</text>')
    parts.append(f'<g transform="translate({30 + k * (cw + gap)},0)">' + "".join(g) + "</g>")
cx = 30 + (4 * cw + 3 * gap) / 2
parts += caption(cx, 322, ["1~15의 수를 맞히는 카드 4장 - 각 칸에 들어갈 수를 직접 정하라"], 22)
W, H = int(cx * 2), 348
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("c3_cards_q.svg", "w", encoding="utf-8").write(svg)
print("wrote c3_cards_q.svg")

# ---------- sc3 예시 풀이: 완성된 카드 A~D ----------
parts = []
for k, (letter, rep, nums) in enumerate(zip(LETTERS4, REPS4, CARDS4)):
    g = [f'<text x="{cw/2}" y="40" text-anchor="middle" font-family="{FONT}" font-size="32" font-weight="800" fill="{INK}">{letter}</text>',
         f'<rect x="0" y="56" width="{cw}" height="176" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>']
    for i, n in enumerate(nums):                     # 4×2 숫자 배열, 첫 수는 굵게
        cx_ = 33 + (i % 4) * 40
        cy_ = 112 + (i // 4) * 62
        g.append(f'<text x="{cx_}" y="{cy_}" text-anchor="middle" font-family="{FONT}" font-size="25" '
                 f'font-weight="{700 if i == 0 else 400}" fill="{INK}">{n}</text>')
    g.append(f'<text x="{cw/2}" y="262" text-anchor="middle" font-family="{FONT}" font-size="19" fill="{INK}">첫 수 = {rep}</text>')
    parts.append(f'<g transform="translate({30 + k * (cw + gap)},0)">' + "".join(g) + "</g>")
cx = 30 + (4 * cw + 3 * gap) / 2
parts += caption(cx, 312, ["카드 X = ‘분해에 X를 쓰는 수들의 목록’ - 첫 수는 1 · 2 · 4 · 8",
                           "검산: 13 = 8+4+1 → D·C·A에만 있다 ✓ · 가짓수: 2⁴ = 16 ≥ 15 (3장은 2³ = 8 < 15라 부족)"], 21)
W, H = int(cx * 2), 350
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("sc3_cards_a.svg", "w", encoding="utf-8").write(svg)
print("wrote sc3_cards_a.svg")
