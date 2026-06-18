# design-system/ — Claude Design 연동 지점

이 디렉터리는 **수업 슬라이드의 디자인 단일 원천(single source of truth)** 이다.
내용물은 **Claude Design(claude.ai/design)에서 제작 → DesignSync(MCP)로 이 경로에 동기화**된다.
손으로 직접 고치지 말 것 — Claude Design에서 고치고 다시 내려받는다.

## 파일과 계약(contract)
`build.py`는 아래 파일·클래스 이름에 의존한다. **이름은 유지, 값(스타일)만 교체**하면
1~32주 모든 덱이 자동으로 새 룩으로 재빌드된다.

- `tokens.css` — Phase accent 4종, 의미색(가정/모순/결론/함정), 타이포, 베이스.
  `body[data-phase="1..4"]` 스위치로 단계 색 전환.
- `components/components.css` — 수학 시각 컴포넌트:
  - `table.truth` (+ `td.ok/td.no`, `tr.win`) — 진리표/경우 검사
  - `.proof-flow .step(.contra)` — 가정→모순 흐름도
  - `ol.reason` — 번호 추론 단계
  - `.trapbox` — 함정/흔한 오답
  - `.reveal-box .concept` — 개념 등장 리빌

## 워크플로
1. Claude Design에서 디자인 시스템 제작/수정 (프롬프트: ../PROMPT_claude_design.md 참고)
2. DesignSync로 이 디렉터리에 동기화
3. `python3 build.py` → docs/weekNN/index.html 재생성
4. `./deploy.sh` → GitHub Pages 게시

> 콘텐츠(퍼즐 내용)는 `../content/weekNN.json`에 있고 디자인과 분리되어 있다.
> 디자인을 바꿔도 콘텐츠는 건드리지 않는다(그 반대도 마찬가지).
