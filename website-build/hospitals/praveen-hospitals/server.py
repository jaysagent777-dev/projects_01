"""Static server for the Praveen Hospitals redesign preview (Railway).

Public by default, so the hospital can open the link without a login. Every page carries a
"Redesign preview — not the live website" banner, and the server sends noindex headers plus a
Disallow-all robots.txt, so it doesn't show up on Google or get mistaken for the real site.
To put it back behind a login, set PREVIEW_REQUIRE_LOGIN=1 and PREVIEW_PASSWORD in Railway variables.
Only the built site files are served — never build.py, the _parts/_style sources, or this file.
"""
import base64
import hmac
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
USER = os.environ.get("PREVIEW_USER", "praveen")
PASSWORD = os.environ.get("PREVIEW_PASSWORD", "")
REQUIRE_LOGIN = os.environ.get("PREVIEW_REQUIRE_LOGIN", "") == "1"
ALLOWED = {".html", ".css", ".js", ".txt"}
PAGES = {"index", "about", "services", "specialities", "patient-care", "empanelments", "gallery", "contact"}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def end_headers(self):
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _authorized(self) -> bool:
        if not REQUIRE_LOGIN:
            return True
        if not PASSWORD:
            return False  # fail closed: never serve publicly without a password configured
        header = self.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            return False
        try:
            user, _, pw = base64.b64decode(header[6:]).decode().partition(":")
        except Exception:
            return False
        return hmac.compare_digest(user, USER) and hmac.compare_digest(pw, PASSWORD)

    def do_GET(self):
        path = self.path.split("?")[0].split("#")[0]
        if path == "/robots.txt":
            body = b"User-agent: *\nDisallow: /\n"
            self.send_response(200); self.send_header("Content-Type", "text/plain"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        if path == "/healthz":
            self.send_response(200); self.send_header("Content-Length", "2"); self.end_headers(); self.wfile.write(b"ok"); return
        if not self._authorized():
            body = b"Private preview. Ask for the login."
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Praveen Hospitals redesign preview", charset="UTF-8"')
            self.send_header("Content-Type", "text/plain"); self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body); return
        name = path.strip("/") or "index.html"
        if name.endswith(".html"):
            name_ok = name[:-5] in PAGES
        else:
            name_ok = name in {"styles.css", "site.js"}
        if "/" in name or not name_ok or Path(name).suffix not in ALLOWED:
            self.send_error(404); return
        self.path = "/" + name
        return super().do_GET()

    do_HEAD = do_GET

    def log_message(self, fmt, *args):
        print("%s %s" % (self.address_string(), fmt % args), flush=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    if REQUIRE_LOGIN and not PASSWORD:
        print("WARNING: PREVIEW_REQUIRE_LOGIN=1 but PREVIEW_PASSWORD not set — every request will be refused.", flush=True)
    print("Login required." if REQUIRE_LOGIN else "Public preview (no login).", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
