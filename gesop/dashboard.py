#!/usr/bin/env python3
"""
GeSoP — News Instagram Dashboard
Run: python3 dashboard.py  →  open http://localhost:5055
"""

import base64, json, os, threading, subprocess
from collections import deque
from pathlib import Path
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify, request, Response

# Load .env from the same directory as this script
load_dotenv(Path(__file__).parent / ".env", override=True)

IMAGES_DIR = Path("generated_images")
IMAGES_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

VISITORS_FILE = Path("data/visitors.json")
VISITORS_FILE.parent.mkdir(exist_ok=True)
_geo_cache = {}
_log_lock = threading.Lock()

def _load_visitors():
    if VISITORS_FILE.exists():
        try:
            return json.loads(VISITORS_FILE.read_text())
        except Exception:
            pass
    return []

def _save_visitors(entries):
    VISITORS_FILE.write_text(json.dumps(entries[-500:], indent=2))

visitor_log = deque(_load_visitors(), maxlen=500)

def _get_country(ip):
    if ip in _geo_cache:
        return
    try:
        import urllib.request as ur
        with ur.urlopen(f"http://ip-api.com/json/{ip}?fields=country,countryCode", timeout=3) as r:
            d = json.loads(r.read())
        _geo_cache[ip] = f"{d.get('country','?')} {d.get('countryCode','')}"
    except Exception:
        _geo_cache[ip] = "?"
    # update country in log and persist
    with _log_lock:
        for v in visitor_log:
            if v["ip"] == ip and v["country"] == "…":
                v["country"] = _geo_cache.get(ip, "?")
        _save_visitors(list(visitor_log))

@app.before_request
def log_visitor():
    if request.path in ("/visitors", "/generate", "/health") or request.path.startswith("/static"):
        return
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    entry = {
        "time": datetime.now(timezone(timedelta(hours=-6))).strftime("%Y-%m-%d %H:%M:%S CST"),
        "ip": ip,
        "country": _geo_cache.get(ip, "…"),
        "path": request.path,
    }
    with _log_lock:
        visitor_log.appendleft(entry)
        _save_visitors(list(visitor_log))
    threading.Thread(target=_get_country, args=(ip,), daemon=True).start()

@app.route("/visitors")
def visitors():
    resp = jsonify(list(visitor_log))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


# ── Claude CLI wrapper ────────────────────────────────────────────────────────

def claude_message(system: str, messages: list, model: str = "claude-opus-4-8", max_tokens: int = 4096):
    """Call claude CLI and parse JSON response."""
    import json
    msg_json = json.dumps(messages)
    cmd = [
        "claude",
        "-p",
        "--model", model,
        "--system-prompt", system,
    ]
    result = subprocess.run(cmd, input=msg_json, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Claude CLI error: {result.stderr}")
    return result.stdout

# ── Agent runner (runs in background thread) ──────────────────────────────────

def _fetch_real_article(keywords: str):
    """Fetch a real article URL and title from Google News RSS."""
    import urllib.request, urllib.parse, xml.etree.ElementTree as ET
    q = urllib.parse.quote(keywords)
    url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        xml_data = r.read()
    root = ET.fromstring(xml_data)
    items = root.findall(".//item")
    if not items:
        return None, None
    item = items[0]
    title = item.findtext("title") or ""
    link = item.findtext("link") or ""
    # Google News wraps links — follow redirect to get real URL
    try:
        req2 = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req2, timeout=8) as r2:
            link = r2.url
    except Exception:
        pass
    return title, link


