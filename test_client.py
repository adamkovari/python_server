import socket
import ssl
import time

host_addr = '127.0.0.1'
host_port = 8082
server_sni_hostname = 'hostname'
server_cert = 'server-public-key.pem'
client_cert = 'ca-public-key.pem'
client_key = 'ca-private-key.pem'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key, password="secret_password")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect((host_addr, host_port))
print("SSL established. Peer: {}".format(conn.getpeercert()))

time.sleep(1)
print("Sending: 'Hello, world!")
conn.send(b"Hello, world!")

time.sleep(5)
print("Closing connection")
conn.close()