# -*- coding: utf-8 -*-
"""St. John's Public School (stjohnspublicschool.com) — redesign preview that KEEPS the original layout:
boxed page, logo + top links, "|" menu, blue admissions strip, banner slider, 4 features + announcements
on blue, 3 photo cards, founders panel; inner pages = banner + text + photo column. Build: python3 site.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_template"))
from classic import *  # noqa

I = "http://stjohnspublicschool.com/images/"
S = {"name": "St. John's Public School", "domain": "stjohnspublicschool.com", "desk": "admissions office",
     "description": "St. John's Public School, Vijayawada — SSC & CBSE from Nursery to Grade X since 1985. Campuses at Gunadala, M.G. Road, Satyanarayanapuram and Bhavanipuram."}

MENU = [
    ("about-school", "About School", [("about-school.html", "About School"), ("management.html", "Management"), ("history.html", "History"), ("careers.html", "Careers")]),
    ("academics", "Academics", [("academics.html", "Academics"), ("achievements.html", "Achievements")]),
    ("activities", "Activities", None),
    ("facilities", "Facilities", [("facilities.html", "Facilities"), ("infrastructure.html", "Infrastructure"), ("transport.html", "Transport &amp; Security")]),
    ("gallery", "Gallery", None),
]
GROUP = {"about-school": "about-school", "management": "about-school", "history": "about-school", "careers": "about-school",
         "academics": "academics", "achievements": "academics", "facilities": "facilities", "infrastructure": "facilities", "transport": "facilities"}

def header(active):
    top = " ".join(f'<a href="{h}"{" aria-current=&quot;page&quot;" if h.startswith(active + ".") else ""}>{l}</a>'.replace("&quot;", '"')
                   for h, l in [("index.html", "Home"), ("alumni.html", "Alumni"), ("enquiry.html", "Enquiry"), ("contact-us.html", "Contact us")])
    return f"""<div class="sj-box">
<header class="sj-head">
  <a class="sj-logo" href="index.html"><img src="{I}st-johns-school-logo.png" alt="St. John's — Nurturing, Only Learning"></a>
  <div class="sj-hr">
    <div class="sj-toplinks">{top}<a class="sj-call" href="tel:+918662452342">{ic("phone", 15)}0866-2452342</a></div>
    {nav(MENU, GROUP.get(active, active), "sj-nav")}
  </div>
</header>
<div class="sj-adm"><span>Admissions Open — Nursery to Grade X · SSC &amp; CBSE</span><a href="enquiry.html">Enquire now →</a></div>"""

def footer(active):
    camp = "".join(f"<li><b>{n}</b> <a href=\"tel:{t.replace('-', '')}\">{t}</a></li>" for n, t in [("Gunadala", "0866-2452342"), ("M.G. Road", "0866-2477140"), ("Satyanarayanapuram", "0866-2578855"), ("Bhavanipuram", "0866-2418855")])
    return f"""<footer class="sj-foot">
  <div class="sj-fgrid">
    <div><img src="{I}st-johns-school-logo.png" alt="St. John's" class="sj-flogo"><p>St. John's Educational Group — quality education in Vijayawada since 1985.</p></div>
    <div><h4>Quick links</h4><ul><li><a href="about-school.html">About School</a></li><li><a href="academics.html">Academics</a></li><li><a href="facilities.html">Facilities</a></li><li><a href="careers.html">Careers</a></li><li><a href="alumni.html">Alumni</a></li></ul></div>
    <div><h4>Campuses</h4><ul>{camp}</ul></div>
  </div>
  <div class="sj-copy">Copyright © 2026, St. John's Public School. · <a href="mailto:info@stjohnspublicschool.com">info@stjohnspublicschool.com</a></div>
</footer>
</div>
<a class="sj-float" href="enquiry.html">{ic("cap", 18)} Admission enquiry</a>"""

def inner(title, banner, body, right_imgs, cls=""):
    rights = "".join(f'<img src="{I}{r}" alt="" loading="lazy" class="reveal">' for r in right_imgs)
    return (f'<div class="sj-banner"><img src="{I}{banner}" alt="{title}"></div>'
            f'<section class="sj-inner {cls}"><div class="sj-main"><h1 class="sj-h1">{title}</h1>{body}</div>'
            f'{f"<aside class=&quot;sj-side&quot;>{rights}</aside>" if rights else ""}</section>').replace("&quot;", '"')

P = lambda *xs: "".join(f"<p>{x}</p>" for x in xs)
H = lambda x: f'<h2 class="sj-h2">{x}</h2>'

CAPTIONS = [  # the original site's slide captions, word for word
    ("Education is what one learns for life. Schooling provides the wings and the knowledge to soar high.", "It provides a platform for the students to strengthen their wings with the help of individual experiences and collective activities."),
    ("Located in the heart of the city of Vijayawada, St. John's created a history by becoming a premier institution offering quality education in the region.", "It nurtures a positive outlook, attitude and aptitude to emerge as a global citizen with sound values."),
    ("St. John's firmly believes that academic excellence along with overall development of the child is the key to succeed in this competitive world.", "Taking best practices from both contemporary and traditional tenets of education, the school offers a custom-created programme."),
    ("St. John's aims to develop inquisitive minds, critical thinkers and self-directed learners", "by laying a proper foundation and honing the students' power of reasoning and analytical skills."),
    ("St. John's believes that creative and performing arts enrich people and communities,", "and are critical to an understanding of global cultures and the common themes that unite societies."),
    ("St. John's has made elaborate transportation arrangements for the convenience of the scholars.", "The fleet of buses covers the entire city, so children reach school on time, safely and comfortably."),
]

PAGES = {}
PAGES["index"] = ("Home", f"""
<section class="sj-hero">
  {slider([(I + f"slider/banner{n}.jpg", "St. John's Public School", f"<b>{a}</b><p>{b}</p>") for n, (a, b) in zip((1, 2, 3, 5, 6, 7), CAPTIONS)], "sj-slider")}
