# -*- coding: utf-8 -*-
"""Andhra Hospitals (andhrahospitals.org) — redesign preview that KEEPS the original layout:
logo + accreditation header, uppercase menu with red "Our Locations" pill, full-width slider,
4 colour boxes, latest-news ticker, intro + appointment form, charity works, news, video feedback,
media, footer — modernised, responsive, and with the original's problems fixed. Build: python3 site.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_template"))
from classic import *  # noqa

A = "https://andhrahospitals.org/assets/"
S = {"name": "Andhra Hospitals", "domain": "andhrahospitals.org", "desk": "appointments desk",
     "description": "Andhra Hospitals, Vijayawada — The People's Pulse. Multi-speciality care, 24×7 emergency, paediatrics and critical care across Andhra Pradesh."}
PHONE, TEL = "0866 2574757", "+918662574757"

SPECIALITIES = ["Surgical Gastroenterology", "General &amp; Laparoscopic Surgery", "General Medicine", "Neonatology", "General Paediatrics",
    "Paediatric Intensive Care", "Medical Gastroenterology", "Obstetrics and Gynaecology", "Fetal &amp; Maternal Medicine", "Critical Care",
    "Emergencies &amp; Trauma", "Joint Replacement &amp; Orthopaedics", "Rheumatology", "Neurology", "Neurosurgery", "Urology", "Nephrology",
    "Pulmonology", "Radiology", "Surgical Oncology", "Medical Oncology", "ENT", "Physiotherapy", "Haemodialysis", "Transfusion Medicine",
    "Child Development Center (CDC)"]
SERVICES = ["24×7 Laboratory", "24×7 Pharmacy", "24×7 Ambulance Services (ACLS)", "Fetal Scanning", "CT Scan", "Ultrasound Scan", "Color Doppler",
    "ECMO (Neonatal, Paediatric &amp; Adult)", "2D Echo", "ECG", "EEG", "ENMG", "NCS", "Laminar Airflow Theatres", "Liquid O2", "CSSD", "Laundry"]
LOCATIONS = ["Vijayawada", "Heart and Brain Institute", "Bhavanipuram", "Eluru", "Machilipatnam", "Visakhapatnam", "Dental Care", "Central Laboratory"]
CHARITY = [
    (A + "img/1577185786s1.jpg", "Healing Little Hearts, UK", "Andhra Hospitals in association with Healing Little Hearts, UK."),
    (A + "img/1577185993s2.jpg", "Super Star Mr. G. Mahesh Babu — Support &amp; Campaign", "Andhra Hospitals in association with Mr. G. Mahesh Babu."),
    (A + "img/1577351681s3.jpg", "Swarna Bharath Trust", "Andhra Hospitals in association with Swarna Bharath Trust."),
    (A + "img/1577352667s4.jpg", "Mrs. Samantha — 'Pratyusha Support'", "Andhra Hospitals in association with Samantha's Pratyusha Support."),
    (A + "img/1577352387s5.jpg", "Rotary Club in Vijayawada", "Andhra Hospitals in association with the Rotary Club in Vijayawada."),
    (A + "img/1577352475s6.jpg", "Medical Camps", "Andhra Hospitals in association with many medical camps."),
]
NEWS = [
    (A + "uploads/news/WhatsApp_Image_2023-02-03_at_12.28.11_PM_(1).jpeg", "3500+ Free Heart Surgeries Completed",
     "Healing Little Hearts, UK, in association with Andhra Hospitals, has completed more than 3,500 free heart surgeries."),
    (A + "uploads/news/Urinary_bladder_cancer.jpg", "A Rare Laparoscopy Surgery Done for Urinary Bladder Cancer",
     "We are glad to share yet another achievement by the doctors at Andhra Hospitals — a rare laparoscopic surgery for urinary bladder cancer."),
]
VIDEOS = ["Re0K8T8a1eM", "d7_oWaSixsI", "QUKkZKM8yuw", "AGWxHDqd7tg", "XRalBRmRteA", "XN5x81yMCfg", "328VfCoJ-6w", "qvI_j-fQtdg"]
GALLERY = [A + f"uploads/gallery/{g}.jpg" for g in ("g4", "g5", "g6", "g7", "g31", "g41")]
SOCIAL = [("Facebook", "https://www.facebook.com/TheAndhraHospitals/"), ("Instagram", "https://www.instagram.com/andhrahospitalsvja/"),
          ("YouTube", "https://www.youtube.com/channel/UCctJa6-B6rdhOENJbhVKO5A"), ("Twitter", "https://twitter.com/andhrahospital1")]

MENU = [
    ("index", "Home", None),
    ("about", "About", [("about.html", "About Us"), ("achievements.html", "Our Achievements")]),
    ("specialities", "Specialities", [(f"specialities.html#s{i}", s) for i, s in enumerate(SPECIALITIES)]),
    ("services", "Support Services", [(f"services.html#v{i}", s) for i, s in enumerate(SERVICES)]),
    ("doctors", "Doctors", None),
    ("gallery", "Gallery", [("gallery.html#photos", "Photos"), ("gallery.html#videos", "Videos")]),
    ("careers", "Careers", None),
    ("contact", "Contact", None),
]

def header(active):
    loc = "".join(f'<li><a href="locations.html#l{i}">{l}</a></li>' for i, l in enumerate(LOCATIONS))
    return f"""<header class="ah-head">
  <div class="wrap ah-top">
    <a href="index.html" class="ah-logo"><img src="{A}uploads/logos/logo_new_(2)1.png" alt="Andhra Hospitals — The People's Pulse"></a>
    <div class="ah-acc">
      <img src="{A}uploads/logos/main13.png" alt="Accredited by the National Accreditation Board for Hospitals &amp; Healthcare Providers">
      <img src="{A}uploads/logos/nabh-black-new1235212.png" alt="Hospital laboratory accredited by the National Accreditation Board for Testing and Calibration Laboratories">
    </div>
    <div class="ah-right">
      <a class="ah-call" href="tel:{TEL}">{ic("phone", 18)}<span><small>24×7 Emergency</small><b>{PHONE}</b></span></a>
      <a class="ah-paed" href="https://www.andhrapaediatrics.com/" target="_blank" rel="noopener">Andhra Paediatrics</a>
    </div>
  </div>
  <div class="ah-navbar"><div class="wrap ah-navrow">
    {nav(MENU, active, "ah-nav")}
    <div class="ah-loc"><button class="ah-loc-btn" aria-haspopup="true">Our Locations <span class="caret">▼</span></button><ul class="ah-loc-dd">{loc}</ul></div>
  </div></div>
