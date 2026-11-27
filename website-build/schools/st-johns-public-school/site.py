# -*- coding: utf-8 -*-
"""St. John's Public School (stjohnspublicschool.com) — redesign preview on the MODERN template
(website-build/_template/sitegen.py, the Praveen Hospitals design system recoloured in St. John's blue).

All 15 pages of the current site are kept (same file names). Content is the school's own text.
Build: python3 site.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_template"))
from sitegen import *  # noqa: F401,F403

I = "https://stjohnspublicschool.com/images/"
B = lambda n: f"{I}slider/banner{n}.jpg"          # 940×432: photo on the left 2/3, plain blue panel on the right
IB = lambda n: f"{I}inner-banners/{n}.jpg"        # 940×230: photo on the left 2/3, caption panel on the right
HIST = [f"{I}school-history-images/{n}.jpg" for n in range(1, 13)]   # 600px black-and-white photos since 1985

CAMPUSES = [
    ("Gunadala", "Near N.T.R. University of Health Sciences, Gunadala, Vijayawada – 520008", ["0866-2452342", "0866-2456789"]),
    ("M.G. Road", "Mohiuddin Estate, M.G. Road, Vijayawada – 520010", ["0866-2477140", "0866-2479155"]),
    ("Satyanarayanapuram — A Block", "Near Old Satyanarayanapuram Rly. Gate, BRTS Road, Vijayawada – 520011", ["0866-2578855"]),
    ("Satyanarayanapuram — B Block", "Beside Sarada College, BRTS Road, Vijayawada – 520011", ["0866-6551888"]),
    ("Bhavanipuram", "Opp. Housing Board Colony, Crombay Road, Bhavanipuram, Vijayawada – 520012", ["0866-2418855", "0866-2418877"]),
]

S = {
    "name": "St. John's Public School", "domain": "stjohnspublicschool.com",
    "primary": "#2f5f9f", "secondary": "#9a6412",
    "logo": I + "st-johns-school-logo.png", "logo_style": "height:62px;width:auto",
    "phone": "0866-2452342", "phone_tel": "+918662452342",
    "cta": ("Admission enquiry", "enquiry.html"), "mbar_label": "Enquire", "fab": "Admission enquiry", "desk": "admissions office",
    "bar_label": "Admissions open",
    "ticker": ["Admissions open — Nursery to Grade X · SSC &amp; CBSE", "Four campuses across Vijayawada",
               "City-wide school buses with a caretaker on every bus", "Careers: applications welcome all year"],
    "tabs": [("index", "Home"), ("about-school", "About"), ("academics", "Academics"), ("activities", "Activities"),
             ("facilities", "Facilities"), ("gallery", "Gallery"), ("enquiry", "Admissions"), ("contact-us", "Contact")],
    "tab_group": {"management": "about-school", "history": "about-school", "careers": "about-school", "alumni": "about-school",
                  "achievements": "academics", "infrastructure": "facilities", "transport": "facilities"},
    "footer_text": "St. John's Educational Group — quality education in Vijayawada since 1985. SSC &amp; CBSE, Nursery to Grade X.",
    "address": CAMPUSES[0][1],
    "footer_contact_title": "Campuses",
    "footer_contacts": [f'{n.split(" —")[0]} · <a href="tel:{p[0].replace("-", "")}">{p[0]}</a>' for n, a, p in CAMPUSES if "B Block" not in n]
                       + ['<a href="mailto:info@stjohnspublicschool.com">info@stjohnspublicschool.com</a>'],
    "description": "St. John's Public School, Vijayawada — SSC & CBSE from Nursery to Grade X since 1985. Campuses at Gunadala, M.G. Road, Satyanarayanapuram and Bhavanipuram.",
    "jsonld": {
        "@context": "https://schema.org", "@type": "School", "name": "St. John's Public School",
        "alternateName": "St. John's Educational Group", "url": "https://stjohnspublicschool.com/",
        "logo": I + "st-johns-school-logo.png", "foundingDate": "1985",
        "telephone": "+91-866-2452342", "email": "info@stjohnspublicschool.com",
        "address": {"@type": "PostalAddress", "streetAddress": "Near N.T.R. University of Health Sciences, Gunadala",
                    "addressLocality": "Vijayawada", "addressRegion": "Andhra Pradesh", "postalCode": "520008", "addressCountry": "IN"},
        "department": [{"@type": "School", "name": f"St. John's Public School — {n}", "telephone": "+91-" + p[0].replace("0866-", "866-"),
                        "address": {"@type": "PostalAddress", "streetAddress": a.split(", Vijayawada")[0], "addressLocality": "Vijayawada", "addressCountry": "IN"}}
                       for n, a, p in CAMPUSES],
    },
}

ABOUT = [("about-school", "About School"), ("management", "Management"), ("history", "History"), ("careers", "Careers"), ("alumni", "Alumni")]
ACAD = [("academics", "Academics"), ("achievements", "Achievements")]
FAC = [("facilities", "Facilities"), ("infrastructure", "Infrastructure"), ("transport", "Transport &amp; Security")]

def wide(src, alt=""):
    """Photo part of a 940×230 inner banner, shown at its real size so it stays sharp."""
    return f'<div class="photo wide"><img src="{src}" alt="{esc(alt)}" loading="lazy"></div>'

def pair(a, b, alt=""):
    """Two of the school's small 245px photos side by side, at real size."""
    return f'<div class="pair"><img src="{I}{a}" alt="{esc(alt)}" loading="lazy"><img src="{I}{b}" alt="" loading="lazy"></div>'

def inner(group, key, crumb, title, sub):
    return page_hero(crumb, title, sub, "") + (subnav(group, key) if group else "")

