# -*- coding: utf-8 -*-
"""Andhra Hospitals (andhrahospitals.org) — redesign preview. Build: python3 site.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_template"))
from sitegen import *  # noqa

A = "https://andhrahospitals.org/assets/"
S = {
    "name": "Andhra Hospitals", "domain": "andhrahospitals.org",
    "description": "Andhra Hospitals, Vijayawada — multi-speciality hospital group with 24×7 emergency, paediatrics, cardiac and critical care across Andhra Pradesh.",
    "primary": "#d0101e", "secondary": "#0050a0",
    "logo": A + "uploads/logos/logo_new_(2)1.png", "logo_style": "",
    "phone": "0866 2574757", "phone_tel": "+918662574757",
    "address": "C.V.R. Complex, Prakasam Road, Vijayawada – 520002, Krishna Dist., Andhra Pradesh",
    "bar_label": "24×7 Emergency &amp; Ambulance",
    "ticker": ["Appointments: 0866 2574757", "3,500+ free heart surgeries completed", "24×7 laboratory, pharmacy &amp; ACLS ambulance", "Health check-up packages for men &amp; women"],
    "cta": ("Book appointment", "contact.html#book"), "mbar_label": "Book", "fab": "Book on WhatsApp", "desk": "appointments desk",
    "tabs": [("index", "Home"), ("about", "About"), ("specialities", "Specialities"), ("services", "24×7 Services"), ("locations", "Locations"), ("contact", "Contact")],
    "footer_text": "Exemplary physical, emotional and spiritual care for every patient and family — guided by a commitment to excellence and leadership.",
    "footer_contact_title": "Reach us", "footer_contacts": ['<a href="mailto:info@andhrahospitals.org">info@andhrahospitals.org</a>', "NABH-accredited care"],
}

SPECS = [  # (image, name, colour)
    (A + "uploads/departments/lapro-scopic-surgery1.jpg", "General &amp; Laparoscopic Surgery", "#d0101e"),
    (A + "uploads/departments/gas.jpg", "Gastroenterology", "#0050a0"),
    (A + "images/neo.jpg", "Neonatology &amp; Paediatrics", "#e07a00"),
    (A + "uploads/departments/gyna.jpg", "Obstetrics &amp; Gynaecology", "#b0125b"),
    (A + "uploads/departments/neuro.jpg", "Neurology &amp; Neurosurgery", "#4f46e5"),
]

PAGES = {}
PAGES["index"] = ("Home",
    slider([
        (A + "uploads/banner_imgs/banner2.jpg", "Andhra Hospitals · Vijayawada", "The people's pulse.",
         "Multi-speciality care with 24×7 emergency, critical care and paediatric intensive care — close to home across Andhra Pradesh.",
         [("Book appointment →", "contact.html#book", "btn-red"), ("Emergency 0866 2574757", "tel:+918662574757", "btn-white")], "p"),
        (A + "uploads/services/Untitled-3.jpg", "Critical care", "Expert care, every hour of every day.",
         "ICUs, laminar airflow theatres, ECMO for newborns, children and adults, and a 24×7 ACLS ambulance.",
         [("24×7 services →", "services.html", "btn-red")], "s"),
        ("http://andhrahospitals.org/img/seeinside.jpg", "Healing little hearts", "3,500+ free heart surgeries completed.",
         "Charity work in association with Healing Little Hearts, UK, and the Swarna Bharath Trust.",
         [("About us →", "about.html", "btn-red")], "p"),
    ])
    + strip([("pulse", "Find a doctor", "Search by speciality and location", "specialities.html", False),
             ("heart", "Health check-up packages", "Packages for men &amp; women", "contact.html#book", False),
             ("ambulance", "24×7 Emergency", "0866 2574757", "tel:+918662574757", True)])
    + two_col("About Andhra Hospitals", "We recognise the value of every person.",
              "Andhra Hospitals provides exemplary physical, emotional and spiritual care for each patient and their family, with an array of medical and surgical services backed by the latest technology — and 24-hour urgent care.",
              photo(A + "uploads/banner_imgs/banner2.jpg", "Andhra Hospitals building"), ("Read more", "about.html"))
    + section(head_("Specialities", "Care for every stage of life.") + tiles([(i, n, "specialities.html", c) for i, n, c in SPECS]), "alt")
    + section(head_("Why families choose us", "Built around patients.") + stats([
        ("heart", "3,500+", 3500, "Free heart surgeries completed"), ("building", "6", 6, "Centres across Andhra Pradesh"),
        ("clock", "24×7", None, "Emergency, lab, pharmacy &amp; ambulance"), ("shield", "NABH", None, "Accredited quality standards")]))
    + cta_band("Need a specialist?", "Book in a minute on WhatsApp, or call us any time — day or night.", ("Book appointment", "contact.html#book"), "0866 2574757"))

PAGES["about"] = ("About",
    page_hero("About", "Our mission: the people's pulse.", "Exemplary care for every patient and family, with social responsibility at the heart of what we do.", A + "uploads/banner_imgs/banner2.jpg")
    + two_col("Who we are", "Excellence, leadership and a tradition of caring.",
              "We demonstrate our commitment by providing exemplary physical, emotional and spiritual care for each of our patients and their families, and by using our resources responsibly.",
              photo(A + "uploads/services/Untitled-3.jpg", "Hospital ward"),
              extra="<p class='muted-p'>The commitment of our staff, physicians and community partners lets us keep a quality of presence and a tradition of caring — and a compassionate environment where our team can deliver the best care every hour of every day.</p>")
    + section(head_("Charity work", "Care that reaches beyond our walls.") + icon_cards([
        ("heart", "Healing Little Hearts, UK", "Andhra Hospitals works with Healing Little Hearts, UK, on free heart surgeries — more than 3,500 completed."),
        ("users", "Community campaigns", "Awareness campaigns supported by well-known public figures, bringing heart care to more families."),
        ("star", "Swarna Bharath Trust", "Andhra Hospitals works in association with the Swarna Bharath Trust on charitable care.")]), "alt mint"))

PAGES["specialities"] = ("Specialities",
    page_hero("Specialities", "More than 25 specialities under one group.", "From newborn intensive care to joint replacement and oncology.", A + "uploads/services/Untitled-3.jpg")
    + section(head_("Departments", "Our specialities", "Tap a department to book a consultation.") + icon_cards([
        ("pulse", "Surgical Gastroenterology", "Advanced surgery of the stomach, liver, pancreas and intestines."),
        ("scan", "General &amp; Laparoscopic Surgery", "Keyhole surgery for faster recovery and shorter stays."),
        ("heart", "General Medicine", "Diagnosis and treatment of adult illnesses."),
        ("baby", "Neonatology", "Specialised care for newborns, including NICU."),
        ("baby", "General Paediatrics", "Complete care for infants, children and adolescents."),
        ("shield", "Paediatric Intensive Care", "24×7 PICU with ECMO support."),
        ("pulse", "Medical Gastroenterology", "Endoscopy and treatment of digestive disorders."),
        ("heart", "Obstetrics &amp; Gynaecology", "Pregnancy, childbirth and women's health."),
        ("heart", "Fetal &amp; Maternal Medicine", "High-risk pregnancy care and fetal scanning."),
        ("ambulance", "Critical Care", "Intensive care for the most seriously ill."),
        ("ambulance", "Emergencies &amp; Trauma", "Round-the-clock emergency response."),
        ("bone", "Joint Replacement &amp; Orthopaedics", "Bones, joints, sports injuries and replacements."),
        ("bone", "Rheumatology", "Arthritis and autoimmune conditions."),
        ("brain", "Neurology &amp; Neurosurgery", "Brain, spine and nerve care, medical and surgical."),
        ("lab", "Urology &amp; Nephrology", "Kidney and urinary care, including haemodialysis."),
        ("pulse", "Pulmonology", "Lung and breathing disorders."),
        ("scan", "Radiology", "CT, ultrasound, colour Doppler and fetal scanning."),
        ("shield", "Surgical &amp; Medical Oncology", "Cancer surgery and medical treatment."),
        ("users", "ENT", "Ear, nose and throat care."),
        ("users", "Physiotherapy &amp; Child Development Centre", "Rehabilitation and developmental support for children."),
    ], cols=4)))

PAGES["services"] = ("24×7 Services",
    page_hero("24×7 Services", "Support services that never close.", "Diagnostics, pharmacy and ambulance — round the clock.", A + "uploads/banner_imgs/banner2.jpg")
    + section(icon_cards([
        ("lab", "24×7 Laboratory", "Round-the-clock tests with a central laboratory."), ("pill", "24×7 Pharmacy", "Medicines available at any hour."),
        ("ambulance", "24×7 Ambulance (ACLS)", "Advanced cardiac life support on the way."), ("heart", "ECMO", "For newborns, children and adults."),
        ("scan", "CT &amp; Ultrasound", "CT scan, ultrasound, colour Doppler and fetal scanning."), ("pulse", "Cardiac &amp; Neuro tests", "2D Echo, ECG, EEG, ENMG and NCS."),
        ("shield", "Laminar airflow theatres", "Sterile operating theatres with CSSD support."), ("building", "Liquid oxygen", "Uninterrupted piped oxygen supply.")], cols=4))
    + section(head_("Health check-ups", "Packages for men &amp; women.", "Ask for the tests and prices on WhatsApp.") + '<p style="text-align:center"><a class="btn btn-red" href="contact.html#book">Ask about packages →</a></p>', "alt mint"))

PAGES["locations"] = ("Locations",
    page_hero("Locations", "Six centres across Andhra Pradesh.", "Find the Andhra Hospitals centre nearest to you.", A + "uploads/banner_imgs/banner2.jpg")
    + section(locations([
        ("Andhra Hospitals — Vijayawada", "C.V.R. Complex, Prakasam Road, Vijayawada – 520002", ["0866 2574757"]),
        ("Heart &amp; Brain Institute", "Vijayawada", ["0866 2574757"]),
        ("Andhra Hospitals — Bhavanipuram", "Bhavanipuram, Vijayawada", ["0866 2574757"]),
        ("Andhra Hospitals — Eluru", "Eluru, Andhra Pradesh", ["0866 2574757"]),
        ("Andhra Hospitals — Machilipatnam", "Machilipatnam, Andhra Pradesh", ["0866 2574757"]),
        ("Andhra Hospitals — Visakhapatnam", "Visakhapatnam, Andhra Pradesh", ["0866 2574757"])])
      + '<p class="note" style="text-align:center;margin-top:18px">Centre-specific addresses and phone numbers to be confirmed with the hospital before launch.</p>'))

PAGES["contact"] = ("Contact",
    page_hero("Contact", "We're here 24×7.", "Call, WhatsApp, or book online — our team will contact you within 24 hours.", A + "uploads/banner_imgs/banner2.jpg")
    + f'<section id="book"><div class="wrap two-col" style="align-items:start">'
    + f'<div class="reveal"><div class="eyebrow">Hassle-free appointments</div><h2 class="h2">Book in under a minute.</h2><p class="lede">Send your details on WhatsApp and our appointments desk will confirm your slot.</p>'
    + f'<div class="info"><div class="card"><span class="ic">{ic("phone", 20)}</span><span><b>Phone</b><a href="tel:+918662574757">0866 2574757</a></span></div>'
    + f'<div class="card"><span class="ic">{ic("mail", 20)}</span><span><b>Email</b><a href="mailto:info@andhrahospitals.org">info@andhrahospitals.org</a></span></div>'
    + f'<div class="card"><span class="ic">{ic("pin", 20)}</span><span><b>Address</b><p>C.V.R. Complex, Prakasam Road, Vijayawada – 520002</p><a href="https://www.google.com/maps/search/?api=1&query=Andhra+Hospitals+Prakasam+Road+Vijayawada" target="_blank" rel="noopener">Get directions →</a></span></div></div></div>'
    + enquiry_form("Appointment request", [("fn", "Patient name", "text", True, None), ("ph", "Mobile number", "tel", True, None),
        ("dp", "Department", "select", False, ["General Medicine", "Paediatrics", "Obstetrics &amp; Gynaecology", "Gastroenterology", "Orthopaedics", "Neurology", "Cardiology", "Health check-up", "Not sure"]),
        ("dt", "Preferred date", "date", False, None), ("ms", "Message", "textarea", False, None)],
        "Send on WhatsApp", "In an emergency, call 0866 2574757 — don't wait.")
    + "</div></section>")

if __name__ == "__main__":
    build(S, PAGES, Path(__file__).resolve().parent)
