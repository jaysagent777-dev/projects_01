# -*- coding: utf-8 -*-
"""Atkinson Senior Secondary School (atkinsonvijayawada.edu.in) — redesign preview that KEEPS the original layout:
dark contact bar, the school's own maroon crest header, maroon dropdown menu, photo slider, Flash News ticker,
Welcome, Latest News with dates, Thought for the Day, footer — modernised, responsive and working. Build: python3 site.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_template"))
from classic import *  # noqa

U = "https://atkinsonvijayawada.edu.in/wp-content/uploads/"
HEADER_IMG = U + "2023/08/Banner-29-06.png"
CAMPUS = U + "2024/05/School-Photo-scaled.jpg"
CAMPUS2 = U + "2024/05/School-Photo-1-scaled-e1717133525900.jpg"
S = {"name": "Atkinson Senior Secondary School", "domain": "atkinsonvijayawada.edu.in", "desk": "school office",
     "description": "Atkinson Senior Secondary School, Vijayawada — a CBSE school run by the Sisters of St. Ann of Providence since 1899."}
PHONE, TEL, EMAIL = "0866 2565790", "+918662565790", "atkinsonvjy@gmail.com"

NEWS = [("15 May 2026", "CBSE — Second Board Exam", "academics.html#results"),
        ("13 May 2026", "Class XII results declared — centum results", "academics.html#results"),
        ("15 Apr 2026", "Class X results declared — centum results", "academics.html#results"),
        ("2026 – 2027", "Admissions open — Pre-KG to UKG co-education, Classes I to VIII for girls", "admission.html")]

MENU = [
    ("index", "Home", None),
    ("about", "About Us", [("about.html", "About Us"), ("about.html#history", "History of Atkinson"), ("about.html#mission", "Our Mission &amp; Vision"), ("about.html#founders", "Our Founders")]),
    ("management", "Management", [("management.html", "School Management"), ("management.html#pta", "PTA")]),
    ("academics", "Academics", [("academics.html", "Academic Facilities"), ("academics.html#info", "School Info"), ("academics.html#results", "Results"), ("academics.html#parents", "Guidelines to the Parents"), ("academics.html#activities", "Co-Curricular Activities")]),
    ("admission", "Students", [("admission.html", "Admission"), ("admission.html#fees", "Fees Schedule"), ("admission.html#tc", "Application for TC")]),
    ("disclosure", "Mandatory Public Disclosure", None),
    ("gallery", "Gallery", None),
    ("contact", "Contact Us", None),
]

def header(active):
    return f"""<div class="ak-topbar"><div class="wrap">
  <span><a href="tel:{TEL}">{ic("phone", 15)} {PHONE}</a><a href="mailto:{EMAIL}">{ic("mail", 15)} {EMAIL}</a></span>
  <a class="ak-adm" href="admission.html">Admissions 2026–27 →</a>
</div></div>
<header class="ak-head">
  <a class="ak-banner" href="index.html"><img src="{HEADER_IMG}" alt="Atkinson Senior Secondary School — Affiliated to CBSE, Delhi — Convent Street, Vijayawada, Andhra Pradesh 520001"></a>
  <div class="ak-navbar"><div class="wrap">{nav(MENU, active, "ak-nav")}</div></div>
</header>"""

def footer(active):
    q = "".join(f'<li><a href="{k}.html">{l}</a></li>' for k, l in [("index", "Home"), ("about", "About Us"), ("academics", "Academics"), ("gallery", "Gallery"), ("admission", "Students"), ("contact", "Contact Us")])
    return f"""<footer class="ak-foot"><div class="wrap ak-fgrid">
  <div><h4>Atkinson Senior Secondary School</h4><p>Run by the Sisters of St. Ann of Providence. Educating young people of character, excellence and service in Vijayawada since 1899.</p></div>
  <div><h4>Quick links</h4><ul>{q}</ul></div>
  <div><h4>Address</h4><p>Convent Street, near Railway Station Road,<br>Vijayawada, Andhra Pradesh 520001</p><p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
