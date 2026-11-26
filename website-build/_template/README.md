# Website redesign template

Turns a short Python config into a full, modern, multi-page preview site — the design system
from the Praveen Hospitals redesign, recoloured from each client's brand colours.

```
website-build/
  _template/            sitegen.py (blocks + build), base.css, site.js, server.py
  hospitals/<client>/   site.py  → python3 site.py builds the pages here
  schools/<client>/     site.py
```

New client: copy a `site.py`, change `S` (name, colours, logo, phone, tabs) and `PAGES`
(built from blocks: slider, strip, two_col, tiles, icon_cards, stats, timeline, people,
locations, gallery, enquiry_form, cta_band, page_hero), then run `python3 site.py`.

Every preview is noindex'd, labelled as a preview, and its forms never send anything.