def maplink(name, addr):
    q = (f"St. John's Public School {name.split(' —')[0]} Vijayawada").replace(" ", "+").replace("'", "%27")
    return f'<a class="maplink2" href="https://www.google.com/maps/search/?api=1&query={q}" target="_blank" rel="noopener">{ic("pin", 16)} Directions</a>'

def campus_cards():
    def tel(p):
        return f'<a href="tel:{p.replace("-", "")}">{p}</a>'
    return '<div class="centres">' + "".join(
        f'<div class="centre reveal"><span class="ic">{ic("building")}</span><b>{n}</b><small>{a}</small><p>{" · ".join(tel(p) for p in ph)}</p>{maplink(n, a)}</div>'
        for n, a, ph in CAMPUSES) + "</div>"

ADMISSION_STEPS = steps([
    ("Send an enquiry", "Fill in the short form or call the campus nearest to you."),
    ("We call you back", "Our admissions office shares availability, fees and the admission process."),
    ("Visit the campus", "Meet the team, see the classrooms and complete the admission."),
])

ENQUIRY_FORM = enquiry_form("Admission enquiry", [
    ("sn", "Name of the student", "text", True, None),
    ("cl", "Class into which admission is sought", "select", True, ["Nursery", "LKG", "UKG"] + [f"Class {n}" for n in range(1, 11)]),
    ("pc", "Present class", "text", False, None),
    ("db", "Date of birth", "date", False, None),
    ("cp", "Preferred campus", "select", False, ["Gunadala", "M.G. Road", "Satyanarayanapuram", "Bhavanipuram"]),
    ("mb", "Parent's mobile", "tel", True, None),
    ("ms", "Anything you'd like to ask", "textarea", False, None),
], "Send on WhatsApp", "Our admissions office will call you back.")

PAGES = {}

# ── HOME ─────────────────────────────────────────────────────────────────────
PAGES["index"] = ("Home", slider([
    (B(1), "Welcome to St. John's Public School", "Quality education in Vijayawada since 1985.",
     "SSC &amp; CBSE from Nursery to Grade X, across four campuses in the city.",
     [("Admission enquiry →", "enquiry.html", "btn-red"), (f"{ic('phone', 18)}Call 0866-2452342", "tel:+918662452342", "btn-white")], "p"),
    (B(3), "Academics", "Academic excellence with all-round development.",
     "A custom-created programme that takes the best of contemporary and traditional education.",
     [("Our academics →", "academics.html", "btn-red")], "p"),
    (B(5), "Inquisitive minds", "Critical thinkers and self-directed learners.",
     "Laying a proper foundation and honing students' reasoning and analytical skills.",
     [("Facilities &amp; labs →", "facilities.html", "btn-red")], "s"),
    (B(7), "Transport &amp; security", "Safe, on-time travel across the city.",
     "A fleet of buses covers Vijayawada, with a caretaker on every bus.",
     [("Bus routes →", "transport.html", "btn-red")], "s"),
]) + strip([
    ("cap", "Admissions open", "Nursery to Grade X · SSC &amp; CBSE — enquire online", "enquiry.html", False),
    ("building", "Four campuses", "Gunadala · M.G. Road · Satyanarayanapuram · Bhavanipuram", "contact-us.html", False),
    ("phone", "Call the school", "0866-2452342", "tel:+918662452342", True),
]) + section(head_("Since 1985", "A small school that grew with Vijayawada.",
                    "From 192 students in its first year to an educational group spread across the city.")
             + stats([("cal", "1985", None, "Founded at M.G. Road"), ("users", "192", 192, "Students in the first year"),
                      ("building", "4", 4, "Campuses in Vijayawada"), ("book", "SSC &amp; CBSE", None, "Nursery to Grade X")])
) + two_col("About St. John's", "A dream started in 1985.",
            "St. John's School began in 1985 at M.G. Road as the dream of our Founder Chairman, Late Shri T. Thyagaraju Sahayam, and his wife Late Dr. T. Sudarsanamma — to build a school with the best infrastructure and every modern facility a growing child needs.",
            wide(IB("about-school"), "St. John's campus building"), ("About the school", "about-school.html"),
            extra='<p class="muted-p">Today, located in the heart of Vijayawada, St. John\'s is a premier institution that nurtures a positive outlook, attitude and aptitude, so children grow into global citizens with sound values.</p>',
            cls="alt") + section(head_("Life at St. John's", "Learning beyond the classroom.")
             + icon_cards([("book", "Academics", "Academic excellence along with overall development of the child — the key to succeed in a competitive world."),
                           ("trophy", "Achievements", "Our young wizards won the City Level Inter-School 20-20 Cricket Tournament, and students have placed at the Indian Science Congress."),
                           ("music", "Activities", "Clubs for music, theatre, dance, visual arts, pottery, debates and more, plus archery, martial arts and yoga."),
                           ("star", "Sports &amp; games", "Students get exposure to many sports and games, depending on their aptitude and liking.")], cols=4)
) + section(head_("Explore", "Find what matters to your family.")
            + tiles([(B(3), "Academics", "academics.html", "#2f5f9f"), (B(6), "Activities", "activities.html", "#9a6412"),
                     (IB("about-school"), "Infrastructure", "infrastructure.html", "#1f7a5a"), (B(7), "Transport", "transport.html", "#b4462e")]), "alt"
) + section(head_("Admissions", "Three simple steps to join St. John's.") + ADMISSION_STEPS
            + '<p style="text-align:center;margin-top:18px"><a class="btn btn-red" href="enquiry.html">Start your enquiry →</a></p>'
) + section(head_("Our founders", "The people behind St. John's.")
            + people([(I + "thyagaraju-sahayam.jpg", "Late Shri T. Thyagaraju Sahayam", "Founder Secretary &amp; Correspondent",
                       "A philanthropist who, with his wife, foresaw the need for quality education that was futuristic and met the highest expectations of parents in the region."),
                      (I + "sudarsanamma.jpg", "Late Dr. T. Sudarsanamma", "Founder President",
                       "Co-founded St. John's Educational Group in 1985. From 192 students, it has grown into a group of institutions across Vijayawada.")]), "alt"
) + cta_band("Looking for admission?", "Send an enquiry in a minute, or call us — we'll help you choose the right campus.", ("Admission enquiry", "enquiry.html"), "0866-2452342"),
    "St. John's Public School, Vijayawada — SSC & CBSE, Nursery to Grade X, since 1985. Four campuses: Gunadala, M.G. Road, Satyanarayanapuram, Bhavanipuram. Admissions open.")

