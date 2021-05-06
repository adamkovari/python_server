import socket

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
from main import object_recognition
from datetime import datetime

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


    def do_POST(self):
        now = datetime.now().time()  # time object
        print("POST started =", now)
        #self.send_response(200)
        #self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_data_str = self.rfile.read(content_length)
        post_data_json = json.loads(post_data_str)
        image_string = object_recognition(post_data_json['img'])
        #print("POST: ")
        #print(post_data_json['img'])
        self.send_response(200)
        #self.send_header('Content-type', 'application/json')
        self.end_headers()
        #print(json.dumps({'img': image_string}))
        now = datetime.now().time()  # time object
        print("Post ended =", now)
        self.wfile.write(json.dumps({
            'img' : image_string
        }).encode())



private_key = generate_private_key("ca-private-key.pem", "secret_password")

generate_public_key(private_key, filename="ca-public-key.pem", country="HU", state="Pest", locality="Budapest", org="BME student project", hostname="hostname",)

server_private_key = generate_private_key("server-private-key.pem", "serverpassword")
print("server_private_key: ")
print(server_private_key)

generate_csr(server_private_key, filename="server-csr.pem", country="HU", state="Pest", locality="Budapest", org="BME student project",  hostname="hostname",)

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


httpd = http.server.HTTPServer(('192.168.1.66', 443), Handler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='server-public-key.pem', keyfile='server-private-key.pem', server_side=True)
print("Server running on https://localhost:" + str(8082))
httpd.serve_forever()