</header>"""

def footer(active):
    links = "".join(f'<li><a href="{k}.html">{l}</a></li>' for k, l in [("index", "Home"), ("about", "About Us"), ("achievements", "Achievements"), ("specialities", "Specialities"),
        ("services", "Services"), ("doctors", "Doctors"), ("gallery", "Photos &amp; Videos"), ("careers", "Careers"), ("contact", "Contact Us")])
    locs = "".join(f'<li><a href="locations.html#l{i}">{l}</a></li>' for i, l in enumerate(LOCATIONS))
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIAL)
    return f"""<footer class="ah-foot">
  <div class="wrap ah-fgrid">
    <div><img class="ah-flogo" src="{A}uploads/logos/logo_new_(2)1.png" alt="Andhra Hospitals"><p>At Andhra Hospitals we recognise the value of every person and are guided by our commitment to excellence and leadership.</p><div class="ah-soc">{soc}</div></div>
    <div><h4>Quick Links</h4><ul>{links}</ul></div>
    <div><h4>Our Locations</h4><ul>{locs}</ul></div>
    <div><h4>Reach Us</h4><p>C.V.R. Complex, Prakasam Road,<br>Vijayawada – 2, Krishna Dist. (A.P.)</p><p><a href="mailto:info@andhrahospitals.org">info@andhrahospitals.org</a></p><p><a class="ah-fcall" href="tel:{TEL}">{PHONE}</a></p></div>
  </div>
  <div class="ah-legal"><div class="wrap"><span>© 2026 Andhra Hospitals. All rights reserved.</span><span>Terms &amp; Conditions · Disclaimer · Privacy Policy · Cancellation &amp; Refund</span></div></div>
</footer>
<a class="ah-float" href="contact.html#book">{ic("cal", 20)}Book Appointment</a>"""

def page_title(title, crumb, img=A + "uploads/banner_imgs/banner2.jpg"):
    return f'<section class="ah-ptitle" style="--bg:url(\'{img}\')"><div class="wrap"><h1>{title}</h1><p><a href="index.html">Home</a> / {crumb}</p></div></section>'

def book_form():
    return f"""<div class="ah-book"><h3>Book Appointment</h3>
{form("Appointment request", [("fn", "First name", "text", True, None), ("ln", "Last name", "text", False, None), ("em", "Email address", "email", False, None),
    ("ph", "Phone number", "tel", True, None), ("dt", "Booking date", "date", False, None), ("ms", "Message", "textarea", False, None)], "Book Appointment")}
