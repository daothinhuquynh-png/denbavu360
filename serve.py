#!/usr/bin/env python3
"""Server tĩnh cho tour + lưu tour.json khi chỉnh nút (POST /save)."""
import http.server, socketserver, json, os

PORT = 8099
HERE = os.path.dirname(os.path.abspath(__file__))
IMG_EXT = (".jpg", ".jpeg", ".png")

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HERE, **k)

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # Liệt kê ảnh 360 có trong panos/ để Trình dựng tour chọn
        if self.path.rstrip("/") == "/panos":
            d = os.path.join(HERE, "panos")
            files = sorted(f for f in os.listdir(d)
                           if f.lower().endswith(IMG_EXT)) if os.path.isdir(d) else []
            return self._json(200, files)
        return super().do_GET()

    def do_POST(self):
        if self.path.rstrip("/") == "/save":
            n = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(n)
            try:
                data = json.loads(body.decode("utf-8"))
                with open(os.path.join(HERE, "tour.json"), "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.send_response(200); self.end_headers()
                self.wfile.write(b'{"ok":true}')
                print("  ✔ da luu tour.json")
            except Exception as e:
                self.send_response(500); self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, *a):  # gọn log
        pass

class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    os.chdir(HERE)
    with Server(("", PORT), H) as httpd:
        print(f"Tour chay tai  http://localhost:{PORT}/   (Ctrl+C de dung)")
        httpd.serve_forever()
