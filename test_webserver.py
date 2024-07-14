import unittest
import socket
import json
import base64
import time

class TestWebServerResponses(unittest.TestCase):
    HOST = '127.0.0.1'
    PORT = 8081

    def create_socket(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.HOST, self.PORT))
        return client_socket

    def send_request(self, client_socket, request):
        client_socket.sendall(request.encode())
        response = client_socket.recv(4096)
        return response.decode()
    
    def send_streaming_request(self, client_socket, request):
        client_socket.sendall(request.encode())
        response = ""
        while True:
            chunk = client_socket.recv(4096).decode()
            if not chunk:
                break
            response += chunk
        return response

    def create_get_request(self, path, auth=None):
        headers = "Connection: close\r\n"
        if auth:
            headers += f"Authorization: {auth}\r\n"
        request = f"GET {path} HTTP/1.1\r\nHost: {self.HOST}\r\n{headers}\r\n"
        return request

    def create_post_request(self, path, data):
        body = json.dumps(data)
        headers = f"Content-Type: application/json\r\nContent-Length: {len(body)}\r\nConnection: close\r\n"
        request = f"POST {path} HTTP/1.1\r\nHost: {self.HOST}\r\n{headers}\r\n{body}"
        return request

    def test_get_response(self):
        client_socket = self.create_socket()
        request = self.create_get_request('/sample_get')
        response = self.send_request(client_socket, request)
        self.assertIn("200 OK", response)
        self.assertIn("Content-Type: text/event-stream", response)
        client_socket.close()

    def test_post_response(self):
        client_socket = self.create_socket()
        request = self.create_post_request('/sample_post', {"key": "value"})
        response = self.send_request(client_socket, request)          
        self.assertIn("200 OK", response)
        self.assertIn("This is a POST response", response)
        client_socket.close()

    def test_get_wrong_auth(self):
        client_socket = self.create_socket()
        auth = "Basic "+base64.b64encode("Wrong:Auth".encode()).decode()
        request = self.create_get_request('/needs_auth', auth=auth)
        response = self.send_request(client_socket, request)
        self.assertIn("401 Unauthorized", response)
        client_socket.close()

    def test_get_correct_auth(self):
        client_socket = self.create_socket()
        auth = "Basic " + base64.b64encode(b'Hassan:Anzor').decode('utf-8')
        request = self.create_get_request('/needs_auth', auth=auth)
        response = self.send_request(client_socket, request)
        self.assertIn("200 OK", response)
        self.assertIn("This is a response for a request that needs authentication", response)
        client_socket.close()

    def test_gibberish_request(self):
        client_socket = self.create_socket()
        request = "GIBBERISH / HTTP/1.1\r\nHost: {self.HOST}\r\nConnection: close\r\n\r\n"
        response = self.send_request(client_socket, request)
        self.assertIn("400 Bad Request", response)
        client_socket.close()

    def test_streaming_endpoint(self):
        client_socket = self.create_socket()
        request = self.create_get_request('/sample_get')          
        response = self.send_streaming_request(client_socket, request)
        self.assertIn("200 OK", response)
        self.assertIn("Content-Type: text/event-stream", response)
        self.assertIn("The status line is the first line", response)
        client_socket.close()

    def test_rate_limiter(self):
        for i in range(20):  
            client_socket = self.create_socket()
            request = self.create_get_request('/sample_post')
            response = self.send_request(client_socket, request)
            if "429 Too Many Requests" in response:
                break
            client_socket.close()
            time.sleep(0.1)
        self.assertIn("429 Too Many Requests", response)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestWebServerResponses('test_get_response'))
    suite.addTest(TestWebServerResponses('test_post_response'))
    suite.addTest(TestWebServerResponses('test_get_wrong_auth'))
    suite.addTest(TestWebServerResponses('test_get_correct_auth'))
    suite.addTest(TestWebServerResponses('test_gibberish_request'))
    suite.addTest(TestWebServerResponses('test_streaming_endpoint'))
    suite.addTest(TestWebServerResponses('test_rate_limiter'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
