# -*- coding: utf-8 -*-
"""Builds the Praveen Hospitals redesign preview: 8 static pages sharing one header, footer, CSS and JS.

Run:  python3 build.py
Edit page bodies below (or the reusable sections in _parts.json), then rebuild.
Every visible string is bilingual: <span lang="en">…</span><span lang="te">…</span>.
"""
import json, re
from pathlib import Path

HERE = Path(__file__).parent
P = json.loads((HERE / "_parts.json").read_text())
IMG = "https://praveenhospitals.com/img/"
LAT, LON = 16.5077909, 80.6427732


def ic(path, fill=False, size=22):
    a = 'fill="currentColor"' if fill else 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" {a} aria-hidden="true">{path}</svg>'
I_PHONE = '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
I_PIN = '<path d="M12 21s-7-4.4-7-11a7 7 0 0 1 14 0c0 6.6-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>'
I_MAIL = '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'
I_MOBILE = '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>'
I_CAL = '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M12 14v4M10 16h4"/>'
I_WA = '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.1.3.6 1 1.3 1.6.9.8 1.6 1 1.9 1.2.2.1.4.1.5-.1l.7-.9c.2-.2.4-.2.6-.1l1.9.9c.2.1.4.2.5.3 0 .2 0 .8-.3 1.4z"/>'
I_HEART = '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>'
I_PULSE = '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/><path d="M3.5 12h4l2-3 3 6 2-3h6"/>'
I_BRIEF = '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>'
I_BODY = '<circle cx="12" cy="5" r="2.5"/><path d="M12 8v7M8 10h8M9 22l3-7 3 7"/>'
I_TARGET = '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>'
I_EYE = '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'
I_CHECK = '<path d="M20 6 9 17l-5-5"/>'
I_BED = '<path d="M2 18v-8M2 14h20v4M22 18v-4a3 3 0 0 0-3-3h-9v3"/><circle cx="6.5" cy="11.5" r="1.5"/>'
I_ACT = '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'
I_ZAP = '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>'
I_DROP = '<path d="M12 2.7s6 6.4 6 11.3a6 6 0 0 1-12 0c0-4.9 6-11.3 6-11.3z"/>'
I_VESSEL = '<path d="M4 20c4-4 4-12 8-12s4 8 8 12"/><path d="M4 4c3 3 13 3 16 0"/>'
I_STENT = '<rect x="3" y="9" width="18" height="6" rx="3"/><path d="M7 9l3 6M11 9l3 6M15 9l3 6"/>'

def t(en, te):
    return f'<span lang="en">{en}</span><span lang="te">{te}</span>'


# ── review fixes applied to the reusable sections ──
for k in P:
    v = P[k]
    v = v.replace('<span class="ic">♡</span>', '<span class="ic">' + ic(I_HEART) + '</span>')
    v = v.replace('<span class="ic">♥</span>', '<span class="ic">' + ic(I_PULSE) + '</span>')
    v = v.replace('<span class="ic">◆</span>', '<span class="ic">' + ic(I_BRIEF) + '</span>')
    v = v.replace('<span class="ic">✚</span>', '<span class="ic">' + ic(I_BODY) + '</span>')
    v = v.replace('<span class="ic">☎</span>', '<span class="ic">' + ic(I_PHONE, size=20) + '</span>')
    v = v.replace('<span class="ic">⌖</span>', '<span class="ic">' + ic(I_PIN, size=20) + '</span>')
    # Dr. Praveen already has the large portrait; the team row shows the rest of the team
    v = v.replace('<div class="member reveal"><img src="https://praveenhospitals.com/img/doctor_m_praveen.jpg" alt=""><span><b>Dr. M. Praveen</b><small>MD, DM · <span lang="en">Cardiologist</span><span lang="te">కార్డియాలజిస్ట్</span></small></span></div>', '')
    v = v.replace('<div class="team">', '<h3 class="team-h"><span lang="en">Our specialist team</span><span lang="te">మా నిపుణుల బృందం</span></h3><div class="team">')
    v = v.replace('alt=""><span><b>Dr. P. Kamala Smitha', 'alt="Dr. P. Kamala Smitha"><span><b>Dr. P. Kamala Smitha').replace('alt=""><span><b>Dr. P. Vijaya Krishna', 'alt="Dr. P. Vijaya Krishna"><span><b>Dr. P. Vijaya Krishna')
    P[k] = v

TABS = [
    ("index", "Home", "హోమ్"),
    ("about", "About Us", "మా గురించి"),
    ("services", "Services", "సేవలు"),
    ("specialities", "Specialities", "విభాగాలు"),
    ("patient-care", "Patient Care", "పేషెంట్ కేర్"),
    ("empanelments", "Empanelments", "పథకాలు"),
    ("gallery", "Gallery", "గ్యాలరీ"),
    ("contact", "Contact Us", "సంప్రదించండి"),
]

PHONE_SVG = '<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'

def header(active):
    CUR = ' aria-current="page"'
    tabs = "".join(
        f'<li><a href="{k}.html"{CUR if k == active else ""}>{t(en, te)}</a></li>' for k, en, te in TABS
    )
    return f"""<div class="preview"><b>Redesign preview</b> — prepared for Praveen Hospitals. Not the live website.</div>
<div class="ebar"><div class="wrap">
  <span class="pulse"><i></i>{t("24×7 Emergency", "24×7 అత్యవసరం")}</span>
  <div class="ticker" aria-label="Announcements"><div class="tk-track"><span>{t("For appointments call 0866-2444440", "అపాయింట్‌మెంట్ల కోసం 0866-2444440కి కాల్ చేయండి")} <b>•</b> {t("Health checkup packages available: General, Master, Executive, Total Body", "హెల్త్ చెకప్ ప్యాకేజీలు అందుబాటులో: జనరల్, మాస్టర్, ఎగ్జిక్యూటివ్, టోటల్ బాడీ")} <b>•</b> </span><span aria-hidden="true">{t("For appointments call 0866-2444440", "అపాయింట్‌మెంట్ల కోసం 0866-2444440కి కాల్ చేయండి")} <b>•</b> {t("Health checkup packages available: General, Master, Executive, Total Body", "హెల్త్ చెకప్ ప్యాకేజీలు అందుబాటులో: జనరల్, మాస్టర్, ఎగ్జిక్యూటివ్, టోటల్ బాడీ")} <b>•</b> </span></div></div>
  <span class="ebar-r">
    <a class="hide-s" href="tel:+918662444440">0866-2444440</a>
    <span class="lang" role="group" aria-label="Language"><button data-set="en" aria-pressed="true">English</button><button data-set="te" class="te" aria-pressed="false">తెలుగు</button></span>
  </span>
</div></div>
<header>
  <div class="wrap nav">
    <a class="brand" href="index.html"><img src="{IMG}praveen-hospital-logo.png" alt="Praveen Hospitals"></a>
    <div class="act">
      <a class="btn btn-line" href="tel:+918662444440">{PHONE_SVG}{t("Call", "కాల్")}</a>
      <a class="btn btn-red" href="contact.html#book">{t("Book appointment", "అపాయింట్‌మెంట్")}</a>
    </div>
  </div>
  <nav class="tabs" aria-label="Main"><div class="wrap"><ul>{tabs}</ul></div></nav>
</header>"""

FOOTER = f"""<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <img src="{IMG}praveen-hospital-logo.png" alt="Praveen Hospitals" style="height:44px;background:#fff;border-radius:10px;padding:6px 10px;margin-bottom:14px">
        <p>{t("To reach every family in Andhra Pradesh and Telangana with quality care, health education and early diagnosis.", "ఆంధ్రప్రదేశ్, తెలంగాణలోని ప్రతి కుటుంబానికి నాణ్యమైన వైద్యం, ఆరోగ్య అవగాహన, ముందస్తు నిర్ధారణ అందించడమే మా లక్ష్యం.")}</p>
        <p style="margin-top:12px">#32-9-18, Moghalrajapuram, Madhugarden Center, No.5 Bus Route, Vijayawada – 520 010</p>
      </div>
      <div><h4>{t("Quick links", "త్వరిత లింకులు")}</h4><ul>{"".join(f'<li><a href="{k}.html">{t(en, te)}</a></li>' for k, en, te in TABS[1:])}</ul></div>
      <div><h4>{t("24×7 Emergency", "24×7 అత్యవసరం")}</h4><ul><li><a href="tel:+918662444440" style="color:#fff;font-size:20px;font-weight:800">0866-2444440</a></li><li><a href="tel:+918662444414">0866-2444414</a></li><li><a href="tel:+919948878877">+91 99488 78877</a></li><li><a href="mailto:praveencardiaccentre@gmail.com">praveencardiaccentre@gmail.com</a></li></ul></div>
    </div>
    <div class="legal"><span>© 2026 Praveen Hospitals, Vijayawada</span><span>{t("Redesign preview — not the live website", "రీడిజైన్ ప్రివ్యూ — ఇది అసలు వెబ్‌సైట్ కాదు")}</span></div>
  </div>
</footer>
<nav class="mbar" aria-label="Quick actions">
  <a class="c" href="tel:+918662444440">{ic(I_PHONE, size=20)}<span>{t("Call", "కాల్")}</span></a>
  <a class="w" href="contact.html#book">{ic(I_WA, fill=True, size=20)}<span>WhatsApp</span></a>
  <a class="b" href="contact.html#book">{ic(I_CAL, size=20)}<span>{t("Book", "బుక్")}</span></a>
</nav>
<a class="fab-wa" href="contact.html#book" aria-label="Book on WhatsApp">{ic(I_WA, fill=True, size=28)}<span>{t("Book on WhatsApp", "WhatsAppలో బుక్")}</span></a>
<button class="to-top" aria-label="Back to top">↑</button>
{P["modal"]}"""