<p class="ah-orcall">(Or) Call — <a href="tel:{TEL}">{PHONE}</a></p></div>"""

def charity_cards():
    return '<div class="ah-cards">' + "".join(
        f'<article class="ah-card reveal"><img src="{i}" alt="" loading="lazy"><div><h3>{t}</h3><p>{d}</p><a class="ah-red" href="about.html#charity">Read More</a></div></article>' for i, t, d in CHARITY) + "</div>"

def news_cards():
    return '<div class="ah-news">' + "".join(
        f'<article class="ah-post reveal"><img src="{i}" alt="" loading="lazy"><div><h3>{t}</h3><p>{d}</p></div></article>' for i, t, d in NEWS) + "</div>"

def videos(n=4):
    return '<div class="ah-vids">' + "".join(
        f'<button class="ah-vid" data-yt="{v}" aria-label="Play patient feedback video {k+1}"><img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" loading="lazy"><span class="ah-play">▶</span></button>' for k, v in enumerate(VIDEOS[:n])) + "</div>"

PAGES = {}
PAGES["index"] = ("Home", f"""
{slider([(A + "uploads/banner_imgs/banner2.jpg", "Andhra Hospitals buildings, Vijayawada"), (A + "uploads/banner_imgs/banner4.jpg", "Andhra Hospitals event"), (A + "uploads/banner_imgs/Untitled-3_copy.jpg", "Andhra Hospitals team")], "ah-slider")}
<section class="wrap ah-boxes">
  <a class="ah-box b1 reveal" href="about.html#courses"><span class="ah-bi">{ic("cap", 30)}</span><h3>Academic Courses</h3><p>Check out our academic courses.</p><span class="ah-bl">Click Here →</span></a>
  <a class="ah-box b2 reveal" href="achievements.html#certifications"><span class="ah-bi">{ic("shield", 30)}</span><h3>Certifications</h3><p>Click here to see our certifications.</p><span class="ah-bl">Know More →</span></a>
  <a class="ah-box b3 reveal" href="doctors.html"><span class="ah-bi">{ic("users", 30)}</span><h3>Find a Doctor</h3><p>Choose by location, speciality and doctor.</p><span class="ah-bl">Click Here →</span></a>
  <a class="ah-box b4 reveal" href="contact.html#book"><span class="ah-bi">{ic("heart", 30)}</span><h3>Packages</h3><p>Medical check-up packages for men &amp; women at Andhra Hospitals.</p><span class="ah-bl">Get Now →</span></a>
</section>
<section class="wrap ah-newsbar">{ticker("Latest News", [n[1] for n in NEWS] + ["24×7 Laboratory, Pharmacy &amp; ACLS Ambulance"])}</section>
<section class="ah-intro"><div class="wrap ah-introgrid">
  <div class="reveal"><h2 class="ah-h2">Andhra Hospital in Vijayawada</h2>
    <p>At Andhra Hospital we recognise the value of every person and are guided by our commitment to excellence and leadership. We demonstrate this by providing exemplary physical, emotional and spiritual care for each of our patients and their families, and by demonstrating social responsibility through the efficient use of our resources.</p>
    <p>The commitment of our staff, physicians and community partners to our mission permits us to maintain a quality of presence and tradition of caring. We offer an array of medical and surgical services including 24-hour urgent care backed by the latest technology.</p>
    <div class="ah-inside"><img src="http://andhrahospitals.org/img/seeinside.jpg" alt="Andhra Hospital building"><span>See Inside Hospital</span></div>
    <a class="ah-orange" href="about.html">About Andhra Hospital</a></div>
  <div class="reveal" id="book">{book_form()}</div>
</div></section>
<section class="ah-blueband"><div class="wrap"><h2 class="ah-h2 light center">Charity Works</h2>{charity_cards()}</div></section>
<section class="ah-soft"><div class="wrap"><p class="ah-kick">Recent Posts</p><h2 class="ah-h2 center">News &amp; Achievements</h2>{news_cards()}<p class="center"><a class="ah-orange" href="achievements.html">View All Posts</a></p></div></section>
<section class="ah-white"><div class="wrap"><p class="ah-kick left">What People Say</p><h2 class="ah-h2">Parents and Patients Feedback</h2>{videos(4)}</div></section>
<section class="ah-blueband"><div class="wrap"><p class="ah-kick light">General Information</p><h2 class="ah-h2 light center">Our Media</h2>
  <div class="ah-media"><div class="ah-mcol"><h3>Videos</h3>{videos(2)}<a class="ah-link" href="https://www.youtube.com/channel/UCctJa6-B6rdhOENJbhVKO5A" target="_blank" rel="noopener">View more on our YouTube channel →</a></div>
  <div class="ah-mcol"><h3>Photo Gallery</h3>{gallery(GALLERY, "ah-gal")}</div></div></div></section>