def _run_agent(keywords: str, callback):
    """Run the Claude news agent via CLI and stream status updates via callback(msg)."""
    try:
        from slide_generator import generate_slides

        SYSTEM = """You are a social media editor creating Instagram carousel posts.
Given a news article title and URL, write an Instagram carousel post.
Return ONLY valid JSON with keys: title, summary, source, category, photo_query, caption.
Tone: sharp, confident, no fluff."""

        callback({"type": "status", "msg": f"Searching for: {keywords}..."})

        real_title, real_link = _fetch_real_article(keywords)
        if real_title:
            callback({"type": "status", "msg": f"Found article: {real_title[:60]}"})

        prompt = f"""Write an Instagram carousel post for this news article:

Title: {real_title or keywords}
URL: {real_link or ''}

Return ONLY valid JSON (no markdown, no extra text):
{{
  "title": "...",
  "summary": "2-3 sentence overview of the story",
  "details": "3-4 sentences with key facts, numbers, quotes or context that go deeper than the summary",
  "source": "...",
  "category": "...",
  "photo_query": "...",
  "caption": "..."
}}"""

        # Call key rotator (OpenAI-compatible endpoint)
        import urllib.request
        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }).encode()
        rotator_url = os.environ.get("KEY_ROTATOR_URL", "http://localhost:7860")
        req = urllib.request.Request(
            f"{rotator_url}/v1/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": "Bearer rotator"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp_data = json.loads(resp.read())
        response_text = resp_data["choices"][0]["message"]["content"]
        callback({"type": "log", "msg": response_text[:200]})

        # Extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            raise Exception("No JSON found in response")

        inp = json.loads(json_match.group())

        callback({"type": "status", "msg": f"Found story: {inp['title'][:60]}"})
        callback({"type": "status", "msg": "Fetching background photo..."})

        paths = generate_slides(inp)

        # Encode slides as base64 for the browser
        slides_b64 = []
        for p in paths:
            with open(p, "rb") as f:
                slides_b64.append(base64.b64encode(f.read()).decode())

        link = real_link or inp.get("link", "")
        caption = inp["caption"]
        if link:
            caption = caption + f"\n\n🔗 Source: {link}"
        result_data = {
            "title":    inp["title"],
            "source":   inp["source"],
            "category": inp["category"],
            "caption":  caption,
            "link":     real_link or inp.get("link", ""),
            "slides":   slides_b64,
        }
        callback({"type": "done", **result_data})

    except Exception as e:
        callback({"type": "error", "msg": str(e)})


# ── SSE endpoint ──────────────────────────────────────────────────────────────

@app.route("/generate")
def generate():
    keywords = request.args.get("q", "world news today")

    queue = []
    done_event = threading.Event()

    def cb(msg):
        queue.append(msg)
        if msg.get("type") in ("done", "error"):
            done_event.set()

    t = threading.Thread(target=_run_agent, args=(keywords, cb), daemon=True)
    t.start()

    def stream():
        sent = 0
        while not done_event.is_set() or sent < len(queue):
            while sent < len(queue):
                yield f"data: {json.dumps(queue[sent])}\n\n"
                sent += 1
            done_event.wait(timeout=0.3)
        # flush any remaining
        while sent < len(queue):
            yield f"data: {json.dumps(queue[sent])}\n\n"
            sent += 1

    return Response(stream(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ── Main HTML page ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>gesop.ai</title>
<style>
  :root {
    --bg:   #0a0a0f;
    --bg2:  #111118;
    --bg3:  #1a1a24;
    --bdr:  #2a2a3a;
    --acc:  #7c3aed;
    --acc2: #a855f7;
    --grn:  #22c55e;
    --red:  #ef4444;
    --txt:  #e2e8f0;
    --muted:#94a3b8;
    --r:    12px;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--txt);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    min-height: 100vh;
  }

  /* ── Top bar ── */
  header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 32px;
    border-bottom: 1px solid var(--bdr);
    background: var(--bg2);
    position: sticky; top: 0; z-index: 100;
  }
  .logo { font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }
  .logo span { color: var(--acc2); }
  .status-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--grn); box-shadow: 0 0 8px var(--grn);
    display: inline-block; margin-right: 8px;
  }
  .status-label { font-size: 13px; color: var(--muted); }

  /* ── Main layout ── */
  .container { max-width: 1200px; margin: 0 auto; padding: 32px 24px; }

  /* ── Search bar ── */
  .search-wrap {
    background: var(--bg2);
    border: 1px solid var(--bdr);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 32px;
  }
  .search-title { font-size: 15px; font-weight: 600; color: var(--muted); margin-bottom: 14px; text-transform: uppercase; letter-spacing: 1px; }
  .search-row { display: flex; gap: 12px; }
  .search-input {
    flex: 1;
    background: var(--bg3);
    border: 1px solid var(--bdr);
    border-radius: 10px;
    padding: 14px 18px;
    color: var(--txt);
    font-size: 16px;
    outline: none;
    transition: border-color .2s;
  }
  .search-input:focus { border-color: var(--acc2); }
  .search-input::placeholder { color: var(--muted); }
  .btn-gen {
    background: linear-gradient(135deg, var(--acc), var(--acc2));
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 14px 28px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    white-space: nowrap;
    transition: opacity .2s, transform .1s;
  }
  .btn-gen:hover { opacity: .9; }
  .btn-gen:active { transform: scale(.97); }
  .btn-gen:disabled { opacity: .5; cursor: not-allowed; }

  /* Quick topic chips */
  .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
  .chip {
    background: var(--bg3);
    border: 1px solid var(--bdr);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 13px;
    color: var(--muted);
    cursor: pointer;
    transition: all .2s;
  }
  .chip:hover { border-color: var(--acc2); color: var(--acc2); }

  /* ── Progress log ── */
  #progress-wrap {
    background: var(--bg2);
    border: 1px solid var(--bdr);
    border-radius: var(--r);
    padding: 20px;
    margin-bottom: 28px;
    display: none;
  }
  #progress-wrap.active { display: block; }
  .log-title { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--muted); margin-bottom: 12px; }
  .log-line {
    font-size: 13px; line-height: 1.6; padding: 4px 0;
    border-left: 2px solid var(--bdr); padding-left: 12px; margin-bottom: 4px;
  }
  .log-line.status { border-color: var(--acc2); color: var(--acc2); }
  .log-line.error  { border-color: var(--red);  color: var(--red); }

  /* Spinner */
  .spinner {
    display: inline-block; width: 14px; height: 14px;
    border: 2px solid var(--bdr); border-top-color: var(--acc2);
    border-radius: 50%; animation: spin .7s linear infinite;
    margin-right: 8px; vertical-align: middle;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* ── Results grid ── */
  #results { display: none; }
  #results.active { display: block; }
  .results-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 20px;
  }
  .results-title { font-size: 20px; font-weight: 700; }
  .badge {
    background: var(--bg3); border: 1px solid var(--bdr);
    border-radius: 20px; padding: 4px 12px; font-size: 12px; color: var(--muted);
  }

  /* Slide carousel */
  .slides-row {
    display: flex; gap: 16px; overflow-x: auto;
    padding-bottom: 12px; scroll-snap-type: x mandatory;
  }
  .slides-row::-webkit-scrollbar { height: 4px; }
  .slides-row::-webkit-scrollbar-thumb { background: var(--bdr); border-radius: 2px; }
  .slide-card {
    flex: 0 0 340px; scroll-snap-align: start;
    border-radius: var(--r); overflow: hidden;
    border: 1px solid var(--bdr);
    position: relative; cursor: pointer;
    transition: transform .2s, box-shadow .2s;
  }
  .slide-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(124,58,237,.25); }
  .slide-card img { width: 100%; display: block; border-radius: var(--r); }
  .slide-num {
    position: absolute; top: 10px; right: 10px;
    background: rgba(0,0,0,.7); border-radius: 20px;
    padding: 3px 10px; font-size: 12px; font-weight: 600;
  }

  /* Caption box */
  .caption-box {
    background: var(--bg2); border: 1px solid var(--bdr);
    border-radius: var(--r); padding: 20px; margin-top: 20px;
  }
  .caption-label { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--muted); margin-bottom: 10px; }
  .caption-text { font-size: 14px; line-height: 1.7; color: var(--txt); white-space: pre-wrap; }

  /* Meta row */
  .meta-row { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
  .meta-tag {
    background: var(--bg3); border: 1px solid var(--bdr);
    border-radius: 8px; padding: 6px 14px; font-size: 13px; font-weight: 600;
  }
  .meta-tag.source { border-color: var(--acc); color: var(--acc2); }
  .meta-tag.cat    { border-color: var(--bdr); color: var(--txt); }

  /* Action buttons */
  .actions { display: flex; gap: 12px; margin-top: 20px; }
  .btn {
    flex: 1; padding: 13px; border-radius: 10px; border: 1px solid var(--bdr);
    font-size: 14px; font-weight: 600; cursor: pointer; text-align: center;
    transition: all .2s;
  }
  .btn-primary { background: linear-gradient(135deg,var(--acc),var(--acc2)); border: none; color: #fff; }
  .btn-primary:hover { opacity: .9; }
  .btn-outline { background: transparent; color: var(--txt); }
  .btn-outline:hover { border-color: var(--acc2); color: var(--acc2); }

  /* Lightbox */
  #lightbox {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,.92); z-index: 999;
    align-items: center; justify-content: center;
  }
  #lightbox.open { display: flex; }
  #lightbox img { max-width: 90vmin; max-height: 90vmin; border-radius: var(--r); }
  #lightbox-close {
    position: absolute; top: 24px; right: 32px;
    font-size: 32px; color: #fff; cursor: pointer; line-height: 1;
  }

  @media (max-width: 600px) {
    header { padding: 14px 16px; }
    .container { padding: 20px 12px; }
    .slide-card { flex: 0 0 80vw; }
  }