# ── ABOUT GROUP ──────────────────────────────────────────────────────────────
PAGES["about-school"] = ("About School", inner(ABOUT, "about-school", "About", "About St. John's",
    "A premier school in the heart of Vijayawada, offering quality education since 1985.")
    + two_col("Our story", "A dream project, started in 1985.",
              "St. John's School started in 1985 at M.G. Road, Vijayawada, as the dream of our Founder Chairman, Late Shri Thyagaraju Sahayam, and his wife Late Smt. T. Sudarsanamma. Their desire was always to build the most ultra-modern school in the city, with the best infrastructure and all the modern facilities a growing child would need.",
              wide(IB("about-school"), "St. John's campus"),
              extra='<p class="muted-p">Many hurdles, many challenges and many agonising moments came their way, but they saw them as opportunities in realising their dream. Unfortunately, they did not live to see their dream project fulfilled.</p>')
    + section(icon_cards([("heart", "A healthy ambience", "St. John's creates an ambience conducive to healthy education, nurturing a positive outlook, attitude and aptitude to emerge as a global citizen with sound values."),
                          ("pin", "In the heart of the city", "Located in the heart of Vijayawada, St. John's created a history by becoming a premier institution offering quality education in the region."),
                          ("users", "Caring early years", "Experienced teachers build warm, caring relationships, so young children express themselves confidently, listen well and develop a love of books and early literacy.")]), "alt")
    + cta_band("Come and see the school", "Send an enquiry and we'll arrange a visit to your nearest campus.", ("Admission enquiry", "enquiry.html"), "0866-2452342"),
    "About St. John's Public School, Vijayawada — founded in 1985 at M.G. Road by Late Shri T. Thyagaraju Sahayam and Late Dr. T. Sudarsanamma.")

PAGES["management"] = ("Management", inner(ABOUT, "management", "Management", "Management",
    "Educationists, academicians and leaders guiding St. John's.")
    + two_col("Advisory Board", "Guiding St. John's, discreetly and steadily.",
              "St. John's Advisory Board comprises educationists, academicians, philanthropists, industrialists, social workers and members of the management who are dedicated to the spread of quality education. They play the role of a rudder, discreetly guiding and directing the St. John's team to emerge as a pioneer in education.",
              wide(IB("vision"), "Students at St. John's"))
    + section(people([(I + "management-img01.jpg", "Mr. T. Suman Thyagaraj", "Secretary &amp; Correspondent",
                       "Completed his postgraduate studies in Business Management and put all his knowledge and talent into the growth of St. John's. He leads from the front, giving his team the freedom to innovate, with one clear objective: to make St. John's the best educational institution in the region, offering education of international standards.")])
              + '<blockquote class="quote2 reveal">"My father taught me the values to be followed in life. My parents instilled in me the passion to shape the future of the society through education. The radiance and glow of knowledge on every child\'s face is the motivation and the driving force."<cite>T. Suman Thyagaraj, Secretary &amp; Correspondent</cite></blockquote>', "alt"),
    "Management of St. John's Public School, Vijayawada — Advisory Board and Secretary & Correspondent Mr. T. Suman Thyagaraj.")

PAGES["history"] = ("History", inner(ABOUT, "history", "History", "Our history",
    "From 192 students in 1985 to an educational group across Vijayawada.")
    + section(timeline([("1985", "St. John's Educational Group is founded by T. Thyagaraju Sahayam and Dr. T. Sudarsanamma, starting at M.G. Road."),
                        ("192", "Students in the first year — the small beginning of a big journey."),
                        ("4", "Campuses today: Gunadala, M.G. Road, Satyanarayanapuram and Bhavanipuram."),
                        ("Today", "Contemporary, technology-integrated education remains the focus at St. John's.")]))
    + section(head_("What we believe", "The tenets of St. John's.", center=False) + ticks([
        "Education that is cognisant of the changing demands of our society.", "Inculcating self-discipline and responsibility.",
        "Excellent infrastructure, educational materials and technology to enhance the curriculum.", "A conducive learning environment that inspires the taught as well as the teacher.",
        "Education should help children develop very clear and strong values.", "Exploring the structure and interconnectivity of knowledge.",
        "The teacher is a navigator who gives children learning maps to chart their own paths.",
        "Equipping children to 'problem find' and organise solutions.", "Team-building, leadership and interpersonal skills as part of schooling."]), "alt")
    + section(head_("Through the years", "Moments from our history.") + gallery(HIST)),
    "History of St. John's Public School, Vijayawada — founded in 1985 with 192 students, now four campuses. Photos through the years.")

