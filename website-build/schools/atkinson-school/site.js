// Shared behaviour for "classic" redesigns (original layout kept). Preview mode: forms never send.
const $ = (id) => document.getElementById(id);

// mobile menu + tap-to-open dropdowns on small screens
document.querySelectorAll(".nv").forEach(nv => {
  const b = nv.querySelector(".burger");
  if (b) b.addEventListener("click", () => { const o = nv.classList.toggle("open"); b.setAttribute("aria-expanded", String(o)); });
  nv.querySelectorAll(".has-dd > a").forEach(a => a.addEventListener("click", e => {
    if (matchMedia("(max-width:980px)").matches) { e.preventDefault(); a.parentElement.classList.toggle("sub-open"); }
  }));
});

// sliders
document.querySelectorAll(".slider").forEach(sl => {
  const slides = [...sl.querySelectorAll(".sl")], dots = [...sl.querySelectorAll(".s-dots button")];
  if (slides.length < 2) { sl.querySelectorAll(".s-arr,.s-dots").forEach(x => x.remove()); return; }
  let i = 0, t = null; const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const go = n => { slides[i].classList.remove("on"); dots[i] && dots[i].removeAttribute("aria-current"); i = (n + slides.length) % slides.length; slides[i].classList.add("on"); dots[i] && dots[i].setAttribute("aria-current", "true"); };
  const play = () => { if (!reduce) { clearInterval(t); t = setInterval(() => go(i + 1), 5500); } };
  sl.querySelector(".s-next").addEventListener("click", () => { go(i + 1); play(); });
  sl.querySelector(".s-prev").addEventListener("click", () => { go(i - 1); play(); });
  dots.forEach((d, n) => d.addEventListener("click", () => { go(n); play(); }));
  sl.addEventListener("mouseenter", () => clearInterval(t)); sl.addEventListener("mouseleave", play);
  let x0 = null;
  sl.addEventListener("touchstart", e => { x0 = e.touches[0].clientX; }, { passive: true });
  sl.addEventListener("touchend", e => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) { go(i + (dx < 0 ? 1 : -1)); play(); } x0 = null; });
  play();
});

// enquiry forms -> WhatsApp message shown in a modal (preview)
const modal = $("modal");
document.querySelectorAll("form.enq").forEach(f => {
  f.querySelectorAll('input[type="date"]').forEach(d => d.min = new Date().toISOString().slice(0, 10));
  f.addEventListener("submit", e => {
    e.preventDefault();
    if (!f.checkValidity()) { f.reportValidity(); return; }
    const lines = [f.dataset.title + " — " + (window.SITE && SITE.name)];
    f.querySelectorAll("[data-label]").forEach(x => { const v = x.value.trim(); if (v) lines.push(x.dataset.label + ": " + (x.type === "date" ? new Date(v + "T00:00").toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }) : v)); });
    $("mText").textContent = lines.join("\n"); modal.classList.add("open");
  });
});
if (modal) { $("mClose").addEventListener("click", () => modal.classList.remove("open")); modal.addEventListener("click", e => { if (e.target === modal) modal.classList.remove("open"); }); }

// lightbox
const lb = $("lightbox");
if (lb) {
  document.querySelectorAll("[data-full]").forEach(b => b.addEventListener("click", () => { lb.querySelector("img").src = b.dataset.full; lb.classList.add("open"); }));
  lb.addEventListener("click", e => { if (e.target !== lb.querySelector("img")) lb.classList.remove("open"); });
}
addEventListener("keydown", e => { if (e.key === "Escape") { modal && modal.classList.remove("open"); lb && lb.classList.remove("open"); } });

// click-to-play YouTube (loads the player only when asked)
document.querySelectorAll("[data-yt]").forEach(v => v.addEventListener("click", () => {
  if (v.querySelector("iframe")) return;
  v.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${v.dataset.yt}?autoplay=1&rel=0" title="Video" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>`;
}));

// reveal on scroll
const io = "IntersectionObserver" in window ? new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }), { threshold: .1 }) : null;
document.querySelectorAll(".reveal").forEach(el => io ? io.observe(el) : el.classList.add("in"));
