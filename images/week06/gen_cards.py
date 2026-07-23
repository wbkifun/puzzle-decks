#!/usr/bin/env python3
"""마술사의 숫자 카드(서브 p6·풀이 s6)와 도전 3(자작 설계) 흑백 스케치 SVG.

- p6_cards_q.svg (문제): 미리 인쇄된 카드 7장(내용은 미공개 — 빼곡한 숫자 암시) + 질문 말풍선.
  1·2·4·… 구성(=풀이)은 노출하지 않는다.
- s6_cards_a.svg (풀이): 대표 수 1·2·4·8·16·32·64 카드 + 예시 37 = 32+4+1 (○×).
- c3_design_q.svg (도전): 후보·도구 재료 → 나만의 맞히기 퍼즐 (정답 횟수는 비밀).
실행: python3 gen_cards.py
"""

INK = "#111111"
FONT = "Pretendard, 'NanumSquareRound', sans-serif"

REPS = [1, 2, 4, 8, 16, 32, 64]
N = 37
picked = [r for r in REPS if N & r]
assert sum(picked) == N and picked == [1, 4, 32]


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


def bubble(x, y, w, h, text, size=23):
    ty = y + h
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>',
            f'<polygon points="{x+w*0.2},{ty} {x+w*0.3},{ty} {x+w*0.18},{ty+15}" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>',
            f'<text x="{x+w/2}" y="{y+h/2+size*0.34}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">{text}</text>']


# ---------- p6 문제: 미공개 카드 7장 ----------
parts = []
parts += bubble(150, 26, 400, 60, "“네 수가 이 카드에 있니?” × 7", 24)
cw, ch = 96, 128
for k in range(7):
    x = 34 + k * (cw + 12)
    y = 140
    parts.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2.8"/>')
    parts.append(f'<text x="{x+cw/2}" y="{y+26}" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="{INK}">카드 {k+1}</text>')
    for r in range(4):                               # 빼곡한 숫자 암시(물결선)
        yy = y + 48 + r * 20
        parts.append(f'<path d="M {x+12} {yy} q 9 -7 18 0 t 18 0 t 18 0 t 18 0" fill="none" stroke="{INK}" stroke-width="1.8" opacity="0.55"/>')
parts += caption(400, 322, ["카드 7장은 대답을 듣기 전에 미리 인쇄되어 있다 — 무엇이 적혀 있을까?"], 22)
W, H = 800, 356
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("p6_cards_q.svg", "w", encoding="utf-8").write(svg)
print("wrote p6_cards_q.svg")

# ---------- s6 풀이: 대표 수 카드 + 37 = 32+4+1 ----------
parts = []
cw, ch = 100, 118
for k, rep in enumerate(REPS):
    x = 30 + k * (cw + 14)
    y = 44
    on = rep in picked
    parts.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="{3.4 if on else 2.2}"/>')
    parts.append(f'<text x="{x+cw/2}" y="{y+52}" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="700" fill="{INK}">{rep}</text>')
    parts.append(f'<text x="{x+cw/2}" y="{y+84}" text-anchor="middle" font-family="{FONT}" font-size="16" fill="{INK}" opacity="0.7">카드의 첫 수</text>')
    mark = "○ 예" if on else "× 아니오"
    parts.append(f'<text x="{x+cw/2}" y="{y+ch+34}" text-anchor="middle" font-family="{FONT}" font-size="21" '
                 f'font-weight="{700 if on else 400}" fill="{INK}">{mark}</text>')
parts += caption(430, 250, ["술래의 수가 37이라면 — ‘예’는 1·4·32 카드에서만"], 23)
parts += caption(430, 300, ["○ 카드의 첫 수만 더하면:  32 + 4 + 1 = 37 — 즉석에서 맞힌다!"], 23)
W, H = 860, 336
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("s6_cards_a.svg", "w", encoding="utf-8").write(svg)
print("wrote s6_cards_a.svg")

# ---------- c3 도전: 나만의 맞히기 퍼즐 설계 ----------
parts = []


def ing(x, y, w, h, title, sub):
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2.6"/>',
            f'<text x="{x+w/2}" y="{y+34}" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="{INK}">{title}</text>',
            f'<text x="{x+w/2}" y="{y+64}" text-anchor="middle" font-family="{FONT}" font-size="18" fill="{INK}" opacity="0.75">{sub}</text>']


parts += ing(30, 40, 210, 84, "① 후보 집합", "요일 · 친구 · 카드 …")
parts += ing(30, 148, 210, 84, "② 도구", "예/아니오 · 저울 · 사지선다")
parts.append(f'<line x1="252" y1="136" x2="316" y2="136" stroke="{INK}" stroke-width="3"/>')
parts.append(f'<polygon points="330,136 316,129 316,143" fill="{INK}"/>')
parts.append(f'<rect x="344" y="62" width="300" height="148" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="3"/>')
parts.append(f'<text x="494" y="112" text-anchor="middle" font-family="{FONT}" font-size="24" font-weight="700" fill="{INK}">나만의 맞히기 퍼즐</text>')
parts.append(f'<text x="494" y="152" text-anchor="middle" font-family="{FONT}" font-size="21" fill="{INK}">“몇 번이면 맞힐 수 있을까?”</text>')
parts.append(f'<rect x="344" y="238" width="300" height="66" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="2.4" stroke-dasharray="8 6"/>')
parts.append(f'<text x="494" y="278" text-anchor="middle" font-family="{FONT}" font-size="20" fill="{INK}">몰래 계산한 정답 횟수 (비밀!)</text>')
parts += caption(340, 356, ["재료를 고르고 — 한계는 세기로 정확하게 심어 둘 것"], 21)
W, H = 680, 388
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       + "\n".join(parts) + "\n</svg>\n")
open("c3_design_q.svg", "w", encoding="utf-8").write(svg)
print("wrote c3_design_q.svg")