def page_hero(eyebrow, title, sub, img="slider/banner_3.jpg"):
    return f"""<section class="phero" style="--bg:url('{IMG}{img}')"><div class="wrap">
  <div class="crumb"><a href="index.html">{t("Home", "హోమ్")}</a> / {eyebrow}</div>
  <h1>{title}</h1><p>{sub}</p>
</div></section>"""

MAP = f"""<div class="map"><iframe title="Map: Praveen Hospitals" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox={LON-0.006},{LAT-0.004},{LON+0.006},{LAT+0.004}&layer=mapnik&marker={LAT},{LON}"></iframe>
<a class="maplink" href="https://www.google.com/maps/search/?api=1&query=Praveen+Hospitals+Moghalrajapuram+Vijayawada" target="_blank" rel="noopener">{t("Open in Google Maps ↗", "Google Mapsలో తెరవండి ↗")}</a></div>"""

VIDEO = f"""<div class="video-card">
  <video controls preload="metadata" playsinline poster="{IMG}gallery/gallery_5.jpg"><source src="https://praveenhospitals.com/videos/vid1.mp4" type="video/mp4"></video>
  <div class="vc-cap"><b>{t("Open heart surgery at Praveen Hospitals", "ప్రవీణ్ హాస్పిటల్స్‌లో ఓపెన్ హార్ట్ సర్జరీ")}</b><small>{t("Contains surgical footage", "శస్త్రచికిత్స దృశ్యాలు ఉన్నాయి")}</small></div>
</div>"""

# The contact page form section, with the blocked Google iframe swapped for the OSM map
BOOK = re.sub(r'<div class="map">.*?</div>', MAP, P["book"], flags=re.S)

PAGES = {}

# ── HOME — same order as the original homepage: slider → camps → about → specialities → statistics → core services ──
SLIDES = [
    ("slider/banner_5.jpg", t("Welcome to", "స్వాగతం"), t("Praveen Hospitals", "ప్రవీణ్ హాస్పిటల్స్"),
     t("Effective, affordable, dedicated and easily accessible quality health care to the needy — at any hour.", "అవసరమైన వారికి ఏ సమయంలోనైనా ప్రభావవంతమైన, అందుబాటు ధరలో, అంకితభావంతో కూడిన నాణ్యమైన వైద్యం."),
     f'<a class="btn btn-red" href="contact.html#book">{t("Book appointment", "అపాయింట్‌మెంట్ బుక్ చేయండి")} →</a><a class="btn btn-white" href="tel:+918662444440">{PHONE_SVG}{t("Emergency 0866-2444440", "అత్యవసరం 0866-2444440")}</a>'),
    ("slider/banner_3.jpg", t("100-bed hospital", "100 పడకల ఆసుపత్రి"), t("Latest ICU. Modular operating theatres.", "ఆధునిక ICU. మాడ్యులర్ ఆపరేషన్ థియేటర్లు."),
     t("Cath-lab, diagnostics and theatres in one building — so treatment starts faster.", "క్యాథ్ ల్యాబ్, డయాగ్నొస్టిక్స్, థియేటర్లు — అన్నీ ఒకే భవనంలో, చికిత్స త్వరగా మొదలవుతుంది."),
     f'<a class="btn btn-red" href="services.html">{t("Our services", "మా సేవలు")} →</a>'),
    ("slider/banner_2.jpg", t("Heart care since 2007", "2007 నుండి గుండె వైద్యం"), t("11,500+ angiograms. 99.6% stent success.", "11,500+ యాంజియోగ్రామ్‌లు. 99.6% స్టెంట్ విజయం."),
     t("4,000 stents and 2,000 bypass surgeries in 14 years, as reported by the hospital.", "14 సంవత్సరాలలో 4,000 స్టెంట్లు, 2,000 బైపాస్ సర్జరీలు — ఆసుపత్రి నివేదిక ప్రకారం."),
     f'<a class="btn btn-red" href="specialities.html">{t("Our specialities", "మా విభాగాలు")} →</a>'),
    ("slider/banner_1.jpg", t("Cashless treatment", "క్యాష్‌లెస్ చికిత్స"), t("Aarogyasri, EHS, ECHS &amp; all TPA insurance.", "ఆరోగ్యశ్రీ, EHS, ECHS &amp; అన్ని TPA ఇన్సూరెన్స్‌లు."),
     t("Treatment at CGHS rates under 12 government schemes and insurers.", "12 ప్రభుత్వ పథకాలు, ఇన్సూరెన్స్‌లతో CGHS ధరలకే చికిత్స."),
     f'<a class="btn btn-red" href="empanelments.html">{t("Check your scheme", "మీ పథకం చూడండి")} →</a>'),
    ("slider/banner_4.jpg", t("Patient care", "పేషెంట్ కేర్"), t("Recovery that continues at home.", "ఇంటి వరకూ కొనసాగే సంరక్షణ."),
     t("Home-care plans for elderly, chronically ill and post-surgery patients.", "వృద్ధులు, దీర్ఘకాల వ్యాధిగ్రస్తులు, శస్త్రచికిత్స తర్వాత కోలుకునే వారికి ఇంటి సంరక్షణ ప్రణాళికలు."),
     f'<a class="btn btn-red" href="patient-care.html">{t("Patient care", "పేషెంట్ కేర్")} →</a>'),
]
CURT = ' aria-current="true"'
SLIDER = '<section class="hero2" aria-roledescription="carousel" aria-label="Highlights"><div class="slides">' + "".join(
    f'<div class="slide{" on" if i == 0 else ""}" role="group" aria-roledescription="slide" aria-label="{i+1} of {len(SLIDES)}" style="--img:url(\'{IMG}{img}\')">'
    f'<div class="wrap"><div class="cap"><div class="eyebrow">{eb}</div>{"<h1>" if i == 0 else "<h2>"}{title}{"</h1>" if i == 0 else "</h2>"}<p>{sub}</p><div class="ctas">{cta}</div></div></div></div>'
    for i, (img, eb, title, sub, cta) in enumerate(SLIDES)
) + '</div><div class="wrap s-ctrl"><button class="s-btn s-prev" aria-label="Previous slide">‹</button><div class="dots">' + "".join(
    f'<button aria-label="Go to slide {i+1}"{CURT if i == 0 else ""}></button>' for i in range(len(SLIDES))
) + '</div><button class="s-btn s-next" aria-label="Next slide">›</button></div></section>'

CAMP_STRIP = f"""<div class="wrap camp-strip">
  <div class="cs reveal"><div class="cal" id="cal-j"><div class="m">—</div><div class="d">—</div><div class="w">—</div></div>
    <div><b>{t("Health camp · Jaggaiahpet", "ఆరోగ్య శిబిరం · జగ్గయ్యపేట")}</b><span>{t("Every Wednesday · 4 PM – 8 PM", "ప్రతి బుధవారం · సా. 4 – రా. 8")}</span><em class="next" id="next-j"></em></div></div>
  <div class="cs reveal"><div class="cal" id="cal-k"><div class="m">—</div><div class="d">—</div><div class="w">—</div></div>
    <div><b>{t("Health camp · Kodad", "ఆరోగ్య శిబిరం · కోదాడ")}</b><span>{t("2nd &amp; 4th Sunday · 11 AM – 2 PM", "2వ &amp; 4వ ఆదివారం · ఉ. 11 – మ. 2")}</span><em class="next" id="next-k"></em></div></div>
  <a class="cs cs-red reveal" href="tel:+918662444440"><span class="cs-ic">{ic(I_PHONE, size=26)}</span>
    <div><b>{t("24×7 Emergency", "24×7 అత్యవసరం")}</b><span class="big">0866-2444440</span></div></a>
</div>"""

HOME_ABOUT = f"""<section><div class="wrap two-col">
  <div class="portrait-card reveal">
    <img src="{IMG}doctor_m_praveen.jpg" alt="Dr. M. Praveen, Cardiologist">
    <div class="pc-badge"><b>2007</b><span>{t("Founded", "స్థాపన")}</span></div>
    <div class="pc-name"><b>Dr. M. Praveen</b><small>MD, DM (Cardiology)</small></div>
  </div>
  <div class="reveal"><div class="eyebrow">{t("About Praveen Hospitals", "ప్రవీణ్ హాస్పిటల్స్ గురించి")}</div>
    <h2 class="h2">{t("A cardiac centre built on one doctor's promise.", "ఒక వైద్యుని సంకల్పంతో నిర్మించిన గుండె వైద్య కేంద్రం.")}</h2>
    <p class="lede">{t("Dr. Praveen Maddirala, an established cardiologist, founded the Praveen Cardiac Centre in Vijayawada in 2007. Today it is a 100-bed hospital with cardiology, neurology, critical care, radiology and anaesthesiology — all under one roof.", "ప్రముఖ కార్డియాలజిస్ట్ డా. ప్రవీణ్ మద్దిరాల 2007లో విజయవాడలో ప్రవీణ్ కార్డియాక్ సెంటర్‌ను స్థాపించారు. నేడు ఇది కార్డియాలజీ, న్యూరాలజీ, క్రిటికల్ కేర్, రేడియాలజీ, అనస్థీషియాలజీ సేవలతో 100 పడకల ఆసుపత్రి — అన్నీ ఒకే చోట.")}</p>
    <a class="btn btn-red" href="about.html">{t("Read more", "మరింత చదవండి")} →</a></div>
</div></section>"""

SPEC_TILES = [("cardiology", "Cardiology", "కార్డియాలజీ"), ("cardiothoracic", "Cardiothoracic Surgery", "కార్డియోథొరాసిక్ సర్జరీ"),
              ("neurology", "Neurology", "న్యూరాలజీ"), ("radiology", "Radiology", "రేడియాలజీ"), ("general_medicine", "General Medicine", "జనరల్ మెడిసిన్")]