</div><div class="ak-copy"><div class="wrap">Copyright © 2026 Atkinson Senior Secondary School, Vijayawada</div></div></footer>
<a class="ak-float" href="admission.html#enquire">{ic("cap", 18)} Admission enquiry</a>"""

def page_title(title, crumb):
    return f'<section class="ak-ptitle"><div class="wrap"><h1>{title}</h1><p><a href="index.html">Home</a> / {crumb}</p></div></section>'

def news_list(items=NEWS):
    return '<ul class="ak-news">' + "".join(f'<li class="reveal"><span class="ak-date">{d}</span><a href="{h}">{t}</a></li>' for d, t, h in items) + "</ul>"

WELCOME = ("In June 1899, the Sisters of St. Ann — Mother Angela, Sr. Hyacinth and Sr. St. Charles — started a primary school of 16 pupils up to Class I, "
           "with help from the Honourable Mr. Atkinson, the then Collector of Krishna District. For this purpose they established their convent in Bezwada (Vijayawada) at the behest of the Bishop of Hyderabad.")

PAGES = {}
PAGES["index"] = ("Home", f"""
{slider([(CAMPUS, "Atkinson Senior Secondary School campus"), (CAMPUS2, "Atkinson school buildings")], "ak-slider")}
<section class="wrap ak-flash">{ticker("Flash News", ["ADMISSIONS OPEN! 2026 – 2027 — Welcome to our school", "Class XII results declared on 13/05/2026 — centum results", "Class X results declared on 15/04/2026 — centum results"])}</section>
<section class="wrap ak-home">
  <div class="ak-welcome reveal">
    <h2 class="ak-h2">Welcome to Atkinson Senior Secondary School</h2>
    <div class="ak-wgrid"><img src="{CAMPUS2}" alt="Atkinson school"><div><p>{WELCOME}</p><p>Within a year the strength grew to 56, and the first inspection was held in 1900. Today Atkinson is home to 4,331 students and 127 staff members.</p><a class="ak-btn" href="about.html#history">Read more</a></div></div>
  </div>
  <aside class="ak-side">
    <div class="ak-panel reveal"><h3>Latest News</h3>{news_list()}<a class="ak-more" href="academics.html#results">View more →</a></div>
    <div class="ak-thought reveal"><h3>Thought for the Day</h3><blockquote>"Beginnings are happy never-endings as long as you remember where you started from."</blockquote></div>
  </aside>
</section>
<section class="ak-band"><div class="wrap ak-mgmt">
  <div class="reveal"><h2 class="ak-h2 light">Management</h2><p>Atkinson is run by the <b>Sisters of St. Ann of Providence</b>, who dedicate themselves to the education of children and youth — with special preference for the poor and the marginalised — imparting quality education and human values so students become instruments of social change.</p><a class="ak-btn gold" href="management.html">School management</a></div>
  <div class="ak-stats">
    <div class="reveal"><b>1899</b><span>Founded</span></div><div class="reveal"><b>4,331</b><span>Students</span></div>
    <div class="reveal"><b>127</b><span>Staff</span></div><div class="reveal"><b>100%</b><span>Board results</span></div>
  </div>
</div></section>
<section class="wrap ak-events"><h2 class="ak-h2 center">Latest Events Gallery</h2>{gallery([CAMPUS, CAMPUS2], "ak-gal")}<p class="center"><a class="ak-btn" href="gallery.html">View gallery</a></p></section>
""")

PAGES["about"] = ("About Us", page_title("About Us", "About Us") + f"""
<section class="wrap ak-page" id="history"><h2 class="ak-h2">The History of Atkinson Senior Secondary School</h2>
<div class="ak-wgrid"><img src="{CAMPUS2}" alt=""><div><p>{WELCOME}</p>
<p>Due to their dedicated labour, within a year the student strength swelled to 56, and the first inspection took place in 1900. A boarding was opened for out-station students and new classrooms were built. Within four years, Atkinson was raised to Middle School and then Secondary School status. It was a co-education school, and students sat the Madras Board Anglo-Indian High School Examination.</p>
<p>After 50 years the staff had grown to 15 and the students to 500 — and to 800 after 75 years. In the last 45 years progress has been rapid: the student strength has soared to 4,331, with 127 staff members. Sr. Stella D'Souza took over the school in 1982, acquired land and constructed six massive buildings.</p></div></div></section>
<section class="ak-soft" id="mission"><div class="wrap ak-two">
  <div class="ak-card reveal"><h3>Vision Statement</h3><p>"We the Sisters of St. Ann of Providence in India, challenged by the life and mission of Jesus Christ, who is the incarnation of the compassionate love of the Father, re-dedicate ourselves with a creative fidelity towards the education of children and youth, with special preference to the poor and the marginalised, to liberate and empower them by imparting quality education, instilling in them human values, and thus enabling them to become instruments of 'Social Change'."</p></div>
  <div class="ak-card reveal"><h3>Mission Statement</h3><p>To form the little ones, youth and marginalised into women and men of character, who will distinguish themselves by their academic and professional excellence, sound human values of love, peace and brotherhood/sisterhood, and holistic growth in their intellectual, emotional, physical and aesthetic abilities — with a spirit of selfless service and leadership.</p></div>
