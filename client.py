# import os
# import requests
#
#
# def get_secret_message():
#     print("send message")
#     response = requests.get("https://127.0.0.1:8000", verify="ca-public-key.pem")
#     print("get response")
#     print(f"The secret message is {response.text}")
#
#
# if __name__ == "__main__":
#     get_secret_message()


# import socket
# import ssl
#
# hostname = 'example.host'
# # PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
# context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# context.load_verify_locations('ca-public-key.pem')
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
#     with context.wrap_socket(sock, server_hostname=hostname) as ssock:
#         print(ssock.version())