PAGES["careers"] = ("Careers", inner(ABOUT, "careers", "Careers", "Careers at St. John's",
    "Join a team that values innovation, growth and good teaching.")
    + two_col("Work with us", "Applications welcome throughout the year.",
              "St. John's welcomes committed and dedicated individuals who can contribute to the high standards of excellence desired at all levels. The school emphasises employee involvement and provides equal growth opportunities to all employees, with good remuneration and scope for career growth.",
              wide(IB("Faculty"), "Teacher with students"),
              extra='<p class="muted-p">Candidates are contacted depending on openings, and shortlisted candidates are invited for a personal interview on campus. We run regular training programmes for professional growth.</p>')
    + section(head_("Areas of appointment", "Roles we hire for.")
              + icon_cards([("book", "Teaching faculty", "Teachers across Nursery to Grade X, SSC and CBSE."),
                            ("building", "Office &amp; admin", "Office and administrative staff."),
                            ("trophy", "Sports &amp; PE", "Sports and physical educators."),
                            ("heart", "Special educators", "Educators who support every learner."),
                            ("users", "Catering &amp; housekeeping", "Staff who keep our campuses running.")], cols=3)
              + '<p style="text-align:center;margin-top:18px">Send your resume to any St. John\'s campus, or email <a href="mailto:info@stjohnspublicschool.com"><b>info@stjohnspublicschool.com</b></a>.</p>', "alt"),
    "Careers at St. John's Public School, Vijayawada — teaching, admin, sports, special educator and support roles. Apply any time of the year.")

PAGES["alumni"] = ("Alumni", inner(ABOUT, "alumni", "Alumni", "Alumni network",
    "Stay connected with St. John's and with each other.")
    + two_col("Stay in touch", "Once a Johnian, always a Johnian.",
              "The Alumni Network builds and strengthens connections between former students and showcases their accomplishments. The management holds alumni meets on campus at regular intervals.",
              enquiry_form("Alumni registration", [("an", "Name", "text", True, None),
                  ("ay", "Year of completion", "select", False, [str(y) for y in range(2026, 1984, -1)]),
                  ("ap", "Phone number", "tel", True, None), ("ae", "Email", "email", False, None),
                  ("ao", "Current occupation", "text", False, None)], "Send on WhatsApp"),
              extra='<p class="muted-p">Alumni help recruit our students for jobs and internships, and volunteer their time to mentor and coach them.</p>'),
    "St. John's Public School alumni network, Vijayawada — register, join alumni meets and mentor current students.")

# ── ACADEMICS GROUP ──────────────────────────────────────────────────────────
PAGES["academics"] = ("Academics", inner(ACAD, "academics", "Academics", "Academics",
    "SSC and CBSE syllabus from Nursery to Grade X.")
    + two_col("Our approach", "Traditional values, progressive learning.",
              "St. John's firmly believes that academic excellence along with overall development of the child is the key to succeed in this competitive world. Taking best practices from both contemporary and traditional tenets of education, the school offers a custom-created programme following both <b>SSC and CBSE</b> syllabus from <b>Nursery to Grade X</b>.",
              wide(IB("academics"), "Students in class"),
              extra='<p class="muted-p">Students become independent, keep their feet firmly on the ground, and learn to adapt and excel in their chosen fields anywhere in the world.</p>')
    + section(icon_cards([("baby", "Early childhood programme", "Radford, our play school under the aegis of St. John's, gives little ones a caring, secure start — colourful classrooms, activity rooms and the latest educational play systems."),
                          ("book", "Primary curriculum", "Driven by children's natural curiosity: they explore, investigate, question and show what they learn in many ways, including dance, theatre and movement."),
                          ("users", "Parents as partners", "Orientation programmes and regular parent–teacher meetings keep parents involved in their child's development."),
                          ("monitor", "Technology in learning", "ICT labs, language labs and a digital library wing support learning, and parents can follow progress online.")], cols=2), "alt")
    + cta_band("Which class are you applying for?", "Tell us the class and campus — our admissions office will call you back.", ("Admission enquiry", "enquiry.html"), "0866-2452342"),
    "Academics at St. John's Public School, Vijayawada — SSC & CBSE, Nursery to Grade X. Early childhood (Radford play school) and primary curriculum.")

PAGES["achievements"] = ("Achievements", inner(ACAD, "achievements", "Achievements", "Achievements",
    "Our students in science, sport and the arts.")
    + section('<div class="ach">'
              + f'<article class="reveal"><img src="{I}achievements/Indian-Science-Congress-s.jpg" alt="P. Partha Koundinya at the Indian Science Congress" loading="lazy"><div><span class="eyebrow">Science</span><h3>103rd Indian Science Congress</h3><p>P. Partha Koundinya of Class X won at district and state level in the National Children\'s Science Congress 2015, took <b>first place</b> at the National Council for Science &amp; Technology Communication, and <b>third place</b> at the 103rd Indian Science Congress, Mysore (January 2016), on "Understanding Weather and Climate".</p></div></article>'
              + f'<article class="reveal"><img src="{I}achievements/wizards_of_st-johns-s.jpg" alt="St. John\'s cricket team" loading="lazy"><div><span class="eyebrow">Sport</span><h3>Wizards of St. John\'s</h3><p>Winners of the City Level Inter-School 20-20 Cricket Tournament hosted by Nalanda Vidya Niketan — beating V.P. Siddhartha Public School and Delhi Public School on the way, and the hosts by 26 runs in the final. T. Raghu was Man of the Match and Man of the Tournament.</p></div></article>'
              + '<article class="reveal"><div><span class="eyebrow">Arts</span><h3>Elocution, essay &amp; art</h3><p>Students from Classes IV–X won prizes in elocution and essay writing at Sarvothama Grandhalayam, the Department of Posts\' Design-a-Stamp contest, and an inter-school drawing competition.</p></div></article>'
              + "</div>"),
    "Achievements of St. John's Public School students — Indian Science Congress, inter-school cricket champions, elocution, essay and art prizes.")