HOME_SPECS = f"""<section class="alt"><div class="wrap">
  <div class="head c reveal"><div class="eyebrow">{t("Our specialities", "మా విభాగాలు")}</div><h2>{t("Heart, brain &amp; diagnostic care.", "గుండె, మెదడు &amp; డయాగ్నొస్టిక్ వైద్యం.")}</h2></div>
  <div class="tiles">{"".join(f'<a class="tile reveal" href="specialities.html"><img src="{IMG}speciality/{f}.jpg" alt="" loading="lazy"><span>{t(en, te)}<i>→</i></span></a>' for f, en, te in SPEC_TILES)}</div>
</div></section>"""

STATS = [
    ("monthly_in_patients", "150–200", None, "Monthly in-patients", "నెలవారీ ఇన్-పేషెంట్లు"),
    ("angiographies", "100–120", None, "Angiographies every month", "ప్రతి నెలా యాంజియోగ్రఫీలు"),
    ("cardiac_peripheral_intervention", "3,800", 3800, "Cardiac &amp; peripheral interventions", "కార్డియాక్ &amp; పెరిఫెరల్ ఇంటర్వెన్షన్లు"),
    ("open_heart_surgery", "2,000", 2000, "Open heart surgeries", "ఓపెన్ హార్ట్ సర్జరీలు"),
    ("permanent_pacemaker", "180", 180, "Permanent pacemakers", "పర్మనెంట్ పేస్‌మేకర్లు"),
    ("peripheral_vascular_surgery", "3,500", 3500, "Peripheral vascular surgeries", "పెరిఫెరల్ వాస్కులర్ సర్జరీలు"),
    ("av_fistula", "200", 200, "AV fistulas for hemodialysis", "హీమోడయాలసిస్ కోసం AV ఫిస్టులా"),
    ("cardiac_electrophysiology", "250", 250, "Cardiac EP &amp; RF ablation", "కార్డియాక్ EP &amp; RF అబ్లేషన్"),
]
STAT_ICON = {"monthly_in_patients": I_BED, "angiographies": I_ACT, "cardiac_peripheral_intervention": I_STENT, "open_heart_surgery": I_HEART,
             "permanent_pacemaker": I_ZAP, "peripheral_vascular_surgery": I_VESSEL, "av_fistula": I_DROP, "cardiac_electrophysiology": I_PULSE}
def stat_card(f, shown, n, en, te):
    num = f'<b class="count" data-to="{n}">{shown}</b>' if n else f'<b>{shown}</b>'
    return f'<div class="stat reveal"><span class="st-ic">{ic(STAT_ICON[f], size=26)}</span>{num}<span>{t(en, te)}</span></div>'
STAT_CARDS = "".join(stat_card(*row) for row in STATS)
HOME_STATS = f"""<section><div class="wrap">
  <div class="head c reveal"><div class="eyebrow">{t("Hospital statistics", "ఆసుపత్రి గణాంకాలు")}</div><h2>{t("Experience you can count on.", "లెక్కించదగిన అనుభవం.")}</h2></div>
  <div class="stats">{STAT_CARDS}</div>
  <p class="note" style="text-align:center">{t("Figures as reported by Praveen Hospitals.", "ప్రవీణ్ హాస్పిటల్స్ నివేదించిన గణాంకాలు.")}</p>
</div></section>"""

HOME_CORE = f"""<section class="alt"><div class="wrap two-col">
  <div class="reveal"><div class="eyebrow">{t("Core services", "ప్రధాన సేవలు")}</div>
    <h2 class="h2">{t("Cardiology services", "కార్డియాలజీ సేవలు")}</h2>
    <p class="lede">{t("From a first ECG to bypass and valve surgery, our cardiologists cover the whole journey — PTCA, pacemakers, EP studies and more.", "మొదటి ECG నుండి బైపాస్, వాల్వ్ సర్జరీ వరకు — PTCA, పేస్‌మేకర్లు, EP స్టడీలు మరియు మరెన్నో — మా కార్డియాలజిస్టులు అన్నీ చూసుకుంటారు.")}</p>
    <a class="btn btn-red" href="services.html">{t("Read more", "మరింత చదవండి")} →</a></div>
  <div class="float-img reveal"><img src="{IMG}cardiology_services.png" alt="" loading="lazy"></div>
</div></section>"""

CTA_BAND = f"""<section class="tight"><div class="wrap"><div class="cta-band reveal">
  <div><h2>{t("Need a heart specialist?", "గుండె నిపుణుడు కావాలా?")}</h2><p>{t("Book in a minute on WhatsApp, or call us any time — day or night.", "WhatsAppలో నిమిషంలో బుక్ చేయండి, లేదా పగలు రాత్రి ఎప్పుడైనా కాల్ చేయండి.")}</p></div>
  <div class="cta-acts"><a class="btn btn-white" href="contact.html#book">{t("Book appointment", "అపాయింట్‌మెంట్ బుక్ చేయండి")} →</a><a class="btn btn-ghost-w" href="tel:+918662444440">{PHONE_SVG}0866-2444440</a></div>
</div></div></section>"""

PAGES["index"] = ("Home", SLIDER + CAMP_STRIP + HOME_ABOUT + HOME_SPECS + HOME_STATS + HOME_CORE + CTA_BAND)

# ── ABOUT ──
CENTRES = [
    (t("Main hospital", "ప్రధాన ఆసుపత్రి"), "Moghalrajapuram, Vijayawada", t("100 beds · ICU · cath-lab · modular OT", "100 పడకలు · ICU · క్యాథ్ ల్యాబ్ · మాడ్యులర్ OT")),
    (t("Hyderabad Road centre", "హైదరాబాద్ రోడ్ కేంద్రం"), "Vijayawada", t("Consultations with Dr. Praveen", "డా. ప్రవీణ్ సంప్రదింపులు")),
    (t("Huzurnagar Road centre", "హుజూర్‌నగర్ రోడ్ కేంద్రం"), "Vijayawada", t("Consultations with Dr. Praveen", "డా. ప్రవీణ్ సంప్రదింపులు")),
]
PAGES["about"] = ("About Us", page_hero(t("About Us", "మా గురించి"), t("Caring for hearts since 2007.", "2007 నుండి గుండెలకు ఆదరణ."),
    t("From a cardiac centre to a 100-bed hospital for cardiology, cardiothoracic surgery, neurology and neurosurgery.", "ఒక కార్డియాక్ సెంటర్ నుండి కార్డియాలజీ, కార్డియోథొరాసిక్ సర్జరీ, న్యూరాలజీ, న్యూరోసర్జరీ కోసం 100 పడకల ఆసుపత్రిగా."), "slider/banner_5.jpg") + f"""
<section><div class="wrap two-col">
  <div class="reveal"><div class="eyebrow">{t("Who we are", "మేము ఎవరం")}</div>
    <h2 class="h2">{t("Everything under one roof.", "అన్నీ ఒకే చోట.")}</h2>
    <p class="lede">{t("We provide consultation, diagnosis and treatment in Cardiology, Cardiothoracic Surgery, Neurology and Neuro Surgery at CGHS rates.", "కార్డియాలజీ, కార్డియోథొరాసిక్ సర్జరీ, న్యూరాలజీ, న్యూరోసర్జరీలో సంప్రదింపులు, నిర్ధారణ, చికిత్స — CGHS ధరలకే.")}</p>
    <p class="muted-p">{t("Diagnostics, operating theatres and a cath-lab sit in the same building, giving patients a wide range of care without moving between centres. Dr. Praveen regularly attends national and state conferences to stay at the forefront of cardiac care.", "డయాగ్నొస్టిక్స్, ఆపరేషన్ థియేటర్లు, క్యాథ్ ల్యాబ్ ఒకే భవనంలో ఉండటం వల్ల పేషెంట్లు వేర్వేరు కేంద్రాలకు తిరగాల్సిన అవసరం లేదు. తాజా గుండె వైద్య పద్ధతుల కోసం డా. ప్రవీణ్ జాతీయ, రాష్ట్ర స్థాయి సదస్సులలో క్రమం తప్పకుండా పాల్గొంటారు.")}</p></div>
  <div class="photo reveal"><img src="{IMG}slider/banner_3.jpg" alt="Intensive care unit at Praveen Hospitals"></div>
</div></section>
<section class="alt"><div class="wrap mv">
  <div class="mvcard reveal"><span class="ic">{ic(I_TARGET)}</span><div class="eyebrow">{t("Mission", "లక్ష్యం")}</div><p>{t("To provide effective, affordable, dedicated and easily accessible quality health care to the needy at any hour.", "అవసరమైన వారికి ఏ సమయంలోనైనా ప్రభావవంతమైన, అందుబాటు ధరలో, అంకితభావంతో కూడిన నాణ్యమైన వైద్యం అందించడం.")}</p></div>
  <div class="mvcard reveal"><span class="ic">{ic(I_EYE)}</span><div class="eyebrow">{t("Vision", "దృష్టి")}</div><p>{t("To reach the entire states of Andhra Pradesh and Telangana, with health education for the public and a stress on preventive care and early diagnosis.", "ఆంధ్రప్రదేశ్, తెలంగాణ రాష్ట్రాలంతటా చేరుకోవడం — ప్రజలకు ఆరోగ్య అవగాహన, ముందస్తు జాగ్రత్త మరియు త్వరిత నిర్ధారణపై దృష్టితో.")}</p></div>
</div></section>
""" + P["doctors"].replace('<section id="doctors" class="alt">', '<section id="doctors">') + f"""
<section class="alt"><div class="wrap">
  <div class="head c reveal"><div class="eyebrow">{t("Where we are", "మా కేంద్రాలు")}</div><h2>{t("Three centres, one standard of care.", "మూడు కేంద్రాలు, ఒకే నాణ్యత.")}</h2></div>
  <div class="centres">{"".join(f'<div class="centre reveal"><span class="ic">{ic(I_PIN)}</span><b>{n}</b><small>{loc}</small><p>{d}</p></div>' for n, loc, d in CENTRES)}</div>
</div></section>""")

