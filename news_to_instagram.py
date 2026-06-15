"""
News-to-Instagram carousel agent.

Flow:
  1. Claude searches the web for the latest news on your topics.
  2. Claude picks the best story and writes 3-4 slide contents (JSON).
  3. Pillow renders each slide as a 1080x1080 image.
  4. Each image is uploaded to imgbb (free public host) to get a URL.
  5. Instagram Graph API publishes a carousel post.

Requirements:
  pip install anthropic requests pillow

Free API keys needed:
  - imgbb:     https://api.imgbb.com  (free, takes 30 seconds)
  - Instagram: Facebook Developer App with instagram_content_publish scope

Environment variables:
  ANTHROPIC_API_KEY
  IMGBB_API_KEY
  INSTAGRAM_ACCESS_TOKEN
  INSTAGRAM_ACCOUNT_ID
  NEWS_TOPICS   (comma-separated, default: "AI, technology, startups")
"""

import base64
import json
import os
import sys
import tempfile
import textwrap
import time
from pathlib import Path

import requests
import anthropic
from PIL import Image, ImageDraw, ImageFont

# ── Config ────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY    = os.environ.get("ANTHROPIC_API_KEY", "")
IMGBB_API_KEY        = os.environ.get("IMGBB_API_KEY", "")
INSTAGRAM_TOKEN      = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID", "")
NEWS_TOPICS          = os.environ.get("NEWS_TOPICS", "AI, technology, startups")

MODEL      = "claude-opus-4-7"
SLIDE_SIZE = (1080, 1080)

# Colour palettes — one is picked per post based on story tone
PALETTES = [
    {"bg_top": (15, 23, 42),   "bg_bot": (30, 64, 175),  "accent": (99, 179, 237),  "text": (255, 255, 255)},  # deep blue
    {"bg_top": (20, 20, 20),   "bg_bot": (55, 0, 80),    "accent": (196, 92, 255),  "text": (255, 255, 255)},  # dark purple
    {"bg_top": (5, 46, 22),    "bg_bot": (6, 95, 70),    "accent": (52, 211, 153),  "text": (255, 255, 255)},  # forest green
    {"bg_top": (67, 20, 7),    "bg_bot": (154, 52, 18),  "accent": (251, 191, 36),  "text": (255, 255, 255)},  # burnt orange
]

GRAPH_BASE = "https://graph.facebook.com/v19.0"

# ── Image rendering ───────────────────────────────────────────────────────────

def _gradient_bg(draw: ImageDraw.ImageDraw, palette: dict) -> None:
    """Vertical gradient from bg_top to bg_bot."""
    top = palette["bg_top"]
    bot = palette["bg_bot"]
    h = SLIDE_SIZE[1]
    for y in range(h):
        t = y / h
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        draw.line([(0, y), (SLIDE_SIZE[0], y)], fill=(r, g, b))


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def render_slide(slide: dict, palette: dict, slide_num: int, total: int) -> Image.Image:
    """
    slide keys:
      type: "cover" | "detail" | "cta"
      label: small tag line at top (e.g. "BREAKING" or "WHY IT MATTERS")
      headline: big bold text
      body: smaller supporting text (optional)
      emoji: single emoji accent (optional)
    """
    img  = Image.new("RGB", SLIDE_SIZE)
    draw = ImageDraw.Draw(img)
    _gradient_bg(draw, palette)

    W, H = SLIDE_SIZE
    pad  = 80

    # Slide counter dots at bottom
    dot_y   = H - 50
    dot_r   = 6
    dot_gap = 22
    total_w = total * dot_r * 2 + (total - 1) * (dot_gap - dot_r * 2)
    dot_x0  = (W - total_w) // 2
    for i in range(total):
        cx = dot_x0 + i * dot_gap + dot_r
        color = palette["accent"] if i == slide_num - 1 else (*palette["text"][:3], 80)
        draw.ellipse([cx - dot_r, dot_y - dot_r, cx + dot_r, dot_y + dot_r], fill=color)

    # Accent bar at top
    draw.rectangle([pad, 60, pad + 6, 60 + 60], fill=palette["accent"])

    cur_y = 70

    # Label
    label = slide.get("label", "").upper()
    if label:
        font_lbl = _load_font(24)
        draw.text((pad + 18, cur_y), label, font=font_lbl, fill=palette["accent"])
        cur_y += 44

    # Emoji
    emoji = slide.get("emoji", "")

    # Headline
    headline = slide.get("headline", "")
    font_h = _load_font(64, bold=True)
    max_chars = 18
    lines = textwrap.wrap(headline, width=max_chars)
    line_h = 76
    total_h_height = len(lines) * line_h
    if slide.get("type") == "cover":
        # vertically centre headline
        cur_y = (H - total_h_height) // 2 - 40
    else:
        cur_y += 20

    for line in lines:
        draw.text((pad, cur_y), line, font=font_h, fill=palette["text"])
        cur_y += line_h

    cur_y += 24

    # Body text
    body = slide.get("body", "")
    if body:
        font_b = _load_font(32)
        for para in textwrap.wrap(body, width=32):
            draw.text((pad, cur_y), para, font=font_b, fill=(*palette["text"][:3],))
            cur_y += 44

    # Emoji bottom-right accent
    if emoji:
        font_e = _load_font(80)
        draw.text((W - pad - 90, H - pad - 110), emoji, font=font_e, fill=palette["text"])

    # Bottom: source credit on CTA slide
    if slide.get("type") == "cta":
        font_s = _load_font(22)
        draw.text((pad, H - 90), "Follow for daily tech updates →", font=font_s, fill=palette["accent"])

    return img


