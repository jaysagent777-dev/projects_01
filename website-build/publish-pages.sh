#!/usr/bin/env bash
# Publish a built redesign preview to its own public GitHub Pages repo.
# Only the built pages (*.html), styles.css and site.js are published — no build
# scripts, PITCH.md, servers or Dockerfiles. Creates the repo and turns on Pages on first run.
#
# Usage: ./publish-pages.sh <site-folder> [repo-name]
#   e.g. ./publish-pages.sh schools/atkinson-school
#        (repo name defaults to "<folder-name>-preview")
set -euo pipefail
cd "$(dirname "$0")"

SITE="${1:?usage: ./publish-pages.sh <site-folder> [repo-name]}"
[ -f "$SITE/index.html" ] || { echo "no index.html in $SITE" >&2; exit 1; }
OWNER="$(gh api user --jq .login)"
NAME="${2:-$(basename "$SITE")-preview}"
REPO="$OWNER/$NAME"
URL="https://$OWNER.github.io/$NAME/"
SRC="$(cd "$SITE" && pwd)"
TITLE="$(head -1 "$SRC/README.md" 2>/dev/null | sed 's/^# *//')"
TITLE="${TITLE:-$(basename "$SITE") — redesign preview}"

if ! gh repo view "$REPO" >/dev/null 2>&1; then
  echo "  creating $REPO"
  gh repo create "$REPO" --public --description "${TITLE} (not the live website)" >/dev/null
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
git clone -q "https://github.com/$REPO.git" "$tmp/site" 2>/dev/null || git init -q -b main "$tmp/site"
cd "$tmp/site"
git checkout -q -B main
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp "$SRC"/*.html .
for f in styles.css site.js; do [ -f "$SRC/$f" ] && cp "$SRC/$f" .; done
touch .nojekyll
cat > README.md <<EOF
# ${TITLE}

A free redesign preview. **Not the organisation's live website.** Content and photos are from their current site.

Preview: ${URL}
EOF
git add -A
if git diff --cached --quiet; then
  echo "  $NAME already up to date"
else
  git -c user.name="$(git -C "$SRC" log -1 --format=%an)" -c user.email="$(git -C "$SRC" log -1 --format=%ae)" \
    commit -q -m "Update preview site"
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$REPO.git"
  git push -q -u origin main
fi

if ! gh api "repos/$REPO/pages" >/dev/null 2>&1; then
  echo "  turning on GitHub Pages"
  gh api -X POST "repos/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" >/dev/null
fi

echo "  waiting for $URL"
for i in $(seq 1 40); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || true)
  if [ "$code" = "200" ]; then echo "  live: $URL"; exit 0; fi
  sleep 6
done
echo "  still HTTP $code after 4 minutes — check https://github.com/$REPO/settings/pages" >&2
exit 1
