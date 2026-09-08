#!/usr/bin/env python3
from chainlib import *

# ---- 검증 ----
assert 6 + 4 == 10 and 6 - 4 == 2                              # 사다리
assert 6 - (10 - 6) == 2                                       # 대입
assert (4, 4, 2) == (4, 4, 2) and 4 + 4 + 2 == 10 and 2*4 + 4*4 + 8*2 == 40 and 4 == 2*2   # 학·거북·문어
for z, y, x in ((1, 7, 2), (2, 4, 4), (3, 1, 6)):
    assert x + y + z == 10 and 2*x + 4*y + 8*z == 40           # 식 2개일 때의 세 답
assert 3*300 + 2*400 == 1700 and 300 + 400 == 700              # 문구점
assert 7 + 1 + 2 == 10 and 3*7 + 1 == 22                       # 승점
assert 70 - 10 == 50 + 10 and 70 + 10 == 2 * (50 - 10)         # 돈 주고받기
for cocks, hens, chicks in ((0, 25, 75), (4, 18, 78), (8, 11, 81), (12, 4, 84)):
    assert cocks + hens + chicks == 100 and 5*cocks + 3*hens + chicks/3 == 100   # 백계 문제

# ---- 대입법: y 자리에 10−x를 갈아 끼운다 ----
parts, xe = term_chain(85, [("x−y=2", {}), ("x−(10−x)=2", G), ("2x−10=2", G), ("x=6", RG)],
                       ["y에 10−x 대입", "정리", "저울·되감기"], x0=60)
write_svg("sr4_subst_a.svg", parts, xe + 60, 170)

# ---- 개념: 소거의 사다리 (미지수 n → n−1) ----
parts, xe = term_chain(85, [("미지수 2 · 식 2", {}), ("미지수 1 · 식 1", G), ("x=6", RG), ("y=4", RG)],
                       ["문자 하나 지우기", "지난주 저울", "거슬러 대입"], x0=60)
write_svg("concept_ladder_a.svg", parts, xe + 60, 170)

# ---- 학·거북·문어: 소거 사다리 3→2→1, 그리고 거슬러 올라가기 ----
parts = []
p, xe1 = term_chain(70, [("미지수 3 · 식 3", {}), ("미지수 2 · 식 2", G), ("미지수 1 · 식 1", G), ("z=2", RG)],
                    ["y=2z 대입", "머리 식 대입", "저울"], x0=130, head="내려가기")
parts += p
p, xe2 = term_chain(180, [("z=2", RG), ("y=2z=4", {}), ("x=10−y−z=4", {})],
                    ["거슬러", "거슬러"], x0=130, head="올라오기")
parts += p
write_svg("s_animals_chain_a.svg", parts, max(xe1, xe2) + 60, 250)

# ---- 도전 2: 돈 주고받기 ----
parts = []
p, xe1 = term_chain(70, [("x−10=y+10", {}), ("x=y+20", G)], ["정리"], x0=130, head="식 ①")
parts += p
p, xe2 = term_chain(180, [("x+10=2(y−10)", {}), ("y+30=2y−20", G), ("y=50, x=70", RG)],
                    ["①의 x 대입", "저울"], x0=130, head="식 ②")
parts += p
write_svg("sc2_money_a.svg", parts, max(xe1, xe2) + 60, 250)