def render_carousel(slides_data: list[dict], palette: dict) -> list[Path]:
    """Render all slides, save to temp files, return paths."""
    paths = []
    total = len(slides_data)
    tmp = Path(tempfile.mkdtemp())
    for i, slide in enumerate(slides_data):
        img = render_slide(slide, palette, slide_num=i + 1, total=total)
        path = tmp / f"slide_{i+1}.jpg"
        img.save(path, "JPEG", quality=92)
        paths.append(path)
        print(f"   🎨  Rendered slide {i+1}/{total}")
    return paths


# ── Image hosting (imgbb) ─────────────────────────────────────────────────────

def upload_image(path: Path) -> str:
    """Upload image to imgbb, return public URL."""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    resp = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": IMGBB_API_KEY, "image": b64},
        timeout=30,
    )
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"imgbb upload failed: {data}")
    return data["data"]["url"]


# ── Instagram Graph API ───────────────────────────────────────────────────────

def _post_carousel(image_urls: list[str], caption: str) -> dict:
    """Create and publish a carousel post. Returns {success, post_id, error}."""
    if not INSTAGRAM_TOKEN or not INSTAGRAM_ACCOUNT_ID:
        return {"success": False, "post_id": None,
                "error": "INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_ACCOUNT_ID not set."}

    # Step 1 – create child media containers
    child_ids = []
    for url in image_urls:
        r = requests.post(
            f"{GRAPH_BASE}/{INSTAGRAM_ACCOUNT_ID}/media",
            params={"image_url": url, "is_carousel_item": "true",
                    "access_token": INSTAGRAM_TOKEN},
            timeout=30,
        )
        d = r.json()
        if "error" in d:
            return {"success": False, "post_id": None, "error": d["error"].get("message")}
        child_ids.append(d["id"])

    time.sleep(2)

    # Step 2 – create carousel container
    r = requests.post(
        f"{GRAPH_BASE}/{INSTAGRAM_ACCOUNT_ID}/media",
        params={"media_type": "CAROUSEL", "caption": caption,
                "children": ",".join(child_ids), "access_token": INSTAGRAM_TOKEN},
        timeout=30,
    )
    d = r.json()
    if "error" in d:
        return {"success": False, "post_id": None, "error": d["error"].get("message")}
    carousel_id = d["id"]

    time.sleep(3)

    # Step 3 – publish
    r = requests.post(
        f"{GRAPH_BASE}/{INSTAGRAM_ACCOUNT_ID}/media_publish",
        params={"creation_id": carousel_id, "access_token": INSTAGRAM_TOKEN},
        timeout=30,
    )
    d = r.json()
    if "error" in d:
        return {"success": False, "post_id": None, "error": d["error"].get("message")}
    return {"success": True, "post_id": d.get("id"), "error": None}


# ── Tool definitions ──────────────────────────────────────────────────────────

