from typing import Optional
#!/usr/bin/env python3
"""
Instagram carousel slide generator — news magazine style.
Matches real viral news accounts: coloured header strip, real photo,
bold overlaid text, clean source branding.
"""

import io, requests
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

IMAGES_DIR = Path("generated_images")
IMAGES_DIR.mkdir(exist_ok=True)

W, H = 1080, 1080

# Source brand colors (header strip bg, text)
SOURCE_BRAND = {
    "REUTERS":    {"bg": (255, 40,  40),  "fg": (255, 255, 255), "name": "REUTERS"},
    "BBC":        {"bg": (255, 40,  40),  "fg": (255, 255, 255), "name": "BBC NEWS"},
    "TECHCRUNCH": {"bg": (20,  20,  20),  "fg": (30,  215, 96),  "name": "TECHCRUNCH"},
    "GUARDIAN":   {"bg": (0,   61,  99),  "fg": (255, 255, 255), "name": "THE GUARDIAN"},
}
DEFAULT_BRAND = {"bg": (20, 20, 20), "fg": (255, 200, 0), "name": "WORLD NEWS"}

# ── Fonts ─────────────────────────────────────────────────────────────────────

_FONT_CACHE: dict = {}

def _ensure_fonts():
    """Download fonts to /tmp if not already present."""
    import urllib.request
    fonts = {
        "regular": ("/tmp/NotoSans-Regular.ttf",
                    "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf"),
        "bold":    ("/tmp/NotoSans-Bold.ttf",
                    "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Bold.ttf"),
    }
    for key, (path, url) in fonts.items():
        if not Path(path).exists():
            try:
                urllib.request.urlretrieve(url, path)
            except Exception:
                pass

