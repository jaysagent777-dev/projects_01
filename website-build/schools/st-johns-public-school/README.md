# St. John's Public School, Vijayawada — website redesign preview

Private pitch preview of a modern redesign of stjohnspublicschool.com. Not the organisation's live website.
Content and photos are taken from their current site.

**Pages:** Home · About · Academics · Campus & Facilities · Activities · Admissions & Contact

## Build
```bash
python3 site.py          # regenerates all pages from the shared template in ../../_template
```

## Run locally with a password
```bash
PREVIEW_PASSWORD=choose-one python3 server.py   # http://localhost:8080, user: preview
```

## Before going live
- Confirm every fact, phone number and address with the organisation
- Confirm the WhatsApp number, then set `whatsapp` in `site.py` and `PREVIEW = false` in `site.js`
- Host photos locally instead of loading them from the current site
- Remove the preview banner, `noindex` and the password server
