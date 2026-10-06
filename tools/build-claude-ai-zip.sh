#!/usr/bin/env bash
# Build the claude.ai skill upload. claude.ai expects promptgremlin/SKILL.md inside the archive.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/promptgremlin.zip
(cd skills && zip -qr ../dist/promptgremlin.zip promptgremlin \
  -x '*/__pycache__/*' 'promptgremlin/scripts/tests/*')
# claude.ai's validator may reject unknown frontmatter keys: drop `context: fork` from the zip copy only.
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
unzip -q dist/promptgremlin.zip promptgremlin/SKILL.md -d "$stage"
grep -v '^context: fork$' "$stage/promptgremlin/SKILL.md" > "$stage/SKILL.md"
(cd "$stage" && mkdir -p promptgremlin && cp SKILL.md promptgremlin/SKILL.md && zip -q "$OLDPWD/dist/promptgremlin.zip" promptgremlin/SKILL.md)
if unzip -l dist/promptgremlin.zip | grep -q ' promptgremlin/SKILL.md$'; then
  echo "built dist/promptgremlin.zip"
else
  echo "promptgremlin/SKILL.md missing from archive" >&2
  exit 1
fi
