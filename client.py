import os
import requests


def get_secret_message():
    print("send message")
    response = requests.get("https://127.0.0.1:8000", verify="ca-public-key.pem")
    print("get response")
    print(f"The secret message is {response.text}")


if __name__ == "__main__":
    get_secret_message()