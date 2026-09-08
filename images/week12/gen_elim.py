#!/usr/bin/env python3
"""세로 소거(가감법) 그림 - 두 식을 위아래로 놓고 더하거나 빼면 문자 하나가 지워진다.
지워지는 항은 빨간 취소선. 텍스트는 g transform 지역좌표, 변수는 KaTeX_Math 이탤릭."""
import re

INK = "#111111"; GRAY = "#9a9a9a"; RED = "#c62828"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"
MATH_FONT = "KaTeX_Math, 'Times New Roman', serif"

# 검증
assert 6 + 4 == 10 and 6 - 4 == 2
assert 9 + 6 == 15 and 9 - 6 == 3
assert 2 * 7 + 3 == 17 and 7 + 3 == 10
assert 3 * 6 + 2 * 4 == 26 and 6 + 4 == 10


def mathify(text, size):
    return re.sub(r"[xyz]", lambda m: (f'<tspan font-family="{MATH_FONT}" font-style="italic" '
                                       f'font-weight="400" font-size="{size + 3}">{m.group(0)}</tspan>'), text)


def txt(x, y, s, size=26, weight=700, anchor="middle", color=INK, math=True):
    body = mathify(s, size) if math else s
    return (f'<g transform="translate({x},{y})"><text x="0" y="0" text-anchor="{anchor}" font-family="{FONT}"'
            f' font-size="{size}" font-weight="{weight}" fill="{color}">{body}</text></g>')


def elim(name, cols, rows, op, result, note, killed, W=None, label_rows=None):
    """cols: x좌표 리스트(항 자리) - rows: 각 식의 항 리스트. op: '+' 또는 '−'.
    result: 결과행 항 리스트. killed: 취소선 그을 (row,col)들 + 결과행은 ('r',col)."""
    xs = cols
    W = W or (xs[-1] + 150)
    parts = []
    y0 = 60
    for r, row in enumerate(rows):
        y = y0 + r * 56
        for c, t in enumerate(row):
            if t:
                parts.append(txt(xs[c], y, t))
        if label_rows:
            parts.append(txt(xs[0] - 60, y, label_rows[r], 20, 700, "end", INK, False))
    parts.append(txt(xs[0] - 60 - (75 if label_rows else 0), y0 + 56, op, 30))
    ly = y0 + 56 * len(rows) - 28
    parts.append(f'<line x1="{xs[0] - 40}" y1="{ly}" x2="{xs[-1] + 60}" y2="{ly}" stroke="{INK}" stroke-width="3"/>')
    ry = ly + 46
    for c, t in enumerate(result):
        if t:
            parts.append(txt(xs[c], ry, t, 26, 800))
    for (r, c) in killed:
        y = (ry if r == "r" else y0 + r * 56)
        parts.append(f'<line x1="{xs[c] - 34}" y1="{y - 9}" x2="{xs[c] + 34}" y2="{y - 9}" '
                     f'stroke="{RED}" stroke-width="3.5"/>')
    parts.append(txt((xs[0] + xs[-1]) / 2, ry + 52, note, 21, 700, "middle", RED, True))
    open(name, "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {ry + 80}" width="{W}" height="{ry + 80}">\n'
        + "\n".join(parts) + "\n</svg>\n")
    print("wrote", name)


C = [120, 200, 280, 360, 440]
# 확인 3: 더하면 y가 지워진다
elim("sr3_add_a.svg", C, [["x", "+y", "=", "10"], ["x", "−y", "=", "2"]], "+",
     ["2x", "", "=", "12"], "+y와 −y가 서로 지운다 - y가 사라졌다!",
     [(0, 1), (1, 1)])
# 변형 1: 합 15 차 3
elim("sv1_add_a.svg", C, [["x", "+y", "=", "15"], ["x", "−y", "=", "3"]], "+",
     ["2x", "", "=", "18"], "y 소거 → x=9, 대입하면 y=6",
     [(0, 1), (1, 1)])
# 변형 2: 빼면 y가 지워진다
elim("sv2_sub_a.svg", C, [["2x", "+y", "=", "17"], ["x", "+y", "=", "10"]], "−",
     ["x", "", "=", "7"], "+y와 +y는 빼야 지워진다 → x=7, y=3",
     [(0, 1), (1, 1)])
# 변형 3: ②×2로 짝을 맞춘 뒤 뺀다
elim("sv3_mul_a.svg", C, [["3x", "+2y", "=", "26"], ["2x", "+2y", "=", "20"]], "−",
     ["x", "", "=", "6"], "짝이 안 맞으면 만든다: ②×2 → 2y끼리 소거 → x=6, y=4",
     [(0, 1), (1, 1)], label_rows=["①", "②×2"])
# 공방 심화: 해가 없는 쌍
elim("sw_none_a.svg", C, [["x", "+y", "=", "10"], ["x", "+y", "=", "12"]], "−",
     ["0", "", "=", "−2"], "거짓 - 동시에 만족하는 (x, y)는 없다: 해 없음",
     [(0, 0), (0, 1), (1, 0), (1, 1)])
