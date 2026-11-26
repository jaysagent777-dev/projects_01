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
  <span class="pulse"><i></i>{t("24×7 Emergency &amp; Cardiac Care", "24×7 అత్యవసర &amp; గుండె వైద్య సేవలు")}</span>
  <span style="display:flex;align-items:center;gap:16px">
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

STATS = [
    ("monthly_in_patients", "150–200", "Monthly in-patients", "నెలవారీ ఇన్-పేషెంట్లు"),
    ("angiographies", "100–120", "Angiographies every month", "ప్రతి నెలా యాంజియోగ్రఫీలు"),
    ("cardiac_peripheral_intervention", "3,800", "Cardiac & peripheral interventions", "కార్డియాక్ & పెరిఫెరల్ ఇంటర్వెన్షన్లు"),
    ("open_heart_surgery", "2,000", "Open heart surgeries", "ఓపెన్ హార్ట్ సర్జరీలు"),
    ("permanent_pacemaker", "180", "Permanent pacemakers", "పర్మనెంట్ పేస్‌మేకర్లు"),
    ("peripheral_vascular_surgery", "3,500", "Peripheral vascular surgeries", "పెరిఫెరల్ వాస్కులర్ సర్జరీలు"),
    ("av_fistula", "200", "AV fistulas for hemodialysis", "హీమోడయాలసిస్ కోసం AV ఫిస్టులా"),
    ("cardiac_electrophysiology", "250", "Cardiac EP & RF ablation", "కార్డియాక్ EP & RF అబ్లేషన్"),
]
STATS_HTML = '<div class="stats">' + "".join(
    f'<div class="stat reveal"><img src="{IMG}statistics/{f}.jpg" alt="" loading="lazy"><b>{n}</b><span>{t(en, te)}</span></div>' for f, n, en, te in STATS
) + "</div>"

VIDEO_SECTION = f"""<section class="alt"><div class="wrap two-col">
  <div class="reveal"><div class="eyebrow">{t("Watch", "చూడండి")}</div>
    <h2 class="h2">{t("Expert surgeons. Modular operating theatres.", "నిపుణులైన సర్జన్లు. మాడ్యులర్ ఆపరేషన్ థియేటర్లు.")}</h2>
    <p class="lede">{t("2,000+ open heart surgeries with a 98% success rate — performed right here in Vijayawada.", "98% విజయ శాతంతో 2,000కు పైగా ఓపెన్ హార్ట్ సర్జరీలు — ఇక్కడే విజయవాడలో.")}</p>
    <a class="btn btn-red" href="gallery.html">{t("See the gallery", "గ్యాలరీ చూడండి")} →</a></div>
  <div class="reveal">{VIDEO}</div>
</div></section>"""

CONTACT_STRIP = f"""<section><div class="wrap two-col">
  <div class="reveal"><div class="eyebrow">{t("Find us", "మా చిరునామా")}</div>
    <h2 class="h2">{t("Moghalrajapuram, on the No.5 bus route.", "మొగల్రాజపురం, నెం.5 బస్ రూట్‌లో.")}</h2>
    <p class="lede">#32-9-18, Moghalrajapuram, Madhugarden Center, Vijayawada – 520 010</p>
    <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-red" href="tel:+918662444440">{PHONE_SVG}0866-2444440</a><a class="btn btn-line" href="contact.html">{t("All contact details", "పూర్తి వివరాలు")}</a></div></div>
  <div class="reveal">{MAP}</div>
</div></section>"""

# The contact page form section, with the blocked Google iframe swapped for the OSM map
BOOK = re.sub(r'<div class="map">.*?</div>', MAP, P["book"], flags=re.S)

# Home: keep the full-page specialities/doctor sections lighter by linking onwards
SPEC_TEASER = P["specialities"].replace('<section id="specialities">', '<section id="specialities">').replace(
    "</div>\n  </div>\n</section>", f'</div>\n    <p style="text-align:center;margin-top:28px"><a class="btn btn-line" href="specialities.html">{t("All specialities", "అన్ని విభాగాలు")} →</a></p>\n  </div>\n</section>', 1)

PAGES = {}