</style>
</head>
<body>

<header>
  <div class="logo">gesop<span>.ai</span></div>
  <div>
    <span class="status-dot"></span>
  </div>
</header>

<div class="container">

  <!-- Search -->
  <div class="search-wrap">
    <div class="search-title">Search Topic / Keywords</div>
    <div class="search-row">
      <input id="q" class="search-input" type="text"
             placeholder="e.g.  AI breakthroughs,  Gaza ceasefire,  Tesla earnings..."
             value="world news today"
             onkeydown="if(event.key==='Enter') generate()">
      <button class="btn-gen" id="gen-btn" onclick="generate()">Generate Slides</button>
    </div>
    <div class="chips">
      <div class="chip" onclick="setQ('AI and machine learning')">AI & Machine Learning</div>
      <div class="chip" onclick="setQ('breaking world news today')">Breaking World News</div>
      <div class="chip" onclick="setQ('tech startups funding')">Tech & Startups</div>
      <div class="chip" onclick="setQ('climate change environment')">Climate</div>
      <div class="chip" onclick="setQ('stock market economy')">Markets & Economy</div>
      <div class="chip" onclick="setQ('politics elections')">Politics</div>
      <div class="chip" onclick="setQ('space exploration NASA SpaceX')">Space</div>
      <div class="chip" onclick="setQ('health medical science')">Health & Science</div>
    </div>
  </div>

  <!-- Progress log -->
  <div id="progress-wrap">
    <div class="log-title"><span class="spinner" id="spinner"></span>Running Agent</div>
    <div id="log-lines"></div>
  </div>

  <!-- Results -->
  <div id="results">
    <div class="results-header">
      <div class="results-title" id="story-title">—</div>
    </div>
    <div class="meta-row" id="meta-row"></div>
    <div class="slides-row" id="slides-row"></div>
    <div class="caption-box">
      <div class="caption-label">Instagram Caption</div>
      <div class="caption-text" id="caption-text">—</div>
    </div>
    <div class="actions">
      <button class="btn btn-primary" onclick="downloadSlides()">Download Slides</button>
      <button class="btn btn-outline" onclick="copyCaption()">Copy Caption</button>
    </div>
  </div>

