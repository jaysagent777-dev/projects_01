# -*- coding: utf-8 -*-
"""Shared core for redesigns that keep each client's ORIGINAL layout and identity.

Unlike sitegen.py (one design for everyone), here every site supplies its own header, footer,
CSS and page bodies that mirror its current website — this module only provides:
  - write_site(): page shell (preview banner, noindex, modal) + copies classic.js / server.py
  - nav(): accessible dropdown menu that becomes a hamburger menu on phones
  - slider(), ticker(), form(), gallery() building blocks with no styling opinions
"""
import html as _html
import shutil
from pathlib import Path

from sitegen import ic  # noqa: F401  (re-exported for site builders)

TEMPLATE = Path(__file__).resolve().parent
esc = _html.escape

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
img{display:block;max-width:100%}
a{color:inherit;text-decoration:none}
button{font:inherit;cursor:pointer}
.preview-bar{background:#111827;color:#cbd5e1;text-align:center;font:12.5px/1.4 -apple-system,Segoe UI,Roboto,sans-serif;padding:6px 12px}
.preview-bar b{color:#fff}
/* nav with dropdowns */
.nv{position:relative}
.nv>ul{display:flex;list-style:none}
.nv li{position:relative}
.nv .dd{position:absolute;top:100%;left:0;min-width:240px;list-style:none;opacity:0;visibility:hidden;transform:translateY(8px);transition:.18s;z-index:60}
.nv li:hover>.dd,.nv li:focus-within>.dd{opacity:1;visibility:visible;transform:none}
.nv .dd a{display:block;white-space:nowrap}
.nv .caret{display:inline-block;margin-left:5px;font-size:.7em;opacity:.7}
.burger{display:none;background:none;border:0;padding:8px}
.burger span{display:block;width:24px;height:2px;background:currentColor;margin:5px 0;transition:.2s}
/* slider */
.slider{position:relative;overflow:hidden}
.slider .sl{position:absolute;inset:0;opacity:0;transition:opacity .9s ease;visibility:hidden}
.slider .sl.on{opacity:1;visibility:visible;position:relative}
.slider .sl img{width:100%;height:100%;object-fit:cover}
.slider .s-arr{position:absolute;top:50%;transform:translateY(-50%);z-index:3;border:0;width:44px;height:44px;border-radius:50%;font-size:24px;line-height:1}
.slider .s-prev{left:14px}.slider .s-next{right:14px}
.slider .s-dots{position:absolute;left:0;right:0;bottom:14px;display:flex;justify-content:center;gap:8px;z-index:3}
.slider .s-dots button{width:10px;height:10px;border-radius:99px;border:0;background:rgba(255,255,255,.6);padding:0;transition:width .3s}
.slider .s-dots button[aria-current]{width:28px;background:#fff}
/* ticker */
.tick{display:flex;align-items:center;overflow:hidden}
.tick .tk-lbl{flex:0 0 auto;font-weight:700;white-space:nowrap}
.tick .tk-win{flex:1;overflow:hidden;min-width:0}
.tick .tk-track{display:inline-flex;white-space:nowrap;animation:tk 40s linear infinite}
.tick .tk-track span{padding-right:48px}
.tick:hover .tk-track{animation-play-state:paused}
@keyframes tk{to{transform:translateX(-50%)}}
/* modal + lightbox + reveal */
.modal{position:fixed;inset:0;z-index:90;background:rgba(15,20,30,.55);display:none;place-items:center;padding:20px}
.modal.open{display:grid}
.modal .box{background:#fff;border-radius:16px;max-width:440px;width:100%;padding:24px;box-shadow:0 30px 80px rgba(0,0,0,.3);font-family:-apple-system,Segoe UI,Roboto,sans-serif}
.modal h3{margin-bottom:8px;font-size:19px}
.modal p{color:#5b6573;font-size:14px}
.modal pre{white-space:pre-wrap;font:14px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:14px;margin:12px 0 16px;color:#14532d}
.modal .mbtn{border:0;border-radius:10px;padding:10px 18px;background:#e5e7eb;font-weight:600}
.lightbox{position:fixed;inset:0;z-index:90;background:rgba(10,12,18,.92);display:none;place-items:center;padding:24px}
.lightbox.open{display:grid}
.lightbox img{max-width:min(1100px,100%);max-height:86vh;border-radius:10px}
.lightbox .lb-x{position:absolute;top:16px;right:20px;width:44px;height:44px;border-radius:50%;border:0;background:#fff;font-size:26px}
.reveal{opacity:0;transform:translateY(14px);transition:opacity .6s ease,transform .6s ease}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}.tick .tk-track{animation:none}html{scroll-behavior:auto}}
@media (max-width:980px){
  .burger{display:block}
  .nv>ul{display:none;position:absolute;top:100%;left:0;right:0;flex-direction:column;z-index:70;max-height:75vh;overflow:auto}
  .nv.open>ul{display:flex}
  .nv .dd{position:static;opacity:1;visibility:visible;transform:none;display:none;min-width:0}
  .nv li.sub-open>.dd{display:block}
}
"""


def nav(items, active, cls=""):
    """items: list of (key_or_href, label, [ (href, label), ... ] or None). Active top item gets aria-current."""
    out = f'<nav class="nv {cls}" aria-label="Main"><button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button><ul>'
    for key, label, sub in items:
        href = key if ("." in key or key.startswith("http") or key.startswith("#")) else f"{key}.html"
        cur = ' aria-current="page"' if key == active else ""
        if sub:
            out += f'<li class="has-dd"><a href="{href}"{cur}>{label}<span class="caret">▼</span></a><ul class="dd">' + "".join(
                f'<li><a href="{h}">{l}</a></li>' for h, l in sub) + "</ul></li>"
        else:
            out += f'<li><a href="{href}"{cur}>{label}</a></li>'
    return out + "</ul></nav>"


def slider(images, cls="", overlay=""):
    """images: list of (src, alt) or (src, alt, caption_html). Optional overlay HTML is placed on top."""
    cur = ' aria-current="true"'
    def one(i, im):
        s, a = im[0], im[1]
        cap = f'<div class="sl-cap">{im[2]}</div>' if len(im) > 2 else ""
        lazy = "" if i == 0 else ' loading="lazy"'
        return f'<div class="sl{" on" if i == 0 else ""}"><img src="{s}" alt="{esc(a)}"{lazy}>{cap}</div>'
    return (f'<div class="slider {cls}" aria-roledescription="carousel">'
            + "".join(one(i, im) for i, im in enumerate(images))
            + overlay
            + '<button class="s-arr s-prev" aria-label="Previous">‹</button><button class="s-arr s-next" aria-label="Next">›</button><div class="s-dots">'
            + "".join(f'<button aria-label="Slide {i+1}"{cur if i == 0 else ""}></button>' for i in range(len(images)))
            + "</div></div>")


def ticker(label, items, cls=""):
    body = "".join(f"<span>{x}</span>" for x in items)
    return f'<div class="tick {cls}"><span class="tk-lbl">{label}</span><div class="tk-win"><div class="tk-track">{body}{body.replace("<span>", "<span aria-hidden=&quot;true&quot;>").replace("&quot;", chr(34))}</div></div></div>'


def form(title, fields, button, cls=""):
    """fields: (id, label, type, required, options). Submitting shows the composed WhatsApp message (preview)."""
    rows = ""
    for fid, label, typ, req, opts in fields:
        r = " required" if req else ""
        if typ == "select":
            ctl = f'<select id="{fid}" data-label="{esc(label)}">' + "".join(f"<option>{o}</option>" for o in opts) + "</select>"
        elif typ == "textarea":
            ctl = f'<textarea id="{fid}" rows="3" data-label="{esc(label)}"{r}></textarea>'
        else:
            ctl = f'<input id="{fid}" type="{typ}" data-label="{esc(label)}"{r}>'
        rows += f'<div class="fld"><label for="{fid}">{label}</label>{ctl}</div>'
    return f'<form class="enq {cls}" data-title="{esc(title)}" novalidate>{rows}<button type="submit" class="enq-btn">{button}</button></form>'


def gallery(images, cls=""):
    return (f'<div class="gal {cls}">' + "".join(f'<button class="gi" data-full="{u}"><img src="{u}" alt="Photo {i+1}" loading="lazy"></button>' for i, u in enumerate(images))
            + '</div>')


def write_site(out, S, pages, css, header, footer):
    """pages: {key: (title, body_html)}; header/footer: callables(active_key) -> html"""
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    (out / "styles.css").write_text(BASE_CSS + css, encoding="utf-8")
    shutil.copy(TEMPLATE / "classic.js", out / "site.js")
    shutil.copy(TEMPLATE / "server.py", out / "server.py")
    (out / "Dockerfile").write_text("FROM python:3.12-slim\nWORKDIR /app\nCOPY . ./\nENV PYTHONUNBUFFERED=1\nCMD [\"python\", \"server.py\"]\n")
    (out / ".dockerignore").write_text("site.py\nPITCH.md\nREADME.md\n__pycache__\n")
    (out / "pages.txt").write_text("\n".join(pages) + "\n")
    for key, (title, body) in pages.items():
        (out / f"{key}.html").write_text(f"""<!DOCTYPE html>
<!-- REDESIGN PREVIEW for {S["domain"]} — private concept that keeps the original site's layout, not the live site. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {esc(S["name"])} (redesign preview)</title>
<meta name="description" content="{esc(S["description"])}">
<meta name="robots" content="noindex">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="preview-bar"><b>Redesign preview</b> — prepared for {S["name"]}. Not the live website.</div>
{header(key)}
<main>
{body}
</main>
{footer(key)}
<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="mTitle"><div class="box">
  <h3 id="mTitle">Your WhatsApp message is ready</h3>
  <p>On the live site this opens WhatsApp straight to the {S["desk"]}. In this preview, nothing is sent.</p>
  <pre id="mText"></pre><button class="mbtn" id="mClose">Close</button>
</div></div>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo"><button class="lb-x" aria-label="Close">×</button><img alt=""></div>
<script>window.SITE = {{ name: {S["name"]!r} }};</script>
<script src="site.js"></script>
</body>
</html>
""", encoding="utf-8")
    print("built", out.name + ":", ", ".join(f"{k}.html" for k in pages))
