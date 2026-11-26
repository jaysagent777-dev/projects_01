// Praveen Hospitals redesign preview — shared script for all pages.
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
