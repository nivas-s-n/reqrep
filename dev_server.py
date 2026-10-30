import http.server
import socketserver
import os
import urllib.parse

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Parse path
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # If root, serve index.html
        if path == '/':
            self.path = '/index.html'
            if parsed_url.query:
                self.path += '?' + parsed_url.query
        else:
            # Check if file exists without extension
            file_path = os.path.join(DIRECTORY, path.lstrip('/'))
            if not os.path.exists(file_path):
                # Try with .html extension
                if os.path.exists(file_path + '.html'):
                    self.path = path + '.html'
                    if parsed_url.query:
                        self.path += '?' + parsed_url.query

        return super().do_GET()

if __name__ == '__main__':
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"=====================================================")
        print(f" DeG Data Purity Portal running locally at:")
        print(f" -> http://localhost:{PORT}/login")
        print(f" -> http://localhost:{PORT}/index")
        print(f" -> http://localhost:{PORT}/form")
        print(f"=====================================================")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
