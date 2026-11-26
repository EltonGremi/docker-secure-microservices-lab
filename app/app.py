import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

START_TIME = time.time()
REQUEST_COUNT = 0


class MicroserviceHandler(BaseHTTPRequestHandler):
    server_version = "InternalAPI/1.0"
    sys_version = ""

    def _send_json(self, status_code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, status_code: int, content_type: str, text: str) -> None:
        body = text.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        global REQUEST_COUNT
        REQUEST_COUNT += 1
        uptime = round(time.time() - START_TIME, 2)

        if self.path == "/health":
            self._send_json(200, {"status": "healthy", "uptime_seconds": uptime})
        elif self.path == "/status":
            self._send_json(
                200,
                {
                    "service": "lab-microservice-api",
                    "status": "operational",
                    "uptime_seconds": uptime,
                    "requests_served": REQUEST_COUNT,
                },
            )
        elif self.path == "/metrics":
            metrics = (
                "# HELP lab_http_requests_total Total HTTP requests handled by the microservice.\n"
                "# TYPE lab_http_requests_total counter\n"
                f"lab_http_requests_total {REQUEST_COUNT}\n"
                "# HELP lab_service_uptime_seconds Service uptime in seconds.\n"
                "# TYPE lab_service_uptime_seconds gauge\n"
                f"lab_service_uptime_seconds {uptime}\n"
            )
            self._send_text(200, "text/plain; version=0.0.4; charset=utf-8", metrics)
        else:
            self._send_json(404, {"error": "not_found"})

    def log_message(self, format: str, *args) -> None:
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8000), MicroserviceHandler)
    server.serve_forever()