# ── SERVICES ──
PAGES["services"] = ("Services", page_hero(t("Services", "సేవలు"), t("100-bed hospital. Latest ICU. Modular OT.", "100 పడకల ఆసుపత్రి. ఆధునిక ICU. మాడ్యులర్ OT."),
    t("In 14 years: 11,500+ angiograms, 4,000 stents with a 99.6% success rate and 2,000 bypass surgeries with a 98% success rate.", "14 సంవత్సరాలలో: 11,500కు పైగా యాంజియోగ్రామ్‌లు, 99.6% విజయ శాతంతో 4,000 స్టెంట్లు, 98% విజయ శాతంతో 2,000 బైపాస్ సర్జరీలు."), "slider/banner_3.jpg") + f"""
<section><div class="wrap svc">
  <div class="svc-card reveal"><img src="{IMG}services/cardiology.png" alt="" loading="lazy">
    <h3>{t("Cardiology services", "కార్డియాలజీ సేవలు")}</h3>
    <ul class="ticks"><li>Bypass &amp; Valve Surgeries</li><li>PTCA (Percutaneous Transluminal Coronary Angioplasty)</li><li>Pacemaker &amp; EP Study</li><li>ECG (Electrocardiogram)</li><li>2D Echo</li><li>TMT (Treadmill Test)</li><li>Ambulatory BP monitoring</li><li>Holter analysis</li></ul></div>
  <div class="svc-card reveal"><img src="{IMG}services/radiology.png" alt="" loading="lazy">
    <h3>{t("Radiology services", "రేడియాలజీ సేవలు")}</h3>
    <ul class="ticks"><li>Ultrasound scan</li><li>Doppler</li><li>Mammography (breast cancer screening)</li></ul>
    <div class="callout">{t("Not sure which test you need? Send us your doctor's prescription on WhatsApp.", "ఏ పరీక్ష అవసరమో తెలియదా? మీ డాక్టర్ ప్రిస్క్రిప్షన్‌ను WhatsAppలో పంపండి.")}</div></div>
</div></section>""" + P["checkups"].replace('<section id="checkups">', '<section id="checkups" class="alt">'))

# ── SPECIALITIES ──
SPEC_BODY = re.sub(r'<div class="head reveal">.*?</div>\s*<div class="spec-grid">', '<div class="spec-grid">', P["specialities"], count=1, flags=re.S)
PAGES["specialities"] = ("Specialities", page_hero(t("Specialities", "విభాగాలు"), t("Five specialities. One team.", "ఐదు విభాగాలు. ఒకే బృందం."),
    t("Diagnostics, operating theatres and a cath-lab in one building — so treatment starts faster.", "డయాగ్నొస్టిక్స్, ఆపరేషన్ థియేటర్లు, క్యాథ్ ల్యాబ్ — అన్నీ ఒకే భవనంలో, చికిత్స త్వరగా మొదలవుతుంది."), "banners/speciality.jpeg")
    + SPEC_BODY)

# ── PATIENT CARE ──
PAGES["patient-care"] = ("Patient Care", page_hero(t("Patient Care", "పేషెంట్ కేర్"), t("Care that continues at home.", "ఇంటి వరకూ కొనసాగే సంరక్షణ."),
    t("Personalised attention from trained, qualified caregivers — in hospital and at home.", "శిక్షణ పొందిన సిబ్బందితో వ్యక్తిగత శ్రద్ధ — ఆసుపత్రిలోనూ, ఇంటి వద్దనూ."), "slider/banner_4.jpg") + f"""
<section><div class="wrap two-col">
  <div class="reveal"><div class="eyebrow">{t("Home care", "ఇంటి వద్ద సంరక్షణ")}</div>
    <h2 class="h2">{t("Plans built around your family.", "మీ కుటుంబానికి తగిన ప్రణాళికలు.")}</h2>
    <p class="lede">{t("Customisable, plan-based programmes bring family members and caregivers together — a practical option for long-term illness and disease management.", "కుటుంబ సభ్యులు, సంరక్షకులు కలిసి పనిచేసే, అవసరానికి తగ్గట్టు మార్చుకోగల ప్రణాళికలు — దీర్ఘకాల వ్యాధుల నిర్వహణకు ఆచరణీయమైన మార్గం.")}</p>
    <ul class="ticks"><li>{t("Elderly care", "వృద్ధుల సంరక్షణ")}</li><li>{t("Chronic illness management", "దీర్ఘకాల వ్యాధుల నిర్వహణ")}</li><li>{t("Post-surgery recovery", "శస్త్రచికిత్స తర్వాత కోలుకోవడం")}</li></ul>
    <a class="btn btn-red" href="contact.html#book">{t("Ask about home care", "ఇంటి సంరక్షణ గురించి అడగండి")} →</a></div>
  <div class="float-img reveal"><img src="{IMG}care.png" alt="" loading="lazy"></div>
</div></section>
<section class="alt"><div class="wrap"><div class="head c reveal"><div class="eyebrow">{t("Patient rights", "పేషెంట్ హక్కులు")}</div><h2>{t("As our patient, you can expect:", "మా పేషెంట్‌గా మీరు ఆశించవచ్చు:")}</h2></div>
<div class="rights">{"".join(f'<div class="right reveal"><span class="ok">{ic(I_CHECK, size=18)}</span><div><b>{h}</b><p>{d}</p></div></div>' for h, d in [
 (t("Informed consent", "సమాచారంతో కూడిన అంగీకారం"), t("Except in emergencies, a clear description of any procedure, its risks, the alternatives and who will perform it — before you decide.", "అత్యవసర పరిస్థితులు తప్ప, ఏ చికిత్స అయినా — దాని ప్రమాదాలు, ప్రత్యామ్నాయాలు, ఎవరు చేస్తారు — మీరు నిర్ణయించే ముందే వివరిస్తాం.")),
 (t("Clear explanations", "స్పష్టమైన వివరణ"), t("Your diagnosis, the benefits and risks of each treatment and the expected outcome, in words you understand.", "మీ వ్యాధి నిర్ధారణ, ప్రతి చికిత్స ప్రయోజనాలు, ప్రమాదాలు, ఆశించిన ఫలితం — మీకు అర్థమయ్యే మాటల్లో.")),
 (t("Privacy &amp; confidentiality", "గోప్యత"), t("Discussions, examinations and records stay confidential. Records are shared only with your written permission.", "చర్చలు, పరీక్షలు, రికార్డులు గోప్యంగా ఉంటాయి. మీ లిఖిత అనుమతితోనే రికార్డులు ఇతరులకు ఇస్తాం.")),
 (t("Respect &amp; dignity", "గౌరవం"), t("Compassionate care in a safe, clean environment — regardless of age, gender, origin, religion or disability.", "వయస్సు, లింగం, మతం, వైకల్యంతో సంబంధం లేకుండా — సురక్షితమైన, పరిశుభ్రమైన వాతావరణంలో ఆదరణతో కూడిన వైద్యం.")),
 (t("Knowing who is present", "ఎవరు ఉన్నారో తెలుసుకోవడం"), t("You may ask why any person is present during your care.", "మీ చికిత్స సమయంలో ఎవరైనా ఎందుకు ఉన్నారో అడిగే హక్కు మీకు ఉంది.")),
 (t("Safety", "భద్రత"), t("Protection from physical abuse and neglect.", "శారీరక వేధింపులు, నిర్లక్ష్యం నుండి రక్షణ.")),
])}</div></div></section>""")

# ── EMPANELMENTS ──
SCHEMES = [
    ("Dr YSR Aarogyasri", "Dr YSR Healthcare Trust", "డా. వైఎస్ఆర్ ఆరోగ్యశ్రీ"),
    ("EHS", "AP State Govt. Employee Health Scheme", "ఏపీ ప్రభుత్వ ఉద్యోగుల ఆరోగ్య పథకం"),
    ("ECHS", "Ex-Servicemen Contributory Health Scheme", "మాజీ సైనికుల ఆరోగ్య పథకం"),
    ("Arogya Bhadratha", "Police Department", "పోలీస్ శాఖ"),
    ("Aarogya Sahayatha", "Prohibition &amp; Excise Department", "ప్రొహిబిషన్ &amp; ఎక్సైజ్ శాఖ"),
    ("APSRTC", "Road Transport Corporation", "ఆర్టీసీ ఉద్యోగులు"),
    ("Railways", "Indian Railways", "భారతీయ రైల్వే"),
    ("BSNL", "BSNL employees", "బీఎస్ఎన్ఎల్ ఉద్యోగులు"),
    ("SBI", "State Bank of India", "స్టేట్ బ్యాంక్ ఆఫ్ ఇండియా"),
    ("APTRANSCO", "AP Transmission Corporation", "ఏపీ ట్రాన్స్‌కో"),
    ("APGENCO", "AP Power Generation Corporation", "ఏపీ జెన్కో"),
    ("All TPA insurance", "Private health insurance via TPAs", "అన్ని ప్రైవేట్ హెల్త్ ఇన్సూరెన్స్‌లు"),
]
PAGES["empanelments"] = ("Empanelments", page_hero(t("Empanelments", "పథకాలు"), t("Your scheme is welcome here.", "మీ పథకం ఇక్కడ వర్తిస్తుంది."),
    t("Treatment at CGHS rates, with cashless care under 12 government schemes and insurers.", "CGHS ధరలకే చికిత్స — 12 ప్రభుత్వ పథకాలు, ఇన్సూరెన్స్‌లతో క్యాష్‌లెస్ సేవలు."), "slider/banner_1.jpg") + f"""
<section><div class="wrap">
  <div class="schemes">{"".join(f'<div class="scheme reveal"><span class="ok">{ic(I_CHECK, size=18)}</span><span><b>{n}</b><small>{t(en, te)}</small></span></div>' for n, en, te in SCHEMES)}</div>
</div></section>
<section class="alt"><div class="wrap">
  <div class="head c reveal"><div class="eyebrow">{t("How cashless works", "క్యాష్‌లెస్ ఎలా పనిచేస్తుంది")}</div><h2>{t("Three simple steps.", "మూడు సులభమైన దశలు.")}</h2></div>
  <div class="steps3">
    <div class="reveal"><b>1</b><span>{t("Bring your scheme card or insurance policy and photo ID.", "మీ పథకం కార్డు లేదా ఇన్సూరెన్స్ పాలసీ, ఫోటో ID తీసుకురండి.")}</span></div>
    <div class="reveal"><b>2</b><span>{t("Our desk checks your eligibility and starts pre-authorisation.", "మా సిబ్బంది అర్హతను పరిశీలించి ముందస్తు అనుమతి ప్రక్రియ ప్రారంభిస్తారు.")}</span></div>
    <div class="reveal"><b>3</b><span>{t("Get treated — we handle the paperwork with the scheme.", "చికిత్స పొందండి — పథకం పత్రాల పని మేము చూసుకుంటాం.")}</span></div>
  </div>
  <p class="note" style="text-align:center">{t("Coverage depends on your scheme's rules. Call 0866-2444440 to confirm before admission.", "కవరేజ్ మీ పథకం నియమాలపై ఆధారపడి ఉంటుంది. చేరే ముందు 0866-2444440కి కాల్ చేసి నిర్ధారించుకోండి.")}</p>
</div></section>""")