</div>

<!-- Lightbox -->
<div id="lightbox" onclick="closeLightbox()">
  <span id="lightbox-close" onclick="closeLightbox()">&times;</span>
  <img id="lightbox-img" src="" alt="">
</div>

<script>
let currentSlides = [];
let currentCaption = '';

function setQ(val) {
  document.getElementById('q').value = val;
  generate();
}

function addLog(text, cls = '') {
  const el = document.createElement('div');
  el.className = 'log-line ' + cls;
  el.textContent = text;
  document.getElementById('log-lines').appendChild(el);
  el.scrollIntoView({ behavior: 'smooth' });
}

function generate() {
  const q = document.getElementById('q').value.trim();
  if (!q) return;

  // Reset UI
  document.getElementById('log-lines').innerHTML = '';
  document.getElementById('progress-wrap').classList.add('active');
  document.getElementById('results').classList.remove('active');
  document.getElementById('slides-row').innerHTML = '';
  document.getElementById('gen-btn').disabled = true;
  document.getElementById('spinner').style.display = 'inline-block';
  currentSlides = [];

  const es = new EventSource('/generate?q=' + encodeURIComponent(q));

  es.onmessage = (e) => {
    const d = JSON.parse(e.data);

    if (d.type === 'status') {
      addLog(d.msg, 'status');
    } else if (d.type === 'log') {
      addLog(d.msg);
    } else if (d.type === 'slides' || d.type === 'done') {
      es.close();
      document.getElementById('spinner').style.display = 'none';
      document.getElementById('gen-btn').disabled = false;

      if (d.slides && d.slides.length) {
        showResults(d);
      }
    } else if (d.type === 'error') {
      es.close();
      addLog('Error: ' + d.msg, 'error');
      document.getElementById('spinner').style.display = 'none';
      document.getElementById('gen-btn').disabled = false;
    }
  };

  es.onerror = () => {
    es.close();
    document.getElementById('spinner').style.display = 'none';
    document.getElementById('gen-btn').disabled = false;
    addLog('Connection lost — try again.', 'error');
  };
}

