# -*- coding: utf-8 -*-
"""St. John's Public School, Vijayawada (stjohnspublicschool.com) — redesign preview. Build: python3 site.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_template"))
from sitegen import *  # noqa

I = "http://stjohnspublicschool.com/images/"
S = {
    "name": "St. John's Public School", "domain": "stjohnspublicschool.com",
    "description": "St. John's Public School, Vijayawada — SSC & CBSE from Nursery to Grade X since 1985, across Gunadala, M.G. Road, Satyanarayanapuram and Bhavanipuram.",
    "primary": "#2f5f9f", "secondary": "#c2410c",
    "logo": I + "st-johns-school-logo.png", "logo_style": "",
    "phone": "0866-2452342", "phone_tel": "+918662452342",
    "address": "Near N.T.R. University of Health Sciences, Gunadala, Vijayawada – 520008",
    "bar_label": "Admissions open",
    "ticker": ["Admissions open — Nursery to Grade X", "SSC &amp; CBSE curriculum", "School buses across Vijayawada with caretakers on every bus", "Campuses: Gunadala · M.G. Road · Satyanarayanapuram · Bhavanipuram"],
    "cta": ("Admission enquiry", "contact.html#enquire"), "mbar_label": "Enquire", "fab": "Enquire on WhatsApp", "desk": "admissions office",
    "extra_css": ".slide::before{background-position:left center}.brand img{height:64px}",
    "tabs": [("index", "Home"), ("about", "About"), ("academics", "Academics"), ("campus", "Campus &amp; Facilities"), ("activities", "Activities"), ("contact", "Admissions &amp; Contact")],
    "footer_text": "Since 1985 — nurturing a positive outlook, attitude and aptitude so every child emerges as a global citizen with sound values.",
    "footer_contact_title": "Admissions", "footer_contacts": ['<a href="tel:+918662477140">M.G. Road: 0866-2477140</a>', '<a href="mailto:info@stjohnspublicschool.com">info@stjohnspublicschool.com</a>'],
}

PAGES = {}
PAGES["index"] = ("Home",
    slider([
        (I + "slider/banner1.jpg", "Admissions open · Nursery to Grade X", "Wings and knowledge to soar high.",
         "Education is what one learns for life. St. John's gives every child the platform to grow through individual experiences and collective activities.",
         [("Admission enquiry →", "contact.html#enquire", "btn-red"), ("Call 0866-2452342", "tel:+918662452342", "btn-white")], "p"),
        (I + "inner-banners/about-school.jpg", "Since 1985", "A premier school in the heart of Vijayawada.",
         "From 192 students to an educational group with four campuses across the city.",
         [("Our story →", "about.html", "btn-red")], "s"),
        (I + "slider/banner5.jpg", "Academics", "Inquisitive minds, critical thinkers.",
         "SSC and CBSE programmes that lay a proper foundation and hone reasoning and analytical skills.",
         [("Academics →", "academics.html", "btn-red")], "p"),
    ])
    + strip([("cap", "SSC &amp; CBSE", "Nursery to Grade X", "academics.html", False),
             ("bus", "School transport", "Buses across the city, caretaker on board", "campus.html", False),
             ("phone", "Admissions office", "0866-2452342", "tel:+918662452342", True)])
    + two_col("About St. John's", "A dream that became a landmark.",
              "St. John's began in 1985 at M.G. Road, Vijayawada — the dream of our Founder Chairman, the late Shri Thyagaraju Sahayam, and his wife, the late Smt. T. Sudarsanamma: an ultra-modern school with the best infrastructure a growing child needs.",
              photo(I + "inner-banners/about-school.jpg", "St. John's school building"), ("Read our story", "about.html"))
    + section(head_("Why parents choose St. John's", "Learning for life.") + stats([
        ("star", "1985", None, "Founded at M.G. Road"), ("building", "4", 4, "Campuses across Vijayawada"),
        ("users", "192", 192, "Students on day one"), ("cap", "SSC + CBSE", None, "Nursery to Grade X")]), "alt")
    + section(head_("Beyond the classroom", "Every child finds their thing.") + icon_cards([
        ("music", "Arts &amp; clubs", "Music, theatre, dance, visual arts, pottery, debates and more."),
        ("trophy", "Sports", "Archery, martial arts, cricket and a wide range of games."),
        ("flask", "Science &amp; ICT labs", "Full-fledged science, language and computer labs."),
        ("bus", "Safe transport", "City-wide bus fleet with a caretaker on every bus.")], cols=4))
    + cta_band("Admissions are open.", "Tell us about your child and the class you're applying for — we'll call you back.", ("Admission enquiry", "contact.html#enquire"), "0866-2452342"))

PAGES["about"] = ("About",
    page_hero("About", "Our story since 1985.", "From a small school of 192 students to an educational group across Vijayawada.", I + "inner-banners/about-school.jpg")
    + section(head_("History", "Three decades of setting standards.") + timeline([
        ("1985", "St. John's founded at M.G. Road by Shri Thyagaraju Sahayam and Dr. T. Sudarsanamma, with 192 students."),
        ("Growth", "New campuses at Gunadala and Satyanarayanapuram bring quality teaching to more of the city."),
        ("Today", "An educational group offering SSC and CBSE from Nursery to Grade X."),
        ("Next", "A new campus in Bhavanipuram.")]))
    + section(head_("Founders &amp; management", "The people behind St. John's.") + people([
        (I + "thyagaraju-sahayam.jpg", "Late Shri Thyagaraju Sahayam", "Founder Chairman", "A philanthropist who dreamed of an ultra-modern school with the best infrastructure for every growing child."),
        (I + "sudarsanamma.jpg", "Late Dr. T. Sudarsanamma", "Founder", "Shared the vision of futuristic, quality education that met the highest expectations of parents."),
        (None, "Mr. T. Suman Thyagaraj", "Secretary &amp; Correspondent", "A postgraduate in business management who leads from the front, with one goal: education of international standards."),
    ]), "alt")
    + section(head_("Our tenets", "What we stand for.") + icon_cards([
        ("target", "Education for a changing world", "Cognizant of the changing demands of society."),
        ("shield", "Self-discipline", "Inculcating self-discipline and responsibility."),
        ("building", "Excellent infrastructure", "Materials and technology that enhance the curriculum."),
        ("heart", "An inspiring environment", "A learning space that inspires students and teachers alike.")], cols=4)))

PAGES["academics"] = ("Academics",
    page_hero("Academics", "Traditional values, progressive learning.", "A custom-created programme following both SSC and CBSE syllabus from Nursery to Grade X.", I + "slider/banner5.jpg")
    + two_col("Our approach", "Student-centric, by design.",
              "Taking the best from contemporary and traditional education, we help students become independent and self-confident — feet firmly on the ground, ready to adapt and excel anywhere in the world.",
              photo(I + "slider/banner3.jpg", "Student reading"),
              extra=ticks(["SSC and CBSE streams", "Nursery to Grade X", "Language, science and ICT labs", "Parents can follow progress online"]))
    + section(head_("Stages", "Learning at every age.") + icon_cards([
        ("baby", "Early childhood", "Radford, our exclusive play school, gives young learners the right start in their own way."),
        ("book", "Primary", "Warm, caring teachers who help children express themselves and listen with confidence."),
        ("cap", "Secondary", "Reasoning, analytical skills and preparation for board examinations.")]), "alt mint"))

PAGES["campus"] = ("Campus &amp; Facilities",
    page_hero("Campus &amp; Facilities", "Built for next-generation schooling.", "Vast campuses with modern architecture, safe classrooms and technology throughout.", I + "inner-banners/about-school.jpg")
    + section(icon_cards([
        ("building", "Child-friendly buildings", "Classrooms tested for lighting and seating distance, with a colour scheme that helps children learn."),
        ("monitor", "ICT labs", "State-of-the-art computer labs with the latest hardware and software."),
        ("flask", "Science labs", "Hands-on experiments in well-equipped laboratories."),
        ("book", "Language labs &amp; library", "Spaces for reading and language practice."),
        ("trophy", "Sports facilities", "Grounds and coaching across many sports and games."),
        ("shield", "Security", "Proximity cards for staff, ID cards for students and parents."),
    ]))
    + two_col("Transport", "Safe, on time, every day.",
              "Our fleet of buses covers the entire city with the latest communication devices. A caretaker rides every bus, and ushers escort students to their classrooms on arrival.",
              photo(I + "inner-banners/transport.jpg", "St. John's school bus"), cls="alt"))

PAGES["activities"] = ("Activities",
    page_hero("Activities", "Creative and innovative, by nature.", "The arts enrich people and communities — and help children understand the world.", I + "slider/banner1.jpg")
    + section(icon_cards([
        ("music", "Music, theatre &amp; dance", "Performing arts clubs led by students and teachers together."),
        ("star", "Visual arts &amp; pottery", "Hands-on creativity and an aesthetic sense."),
        ("users", "Debates &amp; literary clubs", "Confidence in speaking and writing."),
        ("trophy", "Archery, martial arts &amp; yoga", "Trained under experts, with meditation for focus."),
        ("pin", "Field trips", "Educational tours that use every sense to learn."),
        ("heart", "Gardening &amp; cooking", "Life skills and responsibility."),
    ]))
    + section(head_("Achievements", "Our students make us proud.") + icon_cards([
        ("trophy", "Indian Science Congress", "A Grade X student placed first at the National Council for Science &amp; Technology Communication and third at the 103rd Indian Science Congress."),
        ("trophy", "City cricket champions", "Winners of the City Level Inter-School 20-20 Cricket Tournament."),
        ("star", "Competitions", "Regular participation in maths and science competitions for Classes I–XII.")]), "alt"))

PAGES["contact"] = ("Admissions &amp; Contact",
    page_hero("Admissions &amp; Contact", "Admissions are open.", "Send an enquiry and the admissions office will call you back.", I + "slider/banner1.jpg")
    + f'<section id="enquire"><div class="wrap two-col" style="align-items:start">'
    + f'<div class="reveal"><div class="eyebrow">Admission enquiry</div><h2 class="h2">Tell us about your child.</h2><p class="lede">We\'ll share fees, availability and the admission process for your nearest campus.</p>'
    + '<div class="alert-note">Enquiries are for the current academic year. Our admissions team will confirm the class and campus with you.</div></div>'
    + enquiry_form("Admission enquiry", [("sn", "Student name", "text", True, None), ("cl", "Class applying for", "select", True, ["Nursery", "LKG", "UKG"] + [f"Class {n}" for n in range(1, 11)]),
        ("cp", "Preferred campus", "select", False, ["Gunadala", "M.G. Road", "Satyanarayanapuram", "Bhavanipuram"]), ("pn", "Parent's mobile", "tel", True, None), ("ms", "Message", "textarea", False, None)],
        "Send on WhatsApp")
    + "</div></section>"
    + section(head_("Our campuses", "Find the campus nearest you.") + locations([
        ("Gunadala", "Near N.T.R. University of Health Sciences, Gunadala, Vijayawada – 520008", ["0866-2452342", "0866-2456789"]),
        ("M.G. Road", "Mohiuddin Estate, M.G. Road, Vijayawada – 520010", ["0866-2477140", "0866-2479155"]),
        ("Satyanarayanapuram (A &amp; B Blocks)", "Near Old Satyanarayanapuram Rly. Gate, BRTS Road, Vijayawada – 520011", ["0866-2578855", "0866-6551888"]),
        ("Bhavanipuram", "Opp. Housing Board Colony, Crombay Road, Bhavanipuram, Vijayawada – 520012", ["0866-2418855", "0866-2418877"])]), "alt"))

if __name__ == "__main__":
    build(S, PAGES, Path(__file__).resolve().parent)
