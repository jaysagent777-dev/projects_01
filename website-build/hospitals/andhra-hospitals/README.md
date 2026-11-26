# Andhra Hospitals, Vijayawada — website redesign preview

Private pitch preview that keeps the original site's layout and identity, modernised — andhrahospitals.org. Not the organisation's live website.
Content and photos are taken from their current site.

**Pages:** Index · About · Achievements · Specialities · Services · Doctors · Gallery · Careers · Locations · Contact

## Build
```bash
python3 site.py          # regenerates all pages (layout + CSS in site.py, shared core in ../../_template/classic.py)
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
