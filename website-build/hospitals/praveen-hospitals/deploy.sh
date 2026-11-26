#!/usr/bin/env bash
# One-command deploy for the Praveen Hospitals preview:
#   1. rebuild the 8 pages from build.py
#   2. regenerate the client PDF (proposal/Praveen-Hospitals-New-Website.pdf)
#   3. commit this folder and push the branch to GitHub
#   4. deploy to Railway and check the live URL answers without a login
# Usage: ./deploy.sh ["commit message"]
set -euo pipefail
cd "$(dirname "$0")"

RAILWAY_PROJECT="6b9472bf-7c4e-4253-9ee8-6c0aa440ca3c"
RAILWAY_SERVICE="praveen-hospitals-preview"
RAILWAY_ENV="production"
LIVE_URL="https://praveen-hospitals-preview-production.up.railway.app"
MSG="${1:-Update Praveen Hospitals preview}"

echo "→ Building pages"
python3 build.py

echo "→ Building PDF"
python3 - <<'EOF'
from pathlib import Path
from playwright.sync_api import sync_playwright
src = Path("proposal/proposal.html").resolve()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(src.as_uri(), wait_until="load")
    pg.pdf(path="proposal/Praveen-Hospitals-New-Website.pdf", format="A4", print_background=True, prefer_css_page_size=True,
           display_header_footer=True, header_template="<span></span>",
           footer_template='<div style="font-size:7pt;color:#888;width:100%;text-align:center;font-family:Helvetica">'
                           'Praveen Hospitals · New website · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>')
    b.close()
EOF

echo "→ Committing and pushing"
git add -A .
if git diff --cached --quiet; then
  echo "  nothing new to commit"
else
  git commit -q -m "$MSG"
fi
git push -u origin HEAD

echo "→ Deploying to Railway"
railway up --project "$RAILWAY_PROJECT" --service "$RAILWAY_SERVICE" --environment "$RAILWAY_ENV" --ci

echo "→ Checking $LIVE_URL"
for i in $(seq 1 30); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$LIVE_URL/" || true)
  if [ "$code" = "200" ]; then echo "  live, no login (HTTP 200)"; exit 0; fi
  sleep 5
done
echo "  still HTTP $code after 150s — check the Railway dashboard" >&2
exit 1