PAGES["index"] = ("Home", P["hero"] + P["outcomes"] + SPEC_TEASER + P["doctors"] + P["checkups"] + P["camps"] + VIDEO_SECTION + P["insurance"] + CONTACT_STRIP)

PAGES["about"] = ("About Us", page_hero(t("About Us", "మా గురించి"), t("Caring for hearts since 2007.", "2007 నుండి గుండెలకు ఆదరణ."),
    t("A cardiac centre founded by Dr. M. Praveen — today a 100-bed hospital for cardiology, cardiothoracic surgery, neurology and neurosurgery.", "డా. ఎం. ప్రవీణ్ స్థాపించిన కార్డియాక్ సెంటర్ — నేడు కార్డియాలజీ, కార్డియోథొరాసిక్ సర్జరీ, న్యూరాలజీ, న్యూరోసర్జరీ కోసం 100 పడకల ఆసుపత్రి."), "slider/banner_5.jpg") + f"""
<section><div class="wrap two-col">
  <div class="reveal"><div class="eyebrow">{t("Who we are", "మేము ఎవరం")}</div>
    <h2 class="h2">{t("Everything under one roof.", "అన్నీ ఒకే చోట.")}</h2>
    <p class="lede">{t("We provide consultation, diagnosis and treatment in Cardiology, Cardiothoracic Surgery, Neurology and Neuro Surgery at CGHS rates.", "కార్డియాలజీ, కార్డియోథొరాసిక్ సర్జరీ, న్యూరాలజీ, న్యూరోసర్జరీలో సంప్రదింపులు, నిర్ధారణ, చికిత్స — CGHS ధరలకే.")}</p>
    <p class="muted-p">{t("Founded in 2007, the centre has state-of-the-art facilities in Cardiology &amp; Neurology, Critical Care, Radiology and Anesthesiology, with diagnostics, operating theatres and a cath-lab in the same building.", "2007లో ప్రారంభమైన ఈ కేంద్రంలో కార్డియాలజీ &amp; న్యూరాలజీ, క్రిటికల్ కేర్, రేడియాలజీ, అనస్థీషియాలజీలో అత్యాధునిక సదుపాయాలు ఉన్నాయి — డయాగ్నొస్టిక్స్, ఆపరేషన్ థియేటర్లు, క్యాథ్ ల్యాబ్ అన్నీ ఒకే భవనంలో.")}</p></div>
  <div class="photo reveal"><img src="{IMG}slider/banner_3.jpg" alt="Intensive care unit at Praveen Hospitals"></div>
</div></section>
<section class="alt"><div class="wrap mv">
  <div class="mvcard reveal"><span class="ic">{ic(I_TARGET)}</span><div class="eyebrow">{t("Mission", "లక్ష్యం")}</div><p>{t("To provide effective, affordable, dedicated and easily accessible quality health care to the needy at any hour.", "అవసరమైన వారికి ఏ సమయంలోనైనా ప్రభావవంతమైన, అందుబాటు ధరలో, అంకితభావంతో కూడిన నాణ్యమైన వైద్యం అందించడం.")}</p></div>
  <div class="mvcard reveal"><span class="ic">{ic(I_EYE)}</span><div class="eyebrow">{t("Vision", "దృష్టి")}</div><p>{t("To reach the entire states of Andhra Pradesh and Telangana, with health education for the public and a stress on preventive care and early diagnosis.", "ఆంధ్రప్రదేశ్, తెలంగాణ రాష్ట్రాలంతటా చేరుకోవడం — ప్రజలకు ఆరోగ్య అవగాహన, ముందస్తు జాగ్రత్త మరియు త్వరిత నిర్ధారణపై దృష్టితో.")}</p></div>
</div></section>
""" + P["doctors"].replace('<section id="doctors" class="alt">', '<section id="doctors">') + f"""
<section class="alt"><div class="wrap two-col">
  <div class="reveal"><div class="eyebrow">{t("Beyond Vijayawada", "విజయవాడ దాటి")}</div>
    <h2 class="h2">{t("Three centres, one standard of care.", "మూడు కేంద్రాలు, ఒకే నాణ్యత.")}</h2>
    <p class="lede">{t("Besides this hospital, Dr. Praveen also practises at centres on Hyderabad Road and Huzurnagar Road, and our team runs regular health camps in Jaggaiahpet and Kodad.", "ఈ ఆసుపత్రితో పాటు డా. ప్రవీణ్ హైదరాబాద్ రోడ్, హుజూర్‌నగర్ రోడ్‌లోని కేంద్రాలలో కూడా వైద్యం చేస్తారు. జగ్గయ్యపేట, కోదాడలో మా బృందం క్రమం తప్పకుండా ఆరోగ్య శిబిరాలు నిర్వహిస్తుంది.")}</p></div>
  <div class="reveal">{STATS_HTML.replace('class="stats"', 'class="stats mini"', 1)}</div>
</div></section>""")

