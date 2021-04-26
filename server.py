import http.server, ssl
import socketserver
from urllib.parse import urlparse
from http import HTTPStatus
import json


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        print("self" + self)
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version
        }).encode())


httpd = socketserver.TCPServer(('', 8000), Handler)
httpd.serve_forever()
