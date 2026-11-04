#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
VNSTOCK PRO TERMINAL — LOCALHOST SERVER & SSI FASTCONNECT API RELAY
===============================================================================
- Phục vụ Web App TradingView & Market Heatmap tại: http://localhost:8080
- Tự động đọc thông tin xác thực SSI FastConnect từ file `.env` (bảo mật khóa
  API khi đăng dự án lên GitHub Public phục vụ CV / Portfolio).
- Cung cấp Reverse Proxy chống lỗi CORS tại `/api/v2/Market/*`.
===============================================================================
"""

import os
import json
import ssl
import urllib.request
import urllib.error
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


def load_dotenv(dotenv_path=".env"):
    """Đọc biến môi trường từ file .env mà không cần cài thêm thư viện ngoài."""
    if not os.path.exists(dotenv_path):
        return
    with open(dotenv_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


load_dotenv()

HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8080"))

SSI_CONFIG = {
    "base_url": os.environ.get("SSI_BASE_URL", "https://fc-data.ssi.com.vn/api/v2/Market"),
    "consumerID": os.environ.get("SSI_CONSUMER_ID", ""),
    "consumerSecret": os.environ.get("SSI_CONSUMER_SECRET", ""),
    "privateKey": os.environ.get("SSI_PRIVATE_KEY", ""),
}

CACHED_ACCESS_TOKEN = None


class VNStockPortfolioHandler(SimpleHTTPRequestHandler):
    """HTTP Request Handler phục vụ Web App và chuyển tiếp SSI FastConnect API."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, Accept")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.path = "/index.html"
            return super().do_GET()

        # Endpoint nội bộ trả cấu hình từ file .env cho giao diện localhost
        if self.path == "/api/local-config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            payload = {
                "consumerID": SSI_CONFIG["consumerID"],
                "consumerSecret": SSI_CONFIG["consumerSecret"],
                "privateKey": SSI_CONFIG["privateKey"],
                "hasEnv": bool(SSI_CONFIG["consumerID"]),
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        if self.path.startswith("/api/v2/Market/"):
            target_url = "https://fc-data.ssi.com.vn" + self.path
            auth_header = self.headers.get("Authorization")
            if not auth_header and CACHED_ACCESS_TOKEN:
                auth_header = f"Bearer {CACHED_ACCESS_TOKEN}"

            headers = {
                "Accept": "application/json",
                "User-Agent": "VNStockPro-FastConnect-Client/2.0",
            }
            if auth_header:
                headers["Authorization"] = auth_header

            try:
                req = urllib.request.Request(target_url, headers=headers, method="GET")
                ctx = ssl.create_default_context()
                with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                    body = resp.read()
                    self.send_response(resp.status)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(body)
            except urllib.error.HTTPError as e:
                err_body = e.read()
                self.send_response(e.code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(err_body or json.dumps({"status": e.code, "message": str(e)}).encode("utf-8"))
            except Exception as ex:
                self.send_response(502)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": 502, "message": str(ex)}).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/v2/Market/AccessToken"):
            content_len = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_len) if content_len > 0 else b"{}"
            try:
                body_json = json.loads(raw_body.decode("utf-8") or "{}")
            except Exception:
                body_json = {}

            # Nếu client chưa truyền key thì tự động lấy từ .env
            if not body_json.get("consumerID") or "FROM_ENV" in str(body_json.get("consumerID", "")):
                body_json["consumerID"] = SSI_CONFIG["consumerID"]
                body_json["consumerSecret"] = SSI_CONFIG["consumerSecret"]

            target_url = "https://fc-data.ssi.com.vn/api/v2/Market/AccessToken"
            try:
                req = urllib.request.Request(
                    target_url,
                    data=json.dumps(body_json).encode("utf-8"),
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "VNStockPro-FastConnect-Client/2.0",
                    },
                    method="POST",
                )
                ctx = ssl.create_default_context()
                with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                    body = resp.read()
                    try:
                        parsed = json.loads(body.decode("utf-8"))
                        tok = parsed.get("data", {}).get("accessToken")
                        if tok:
                            global CACHED_ACCESS_TOKEN
                            CACHED_ACCESS_TOKEN = tok
                    except Exception:
                        pass
                    self.send_response(resp.status)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(body)
            except Exception as ex:
                self.send_response(502)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": 502, "message": str(ex)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    server = ThreadingHTTPServer((HOST, PORT), VNStockPortfolioHandler)
    url = f"http://localhost:{PORT}"
    print("=" * 72)
    print("🚀 VNSTOCK PRO TERMINAL — LOCALHOST SERVER ĐÃ KHỞI ĐỘNG!")
    print(f"👉 Địa chỉ Web App Dashboard : {url}")
    print(f"👉 Trạng thái khóa .env SSI  : {'ĐÃ NẠP AN TOÀN' if SSI_CONFIG['consumerID'] else 'CHƯA CẤU HÌNH'}")
    print("👉 Nhấn Ctrl + C để dừng server.")
    print("=" * 72)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Đã dừng máy chủ Localhost.")
        server.server_close()


if __name__ == "__main__":
    main()