PAGES["services"] = ("Services", page_hero(t("Services", "సేవలు"), t("100-bed hospital. Latest ICU. Modular OT.", "100 పడకల ఆసుపత్రి. ఆధునిక ICU. మాడ్యులర్ OT."),
    t("In 14 years: 11,500+ angiograms, 4,000 stents with a 99.6% success rate and 2,000 bypass surgeries with a 98% success rate.", "14 సంవత్సరాలలో: 11,500కు పైగా యాంజియోగ్రామ్‌లు, 99.6% విజయ శాతంతో 4,000 స్టెంట్లు, 98% విజయ శాతంతో 2,000 బైపాస్ సర్జరీలు.")) + f"""
<section><div class="wrap">
  <div class="head reveal"><div class="eyebrow">{t("Hospital statistics", "ఆసుపత్రి గణాంకాలు")}</div><h2>{t("Experience you can count on.", "లెక్కించదగిన అనుభవం.")}</h2></div>
  {STATS_HTML}
  <p class="note">{t("Figures as reported by Praveen Hospitals.", "ప్రవీణ్ హాస్పిటల్స్ నివేదించిన గణాంకాలు.")}</p>
</div></section>
<section class="alt"><div class="wrap svc">
  <div class="svc-card reveal"><img src="{IMG}services/cardiology.png" alt="" loading="lazy">
    <h3>{t("Cardiology services", "కార్డియాలజీ సేవలు")}</h3>
    <ul class="ticks"><li>Bypass &amp; Valve Surgeries</li><li>PTCA (Percutaneous Transluminal Coronary Angioplasty)</li><li>Pacemaker &amp; EP Study</li><li>ECG (Electrocardiogram)</li><li>2D Echo</li><li>TMT (Treadmill Test)</li><li>Ambulatory BP monitoring</li><li>Holter analysis</li></ul></div>
  <div class="svc-card reveal"><img src="{IMG}services/radiology.png" alt="" loading="lazy">
    <h3>{t("Radiology services", "రేడియాలజీ సేవలు")}</h3>
    <ul class="ticks"><li>Ultrasound scan</li><li>Doppler</li><li>Mammography (breast cancer screening)</li></ul>
    <div class="callout">{t("Not sure which test you need? Send us your doctor's prescription on WhatsApp.", "ఏ పరీక్ష అవసరమో తెలియదా? మీ డాక్టర్ ప్రిస్క్రిప్షన్‌ను WhatsAppలో పంపండి.")}</div></div>
</div></section>""" + P["checkups"] + VIDEO_SECTION)

PAGES["specialities"] = ("Specialities", page_hero(t("Specialities", "విభాగాలు"), t("Five specialities. One team.", "ఐదు విభాగాలు. ఒకే బృందం."),
    t("Heart, brain and diagnostic care, coordinated under one roof.", "గుండె, మెదడు, డయాగ్నొస్టిక్ వైద్యం — అన్నీ ఒకే చోట సమన్వయంతో."), "banners/speciality.jpeg")
    + P["specialities"] + P["doctors"] + CONTACT_STRIP)