</section>
<section class="sj-features">
  <div class="sj-fgrid4">
    <a class="sj-feat reveal" href="academics.html"><span class="sj-fi">{ic("book", 26)}</span><div><h3>Academics</h3><p>St. John's firmly believes that academic excellence along with overall development of the child is the key to succeed in this competitive world.</p></div></a>
    <a class="sj-feat reveal" href="achievements.html"><span class="sj-fi">{ic("trophy", 26)}</span><div><h3>Achievements</h3><p>The honour of St. John's flies high — our young wizards won the City Level Inter-School 20-20 Cricket Tournament.</p></div></a>
    <a class="sj-feat reveal" href="activities.html"><span class="sj-fi">{ic("music", 26)}</span><div><h3>Activities</h3><p>Students are encouraged to participate and get trained under experts in archery, martial arts, yoga and meditation.</p></div></a>
    <a class="sj-feat reveal" href="facilities.html"><span class="sj-fi">{ic("star", 26)}</span><div><h3>Sports / Games</h3><p>Students get exposure to various sports and games, depending on their aptitude and liking.</p></div></a>
  </div>
  <aside class="sj-ann reveal"><h3>{ic("pulse", 20)} Announcements</h3>
    <ul><li><b>Admissions open</b> — Nursery to Grade X (SSC &amp; CBSE). <a href="enquiry.html">Enquire online →</a></li>
    <li><b>Alumni</b> — reconnect with St. John's through our alumni network. <a href="alumni.html">Register →</a></li>
    <li><b>Careers</b> — applications welcome throughout the year. <a href="careers.html">Details →</a></li></ul></aside>
</section>
<section class="sj-cards">
  <article class="sj-card reveal"><div class="sj-cimg"><img src="{I}vision-img.jpg" alt=""><span>About School</span></div><p>St. John's School, a dream project started in the year 1985 at M.G. Road by our beloved Founder Chairman, Late Shri Thyagaraju Sahayam and his wife Late Smt. T. Sudarsanamma.</p><a href="about-school.html">Read more</a></article>
  <article class="sj-card reveal"><div class="sj-cimg"><img src="{I}infrastructure-img.jpg" alt=""><span>Infrastructure</span></div><p>At St. John's, each classroom has been designed with emphasis on providing a vibrant and safe learning environment, tested for lighting and seating distance.</p><a href="infrastructure.html">Read more</a></article>
  <article class="sj-card reveal"><div class="sj-cimg"><img src="{I}management-img.jpg" alt=""><span>Management</span></div><p>St. John's Advisory Board comprises educationists, academicians, philanthropists, industrialists, social workers and members of the management.</p><a href="management.html">Read more</a></article>
</section>
<section class="sj-founders reveal">
  <figure><img src="{I}thyagaraju-sahayam.jpg" alt="Late Shri T. Thyagaraju Sahayam"><figcaption>Founder Secretary and Correspondent<br><b>Late Shri T. Thyagaraju Sahayam</b></figcaption></figure>
  <figure><img src="{I}sudarsanamma.jpg" alt="Late Dr. T. Sudarsanamma"><figcaption>Founder President<br><b>Late Dr. T. Sudarsanamma</b></figcaption></figure>
  <div><p><b>St. John's Educational Group</b> was established in the year 1985 by T. Thyagaraju Sahayam, a philanthropist, and his wife Dr. T. Sudarsanamma, who together foresaw the need to provide quality education that was futuristic and met the highest expectations of parents in the region.</p>
  <p>From a small school with merely 192 students, today it has emerged as an educational group with its institutions spread across Vijayawada — the educational hub of Andhra Pradesh.</p><a class="sj-btn" href="history.html">Our history</a></div>
