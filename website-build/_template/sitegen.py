# -*- coding: utf-8 -*-
"""Reusable redesign-preview generator, extracted from the Praveen Hospitals build.

A site is a small Python config (see ../hospitals/andhra-hospitals/site.py) that calls the block helpers
below and then build(SITE, PAGES, out_dir). Output: static pages + styles.css + site.js + server.py.

- base.css is the Praveen design system; theme_css() recolours it from the site's brand colours.
- Every preview is marked "Redesign preview — not the live website" and noindex'd.
- Forms never submit anywhere: in preview they show the composed WhatsApp message instead.
"""
import html as _html
import shutil
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent


# ── colour helpers ───────────────────────────────────────────────────────────
def _rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def _hex(c):
    return "#" + "".join(f"{max(0, min(255, round(v))):02x}" for v in c)
def mix(a, b, t):
    x, y = _rgb(a), _rgb(b); return _hex([x[i] + (y[i] - x[i]) * t for i in range(3)])

def theme_css(primary, secondary):
    """Recolour the Praveen base.css: red family -> primary, teal family -> secondary."""
    css = (TEMPLATE / "base.css").read_text(encoding="utf-8")
    P, S = primary.lower(), secondary.lower()
    pr, sr = _rgb(P), _rgb(S)
    reps = [
        ("%23c62828", "%23" + P[1:]), ("%230e7c6b", "%23" + S[1:]),
        ("rgba(198,40,40", "rgba(%d,%d,%d" % pr), ("rgba(224,83,63", "rgba(%d,%d,%d" % _rgb(mix(P, "#ffffff", .25))),
        ("rgba(14,124,107", "rgba(%d,%d,%d" % sr),
        ("#c62828", P), ("#d63333", mix(P, "#ffffff", .1)), ("#e0533f", mix(P, "#ffb347", .35)),
        ("#a81f1f", mix(P, "#000000", .15)), ("#b62222", mix(P, "#000000", .08)), ("#9e1f1f", mix(P, "#000000", .2)), ("#8f1b1b", mix(P, "#000000", .28)),
        ("#ffe3e0", mix(P, "#ffffff", .88)), ("#ffc2bd", mix(P, "#ffffff", .72)), ("#ff8a80", mix(P, "#ffffff", .5)),
        ("#fdf0f0", mix(P, "#ffffff", .94)), ("#fdf3f2", mix(P, "#ffffff", .955)), ("#fbeeec", mix(P, "#ffffff", .93)),
        ("#0e7c6b", S), ("#13917e", mix(S, "#ffffff", .1)), ("#0b5e52", mix(S, "#000000", .25)), ("#5cc4b2", mix(S, "#ffffff", .45)),
        ("#eaf6f3", mix(S, "#ffffff", .92)), ("#f0f8f6", mix(S, "#ffffff", .95)), ("#e6f3ef", mix(S, "#ffffff", .9)), ("#e7f5f2", mix(S, "#ffffff", .91)),
    ]
    for a, b in reps:
        css = css.replace(a, b)
    return css + EXTRA_CSS