PAGES["patient-care"] = ("Patient Care", page_hero(t("Patient Care", "పేషెంట్ కేర్"), t("Care that continues at home.", "ఇంటి వరకూ కొనసాగే సంరక్షణ."),
    t("Personalised attention for elderly, chronically ill and post-surgery patients — from trained, qualified caregivers.", "వృద్ధులు, దీర్ఘకాల వ్యాధిగ్రస్తులు, శస్త్రచికిత్స తర్వాత కోలుకుంటున్న వారికి — శిక్షణ పొందిన సిబ్బందితో వ్యక్తిగత శ్రద్ధ."), "slider/banner_2.jpg") + f"""
<section><div class="wrap two-col">
  <div class="reveal"><div class="eyebrow">{t("Home care", "ఇంటి వద్ద సంరక్షణ")}</div>
    <h2 class="h2">{t("Plans built around your family.", "మీ కుటుంబానికి తగిన ప్రణాళికలు.")}</h2>
    <p class="lede">{t("Care is delivered through customisable, plan-based programmes that bring family members and caregivers together — a practical option for long-term illness and disease management.", "కుటుంబ సభ్యులు, సంరక్షకులు కలిసి పనిచేసే, అవసరానికి తగ్గట్టు మార్చుకోగల ప్రణాళికలతో సంరక్షణ — దీర్ఘకాల వ్యాధుల నిర్వహణకు ఆచరణీయమైన మార్గం.")}</p>
    <ul class="ticks"><li>{t("Elderly care", "వృద్ధుల సంరక్షణ")}</li><li>{t("Chronic illness management", "దీర్ఘకాల వ్యాధుల నిర్వహణ")}</li><li>{t("Post-surgery recovery", "శస్త్రచికిత్స తర్వాత కోలుకోవడం")}</li></ul>
    <a class="btn btn-red" href="contact.html#book">{t("Ask about home care", "ఇంటి సంరక్షణ గురించి అడగండి")} →</a></div>
  <div class="photo reveal"><img src="{IMG}care.png" alt="" loading="lazy" style="object-fit:contain;background:#fff"></div>
</div></section>""" + P["rights"].replace('<details open>', '<details open>', 1) + f"""
<section><div class="wrap"><div class="head reveal"><div class="eyebrow">{t("Your rights, in full", "మీ పూర్తి హక్కులు")}</div><h2>{t("As a patient, you can expect:", "పేషెంట్‌గా మీరు ఆశించవచ్చు:")}</h2></div>
<ul class="ticks big reveal">
<li>{t("To be treated with respect, consideration, compassion and dignity, in a safe and clean environment.", "సురక్షితమైన, పరిశుభ్రమైన వాతావరణంలో గౌరవం, ఆదరణ, మర్యాదతో కూడిన చికిత్స.")}</li>
<li>{t("Full protection of your privacy, dignity and confidentiality in discussions, examinations and treatment.", "చర్చలు, పరీక్షలు, చికిత్సలో మీ గోప్యత మరియు గౌరవానికి పూర్తి రక్షణ.")}</li>
<li>{t("A clear explanation of your diagnosis, the benefits and risks of each treatment, and the expected outcome.", "మీ వ్యాధి నిర్ధారణ, ప్రతి చికిత్స ప్రయోజనాలు, ప్రమాదాలు, ఆశించిన ఫలితంపై స్పష్టమైన వివరణ.")}</li>
<li>{t("To be told why any person is present during your care.", "మీ చికిత్స సమయంలో ఎవరైనా ఎందుకు ఉన్నారో తెలుసుకునే హక్కు.")}</li>
<li>{t("Written permission before your records are shared with anyone not directly involved in your care.", "మీ చికిత్సతో సంబంధం లేని వారికి రికార్డులు ఇచ్చే ముందు మీ లిఖిత అనుమతి.")}</li>
<li>{t("Protection from physical abuse and neglect.", "శారీరక వేధింపులు, నిర్లక్ష్యం నుండి రక్షణ.")}</li>
</ul></div></section>""")

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
  <div class="steps3 reveal">
    <div><b>1</b>{t("Bring your scheme card or insurance policy and photo ID.", "మీ పథకం కార్డు లేదా ఇన్సూరెన్స్ పాలసీ, ఫోటో ID తీసుకురండి.")}</div>
    <div><b>2</b>{t("Our desk checks your eligibility and starts pre-authorisation.", "మా సిబ్బంది అర్హతను పరిశీలించి ముందస్తు అనుమతి ప్రక్రియ ప్రారంభిస్తారు.")}</div>
    <div><b>3</b>{t("Get treated — we handle the paperwork with the scheme.", "చికిత్స పొందండి — పథకం పత్రాల పని మేము చూసుకుంటాం.")}</div>
  </div>
  <p class="note" style="text-align:center">{t("Coverage depends on your scheme's rules. Call 0866-2444440 to confirm before admission.", "కవరేజ్ మీ పథకం నియమాలపై ఆధారపడి ఉంటుంది. చేరే ముందు 0866-2444440కి కాల్ చేసి నిర్ధారించుకోండి.")}</p>
