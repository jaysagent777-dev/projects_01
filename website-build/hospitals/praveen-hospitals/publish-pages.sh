#!/usr/bin/env bash
# Publish the built Praveen Hospitals preview to GitHub Pages.
# Only the 8 built pages, styles.css and site.js go into the Pages repo — no build
# scripts, PITCH.md, screenshots or PDF. Creates the repo and turns on Pages on first run.
# Usage: ./publish-pages.sh   (deploy.sh calls it)
set -euo pipefail
cd "$(dirname "$0")"

REPO="jaysagent777-dev/praveen-hospitals-preview"
URL="https://jaysagent777-dev.github.io/praveen-hospitals-preview/"
FILES=(index.html about.html services.html specialities.html patient-care.html empanelments.html gallery.html contact.html styles.css site.js)

if ! gh repo view "$REPO" >/dev/null 2>&1; then
  echo "  creating $REPO"
  gh repo create "$REPO" --public --description "Redesign preview for Praveen Hospitals, Vijayawada (not the live website)" >/dev/null
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
git clone -q "https://github.com/$REPO.git" "$tmp/site" 2>/dev/null || git init -q -b main "$tmp/site"
cd "$tmp/site"
git checkout -q -B main
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
for f in "${FILES[@]}"; do cp "$OLDPWD/$f" .; done
touch .nojekyll
cat > README.md <<'EOF'
# Praveen Hospitals — redesign preview

A free redesign preview of praveenhospitals.com (Telugu + English, WhatsApp booking, mobile-first).
**Not the hospital's live website.** Content and photos are from the hospital's current site.

Preview: https://jaysagent777-dev.github.io/praveen-hospitals-preview/
EOF
git add -A
if git diff --cached --quiet; then
  echo "  GitHub Pages already up to date"
else
  # same author identity as the main repo's commits
  git -c user.name="$(git -C "$OLDPWD" log -1 --format=%an)" -c user.email="$(git -C "$OLDPWD" log -1 --format=%ae)" \
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
  if [ "$code" = "200" ]; then echo "  GitHub Pages live (HTTP 200)"; exit 0; fi
  sleep 6
done
echo "  GitHub Pages still HTTP $code after 4 minutes — check https://github.com/$REPO/settings/pages" >&2
exit 1
