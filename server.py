from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from getpass import getpass
from http import HTTPStatus
from https import generate_public_key, generate_private_key
from https import generate_csr
from https import sign_csr
from urllib.parse import urlparse
import http.server
import ssl
import json
import socketserver


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version
        }).encode())

private_key = generate_private_key("ca-private-key.pem", "secret_password")

generate_public_key(private_key, filename="ca-public-key.pem", country="HU", state="Pest", locality="Budapest", org="BME student project", hostname="192.168.1.66",)

server_private_key = generate_private_key("server-private-key.pem", "serverpassword")
print("server_private_key: ")
print(server_private_key)

generate_csr(server_private_key, filename="server-csr.pem", country="HU", state="Pest", locality="Budapest", org="BME student project", alt_names=["localhost"], hostname="192.168.1.66",)

csr_file = open("server-csr.pem", "rb")
csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())
print("csr: ")
print(csr)

ca_public_key_file = open("ca-public-key.pem", "rb")
ca_public_key = x509.load_pem_x509_certificate(ca_public_key_file.read(), default_backend())
print("ca_public_key: ")
print(ca_public_key)

ca_private_key_file = open("ca-private-key.pem", "rb")
ca_private_key = load_pem_private_key(ca_private_key_file.read(), "secret_password".encode("utf-8"), default_backend())

print("private_key: ")
print(private_key)


sign_csr(csr, ca_public_key, ca_private_key, "server-public-key.pem")
print("signed")

httpd = http.server.HTTPServer(('', 8000), Handler)
print("signed2")
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='ca-public-key.pem', keyfile='ca-private-key.pem', server_side=True)
print("Server running on https://0.0.0.0:" + str(8000))
httpd.serve_forever()