# ── icons ────────────────────────────────────────────────────────────────────
ICONS = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "pin": '<path d="M12 21s-7-4.4-7-11a7 7 0 0 1 14 0c0 6.6-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M12 14v4M10 16h4"/>',
    "wa": '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.1.3.6 1 1.3 1.6.9.8 1.6 1 1.9 1.2.2.1.4.1.5-.1l.7-.9c.2-.2.4-.2.6-.1l1.9.9c.2.1.4.2.5.3 0 .2 0 .8-.3 1.4z"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>',
    "pulse": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5V21h16"/>',
    "cap": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14.2c2.9-.4 5.5 1.3 5.5 4.3"/>',
    "bus": '<rect x="4" y="3" width="16" height="15" rx="3"/><path d="M4 11h16M8 18v3M16 18v3"/><circle cx="8" cy="14.5" r="1"/><circle cx="16" cy="14.5" r="1"/>',
    "flask": '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/><path d="M7 15h10"/>',
    "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    "trophy": '<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M17 5h3a2 2 0 0 1-2 4M7 5H4a2 2 0 0 0 2 4"/>',
    "monitor": '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "star": '<path d="M12 3l2.6 5.3 5.8.8-4.2 4.1 1 5.8L12 16.3 6.8 19l1-5.8L3.6 9.1l5.8-.8z"/>',
    "ambulance": '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/><path d="M8.5 9.5v4M6.5 11.5h4"/>',
    "lab": '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/>',
    "pill": '<rect x="2.5" y="8" width="19" height="8" rx="4" transform="rotate(-45 12 12)"/><path d="m8.5 8.5 7 7"/>',
    "scan": '<path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="3.5"/>',
    "baby": '<circle cx="12" cy="8" r="4"/><path d="M6 21a6 6 0 0 1 12 0"/><path d="M10.5 8h.01M13.5 8h.01"/>',
    "bone": '<path d="M17 10c.7-.7 1.7-.7 2.8-1.7a2.5 2.5 0 1 0-3.5-3.5 2.5 2.5 0 1 0-3.5 3.5L7 14.1a2.5 2.5 0 1 0-3.5 3.5 2.5 2.5 0 1 0 3.5 3.5c1-1 1-2.1 1.7-2.8"/>',
    "brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 3V4zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 3V4z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "building": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M10 21v-4h4v4"/>',
}
def ic(name, size=22, fill=False):
    a = 'fill="currentColor"' if fill else 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" {a} aria-hidden="true">{ICONS[name]}</svg>'

esc = _html.escape


# ── blocks ───────────────────────────────────────────────────────────────────
def head_(eyebrow, title, sub="", center=True):
    return f'<div class="head{" c" if center else ""} reveal"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>'

def section(inner, cls=""):
    return f'<section{f" class=&quot;{cls}&quot;" if cls else ""}><div class="wrap">{inner}</div></section>'.replace("&quot;", '"')

def slider(slides):
    """slides: list of (img_url, eyebrow, title, sub, [(label, href, style)], tone) ; tone 'p' or 's'."""
    out = '<section class="hero2" aria-roledescription="carousel" aria-label="Highlights"><div class="slides">'
    for i, (img, eb, title, sub, btns, tone) in enumerate(slides):
        tag = "h1" if i == 0 else "h2"
        b = "".join(f'<a class="btn {st}" href="{href}">{lab}</a>' for lab, href, st in btns)
        out += (f'<div class="slide{" on" if i == 0 else ""}{" teal" if tone == "s" else ""}" role="group" aria-roledescription="slide" '
                f'aria-label="{i+1} of {len(slides)}" style="--img:url(\'{img}\')"><div class="wrap"><div class="cap"><div class="eyebrow">{eb}</div>'
                f'<{tag}>{title}</{tag}><p>{sub}</p><div class="ctas">{b}</div></div></div></div>')
    cur = ' aria-current="true"'
    out += ('</div><div class="wrap s-ctrl"><button class="s-btn s-prev" aria-label="Previous slide">‹</button><div class="dots">'
            + "".join(f'<button aria-label="Go to slide {i+1}"{cur if i == 0 else ""}></button>' for i in range(len(slides)))
            + '</div><button class="s-btn s-next" aria-label="Next slide">›</button></div></section>')
    return out

def strip(cards):
    """cards: (icon, title, text, href or None, accent bool) — 3 cards overlapping the slider."""
    out = '<div class="wrap camp-strip">'
    for icon, title, text, href, accent in cards:
        tag = "a" if href else "div"
        attr = f' href="{href}"' if href else ""
        if accent:
            out += f'<{tag} class="cs cs-red reveal"{attr}><span class="cs-ic">{ic(icon, 26)}</span><div><b>{title}</b><span class="big">{text}</span></div></{tag}>'
        else:
            out += f'<{tag} class="cs reveal"{attr}><span class="cs-ic2">{ic(icon, 24)}</span><div><b>{title}</b><span>{text}</span></div></{tag}>'
    return out + "</div>"

