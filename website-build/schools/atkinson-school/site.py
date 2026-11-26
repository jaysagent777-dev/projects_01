# -*- coding: utf-8 -*-
"""Atkinson Senior Secondary School, Vijayawada (atkinsonvijayawada.edu.in) — redesign preview. Build: python3 site.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_template"))
from sitegen import *  # noqa

U = "https://atkinsonvijayawada.edu.in/wp-content/uploads/"
CAMPUS = U + "2024/05/School-Photo-scaled.jpg"
CAMPUS2 = U + "2024/05/School-Photo-1-scaled-e1717133525900.jpg"
S = {
    "name": "Atkinson Senior Secondary School", "domain": "atkinsonvijayawada.edu.in",
    "description": "Atkinson Senior Secondary School, Vijayawada — a CBSE school run by the Sisters of St. Ann of Providence since 1899.",
    "primary": "#8a1c2b", "secondary": "#8a6100",
    "logo": "", "logo_badge": "A", "logo_text": ("Atkinson Senior Secondary School", "VIJAYAWADA · SINCE 1899 · CBSE"),
    "phone": "0866 2565790", "phone_tel": "+918662565790",
    "address": "Convent Street, near Railway Station Road, Vijayawada, Andhra Pradesh – 520001",
    "bar_label": "Admissions 2026–27",
    "ticker": ["Admissions open for 2026–2027", "Pre-KG to UKG: co-education", "Classes I to VIII: girls only", "Class X and XII results declared — centum results"],
    "cta": ("Admission enquiry", "admissions.html#enquire"), "mbar_label": "Enquire", "fab": "Enquire on WhatsApp", "desk": "school office",
    "tabs": [("index", "Home"), ("about", "About"), ("academics", "Academics"), ("admissions", "Admissions"), ("contact", "Contact")],
    "footer_text": "Run by the Sisters of St. Ann of Providence — forming young people of character, excellence and service since 1899.",
    "footer_contact_title": "School office", "footer_contacts": ['<a href="mailto:atkinsonvjy@gmail.com">atkinsonvjy@gmail.com</a>', "Fees: Mon–Sat, 8.30–11.30 a.m."],
}

PAGES = {}
PAGES["index"] = ("Home",
    slider([
        (CAMPUS, "Admissions open · 2026–2027", "More than 125 years of educating Vijayawada.",
         "Founded in 1899 by the Sisters of St. Ann, Atkinson forms young people of character, academic excellence and selfless service.",
         [("Admission enquiry →", "admissions.html#enquire", "btn-red"), ("Call 0866 2565790", "tel:+918662565790", "btn-white")], "p"),
        (CAMPUS2, "CBSE", "Centum results in Class X and XII.",
         "Class XII results declared 13 May 2026 and Class X results declared 15 April 2026 — 100% results.",
         [("Academics →", "academics.html", "btn-red")], "s"),
    ])
    + strip([("cap", "CBSE curriculum", "Pre-KG to Senior Secondary", "academics.html", False),
             ("users", "Pre-KG to UKG co-ed", "Classes I–VIII for girls", "admissions.html", False),
             ("phone", "School office", "0866 2565790", "tel:+918662565790", True)])
    + two_col("Welcome to Atkinson", "From 16 pupils to more than 4,000.",
              "In June 1899, Mother Angela, Sr. Hyacinth and Sr. St. Charles of the Sisters of St. Ann started a primary school of 16 pupils, on land from the Honourable Mr. Atkinson, then Collector of Krishna District.",
              photo(CAMPUS2, "Atkinson school campus"), ("Our history", "about.html"))
    + section(head_("Atkinson in numbers", "A legacy that keeps growing.") + stats([
        ("star", "1899", None, "Founded by the Sisters of St. Ann"), ("users", "4,331", 4331, "Students"),
        ("book", "127", 127, "Staff members"), ("trophy", "100%", None, "Class X &amp; XII results")]), "alt")
    + section(head_("Our values", "Character, excellence and service.") + icon_cards([
        ("heart", "Compassion", "Inspired by the compassionate love at the heart of our founders' mission."),
        ("cap", "Academic excellence", "Professional and academic excellence for every student."),
        ("users", "Leadership &amp; service", "A spirit of selfless service and leadership."),
        ("shield", "Empowerment", "Special care for the poor and marginalised, so education becomes a force for social change.")], cols=4))
    + cta_band("Admissions are open for 2026–27.", "Send an enquiry and the school office will guide you through the process.", ("Admission enquiry", "admissions.html#enquire"), "0866 2565790"))

PAGES["about"] = ("About",
    page_hero("About", "Our history since 1899.", "A story of faith, perseverance and education in the heart of Vijayawada.", CAMPUS)
    + section(head_("History", "Milestones") + timeline([
        ("1899", "The Sisters of St. Ann start a primary school of 16 pupils in Bezwada (Vijayawada) at the behest of the Bishop of Hyderabad."),
        ("1900", "Within a year, 56 students — and the school's first inspection."),
        ("Early 1900s", "Raised to Middle School and then Secondary School status within four years."),
        ("1982", "Sr. Stella D'Souza takes over, acquires land and builds six major buildings."),
    ]) + '<p class="lede" style="margin-top:34px;text-align:center">Today: 4,331 students and 127 staff members.</p>')
    + section(head_("Vision &amp; mission", "Why we teach.") + '<div class="mv">'
      + f'<div class="mvcard reveal"><span class="ic">{ic("eye")}</span><div class="eyebrow">Vision</div><p>Quality education with special preference for the poor and the marginalised — instilling human values so students become instruments of social change.</p></div>'
      + f'<div class="mvcard reveal"><span class="ic">{ic("target")}</span><div class="eyebrow">Mission</div><p>To form young people of character, distinguished by academic and professional excellence, sound human values, holistic growth, selfless service and leadership.</p></div>'
      + "</div>", "alt mint"))

PAGES["academics"] = ("Academics",
    page_hero("Academics", "CBSE education with heart.", "Holistic growth — intellectual, emotional, physical and aesthetic.", CAMPUS2)
    + section(icon_cards([
        ("baby", "Pre-KG to UKG", "Co-educational early years, with admission to LKG from age 3 (by June)."),
        ("book", "Classes I – VIII", "Girls' school with a strong foundation in every subject."),
        ("cap", "Secondary &amp; Senior Secondary", "CBSE board preparation, with centum results in Classes X and XII."),
    ]))
    + section(head_("Results", "Latest board results.") + icon_cards([
        ("trophy", "Class XII", "Results declared 13 May 2026 — centum results."),
        ("trophy", "Class X", "Results declared 15 April 2026 — centum results."),
        ("cal", "CBSE second board exam", "Scheduled 15 May 2026.")]), "alt"))

PAGES["admissions"] = ("Admissions",
    page_hero("Admissions", "Admissions open: 2026–2027.", "Pre-KG to UKG co-education · Classes I to VIII for girls.", CAMPUS)
    + section(head_("How to apply", "Four simple steps.") + '<div class="steps3 four">'
      + "".join(f'<div class="reveal"><b>{n}</b><span>{t}</span></div>' for n, t in [
          (1, "Parents introduce the child in person to the Principal."),
          (2, "Fill in the registration form with all documents — incomplete forms are not accepted."),
          (3, "Older children take a placement test for the class they are applying to."),
          (4, "Pay the admission fee and term fees at the time of admission.")])
      + "</div>")
    + section('<div class="two-col" style="align-items:start"><div class="reveal">' + '<div class="eyebrow">Documents</div><h2 class="h2">What to bring</h2>'
      + ticks(["Birth certificate from the Municipality (photocopy)", "Baptismal certificate (for Catholics)", "Copy of Aadhaar card", "A self-addressed stamped envelope",
               "Transfer certificate for higher classes (counter-signed for students from other states)"])
      + '<div class="alert-note">Fees are collected Monday–Saturday, 8.30–11.30 a.m. Term I before 15 July · Term II before 1 November · Term III before 1 March.</div></div>'
      + '<div id="enquire">' + enquiry_form("Admission enquiry", [("sn", "Child's name", "text", True, None),
          ("cl", "Class applying for", "select", True, ["Pre-KG", "LKG", "UKG"] + [f"Class {n}" for n in range(1, 9)]), ("pn", "Parent's mobile", "tel", True, None), ("ms", "Message", "textarea", False, None)],
          "Send on WhatsApp") + "</div></div>", "alt mint"))

PAGES["contact"] = ("Contact",
    page_hero("Contact", "Visit or call the school office.", "Convent Street, near Railway Station Road, Vijayawada.", CAMPUS)
    + section('<div class="qc">'
      + f'<a class="qcard reveal" href="tel:+918662565790"><span class="ic">{ic("phone")}</span><b>Phone</b><span>0866 2565790</span></a>'
      + f'<a class="qcard reveal" href="mailto:atkinsonvjy@gmail.com"><span class="ic">{ic("mail")}</span><b>Email</b><span>atkinsonvjy@gmail.com</span></a>'
      + f'<a class="qcard reveal" href="https://www.google.com/maps/search/?api=1&query=Atkinson+Senior+Secondary+School+Vijayawada" target="_blank" rel="noopener"><span class="ic">{ic("pin")}</span><b>Directions</b><span>Convent Street, Vijayawada – 520001</span></a>'
      + "</div>"))

if __name__ == "__main__":
    build(S, PAGES, Path(__file__).resolve().parent)