""")

PAGES["about"] = ("About Us", page_title("About Us", "About Us") + f"""
<section class="ah-white"><div class="wrap ah-introgrid">
  <div class="reveal"><h2 class="ah-h2">History of Andhra Hospitals</h2>
    <p>At Andhra Hospitals we recognise the value of every person and are guided by our commitment to excellence and leadership. We demonstrate this by providing exemplary physical, emotional and spiritual care for each of our patients and their families, and by demonstrating social responsibility through the efficient use of our resources.</p>
    <p>The commitment of our staff, physicians and community partners to our mission permits us to maintain a quality of presence and tradition of caring. We offer an array of medical and surgical services including 24-hour urgent care backed by the latest technology. We strive to create a compassionate environment where our employees can deliver the best care every hour of every day.</p></div>
  <div class="reveal ah-inside"><img src="{A}uploads/services/Untitled-3.jpg" alt="Andhra Hospitals ward"><span>Get Well Soon</span></div>
</div></section>
<section class="ah-blueband" id="charity"><div class="wrap"><h2 class="ah-h2 light center">Charity Works</h2>{charity_cards()}</div></section>
<section class="ah-soft" id="courses"><div class="wrap"><h2 class="ah-h2 center">Academic Courses</h2><p class="center ah-muted">Details of our academic and training courses — to be added from the hospital's course list.</p></div></section>""")

PAGES["achievements"] = ("Our Achievements", page_title("Our Achievements", "Our Achievements") + f"""
<section class="ah-soft"><div class="wrap"><p class="ah-kick">Recent Posts</p><h2 class="ah-h2 center">News &amp; Achievements</h2>{news_cards()}</div></section>
<section class="ah-white" id="certifications"><div class="wrap"><h2 class="ah-h2 center">Certifications</h2>
<div class="ah-certs"><div class="reveal"><img src="{A}uploads/logos/main13.png" alt=""><p>Accredited by the National Accreditation Board for Hospitals &amp; Healthcare Providers (NABH)</p></div>
<div class="reveal"><img src="{A}uploads/logos/nabh-black-new1235212.png" alt=""><p>Hospital laboratory accredited by the National Accreditation Board for Testing and Calibration Laboratories (NABL)</p></div></div></div></section>""")

PAGES["specialities"] = ("Specialities", page_title("Specialities", "Specialities", A + "uploads/services/Untitled-3.jpg") + f"""
<section class="ah-white"><div class="wrap"><h2 class="ah-h2 center">Our Specialities</h2><p class="center ah-muted">{len(SPECIALITIES)} specialities across our hospitals. Tap any to book a consultation.</p>
<div class="ah-list">{"".join(f'<a id="s{i}" class="ah-li reveal" href="contact.html#book"><span>{ic("heart", 18)}</span>{s}</a>' for i, s in enumerate(SPECIALITIES))}</div></div></section>""")

PAGES["services"] = ("Support Services", page_title("Support Services", "Support Services") + f"""
<section class="ah-soft"><div class="wrap"><h2 class="ah-h2 center">Our Services &amp; Facilities</h2>
<div class="ah-list">{"".join(f'<div id="v{i}" class="ah-li reveal"><span>{ic("check", 18)}</span>{s}</div>' for i, s in enumerate(SERVICES))}</div></div></section>""")

PAGES["doctors"] = ("Doctors", page_title("Find a Doctor", "Doctors") + f"""
<section class="ah-white"><div class="wrap ah-introgrid">
  <div class="reveal"><h2 class="ah-h2">Choose by location, speciality and doctor</h2><p>Tell us the speciality and the centre you prefer — our appointments desk will match you with the right doctor and confirm a time.</p>
  <div class="ah-list two">{"".join(f'<div class="ah-li"><span>{ic("pin", 18)}</span>{l}</div>' for l in LOCATIONS[:6])}</div></div>
  <div class="reveal">{book_form()}</div></div></section>""")

PAGES["gallery"] = ("Gallery", page_title("Gallery", "Gallery") + f"""
<section class="ah-white" id="photos"><div class="wrap"><h2 class="ah-h2 center">Photo Gallery</h2>{gallery(GALLERY, "ah-gal big")}</div></section>
<section class="ah-soft" id="videos"><div class="wrap"><h2 class="ah-h2 center">Parents and Patients Feedback</h2>{videos(8)}</div></section>""")

PAGES["careers"] = ("Careers", page_title("Careers", "Careers") + f"""
<section class="ah-white"><div class="wrap" style="max-width:820px"><h2 class="ah-h2">Join Andhra Hospitals</h2>
<p class="ah-muted">Current openings — to be added from the hospital's careers list. Meanwhile, send your resume and the role you're interested in to <a class="ah-link" href="mailto:info@andhrahospitals.org">info@andhrahospitals.org</a>.</p></div></section>""")