def two_col(eyebrow, title, lede, right, btn=None, extra="", flip=False, cls=""):
    left = f'<div class="reveal"><div class="eyebrow">{eyebrow}</div><h2 class="h2">{title}</h2><p class="lede">{lede}</p>{extra}{f"<a class=&quot;btn btn-red&quot; href=&quot;{btn[1]}&quot;>{btn[0]} →</a>" if btn else ""}</div>'.replace("&quot;", '"')
    r = f'<div class="reveal">{right}</div>'
    return section(f'<div class="two-col">{r + left if flip else left + r}</div>', cls)

def photo(src, alt=""):
    return f'<div class="photo"><img src="{src}" alt="{esc(alt)}" loading="lazy"></div>'

def tiles(items):
    """items: (img, label, href, color)"""
    return '<div class="tiles">' + "".join(
        f'<a class="tile reveal" href="{href}" style="--sp:{col}"><img src="{img}" alt="" loading="lazy"><span>{lab}<i>→</i></span></a>' for img, lab, href, col in items) + "</div>"

def icon_cards(items, cols=3):
    """items: (icon, title, text)"""
    return f'<div class="icards c{cols}">' + "".join(
        f'<div class="icard reveal"><span class="ic">{ic(i)}</span><h3>{t}</h3><p>{x}</p></div>' for i, t, x in items) + "</div>"

def stats(items):
    """items: (icon, number_display, numeric or None, label)"""
    out = '<div class="stats">'
    for icn, shown, n, label in items:
        num = f'<b class="count" data-to="{n}">{shown}</b>' if n else f"<b>{shown}</b>"
        out += f'<div class="stat reveal"><span class="st-ic">{ic(icn, 26)}</span>{num}<span>{label}</span></div>'
    return out + "</div>"

def ticks(items, big=False):
    return f'<ul class="ticks{" big" if big else ""}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def timeline(items):
    """items: (year, text)"""
    return '<div class="tline">' + "".join(f'<div class="tl-i reveal"><b>{y}</b><p>{t}</p></div>' for y, t in items) + "</div>"

def people(items):
    """items: (img or None, name, role, text)"""
    out = '<div class="people">'
    for img, name, role, text in items:
        av = f'<img src="{img}" alt="{esc(name)}" loading="lazy">' if img else f'<span class="av">{esc(name[:1])}</span>'
        out += f'<div class="person reveal">{av}<div><h3>{name}</h3><div class="role">{role}</div><p>{text}</p></div></div>'
    return out + "</div>"

def gallery(imgs):
    return ('<div class="pgrid">' + "".join(f'<button class="ph reveal" data-full="{u}"><img src="{u}" alt="Photo {i+1}" loading="lazy"></button>' for i, u in enumerate(imgs))
            + '</div><div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo"><button class="lb-x" aria-label="Close">×</button><img alt=""></div>')

def locations(items):
    """items: (name, address, phones)"""
    def tel(p):
        return '<a href="tel:' + p.replace(" ", "").replace("-", "") + '">' + p + "</a>"
    return '<div class="centres">' + "".join(
        f'<div class="centre reveal"><span class="ic">{ic("pin")}</span><b>{n}</b><small>{a}</small><p>{" · ".join(tel(p) for p in ph)}</p></div>'
        for n, a, ph in items) + "</div>"

def cta_band(title, text, primary, phone):
    return (f'<section class="tight"><div class="wrap"><div class="cta-band reveal"><div><h2>{title}</h2><p>{text}</p></div>'
            f'<div class="cta-acts"><a class="btn btn-white" href="{primary[1]}">{primary[0]} →</a><a class="btn btn-ghost-w" href="tel:{phone.replace(" ", "").replace("-", "")}">{ic("phone", 18)}{phone}</a></div></div></div></section>')

def page_hero(crumb, title, sub, img):
    return (f'<section class="phero" style="--bg:url(\'{img}\')"><div class="wrap"><div class="crumb"><a href="index.html">Home</a> / {crumb}</div>'
            f"<h1>{title}</h1><p>{sub}</p></div></section>")

def subnav(items, active):
    """Secondary menu for a group of pages. items: (key, label)"""
    cur = ' aria-current="page"'
    return '<nav class="subnav" aria-label="In this section"><div class="wrap">' + "".join(
        f'<a href="{k}.html"{cur if k == active else ""}>{lab}</a>' for k, lab in items) + "</div></nav>"