def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    key = (size, bold)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]

    _ensure_fonts()

    candidates = [
        "/tmp/NotoSans-Bold.ttf" if bold else "/tmp/NotoSans-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                f = ImageFont.truetype(p, size)
                _FONT_CACHE[key] = f
                return f
            except Exception:
                continue
    return ImageFont.load_default()

# ── Photo fetch ───────────────────────────────────────────────────────────────

def _fetch_from_url(url: str) -> Optional[Image.Image]:
    try:
        r = requests.get(url, timeout=15, allow_redirects=True,
                         headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200 and "image" in r.headers.get("content-type", ""):
            return Image.open(io.BytesIO(r.content)).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    except Exception:
        pass
    return None


def _scrape_article_image(article_url: str) -> Optional[Image.Image]:
    """Try to pull the main image directly from the article page."""
    if not article_url or article_url == "#":
        return None
    try:
        from html.parser import HTMLParser

        r = requests.get(article_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return None

        # Look for og:image or twitter:image meta tags
        content = r.text
        for tag in ['og:image', 'twitter:image']:
            idx = content.find(f'property="{tag}"')
            if idx == -1:
                idx = content.find(f"property='{tag}'")
            if idx == -1:
                idx = content.find(f'name="{tag}"')
            if idx != -1:
                chunk = content[idx:idx+300]
                for attr in ['content="', "content='"]:
                    ci = chunk.find(attr)
                    if ci != -1:
                        end = chunk.find('"' if attr.endswith('"') else "'", ci + len(attr))
                        img_url = chunk[ci + len(attr):end]
                        if img_url.startswith("http"):
                            img = _fetch_from_url(img_url)
                            if img:
                                return img
    except Exception:
        pass
    return None


def _fetch_photo(query: str, article_url: str = "") -> Optional[Image.Image]:
    import random, os
    salt = random.randint(1, 99999)
    keyword_pexels = query.replace(",", " ")[:80]

    # 1. Scrape image directly from the article
    print(f"   🔗  Trying article image from: {article_url[:60]}...")
    img = _scrape_article_image(article_url)
    if img:
        print("   ✅  Got image from article!")
        return img

    # 2. Pexels — topic-relevant stock photos
    pexels_key = os.environ.get("PEXELS_API_KEY", "")
    if pexels_key:
        try:
            r = requests.get(
                "https://api.pexels.com/v1/search",
                headers={"Authorization": pexels_key},
                params={"query": keyword_pexels, "per_page": 15, "orientation": "square"},
                timeout=10,
            )
            if r.status_code == 200:
                photos = r.json().get("photos", [])
                if photos:
                    img = _fetch_from_url(random.choice(photos)["src"]["large"])
                    if img:
                        print("   ✅  Got image from Pexels")
                        return img
        except Exception:
            pass

    # 3. loremflickr fallback
    img = _fetch_from_url(
        f"https://loremflickr.com/1080/1080/{query.replace(' ', '+')[:60]}?lock={salt}"
    )
    if img:
        return img

    # 4. Pure random fallback
    return _fetch_from_url(f"https://picsum.photos/seed/{salt}/1080/1080")

# ── Word wrap ─────────────────────────────────────────────────────────────────

def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_px: int) -> list:
    words, lines, cur = text.split(), [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if draw.textlength(test, font=font) <= max_px:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

# ── Shared components ─────────────────────────────────────────────────────────

def _header_strip(img: Image.Image, brand: dict, height: int = 100) -> None:
    """Draw the top coloured strip with source name."""
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, height], fill=brand["bg"])
    font = _font(38, bold=True)
    tw = draw.textlength(brand["name"], font=font)
    draw.text(((W - tw) // 2, (height - 38) // 2), brand["name"], font=font, fill=brand["fg"])

def _photo_section(img: Image.Image, photo: Optional[Image.Image], y_top: int, y_bot: int) -> None:
    """Paste a darkened, slightly blurred photo into a vertical slice of the canvas."""
    if photo:
        # Crop to fit the section proportionally
        section_h = y_bot - y_top
        crop = photo.crop((0, 0, W, H))
        # Darken + subtle blur
        crop = ImageEnhance.Brightness(crop.filter(ImageFilter.GaussianBlur(2))).enhance(0.45)
        # Crop a proportional slice from the photo
        src_slice = crop.crop((0, int(H * y_top / H), W, int(H * y_bot / H)))
        src_slice = src_slice.resize((W, section_h), Image.Resampling.LANCZOS)
        img.paste(src_slice, (0, y_top))
    else:
        draw = ImageDraw.Draw(img)
        for y in range(y_top, y_bot):
            t = (y - y_top) / (y_bot - y_top)
            c = int(15 + 25 * t)
            draw.line([(0, y), (W, y)], fill=(c, c, c + 10))

def _gradient_overlay(img: Image.Image, y_top: int, y_bot: int) -> None:
    """Heavy bottom-weighted gradient over the photo section."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(y_top, y_bot):
        t = (y - y_top) / (y_bot - y_top)
        alpha = int(20 + t * 210)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    base = img.convert("RGBA")
    base.alpha_composite(overlay)
    img.paste(base.convert("RGB"))

def _pill(draw, x, y, text, font, bg, fg=(255, 255, 255), px=20, py=8) -> int:
    tw = int(draw.textlength(text, font=font))
    x2, y2 = x + tw + px * 2, y + font.size + py * 2
    draw.rounded_rectangle([x, y, x2, y2], radius=(y2 - y) // 2, fill=bg)
    draw.text((x + px, y + py), text, font=font, fill=fg)
    return x2

def _dot_row(draw, current, total, accent, cy):
    r, gap = 8, 28
    total_w = total * r * 2 + (total - 1) * (gap - r * 2)
    x0 = (W - total_w) // 2
    for i in range(total):
        cx = x0 + i * gap + r
        if i == current - 1:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
        else:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 200, 200), width=2)

# ── SLIDE 1: COVER ────────────────────────────────────────────────────────────

def make_cover(title: str, category: str, source: str, photo: Optional[Image.Image]) -> Image.Image:
    brand  = SOURCE_BRAND.get(source, DEFAULT_BRAND)
    accent = brand["fg"]

    img = Image.new("RGB", (W, H), (10, 10, 10))

    # Full bleed photo
    _photo_section(img, photo, 0, H)
    _gradient_overlay(img, 0, H)

    draw = ImageDraw.Draw(img)
    pad  = 60

    # Category pill — top left
    font_cat = _font(26, bold=True)
    _pill(draw, pad, 50, category.upper(), font_cat,
          bg=accent, fg=(0, 0, 0) if sum(accent) > 500 else (255, 255, 255))

    # Headline — bottom of slide
    font_h = _font(72, bold=True)
    lines  = _wrap(draw, title, font_h, W - pad * 2)[:4]
    lh     = 84
    hl_y   = H - len(lines) * lh - 80

    for line in lines:
        draw.text((pad + 2, hl_y + 2), line, font=font_h, fill=(0, 0, 0))
        draw.text((pad, hl_y), line, font=font_h, fill=(255, 255, 255))
        hl_y += lh

    return img

# ── SLIDE 2: DETAIL ───────────────────────────────────────────────────────────

def make_detail(title: str, summary: str, source: str, photo: Optional[Image.Image]) -> Image.Image:
    brand  = SOURCE_BRAND.get(source, DEFAULT_BRAND)
    accent = brand["fg"]

    img = Image.new("RGB", (W, H), (10, 10, 10))
    PHOTO_BOT = 480

    # Photo top half, text bottom half
    _photo_section(img, photo, 0, PHOTO_BOT)
    _gradient_overlay(img, 0, PHOTO_BOT)

    draw = ImageDraw.Draw(img)
    pad  = 60

    # "DETAILS" pill — top left
    font_chip = _font(24, bold=True)
    _pill(draw, pad, 40, "DETAILS", font_chip, bg=accent,
          fg=(0, 0, 0) if sum(accent) > 500 else (255, 255, 255))

    # Compact headline at bottom of photo
    font_h  = _font(52, bold=True)
    lines_h = _wrap(draw, title, font_h, W - pad * 2)[:3]
    hl_y    = PHOTO_BOT - len(lines_h) * 64 - 24
    for line in lines_h:
        draw.text((pad + 2, hl_y + 2), line, font=font_h, fill=(0, 0, 0))
        draw.text((pad, hl_y), line, font=font_h, fill=(255, 255, 255))
        hl_y += 64

    # Summary text below photo
    y = PHOTO_BOT + 30
    draw.rectangle([pad, y, pad + 70, y + 5], fill=accent)
    y += 28

    clean = (summary
             .replace("<p>", " ").replace("</p>", " ")
             .replace("<b>", "").replace("</b>", "")
             .replace("  ", " ").strip())
    font_b = _font(36)
    for line in _wrap(draw, clean[:300], font_b, W - pad * 2)[:7]:
        draw.text((pad, y), line, font=font_b, fill=(220, 220, 220))
        y += 50

    return img

# ── SLIDE 3: DETAILS 2 ────────────────────────────────────────────────────────

def make_detail2(title: str, details: str, source: str, photo: Optional[Image.Image]) -> Image.Image:
    brand  = SOURCE_BRAND.get(source, DEFAULT_BRAND)
    accent = brand["fg"]

    img = Image.new("RGB", (W, H), (15, 15, 20))
    PHOTO_BOT = 340

    _photo_section(img, photo, 0, PHOTO_BOT)
    _gradient_overlay(img, 0, PHOTO_BOT)

    draw = ImageDraw.Draw(img)
    pad  = 60

    font_chip = _font(24, bold=True)
    _pill(draw, pad, 40, "KEY FACTS", font_chip, bg=accent,
          fg=(0, 0, 0) if sum(accent) > 500 else (255, 255, 255))

    y = PHOTO_BOT + 30
    draw.rectangle([pad, y, pad + 70, y + 5], fill=accent)
    y += 28

    clean = (details
             .replace("<p>", " ").replace("</p>", " ")
             .replace("<b>", "").replace("</b>", "")
             .replace("  ", " ").strip())
    font_b = _font(36)
    for line in _wrap(draw, clean[:400], font_b, W - pad * 2)[:8]:
        draw.text((pad, y), line, font=font_b, fill=(220, 220, 220))
        y += 50

    return img

# ── SLIDE 4: CTA ─────────────────────────────────────────────────────────────

def make_cta(source: str, photo: Optional[Image.Image]) -> Image.Image:
    brand  = SOURCE_BRAND.get(source, DEFAULT_BRAND)
    accent = brand["fg"]

    img = Image.new("RGB", (W, H), (10, 10, 10))

    # Full bleed photo, very dark
    _photo_section(img, photo, 0, H)
    # Extra darkness for CTA
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 170))
    base = img.convert("RGBA")
    base.alpha_composite(overlay)
    img.paste(base.convert("RGB"))

    draw = ImageDraw.Draw(img)

    # Big centred CTA
    font_big = _font(96, bold=True)
    font_med = _font(38)
    font_sm  = _font(28)

    texts   = ["FOLLOW FOR", "DAILY NEWS"]
    total_h = len(texts) * 110 + 80
    y       = (H - total_h) // 2 + 20

    for t in texts:
        tw = draw.textlength(t, font=font_big)
        draw.text(((W - tw) // 2 + 3, y + 3), t, font=font_big, fill=(0, 0, 0))
        draw.text(((W - tw) // 2, y), t, font=font_big, fill=(255, 255, 255))
        y += 110

    # Divider
    draw.rectangle([(W // 2 - 100, y + 10), (W // 2 + 100, y + 14)], fill=accent)
    y += 36

    sub = "Turn on post notifications"
    tw = draw.textlength(sub, font=font_med)
    draw.text(((W - tw) // 2, y), sub, font=font_med, fill=accent)
    y += 52

    return img

# ── Public API ────────────────────────────────────────────────────────────────

def generate_slides(article: dict) -> list:
    title    = article.get("title", "")[:140]
    summary  = article.get("summary", "")
    details  = article.get("details", summary)
    source   = article.get("source", "NEWS").upper()
    category = article.get("category", "WORLD NEWS")
    query       = article.get("photo_query") or (category + " " + title[:30])
    article_url = article.get("link", "") or article.get("url", "")

    hash_id = abs(hash(title))

    print(f"   📷  Fetching photo: '{query[:40]}'...")
    photo = _fetch_photo(query, article_url)
    print("   ✅  Photo loaded" if photo else "   ⚠️   Using dark fallback")

    slides = [
        make_cover(title,   category, source, photo),
        make_detail(title,  summary,  source, photo),
        make_detail2(title, details,  source, photo),
        make_cta(source, photo),
    ]

    paths = []
    for i, slide in enumerate(slides, 1):
        path = IMAGES_DIR / f"{hash_id}_slide_{i}.png"
        slide.save(path, "PNG")
        paths.append(path)
        print(f"   🖼   Slide {i}/{len(slides)} -> {path.name}")

    return paths

# ── Test ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        {
            "title":       "Nvidia RTX 5090 breaks every benchmark — and it's not even close",
            "summary":     "Nvidia's flagship RTX 5090 GPU has shattered performance records in leaked benchmark tests, outperforming the previous RTX 4090 by up to 85% in ray-traced workloads. Analysts say it could redefine PC gaming and professional AI workloads.",
            "source":      "TECHCRUNCH",
            "category":    "TECH",
            "photo_query": "nvidia gpu technology",
        },
        {
            "title":       "Units in East Germany soar as housing crisis deepens",
            "summary":     "Rental prices across East German cities have surged 34% year-on-year as housing supply fails to meet demand. Berlin economists warn the crisis could spread westward within 18 months if no new construction policy is introduced.",
            "source":      "REUTERS",
            "category":    "ECONOMY",
            "photo_query": "germany city housing",
        },
        {
            "title":       "Anthropic confidentially files draft S-1 with the SEC",
            "summary":     "AI safety company Anthropic has filed a confidential draft IPO prospectus with the SEC, sources familiar with the matter confirmed. The company, valued at $61 billion, is targeting a public listing before the end of the year.",
            "source":      "GUARDIAN",
            "category":    "BUSINESS",
            "photo_query": "stock market finance IPO",
        },
    ]

    for article in tests:
        print(f"\n--- {article['source']}: {article['title'][:50]} ---")
        generate_slides(article)

    print(f"\nDone! Check: {IMAGES_DIR.resolve()}")