PAGES["activities"] = ("Activities", inner(None, "activities", "Activities", "Activities",
    "Creative and performing arts, clubs, field trips and more.")
    + two_col("Creative &amp; innovative platform", "Arts that enrich children and communities.",
              "St. John's believes that creative and performing arts enrich people and communities, and are critical to understanding global cultures and the common themes that unite societies.",
              wide(IB("extra-curricular-activities"), "Student on a field trip"),
              extra='<p class="muted-p">An aesthetically designed indoor AV room hosts shows and small gatherings, and an open-air amphitheatre hosts annual day celebrations and cultural events.</p>')
    + section(head_("Clubs &amp; societies", "Designed together by students and teachers.")
              + '<div class="chips2 reveal">' + "".join(f"<span>{c}</span>" for c in ["Music", "Theatre", "Dance", "Visual arts", "Pottery", "Debates", "Stamp collection", "Gardening", "Cooking", "Cultural &amp; literary", "Archery", "Martial arts", "Yoga &amp; meditation"]) + "</div>", "alt")
    + section(icon_cards([("pin", "Field trips", "'Classrooms without walls': field trips, hikes, nature walks and treks to learn about the environment, geography, history and archaeology — and the value of sharing, caring and teamwork."),
                          ("music", "Art &amp; music", "Lessons by trained faculty in the Art and Music room, with Indian and western classical music. Exceptional work is displayed in the school museum.")], cols=2)),
    "Activities at St. John's Public School, Vijayawada — music, theatre, dance, art, clubs, field trips, archery, martial arts and yoga.")

# ── FACILITIES GROUP ─────────────────────────────────────────────────────────
PAGES["facilities"] = ("Facilities", inner(FAC, "facilities", "Facilities", "Facilities",
    "Labs, library and technology that keep improving every year.")
    + two_col("Growing every year", "Quality teaching across the city.",
              "Our facilities keep improving with every passing year. The success of St. John's prompted the management to spread quality teaching to M.G. Road, Gunadala, Satyanarayanapuram and Bhavanipuram.",
              wide(IB("academics"), "Students at St. John's"))
    + section(icon_cards([("monitor", "Latest technology", "Language labs for students from different regions, full-fledged ICT labs with the latest hardware and software, and a digital library wing. Parents can log in to follow their ward's progress."),
                          ("flask", "Science labs", "Labs that create the right ambience for experiments, group projects, symposia and science fairs."),
                          ("book", "Library-Media Centre", "Books, reference materials, dailies, journals and quiet story-telling corners — with special library weeks. Technology will never replace the book.")]), "alt"),
    "Facilities at St. John's Public School, Vijayawada — ICT and language labs, science labs, digital library and Library-Media Centre.")

PAGES["infrastructure"] = ("Infrastructure", inner(FAC, "infrastructure", "Infrastructure", "Infrastructure",
    "A modern, child-friendly campus at Gunadala.")
    + two_col("Gunadala campus", "Built as a learning aid.",
              "The premises of St. John's at Gunadala are vast and ideally located for easy access. The design and architecture are modern and aesthetic, and the campus facilities are apt for next-generation schooling.",
              wide(IB("about-school"), "St. John's Gunadala campus"),
              extra='<p class="muted-p">Each classroom is tested for lighting and seating distance from the boards, with a colour scheme conducive to learning. Furniture is built from child-friendly materials, with plenty of open space for project work.</p>')
    + section(icon_cards([("book", "Library", "Books on literature, religion and technology in English, Hindi and more."),
                          ("monitor", "Computer lab", "Latest computers with inverter and UPS backup. Computer education from Class 1 to 10."),
                          ("users", "Multi-purpose hall", "A large hall with stage, lighting and sound for cultural and co-curricular activities."),
                          ("heart", "Green park", "Greenery all around for a healthy environment and fresh air."),
                          ("check", "Hygienic water", "RO-filtered, pure drinking water."),
                          ("trophy", "Grounds", "Space for athletics and sports.")]), "alt"),
    "Infrastructure at St. John's Public School, Gunadala, Vijayawada — child-friendly classrooms, library, computer lab, multi-purpose hall, grounds.")

PAGES["transport"] = ("Transport &amp; Security", inner(FAC, "transport", "Transport", "Transport &amp; security",
    "School buses across the city, with a caretaker on every bus.")
    + two_col("Safe travel", "On time, safely and comfortably.",
              "St. John's has made elaborate transport arrangements for the convenience of the scholars. The fleet of buses covers the entire city with the latest communication devices, so children reach school on time, safely and comfortably.",
              wide(IB("transport"), "Children getting off the school bus"),
              extra=ticks(["A caretaker on every bus", "Students escorted to their classrooms by ushers", "Proximity cards for staff, identity cards for students and parents"]))
    + section(head_("Bus routes", "Where our buses go.", "Full stop-by-stop lists are available from the school office.")
              + '<div class="routes">' + "".join(f'<details class="reveal"><summary>{r}</summary><p>{s}</p></details>' for r, s in [
                  ("Route 1", "I Town K.R. Market · Gandhi Mahila Kalasala · Panja Centre · K.B.N. College · Chitti Nagar · Bhavanipuram Road · P.N. Bus Stand · Krishna Lanka · M.G. Road · Benz Circle · Gayatri Nagar"),
                  ("Route 2", "Hanuman Pet · Gandhi Nagar · Devi Nagar · Government Press · S.N. Puram · Madhura Nagar · Durga Puram · Sambamurthy Road · Kothavantena"),
                  ("Route 3", "Gowtham College opposite street · Janitha Enclave · Ramavarappadu · Gummadi Enclave · Ramavarappadu Ring"),
                  ("Route 4", "Eluru Road (Sono Vision, Rama Mandiram) · Suryarao Pet and onwards")]) + "</div>", "alt"),
    "School transport at St. John's Public School, Vijayawada — city-wide bus routes, a caretaker on every bus, campus security.")

