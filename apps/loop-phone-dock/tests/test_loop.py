import json
import os
import sys
import unittest
from urllib.request import Request, urlopen

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dock.phone import Phone
from dock.planner import act


class LoopTest(unittest.TestCase):
    def test_read_model(self):
        phone = Phone()
        result = act(phone, "打开设置并读出型号")
        self.assertTrue(result["ok"])
        self.assertEqual(result["answer"], "LOOP-PHONE")
        self.assertEqual(result["steps"], ["settings", "about", "model"])

    def test_send_is_held(self):
        phone = Phone()
        act(phone, "打开值班群")
        phone.type_text("夜场热力偏冷")
        send = next(t for t in phone.targets() if t.id == "send")
        out = phone.tap(send.x + 4, send.y + 4)
        self.assertEqual(out["last_result"], "held:夜场热力偏冷")
        self.assertTrue(any("held" in line for line in out["log"]))

    def test_miss(self):
        phone = Phone()
        out = phone.tap(1, 1)
        self.assertFalse(out["ok"])


class HttpTest(unittest.TestCase):
    def test_server_roundtrip(self):
        from dock.server import Handler, PHONE
        from http.server import ThreadingHTTPServer
        import threading

        PHONE.screen = "home"
        PHONE.last_result = ""
        PHONE.log.clear()
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            req = Request(
                f"http://127.0.0.1:{port}/act",
                data=json.dumps({"instruction": "打开设置并读出型号"}).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req) as resp:
                body = json.loads(resp.read().decode())
            self.assertEqual(body["answer"], "LOOP-PHONE")
        finally:
            server.shutdown()


if __name__ == "__main__":
    unittest.main()
