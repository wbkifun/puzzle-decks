#!/usr/bin/env bash
# 전체 덱 재빌드 → 커밋 → GitHub Pages 게시
set -euo pipefail
cd "$(dirname "$0")"

python3 build.py
git add -A
if git diff --cached --quiet; then
  echo "변경 없음 — 게시 생략"; exit 0
fi
git commit -m "${1:-update decks}"
git push
echo "✓ 게시 완료. 잠시 후 Pages URL에서 확인 (보통 30~60초)."