# ── GALLERY ──
GALLERY = ["slider/banner_3.jpg", "gallery/gallery_1.jpg", "gallery/gallery_2.jpg", "gallery/gallery_3.jpg", "gallery/gallery_4.jpg",
           "gallery/gallery_5.jpg", "gallery/gallery_6.jpg", "gallery/gallery_7.jpg", "slider/banner_4.jpg", "slider/banner_5.jpg"]
PAGES["gallery"] = ("Gallery", page_hero(t("Gallery", "గ్యాలరీ"), t("Inside Praveen Hospitals.", "ప్రవీణ్ హాస్పిటల్స్ లోపల."),
    t("Our ICU, operating theatres, cath-lab and wards.", "మా ICU, ఆపరేషన్ థియేటర్లు, క్యాథ్ ల్యాబ్, వార్డులు."), "gallery/gallery_4.jpg") + f"""
<section><div class="wrap two-col">
  <div class="reveal"><div class="eyebrow">{t("Video", "వీడియో")}</div><h2 class="h2">{t("Open heart surgery", "ఓపెన్ హార్ట్ సర్జరీ")}</h2>
    <p class="lede">{t("A look inside one of our modular operating theatres.", "మా మాడ్యులర్ ఆపరేషన్ థియేటర్ లోపలి దృశ్యం.")}</p></div>
  <div class="reveal">{VIDEO}</div>
</div></section>
<section class="alt"><div class="wrap">
  <div class="head c reveal"><div class="eyebrow">{t("Photos", "ఫోటోలు")}</div><h2>{t("Our facilities", "మా సదుపాయాలు")}</h2><p>{t("Tap any photo to enlarge.", "పెద్దగా చూడటానికి ఫోటోపై నొక్కండి.")}</p></div>
  <div class="pgrid">{"".join(f'<button class="ph reveal" data-full="{IMG}{f}"><img src="{IMG}{f}" alt="Praveen Hospitals photo {i+1}" loading="lazy"></button>' for i, f in enumerate(GALLERY))}</div>
</div></section>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo"><button class="lb-x" aria-label="Close">×</button><img alt=""></div>""")

# ── CONTACT ── (phone numbers live in the cards; the booking section keeps only address + map)
BOOK = re.sub(r'<div class="card"><span class="ic">.*?</span></div>\s*', '', BOOK, count=1, flags=re.S)
PAGES["contact"] = ("Contact Us", page_hero(t("Contact Us", "సంప్రదించండి"), t("We're here 24×7.", "24×7 అందుబాటులో ఉన్నాం."),
    t("Call, WhatsApp, or book online — whatever is easiest for you.", "కాల్, WhatsApp లేదా ఆన్‌లైన్ బుకింగ్ — మీకు ఏది సులభమో అది."), "slider/banner_5.jpg") + f"""
<section style="padding-bottom:0"><div class="wrap qc">
  <a class="qcard reveal" href="tel:+918662444440"><span class="ic">{ic(I_PHONE)}</span><b>{t("Emergency &amp; appointments", "అత్యవసరం &amp; అపాయింట్‌మెంట్లు")}</b><span>0866-2444440 · 0866-2444414</span></a>
  <a class="qcard reveal" href="tel:+919948878877"><span class="ic">{ic(I_MOBILE)}</span><b>{t("Mobile", "మొబైల్")}</b><span>+91 99488 78877</span></a>
  <a class="qcard reveal" href="mailto:praveencardiaccentre@gmail.com"><span class="ic">{ic(I_MAIL)}</span><b>{t("Email", "ఈమెయిల్")}</b><span>praveencardiaccentre@gmail.com</span></a>
</div></section>""" + BOOK)