</section>
""")

PAGES["about-school"] = ("About School", inner("About School", "inner-banners/about-school.jpg",
    P("St. John's School, a dream project started in the year 1985 at M.G. Road, Vijayawada by our beloved Founder Chairman, Late Shri Thyagaraju Sahayam and his wife Late Smt. T. Sudarsanamma. Their desire was always to build the most ultra-modern school in the city, with the best infrastructure and all the modern facilities that a growing child would need. Many hurdles, many challenges and many agonising moments came their way, but they saw them as opportunities in realising their dream. Unfortunately, they did not live to see their dream project fulfilled.",
      "St. John's attempts to create an ambience conducive to a healthy education. It nurtures a positive outlook, attitude and aptitude to emerge as a global citizen with sound values.",
      "Located in the heart of the city of Vijayawada, St. John's created a history by becoming a premier institution offering quality education in the region.",
      "Experienced teachers for the lower section at St. John's are skilled in developing warm, caring relationships with children, allowing them to express their needs and wants confidently. Staff encourage them to listen, both to adults and to other children, to talk confidently in a variety of situations, to develop an enthusiasm for books of all kinds, and to develop early literacy skills."),
    ["inner-rgts-imgs/St-Johns-School2.jpg", "inner-rgts-imgs/St-Johns-School1.jpg"]))

PAGES["management"] = ("Management", inner("Management", "slider/inner-banner.jpg",
    P("St. John's Advisory Board comprises a group of educationists, academicians, philanthropists, industrialists, social workers and members of the management who are dedicated to the spread of quality education in these parts of the country. They have been playing the role of a rudder, discreetly guiding and directing the St. John's team to emerge as a pioneer in education.",
      "Mr. T. Suman Thyagaraj, the Secretary and Correspondent of St. John's, completed his postgraduate studies in Business Management and decided to put all his knowledge and talent into the growth of St. John's. Like a true leader, he believes in leading from the front, taking along his talented team. The secret of his team's success lies in their freedom to innovate and ideate for the development of the institution at all times. His clear objective is to make St. John's the best educational institution in the region, offering education of international standards.")
    + H("Secretary's Message") + '<blockquote class="sj-quote">"My father taught me the values to be followed in life. My parents instilled in me the passion to shape the future of the society through education. The radiance and glow of knowledge on every child\'s face is the motivation and the driving force."<cite>T. Suman Thyagaraj, Secretary &amp; Correspondent</cite></blockquote>',
    ["management-img01.jpg"]))

PAGES["history"] = ("History", inner("History", "inner-banners/history.jpg",
    P("St. John's Educational Group was established in the year 1985 by T. Thyagaraju Sahayam, a philanthropist, and his wife Dr. T. Sudarsanamma, who together foresaw the need to provide quality education that was futuristic and met the highest educational expectations and needs of the parents in the region. From a small school with merely 192 students, today it has emerged as an educational group with its institutions spread across Vijayawada — the educational hub of Andhra Pradesh.",
      "Learning to teach, setting standards, paving paths, creating history have all been a part of the achievement in this eventful journey of three decades. Providing contemporary and technology-integrated education has been, is and will always be the point of focus at St. John's.")
    + H("The Tenets of St. John's") + '<ul class="sj-ticks">' + "".join(f"<li>{x}</li>" for x in [
      "Education that is cognisant of the changing demands of our society.", "Inculcating self-discipline and responsibility.",
      "Excellent infrastructure, educational materials and technology to enhance the curriculum.", "A conducive learning environment that inspires the taught as well as the teacher.",
      "Education should deal with pivotal intellectual tasks.", "Education should help children develop very clear and strong values.",
      "Education should encourage exploration of the structure and interconnectivity of knowledge.", "Learning must be guided by generalised principles in order to be widely applicable.",
      "The teacher's role is that of a navigator who provides children with learning maps to chart their learning paths.",
      "Education should equip children with the ability to 'problem find' and to organise solutions.", "Team-building, leadership training and interpersonal skills should be developed as part of schooling."]) + "</ul>"
    + H("Through the years") + gallery([I + f"school-history-images/{n}s.jpg" for n in range(1, 13)], "sj-gal"),
    ["thyagaraju-sahayam.jpg", "sudarsanamma.jpg"]))

PAGES["careers"] = ("Careers", inner("Careers", "inner-banners/careers.jpg",
    P("St. John's welcomes applications from committed and dedicated individuals who can contribute to the high standards of excellence desired at all levels. The school emphasises employee involvement and provides equal growth opportunities to all employees.",
      "We are looking for talented individuals who aspire to a career in education with good remuneration and scope for career growth. Interested candidates may send their applications at any time of the year; candidates will be contacted depending on openings.",
      "The broad areas of appointment are Teaching Faculty, Office and Admin staff, Sports and Physical Educators, Special Educators, and Catering and Housekeeping staff.",
      'To apply, send your resume to any St. John\'s location you wish to join, or email <a href="mailto:info@stjohnspublicschool.com">info@stjohnspublicschool.com</a>. Shortlisted candidates will be contacted by telephone for a personal interview on campus.',
      "<b>Benefits:</b> we conduct regular training programmes for professional growth."),
    ["inner-rgts-imgs/faculty.jpg"]))

PAGES["academics"] = ("Academics", inner("Academics", "inner-banners/academics.jpg",
    P("St. John's firmly believes that academic excellence along with overall development of the child is the key to succeed in this competitive world. Taking best practices from both contemporary and traditional tenets of education, the school offers a custom-created programme following both <b>SSC and CBSE</b> syllabus from <b>Nursery to Grade X</b>.",
      "The unique learning philosophy at St. John's infuses traditional values into a progressive approach, equipping students to become independent, have their feet firmly on the ground, yet adapt and excel in their chosen fields anywhere in the world.")
    + H("Early Childhood Programme") + P("The child in the formative years is eager to learn, but in their own way. Radford — an exclusive play school under the aegis of St. John's — provides the right impetus for the child to bloom.",
      "Sensitive and appreciative teachers create a caring, secure space for little ones in the \"big school\". Colourful classrooms and specially designed activity rooms with the latest educational play systems, toys and games make learning interesting and interactive.")
    + H("Primary School Curriculum") + P("St. John's includes the active participation of parents in charting the child's development through orientation programmes and periodic parent–teacher meetings.",
      "The primary curriculum is driven by the natural curiosity children show at this age. They explore and investigate, consolidate and connect what they learn, question it, and demonstrate their learning in multiple ways — including dance, theatre and movement."),
    ["inner-rgts-imgs/early-childhood-programme.jpg", "inner-rgts-imgs/primary_school_curriculum.jpg", "inner-rgts-imgs/presentation_skills.jpg"]))

PAGES["achievements"] = ("Achievements", inner("Achievements", "inner-banners/vision.jpg",
    '<p class="sj-lead">Students\' achievements in events and competitions.</p>'
    + '<div class="sj-ach">'
    + f'<article class="reveal"><img src="{I}achievements/Indian-Science-Congress-s.jpg" alt="" loading="lazy"><div><h3>103rd Indian Science Congress</h3><p>P. Partha Koundinya of Class X won at district and state level in the National Children\'s Science Congress 2015, took <b>first place</b> at the National Council for Science &amp; Technology Communication and <b>third place</b> at the 103rd Indian Science Congress, Mysore (January 2016), on the theme "Understanding Weather and Climate".</p></div></article>'
    + f'<article class="reveal"><img src="{I}achievements/wizards_of_st-johns-s.jpg" alt="" loading="lazy"><div><h3>Wizards of St. John\'s</h3><p>Winners of the City Level Inter-School 20-20 Cricket Tournament conducted by Nalanda Vidya Niketan — beating V.P. Siddhartha Public School and Delhi Public School on the way, and the hosts by 26 runs in the final. T. Raghu was Man of the Match and Man of the Tournament.</p></div></article>'
    + '<article class="reveal"><div><h3>Elocution, essay &amp; art competitions</h3><p>Students from Classes IV–X won prizes in elocution and essay writing at Sarvothama Grandhalayam, the Department of Posts\' Design-a-Stamp contest, and an inter-school drawing competition.</p></div></article>'
    + "</div>", []))

PAGES["activities"] = ("Activities", inner("Activities", "inner-banners/extra-curricular-activities.jpg",
    H("Creative and Innovative Platform") + P("St. John's believes that creative and performing arts enrich people and communities, and are critical to an understanding of global cultures and the common themes that unite societies.",
      "The school has established clubs and societies — music, theatre, dance, visual arts, pottery, debates, stamp collection, gardening, cooking, cultural and literary activities — that students and teachers design together. An aesthetically designed indoor AV room hosts shows and small gatherings.")
    + H("Field Trips") + P("Educational tours are 'classrooms without walls'. Students and teachers venture out for field trips, hikes, nature walks and treks to learn about environmental, geographical, historical and archaeological subjects — and the value of sharing, caring and teamwork.")
    + H("Art Develops Ideas") + P("The Art and Music room offers lessons by trained faculty, with training in Indian and western classical music. Exceptional work is displayed in the school museum, and an open-air amphitheatre hosts annual day celebrations and cultural events."),
    ["inner-rgts-imgs/academics8.jpg", "inner-rgts-imgs/field-trips.jpg", "inner-rgts-imgs/music.jpg"]))

PAGES["facilities"] = ("Facilities", inner("Facilities", "inner-banners/Faculty.jpg",
    P("Our facilities keep improving with every passing year. The success of St. John's prompted the management to spread quality teaching to M.G. Road, Gunadala, Satyanarayanapuram and Bhavanipuram.")
    + H("Adopting the Latest Technology") + P("Language labs support students from different regions, and parents can log in to follow their ward's progress online. Full-fledged ICT labs with the latest hardware and software offer a computer course that surpasses the board stipulation, with a digital library wing attached.")
    + H("State-of-the-art Labs for Science") + P("Science labs create the right ambience for experiments, with group projects, symposia and science fairs. The Library-Media Centre stocks books, reference materials, dailies and journals, and runs special library weeks.")
    + H("Love for Reading") + P("We confidently predict that technology will never replace the book. The Library-Media Centre features books, periodicals and quiet story-telling corners."),
    ["inner-rgts-imgs/lab.jpg", "inner-rgts-imgs/science-lab.jpg", "inner-rgts-imgs/reading.jpg", "inner-rgts-imgs/sports.jpg"]))

PAGES["infrastructure"] = ("Infrastructure", inner("Infrastructure", "inner-banners/about-school.jpg",
    P("The premises of St. John's at Gunadala are vast and ideally located for easy access. The design and architecture are modern and aesthetic, and the campus facilities are apt for next-generation schooling.",
      "Each classroom has been designed to provide a vibrant and safe learning environment — tested for adequate lighting and seating distance from the boards, with a colour scheme conducive to learning.")
    + H("Child-Friendly Building and Furniture") + P("The building follows the principle of \"building as a learning aid\", with plenty of open spaces for project work and open learning. Furniture is built from child-friendly materials.")
    + '<div class="sj-tiles">' + "".join(f'<div class="reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in [
        ("Library", "Books on literature, religion and technology in English, Hindi and more."), ("Computer Lab", "Latest computers with inverter and UPS backup. Computer education from Class 1 to 10."),
        ("Multi-Purpose Hall", "A large hall with stage, lighting and sound for cultural and co-curricular activities."), ("Green Park", "Greenery all around for a healthy environment and fresh air."),
        ("Hygienic Water", "RO-filtered, pure drinking water."), ("Grounds", "For athletics and sports.")]) + "</div>",
    ["inner-rgts-imgs/St-Johns-School2.jpg", "inner-rgts-imgs/academics6.jpg", "inner-rgts-imgs/academics7.jpg"]))

PAGES["transport"] = ("Transport &amp; Security", inner("Transport &amp; Security", "inner-banners/transport.jpg",
    P("St. John's has made elaborate transport arrangements for the convenience of the scholars. The fleet of buses covers the entire city with the latest communication devices, so children reach school on time, safely and comfortably.",
      "Every bus has a caretaker to ensure the safety of children in transit. On alighting, students are escorted to their classrooms by ushers appointed for this purpose.",
      "Elaborate security arrangements are in place on campus: staff have proximity cards, and identity cards are issued for students and parents.")
    + H("Bus routes") + '<div class="sj-routes">' + "".join(f'<details class="reveal"><summary>{r}</summary><p>{s}</p></details>' for r, s in [
        ("Route 1", "I Town K.R. Market · Gandhi Mahila Kalasala · Panja Centre · K.B.N. College · Chitti Nagar · Bhavanipuram Road · P.N. Bus Stand · Krishna Lanka · M.G. Road · Benz Circle · Gayatri Nagar"),
        ("Route 2", "Hanuman Pet · Gandhi Nagar · Devi Nagar · Government Press · S.N. Puram · Madhura Nagar · Durga Puram · Sambamurthy Road · Kothavantena"),
        ("Route 3", "Gowtham College opposite street · Janitha Enclave · Ramavarappadu · Gummadi Enclave · Ramavarappadu Ring"),
        ("Route 4", "Eluru Road (Sono Vision, Rama Mandiram) · Suryarao Pet and onwards")]) + "</div>"
    + '<p class="sj-note">Full stop-by-stop route lists are available from the school office.</p>',
    ["inner-rgts-imgs/transport.jpg"]))

PAGES["gallery"] = ("Gallery", inner("Photo Gallery", "inner-banners/gallery.jpg",
    '<p class="sj-lead">Events, festivals, celebrations, competitions, activities and more.</p>'
    + '<div class="sj-albums">' + "".join(f'<button class="sj-album reveal" data-full="{I}{y}.jpg"><img src="{I}{y}.jpg" alt="" loading="lazy"><span>{y.replace("-", " – ")}</span></button>' for y in ("2021-2022", "2015-2016", "2014-2015", "2013-2014")) + "</div>",
    []))

PAGES["alumni"] = ("Alumni", inner("Alumni", "inner-banners/careers.jpg",
    P("The Alumni Network creates opportunities for alumni by building and strengthening a network of former students, and showcases alumni accomplishments.",
      "The management conducts alumni meets at regular intervals on campus. Alumni play a key role in recruiting our students for jobs and internships, and volunteer their time to mentor and coach them.")
    + H("Send us your details") + form("Alumni registration", [("an", "Name", "text", True, None), ("ay", "Year of completion", "select", False, [str(y) for y in range(2026, 1984, -1)]),
        ("ap", "Phone number", "tel", True, None), ("ae", "Email", "email", False, None), ("ao", "Current occupation", "text", False, None)], "Send on WhatsApp", "sj-form"),
    ["inner-rgts-imgs/vision.jpg"]))

PAGES["enquiry"] = ("Enquiry", inner("Admission Enquiry", "inner-banners/about-school.jpg",
    P("Fill in the form and our admissions office will call you back with details of availability, fees and the admission process for your nearest campus.")
    + form("Admission enquiry", [("sn", "Name of the student", "text", True, None), ("pc", "Present class", "text", False, None),
        ("cl", "Class into which admission is sought", "select", True, ["Nursery", "LKG", "UKG"] + [f"Class {n}" for n in range(1, 11)]),
        ("db", "Date of birth", "date", False, None), ("cp", "Preferred campus", "select", False, ["Gunadala", "M.G. Road", "Satyanarayanapuram", "Bhavanipuram"]),
        ("mb", "Mobile", "tel", True, None), ("ms", "Enquiry details", "textarea", False, None)], "Send on WhatsApp", "sj-form"),
    []))

PAGES["contact-us"] = ("Contact Us", inner("Contact Us", "inner-banners/about-school.jpg",
    '<div class="sj-camps">' + "".join(f'<div class="reveal"><h3>{n}</h3><p>{a}</p><p>{" · ".join(f"<a href=&quot;tel:{t.replace(chr(45), str())}&quot;>{t}</a>" for t in ts)}</p></div>'.replace("&quot;", '"') for n, a, ts in [
        ("Gunadala", "Near N.T.R. University of Health Sciences, Gunadala, Vijayawada – 08", ["0866-2452342", "0866-2456789"]),
        ("M.G. Road", "Mohiuddin Estate, M.G. Road, Vijayawada – 10", ["0866-2477140", "0866-2479155"]),
        ("Satyanarayanapuram — A Block", "Near Old Satyanarayanapuram Rly. Gate, BRTS Road, Vijayawada – 11", ["0866-2578855"]),
        ("Satyanarayanapuram — B Block", "Near Old Satyanarayanapuram Rly. Gate, beside Sarada College, BRTS Road, Vijayawada – 11", ["0866-6551888"]),
        ("Bhavanipuram", "Opp. Housing Board Colony, Crombay Road, Swathi Theatre Road, Bhavanipuram, Vijayawada – 12", ["0866-2418855", "0866-2418877"])])
    + '</div><p>E-mail: <a href="mailto:info@stjohnspublicschool.com">info@stjohnspublicschool.com</a></p>',
    []))

CSS = r"""
:root{--sj-blue:#2f5f9f;--sj-navy:#1f3f6e;--sj-sky:#e8f0fa;--sj-ink:#26313f;--sj-muted:#5b6675;--sj-red:#d62839}
body{font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--sj-ink);background:linear-gradient(180deg,#d9dee6,#c9d0db) fixed;-webkit-font-smoothing:antialiased}
.sj-box{max-width:1140px;margin:0 auto;background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.04),0 30px 80px -30px rgba(20,40,80,.35)}
/* header (logo left, small top links, | menu) */
.sj-head{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;padding:16px 34px 0;position:sticky;top:0;background:#fff;z-index:50;border-bottom:1px solid #eef1f5}
.sj-logo img{height:84px;width:auto;margin-bottom:12px}
.sj-hr{display:flex;flex-direction:column;align-items:flex-end;gap:6px}
.sj-toplinks{display:flex;gap:16px;align-items:center;font-size:13px;color:var(--sj-blue)}
.sj-toplinks a:hover,.sj-toplinks a[aria-current]{text-decoration:underline}
.sj-call{display:inline-flex;align-items:center;gap:6px;background:var(--sj-sky);padding:4px 10px;border-radius:999px;font-weight:700}
.sj-nav>ul>li+li>a::before{content:"|";color:#b9c3d0;margin-right:14px;font-weight:400}
.sj-nav>ul>li>a{display:block;padding:10px 0 14px 14px;font-size:15px;font-weight:600;color:#33404f}
.sj-nav>ul>li:first-child>a{padding-left:0}
.sj-nav>ul>li>a:hover,.sj-nav>ul>li>a[aria-current]{color:var(--sj-blue)}
.sj-nav>ul>li>a[aria-current]{box-shadow:inset 0 -3px 0 var(--sj-blue)}
.sj-nav .dd{right:0;left:auto;background:#fff;border-radius:0 0 10px 10px;box-shadow:0 16px 34px rgba(20,40,80,.18);padding:6px 0;border-top:3px solid var(--sj-blue)}
.sj-nav .dd a{padding:9px 18px;font-size:14.5px}
.sj-nav .dd a:hover{background:var(--sj-sky);color:var(--sj-blue)}
.sj-nav .caret{display:none}
.burger{color:var(--sj-blue)}
.sj-adm{display:flex;justify-content:center;align-items:center;gap:18px;background:linear-gradient(90deg,#b7cbe6,#cfdcee,#b7cbe6);color:var(--sj-navy);font-weight:700;padding:9px 16px;font-size:15px;text-align:center;flex-wrap:wrap}
.sj-adm a{background:var(--sj-blue);color:#fff;padding:4px 12px;border-radius:999px;font-size:13px}
/* hero: slider on blue (captions are part of the original banner images) */
.sj-hero{background:linear-gradient(180deg,#2f5f9f,#28568f);padding:22px 22px 0}
.sj-slider{aspect-ratio:940/432;border-radius:10px;overflow:hidden;box-shadow:0 18px 40px -18px rgba(0,0,0,.5)}
.sj-slider .sl{height:100%}
.sj-slider .s-arr{background:rgba(47,95,159,.85);color:#fff}
.sj-slider .sl{position:relative}
.sj-slider .sl-cap{position:absolute;top:0;right:0;bottom:0;width:32.5%;display:flex;flex-direction:column;justify-content:center;gap:14px;padding:26px 30px;color:#fff;text-align:center}
.sj-slider .sl-cap b{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:clamp(15px,1.75vw,22px);line-height:1.35}
.sj-slider .sl-cap p{font-size:clamp(12px,1.1vw,14.5px);color:#dbe7f6;font-weight:600;line-height:1.5}
.sj-slider .sl.on .sl-cap{animation:capin .9s .2s both}
@keyframes capin{from{opacity:0;transform:translateX(16px)}to{opacity:1;transform:none}}
@media (max-width:640px){.sj-slider .sl-cap p{display:none}.sj-slider .sl-cap{padding:10px}}
/* features + announcements on blue */
.sj-features{background:linear-gradient(180deg,#28568f,#234b7d);color:#fff;padding:30px 34px 36px;display:grid;grid-template-columns:2fr 1fr;gap:28px}
.sj-fgrid4{display:grid;grid-template-columns:1fr 1fr;gap:18px 26px}
.sj-feat{display:flex;gap:14px;align-items:flex-start;padding:12px;border-radius:12px;transition:background .2s}
.sj-feat:hover{background:rgba(255,255,255,.08)}
.sj-fi{flex:0 0 46px;height:46px;border-radius:12px;background:#fff;color:var(--sj-blue);display:grid;place-items:center;box-shadow:0 6px 16px -6px rgba(0,0,0,.4)}
.sj-feat h3{font-size:17px;margin-bottom:4px}
.sj-feat p{font-size:14px;color:#d6e3f5;line-height:1.55}
.sj-ann{background:rgba(255,255,255,.1);border-radius:14px;padding:18px 20px;border:1px solid rgba(255,255,255,.15)}
.sj-ann h3{display:flex;gap:8px;align-items:center;font-size:17px;margin-bottom:10px}
.sj-ann ul{list-style:none;display:grid;gap:12px}
.sj-ann li{font-size:14px;color:#e3ecf8;padding-left:12px;border-left:3px solid #ffd166}
.sj-ann a{color:#ffd166;font-weight:700;white-space:nowrap}
/* 3 photo cards */
.sj-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;padding:40px 34px}
.sj-card{display:flex;flex-direction:column;gap:12px}
.sj-cimg{position:relative;border-radius:10px;overflow:hidden;box-shadow:0 12px 30px -16px rgba(20,40,80,.5)}
.sj-cimg img{width:100%;aspect-ratio:294/122;object-fit:cover;transition:transform .5s}
.sj-card:hover .sj-cimg img{transform:scale(1.05)}
.sj-cimg span{position:absolute;left:0;bottom:0;background:var(--sj-blue);color:#fff;font-weight:700;font-size:14px;padding:6px 14px;border-top-right-radius:10px}
.sj-card p{font-size:14.5px;color:var(--sj-muted);flex:1}
.sj-card>a{align-self:flex-end;border:1px solid #cfd8e3;border-radius:8px;padding:5px 14px;font-size:13.5px;color:var(--sj-blue);font-weight:600;transition:.15s}
.sj-card>a:hover{background:var(--sj-blue);color:#fff;border-color:var(--sj-blue)}
/* founders panel */
.sj-founders{display:grid;grid-template-columns:auto auto 1fr;gap:26px;align-items:center;margin:0 34px 40px;background:#f1f3f6;border:1px solid #e3e7ec;border-radius:14px;padding:24px}
.sj-founders figure{background:#fff;padding:10px;border-radius:10px;box-shadow:0 8px 20px -12px rgba(0,0,0,.35);text-align:center;width:170px}
.sj-founders img{width:100%;aspect-ratio:200/256;object-fit:cover;border-radius:6px}
.sj-founders figcaption{font-size:12px;color:var(--sj-muted);margin-top:8px;line-height:1.4}
.sj-founders figcaption b{color:var(--sj-ink)}
.sj-founders p{font-size:15px;color:#3b4654;margin-bottom:10px}
.sj-btn{display:inline-block;background:var(--sj-blue);color:#fff;padding:9px 18px;border-radius:8px;font-weight:700;font-size:14px}
/* inner pages: banner + text + photo column (as original) */
.sj-banner img{width:100%;aspect-ratio:940/230;object-fit:cover}
.sj-inner{display:grid;grid-template-columns:1fr 280px;gap:34px;padding:34px}
.sj-inner:not(:has(.sj-side)){grid-template-columns:1fr}
.sj-h1{font-size:30px;color:var(--sj-blue);font-weight:700;padding-bottom:10px;margin-bottom:18px;border-bottom:2px solid var(--sj-sky);position:relative}
.sj-h1::after{content:"";position:absolute;left:0;bottom:-2px;width:80px;height:2px;background:var(--sj-blue)}
.sj-h2{font-size:20px;color:var(--sj-navy);margin:26px 0 10px}
.sj-main p{margin-bottom:14px;color:#3b4654}
.sj-main a{color:var(--sj-blue);font-weight:600}
.sj-lead{font-size:17px}
.sj-side{display:flex;flex-direction:column;gap:14px}
.sj-side img{width:100%;border-radius:10px;box-shadow:0 12px 28px -14px rgba(20,40,80,.5);border:4px solid #fff}
.sj-quote{background:var(--sj-sky);border-left:4px solid var(--sj-blue);border-radius:10px;padding:18px 20px;font-style:italic;color:#2c3a4b}
.sj-quote cite{display:block;margin-top:10px;font-style:normal;font-weight:700;color:var(--sj-blue)}
.sj-ticks{list-style:none;display:grid;gap:8px}
.sj-ticks li{padding-left:28px;position:relative;color:#3b4654}
.sj-ticks li::before{content:"✓";position:absolute;left:0;top:1px;width:20px;height:20px;border-radius:50%;background:var(--sj-sky);color:var(--sj-blue);font-weight:800;font-size:12px;display:grid;place-items:center}
.sj-ach{display:grid;gap:18px}
.sj-ach article{display:grid;grid-template-columns:180px 1fr;gap:18px;background:#f7f9fc;border-radius:12px;padding:16px;border:1px solid #e6ebf2}
.sj-ach article:not(:has(img)){grid-template-columns:1fr}
.sj-ach img{width:100%;border-radius:8px;object-fit:cover}
.sj-ach h3{color:var(--sj-navy);font-size:17px;margin-bottom:6px}
.sj-tiles{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}
.sj-tiles div{background:#f7f9fc;border:1px solid #e6ebf2;border-radius:12px;padding:16px;border-top:3px solid var(--sj-blue)}
.sj-tiles h3{font-size:16px;color:var(--sj-navy);margin-bottom:4px}
.sj-tiles p{font-size:14px;margin:0}
.sj-routes details{border:1px solid #e3e8ef;border-radius:10px;padding:12px 16px;margin-bottom:8px;background:#fafbfd}
.sj-routes summary{font-weight:700;color:var(--sj-blue);cursor:pointer}
.sj-routes p{margin:8px 0 0;font-size:14.5px}
.sj-note{font-size:14px;color:var(--sj-muted)}
.sj-albums{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.sj-album{position:relative;border:0;padding:0;border-radius:12px;overflow:hidden;cursor:zoom-in;box-shadow:0 12px 28px -14px rgba(20,40,80,.5)}
.sj-album img{width:100%;aspect-ratio:4/3;object-fit:cover}
.sj-album span{position:absolute;left:0;right:0;bottom:0;background:linear-gradient(transparent,rgba(20,40,80,.85));color:#fff;font-weight:700;padding:28px 14px 12px;text-align:left}
.sj-gal{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.gi{border:0;padding:0;border-radius:8px;overflow:hidden;aspect-ratio:4/3;cursor:zoom-in;background:#eef2f7}
.gi img{width:100%;height:100%;object-fit:cover}
.sj-camps{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}
.sj-camps div{background:#f7f9fc;border:1px solid #e6ebf2;border-radius:12px;padding:16px;border-left:4px solid var(--sj-blue)}
.sj-camps h3{color:var(--sj-navy);font-size:17px;margin-bottom:4px}
.sj-camps p{font-size:14.5px;margin-bottom:4px}
/* forms */
.sj-form{display:grid;grid-template-columns:1fr 1fr;gap:12px;background:#f7f9fc;border:1px solid #e6ebf2;border-radius:14px;padding:20px;margin-top:10px}
.sj-form .fld{display:grid;gap:4px}
.sj-form .fld:last-of-type{grid-column:1/-1}
.sj-form label{font-size:13px;font-weight:700;color:var(--sj-navy)}
.sj-form input,.sj-form select,.sj-form textarea{font:inherit;font-size:15px;padding:10px 12px;border:1px solid #cfd8e3;border-radius:8px;background:#fff;width:100%}
.sj-form input:focus,.sj-form select:focus,.sj-form textarea:focus{outline:none;border-color:var(--sj-blue);box-shadow:0 0 0 3px rgba(47,95,159,.15)}
.sj-form .enq-btn{grid-column:1/-1;justify-self:start;border:0;border-radius:8px;padding:11px 22px;background:var(--sj-blue);color:#fff;font-weight:700}
/* footer */
.sj-foot{background:#2c2f34;color:#c4c9d1;font-size:14.5px}
.sj-fgrid{display:grid;grid-template-columns:1.3fr 1fr 1.3fr;gap:28px;padding:34px}
.sj-flogo{height:58px;background:#fff;border-radius:8px;padding:4px 8px;margin-bottom:10px}
.sj-foot h4{color:#fff;font-size:14px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px}
.sj-foot ul{list-style:none;display:grid;gap:6px}
.sj-foot a:hover{color:#fff}
.sj-copy{border-top:1px solid #42464d;padding:14px 34px;font-size:13px;color:#9aa1ab}
.sj-float{position:fixed;right:18px;bottom:18px;z-index:45;display:flex;gap:8px;align-items:center;background:var(--sj-blue);color:#fff;font-weight:700;padding:11px 16px;border-radius:999px;box-shadow:0 14px 30px -10px rgba(47,95,159,.7);font-size:14px}
@media (max-width:980px){
  .sj-head{align-items:center;padding:10px 18px;flex-wrap:wrap}
  .sj-logo img{height:62px;margin:0}
  .sj-hr{flex-direction:row-reverse;align-items:center}
  .sj-toplinks a:not(.sj-call){display:none}
  .sj-nav>ul{background:#fff;box-shadow:0 18px 40px rgba(20,40,80,.18);right:0;left:auto;width:min(320px,90vw)}
  .sj-nav>ul>li>a{padding:12px 18px !important;border-bottom:1px solid #eef1f5}
  .sj-nav>ul>li+li>a::before{display:none}
  .sj-nav .dd{border-top:0;box-shadow:none;background:#f6f8fb}
  .sj-features{grid-template-columns:1fr;padding:24px 18px}
  .sj-cards{grid-template-columns:1fr;padding:28px 18px}
  .sj-founders{grid-template-columns:1fr 1fr;margin:0 18px 28px}
  .sj-founders>div{grid-column:1/-1}
  .sj-founders figure{width:auto}
  .sj-inner{grid-template-columns:1fr;padding:24px 18px}
  .sj-side{flex-direction:row;overflow-x:auto}
  .sj-side img{width:220px;flex:0 0 auto}
  .sj-fgrid{grid-template-columns:1fr;padding:24px 18px}
  .sj-hero{padding:12px 12px 0}
}
@media (max-width:640px){
  .sj-fgrid4,.sj-tiles,.sj-albums,.sj-camps,.sj-form{grid-template-columns:1fr}
  .sj-gal{grid-template-columns:1fr 1fr}
  .sj-ach article{grid-template-columns:1fr}
  .sj-adm{font-size:13.5px}
}
"""

if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    for f in out.glob("*.html"):
        f.unlink()
    write_site(out, S, PAGES, CSS, header, footer)