PAGES["locations"] = ("Our Locations", page_title("Our Locations", "Our Locations") + f"""
<section class="ah-soft"><div class="wrap"><h2 class="ah-h2 center">Andhra Hospitals across Andhra Pradesh</h2>
<div class="ah-locs">{"".join(f'<div id="l{i}" class="ah-locc reveal"><span>{ic("pin", 22)}</span><h3>{l}</h3><p>Address and phone to be confirmed with the hospital.</p></div>' for i, l in enumerate(LOCATIONS))}</div></div></section>""")

PAGES["contact"] = ("Contact Us", page_title("Contact Us", "Contact Us") + f"""
<section class="ah-intro"><div class="wrap ah-introgrid">
  <div class="reveal"><h2 class="ah-h2">Get in touch</h2>
    <div class="ah-reach"><p>{ic("pin", 20)}<span>C.V.R. Complex, Prakasam Road, Vijayawada – 2, Krishna Dist. (A.P.)</span></p>
    <p>{ic("mail", 20)}<a href="mailto:info@andhrahospitals.org">info@andhrahospitals.org</a></p>
    <p>{ic("phone", 20)}<a href="tel:{TEL}">{PHONE}</a></p></div>
    <a class="ah-orange" href="https://www.google.com/maps/search/?api=1&query=Andhra+Hospitals+Prakasam+Road+Vijayawada" target="_blank" rel="noopener">Get Directions</a>
    <p class="ah-muted" style="margin-top:18px">Hassle-free online appointment — our team will contact you within 24 hours.</p></div>
  <div class="reveal" id="book">{book_form()}</div></div></section>""")

