#!/usr/bin/env python3
"""워밍업 2 · 체스판의 두 색 — 흑백 스케치 SVG 생성 (문제용 _q / 풀이용 _a).

TikZ 대신 SVG 직접 저작: 이 시스템 texlive는 한글(fontspec/kotex) 지원이
빠져 있고, 덱이 자기완결형 HTML이라 SVG가 그대로 인라인되어 덱 폰트
(Pretendard)로 라벨이 렌더된다. 실행: python3 gen_w2_board.py
"""

INK = "#111111"          # 검은 칸·선 (흑백 스케치)
FONT = "Pretendard, 'NanumSquareRound', sans-serif"


def board(x0, y0, n, cell, sw_grid=1.5, sw_frame=3):
    """좌하단이 검은 칸인 n×n 체스판. (x0,y0)=좌상단."""
    p = []
    for i in range(n):          # 열
        for j in range(n):      # 행 (0=아래)
            if (i + j) % 2 == 0:
                x, y = x0 + i * cell, y0 + (n - 1 - j) * cell
                p.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{INK}"/>')
    for k in range(n + 1):      # 격자
        p.append(f'<line x1="{x0 + k*cell}" y1="{y0}" x2="{x0 + k*cell}" y2="{y0 + n*cell}" stroke="{INK}" stroke-width="{sw_grid}"/>')
        p.append(f'<line x1="{x0}" y1="{y0 + k*cell}" x2="{x0 + n*cell}" y2="{y0 + k*cell}" stroke="{INK}" stroke-width="{sw_grid}"/>')
    p.append(f'<rect x="{x0}" y="{y0}" width="{n*cell}" height="{n*cell}" fill="none" stroke="{INK}" stroke-width="{sw_frame}"/>')
    return p


def pair_outline(x, y, w, h):
    """이웃 두 칸 강조 — 칸 경계에 맞춘 도미노 테 (흰 헤일로로 검은 칸 위에서도 보이게)."""
    return [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="#ffffff" stroke-width="7.5"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{INK}" stroke-width="4"/>',
    ]


def caption(cx, y, lines, size=21):
    t = [f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" fill="{INK}">']
    for k, ln in enumerate(lines):
        t.append(f'<tspan x="{cx}" dy="{0 if k == 0 else size + 5}">{ln}</tspan>')
    t.append("</text>")
    return ["".join(t)]


def figure(captions):
    parts = []
    BOT = 296                                # 모든 판의 아래 변
    CAP = BOT + 34                           # 캡션 기준선

    c1 = 33                                  # 패널 1: 8×8
    parts += board(24, BOT - 8 * c1, 8, c1)
    parts += caption(24 + 4 * c1, CAP, captions[0])

    x2 = 356                                 # 패널 2: 7×7
    parts += board(x2, BOT - 7 * c1, 7, c1)
    parts += caption(x2 + 3.5 * c1, CAP, captions[1])

    c3, x3 = 46, 668                         # 패널 3: 4×4 확대 + 이웃 두 칸 강조
    y3 = BOT - 4 * c3
    parts += board(x3, y3, 4, c3)
    parts += pair_outline(x3 + 0.03 * c3, y3 + 1.03 * c3, 1.94 * c3, 0.94 * c3)   # 가로: 검+흰
    parts += pair_outline(x3 + 2.03 * c3, y3 + 2.03 * c3, 0.94 * c3, 1.94 * c3)   # 세로: 흰+검
    parts += caption(x3 + 2 * c3, CAP, captions[2])

    W, H = 880, 396
    # 배경 사각형 없음(투명) → 슬라이드에 인라인해도 배경색과 자연스럽게 어울림
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">\n'
            + "\n".join(parts) + "\n</svg>\n")


VARIANTS = {
    # 문제 슬라이드용 — 정답 미노출, 질문형 캡션
    "w2_board_q.svg": [["8×8 — 검과 흰, 어느 쪽이 많을까?"],
                       ["7×7이라면?"],
                       ["이웃 두 칸의 색은", "어떤 관계?"]],
    # 풀이 슬라이드용 — 정답 캡션
    "w2_board_a.svg": [["8×8 — 검 32 · 흰 32"],
                       ["7×7 — 검 25 · 흰 24"],
                       ["이웃 두 칸은 언제나", "검 1 + 흰 1"]],
}

for name, caps in VARIANTS.items():
    open(name, "w", encoding="utf-8").write(figure(caps))
    print("wrote", name)