# ── GALLERY / ADMISSIONS / CONTACT ───────────────────────────────────────────
# Year albums from the school's current gallery (gallery-data.json: year -> events -> photo URLs)
import json as _json
GAL = _json.loads((Path(__file__).resolve().parent / "gallery-data.json").read_text(encoding="utf-8"))

def year_albums():
    total = sum(len(e["photos"]) for y in GAL for e in y["events"])
    chips = "".join(f'<a href="#y{y["year"][:4]}">{y["year"]}</a>' for y in GAL) + '<a href="#history">Through the years</a>'
    out = (f'<p class="gal-intro reveal">{total:,} photos from {sum(len(y["events"]) for y in GAL)} events across our campuses. Tap an event to open its photos.</p>'
           f'<nav class="ychips reveal" aria-label="Years">{chips}</nav>')
    for y in GAL:
        n = sum(len(e["photos"]) for e in y["events"])
        cards = ""
        for e in y["events"]:
            ph = e["photos"]
            sub = " · ".join(x for x in [e["campus"], f'{len(ph)} photo{"s" if len(ph) != 1 else ""}'] if x)
            grid = "".join(f'<button data-full="{u}"><img src="{u}" alt="{esc(e["title"])}, photo {i+1}" loading="lazy"></button>' for i, u in enumerate(ph))
            cards += (f'<details class="album reveal"><summary><img class="cv" src="{ph[0]}" alt="" loading="lazy">'
                      f'<span class="meta"><b>{esc(e["title"])}</b><small>{sub}</small><i></i></span></summary>'
                      f'<div class="agrid" data-group>{grid}</div></details>')
        out += (f'<div class="yr" id="y{y["year"][:4]}"><div class="yhead"><h2>{y["year"]}</h2><span>{len(y["events"])} events · {n} photos</span></div>'
                f'<div class="albums">{cards}</div></div>')
    return out

PAGES["gallery"] = ("Gallery", inner(None, "gallery", "Gallery", "Photo gallery",
    "Events, celebrations and classroom moments, year by year.")
    + section(year_albums())
    + '<section class="alt" id="history"><div class="wrap">' + head_("Since 1985", "Through the years.") + gallery(HIST) + "</div></section>",
    "Photo gallery of St. John's Public School, Vijayawada — year albums from 2013–14 to 2021–22: Teachers' Day, Children's Day, Independence Day, graduation, field trips and more.")

PAGES["enquiry"] = ("Admissions", inner(None, "enquiry", "Admissions", "Admissions open",
    "Nursery to Grade X · SSC &amp; CBSE · four campuses in Vijayawada.")
    + section(head_("How it works", "Three simple steps.") + ADMISSION_STEPS)
    + two_col("Admission enquiry", "Send your enquiry in a minute.",
              "Fill in the form and our admissions office will call you back with details of availability, fees and the admission process for your nearest campus.",
              ENQUIRY_FORM,
              extra=ticks(["Nursery, LKG and UKG", "Classes 1 to 10", "SSC and CBSE syllabus", "Campuses at Gunadala, M.G. Road, Satyanarayanapuram and Bhavanipuram"])
                    + '<p class="muted-p" style="margin-top:14px">Prefer to talk? Call <a href="tel:+918662452342"><b>0866-2452342</b></a>.</p>', cls="alt"),
    "Admissions open at St. John's Public School, Vijayawada — Nursery to Grade X, SSC & CBSE. Send an enquiry online or call 0866-2452342.")

PAGES["contact-us"] = ("Contact Us", inner(None, "contact-us", "Contact", "Contact us",
    "Five campus blocks across Vijayawada. Call, email or get directions.")
    + section(campus_cards()
              + '<p style="text-align:center;margin-top:18px">Email: <a href="mailto:info@stjohnspublicschool.com"><b>info@stjohnspublicschool.com</b></a></p>')
    + cta_band("Have a question about admission?", "Send an enquiry and our admissions office will call you back.", ("Admission enquiry", "enquiry.html"), "0866-2452342"),
    "Contact St. John's Public School, Vijayawada — Gunadala 0866-2452342, M.G. Road 0866-2477140, Satyanarayanapuram 0866-2578855, Bhavanipuram 0866-2418855.")

