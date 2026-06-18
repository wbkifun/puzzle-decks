# 논리퍼즐 수업 — reveal.js 슬라이드 덱

중학생 5명 토론 수업(주 1회 90분)을 위한 32주 슬라이드.

## 구조
- `content/weekNN.json` — 퍼즐 콘텐츠 (디자인과 분리)
- `design-system/` — 디자인 토큰·컴포넌트. **Claude Design(claude.ai/design)에서
  제작 → DesignSync로 동기화.** 손으로 고치지 말 것 (BRIEF.md / README.md 참고).
- `build.py` — content + design-system → `docs/weekNN/index.html` (자기완결형 단일 파일)
- `deploy.sh` — 재빌드 + GitHub Pages 게시
- `docs/` — GitHub Pages 게시 루트 (자기완결형이라 오프라인 더블클릭도 작동)

## 사용
    python3 build.py            # 전체 재빌드
    python3 build.py content/week01.json   # 특정 주차
    ./deploy.sh "메시지"        # 빌드+게시

발표: 덱 열고 F(전체화면), S(발표자 노트/교사용 발문).
