#!/usr/bin/env python3
"""Loopback-only preview of the modified SmartBox page; device reads only."""
from __future__ import annotations

import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "web-ui"
PREVIEW_JS = r"""
window.onUpdate = window.onCommit = window.aa_update = function () {
  weui.alert('Lokale Vorschau: Diese Aktion ist hier gesperrt.');
};
window.addEventListener('DOMContentLoaded', function () {
  var note = document.createElement('aside');
  note.className = 'bh-preview-banner';
  note.textContent = 'LOKALE VORSCHAU · Noch nicht auf dem Adapter installiert. Einstellungen und Uploads sind gesperrt.';
  document.querySelector('.bh-header').insertAdjacentElement('afterend', note);
});
"""


class Preview(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI), **kwargs)

    def send_bytes(self, data: bytes, content_type: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path == "/cgi-bin/bh-diagnostics.cgi":
            return self.send_bytes(b'{"error":"Diagnostics require the installed device backend"}', "application/json", 503)
        if parsed.path == "/cgi-bin/index.cgi":
            params = parse_qs(parsed.query)
            if params != {"id": ["host"]}:
                return self.send_bytes(b'{"code":403,"msg":"Preview is read-only"}', "application/json", 403)
            try:
                request = Request(self.server.device + "/cgi-bin/index.cgi?id=host", headers={"Accept-Language": "de-DE"})
                with urlopen(request, timeout=5) as response:
                    data = response.read(128 * 1024)
                json.loads(data)
                self.server.last_source = "live-device"
            except (URLError, TimeoutError, ValueError, OSError):
                data = (ROOT / "evidence/logs/2026-10-25-strict-validated/host.json").read_bytes()
                self.server.last_source = "archived-device-snapshot"
            return self.send_bytes(data, "application/json; charset=utf-8")
        if parsed.path == "/preview-mode.js":
            return self.send_bytes(PREVIEW_JS.encode(), "application/javascript; charset=utf-8")
        if parsed.path == "/preview-info":
            data = json.dumps({"preview": True, "device_modified": False, "write_proxy": False,
                               "status_source": self.server.last_source}).encode()
            return self.send_bytes(data, "application/json")
        if parsed.path in ("/", "/index.html"):
            page = (UI / "index.html").read_text(encoding="utf-8")
            page = page.replace("</body>", '<script src="/preview-mode.js"></script></body>')
            return self.send_bytes(page.encode(), "text/html; charset=utf-8")
        return super().do_GET()

    def do_POST(self):
        self.send_bytes(b'{"code":403,"msg":"Uploads disabled in preview"}', "application/json", 403)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8354)
    parser.add_argument("--device", default="http://192.168.1.101")
    args = parser.parse_args()
    device = urlsplit(args.device)
    if device.scheme != "http" or device.hostname != "192.168.1.101" or device.port not in (None, 80):
        parser.error("only the identified SmartBox HTTP endpoint is supported")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Preview)
    server.device = args.device.rstrip("/")
    server.last_source = "not-yet-read"
    print(f"SmartBox UI preview: http://127.0.0.1:{args.port} (read-only; no device deployment)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