S["extra_css"] = r"""
/* inner pages: compact title strip, no photo banner (only home has the big image) */
.phero{background:#f5f7fb;padding:0}
.phero::before,.phero::after{display:none}
.phero .wrap{padding:34px 24px 30px}
.phero h1{max-width:none}
/* hero: the school's banners are a photo (left 2/3) + plain blue panel; show only the photo, faded */
.hero2{height:540px}
.slide::before{inset:0 0 0 44%;background-size:150% auto;background-position:0% 50%}
.slide::after{background:linear-gradient(90deg,#fff 0%,#fff 44%,rgba(255,255,255,.7) 49%,rgba(255,255,255,.12) 64%,rgba(255,255,255,0) 100%)}
@media (max-width:980px){
  .slide::before{inset:0;background-size:auto 100%;background-position:28% center}
}
.tile img{object-position:18% center}
/* photos shown at their real size so they stay sharp */
.photo.wide{max-width:627px;aspect-ratio:auto;background:none}
.photo.wide img{width:100%;height:auto;aspect-ratio:627/230;object-fit:cover;object-position:0 50%;border-radius:20px;display:block}
.pair{display:flex;gap:14px;flex-wrap:wrap}
.pair img{width:min(245px,47%);border-radius:18px;box-shadow:var(--sh-2)}
.pair.one img{width:245px}
.muted-p{color:var(--muted);margin-top:12px}
.quote2{max-width:820px;margin:26px auto 0;background:#fff;border-radius:18px;padding:22px 26px;box-shadow:var(--sh-1);font-style:italic;color:#2c3a4b;border-left:4px solid var(--red)}
.quote2 cite{display:block;margin-top:10px;font-style:normal;font-weight:700;color:var(--red)}
.ach{display:grid;gap:18px}
.ach article{display:grid;grid-template-columns:245px 1fr;gap:22px;background:#fff;border-radius:20px;padding:20px;box-shadow:var(--sh-1);align-items:start}
.ach article:not(:has(img)){grid-template-columns:1fr}
.ach img{width:245px;border-radius:14px}
.ach h3{font-size:20px;margin:4px 0 8px}
.ach p{color:var(--muted)}
.routes details{background:#fff;border-radius:14px;padding:14px 18px;margin-bottom:10px;box-shadow:var(--sh-1)}
.routes summary{font-weight:800;color:var(--red);cursor:pointer}
.routes p{margin-top:8px;color:var(--muted);font-size:15px}
.maplink2{display:inline-flex;gap:6px;align-items:center;margin-top:10px;font-weight:700;color:var(--red);font-size:14.5px}
.centres{grid-template-columns:repeat(3,1fr)}
.people .person img{object-position:center top}
/* gallery: year albums */
.gal-intro{text-align:center;color:var(--muted);margin-bottom:14px}
.ychips{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:34px}
.ychips a{padding:9px 18px;border-radius:999px;background:#fff;box-shadow:var(--sh-1);font-weight:700;color:var(--navy)}
.ychips a:hover{background:var(--red);color:#fff}
.yr{scroll-margin-top:150px;margin-bottom:44px}
.yhead{display:flex;align-items:baseline;gap:14px;margin-bottom:16px;border-bottom:2px solid var(--bg);padding-bottom:8px}
.yhead h2{font-size:32px}
.yhead span{color:var(--muted);font-weight:600}
.albums{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.album{background:#fff;border-radius:18px;box-shadow:var(--sh-1);overflow:hidden;transition:box-shadow .2s}
.album:hover{box-shadow:var(--sh-3)}
.album summary{list-style:none;cursor:pointer;display:block}
.album summary::-webkit-details-marker{display:none}
.album summary::after{content:none!important;display:none}
.album .cv{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:var(--bg)}
.album .meta{display:block;padding:12px 14px 14px}
.album .meta b{display:block;font-size:15.5px;color:var(--navy);line-height:1.3}
.album .meta small{display:block;color:var(--muted);font-size:13px;margin-top:3px}
.album .meta i{display:block;font-style:normal;font-weight:700;font-size:13.5px;color:var(--red);margin-top:8px}
.album .meta i::after{content:"View photos →"}
.album[open]{grid-column:1/-1}
.album[open] .cv{display:none}
.album[open] .meta{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:16px 18px}
.album[open] .meta small{margin:0}
.album[open] .meta i{margin:0 0 0 auto}
.album[open] .meta i::after{content:"Close ✕"}
.agrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;padding:0 18px 18px}
.agrid button{border:0;padding:0;border-radius:12px;overflow:hidden;aspect-ratio:1;cursor:zoom-in;background:var(--bg)}
.agrid img{width:100%;height:100%;object-fit:cover;transition:transform .3s}
.agrid button:hover img{transform:scale(1.05)}
@media (max-width:980px){.centres{grid-template-columns:1fr 1fr}.albums{grid-template-columns:repeat(3,1fr)}}
@media (max-width:640px){.albums{grid-template-columns:1fr 1fr;gap:12px}.agrid{grid-template-columns:repeat(3,1fr);padding:0 10px 10px;gap:6px}.yhead h2{font-size:26px}.album .meta b{font-size:14.5px}}
@media (max-width:640px){.centres{grid-template-columns:1fr}.ach article{grid-template-columns:1fr}.ach img{width:100%;max-width:245px}.hero2{height:560px}}
"""


