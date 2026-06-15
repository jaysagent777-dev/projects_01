"""
News Slide Agent
────────────────
1. Claude searches the web for the latest world news.
2. Picks the 3 best stories.
3. Renders each story as a beautiful 1080x1080 slide image.
4. Saves slides to ~/Desktop/news_slides/

Only needs: ANTHROPIC_API_KEY
Optional:   INSTAGRAM_ACCESS_TOKEN + INSTAGRAM_ACCOUNT_ID  (to auto-post)
            IMGBB_API_KEY  (needed for Instagram posting)

Install:
  pip install anthropic pillow requests
"""

import base64, json, os, sys, tempfile, textwrap, time
from pathlib import Path
from datetime import datetime

import anthropic
import requests
from PIL import Image, ImageDraw, ImageFont

# ── Config ────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY    = os.environ.get("ANTHROPIC_API_KEY", "")
IMGBB_API_KEY        = os.environ.get("IMGBB_API_KEY", "")
INSTAGRAM_TOKEN      = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID", "")

MODEL      = "claude-opus-4-7"
SLIDE_SIZE = (1080, 1080)
OUTPUT_DIR = Path.home() / "Desktop" / "news_slides"

PALETTES = [
    {"bg_top": (10, 10, 30),   "bg_bot": (20, 50, 160),  "accent": (80, 160, 255), "text": (255, 255, 255)},  # blue
    {"bg_top": (15, 5,  30),   "bg_bot": (80, 0,  120),  "accent": (200, 80, 255), "text": (255, 255, 255)},  # purple
    {"bg_top": (5,  30, 15),   "bg_bot": (0,  100, 60),  "accent": (50, 220, 140), "text": (255, 255, 255)},  # green
    {"bg_top": (60, 15, 5),    "bg_bot": (160, 50, 10),  "accent": (255, 190, 30), "text": (255, 255, 255)},  # orange
    {"bg_top": (30, 5,  5),    "bg_bot": (140, 20, 20),  "accent": (255, 80,  80), "text": (255, 255, 255)},  # red
]

# ── Fonts ─────────────────────────────────────────────────────────────────────

def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ── Slide renderer ────────────────────────────────────────────────────────────

def render_slide(story: dict, palette: dict, idx: int, total: int) -> Image.Image:
    """
    story keys: headline, body, category, emoji, palette_index
    """
    img  = Image.new("RGB", SLIDE_SIZE)
    draw = ImageDraw.Draw(img)
    W, H = SLIDE_SIZE

    # Gradient background
    top, bot = palette["bg_top"], palette["bg_bot"]
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i]-top[i])*t) for i in range(3)))

    # Top accent stripe
    draw.rectangle([0, 0, W, 8], fill=palette["accent"])

    pad = 80

    # Category tag
    cat = story.get("category", "WORLD NEWS").upper()
    font_tag = _font(26)
    draw.rectangle([pad, 60, pad + len(cat)*14 + 24, 100], fill=palette["accent"])
    draw.text((pad + 12, 64), cat, font=font_tag, fill=(0, 0, 0))

    # Emoji (large, top right)
    emoji = story.get("emoji", "🌍")
    font_e = _font(120)
    draw.text((W - pad - 130, 50), emoji, font=font_e, fill=palette["text"])

    # Headline
    headline = story.get("headline", "")
    font_h   = _font(68, bold=True)
    lines    = textwrap.wrap(headline, width=16)
    y = 180
    for line in lines[:4]:
        draw.text((pad, y), line, font=font_h, fill=palette["text"])
        y += 82

    # Divider line
    y += 10
    draw.rectangle([pad, y, W - pad, y + 3], fill=palette["accent"])
    y += 24

    # Body text
    body = story.get("body", "")
    font_b = _font(34)
    for para in textwrap.wrap(body, width=30)[:5]:
        draw.text((pad, y), para, font=font_b, fill=(*palette["text"][:3],))
        y += 50

    # Slide number dots
    dot_r, gap = 7, 26
    total_w = total * dot_r * 2 + (total - 1) * (gap - dot_r * 2)
    x0 = (W - total_w) // 2
    for i in range(total):
        cx = x0 + i * gap + dot_r
        cy = H - 55
        fill = palette["accent"] if i == idx else (200, 200, 200, 80)
        draw.ellipse([cx-dot_r, cy-dot_r, cx+dot_r, cy+dot_r], fill=fill)

    # Footer
    date_str = datetime.now().strftime("%B %d, %Y")
    font_f = _font(22)
    draw.text((pad, H - 75), f"📡  NewsAgent  •  {date_str}", font=font_f, fill=palette["accent"])

    return img


