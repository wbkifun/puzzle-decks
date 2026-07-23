#!/usr/bin/env python3
"""수 범위(무대 설정·메인 문제·도전 1)와 반씩 자르기 풀이 흑백 스케치 SVG.

- setup_range.svg  (설정): 1~100 띠 + 예/아니오 질문 말풍선(중립 예시 ‘홀수니?’ - 반반 전략 미노출).
- p2_range_q.svg   (문제): 1~16 타일 띠 + 몇 번?
- s2_halving_a.svg (풀이): 16→8→4→2→1 막대 반감 + 두 배의 사다리.
- p3_range_q.svg   (문제): 1~100 띠 + 7번이면 충분할까?
- s3_chain_a.svg   (풀이): 100→50→25→13→7→4→2→1 사슬 + 2⁷=128≥100.
- c1_range_q.svg   (도전): 1~1000 · 1~1,000,000 띠 + 몇 번?
실행: python3 gen_ranges.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

# 최악의 경우 사슬 검증: 100에서 반씩(큰 쪽) 7번이면 1
chain = [100]
while chain[-1] > 1:
    chain.append((chain[-1] + 1) // 2)
assert chain == [100, 50, 25, 13, 7, 4, 2, 1], chain
assert len(chain) - 1 == 7


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


def strip(x, y, w, h, left, right, ticks=9):
    """수 범위 띠: 양 끝 라벨 + 눈금."""
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>']
    for k in range(1, ticks + 1):
        tx = x + w * k / (ticks + 1)
        p.append(f'<line x1="{tx:.1f}" y1="{y+h*0.28}" x2="{tx:.1f}" y2="{y+h*0.72}" stroke="{INK}" stroke-width="1.6"/>')
    p.append(f'<text x="{x-14}" y="{y+h/2+9}" text-anchor="end" font-family="{FONT}" font-size="26" font-weight="700" fill="{INK}">{left}</text>')
    p.append(f'<text x="{x+w+14}" y="{y+h/2+9}" font-family="{FONT}" font-size="26" font-weight="700" fill="{INK}">{right}</text>')
    return p


def bubble(x, y, w, h, text, size=23, tail="down"):
    ty = y + h
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>']
    if tail == "down":
        p.append(f'<polygon points="{x+w*0.22},{ty} {x+w*0.32},{ty} {x+w*0.2},{ty+16}" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>')
    p.append(f'<text x="{x+w/2}" y="{y+h/2+size*0.34}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">{text}</text>')
    return p


def arrow_d(x, y1, y2, label=None):
    p = [f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-12}" stroke="{INK}" stroke-width="2.6"/>',
         f'<polygon points="{x},{y2} {x-6.5},{y2-13} {x+6.5},{y2-13}" fill="{INK}"/>']
    if label:
        p.append(f'<text x="{x+14}" y="{(y1+y2)/2+6}" font-family="{FONT}" font-size="19" fill="{INK}">{label}</text>')
    return p


def arrow_r(x1, x2, y, label=None):
    p = [f'<line x1="{x1}" y1="{y}" x2="{x2-11}" y2="{y}" stroke="{INK}" stroke-width="2.6"/>',
         f'<polygon points="{x2},{y} {x2-13},{y-6.5} {x2-13},{y+6.5}" fill="{INK}"/>']
    if label:
        p.append(f'<text x="{(x1+x2)/2}" y="{y-12}" text-anchor="middle" font-family="{FONT}" font-size="18" fill="{INK}">{label}</text>')
    return p


# ---------- setup: 1~100 띠 + 규칙 ----------
parts = []
parts += bubble(90, 40, 280, 62, "“그 수, 홀수니?”", 24)
parts += bubble(470, 40, 220, 62, "“아니오.”", 24)
parts += strip(90, 170, 560, 46, "1", "100")
parts += caption(370, 300, ["술래의 수는 1~100 중 하나 · 질문은 ‘예/아니오’로 답할 수 있는 것만",
                            "몇 번이면 확실히 맞힐 수 있을까?"])
W, H = 760, 350
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("setup_range.svg", "w", encoding="utf-8").write(svg)
print("wrote setup_range.svg")

# ---------- p2: 1~16 타일 ----------
parts = []
S, G = 40, 6
for k in range(16):
    x = 30 + k * (S + G)
    parts.append(f'<rect x="{x}" y="90" width="{S}" height="{S}" rx="6" fill="#ffffff" stroke="{INK}" stroke-width="2"/>')
    parts.append(f'<text x="{x+S/2}" y="{90+S*0.66}" text-anchor="middle" font-family="{FONT}" font-size="17" fill="{INK}">{k+1}</text>')
parts.append(f'<text x="{30 + 8*(S+G) - G/2}" y="60" text-anchor="middle" font-family="{FONT}" font-size="26" font-weight="700" fill="{INK}">후보 16개</text>')
parts += caption(30 + 8 * (S + G) - G / 2, 200, ["어떤 대답이 돌아와도 끝까지 통하는 질문 목록 -", "몇 번이면 반드시 맞힐 수 있을까?"], 22)
W, H = 800, 250
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p2_range_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p2_range_q.svg")

# ---------- s2: 16→8→4→2→1 반감 막대 + 두 배의 사다리(조각 개수로) ----------
parts = []
x0, unit, bh = 60, 26, 34
labels = [16, 8, 4, 2, 1]
for i, n in enumerate(labels):
    y = 34 + i * (bh + 26)
    parts.append(f'<rect x="{x0}" y="{y}" width="{n*unit}" height="{bh}" rx="7" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>')
    parts.append(f'<text x="{x0+n*unit+12}" y="{y+bh*0.72}" font-family="{FONT}" font-size="24" font-weight="700" fill="{INK}">{n}</text>')
    if i < 4:
        parts += arrow_d(x0 + n * unit / 2, y + bh + 2, y + bh + 26, f"질문 {i+1} - 반으로")
parts += caption(x0 + 8 * unit, 356, ["질문마다 최악의 경우 후보가 반으로 - 4번이면 반드시"], 22)
lx = 585
parts.append(f'<text x="{lx}" y="52" font-family="{FONT}" font-size="24" font-weight="700" fill="{INK}">두 배의 사다리</text>')
ts, tg = 16, 4                                       # 층마다 후보를 작은 조각 개수로
for i, v in enumerate([16, 8, 4, 2, 1]):
    y = 84 + i * 52
    for k in range(v):
        parts.append(f'<rect x="{lx + k*(ts+tg)}" y="{y}" width="{ts}" height="{ts}" rx="4" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>')
    parts.append(f'<text x="{lx + 16*(ts+tg) + 10}" y="{y+ts-1}" font-family="{FONT}" font-size="21" fill="{INK}">{v}개 - 질문 {4-i}번</text>')
parts += caption(lx + 230, 356, ["후보 ×2 = 질문 +1"], 22)
W, H = 1080, 392
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s2_halving_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s2_halving_a.svg")

# ---------- p3: 1 2 3 … 98 99 100 숫자 조각 ----------
parts = []
cells = ["1", "2", "3", "4", "5", "6", "…", "98", "99", "100"]
S, G = 54, 8
x = 40
mid = 0
for c in cells:
    if c == "…":
        parts.append(f'<text x="{x+22}" y="{90+S*0.62}" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="{INK}">⋯</text>')
        x += 44 + G
        continue
    parts.append(f'<rect x="{x}" y="90" width="{S}" height="{S}" rx="7" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>')
    parts.append(f'<text x="{x+S/2}" y="{90+S*0.64}" text-anchor="middle" font-family="{FONT}" font-size="21" fill="{INK}">{c}</text>')
    x += S + G
mid = (40 + x - G) / 2
parts.append(f'<text x="{mid}" y="56" text-anchor="middle" font-family="{FONT}" font-size="27" font-weight="700" fill="{INK}">이번엔 후보 100개</text>')
parts += caption(mid, 196, ["소문: “7번이면 반드시 맞힐 수 있다” - 정말일까?", "홀수 개가 남으면 어떻게 가르는 게 최선일까?"], 22)
W, H = int(x + 36), 252
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p3_range_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p3_range_q.svg")

# ---------- s3: 100→…→1 사슬(화살표에 실행 횟수) + 사다리 ----------
parts = []
y, bw, bh, gap = 96, 84, 56, 52
xs = 26
for i, n in enumerate(chain):
    x = xs + i * (bw + gap)
    bold = 700 if i in (0, len(chain) - 1) else 400
    parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>')
    parts.append(f'<text x="{x+bw/2}" y="{y+bh*0.64}" text-anchor="middle" font-family="{FONT}" font-size="26" font-weight="{bold}" fill="{INK}">{n}</text>')
    if i < len(chain) - 1:
        parts += arrow_r(x + bw + 4, x + bw + gap - 4, y + bh / 2, f"{i+1}회")
cx = xs + (len(chain) * bw + (len(chain) - 1) * gap) / 2
parts += caption(cx, 62, ["최악의 경우 후보 수 - 일곱 계단이면 1"], 23)
parts += caption(cx, 216, ["거꾸로 두 배의 사다리: 2 · 4 · 8 · 16 · 32 · 64 · 128",
                           "2⁷ = 128 ≥ 100 - 그래서 7번이면 충분하다"], 23)
W, H = int(cx * 2 + 26), 274
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s3_chain_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s3_chain_a.svg")

# ---------- c1: 1~1000 · 1~백만 띠 ----------
parts = []
parts += strip(110, 50, 480, 42, "1", "1,000")
parts.append(f'<text x="782" y="80" font-family="{FONT}" font-size="26" font-weight="700" fill="{INK}">- 몇 번?</text>')
parts += strip(110, 150, 480, 42, "1", "1,000,000")
parts.append(f'<text x="782" y="180" font-family="{FONT}" font-size="26" font-weight="700" fill="{INK}">- 몇 번?</text>')
parts += caption(440, 268, ["‘두 배의 사다리’로 답하라 - 그리고 하나 적은 횟수로는 왜 안 되는지도"], 22)
W, H = 910, 306
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("c1_range_q.svg", "w", encoding="utf-8").write(svg)
print("wrote c1_range_q.svg")