def steps(items):
    """Numbered steps. items: (title, text)"""
    return '<div class="steps3">' + "".join(f'<div class="reveal"><b>{i+1}</b><p><strong>{t}</strong><br>{x}</p></div>' for i, (t, x) in enumerate(items)) + "</div>"

def enquiry_form(title, fields, button, note=""):
    """fields: list of (id, label, type, required, options) ; type in text,tel,email,date,select,textarea"""
    rows = ""
    for fid, label, typ, req, opts in fields:
        r = " required" if req else ""
        if typ == "select":
            ctl = f'<select id="{fid}" data-label="{esc(label)}">' + "".join(f"<option>{o}</option>" for o in opts) + "</select>"
        elif typ == "textarea":
            ctl = f'<textarea id="{fid}" rows="3" data-label="{esc(label)}"{r}></textarea>'
        else:
            ctl = f'<input id="{fid}" type="{typ}" data-label="{esc(label)}"{r}>'
        rows += f'<div class="field"><label for="{fid}">{label}</label>{ctl}</div>'
    return (f'<form class="form reveal" id="enqForm" data-title="{esc(title)}" novalidate>{rows}'
            f'<button class="btn btn-red" type="submit" style="justify-content:center">{button} →</button>{f"<small>{note}</small>" if note else ""}</form>')


# ── page shell ───────────────────────────────────────────────────────────────
def _logo(S):
    if S.get("logo"):
        return f'<img src="{S["logo"]}" alt="{esc(S["name"])}" style="{S.get("logo_style", "")}">'
    return f'<span class="wordmark"><span class="wm-badge">{S["logo_badge"]}</span><span><b>{S["logo_text"][0]}</b><small>{S["logo_text"][1]}</small></span></span>'

def _header(S, active):
    cur = ' aria-current="page"'
    active = S.get("tab_group", {}).get(active, active)   # sub-pages highlight their section's tab
    tabs = "".join(f'<li><a href="{k}.html"{cur if k == active else ""}>{label}</a></li>' for k, label in S["tabs"])
    tick = " <b>•</b> ".join(S["ticker"])
    return f"""<div class="preview"><b>Redesign preview</b> — prepared for {S["name"]}. Not the live website.</div>
<div class="ebar"><div class="wrap">
  <span class="pulse"><i></i>{S["bar_label"]}</span>
  <div class="ticker" aria-label="Announcements"><div class="tk-track"><span>{tick} <b>•</b> </span><span aria-hidden="true">{tick} <b>•</b> </span></div></div>
  <span class="ebar-r"><a href="tel:{S["phone_tel"]}">{S["phone"]}</a></span>
</div></div>
<header>
  <div class="wrap nav">
    <a class="brand" href="index.html">{_logo(S)}</a>
    <div class="act">
      <a class="btn btn-line" href="tel:{S["phone_tel"]}">{ic("phone", 18)}Call</a>
      <a class="btn btn-red" href="{S["cta"][1]}">{S["cta"][0]}</a>
    </div>
  </div>
  <nav class="tabs" aria-label="Main"><div class="wrap"><ul>{tabs}</ul></div></nav>
</header>"""