</div></section>
<section class="wrap ak-page" id="founders"><h2 class="ak-h2">Our Founders</h2>
<p>The Sisters of St. Ann of Providence carry forward the intention of their founders, <b>Marquis Carlo Tancredi</b> and <b>Marchioness Giulia Di Barolo</b>. Atkinson itself was begun in 1899 by <b>Mother Angela, Sr. Hyacinth and Sr. St. Charles</b>.</p></section>""")

PAGES["management"] = ("Management", page_title("School Management", "Management") + f"""
<section class="wrap ak-page"><h2 class="ak-h2">Sisters of St. Ann of Providence</h2>
<p>Atkinson Senior Secondary School is managed by the Sisters of St. Ann of Providence, who have guided the school since its founding in 1899.</p>
<p class="ak-note">Names and messages of the Correspondent, Principal and management committee — to be added from the school.</p>
<h2 class="ak-h2" id="pta">Parent Teacher Association</h2><p class="ak-note">PTA members and activities — to be added from the school.</p></section>""")

PAGES["academics"] = ("Academics", page_title("Academics", "Academics") + f"""
<section class="wrap ak-page"><h2 class="ak-h2">Academic Facilities</h2>
<div class="ak-three">
  <div class="ak-card reveal"><h3>Pre-KG to UKG</h3><p>Co-educational early years. Admission to LKG at age 3 (by June).</p></div>
  <div class="ak-card reveal"><h3>Classes I – VIII</h3><p>A girls' school with a strong foundation across all subjects.</p></div>
  <div class="ak-card reveal"><h3>Secondary &amp; Senior Secondary</h3><p>Affiliated to CBSE, Delhi, with centum results in Classes X and XII.</p></div>
