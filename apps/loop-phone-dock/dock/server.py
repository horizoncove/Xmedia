"""HTTP surface: screen, tap, swipe, type, act. Default port 8787."""

from __future__ import annotations

import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from dock.phone import Phone
from dock.planner import act

UI = Path(__file__).resolve().parent.parent / "sim" / "index.html"

PHONE = Phone()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def _send(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/ui"):
            page = UI.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
            return
        if self.path == "/health":
            self._send(200, {"status": "ok", "device": "virtual-phone"})
            return
        if self.path == "/screen":
            self._send(200, PHONE.snapshot())
            return
        self._send(404, {"ok": False, "reason": "not-found"})

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode() or "{}")
        except json.JSONDecodeError:
            self._send(400, {"ok": False, "reason": "bad-json"})
            return

        if self.path == "/tap":
            self._send(200, PHONE.tap(int(data["x"]), int(data["y"])))
            return
        if self.path == "/swipe":
            self._send(
                200,
                PHONE.swipe(int(data["x1"]), int(data["y1"]), int(data["x2"]), int(data["y2"])),
            )
            return
        if self.path == "/type":
            self._send(200, PHONE.type_text(str(data.get("text", ""))))
            return
        if self.path == "/act":
            result = act(PHONE, str(data.get("instruction", "")))
            self._send(200 if result.get("ok") else 422, result)
            return
        if self.path == "/reset":
            PHONE.screen = "home"
            PHONE.typed = ""
            PHONE.last_result = ""
            PHONE.log.clear()
            self._send(200, PHONE.snapshot())
            return
        self._send(404, {"ok": False, "reason": "not-found"})


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8787), Handler)
    print("LOOP phone dock sim  http://127.0.0.1:8787/")
    server.serve_forever()


if __name__ == "__main__":
    main()