CSS_EXTRA = """
/* ── multi-page additions ─────────────────────────────── */
.nav .act{margin-left:auto}
.tabs{background:#fff;border-top:1px solid var(--line);position:relative}
.tabs .wrap{position:relative}
.tabs ul{display:flex;gap:6px;list-style:none;overflow-x:auto;scrollbar-width:none;padding:8px 0;-webkit-overflow-scrolling:touch;scroll-snap-type:x proximity}
.tabs ul::-webkit-scrollbar{display:none}
.tabs li{scroll-snap-align:start}
.tabs a{display:block;padding:9px 16px;font-weight:700;font-size:14.5px;color:var(--ink);border-radius:999px;white-space:nowrap;transition:background .15s,color .15s}
.tabs a:hover{color:var(--red);background:var(--red-l)}
.tabs a[aria-current]{color:#fff;background:var(--red);box-shadow:0 6px 16px -6px rgba(198,40,40,.6)}
.tabs .wrap::after{content:"";position:absolute;right:0;top:0;bottom:0;width:48px;pointer-events:none;background:linear-gradient(90deg,rgba(255,255,255,0),#fff);opacity:var(--fade,1)}
.burger{display:none}
.drawer{display:none}
.phero{position:relative;color:#fff;background:var(--navy);overflow:hidden}
.phero::before{content:"";position:absolute;inset:0;background:var(--bg) center/cover;opacity:.35}
.phero::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(28,36,48,.95),rgba(28,36,48,.6))}
.phero .wrap{position:relative;z-index:1;padding:64px 24px 70px}
.phero .crumb{font-size:14px;color:#c9ced6;margin-bottom:14px}
.phero .crumb a{color:#fff;text-decoration:underline;text-underline-offset:3px}
.phero h1{color:#fff;font-size:clamp(32px,4.4vw,52px);max-width:20ch}
.phero p{color:#e4e7ec;font-size:18px;max-width:60ch;margin-top:14px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.h2{font-size:clamp(28px,3.4vw,40px);margin:12px 0 14px}
.lede{font-size:18px;color:var(--muted);margin-bottom:20px}
.muted-p{color:var(--muted);margin-bottom:14px}
.photo{border-radius:20px;overflow:hidden;box-shadow:var(--shadow);aspect-ratio:4/3;background:var(--bg)}
.photo img{width:100%;height:100%;object-fit:cover}
.mv{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.mvcard{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:30px}
.mvcard .ic{width:48px;height:48px;border-radius:14px;background:var(--red-l);color:var(--red);display:grid;place-items:center;font-size:22px;margin-bottom:14px}
.mvcard p{font-size:18px;margin-top:10px;color:var(--ink)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.stat{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px;display:flex;flex-direction:column;gap:6px}
.stat img{width:48px;height:48px;object-fit:contain;margin-bottom:6px}
.stat b{font-size:30px;font-weight:800;color:var(--navy);letter-spacing:-.02em;line-height:1}
.stat span{color:var(--muted);font-size:14.5px}
.stats.mini{grid-template-columns:1fr 1fr}
.stats.mini .stat img{display:none}
.svc{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.svc-card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:28px}
.svc-card img{height:72px;width:auto;margin-bottom:14px}
.svc-card h3{font-size:23px;margin-bottom:14px}
.ticks{list-style:none;display:grid;gap:10px;margin:6px 0 22px}
.ticks li{display:flex;gap:10px;align-items:flex-start}
.ticks li::before{content:"✓";flex:0 0 22px;height:22px;border-radius:50%;background:var(--red-l);color:var(--red);font-weight:800;font-size:12px;display:grid;place-items:center;margin-top:2px}
.ticks.big li{font-size:17px;padding:14px 16px;background:#fff;border:1px solid var(--line);border-radius:14px}
.callout{background:var(--green-l);border:1px solid #b8e2da;color:var(--green-d);border-radius:12px;padding:14px 16px;font-size:15px}
.schemes{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:40px}
.scheme{display:flex;gap:14px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.scheme .ok{flex:0 0 36px;height:36px;border-radius:50%;background:var(--green-l);color:var(--green);display:grid;place-items:center;font-weight:800}
.scheme b{display:block}
.scheme small{color:var(--muted)}
.steps3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:14px}
.steps3 div{background:var(--bg);border-radius:14px;padding:20px;display:flex;gap:12px;align-items:flex-start}
.steps3 b{flex:0 0 32px;height:32px;border-radius:50%;background:var(--red);color:#fff;display:grid;place-items:center}
.video-card{border-radius:20px;overflow:hidden;background:#000;box-shadow:var(--shadow)}
.video-card video{display:block;width:100%;aspect-ratio:16/9;background:#000}
.vc-cap{background:#fff;padding:14px 18px;display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap}
.vc-cap small{color:var(--muted)}
.map{position:relative;border-radius:18px;overflow:hidden;border:1px solid var(--line);height:340px;background:var(--bg);box-shadow:var(--shadow)}
.map iframe{width:100%;height:100%;border:0;display:block}
.maplink{position:absolute;right:12px;bottom:12px;background:#fff;color:var(--navy);font-weight:700;font-size:14px;padding:9px 14px;border-radius:10px;box-shadow:var(--shadow)}
.info .map{height:260px}
.pgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.pgrid .ph{border:0;padding:0;cursor:zoom-in;border-radius:14px;overflow:hidden;aspect-ratio:4/3;background:var(--bg)}
.pgrid .ph img{width:100%;height:100%;object-fit:cover;transition:transform .4s}
.pgrid .ph:hover img{transform:scale(1.05)}
.lightbox{position:fixed;inset:0;z-index:70;background:rgba(20,24,30,.92);display:none;place-items:center;padding:24px}
.lightbox.open{display:grid}
.lightbox img{max-width:min(1100px,100%);max-height:85vh;border-radius:12px}
.lb-x{position:absolute;top:16px;right:20px;background:#fff;border:0;width:44px;height:44px;border-radius:50%;font-size:26px;cursor:pointer}
.qc{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.qcard{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px;display:flex;flex-direction:column;gap:6px;transition:border-color .15s,transform .15s}
.qcard:hover{border-color:var(--red);transform:translateY(-2px)}
.qcard .ic{width:44px;height:44px;border-radius:12px;background:var(--red-l);color:var(--red);display:grid;place-items:center;font-size:20px;margin-bottom:6px}
.qcard span:last-child{color:var(--muted)}
.spec.cta{grid-column:1/-1;display:grid;grid-template-columns:1fr auto;column-gap:28px;row-gap:6px;align-items:center;padding:28px 32px}
.spec.cta h3,.spec.cta p{grid-column:1}
.spec.cta .btn{grid-column:2;grid-row:1/3;align-self:center !important}
.team-h{margin:56px 0 0;font-size:20px}
.team-h+.team{margin-top:16px;grid-template-columns:repeat(2,minmax(0,420px))}
.pk .ic svg,.mvcard .ic svg,.qcard .ic svg{width:24px;height:24px}
.scheme .ok svg{width:18px;height:18px}
.mbar a svg{width:20px;height:20px}
@media (max-width:980px){
  .team-h+.team{grid-template-columns:1fr}
  .tabs .wrap{padding:0 12px}
  .drawer.open{display:block;border-top:1px solid var(--line);padding:8px 24px 20px;background:#fff;max-height:calc(100vh - 140px);overflow:auto}
  .drawer ul{list-style:none}
  .drawer a{display:block;padding:13px 4px;border-bottom:1px solid var(--line);font-weight:600}
  .drawer a[aria-current]{color:var(--red)}
  .drawer a.btn{display:flex;margin-top:16px;border:0;justify-content:center;width:100%;color:#fff}
  .two-col,.mv,.svc{grid-template-columns:1fr;gap:28px}
  .stats{grid-template-columns:1fr 1fr}
  .schemes,.steps3,.qc{grid-template-columns:1fr}
  .pgrid{grid-template-columns:1fr 1fr}
}
@media (max-width:640px){ .spec.cta{grid-template-columns:1fr} .spec.cta .btn{grid-column:1;grid-row:auto;justify-self:start} .nav .act{display:flex} .nav .act .btn-red{display:none} .nav .act .btn-line{display:inline-flex;padding:9px 12px} }

/* ══ v2: white surfaces + soft layered shadows ══════════════════════════ */
:root{
  --sh-1:0 1px 2px rgba(28,36,48,.04),0 6px 18px rgba(28,36,48,.07);
  --sh-2:0 2px 6px rgba(28,36,48,.05),0 18px 40px rgba(28,36,48,.10);
  --sh-3:0 4px 10px rgba(28,36,48,.06),0 28px 60px -12px rgba(28,36,48,.22);
  --sh-red:0 10px 28px -8px rgba(198,40,40,.55);
  --bg:#f7f6f4;
}
body{background:#fff}
.alt{background:linear-gradient(180deg,#faf9f7 0%,#f5f3f0 100%)}
section{padding:104px 0}
section.tight{padding:72px 0}

/* buttons */
.btn{border-radius:14px}
.btn-red{background:linear-gradient(180deg,#d63333,#c62828 55%,#b62222);box-shadow:var(--sh-red),inset 0 1px 0 rgba(255,255,255,.25)}
.btn-red:hover{background:linear-gradient(180deg,#c62828,#a81f1f);box-shadow:0 14px 32px -8px rgba(198,40,40,.6)}
.btn-line,.btn-white{background:#fff;color:var(--ink);box-shadow:var(--sh-1)}
.btn-line:hover,.btn-white:hover{box-shadow:var(--sh-2);color:var(--red)}
.btn-ghost-w{background:rgba(255,255,255,.14);color:#fff;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.5)}
.btn-ghost-w:hover{background:rgba(255,255,255,.24)}

/* top bar with scrolling notice (as on the original site) */
.ebar .wrap{gap:18px}
.ebar .pulse{white-space:nowrap}
.ticker{flex:1;overflow:hidden;min-width:0;-webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
.tk-track{display:inline-flex;white-space:nowrap;animation:tick 48s linear infinite}
.tk-track span{padding-right:28px;font-size:13.5px;font-weight:500}
.tk-track b{opacity:.6;margin:0 10px}
.ticker:hover .tk-track{animation-play-state:paused}
@keyframes tick{to{transform:translateX(-50%)}}
.ebar-r{display:flex;align-items:center;gap:16px;white-space:nowrap}

/* header: larger logo, shadow + compact on scroll */
header{background:#fff;border-bottom:0;box-shadow:0 1px 0 var(--line);transition:box-shadow .25s}
header.scrolled{box-shadow:0 8px 30px rgba(28,36,48,.10)}
.nav{height:88px;transition:height .25s}
.brand img{height:60px;transition:height .25s}
header.scrolled .nav{height:70px}
header.scrolled .brand img{height:48px}
.tabs{border-top:1px solid #f0efed}

/* headings: red heartbeat line before eyebrows, accent bar under section titles */
.eyebrow{display:inline-flex;align-items:center;gap:10px}
.eyebrow::before{content:"";width:34px;height:14px;flex:0 0 auto;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 34 14' fill='none' stroke='%23c62828' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M1 7h9l3-5 4 10 3-7 2 2h11'/%3E%3C/svg%3E") center/contain no-repeat}
.head h2::after,.h2::after{content:"";display:block;width:56px;height:4px;border-radius:4px;background:var(--red);margin-top:18px}
.head.c h2::after{margin-left:auto;margin-right:auto}
.cta-band h2::after,.cap h1::after,.cap h2::after,.phero h1::after{display:none}

/* cards: white, no hard borders, soft shadow, lift on hover */
.spec,.pk,.camp,.member,.scheme,.svc-card,.qcard,.mvcard,.stat,.info .card,details,.centre,.right,.steps3 div,.form{border:0 !important;background:#fff;box-shadow:var(--sh-1)}
.spec,.pk,.member,.scheme,.svc-card,.qcard,.mvcard,.stat,.centre,.right,.steps3 div{transition:transform .25s ease,box-shadow .25s ease}
.spec:hover,.pk:hover,.member:hover,.scheme:hover,.svc-card:hover,.qcard:hover,.mvcard:hover,.stat:hover,.centre:hover,.right:hover{transform:translateY(-5px);box-shadow:var(--sh-3)}
.pk.pop{box-shadow:0 0 0 2px var(--red),var(--sh-2)}
.form{box-shadow:var(--sh-2)}
.spec.cta{background:linear-gradient(135deg,#d63333,#a81f1f);box-shadow:var(--sh-red)}
.photo,.video-card,.map{box-shadow:var(--sh-2);border:0}

/* page headers: photo with a white wash over it */
.phero{background:#fff;color:var(--ink);border-bottom:1px solid #f0efed}
.phero::before{left:35%;opacity:1;background:var(--bg) center/cover}
.phero::after{background:linear-gradient(90deg,#fff 0%,#fff 34%,rgba(255,255,255,.88) 46%,rgba(255,255,255,.25) 72%,rgba(255,255,255,0) 100%)}
.phero .wrap{padding:76px 24px 82px}
.phero .crumb{color:var(--muted)}
.phero .crumb a{color:var(--red);text-decoration:none;font-weight:700}
.phero h1{color:var(--navy);max-width:16ch}
.phero p{color:var(--muted)}

/* home slider */
.hero2{position:relative;height:600px;overflow:hidden;background:#fff}
.slides,.slide{position:absolute;inset:0}
.slide{opacity:0;visibility:hidden;transition:opacity .9s ease,visibility .9s}
.slide.on{opacity:1;visibility:visible}
.slide::before{content:"";position:absolute;inset:0 0 0 30%;background:var(--img) center/cover;transform:scale(1.08);transition:transform 7s ease-out}
.slide.on::before{transform:scale(1)}
.slide::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#fff 0%,#fff 32%,rgba(255,255,255,.9) 44%,rgba(255,255,255,.2) 70%,rgba(255,255,255,0) 100%)}
.slide .wrap{position:relative;z-index:2;height:100%;display:flex;align-items:center}
.cap{max-width:560px;transform:translateY(16px);opacity:0;transition:transform .8s .25s ease,opacity .8s .25s ease}
.slide.on .cap{transform:none;opacity:1}
.cap h1,.cap h2{font-size:clamp(36px,4.6vw,58px);margin:14px 0 16px;color:var(--navy)}
.cap p{font-size:19px;color:var(--muted);max-width:46ch}
.cap .ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.s-ctrl{position:absolute;left:0;right:0;bottom:84px;z-index:3;display:flex;align-items:center;gap:14px}
.s-btn{width:44px;height:44px;border-radius:50%;border:0;background:#fff;box-shadow:var(--sh-1);font-size:24px;line-height:1;color:var(--ink);cursor:pointer}
.s-btn:hover{color:var(--red);box-shadow:var(--sh-2)}
.dots{display:flex;gap:8px}
.dots button{width:10px;height:10px;border-radius:999px;border:0;background:#d8d4cf;cursor:pointer;padding:0;transition:width .3s,background .3s}
.dots button[aria-current]{width:34px;background:var(--red)}

/* camp strip overlapping the slider (as on the original homepage) */
.camp-strip{position:relative;z-index:5;margin-top:-56px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
.cs{display:flex;gap:16px;align-items:center;background:#fff;border-radius:18px;padding:18px 20px;box-shadow:var(--sh-2)}
.cs b{display:block;font-size:16px}
.cs span{color:var(--muted);font-size:14px}
.cs .next{display:inline-block;margin-top:6px;font-style:normal;font-size:12.5px;font-weight:700;color:var(--green);background:var(--green-l);padding:3px 9px;border-radius:7px}
.cs .cal{flex:0 0 70px;box-shadow:none;border:1px solid #f0efed}
.cs .cal .d{font-size:26px}
.cs-red{background:linear-gradient(135deg,#d63333,#a81f1f);color:#fff;box-shadow:var(--sh-red)}
.cs-red span{color:#ffe3e0}
.cs-red .big{display:block;color:#fff;font-size:24px;font-weight:800;letter-spacing:-.01em}
.cs-ic{width:54px;height:54px;border-radius:16px;background:rgba(255,255,255,.18);display:grid;place-items:center;color:#fff;flex:0 0 auto}

/* home: portrait card, speciality tiles, stats, floating image, CTA band */
.portrait-card{position:relative;max-width:380px;margin:0 auto;padding:18px;background:#fff;border-radius:26px;box-shadow:var(--sh-3)}
.portrait-card img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:top;border-radius:18px}
.pc-badge{position:absolute;top:-18px;right:-18px;background:var(--red);color:#fff;border-radius:18px;padding:14px 18px;text-align:center;box-shadow:var(--sh-red)}
.pc-badge b{display:block;font-size:26px;line-height:1}
.pc-badge span{font-size:12px;font-weight:600;opacity:.9}
.pc-name{position:absolute;left:-22px;bottom:34px;background:#fff;border-radius:14px;padding:12px 16px;box-shadow:var(--sh-2)}
.pc-name b{display:block}
.pc-name small{color:var(--muted)}
.tiles{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}
.tile{position:relative;border-radius:20px;overflow:hidden;aspect-ratio:3/4;box-shadow:var(--sh-1);transition:transform .3s,box-shadow .3s;background:#fff}
.tile img{width:100%;height:100%;object-fit:cover;transition:transform .6s}
.tile::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(28,36,48,.82))}
.tile span{position:absolute;z-index:1;left:16px;right:16px;bottom:16px;color:#fff;font-weight:800;font-size:17px;display:flex;justify-content:space-between;gap:8px;align-items:end}
.tile i{font-style:normal;width:30px;height:30px;border-radius:50%;background:#fff;color:var(--red);display:grid;place-items:center;flex:0 0 auto;transform:translateX(-6px);opacity:0;transition:.3s}
.tile:hover{transform:translateY(-6px);box-shadow:var(--sh-3)}
.tile:hover img{transform:scale(1.07)}
.tile:hover i{opacity:1;transform:none}
.stats{gap:18px}
.stat{border-radius:20px;padding:24px;align-items:flex-start}
.st-ic{width:58px;height:58px;border-radius:16px;background:var(--red-l);color:var(--red);display:grid;place-items:center;margin-bottom:10px}
.st-ic img{width:38px;height:38px;object-fit:contain;mix-blend-mode:multiply;margin:0}
.stat b{font-size:34px;color:var(--red)}
.float-img{display:grid;place-items:center}
.float-img img{max-width:100%;max-height:380px;filter:drop-shadow(0 30px 40px rgba(28,36,48,.15))}
.cta-band{border-radius:28px;padding:48px 52px;background:linear-gradient(135deg,#d63333 0%,#b62222 60%,#8f1b1b 100%);color:#fff;display:flex;justify-content:space-between;align-items:center;gap:32px;flex-wrap:wrap;box-shadow:var(--sh-red);position:relative;overflow:hidden}
.cta-band::before{content:"";position:absolute;right:-60px;top:-60px;width:260px;height:260px;border-radius:50%;background:rgba(255,255,255,.08)}
.cta-band h2{color:#fff;font-size:clamp(26px,3vw,36px)}
.cta-band p{color:#ffe3e0;margin-top:8px;font-size:17px}
.cta-acts{display:flex;gap:12px;flex-wrap:wrap;position:relative}

/* about centres, patient rights */
.centres{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.centre{border-radius:20px;padding:26px;display:flex;flex-direction:column;gap:6px}
.centre .ic{width:46px;height:46px;border-radius:14px;background:var(--red-l);color:var(--red);display:grid;place-items:center;margin-bottom:8px}
.centre small{color:var(--muted)}
.centre p{color:var(--ink);margin-top:6px}
.rights{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.right{display:flex;gap:16px;border-radius:18px;padding:22px}
.right .ok{flex:0 0 38px;height:38px;border-radius:50%;background:var(--green-l);color:var(--green);display:grid;place-items:center}
.right b{display:block;margin-bottom:4px}
.right p{color:var(--muted);font-size:15px}
.steps3 div{border-radius:18px;padding:24px;flex-direction:column;gap:12px}
.steps3 b{width:40px;height:40px;flex:none;box-shadow:var(--sh-red)}
.member img{box-shadow:0 0 0 3px #fff,0 0 0 5px var(--red-l)}

/* floating WhatsApp + back to top */
.fab-wa{position:fixed;right:22px;bottom:22px;z-index:45;display:flex;align-items:center;gap:10px;background:var(--wa);color:#063b1c;font-weight:800;padding:12px 18px 12px 14px;border-radius:999px;box-shadow:0 14px 30px -8px rgba(37,211,102,.6)}
.fab-wa::before{content:"";position:absolute;inset:-6px;border-radius:inherit;border:2px solid rgba(37,211,102,.45);animation:ring 2.4s ease-out infinite}
@keyframes ring{from{transform:scale(.95);opacity:1}to{transform:scale(1.18);opacity:0}}
.to-top{position:fixed;right:26px;bottom:90px;z-index:45;width:44px;height:44px;border-radius:50%;border:0;background:#fff;color:var(--red);font-size:20px;font-weight:800;box-shadow:var(--sh-2);cursor:pointer;opacity:0;transform:translateY(10px);pointer-events:none;transition:.25s}
.to-top.show{opacity:1;transform:none;pointer-events:auto}

@media (prefers-reduced-motion:reduce){.tk-track{animation:none}.slide::before{transition:none;transform:none}.fab-wa::before{animation:none}}
@media (max-width:980px){
  .hero2{height:560px}
  .slide::before{inset:0}
  .slide::after{background:linear-gradient(180deg,rgba(255,255,255,.55) 0%,rgba(255,255,255,.93) 52%,#fff 100%)}
  .slide .wrap{align-items:flex-end;padding-bottom:120px}
  .s-ctrl{bottom:66px}
  .camp-strip{grid-template-columns:1fr;margin-top:-40px}
  .tiles{grid-template-columns:repeat(3,1fr)}
  .centres,.rights{grid-template-columns:1fr}
  .phero::before{left:0}
  .phero::after{background:linear-gradient(180deg,rgba(255,255,255,.7),rgba(255,255,255,.95) 60%,#fff)}
  .ticker{display:none}
  .pc-name{left:10px}
  .pc-badge{right:6px}
}
@media (max-width:640px){
  .nav{height:70px}
  .brand img{height:46px}
  header.scrolled .nav{height:62px}
  header.scrolled .brand img{height:40px}
  .hero2{height:540px}
  .tiles{grid-template-columns:1fr 1fr}
  .tile{aspect-ratio:1/1}
  .cta-band{padding:32px 26px}
  .fab-wa{display:none}
  .to-top{bottom:96px;right:16px}
  .stats{grid-template-columns:1fr 1fr}
  .stat b{font-size:28px}
  .ebar .pulse{display:none}
}
"""