</div></section>
<section class="ak-soft" id="results"><div class="wrap ak-page"><h2 class="ak-h2">Results &amp; Notices</h2>{news_list(NEWS[:3] + [("01 Jun 2024", "CBSE — Improvement / Supplementary notice", "academics.html#results")])}</div></section>
<section class="wrap ak-page" id="info"><h2 class="ak-h2">School Info</h2><p>Address: Convent Street, near Railway Station Road, Vijayawada, Andhra Pradesh 520001 · Phone: {PHONE} · Email: {EMAIL}</p>
<h2 class="ak-h2" id="parents">Guidelines to the Parents</h2><p class="ak-note">Guidelines — to be added from the school's handbook.</p>
<h2 class="ak-h2" id="activities">Co-Curricular Activities</h2><p>Holistic growth — intellectual, emotional, physical and aesthetic — is at the heart of our mission. <span class="ak-note">Activity list to be added from the school.</span></p></section>""")

PAGES["admission"] = ("Admission", page_title("Admission", "Students / Admission") + f"""
<section class="wrap ak-page ak-adm-grid">
  <div><h2 class="ak-h2">Admissions Open 2026 – 2027</h2>
  <p><b>Pre-KG to UKG — co-education · Classes I to VIII — only for girls</b></p>
  <p>Every child seeking admission must be introduced in person to the Principal by the parents. Registration forms should be filled in and submitted with the following documents — incomplete forms will be rejected. The age for admission to L.K.G. is 3 years (by June).</p>
  <ul class="ak-ticks"><li>Photocopy of the Birth Certificate from the Municipality, and Baptismal Certificate for Catholics</li><li>Copy of Aadhaar card</li><li>A self-addressed stamped envelope for a reply</li></ul>
  <p>Candidates for higher classes will be tested and admitted to the class for which they are found fit, with a transfer certificate from the school last attended. Students from other states must have the transfer certificate counter-signed by their state's Education Department. Admission is entirely at the discretion of the Principal.</p>
  <h2 class="ak-h2" id="fees">Fees Schedule</h2>
  <div class="ak-fees"><div><b>Term I</b><span>before 15 July</span></div><div><b>Term II</b><span>before 1 November</span></div><div><b>Term III</b><span>before 1 March</span></div></div>
  <p class="ak-note">Admission and term fees are paid at the time of admission. Fees are collected Monday to Saturday, 8.30 – 11.30 a.m.; a fine is levied after the due date.</p>
  <h2 class="ak-h2" id="tc">Application for TC</h2><p>Parents may apply for a Transfer Certificate at the school office.</p></div>
  <div id="enquire"><div class="ak-formbox"><h3>Admission enquiry</h3>
  {form("Admission enquiry", [("cn", "Child's name", "text", True, None), ("cl", "Class applying for", "select", True, ["Pre-KG", "LKG", "UKG"] + [f"Class {n}" for n in range(1, 9)]),
      ("pn", "Parent's name", "text", True, None), ("pm", "Parent's mobile", "tel", True, None), ("ms", "Message", "textarea", False, None)], "Send on WhatsApp")}</div></div>
</section>""")

PAGES["disclosure"] = ("Mandatory Public Disclosure", page_title("Mandatory Public Disclosure", "Mandatory Public Disclosure") + """
<section class="wrap ak-page"><h2 class="ak-h2">As required by CBSE</h2>
<div class="ak-disc">""" + "".join(f'<div class="reveal"><b>{t}</b><span>Document to be uploaded</span></div>' for t in [
    "General information", "Documents and information (affiliation, recognition, NOC)", "Results and academics", "Staff (teaching)", "School infrastructure", "Fee structure", "Annual academic calendar", "School Management Committee", "Parent Teacher Association"]) + "</div></section>")

PAGES["gallery"] = ("Gallery", page_title("Photo Gallery", "Gallery") + f"""
<section class="wrap ak-page">{gallery([CAMPUS, CAMPUS2], "ak-gal big")}<p class="ak-note center">Event albums — to be added from the school's photo library.</p></section>""")

PAGES["contact"] = ("Contact Us", page_title("Contact Us", "Contact Us") + f"""
<section class="wrap ak-page ak-adm-grid">
  <div><h2 class="ak-h2">Get in touch</h2>
  <div class="ak-contact"><p>{ic("pin", 20)}<span>Convent Street, near Railway Station Road, Vijayawada, Andhra Pradesh 520001</span></p>
  <p>{ic("phone", 20)}<a href="tel:{TEL}">{PHONE}</a></p><p>{ic("mail", 20)}<a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p>{ic("clock", 20)}<span>Office &amp; fee counter: Monday – Saturday, 8.30 – 11.30 a.m.</span></p></div>
  <a class="ak-btn" href="https://www.google.com/maps/search/?api=1&query=Atkinson+Senior+Secondary+School+Convent+Street+Vijayawada" target="_blank" rel="noopener">Get directions</a></div>
  <div><div class="ak-formbox"><h3>Send a message</h3>{form("Message to the school", [("nm", "Your name", "text", True, None), ("ph", "Mobile", "tel", True, None), ("ms", "Message", "textarea", True, None)], "Send on WhatsApp")}</div></div>
</section>""")

