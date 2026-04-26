"""
server.py  —  python server.py
Routes:
  /          -> index.html
  /admin     -> mapper.html
  everything else -> served as static files from this folder
"""
import http.server
import os

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        # Strip query string
        path = self.path.split('?')[0].rstrip('/')

        if path == '' or path == '/':
            self.path = '/index.html'
        elif path == '/admin':
            self.path = '/mapper.html'
        # All other paths (static files) pass through unchanged

        return super().do_GET()

    def log_message(self, fmt, *args):
        # Clean log output
        print(f"  {self.address_string()}  {fmt % args}")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with http.server.HTTPServer(('', PORT), Handler) as httpd:
        print(f"\n  Graveyard Map Server")
        print(f"  ─────────────────────────────")
        print(f"  Map   →  http://localhost:{PORT}/")
        print(f"  Admin →  http://localhost:{PORT}/admin")
        print(f"\n  Press Ctrl+C to stop.\n")
        httpd.serve_forever()