SITE_JS = r"""// Praveen Hospitals redesign preview — shared script for all pages.
// PREVIEW = true shows the composed WhatsApp message instead of sending it, so testing never messages the real hospital.
// Before launch: confirm the front-desk WhatsApp number with the hospital and set PREVIEW = false.
const PREVIEW = true;
const WHATSAPP = "919948878877"; // mobile listed on the current site; WhatsApp availability unconfirmed
const $ = (id) => document.getElementById(id);
const root = document.documentElement;

// ── language (remembered across pages) ──
function setLang(l) {
  root.dataset.lang = l; root.lang = l;
  document.querySelectorAll(".lang button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.set === l)));
  try { localStorage.setItem("ph-lang", l); } catch (e) {}
  renderCamps();
}
document.querySelectorAll(".lang button").forEach(b => b.addEventListener("click", () => setLang(b.dataset.set)));

// ── tabs: keep the current tab in view on narrow screens ──
const tabList = document.querySelector(".tabs ul"), curTab = document.querySelector(".tabs a[aria-current]");
if (tabList && curTab) {
  tabList.scrollLeft = curTab.parentElement.offsetLeft - (tabList.clientWidth - curTab.offsetWidth) / 2;
  const fade = () => tabList.parentElement.style.setProperty("--fade", tabList.scrollLeft + tabList.clientWidth >= tabList.scrollWidth - 4 ? 0 : 1);
  tabList.addEventListener("scroll", fade, { passive: true }); addEventListener("resize", fade); fade();
}

// ── next health-camp dates ──
const TE_M = ["జన","ఫిబ్ర","మార్చి","ఏప్రి","మే","జూన్","జులై","ఆగ","సెప్టె","అక్టో","నవం","డిసెం"];
const TE_D = ["ఆది","సోమ","మంగళ","బుధ","గురు","శుక్ర","శని"];
function nextWednesday(now) {
  const d = new Date(now); d.setHours(0,0,0,0);
  const end = new Date(now); end.setHours(20,0,0,0);
  let add = (3 - d.getDay() + 7) % 7; if (add === 0 && now > end) add = 7;
  d.setDate(d.getDate() + add); return d;
}
function nthSunday(y, m, n) { const d = new Date(y, m, 1); d.setDate(1 + ((7 - d.getDay()) % 7) + (n - 1) * 7); return d; }
function nextKodad(now) {
  for (let k = 0; k < 3; k++) for (const n of [2, 4]) {
    const d = nthSunday(now.getFullYear(), now.getMonth() + k, n), end = new Date(d); end.setHours(14,0,0,0);
    if (end > now) return d;
  }
}
function fill(calId, nextId, d) {
  const te = root.dataset.lang === "te", el = $(calId); if (!el) return;
  el.querySelector(".m").textContent = te ? TE_M[d.getMonth()] : d.toLocaleString("en-IN", { month: "short" }).toUpperCase();
  el.querySelector(".d").textContent = d.getDate();
  el.querySelector(".w").textContent = te ? TE_D[d.getDay()] + "వారం" : d.toLocaleString("en-IN", { weekday: "long" });
  const days = Math.round((d - new Date(new Date().setHours(0,0,0,0))) / 864e5);
  $(nextId).textContent = te ? (days === 0 ? "ఈరోజే" : days === 1 ? "రేపు" : days + " రోజుల్లో") : (days === 0 ? "Today" : days === 1 ? "Tomorrow" : "In " + days + " days");
}
function renderCamps() {
  const now = new Date(), j = nextWednesday(now), k = nextKodad(now), te = root.dataset.lang === "te";
  fill("cal-j", "next-j", j); fill("cal-k", "next-k", k);
  const hc = $("heroCamp"); if (!hc) return;
  const f = j <= k ? ["Jaggaiahpet", "జగ్గయ్యపేట", j] : ["Kodad", "కోదాడ", k];
  hc.textContent = te ? `తదుపరి: ${f[1]}, ${f[2].getDate()} ${TE_M[f[2].getMonth()]}` : `Next: ${f[0]}, ${f[2].toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short" })}`;
}

// ── booking: buttons on any page pre-fill the form on the contact page ──
const form = $("bookForm");
function prefill(dept, msg) {
  if (form) { $("fdept").value = dept; if (msg) $("fmsg").value = msg; return; }
  try { sessionStorage.setItem("ph-prefill", JSON.stringify({ dept, msg })); } catch (e) {}
}
document.querySelectorAll("a[href='#book']").forEach(a => { if (!form) a.setAttribute("href", "contact.html#book"); });
document.querySelectorAll("[data-pkg]").forEach(a => a.addEventListener("click", () => prefill("Health Checkup", "Please share details and price for the " + a.dataset.pkg + ".")));
document.querySelectorAll("[data-doctor]").forEach(a => a.addEventListener("click", () => prefill("Cardiology", "I'd like to consult " + a.dataset.doctor + ".")));
document.querySelectorAll("[data-wa='symptoms']").forEach(a => a.addEventListener("click", () => prefill("Not sure", "")));

function send(text) {
  if (PREVIEW) { $("mText").textContent = text; $("modal").classList.add("open"); return; }
  window.open("https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(text), "_blank", "noopener");
}
if (form) {
  $("fdate").min = new Date().toISOString().slice(0, 10);
  try { const p = JSON.parse(sessionStorage.getItem("ph-prefill") || "null"); if (p) { $("fdept").value = p.dept; if (p.msg) $("fmsg").value = p.msg; sessionStorage.removeItem("ph-prefill"); } } catch (e) {}
  form.addEventListener("submit", e => {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    const v = id => $(id).value.trim();
    const lines = ["Appointment request — Praveen Hospitals", "Name: " + v("fname"), "Mobile: " + v("fphone"), "Department: " + v("fdept")];
    if (v("fdate")) lines.push("Preferred date: " + new Date(v("fdate") + "T00:00").toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short", year: "numeric" }));
    if (v("fmsg")) lines.push("Message: " + v("fmsg"));
    send(lines.join("\n"));
  });
}
const modal = $("modal");
if (modal) {
  $("mClose").addEventListener("click", () => modal.classList.remove("open"));
  modal.addEventListener("click", e => { if (e.target === modal) modal.classList.remove("open"); });
}

// ── gallery lightbox ──
const lb = $("lightbox");
if (lb) {
  document.querySelectorAll("[data-full]").forEach(b => b.addEventListener("click", () => { lb.querySelector("img").src = b.dataset.full; lb.classList.add("open"); }));
  lb.addEventListener("click", e => { if (e.target !== lb.querySelector("img")) lb.classList.remove("open"); });
}
addEventListener("keydown", e => { if (e.key === "Escape") { modal && modal.classList.remove("open"); lb && lb.classList.remove("open"); } });

// ── reveal on scroll ──
const io = "IntersectionObserver" in window ? new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }), { threshold: .1 }) : null;
document.querySelectorAll(".reveal").forEach(el => io ? io.observe(el) : el.classList.add("in"));

// ── header: shrink + shadow on scroll; back-to-top ──
const hdr = document.querySelector("header"), toTop = document.querySelector(".to-top");
const onScroll = () => { const y = scrollY > 40; hdr && hdr.classList.toggle("scrolled", y); toTop && toTop.classList.toggle("show", scrollY > 600); };
addEventListener("scroll", onScroll, { passive: true }); onScroll();
if (toTop) toTop.addEventListener("click", () => scrollTo({ top: 0, behavior: "smooth" }));

// ── home slider: autoplay, arrows, dots, swipe; pauses on hover/focus; no autoplay for reduced motion ──
const hero = document.querySelector(".hero2");
if (hero) {
  const slides = [...hero.querySelectorAll(".slide")], dots = [...hero.querySelectorAll(".dots button")];
  let i = 0, timer = null;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const go = (n) => {
    slides[i].classList.remove("on"); dots[i].removeAttribute("aria-current");
    i = (n + slides.length) % slides.length;
    slides[i].classList.add("on"); dots[i].setAttribute("aria-current", "true");
  };
  const play = () => { if (!reduce) { clearInterval(timer); timer = setInterval(() => go(i + 1), 6500); } };
  const stop = () => clearInterval(timer);
  hero.querySelector(".s-next").addEventListener("click", () => { go(i + 1); play(); });
  hero.querySelector(".s-prev").addEventListener("click", () => { go(i - 1); play(); });
  dots.forEach((d, n) => d.addEventListener("click", () => { go(n); play(); }));
  hero.addEventListener("mouseenter", stop); hero.addEventListener("mouseleave", play);
  hero.addEventListener("focusin", stop); hero.addEventListener("focusout", play);
  let x0 = null;
  hero.addEventListener("touchstart", e => { x0 = e.touches[0].clientX; }, { passive: true });
  hero.addEventListener("touchend", e => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) { go(i + (dx < 0 ? 1 : -1)); play(); } x0 = null; });
  play();
}

// ── animated counters for hospital statistics ──
const counters = document.querySelectorAll(".count[data-to]");
if (counters.length && "IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const co = new IntersectionObserver(es => es.forEach(en => {
    if (!en.isIntersecting) return; co.unobserve(en.target);
    const el = en.target, to = +el.dataset.to, t0 = performance.now(), dur = 1400;
    const step = (now) => { const p = Math.min((now - t0) / dur, 1), v = Math.round(to * (1 - Math.pow(1 - p, 3))); el.textContent = v.toLocaleString("en-IN"); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0"; requestAnimationFrame(step);
  }), { threshold: .4 });
  counters.forEach(c => co.observe(c));
}

let saved = "en"; try { saved = localStorage.getItem("ph-lang") || "en"; } catch (e) {}
setLang(saved);
"""