CSS = r"""
:root{--ak-maroon:#7a1b2d;--ak-deep:#4a0f1c;--ak-dark:#2a0a12;--ak-gold:#e3b23c;--ak-ink:#2a2226;--ak-muted:#66595e;--ak-cream:#fbf6ef}
body{font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ak-ink);background:#fff;-webkit-font-smoothing:antialiased}
.wrap{max-width:1200px;margin:0 auto;padding:0 22px}
.center{text-align:center}
/* dark contact bar, crest header, maroon menu (as original) */
.ak-topbar{background:var(--ak-dark);color:#f1dfc4;font-size:14px}
.ak-topbar .wrap{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:8px 22px;flex-wrap:wrap}
.ak-topbar span{display:flex;gap:20px;flex-wrap:wrap}
.ak-topbar a{display:inline-flex;align-items:center;gap:6px}
.ak-topbar a:hover{color:#fff}
.ak-adm{background:var(--ak-gold);color:var(--ak-dark) !important;font-weight:800;padding:4px 12px;border-radius:999px;font-size:13px}
.ak-head{position:sticky;top:0;z-index:50;box-shadow:0 6px 24px rgba(42,10,18,.25)}
.ak-banner{display:block;background:linear-gradient(90deg,#7a1b2d,#5c1322)}
.ak-banner img{width:100%;max-height:150px;object-fit:cover;object-position:center}
.ak-navbar{background:linear-gradient(180deg,#2d0b14,#1f070e);border-top:2px solid var(--ak-gold)}
.ak-nav>ul{justify-content:center;flex-wrap:wrap}
.ak-nav>ul>li>a{display:block;padding:12px 13px;color:#f4e6d2;font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.ak-nav>ul>li>a:hover,.ak-nav>ul>li>a[aria-current]{color:var(--ak-gold);background:rgba(255,255,255,.05)}
.ak-nav>ul>li>a[aria-current]{box-shadow:inset 0 -3px 0 var(--ak-gold)}
.ak-nav .dd{background:#fff;border-top:3px solid var(--ak-gold);border-radius:0 0 10px 10px;box-shadow:0 18px 40px rgba(42,10,18,.25);padding:6px 0}
.ak-nav .dd a{padding:9px 18px;font-size:14px;color:var(--ak-ink)}
.ak-nav .dd a:hover{background:var(--ak-cream);color:var(--ak-maroon)}
.ak-nav .burger{color:#f4e6d2}
/* slider + flash news */
.ak-slider{height:min(36vw,480px);background:#e9e1d6}
.ak-slider .sl{height:100%}
.ak-slider .s-arr{background:rgba(122,27,45,.85);color:#fff}
.ak-flash{margin-top:22px}
.ak-flash .tick{border-radius:10px;overflow:hidden;box-shadow:0 8px 24px -10px rgba(42,10,18,.35);background:#fff}
.ak-flash .tk-lbl{background:var(--ak-maroon);color:#fff;padding:11px 18px;text-transform:uppercase;font-size:13px;letter-spacing:.06em;position:relative}
.ak-flash .tk-lbl::after{content:"";position:absolute;right:-10px;top:0;bottom:0;border-left:10px solid var(--ak-maroon);border-top:21px solid transparent;border-bottom:21px solid transparent}
.ak-flash .tk-track span{padding:11px 48px 11px 22px;font-weight:700;color:var(--ak-maroon)}
/* home: welcome + latest news + thought */
.ak-home{display:grid;grid-template-columns:1.6fr 1fr;gap:30px;padding-top:44px;padding-bottom:56px}
.ak-h2{font-size:clamp(23px,2.6vw,30px);color:var(--ak-maroon);font-weight:800;margin-bottom:16px;line-height:1.25}
.ak-h2::after{content:"";display:block;width:64px;height:3px;background:var(--ak-gold);margin-top:10px;border-radius:3px}
.ak-h2.center::after{margin-left:auto;margin-right:auto}
.ak-h2.light{color:#fff}
.ak-wgrid{display:grid;grid-template-columns:260px 1fr;gap:22px;align-items:start}
.ak-wgrid img{width:100%;border-radius:12px;box-shadow:0 14px 30px -14px rgba(42,10,18,.5);aspect-ratio:4/3;object-fit:cover}
.ak-wgrid p,.ak-page p{color:#4a3f43;margin-bottom:12px}
.ak-btn{display:inline-block;background:var(--ak-maroon);color:#fff;font-weight:700;padding:10px 20px;border-radius:8px;font-size:14px;transition:.15s}
.ak-btn:hover{background:var(--ak-deep)}
.ak-btn.gold{background:var(--ak-gold);color:var(--ak-dark)}
.ak-side{display:grid;gap:18px;align-content:start}
.ak-panel{background:#fff;border-radius:14px;box-shadow:0 12px 32px -16px rgba(42,10,18,.4);overflow:hidden}
.ak-panel h3,.ak-thought h3{background:var(--ak-maroon);color:#fff;font-size:15px;letter-spacing:.06em;text-transform:uppercase;padding:12px 18px}
.ak-news{list-style:none}
.ak-panel .ak-news{padding:6px 18px}
.ak-news li{display:grid;gap:2px;padding:12px 0;border-bottom:1px dashed #e6d9cc}
.ak-news li:last-child{border-bottom:0}
.ak-date{font-size:12.5px;font-weight:800;color:#a0742a;letter-spacing:.03em}
.ak-news a{font-weight:600;color:var(--ak-ink)}
.ak-news a:hover{color:var(--ak-maroon)}
.ak-more{display:block;text-align:right;padding:0 18px 14px;font-weight:700;color:var(--ak-maroon);font-size:14px}
.ak-thought{border-radius:14px;overflow:hidden;background:var(--ak-cream);box-shadow:0 12px 32px -16px rgba(42,10,18,.4)}
.ak-thought h3{background:var(--ak-gold);color:var(--ak-dark)}
.ak-thought blockquote{padding:18px;font-family:Georgia,serif;font-style:italic;font-size:18px;color:var(--ak-deep);line-height:1.5}
/* management band + stats */
.ak-band{background:linear-gradient(135deg,#7a1b2d,#4a0f1c);color:#f6e8d6;padding:60px 0}
.ak-mgmt{display:grid;grid-template-columns:1.2fr 1fr;gap:36px;align-items:center}
.ak-mgmt p{margin-bottom:16px;color:#f1dcc6}
.ak-stats{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.ak-stats div{background:rgba(255,255,255,.08);border:1px solid rgba(227,178,60,.35);border-radius:14px;padding:18px;text-align:center}
.ak-stats b{display:block;font-size:30px;color:var(--ak-gold)}
.ak-stats span{font-size:14px}
.ak-events{padding-top:56px;padding-bottom:56px}
.gal{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:22px}
.gi{border:0;padding:0;border-radius:12px;overflow:hidden;aspect-ratio:16/9;cursor:zoom-in;box-shadow:0 12px 28px -14px rgba(42,10,18,.5)}
.gi img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.gi:hover img{transform:scale(1.04)}
/* inner pages */
.ak-ptitle{background:linear-gradient(135deg,#7a1b2d,#4a0f1c);color:#fff;padding:46px 0;border-bottom:3px solid var(--ak-gold)}
.ak-ptitle h1{font-size:clamp(26px,3.6vw,38px)}
.ak-ptitle p{opacity:.85}
.ak-ptitle a{text-decoration:underline}
.ak-page{padding-top:44px;padding-bottom:44px}
.ak-page .ak-h2:not(:first-child){margin-top:30px}
.ak-soft{background:var(--ak-cream)}
.ak-two{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding-top:44px;padding-bottom:44px}
.ak-three{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.ak-card{background:#fff;border-radius:14px;padding:22px;box-shadow:0 12px 30px -16px rgba(42,10,18,.4);border-top:4px solid var(--ak-maroon)}
.ak-card h3{color:var(--ak-maroon);margin-bottom:8px}
.ak-card p{color:#4a3f43}
.ak-note{color:#9a7d5a !important;font-style:italic;font-size:14.5px}
.ak-ticks{list-style:none;display:grid;gap:8px;margin:6px 0 16px}
.ak-ticks li{padding-left:28px;position:relative}
.ak-ticks li::before{content:"✓";position:absolute;left:0;top:2px;width:20px;height:20px;border-radius:50%;background:var(--ak-cream);color:var(--ak-maroon);font-weight:800;font-size:12px;display:grid;place-items:center}
.ak-adm-grid{display:grid;grid-template-columns:1.4fr 1fr;gap:34px;align-items:start}
.ak-fees{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:12px}
.ak-fees div{background:var(--ak-cream);border-radius:12px;padding:14px;text-align:center;border:1px solid #eadcc7}
.ak-fees b{display:block;color:var(--ak-maroon)}
.ak-fees span{font-size:14px;color:var(--ak-muted)}
.ak-formbox{background:#fff;border-radius:16px;box-shadow:0 18px 40px -18px rgba(42,10,18,.45);overflow:hidden;position:sticky;top:240px}
.ak-formbox h3{background:var(--ak-maroon);color:#fff;padding:14px 20px;font-size:16px;letter-spacing:.04em;text-transform:uppercase}
.ak-formbox .enq{display:grid;gap:12px;padding:20px}
.ak-formbox .fld{display:grid;gap:4px}
.ak-formbox label{font-size:13px;font-weight:700;color:var(--ak-deep)}
.ak-formbox input,.ak-formbox select,.ak-formbox textarea{font:inherit;font-size:15px;padding:10px 12px;border:1px solid #e0d2c0;border-radius:8px;width:100%;background:#fff}
.ak-formbox input:focus,.ak-formbox select:focus,.ak-formbox textarea:focus{outline:none;border-color:var(--ak-maroon);box-shadow:0 0 0 3px rgba(122,27,45,.15)}
.ak-formbox .enq-btn{border:0;border-radius:8px;padding:12px;background:var(--ak-gold);color:var(--ak-dark);font-weight:800}
.ak-disc{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.ak-disc div{background:#fff;border-radius:12px;padding:16px;box-shadow:0 8px 24px -14px rgba(42,10,18,.4);border-left:4px solid var(--ak-gold);display:grid;gap:4px}
.ak-disc span{font-size:13px;color:#9a7d5a;font-style:italic}
.ak-contact p{display:flex;gap:12px;align-items:flex-start;font-size:16.5px}
.ak-contact svg{color:var(--ak-maroon);flex:0 0 auto;margin-top:4px}
.ak-contact a{color:var(--ak-maroon);font-weight:700}
/* footer */
.ak-foot{background:var(--ak-dark);color:#d9c6ad;padding-top:44px;font-size:15px;border-top:4px solid var(--ak-gold)}
.ak-fgrid{display:grid;grid-template-columns:1.4fr 1fr 1.2fr;gap:30px;padding-bottom:30px}
.ak-foot h4{color:var(--ak-gold);font-size:15px;margin-bottom:10px;letter-spacing:.03em}
.ak-foot ul{list-style:none;display:grid;gap:6px}
.ak-foot a:hover{color:#fff}
.ak-foot p{margin-bottom:10px}
.ak-copy{border-top:1px solid rgba(255,255,255,.08);padding:14px 0;font-size:13px;color:#a8937a}
.ak-float{position:fixed;right:18px;bottom:18px;z-index:45;display:flex;gap:8px;align-items:center;background:var(--ak-maroon);color:#fff;font-weight:700;padding:11px 16px;border-radius:999px;box-shadow:0 14px 30px -10px rgba(122,27,45,.7);font-size:14px;border:2px solid var(--ak-gold)}
@media (max-width:980px){
  .ak-banner img{max-height:none;height:90px;object-position:28% center}
  .ak-navbar .wrap{display:flex;justify-content:flex-end}
  .ak-nav>ul{background:#1f070e;padding:6px 0}
  .ak-nav>ul>li>a{border-bottom:1px solid rgba(255,255,255,.06)}
  .ak-nav .dd{border-top:0;box-shadow:none;border-radius:0}
  .ak-home,.ak-mgmt,.ak-two,.ak-adm-grid{grid-template-columns:1fr}
  .ak-three,.ak-disc{grid-template-columns:1fr 1fr}
  .ak-fgrid{grid-template-columns:1fr}
  .ak-formbox{position:static}
}
@media (max-width:640px){
  .ak-banner img{height:70px}
  .ak-wgrid,.ak-three,.ak-disc,.ak-fees,.gal{grid-template-columns:1fr}
  .ak-slider{height:220px}
  .ak-topbar span a:last-child{display:none}
}
"""

if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    for f in out.glob("*.html"):
        f.unlink()
    write_site(out, S, PAGES, CSS, header, footer)