TOOLS = [
    {"type": "web_search_20260209", "name": "web_search"},
    {
        "type": "custom",
        "name": "create_carousel_post",
        "description": (
            "Render a 3-4 slide carousel and post it to Instagram. "
            "Call this once — after you have the story and have written all slide content."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "slides": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 4,
                    "description": "Ordered list of slides. First must be type 'cover', last must be type 'cta'.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type":     {"type": "string", "enum": ["cover", "detail", "cta"]},
                            "label":    {"type": "string", "description": "Short tag in accent colour, e.g. 'BREAKING' or 'WHY IT MATTERS'"},
                            "headline": {"type": "string", "description": "Big bold text. Max ~50 chars."},
                            "body":     {"type": "string", "description": "Supporting sentence or two. Max ~120 chars."},
                            "emoji":    {"type": "string", "description": "A single relevant emoji for the slide."},
                        },
                        "required": ["type", "headline"],
                    },
                },
                "caption": {
                    "type": "string",
                    "description": "Instagram caption (under 2200 chars) with relevant hashtags.",
                },
                "palette_index": {
                    "type": "integer",
                    "description": "Colour palette 0-3. 0=blue, 1=purple, 2=green, 3=orange. Pick based on the story's vibe.",
                    "minimum": 0,
                    "maximum": 3,
                },
            },
            "required": ["slides", "caption", "palette_index"],
        },
    },
]


# ── Tool execution ────────────────────────────────────────────────────────────

def execute_tool(name: str, tool_input: dict) -> str:
    if name != "create_carousel_post":
        return json.dumps({"error": f"Unknown tool: {name}"})

    slides        = tool_input["slides"]
    caption       = tool_input["caption"]
    palette_index = tool_input.get("palette_index", 0)
    palette       = PALETTES[palette_index % len(PALETTES)]

    # Render slides
    print(f"\n🖼   Rendering {len(slides)} slides...")
    paths = render_carousel(slides, palette)

    # Upload images
    print("☁️   Uploading images...")
    image_urls = []
    for i, path in enumerate(paths):
        url = upload_image(path)
        image_urls.append(url)
        print(f"   ✅  Slide {i+1} → {url}")

    # Post to Instagram
    print("📲  Publishing carousel to Instagram...")
    result = _post_carousel(image_urls, caption)
    return json.dumps(result)


# ── Agent loop ────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a social media editor creating Instagram carousel posts about tech news.

Steps:
1. Search the web for the 5 most recent, interesting stories on the given topics.
2. Choose the single best story — most timely, most surprising, or most impactful.
3. Plan a carousel of 3-4 slides:
   - Slide 1 (cover): punchy headline, story label, hook emoji
   - Slide 2 (detail): key fact or statistic
   - Slide 3 (detail): why it matters / surprising angle
   - Slide 4 (cta, optional): bold takeaway or call to action
4. Write an Instagram caption (conversational, 3-5 sentences + 8-12 hashtags).
5. Pick a palette (0=blue tech, 1=purple innovation, 2=green sustainability, 3=orange disruption).
6. Call create_carousel_post with all of this.

Tone: sharp, confident, no fluff. Write for a smart, curious audience.
Headlines must be short (≤50 chars). Body text ≤120 chars per slide.
"""


def run_agent(topics: str = NEWS_TOPICS) -> None:
    if not IMGBB_API_KEY:
        print("⚠️  IMGBB_API_KEY not set — images won't upload. Get a free key at https://api.imgbb.com")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    messages = [
        {
            "role": "user",
            "content": f"Find the latest news about: {topics}. Create a carousel post for the best story.",
        }
    ]

    print(f"\n🔍  Scanning news: {topics}\n{'─' * 50}")

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        for block in response.content:
            if block.type == "text":
                print(block.text)

        if response.stop_reason == "end_turn":
            print("\n✅  Done.")
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"\n🔧  {block.name}")
                    result_str  = execute_tool(block.name, block.input)
                    result_data = json.loads(result_str)

                    if block.name == "create_carousel_post":
                        if result_data.get("success"):
                            print(f"\n🎉  Posted! Instagram post ID: {result_data['post_id']}")
                        else:
                            print(f"\n❌  Post failed: {result_data.get('error')}")

                    tool_results.append(
                        {"type": "tool_result", "tool_use_id": block.id, "content": result_str}
                    )
            messages.append({"role": "user", "content": tool_results})
            continue

        if response.stop_reason == "pause_turn":
            continue

        print(f"Stopped: {response.stop_reason}")
        break


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    topics = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else NEWS_TOPICS
    run_agent(topics)
