import socket
import json
import sys

def create_socket(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def send_request(client_socket, request):
    client_socket.sendall(request.encode())
    response = b''
    while True:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        response += chunk
        print(chunk.decode("utf-8"), end="")
    return response.decode()

def create_get_request(path):
    request = f"GET {path} HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
    return request

def create_post_request(path, data):
    body = json.dumps(data)
    headers = f"Content-Type: application/json\r\nContent-Length: {len(body)}"
    request = f"POST {path} HTTP/1.1\r\nHost: localhost\r\n{headers}\r\nConnection: close\r\n\r\n{body}"
    return request

def main():
    host = '127.0.0.1' 
    port = 8080  

    client_socket = create_socket(host, port)

    try:
        get_request = create_get_request('/sample_get')
        response = send_request(client_socket, get_request)
        print("GET /sample_get response:\n")
        print(response)

        client_socket = create_socket(host, port)

        get_request = create_get_request('/needs_auth')
        response = send_request(client_socket, get_request)
        print("GET /needs_auth response:\n")
        print(response)

        client_socket = create_socket(host, port)

        post_data = {"key": "value"}
        post_request = create_post_request('/sample_post', post_data)
        response = send_request(client_socket, post_request)
        print("POST /sample_post response:\n")
        print(response)
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