def main():
    style = (HERE / "_style.css").read_text()
    # old single-page nav list is replaced by the tab bar
    style = style.replace(".nav ul{display:flex;gap:26px;list-style:none;font-weight:600;font-size:15px;color:var(--muted)}", "")
    style = style.replace(".nav ul,.nav .act .btn-line{display:none}", "")
    style = style.replace(".nav .act{display:none}", "")
    (HERE / "styles.css").write_text(style + CSS_EXTRA)
    (HERE / "site.js").write_text(SITE_JS)
    for key, (title, body) in PAGES.items():
        html = f"""<!DOCTYPE html>
<!-- REDESIGN PREVIEW for praveenhospitals.com — private concept, not the live site. Built by build.py. -->
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Praveen Hospitals, Vijayawada (redesign preview)</title>
<meta name="description" content="Praveen Hospitals, Moghalrajapuram, Vijayawada — 100-bed cardiac and multispeciality hospital. 24×7 emergency. Arogyasri, EHS, ECHS and all TPA insurance accepted.">
<meta name="robots" content="noindex">
<link rel="stylesheet" href="styles.css">
</head>
<body>
{header(key)}
<main id="top">
{body}
</main>
{FOOTER}
<script src="site.js"></script>
</body>
</html>
"""
        (HERE / f"{key}.html").write_text(html)
    print("built:", ", ".join(f"{k}.html" for k in PAGES))

main()