function showResults(d) {
  document.getElementById('results').classList.add('active');
  document.getElementById('story-title').textContent = d.title || '';
  currentCaption = d.caption || '';
  document.getElementById('caption-text').textContent = currentCaption;

  // Meta tags
  const meta = document.getElementById('meta-row');
  meta.innerHTML = '';
  if (d.source)   meta.innerHTML += `<div class="meta-tag source">${d.source}</div>`;
  if (d.category) meta.innerHTML += `<div class="meta-tag cat">${d.category}</div>`;
  if (d.link && d.link !== 'https://actual-article-url.com') {
    meta.innerHTML += `<a class="meta-tag" href="${d.link}" target="_blank" rel="noopener" style="border-color:#22c55e;color:#22c55e;text-decoration:none;">&#x1F517; Read Article</a>`;
  }

  // Slides
  const row = document.getElementById('slides-row');
  row.innerHTML = '';
  currentSlides = d.slides || [];
  currentSlides.forEach((b64, i) => {
    const card = document.createElement('div');
    card.className = 'slide-card';
    card.innerHTML = `
      <img src="data:image/png;base64,${b64}" alt="Slide ${i+1}"
           onclick="openLightbox(${i})">
      `;
    row.appendChild(card);
  });

  document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function openLightbox(i) {
  document.getElementById('lightbox-img').src = 'data:image/png;base64,' + currentSlides[i];
  document.getElementById('lightbox').classList.add('open');
}

function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(); });

function downloadSlides() {
  currentSlides.forEach((b64, i) => {
    const a = document.createElement('a');
    a.href = 'data:image/png;base64,' + b64;
    a.download = `slide_${i + 1}.png`;
    a.click();
  });
}

function copyCaption() {
  navigator.clipboard.writeText(currentCaption).then(() => {
    const btn = document.querySelector('.btn-outline');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy Caption', 2000);
  });
}

</script>
</body>
</html>"""


if __name__ == "__main__":
    print("\n🎨  GeSoP Dashboard")
    print("   Open → http://localhost:5055")
    print("   Using: Claude CLI (pure, no SDK keys needed)\n")
    app.run(host="0.0.0.0", port=5055, debug=False, threaded=True)