def _footer(S):
    links = "".join(f'<li><a href="{k}.html">{label}</a></li>' for k, label in S["tabs"][1:])
    contacts = "".join(f"<li>{c}</li>" for c in S["footer_contacts"])
    return f"""<footer>
  <div class="wrap">
    <div class="foot">
      <div><div class="foot-logo">{_logo(S)}</div>
        <p>{S["footer_text"]}</p><p style="margin-top:12px">{S["address"]}</p></div>
      <div><h4>Quick links</h4><ul>{links}</ul></div>
      <div><h4>{S["footer_contact_title"]}</h4><ul><li><a href="tel:{S["phone_tel"]}" style="color:#fff;font-size:20px;font-weight:800">{S["phone"]}</a></li>{contacts}</ul></div>
    </div>
    <div class="legal"><span>© 2026 {S["name"]}</span><span>Redesign preview — not the live website</span></div>
  </div>
</footer>
<nav class="mbar" aria-label="Quick actions">
  <a class="c" href="tel:{S["phone_tel"]}">{ic("phone", 20)}<span>Call</span></a>
  <a class="w" href="{S["cta"][1]}">{ic("wa", 20, True)}<span>WhatsApp</span></a>
  <a class="b" href="{S["cta"][1]}">{ic("cal", 20)}<span>{S["mbar_label"]}</span></a>
</nav>
<a class="fab-wa" href="{S["cta"][1]}" aria-label="{S["fab"]}">{ic("wa", 28, True)}<span>{S["fab"]}</span></a>
<button class="to-top" aria-label="Back to top">↑</button>
<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="mTitle"><div class="box">
  <h3 id="mTitle">Your WhatsApp message is ready</h3>
  <p style="color:var(--muted);font-size:14px">On the live site this opens WhatsApp straight to the {S["desk"]}. In this preview, nothing is sent.</p>
  <pre id="mText"></pre><div class="acts"><button class="btn btn-line" id="mClose">Close</button></div>
</div></div>"""

