# Praveen Hospitals, Vijayawada — website redesign preview

Free pitch preview of a bilingual (Telugu + English) redesign of praveenhospitals.com.
Not the hospital's live website. Content and photos are from the hospital's current site.

## Pages
Home · About Us · Services · Specialities · Patient Care · Empanelments · Gallery · Contact Us

## Edit and rebuild
Page content lives in `build.py` (plus the reusable sections in `_parts.json` and base styles in `_style.css`).

```bash
python3 build.py
```

## Run locally
```bash
python3 server.py   # http://localhost:8080 — public, no login
```

## Deploy (Railway)
Built from the `Dockerfile`. The preview is public (no login) but sends noindex headers and a Disallow-all robots.txt.
To require a login again, set `PREVIEW_REQUIRE_LOGIN=1` and `PREVIEW_PASSWORD` in Railway variables (user `praveen`).

## Before going live
- Native-speaker review of all Telugu text
- Confirm the front-desk WhatsApp number, then set `PREVIEW = false` and `WHATSAPP` in `build.py` and rebuild
- Real test lists and prices for the health-checkup packages
- Host photos and video locally instead of loading them from the current site
- Remove the preview banner and the `noindex` headers
