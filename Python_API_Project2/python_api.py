#!/usr/bin/env python3

import http.server
import socketserver
import base64
import json
import pwd
import grp

# The API only listens on localhost, port 3000
HOST = "0.0.0.0"
PORT = 3000

# Required credentials
AUTH_USER = "test"
AUTH_PASS = "abcABC123456"


class APIHandler(http.server.SimpleHTTPRequestHandler):
    """
    Very small HTTP API that exposes two POST endpoints:
      /api/users
      /api/groups

    The API requires Basic Auth and returns JSON.
    """

    def do_POST(self):
        # Check Basic Auth first
        auth_header = self.headers.get("Authorization")
        if not auth_header or not self._check_auth(auth_header):
            self._send_unauthorized()
            return

        # Route the request
        if self.path == "/api/users":
            self._send_users()
        elif self.path == "/api/groups":
            self._send_groups()
        else:
            self.send_response(404)
            self.end_headers()

    def _check_auth(self, header):
        """Validate the Basic Auth header."""
        try:
            parts = header.split(" ")
            if len(parts) != 2:
                return False

            encoded = parts[1]
            decoded = base64.b64decode(encoded).decode("utf-8")

            if ":" not in decoded:
                return False

            username, password = decoded.split(":", 1)
            return username == AUTH_USER and password == AUTH_PASS
        except Exception:
            return False

    def _send_unauthorized(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="API"')
        self.end_headers()

    def _send_users(self):
        """Return system users in the required numbered JSON format."""
        users = pwd.getpwall()
        data = {str(i): u.pw_name for i, u in enumerate(users)}
        self._send_json(data)

    def _send_groups(self):
        """Return system groups in the required numbered JSON format."""
        groups = grp.getgrall()
        data = {str(i): g.gr_name for i, g in enumerate(groups)}
        self._send_json(data)

    def _send_json(self, data):
        """Helper to send JSON responses."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"Starting API on http://{HOST}:{PORT}")
    with socketserver.TCPServer((HOST, PORT), APIHandler) as httpd:
        httpd.serve_forever()