def build(S, PAGES, out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    (out / "styles.css").write_text(theme_css(S["primary"], S["secondary"]) + S.get("extra_css", ""), encoding="utf-8")
    shutil.copy(TEMPLATE / "site.js", out / "site.js")
    shutil.copy(TEMPLATE / "server.py", out / "server.py")
    (out / "Dockerfile").write_text("FROM python:3.12-slim\nWORKDIR /app\nCOPY . ./\nENV PYTHONUNBUFFERED=1\nCMD [\"python\", \"server.py\"]\n")
    (out / ".dockerignore").write_text("site.py\nPITCH.md\nREADME.md\n__pycache__\n")
    (out / "pages.txt").write_text("\n".join(PAGES) + "\n")
    import json as _json
    ld = ("<script type=\"application/ld+json\">" + _json.dumps(S["jsonld"], ensure_ascii=False).replace("</", "<\\/") + "</script>\n") if S.get("jsonld") else ""
    for key, page in PAGES.items():
        title, body = page[0], page[1]
        desc = page[2] if len(page) > 2 else S["description"]   # optional per-page description
        (out / f"{key}.html").write_text(f"""<!DOCTYPE html>
<!-- REDESIGN PREVIEW for {S["domain"]} — private concept, not the live site. Built from website-build/_template. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {esc(S["name"])} (redesign preview)</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex">
<link rel="stylesheet" href="styles.css">
{ld}</head>
<body{f" class=&quot;{S.get('body_class', '')}&quot;" if S.get("body_class") else ""}>
{_header(S, key)}
<main id="top">
{body}
</main>
{_footer(S)}
<script>window.SITE = {{ name: {S["name"]!r}, whatsapp: {S.get("whatsapp", "")!r} }};</script>
<script src="site.js"></script>
</body>
</html>
""".replace("&quot;", '"'), encoding="utf-8")
    print("built", out.name + ":", ", ".join(f"{k}.html" for k in PAGES))


EXTRA_CSS = """
/* ── template additions ── */
.wordmark{display:flex;align-items:center;gap:12px}
.wm-badge{width:52px;height:52px;border-radius:14px;background:linear-gradient(135deg,var(--red),#000 160%);color:#fff;display:grid;place-items:center;font-weight:800;font-size:20px;box-shadow:var(--sh-red);flex:0 0 auto}
.wordmark b{display:block;font-size:19px;color:var(--navy);letter-spacing:-.01em;line-height:1.15}
.wordmark small{display:block;font-size:12.5px;color:var(--muted);font-weight:600;letter-spacing:.04em}
.foot-logo{display:inline-block;background:#fff;border-radius:12px;padding:8px 12px;margin-bottom:14px}
.foot-logo img{height:48px}
header.scrolled .wm-badge{width:44px;height:44px}
@media (max-width:640px){.wordmark b{font-size:15px}.wordmark small{display:none}.wm-badge{width:42px;height:42px;font-size:16px}}
.hero2 .slide .wrap{padding-bottom:88px}
.s-ctrl{bottom:40px}
.camp-strip{margin-top:-28px}
.cs-ic2{width:54px;height:54px;border-radius:16px;background:var(--red-l);color:var(--red);display:grid;place-items:center;flex:0 0 auto}
.cs:nth-child(2) .cs-ic2{background:var(--teal-l);color:var(--teal)}
a.cs{transition:transform .25s,box-shadow .25s}
a.cs:hover{transform:translateY(-4px);box-shadow:var(--sh-3)}
.icards{display:grid;gap:18px}
.icards.c3{grid-template-columns:repeat(3,1fr)}
.icards.c4{grid-template-columns:repeat(4,1fr)}
.icards.c2{grid-template-columns:repeat(2,1fr)}
.icard{background:#fff;border-radius:20px;padding:26px;box-shadow:var(--sh-1);transition:transform .25s,box-shadow .25s}
.icard:hover{transform:translateY(-5px);box-shadow:var(--sh-3)}
.icard .ic{width:50px;height:50px;border-radius:14px;background:var(--red-l);color:var(--red);display:grid;place-items:center;margin-bottom:14px}
.icard:nth-child(even) .ic{background:var(--teal-l);color:var(--teal)}
.icard h3{font-size:19px;margin-bottom:8px}
.icard p{color:var(--muted);font-size:15px}
.tline{display:grid;grid-template-columns:repeat(4,1fr);gap:0;position:relative;margin-top:10px}
.tline::before{content:"";position:absolute;left:0;right:0;top:9px;height:2px;background:linear-gradient(90deg,var(--red),var(--teal))}
.tl-i{position:relative;padding:36px 22px 0 0}
.tl-i::before{content:"";position:absolute;top:2px;left:0;width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:0 0 0 3px var(--red)}
.tl-i:nth-child(even)::before{box-shadow:0 0 0 3px var(--teal)}
.tl-i b{display:block;font-size:26px;font-weight:800;color:var(--navy);margin-bottom:8px}
.tl-i p{color:var(--muted);font-size:15px}
.people{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.people .person{display:grid;grid-template-columns:110px 1fr;gap:22px;background:#fff;border:0;border-radius:20px;padding:24px;box-shadow:var(--sh-1)}
.people .person img,.people .av{width:110px;height:130px;border-radius:16px;object-fit:cover;object-position:top}
.people .av{display:grid;place-items:center;background:var(--red-l);color:var(--red);font-size:40px;font-weight:800}
.people h3{font-size:20px}
.people .role{color:var(--red);font-weight:700;font-size:14px;margin:4px 0 10px}
.people p{color:var(--muted);font-size:15px}
.chips2{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.chips2 span{background:#fff;border-radius:12px;padding:10px 16px;font-weight:600;font-size:15px;box-shadow:var(--sh-1)}
.alert-note{background:#fff7e6;border-radius:14px;padding:16px 18px;color:#7a4b00;box-shadow:inset 3px 0 0 #f0a020;font-size:15px}
.steps3.four{grid-template-columns:repeat(4,1fr)}
.steps3 p{color:var(--muted);font-size:15px}
.steps3 p strong{color:var(--navy);font-size:16.5px}
.subnav{background:#fff;border-bottom:1px solid #eef0f3}
.subnav .wrap{display:flex;gap:8px;overflow-x:auto;padding-top:12px;padding-bottom:12px;scrollbar-width:none}
.subnav a{flex:0 0 auto;padding:8px 16px;border-radius:999px;font-weight:700;font-size:14.5px;color:var(--muted);background:var(--bg)}
.subnav a:hover{color:var(--navy)}
.subnav a[aria-current]{background:var(--red);color:#fff}
@media (max-width:980px){.steps3.four{grid-template-columns:1fr 1fr}.icards.c3,.icards.c4{grid-template-columns:1fr 1fr}.tline{grid-template-columns:1fr 1fr;row-gap:26px}.tline::before{display:none}.people{grid-template-columns:1fr}}
@media (max-width:640px){.steps3.four{grid-template-columns:1fr}.icards.c2,.icards.c3,.icards.c4{grid-template-columns:1fr}.tline{grid-template-columns:1fr}.people .person{grid-template-columns:1fr}}
"""