S["extra_css"] += r"""
/* ── colour pass: St. John's blue + school colours (sun yellow, teal, coral, purple) ── */
:root{--sj1:#2f5f9f;--sj2:#f2a900;--sj3:#16a085;--sj4:#e2503c;--sj5:#7a4fc2;--sjsky:#eaf2fc;--sjsun:#fff6df}
.alt{background:var(--sjsky)}
/* page title strip: blue gradient with soft circles */
.phero{background:linear-gradient(120deg,#1d3c6b 0%,#2f5f9f 55%,#3f7bc8 100%);position:relative;overflow:hidden}
.phero .wrap{position:relative;z-index:1}
.phero h1{color:#fff}
.phero p{color:#dbe7f7}
.phero .crumb{color:#bcd0ec}
.phero .crumb a{color:#ffd166}
.phero .wrap::after{content:"";position:absolute;right:-60px;top:-90px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(242,169,0,.35),transparent 70%);pointer-events:none}
.subnav{background:#fff}
/* home hero: light sky tint instead of plain white */
.hero2{background:var(--sjsky)}
.slide::after{background:linear-gradient(90deg,var(--sjsky) 0%,var(--sjsky) 44%,rgba(234,242,252,.7) 49%,rgba(234,242,252,.12) 64%,rgba(234,242,252,0) 100%)}
@media (max-width:980px){.slide::after{background:linear-gradient(180deg,rgba(234,242,252,.55) 0%,rgba(234,242,252,.93) 52%,var(--sjsky) 100%)}}
.slide .eyebrow{color:var(--sj4)}
/* strip cards under the hero */
.camp-strip .cs:nth-child(1) .cs-ic2{background:#fff1cc;color:#b77d00}
.camp-strip .cs:nth-child(2) .cs-ic2{background:#d9f3ec;color:var(--sj3)}
/* numbers band: deep blue */
section:has(.stats){background:linear-gradient(135deg,#1d3c6b,#2f5f9f 60%,#3a72b8);color:#fff}
section:has(.stats) .head h2{color:#fff}
section:has(.stats) .head p{color:#d6e3f5}
section:has(.stats) .eyebrow{color:#ffd166}
section:has(.stats) .head h2::after{background:#ffd166}
.stat{border-top:4px solid var(--cc,#2f5f9f)}
.stats .stat:nth-child(1){--cc:var(--sj2)}.stats .stat:nth-child(2){--cc:var(--sj3)}.stats .stat:nth-child(3){--cc:var(--sj4)}.stats .stat:nth-child(4){--cc:var(--sj5)}
.stats .stat .st-ic{background:color-mix(in srgb,var(--cc) 14%,#fff);color:var(--cc)}
.stats .stat b{color:var(--cc)}
.stats .stat:nth-child(1) b{color:#b77d00}
/* icon cards: one colour each */
.icard{border-top:4px solid var(--cc)}
.icards .icard:nth-child(5n+1){--cc:var(--sj1)}.icards .icard:nth-child(5n+2){--cc:var(--sj2)}.icards .icard:nth-child(5n+3){--cc:var(--sj3)}
.icards .icard:nth-child(5n+4){--cc:var(--sj4)}.icards .icard:nth-child(5n+5){--cc:var(--sj5)}
.icards .icard .ic{background:color-mix(in srgb,var(--cc) 13%,#fff);color:var(--cc)}
.icards .icard:nth-child(5n+2) .ic{color:#b77d00}
/* admissions steps on a warm band */
section:has(.steps3){background:linear-gradient(180deg,var(--sjsun),#fff0c7)}
.steps3 div{border-top:4px solid var(--cc)}
.steps3 div:nth-child(1){--cc:var(--sj1)}.steps3 div:nth-child(2){--cc:var(--sj3)}.steps3 div:nth-child(3){--cc:var(--sj4)}
.steps3 b{background:var(--cc)}
/* people, campuses, quote, routes */
.people .person{border-left:5px solid var(--cc,var(--sj1))}
.people .person:nth-child(2){--cc:var(--sj2)}
.centres .centre{border-top:4px solid var(--cc)}
.centres .centre:nth-child(5n+1){--cc:var(--sj1)}.centres .centre:nth-child(5n+2){--cc:var(--sj3)}.centres .centre:nth-child(5n+3){--cc:var(--sj4)}
.centres .centre:nth-child(5n+4){--cc:var(--sj5)}.centres .centre:nth-child(5n+5){--cc:var(--sj2)}
.centres .centre .ic{background:color-mix(in srgb,var(--cc) 13%,#fff);color:var(--cc)}
.quote2{border-left-color:var(--sj2);background:var(--sjsun)}
.routes details:nth-child(1){border-left:5px solid var(--sj1)}.routes details:nth-child(2){border-left:5px solid var(--sj3)}
.routes details:nth-child(3){border-left:5px solid var(--sj4)}.routes details:nth-child(4){border-left:5px solid var(--sj5)}
.chips2 span:nth-child(5n+1){background:#e3edfa;color:#1f4a85}.chips2 span:nth-child(5n+2){background:#fff1cc;color:#8a5a00}
.chips2 span:nth-child(5n+3){background:#d9f3ec;color:#0e6e5c}.chips2 span:nth-child(5n+4){background:#fde3df;color:#a8321f}.chips2 span:nth-child(5n+5){background:#ece4fa;color:#55349a}
.ach article{border-left:5px solid var(--cc)}
.ach article:nth-child(1){--cc:var(--sj3)}.ach article:nth-child(2){--cc:var(--sj2)}.ach article:nth-child(3){--cc:var(--sj4)}
.tiles{grid-template-columns:repeat(4,1fr)}
@media (max-width:980px){.tiles{grid-template-columns:1fr 1fr}}
/* call-to-action band: blue to purple */
.cta-band{background:linear-gradient(120deg,#2f5f9f,#4a5fc2 55%,#7a4fc2)}
/* gallery: a colour per year */
.yr:nth-of-type(1){--cc:var(--sj4)}.yr:nth-of-type(2){--cc:var(--sj3)}.yr:nth-of-type(3){--cc:var(--sj5)}.yr:nth-of-type(4){--cc:var(--sj1)}
.yhead{border-bottom-color:color-mix(in srgb,var(--cc) 30%,#fff)}
.yhead h2{color:var(--cc)}
.album{border-top:4px solid var(--cc)}
.album .meta i{color:var(--cc)}
.ychips a:nth-child(1){color:var(--sj4)}.ychips a:nth-child(2){color:var(--sj3)}.ychips a:nth-child(3){color:var(--sj5)}.ychips a:nth-child(4){color:var(--sj1)}.ychips a:nth-child(5){color:#b77d00}
.ychips a:hover{color:#fff}
"""

if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    for f in out.glob("*.html"):
        f.unlink()
    build(S, PAGES, out)