CSS = r"""
:root{--ah-red:#e01020;--ah-blue:#0050a0;--ah-sky:#1e88e5;--ah-orange:#f26a2e;--ah-ink:#1d2433;--ah-muted:#5a6475;--ah-soft:#eaf3fc}
body{font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ah-ink);background:#fff;-webkit-font-smoothing:antialiased}
.wrap{max-width:1220px;margin:0 auto;padding:0 22px}
.center{text-align:center}
.ah-muted{color:var(--ah-muted)}
.ah-link{color:var(--ah-blue);font-weight:700}
/* header — logo, accreditations, paediatrics (as original) */
.ah-head{position:sticky;top:0;z-index:50;background:#fff;box-shadow:0 2px 16px rgba(0,40,90,.08)}
.ah-top{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:12px 22px}
.ah-logo img{height:58px;width:auto}
.ah-acc{display:flex;gap:26px;align-items:center}
.ah-acc img{height:46px;width:auto}
.ah-right{display:flex;align-items:center;gap:14px}
.ah-call{display:flex;align-items:center;gap:10px;color:var(--ah-red)}
.ah-call small{display:block;font-size:11px;color:var(--ah-muted);font-weight:600;letter-spacing:.04em;text-transform:uppercase}
.ah-call b{font-size:17px}
.ah-paed{border:2px solid var(--ah-red);color:var(--ah-red);border-radius:8px;padding:8px 14px;font-weight:700;font-size:14px;transition:.15s}
.ah-paed:hover{background:var(--ah-red);color:#fff}
.ah-navbar{border-top:1px solid #edf1f6}
.ah-navrow{display:flex;align-items:center;justify-content:space-between;gap:16px}
.ah-nav>ul>li>a{display:block;padding:14px 13px;font-weight:700;font-size:13.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--ah-ink);border-bottom:3px solid transparent}
.ah-nav>ul>li>a:hover,.ah-nav>ul>li>a[aria-current]{color:var(--ah-red);border-bottom-color:var(--ah-red)}
.ah-nav .dd{background:#fff;border-radius:0 0 12px 12px;box-shadow:0 18px 40px rgba(0,40,90,.16);padding:8px 0;max-height:70vh;overflow:auto;border-top:3px solid var(--ah-red)}
.ah-nav .dd a{padding:9px 18px;font-size:14px;color:var(--ah-ink)}
.ah-nav .dd a:hover{background:var(--ah-soft);color:var(--ah-blue)}
.ah-nav li:nth-child(3) .dd,.ah-nav li:nth-child(4) .dd{columns:2;min-width:520px}
.ah-loc{position:relative}
.ah-loc-btn{background:var(--ah-red);color:#fff;border:0;border-radius:999px;padding:9px 18px;font-weight:700;font-size:13px;letter-spacing:.04em;text-transform:uppercase;box-shadow:0 8px 20px -8px rgba(224,16,32,.6)}
.ah-loc-dd{position:absolute;right:0;top:calc(100% + 6px);list-style:none;background:#fff;border-radius:12px;box-shadow:0 18px 40px rgba(0,40,90,.16);padding:8px 0;min-width:240px;opacity:0;visibility:hidden;transition:.18s;z-index:60}
.ah-loc:hover .ah-loc-dd,.ah-loc:focus-within .ah-loc-dd{opacity:1;visibility:visible}
.ah-loc-dd a{display:block;padding:9px 18px;font-size:14px}
.ah-loc-dd a:hover{background:var(--ah-soft);color:var(--ah-blue)}
/* slider + colour boxes */
.ah-slider{height:min(42vw,560px);background:#dfe9f5}
.ah-slider .sl{height:100%}
.ah-slider .s-arr{background:rgba(255,255,255,.85);color:var(--ah-ink)}
.ah-boxes{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:-70px;position:relative;z-index:5}
.ah-box{border-radius:16px;padding:26px 24px;color:#fff;min-height:230px;display:flex;flex-direction:column;gap:10px;box-shadow:0 18px 40px -14px rgba(0,40,90,.45);position:relative;overflow:hidden;transition:transform .25s}
.ah-box::after{content:"";position:absolute;right:-40px;bottom:-40px;width:150px;height:150px;border-radius:50%;background:rgba(255,255,255,.12)}
.ah-box:hover{transform:translateY(-6px)}
.ah-box h3{font-size:19px;text-transform:uppercase;letter-spacing:.03em}
.ah-box p{opacity:.92;font-size:15px;flex:1}
.ah-bi{width:54px;height:54px;border-radius:14px;background:rgba(255,255,255,.18);display:grid;place-items:center}
.ah-bl{font-weight:800;font-size:13px;letter-spacing:.06em;text-transform:uppercase}
.b1{background:linear-gradient(135deg,#2563eb,#1e40af)}.b2{background:linear-gradient(135deg,#0ea5e9,#0369a1)}
.b3{background:linear-gradient(135deg,#3b82f6,#1d4ed8)}.b4{background:linear-gradient(135deg,#8b5cf6,#5b21b6)}
.ah-newsbar{margin-top:34px}
.ah-newsbar .tick{background:#fff;border-radius:12px;box-shadow:0 6px 22px rgba(0,40,90,.1);overflow:hidden}
.ah-newsbar .tk-lbl{background:var(--ah-red);color:#fff;padding:12px 18px;text-transform:uppercase;font-size:13px;letter-spacing:.05em}
.ah-newsbar .tk-track span{padding:12px 48px 12px 18px;font-weight:600;color:var(--ah-blue)}
/* sections */
.ah-intro{background:linear-gradient(180deg,#f2f8ff,#e6f1fc);padding:80px 0}
.ah-white{background:#fff;padding:80px 0}
.ah-soft{background:var(--ah-soft);padding:80px 0}
.ah-blueband{background:linear-gradient(135deg,#0b5cad,#0050a0 50%,#003f80);padding:80px 0}
.ah-h2{font-size:clamp(26px,3vw,36px);font-weight:800;text-transform:uppercase;letter-spacing:.02em;color:var(--ah-ink);margin-bottom:22px;line-height:1.2}
.ah-h2::after{content:"";display:block;width:70px;height:4px;border-radius:4px;background:var(--ah-red);margin-top:14px}
.ah-h2.center::after,.center .ah-h2::after{margin-left:auto;margin-right:auto}
.ah-h2.light{color:#fff}.ah-h2.light::after{background:#fff}
.ah-kick{text-align:center;color:var(--ah-muted);font-weight:700;font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:4px}
.ah-kick.left{text-align:left}.ah-kick.light{color:#cfe3ff}
.ah-introgrid{display:grid;grid-template-columns:1.25fr 1fr;gap:48px;align-items:start}
.ah-introgrid p{color:var(--ah-muted);margin-bottom:14px}
.ah-inside{position:relative;border-radius:16px;overflow:hidden;margin:22px 0;box-shadow:0 16px 40px -14px rgba(0,40,90,.4);max-width:520px}
.ah-inside img{width:100%;aspect-ratio:16/9;object-fit:cover}
.ah-inside span{position:absolute;left:16px;top:16px;background:var(--ah-red);color:#fff;font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:13px;padding:7px 12px;border-radius:8px}
.ah-orange{display:inline-block;background:var(--ah-orange);color:#fff;font-weight:800;text-transform:uppercase;letter-spacing:.05em;font-size:14px;padding:13px 22px;border-radius:10px;box-shadow:0 10px 24px -10px rgba(242,106,46,.7);transition:.15s}
.ah-orange:hover{background:#d9541b}
.ah-red{display:inline-block;background:var(--ah-red);color:#fff;font-weight:800;text-transform:uppercase;letter-spacing:.05em;font-size:13px;padding:10px 18px;border-radius:8px}
/* appointment box (blue with orange button, as original) */
.ah-book{background:linear-gradient(180deg,#1e88e5,#1565c0);border-radius:18px;padding:26px;color:#fff;box-shadow:0 24px 50px -20px rgba(0,60,140,.6)}
.ah-book h3{text-transform:uppercase;letter-spacing:.06em;font-size:18px;text-align:center;margin-bottom:16px}
.ah-book .enq{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.ah-book .fld{display:grid;gap:5px}
.ah-book .fld:nth-child(n+3){grid-column:1/-1}
.ah-book label{font-size:12.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#e3f0ff}
.ah-book input,.ah-book textarea,.ah-book select{font:inherit;font-size:15px;padding:11px 12px;border-radius:9px;border:0;background:rgba(255,255,255,.95);color:var(--ah-ink);width:100%}
.ah-book input:focus,.ah-book textarea:focus{outline:3px solid #ffd2bd}
.ah-book .enq-btn{grid-column:1/-1;border:0;border-radius:10px;padding:14px;background:var(--ah-orange);color:#fff;font-weight:800;text-transform:uppercase;letter-spacing:.06em}
.ah-orcall{text-align:center;margin-top:14px;font-size:20px;font-weight:800}
.ah-orcall a{color:#fff}
/* cards */
.ah-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.ah-card{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 16px 40px -18px rgba(0,0,0,.45);display:flex;flex-direction:column;transition:transform .25s}
.ah-card:hover{transform:translateY(-6px)}
.ah-card img{width:100%;aspect-ratio:16/9;object-fit:cover}
.ah-card>div{padding:20px;display:flex;flex-direction:column;gap:10px;flex:1}
.ah-card h3{font-size:16px;text-transform:uppercase;letter-spacing:.02em}
.ah-card p{color:var(--ah-muted);font-size:14.5px;flex:1}
.ah-card .ah-red{align-self:flex-start}
.ah-news{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin:10px 0 30px}
.ah-post{display:grid;grid-template-columns:200px 1fr;gap:20px;background:#fff;border-radius:16px;padding:16px;box-shadow:0 10px 30px -16px rgba(0,40,90,.35)}
.ah-post img{width:100%;height:150px;object-fit:cover;border-radius:12px}
.ah-post h3{font-size:16px;text-transform:uppercase;color:var(--ah-ink);margin-bottom:8px}
.ah-post p{color:var(--ah-muted);font-size:14.5px}
.ah-vids{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:10px}
.ah-vid{position:relative;border:0;padding:0;border-radius:14px;overflow:hidden;aspect-ratio:16/9;background:#000;box-shadow:0 10px 26px -14px rgba(0,0,0,.6)}
.ah-vid img{width:100%;height:100%;object-fit:cover;opacity:.85}
.ah-vid iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.ah-play{position:absolute;inset:0;margin:auto;width:56px;height:40px;border-radius:12px;background:var(--ah-red);color:#fff;display:grid;place-items:center;font-size:18px}
.ah-media{display:grid;grid-template-columns:1fr 1fr;gap:24px;background:#fff;border-radius:18px;padding:28px}
.ah-mcol h3{text-transform:uppercase;font-size:20px;margin-bottom:14px}
.ah-media .ah-vids{grid-template-columns:1fr 1fr}
.ah-media .ah-link{display:inline-block;margin-top:14px}
.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.gal.big{grid-template-columns:repeat(3,1fr);gap:14px}
.gi{border:0;padding:0;border-radius:10px;overflow:hidden;aspect-ratio:4/3;background:#eef3f9;cursor:zoom-in}
.gi img{width:100%;height:100%;object-fit:cover;transition:transform .4s}
.gi:hover img{transform:scale(1.06)}
/* inner pages */
.ah-ptitle{position:relative;padding:70px 0;color:#fff;overflow:hidden;background:var(--ah-blue)}
.ah-ptitle::before{content:"";position:absolute;inset:0;background:var(--bg) center/cover;opacity:.25}
.ah-ptitle .wrap{position:relative}
.ah-ptitle h1{font-size:clamp(28px,4vw,44px);text-transform:uppercase;letter-spacing:.03em}
.ah-ptitle p{opacity:.9;margin-top:6px}
.ah-ptitle a{text-decoration:underline}
.ah-list{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:26px}
.ah-list.two{grid-template-columns:1fr 1fr}
.ah-li{display:flex;align-items:center;gap:12px;background:#fff;border-radius:12px;padding:14px 16px;font-weight:600;box-shadow:0 6px 20px -12px rgba(0,40,90,.35);border-left:4px solid var(--ah-red);transition:.2s}
a.ah-li:hover{transform:translateX(4px);border-left-color:var(--ah-blue)}
.ah-li span{color:var(--ah-red);display:grid}
.ah-certs{display:grid;grid-template-columns:1fr 1fr;gap:22px;max-width:820px;margin:20px auto 0}
.ah-certs>div{background:#fff;border-radius:16px;padding:24px;text-align:center;box-shadow:0 10px 30px -16px rgba(0,40,90,.35)}
.ah-certs img{height:60px;margin:0 auto 12px}
.ah-locs{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:20px}
.ah-locc{background:#fff;border-radius:16px;padding:22px;box-shadow:0 10px 30px -16px rgba(0,40,90,.35);border-top:4px solid var(--ah-red)}
.ah-locc span{color:var(--ah-red)}
.ah-locc h3{margin:8px 0 6px;text-transform:uppercase;font-size:16px}
.ah-locc p{color:var(--ah-muted);font-size:14px}
.ah-reach p{display:flex;gap:12px;align-items:flex-start;color:var(--ah-ink);font-size:17px}
.ah-reach svg{color:var(--ah-red);flex:0 0 auto;margin-top:3px}
/* footer */
.ah-foot{background:#0b1f3a;color:#c3cede;padding-top:60px;font-size:15px}
.ah-fgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.2fr;gap:34px;padding-bottom:40px}
.ah-flogo{height:52px;background:#fff;border-radius:10px;padding:6px 10px;margin-bottom:14px}
.ah-foot h4{color:#fff;text-transform:uppercase;letter-spacing:.06em;font-size:14px;margin-bottom:14px}
.ah-foot ul{list-style:none;display:grid;gap:7px}
.ah-foot a:hover{color:#fff}
.ah-foot p{margin-bottom:10px}
.ah-fcall{color:#fff;font-size:22px;font-weight:800}
.ah-soc{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}
.ah-soc a{background:rgba(255,255,255,.08);padding:7px 12px;border-radius:8px;font-size:13px}
.ah-legal{border-top:1px solid rgba(255,255,255,.1);padding:16px 0;font-size:13px;color:#8d9ab0}
.ah-legal .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.ah-float{position:fixed;right:20px;bottom:20px;z-index:45;display:flex;gap:8px;align-items:center;background:var(--ah-orange);color:#fff;font-weight:800;padding:12px 18px;border-radius:999px;box-shadow:0 14px 30px -8px rgba(242,106,46,.7);text-transform:uppercase;font-size:13px;letter-spacing:.04em}
@media (max-width:1100px){.ah-acc{display:none}.ah-nav>ul>li>a{padding:14px 9px;font-size:12.5px}}
@media (max-width:980px){
  .ah-navrow{padding:6px 22px}
  .ah-nav>ul{background:#fff;box-shadow:0 18px 40px rgba(0,40,90,.16);padding:6px 0}
  .ah-nav>ul>li>a{border-bottom:1px solid #eef2f7;padding:13px 22px}
  .ah-nav .dd{box-shadow:none;border-top:0;columns:1 !important;min-width:0 !important;background:#f6f9fd;border-radius:0}
  .ah-boxes{grid-template-columns:1fr 1fr;margin-top:20px}
  .ah-introgrid{grid-template-columns:1fr}
  .ah-cards{grid-template-columns:1fr 1fr}.ah-news{grid-template-columns:1fr}.ah-vids{grid-template-columns:1fr 1fr}
  .ah-media{grid-template-columns:1fr}.ah-list{grid-template-columns:1fr 1fr}.ah-locs{grid-template-columns:1fr 1fr}
  .ah-fgrid{grid-template-columns:1fr 1fr}
}
@media (max-width:640px){
  .ah-top{padding:10px 16px}.ah-logo img{height:44px}.ah-call small{display:none}.ah-paed{display:none}
  .ah-boxes,.ah-cards,.ah-list,.ah-list.two,.ah-locs,.ah-certs,.ah-fgrid{grid-template-columns:1fr}
  .ah-box{min-height:0}.ah-post{grid-template-columns:1fr}
  .ah-book .enq{grid-template-columns:1fr}.ah-book .fld:nth-child(2){grid-column:auto}
  .ah-slider{height:220px}.ah-loc-btn{padding:8px 12px;font-size:12px}
  .ah-float{right:12px;bottom:12px;padding:10px 14px}
}
"""

if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    for f in ["about.html", "specialities.html", "services.html", "locations.html", "contact.html", "index.html", "achievements.html", "doctors.html", "gallery.html", "careers.html"]:
        (out / f).unlink(missing_ok=True)
    write_site(out, S, PAGES, CSS, header, footer)
