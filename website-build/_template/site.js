// Shared script for template-built redesign previews.
// Forms never send anything in preview: they show the composed WhatsApp message instead.
const PREVIEW = true;
const $ = (id) => document.getElementById(id);

// tabs: keep the current tab in view on narrow screens
const tabList = document.querySelector(".tabs ul"), curTab = document.querySelector(".tabs a[aria-current]");
if (tabList && curTab) {
  tabList.scrollLeft = curTab.parentElement.offsetLeft - (tabList.clientWidth - curTab.offsetWidth) / 2;
  const fade = () => tabList.parentElement.style.setProperty("--fade", tabList.scrollLeft + tabList.clientWidth >= tabList.scrollWidth - 4 ? 0 : 1);
  tabList.addEventListener("scroll", fade, { passive: true }); addEventListener("resize", fade); fade();
}

// header shrink + back to top
const hdr = document.querySelector("header"), toTop = document.querySelector(".to-top");
const onScroll = () => { hdr && hdr.classList.toggle("scrolled", scrollY > 40); toTop && toTop.classList.toggle("show", scrollY > 600); };
addEventListener("scroll", onScroll, { passive: true }); onScroll();
if (toTop) toTop.addEventListener("click", () => scrollTo({ top: 0, behavior: "smooth" }));

// slider
const hero = document.querySelector(".hero2");
if (hero) {
  const slides = [...hero.querySelectorAll(".slide")], dots = [...hero.querySelectorAll(".dots button")];
  let i = 0, timer = null; const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const go = (n) => { slides[i].classList.remove("on"); dots[i].removeAttribute("aria-current"); i = (n + slides.length) % slides.length; slides[i].classList.add("on"); dots[i].setAttribute("aria-current", "true"); };
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

// counters
const counters = document.querySelectorAll(".count[data-to]");
if (counters.length && "IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const co = new IntersectionObserver(es => es.forEach(en => {
    if (!en.isIntersecting) return; co.unobserve(en.target);
    const el = en.target, to = +el.dataset.to, t0 = performance.now(), dur = 1400;
    const step = (now) => { const p = Math.min((now - t0) / dur, 1); el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))).toLocaleString("en-IN"); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0"; requestAnimationFrame(step);
  }), { threshold: .4 });
  counters.forEach(c => co.observe(c));
}

// enquiry form -> WhatsApp message (preview shows it instead of sending)
const form = $("enqForm"), modal = $("modal");
if (form) {
  form.querySelectorAll('input[type="date"]').forEach(d => d.min = new Date().toISOString().slice(0, 10));
  form.addEventListener("submit", e => {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    const lines = [form.dataset.title + " — " + (window.SITE && SITE.name)];
    form.querySelectorAll("[data-label]").forEach(f => { const v = f.value.trim(); if (v) lines.push(f.dataset.label + ": " + (f.type === "date" ? new Date(v + "T00:00").toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }) : v)); });
    const text = lines.join("\n");
    if (PREVIEW || !(window.SITE && SITE.whatsapp)) { $("mText").textContent = text; modal.classList.add("open"); return; }
    window.open("https://wa.me/" + SITE.whatsapp + "?text=" + encodeURIComponent(text), "_blank", "noopener");
  });
}
if (modal) { $("mClose").addEventListener("click", () => modal.classList.remove("open")); modal.addEventListener("click", e => { if (e.target === modal) modal.classList.remove("open"); }); }

// lightbox: prev / next within the clicked photo's album ([data-group]), arrow keys and swipe
const lb = $("lightbox");
if (lb) {
  const img = lb.querySelector("img"), num = lb.querySelector(".lb-n");
  let set = [], idx = 0, x0 = null;
  const show = i => { idx = (i + set.length) % set.length; img.src = set[idx].dataset.full; if (num) num.textContent = set.length > 1 ? (idx + 1) + " / " + set.length : ""; lb.classList.toggle("multi", set.length > 1); };
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-full]"); if (!b || lb.contains(b)) return;
    const g = b.closest("[data-group]") || document; set = [...g.querySelectorAll("[data-full]")]; show(set.indexOf(b)); lb.classList.add("open");
  });
  lb.addEventListener("click", e => {
    if (e.target.closest(".lb-prev")) return show(idx - 1);
    if (e.target.closest(".lb-next")) return show(idx + 1);
    if (e.target !== img) lb.classList.remove("open");
  });
  addEventListener("keydown", e => { if (!lb.classList.contains("open")) return; if (e.key === "ArrowLeft") show(idx - 1); if (e.key === "ArrowRight") show(idx + 1); });
  lb.addEventListener("touchstart", e => { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", e => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) show(idx + (dx < 0 ? 1 : -1)); x0 = null; });
}
addEventListener("keydown", e => { if (e.key === "Escape") { modal && modal.classList.remove("open"); lb && lb.classList.remove("open"); } });

// reveal on scroll
const io = "IntersectionObserver" in window ? new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }), { threshold: .1 }) : null;
document.querySelectorAll(".reveal").forEach(el => io ? io.observe(el) : el.classList.add("in"));
