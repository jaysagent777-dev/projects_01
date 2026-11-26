# Praveen Hospitals: current site vs. redesign

Pitch backup. Every "Current site" point was checked on praveenhospitals.com (all 8 pages) on 26 Nov 2026. Re-check before the call.
Goes with `PITCH.md` in this folder.

## Summary: three things to lead with

1. **Patients can act from their phone.** The current site has **no tap-to-call links on any page** and no WhatsApp. The redesign has 53 tap-to-call links across its pages, WhatsApp booking, and a fixed Call / WhatsApp / Book bar on mobile.
2. **Telugu.** The current site is English only. The redesign has full Telugu on every page, switched with one tap.
3. **Credibility.** The current site has a typo in its main About paragraph, a broken email link, the wrong word in its stats, and old copyright and year text. The redesign fixes all of these and shows the outcome numbers prominently.

---

## Side-by-side

| Area | Current site (praveenhospitals.com) | Redesign | Why it matters |
|---|---|---|---|
| **Calling** | Phone numbers are plain text. There are 0 `tel:` links on all 8 pages, so a patient on a phone has to copy and dial the number. | Every number is tappable. "Emergency: 0866-2444440" appears in the hero, footer and CTA band. | In an emergency, one tap matters. |
| **Booking** | The only booking option is "For appointments contact 0866-2444440". The contact form posts to an AWS endpoint whose path ends in `/dev/` (a test stage), so it's unclear whether messages arrive. | A Book appointment form (name, mobile, department) sends the request to the front desk on WhatsApp. WhatsApp buttons are on every page. | Turns visits into appointments. |
| **Email link** | The header email link is `href="praveencardiaccentre@gmail.com"` with no `mailto:`, so clicking it opens a broken page. | A working `mailto:` link. | Small, but it's broken today. |
| **Language** | English only. | Full English and Telugu, switched with one tap at the top. | Patients come from Jaggaiahpet, Kodad and nearby Telugu-speaking towns. |
| **Mobile layout** | Bootstrap 3 (2016). On a phone, the logo plus a stacked contact block take up the first screen before any content. The home page is about 7,000px long. | Built mobile-first. The hero, Book button and emergency number all show on the first screen, with a fixed action bar at the bottom. | Most patients search on a phone. |
| **About text** | "The **senator** whose foundation was laid in 2007…" appears on both Home and About (it should say "centre"). | Rewritten: "Dr. Praveen Maddirala… founded the Praveen Cardiac Centre in Vijayawada in 2007. Today it is a 100-bed hospital…" | A typo in the first paragraph hurts trust. |
| **Stats wording** | "Cardiac Electro Physiology & Radio Frequency **ambulation**" (it should say ablation). | "Cardiac EP & RF ablation". | A doctor will notice this. |
| **Outcome numbers** | Split across pages in plain text: "3800 interventions" on Home, "4000 stents, 99.6%" on Services. "During the last 14 years" is out of date, since 2007 was 19 years ago. | Stat cards with icons and count-up animation, labelled "Figures as reported by Praveen Hospitals". | Their record (11,500+ angiograms, 99.6% stent success) is the strongest selling point. |
| **Dr. Praveen's credentials** | Long paragraph on the About page only. | Large portrait with name and MD, DM (Cardiology) on Home and About. Credentials, the gold medal and NIMS are laid out clearly. | Patients choose a cardiologist they trust. |
| **Health camps** | Static text: "Wednesday at Jaggaiahpet, 2nd & 4th Sunday at Kodad". | A camp strip that **calculates and shows the next camp date** for each location. | Turns a notice into a reason to visit. |
| **Empanelments** | A plain list of 12 schemes. A commented-out heading ("Railways and CS (MA) – will be added soon") is still in the page source. | All schemes shown as cards, plus a simple guide to cashless treatment (Aarogyasri, EHS, ECHS, all TPA insurance). | Cashless treatment is a deciding factor for many families. |
| **Health checkups** | A one-line notice: "General, Master, Executive, Total Body – Available". | Package cards, each with "ask on WhatsApp for tests and price". | Health checkups bring in repeat, non-emergency revenue. |
| **Page titles / Google** | 7 of 8 pages have the same title, "Praveen Hospitals". Every page has the same meta description. No structured data. | Each page has its own title and its own description. Every page also carries schema.org `Hospital` structured data: address, map location, all 3 phones, 24×7 hours, specialities, procedures and founder. | Google can show the hospital correctly, with its phone, hours and map. |
| **Welcome message on phones** | The "Welcome to Praveen Hospitals" caption is taller than the slider (232px of text in a 167px slide), so "Welcome to" is cut off at the top and the paragraph is cut off at the bottom. Screenshot: `evidence/live-mobile-welcome-cut-off.png`. | The hero headline, Book button and emergency number fit on the first screen. | The first thing a patient sees on a phone is broken. |
| **Map** | A 2016 Google Maps embed labelled "Praveen Cardiac Centre". | Map plus a one-tap "Open in Google Maps" button for directions. | Directions on a phone in one tap. |
| **Gallery / video** | Photo grid and a raw `<video>` tag. | Lightbox gallery, and the surgery video is labelled "Contains surgical footage". | Looks polished and is considerate to viewers. |
| **Speed / code** | Loads Bootstrap 3, jQuery 1.12, Font Awesome, Ionicons and animate.css from 5 CDNs. The contact page also loads the **unminified development build of Vue (341 KB)**, axios and vee-validate. | One small CSS file and one 9 KB script, with no frameworks. Images load lazily. | Faster on 4G in smaller towns. |
| **Accessibility** | 1 image on the home page has no alt text. The slider has no labels. | All images have alt text, the slider has ARIA labels, and animation turns off for users who set "reduce motion". | Usable by more people, and good practice. |
| **Footer** | "Copyright (c) ." with the year missing on 7 pages, and "(c) 2016" on Services. | "© 2026 Praveen Hospitals, Vijayawada". | Makes the site look maintained. |

---

## Pitch claims: checked and fixed (26 Nov 2026)

- **Google search claim:** it's now true. Added `Hospital` structured data and a separate description to every page in `build.py`, then rebuilt. Test after go-live with Google's Rich Results Test. The preview is `noindex`, so Google won't read it until then.
- **"Welcome heading cut off on phones":** confirmed at 375px wide (see the screenshot in `evidence/`). It stays in the pitch.
- **"Numbers differ between pages":** replaced in `PITCH.md` with stronger, verified points: no tap-to-call, the broken email link, and "ambulation" instead of "ablation".

## Not done yet (expected, it's a preview)

- WhatsApp number is set to the mobile on their site (+91 99488 78877). Confirm the front-desk number.
- Telugu still needs a native-speaker review.
- Checkup package tests and prices are placeholders.
- Photos and video are loaded from their current server. Host them yourself before go-live.
- `noindex`, the preview banner and the password are still on, which is correct for a preview.