</div></section>""" + CONTACT_STRIP)

GALLERY = [("slider/banner_3.jpg", "ICU"), ("gallery/gallery_1.jpg", ""), ("gallery/gallery_2.jpg", ""), ("gallery/gallery_3.jpg", ""),
           ("gallery/gallery_4.jpg", ""), ("gallery/gallery_5.jpg", ""), ("gallery/gallery_6.jpg", ""), ("gallery/gallery_7.jpg", ""),
           ("slider/banner_4.jpg", ""), ("slider/banner_5.jpg", ""), ("praveen.jpg", "")]
PAGES["gallery"] = ("Gallery", page_hero(t("Gallery", "గ్యాలరీ"), t("Inside Praveen Hospitals.", "ప్రవీణ్ హాస్పిటల్స్ లోపల."),
    t("Our ICU, operating theatres, cath-lab and wards.", "మా ICU, ఆపరేషన్ థియేటర్లు, క్యాథ్ ల్యాబ్, వార్డులు."), "gallery/gallery_4.jpg") + f"""
<section><div class="wrap">
  <div class="head reveal"><div class="eyebrow">{t("Video", "వీడియో")}</div><h2>{t("Open heart surgery", "ఓపెన్ హార్ట్ సర్జరీ")}</h2></div>
  <div class="reveal" style="max-width:900px">{VIDEO}</div>
</div></section>
<section class="alt"><div class="wrap">
  <div class="head reveal"><div class="eyebrow">{t("Photos", "ఫోటోలు")}</div><h2>{t("Facilities", "సదుపాయాలు")}</h2><p>{t("Tap any photo to enlarge.", "పెద్దగా చూడటానికి ఫోటోపై నొక్కండి.")}</p></div>
  <div class="pgrid">{"".join(f'<button class="ph reveal" data-full="{IMG}{f}"><img src="{IMG}{f}" alt="Praveen Hospitals photo {i+1}" loading="lazy"></button>' for i, (f, c) in enumerate(GALLERY))}</div>
</div></section>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo"><button class="lb-x" aria-label="Close">×</button><img alt=""></div>""")

PAGES["contact"] = ("Contact Us", page_hero(t("Contact Us", "సంప్రదించండి"), t("We're here 24×7.", "24×7 అందుబాటులో ఉన్నాం."),
    t("Call, WhatsApp, or book online — whatever is easiest for you.", "కాల్, WhatsApp లేదా ఆన్‌లైన్ బుకింగ్ — మీకు ఏది సులభమో అది."), "slider/banner_5.jpg") + f"""
<section style="padding-bottom:0"><div class="wrap qc">
  <a class="qcard reveal" href="tel:+918662444440"><span class="ic">{ic(I_PHONE)}</span><b>{t("Emergency &amp; appointments", "అత్యవసరం &amp; అపాయింట్‌మెంట్లు")}</b><span>0866-2444440 · 0866-2444414</span></a>
  <a class="qcard reveal" href="tel:+919948878877"><span class="ic">{ic(I_MOBILE)}</span><b>{t("Mobile", "మొబైల్")}</b><span>+91 99488 78877</span></a>
  <a class="qcard reveal" href="mailto:praveencardiaccentre@gmail.com"><span class="ic">{ic(I_MAIL)}</span><b>{t("Email", "ఈమెయిల్")}</b><span>praveencardiaccentre@gmail.com</span></a>
</div></section>""" + BOOK + P["camps"])

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