def save_slides(stories: list[dict]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    total = len(stories)
    for i, story in enumerate(stories):
        p = PALETTES[story.get("palette_index", i) % len(PALETTES)]
        img = render_slide(story, p, idx=i, total=total)
        out = OUTPUT_DIR / f"slide_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        img.save(out, "JPEG", quality=93)
        paths.append(out)
        print(f"   🖼   Slide {i+1}/{total} saved → {out}")
    return paths


# ── Optional: imgbb upload ────────────────────────────────────────────────────

def upload_to_imgbb(path: Path) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    r = requests.post("https://api.imgbb.com/1/upload",
                      data={"key": IMGBB_API_KEY, "image": b64}, timeout=30)
    d = r.json()
    if not d.get("success"):
        raise RuntimeError(f"imgbb failed: {d}")
    return d["data"]["url"]


# ── Optional: Instagram post ──────────────────────────────────────────────────

def post_to_instagram(image_urls: list[str], caption: str) -> dict:
    if not INSTAGRAM_TOKEN or not INSTAGRAM_ACCOUNT_ID:
        return {"success": False, "error": "Instagram credentials not set"}
    base = "https://graph.facebook.com/v19.0"
    child_ids = []
    for url in image_urls:
        r = requests.post(f"{base}/{INSTAGRAM_ACCOUNT_ID}/media",
                          params={"image_url": url, "is_carousel_item": "true",
                                  "access_token": INSTAGRAM_TOKEN}, timeout=30)
        d = r.json()
        if "error" in d:
            return {"success": False, "error": d["error"].get("message")}
        child_ids.append(d["id"])
    time.sleep(2)
    r = requests.post(f"{base}/{INSTAGRAM_ACCOUNT_ID}/media",
                      params={"media_type": "CAROUSEL", "caption": caption,
                              "children": ",".join(child_ids), "access_token": INSTAGRAM_TOKEN}, timeout=30)
    d = r.json()
    if "error" in d:
        return {"success": False, "error": d["error"].get("message")}
    carousel_id = d["id"]
    time.sleep(3)
    r = requests.post(f"{base}/{INSTAGRAM_ACCOUNT_ID}/media_publish",
                      params={"creation_id": carousel_id, "access_token": INSTAGRAM_TOKEN}, timeout=30)
    d = r.json()
    if "error" in d:
        return {"success": False, "error": d["error"].get("message")}
    return {"success": True, "post_id": d.get("id")}


# ── Tool definitions ──────────────────────────────────────────────────────────

TOOLS = [
    {"type": "web_search_20260209", "name": "web_search"},
    {
        "type": "custom",
        "name": "publish_news_slides",
        "description": (
            "Call this after researching the news. Pass exactly 3 stories. "
            "This renders slide images and saves them to the desktop. "
            "If Instagram credentials are available, it also posts as a carousel."
        ),
        "input_schema": {
            "type": "object",
            "required": ["stories", "caption"],
            "properties": {
                "stories": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 3,
                    "description": "Exactly 3 top news stories.",
                    "items": {
                        "type": "object",
                        "required": ["headline", "body", "category", "emoji", "palette_index"],
                        "properties": {
                            "headline":      {"type": "string", "description": "Bold headline, max 50 chars."},
                            "body":          {"type": "string", "description": "2-3 sentence summary, max 150 chars."},
                            "category":      {"type": "string", "description": "e.g. TECH, POLITICS, CLIMATE, BUSINESS, SCIENCE"},
                            "emoji":         {"type": "string", "description": "One relevant emoji."},
                            "palette_index": {"type": "integer", "minimum": 0, "maximum": 4,
                                              "description": "Colour theme: 0=blue, 1=purple, 2=green, 3=orange, 4=red"},
                        },
                    },
                },
                "caption": {
                    "type": "string",
                    "description": "Instagram caption with 3-5 sentences + 10 hashtags.",
                },
            },
        },
    },
]

SYSTEM = """You are a world news editor creating visual slide summaries.

Steps:
1. Search the web for today's top world news across different categories (tech, politics, climate, business, science, etc.)
2. Pick the 3 most interesting, impactful, or surprising stories from different categories.
3. For each story write a punchy headline (≤50 chars), a clear 2-3 sentence body (≤150 chars), pick a category tag, an emoji, and a colour palette.
4. Write an Instagram caption summarising all 3 stories with energy and 10 relevant hashtags.
5. Call publish_news_slides with all 3 stories and the caption.

Be globally diverse — don't pick 3 stories from the same country or topic.
Headlines must grab attention. Body must be clear and informative.
"""


# ── Agent loop ────────────────────────────────────────────────────────────────

DEMO_STORIES = [
    {
        "headline": "AI Beats Doctors at Diagnosis",
        "body": "A new AI model outperformed specialist doctors in diagnosing rare diseases, cutting diagnosis time from months to minutes.",
        "category": "TECH",
        "emoji": "🤖",
        "palette_index": 0,
    },
    {
        "headline": "Arctic Ice Hits Record Low",
        "body": "Scientists report Arctic sea ice has reached its lowest level ever recorded, raising urgent concerns about global climate tipping points.",
        "category": "CLIMATE",
        "emoji": "🧊",
        "palette_index": 2,
    },
    {
        "headline": "Global Economy Beats Forecasts",
        "body": "The IMF upgraded its global growth forecast for 2026, citing stronger-than-expected consumer spending across emerging markets.",
        "category": "BUSINESS",
        "emoji": "📈",
        "palette_index": 3,
    },
]

def run(topics: str = "world news, technology, climate, politics, science, business") -> None:
    print(f"\n🌍  NewsAgent starting (DEMO MODE — no API key needed)...\n{'─'*50}")

    stories = DEMO_STORIES
    print(f"\n🎨  Rendering {len(stories)} slides...")
    paths = save_slides(stories)
    print(f"\n📁  Slides saved to: {OUTPUT_DIR}")
    print("\n✅  Done!")


if __name__ == "__main__":
    topics = " ".join(sys.argv[1:]) or "world news, technology, climate, politics, science, business"
    run(topics)
